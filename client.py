import os
import sys
import socket
from dotenv import load_dotenv
import networkx as nx
from visualize import visualize  # helper to draw the graph

# -----------------------------
# 1. Load server configuration
# -----------------------------
# We don't hardcode IP/Port. Instead, we load them from a .env file.
# This makes the client portable and secure.
load_dotenv()
SERVER_IP = os.getenv("SERVER_IP")
SERVER_PORT = os.getenv("SERVER_PORT")

# If config is missing, stop early with a clear error.
if not SERVER_IP or not SERVER_PORT:
    print("SERVER_IP and SERVER_PORT must be set", file=sys.stderr)
    sys.exit(1)

SERVER_PORT = int(SERVER_PORT)


# -----------------------------
# 2. Helper: receive LF-terminated lines
# -----------------------------
def recv_lines(sock):
    """
    Read response lines from server until a newline is found.
    - We buffer chunks until we see '\n'
    - Then split into clean strings
    """
    buffer = b""
    sock.settimeout(5.0)

    while True:
        chunk = sock.recv(1024)
        if not chunk:  # connection closed
            break
        buffer += chunk
        if b"\n" in buffer:  # stop once newline arrives
            break

    # Decode bytes → str, strip whitespace, ignore empty lines
    return [line.decode().strip() for line in buffer.split(b"\n") if line.strip()]


# -----------------------------
# 3. Node class: represent states
# -----------------------------
class Node:
    """
    Each state in the machine is represented as a Node.
    - name: state label (A, B, C, ... Z)
    - action_counter: how many actions we've tried from this node
    - entry_list: sequence of actions to reach this node
    - exit_list: sequence of actions to leave this node back to Z
    """
    def __init__(self, name):
        self.name = name
        self.action_counter = 1
        self.entry_list = []
        self.exit_list = []


# -----------------------------
# 4. Reset helpers
# -----------------------------
def reset_server_state_to_z(sock, from_node):
    """Reset server back to Z using the exit_list of a node."""
    for _, action in from_node.exit_list:
        sock.sendall(f"{action}\n".encode())
        recv_lines(sock)


def reset_server_state_to_node(sock, to_node):
    """Reset server forward to a given node using its entry_list."""
    for _, action in to_node.entry_list:
        sock.sendall(f"{action}\n".encode())
        recv_lines(sock)


# -----------------------------
# 5. DFS exploration
# -----------------------------
def dfs_recursive(graph, sock, node, node_map=None, path_list=None):
    """
    Depth-first search through the state machine.
    - Sends actions (1,2,3) from a node
    - Records transitions in the graph
    - Tracks shortest entry/exit paths
    """
    if node_map is None:
        node_map = {}
    if path_list is None:
        path_list = []

    action = node.action_counter

    # Case 1: exhausted actions → reset to Z
    if action > 3:
        reset_server_state_to_z(sock, node)
        next_node_name = "Z"
        path_list += node.exit_list

    # Case 2: still have actions → send next one
    else:
        node.action_counter += 1
        sock.sendall(f"{action}\n".encode())
        lines = recv_lines(sock)
        next_node_name = lines[0]

        # Deduplicate edges: merge labels if edge already exists
        if graph.has_edge(node.name, next_node_name):
            existing_label = graph[node.name][next_node_name]["label"]
            graph[node.name][next_node_name]["label"] = f"{existing_label}, {action}"
        else:
            graph.add_edge(node.name, next_node_name, label=str(action))

        print(f"[Transition] {node.name} --({action})--> {next_node_name}")

    # If we hit Z, update exit paths and stop recursion
    if next_node_name == "Z":
        graph.add_edge("Z", "A", label="reset")
        for i, (node_name, action) in enumerate(path_list):
            new_list = list(path_list[i:])
            old_list = node_map[node_name].exit_list
            if not old_list or len(old_list) > len(new_list):
                node_map[node_name].exit_list = new_list
        return node_map

    # Otherwise, continue exploring
    next_node = node_map.get(next_node_name, Node(next_node_name))
    node_map[next_node_name] = next_node

    path_list.append((node.name, action))

    # Update entry path if shorter
    if not next_node.entry_list or len(path_list) < len(next_node.entry_list):
        next_node.entry_list = list(path_list)

    return dfs_recursive(graph, sock, next_node, node_map, path_list)


# -----------------------------
# 6. Halt condition
# -----------------------------
def should_halt(node_map):
    """Return a node that still has unexplored actions, or None if done."""
    for node in node_map.values():
        if node.action_counter < 4:
            return node
    return None


# -----------------------------
# 7. Main client runner
# -----------------------------
def run_client():
    """Connect to server, explore all states, and build graph."""
    graph = nx.DiGraph()  # use DiGraph to avoid duplicate edges

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_IP, SERVER_PORT))

        # First state (always A)
        _ = recv_lines(sock)
        start_node = Node("A")
        node_map = {"A": start_node}

        # Explore until all nodes exhausted
        while (node := should_halt(node_map)) is not None:
            reset_server_state_to_node(sock, node)
            node_map = dfs_recursive(graph, sock, node, node_map, node.entry_list)

        # Clean summary of all states
        print("\n=== State Machine Summary ===")
        for key, node in node_map.items():
            entry = " → ".join([f"{src}({act})" for src, act in node.entry_list]) or "-"
            exit_ = " → ".join([f"{src}({act})" for src, act in node.exit_list]) or "-"
            print(f"State {key}:")
            print(f"  Actions tried: {node.action_counter - 1}/3")
            print(f"  Entry path : {entry}")
            print(f"  Exit path  : {exit_}\n")

        print(f"Total states discovered: {len(node_map)}")

    return graph


# -----------------------------
# 8. Entry point
# -----------------------------
if __name__ == "__main__":
    try:
        state_graph = run_client()
        visualize(state_graph)  # draw diagram to images/state_machine.png
    except KeyboardInterrupt:
        print("\nStopped by user. Exiting gracefully.")
