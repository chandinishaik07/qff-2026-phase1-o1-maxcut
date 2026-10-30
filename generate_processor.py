import json
import os
import networkx as nx
import matplotlib.pyplot as plt

os.makedirs('processors', exist_ok=True)
os.makedirs('results/figures', exist_ok=True)
os.makedirs('results/tables', exist_ok=True)

# Load official instances.json
with open('instances.json', 'r') as f:
    data = json.load(f)

# Extract PS-O1 data
pso1 = data.get("PS-O1", data)
edges = pso1.get("edges", [])

G = nx.Graph()
for edge in edges:
    u, v, w = edge[0], edge[1], edge[2]
    G.add_edge(u, v, weight=w)

print(f"--- Graph Loaded: {G.number_of_nodes()} Nodes, {G.number_of_edges()} Edges ---")
for node, degree in G.degree():
    print(f"Vertex {node}: degree = {degree}")

# Build bidirectional coupling map for Processor D
coupling_map = []
for u, v, _ in G.edges(data=True):
    coupling_map.append([u, v])
    coupling_map.append([v, u])

processor_D_data = {
    "name": "Processor D",
    "team": "Team",
    "problem_statement": "PS-O1",
    "num_qubits": 6,
    "edges": [[u, v] for u, v, _ in G.edges(data=True)],
    "coupling_map": sorted(coupling_map),
    "basis_gates": ["rz", "sx", "x", "cx"],
    "noise": {
        "model": "official",
        "p1": 0.001,
        "p2": 0.005,
        "p_readout": 0.01
    },
    "design_rationale": "Coupling map perfectly matches the 6-vertex PS-O1 problem graph to eliminate routing overhead."
}

# Write Processor D JSON
with open('processors/processor_D.json', 'w') as f:
    json.dump(processor_D_data, f, indent=4)

print("\n[SUCCESS] processors/processor_D.json written with 6 qubits.")

# Generate and save topology figure
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(6, 5))
nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700)
nx.draw_networkx_labels(G, pos, font_weight='bold')
nx.draw_networkx_edges(G, pos, width=2)
edge_labels = {(u, v): f"{w}" for u, v, w in G.edges(data='weight', default=1)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("Processor D Topology (PS-O1, 6 Qubits)")
plt.tight_layout()
plt.savefig("results/figures/optimal_partition.png")
plt.close()
print("[SUCCESS] Topology figure saved to results/figures/optimal_partition.png")
