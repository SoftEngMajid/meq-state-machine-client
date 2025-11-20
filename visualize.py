import os
import networkx as nx

def visualize(graph, output_path="images/state_machine.png"):
    """
    Render the state machine graph using Graphviz with clean layout.
    - Deduplicated edges
    - Left-to-right layout
    - Rounded, filled nodes
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Convert to Graphviz AGraph
    a = nx.nx_agraph.to_agraph(graph)

    # Graph-level styling
    a.graph_attr.update(rankdir="LR", splines="true", overlap="false")

    # Node styling
    a.node_attr.update(
        shape="box",
        style="rounded,filled",
        fillcolor="lightblue",
        fontname="Helvetica",
        fontsize="10"
    )

    # Edge styling
    a.edge_attr.update(
        fontname="Helvetica",
        fontsize="9",
        color="gray40"
    )

    # Layout and render
    a.layout(prog="dot")
    a.draw(output_path)
    print(f"State machine diagram saved to {output_path}")
