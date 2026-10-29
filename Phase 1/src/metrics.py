import math

def extract_circuit_metrics(compiled_circuit, logical_cx_count=12):
    ops = compiled_circuit.count_ops()
    two_q_gates = ['cx', 'cz', 'ecr', 'swap', 'rxx', 'ryy', 'rzz']
    two_q_count = sum(count for gate, count in ops.items() if gate.lower() in two_q_gates)
    
    # In Qiskit, each SWAP decomposes into 3 CX gates
    equivalent_swaps = max(0.0, (two_q_count - logical_cx_count) / 3.0)
    
    return {
        "depth": compiled_circuit.depth(),
        "num_qubits": compiled_circuit.num_qubits,
        "total_gates": sum(ops.values()),
        "two_qubit_gates": two_q_count,
        "equivalent_swaps": round(equivalent_swaps, 2),
        "operations": dict(ops)
    }

def calculate_approximation_ratio(counts, G, optimal_cut):
    total_shots = sum(counts.values())
    expected_cut = 0.0
    
    for bitstring, count in counts.items():
        bits = [int(b) for b in reversed(bitstring)]
        cut = sum(1 for u, v in G.edges() if bits[u] != bits[v])
        expected_cut += cut * (count / total_shots)
        
    approx_ratio = expected_cut / optimal_cut if optimal_cut > 0 else 0.0
    # Standard error of the mean cut estimate
    variance = sum(((sum(1 for u, v in G.edges() if [int(b) for b in reversed(bitstring)][u] != [int(b) for b in reversed(bitstring)][v]) - expected_cut) ** 2) * (count / total_shots) for bitstring, count in counts.items())
    standard_error = math.sqrt(variance / total_shots)
    
    return expected_cut, approx_ratio, standard_error