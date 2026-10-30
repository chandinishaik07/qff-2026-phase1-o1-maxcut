import json
import os
import networkx as nx
import matplotlib.pyplot as plt

os.makedirs("processors", exist_ok=True)
os.makedirs("results/figures", exist_ok=True)
os.makedirs("results/tables", exist_ok=True)


def load_json(path):
    with open(path, "r", encoding="utf-8-sig")as file:
        return json.load(file)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def create_graph(num_qubits, edges):
    graph = nx.Graph()

    graph.add_nodes_from(range(num_qubits))

    for edge in edges:
        u, v = edge[0], edge[1]
        graph.add_edge(u, v)

    return graph


def draw_processor_graph(processor_name, processor_data):

    num_qubits = processor_data["num_qubits"]
    edges = processor_data["coupling_map"]

    graph = create_graph(num_qubits, edges)

    degrees = dict(graph.degree())

    positions = nx.spring_layout(
        graph,
        seed=42,
        k=1.8,
        iterations=200
    )

    fig, ax = plt.subplots(figsize=(16, 11))

    nx.draw_networkx_edges(
        graph,
        positions,
        ax=ax,
        width=3,
        edge_color="#566573",
        alpha=0.9
    )

    nx.draw_networkx_nodes(
        graph,
        positions,
        ax=ax,
        node_size=2300,
        node_color=[
            "#2874A6" if degrees[node] > 1 else "#85C1E9"
            for node in graph.nodes()
        ],
        edgecolors="#17202A",
        linewidths=2
    )

    labels = {
        node: f"QUBIT {node}\nDegree: {degrees[node]}"
        for node in graph.nodes()
    }

    nx.draw_networkx_labels(
        graph,
        positions,
        labels=labels,
        ax=ax,
        font_size=9,
        font_weight="bold",
        font_color="white"
    )

    edge_labels = {
        (u, v): f"Q{u} ↔ Q{v}"
        for u, v in graph.edges()
    }

    nx.draw_networkx_edge_labels(
        graph,
        positions,
        edge_labels=edge_labels,
        ax=ax,
        font_size=8,
        font_color="#922B21",
        rotate=False,
        bbox=dict(
            facecolor="white",
            edgecolor="none",
            alpha=0.8
        )
    )

    total_edges = graph.number_of_edges()
    average_degree = (
        sum(degrees.values()) / num_qubits
        if num_qubits > 0 else 0
    )

    max_degree = max(degrees.values()) if degrees else 0

    connected = nx.is_connected(graph)

    information = (
        f"PROCESSOR SPECIFICATIONS\n"
        f"------------------------------\n"
        f"Processor: {processor_name}\n"
        f"Physical qubits: {num_qubits}\n"
        f"Direct connections: {total_edges}\n"
        f"Average degree: {average_degree:.2f}\n"
        f"Maximum degree: {max_degree}\n"
        f"Connected architecture: {'Yes' if connected else 'No'}\n\n"
        f"HOW TO READ THIS DIAGRAM\n"
        f"------------------------------\n"
        f"Each circle represents one physical qubit.\n"
        f"Qubit numbers identify individual qubits.\n"
        f"Degree indicates the number of direct\n"
        f"connections available to that qubit.\n"
        f"Each line represents a direct connection\n"
        f"between two physical qubits.\n\n"
        f"WHY CONNECTIONS MATTER\n"
        f"------------------------------\n"
        f"Two-qubit gates such as CX can operate\n"
        f"directly on connected qubit pairs.\n"
        f"Non-connected pairs may require routing\n"
        f"or SWAP operations.\n\n"
        f"NODE LEGEND\n"
        f"------------------------------\n"
        f"Dark blue: More than one connection\n"
        f"Light blue: One or zero connections\n"
        f"Red edge labels: Connected qubit pair"
    )

    ax.text(
        1.02,
        0.5,
        information,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="center",
        bbox=dict(
            boxstyle="round,pad=1",
            facecolor="#F2F4F4",
            edgecolor="#566573",
            linewidth=1.5
        )
    )

    ax.set_title(
        f"{processor_name}\n"
        f"Quantum Processor Connectivity Architecture",
        fontsize=19,
        fontweight="bold",
        pad=25
    )

    ax.text(
        0.5,
        -0.06,
        "Architecture diagram showing physical qubits "
        "and their direct connectivity.",
        transform=ax.transAxes,
        ha="center",
        fontsize=11
    )

    ax.axis("off")

    plt.tight_layout()

    output_path = (
        f"results/figures/{processor_name.lower().replace(' ', '_')}_topology.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
        facecolor="white"
    )

    plt.close()

    print(f"[SUCCESS] {processor_name} graph saved: {output_path}")


# --------------------------------------------------
# LOAD OFFICIAL INSTANCE DATA
# --------------------------------------------------

official_data = load_json("instances.json")

pso1 = official_data["PS-O1"]

weighted_edges = pso1["weighted_edges"]

problem_graph = create_graph(
    pso1["num_vertices"],
    weighted_edges
)

print("\nOFFICIAL PS-O1 GRAPH")
print("------------------------------")
print(f"Vertices: {problem_graph.number_of_nodes()}")
print(f"Edges: {problem_graph.number_of_edges()}")


# --------------------------------------------------
# LOAD PROCESSOR A
# --------------------------------------------------

processor_A = load_json("processors/processor_A.json")

if "coupling_map" not in processor_A:
    processor_A["coupling_map"] = [
        edge
        for u, v in processor_A["edges"]
        for edge in ([u, v], [v, u])
    ]

draw_processor_graph("Processor A", processor_A)


# --------------------------------------------------
# LOAD PROCESSOR B
# --------------------------------------------------

processor_B = load_json("processors/processor_B.json")

if "coupling_map" not in processor_B:
    processor_B["coupling_map"] = [
        edge
        for u, v in processor_B["edges"]
        for edge in ([u, v], [v, u])
    ]

draw_processor_graph("Processor B", processor_B)


# --------------------------------------------------
# GENERATE PROCESSOR D
# --------------------------------------------------

G = problem_graph.copy()

coupling_map_D = [
    edge
    for u, v in G.edges()
    for edge in ([u, v], [v, u])
]

processor_D = {
    "name": "Processor D",
    "team": "Team",
    "problem_statement": "PS-O1",
    "num_qubits": pso1["num_vertices"],
    "edges": [[u, v] for u, v in G.edges()],
    "coupling_map": sorted(coupling_map_D),
    "basis_gates": official_data["benchmark_settings"]["basis_gates"],
    "noise": {
        "model": "official",
        "p1": official_data["benchmark_settings"]["noise"]["p1_depolarizing"],
        "p2": official_data["benchmark_settings"]["noise"]["p2_depolarizing_cx"],
        "p_readout": official_data["benchmark_settings"]["noise"]["readout_bitflip"]
    },
    "design_rationale": (
        "Coupling map matches the six-vertex PS-O1 problem graph "
        "to eliminate routing overhead for its graph edges."
    )
}

save_json("processors/processor_D.json", processor_D)

print("\n[SUCCESS] Processor D JSON generated.")


# --------------------------------------------------
# GENERATE PROCESSOR D GRAPH
# --------------------------------------------------

draw_processor_graph("Processor D", processor_D)


# --------------------------------------------------
# FINAL SUMMARY
# --------------------------------------------------

print("\n====================================")
print("ALL PROCESSOR GRAPHS GENERATED")
print("====================================")

print("Processor A: results/figures/processor_a_topology.png")
print("Processor B: results/figures/processor_b_topology.png")
print("Processor D: results/figures/processor_d_topology.png")
