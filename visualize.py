import os
import networkx as nx
import matplotlib
matplotlib.use("Agg")  # use non-GUI backend (works on servers)
import matplotlib.pyplot as plt

def visualize(graph, outfile="images/state_machine.png"):
    """Draw the state machine graph and save as PNG."""
    # Make sure images/ folder exists
    os.makedirs(os.path.dirname(outfile), exist_ok=True)

    # Layout positions for nodes
    pos = nx.spring_layout(graph, seed=42)

    # Get labels for edges (actions 1,2,3)
    edge_labels = nx.get_edge_attributes(graph, "label")

    # Draw nodes and edges
    plt.figure(figsize=(14, 10))
    nx.draw(
        graph, pos,
        with_labels=True,
        node_color="#9ddcff",  # light blue hex color
        edge_color="#333333",
        node_size=1800,
        font_size=10,
        arrows=True,
        arrowsize=20,
    )

    # Draw edge labels (show action numbers)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)

    # Save the image
    plt.tight_layout()
    plt.savefig("images/state_machine.png", dpi=200)
    print(f"Saved visualization to {outfile}")
