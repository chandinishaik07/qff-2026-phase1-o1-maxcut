import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

EDGES = [
    (0, 2, 1), (0, 3, 4), (0, 4, 4),
    (1, 4, 3), (1, 5, 3), (2, 3, 5),
    (2, 4, 1), (3, 4, 4), (3, 5, 2)
]
NUM_QUBITS = 6

def cut_weight(x: tuple) -> float:
    val = 0
    for u, v, w in EDGES:
        val += w * (x[u] + x[v] - 2 * x[u] * x[v])
    return val

def solve_classical_maxcut():
    all_bitstrings = [tuple(int(b) for b in f"{i:06b}") for i in range(64)]
    cut_values = {bs: cut_weight(bs) for bs in all_bitstrings}
    c_star = max(cut_values.values())
    optimal_set = {bs for bs, val in cut_values.items() if val == c_star}
    random_r = float(np.mean(list(cut_values.values())) / c_star)
    random_p_opt = float(len(optimal_set) / 64.0)
    return c_star, optimal_set, random_r, random_p_opt

def build_qaoa_circuit(gamma=None, beta=None, measure=True):
    qc = QuantumCircuit(NUM_QUBITS)
    qc.h(range(NUM_QUBITS))
    
    g = Parameter("gamma") if gamma is None else gamma
    b = Parameter("beta") if beta is None else beta
    
    for u, v, w in EDGES:
        qc.cx(u, v)
        qc.rz(2 * g * w, v)
        qc.cx(u, v)
        
    for q in range(NUM_QUBITS):
        qc.rx(2 * b, q)
        
    if measure:
        qc.measure_all()
    return qc