import networkx as nx
from qiskit import QuantumCircuit

def create_problem_graph():
    """5-node ring graph with a cross edge to induce routing."""
    G = nx.Graph()
    G.add_nodes_from(range(5))
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 3)]
    G.add_edges_from(edges)
    return G

def compute_classical_max_cut(G):
    """Brute force optimal cut for verification/baseline."""
    nodes = list(G.nodes())
    n = len(nodes)
    best_cut = 0
    best_partition = None
    
    for i in range(1 << n):
        partition = [(i >> j) & 1 for j in range(n)]
        cut = 0
        for u, v in G.edges():
            if partition[u] != partition[v]:
                cut += 1
        if cut > best_cut:
            best_cut = cut
            best_partition = partition
            
    return best_cut, best_partition

def build_qaoa_circuit(G, gamma=0.39, beta=0.78):
    """Build logical QAOA depth-1 circuit for Max-Cut."""
    n = G.number_of_nodes()
    qc = QuantumCircuit(n, n)
    
    # Initial Superposition
    qc.h(range(n))
    qc.barrier()
    
    # Cost Hamiltonian: exp(-i * gamma * Z_i * Z_j) for (i, j) in E
    for u, v in G.edges():
        qc.cx(u, v)
        qc.rz(2 * gamma, v)
        qc.cx(u, v)
    qc.barrier()
    
    # Mixer Hamiltonian: exp(-i * beta * X_i)
    for i in range(n):
        qc.rx(2 * beta, i)
    qc.barrier()
    
    qc.measure(range(n), range(n))
    return qc