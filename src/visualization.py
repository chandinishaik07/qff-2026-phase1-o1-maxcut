import json
import networkx as nx
import matplotlib.pyplot as plt

def plot_processor_topology(json_path, output_png, title):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    G = nx.Graph()
    G.add_nodes_from(range(data["num_qubits"]))
    G.add_edges_from(data["coupling_map"])
    plt.figure(figsize=(4, 3))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color="#3498db", node_size=600, font_color="white", font_weight="bold")
    plt.title(title)
    plt.savefig(output_png, bbox_inches='tight', dpi=200)
    plt.close()