import os
import socket
import sys
from dotenv import load_dotenv
import networkx as nx
from visualize import visualize  # draw the graph

# Load server details from environment
load_dotenv()
server_ip = os.getenv("SERVER_IP")
server_port = os.getenv("SERVER_PORT")

# Stop if env vars are missing
if not server_ip or not server_port:
    print("SERVER_IP and SERVER_PORT must be set", file=sys.stderr)
    sys.exit(1)

server_port = int(server_port)


def recv_lines(sock):
    """Read response lines from server until newline found."""
    buffer = b""
    sock.settimeout(5.0)

    while True:
        chunk = sock.recv(1024)
        if not chunk:
            break
        buffer += chunk
        if b"\n" in buffer:
            break

    # Split by LF and clean up
    lines = [line.decode().strip() for line in buffer.split(b"\n") if line.strip()]
    return lines


def run_client():
    """Connect to server, explore states, build graph."""
    graph = nx.DiGraph()
    discovered_states = set()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_ip, server_port))

        # First state (always A)
        lines = recv_lines(sock)
        current_state = lines[-1]
        print(f"Server: {current_state}")
        discovered_states.update(lines)

        to_explore = ["A"]

        while to_explore:
            state = to_explore.pop(0)

            # Try actions 1,2,3 from this state
            for action in ["1", "2", "3"]:
                sock.sendall((action + "\n").encode())
                lines = recv_lines(sock)

                for next_state in lines:
                    print(f"{state} --{action}--> {next_state}")
                    graph.add_edge(state, next_state, label=action)
                    discovered_states.add(next_state)

                current_state = lines[-1]
                if current_state not in to_explore and current_state != "Z":
                    to_explore.append(current_state)

            # Stop when all states mapped
            if len(discovered_states) >= 26 and all(
                st == "Z" or len(list(graph.out_edges(st))) >= 3 for st in discovered_states
            ):
                break

    return graph


if __name__ == "__main__":
    # Run client and draw the state machine with a clean exit if stopped by Mr.Ant
    try:
        state_graph = run_client()
        visualize(state_graph)
    except KeyboardInterrupt:
        print("\nStopped by user. Exiting gracefully.")
