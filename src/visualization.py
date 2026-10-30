import json
import networkx as nx
import matplotlib.pyplot as plt


def plot_processor_topology(json_path, output_png, title):

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    G = nx.Graph()

    num_qubits = data["num_qubits"]
    coupling_map = data["coupling_map"]

    G.add_nodes_from(range(num_qubits))
    G.add_edges_from(coupling_map)

    fig, ax = plt.subplots(figsize=(12, 9))

    pos = nx.spring_layout(G, seed=42, k=1.5, iterations=100)

    degrees = dict(G.degree())

    node_colors = [
        "#2471A3" if degrees[node] > 1 else "#5DADE2"
        for node in G.nodes()
    ]

    nx.draw_networkx_edges(
        G, pos,
        ax=ax,
        width=2.5,
        edge_color="#7F8C8D",
        alpha=0.8
    )

    nx.draw_networkx_nodes(
        G, pos,
        ax=ax,
        node_color=node_colors,
        node_size=1800,
        edgecolors="#17202A",
        linewidths=2
    )

    nx.draw_networkx_labels(
        G, pos,
        ax=ax,
        labels={node: f"Qubit {node}" for node in G.nodes()},
        font_size=10,
        font_color="white",
        font_weight="bold"
    )

    edge_labels = {
        (u, v): "Connected"
        for u, v in G.edges()
    }

    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_labels,
        font_size=7,
        font_color="#34495E",
        ax=ax
    )

    legend_text = (
        f"PROCESSOR INFORMATION\n"
        f"Total qubits: {num_qubits}\n"
        f"Total connections: {G.number_of_edges()}\n"
        f"Maximum connections per qubit: {max(degrees.values())}\n"
        f"Average connections per qubit: "
        f"{sum(degrees.values()) / num_qubits:.2f}\n\n"
        f"HOW TO READ THIS GRAPH\n"
        f"Each circle represents one physical qubit.\n"
        f"Each line represents a direct connection.\n"
        f"Connected qubits can perform two-qubit operations.\n"
        f"Darker blue: Qubit with multiple connections.\n"
        f"Lighter blue: Qubit with one or fewer connections."
    )

    ax.text(
        1.03, 0.5,
        legend_text,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="center",
        bbox=dict(
            boxstyle="round,pad=0.8",
            facecolor="#F4F6F7",
            edgecolor="#AAB7B8"
        )
    )

    ax.set_title(
        f"{title}\nPhysical Qubit Connectivity Architecture",
        fontsize=17,
        fontweight="bold",
        pad=20
    )

    ax.axis("off")

    plt.tight_layout()
    plt.savefig(output_png, dpi=300, bbox_inches="tight")
    plt.close()
