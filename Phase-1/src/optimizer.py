import numpy as np
from scipy.optimize import minimize
from qiskit_aer import AerSimulator
from src.problem import build_qaoa_circuit
from src.metrics import calculate_approximation_ratio

def optimize_qaoa_angles(graph, max_cut_val):
    sim = AerSimulator()

    def cost_func(params):
        gamma, beta = params
        circuit = build_qaoa_circuit(graph, gamma=gamma, beta=beta)
        result = sim.run(circuit, shots=2048, seed_simulator=42).result()
        counts = result.get_counts()
        cut_val, _, _ = calculate_approximation_ratio(counts, graph, max_cut_val)
        return -cut_val

    init_angles = [0.5, 0.5]
    res = minimize(cost_func, init_angles, method='COBYLA', options={'maxiter': 30})

    opt_gamma, opt_beta = float(res.x[0]), float(res.x[1])
    optimal_cut = float(-res.fun)
    return opt_gamma, opt_beta, optimal_cut