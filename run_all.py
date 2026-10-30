import matplotlib
matplotlib.use("Agg")
import os, csv
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.optimize import minimize
from qiskit_aer import AerSimulator


from qff_phase2 import (
    PROCESSOR_A, PROCESSOR_B, load_processor, validate_processor_d,
    circuit_metrics, transpile_for, simulator, bell_experiment,
    counts_to_x, SHOTS, SEED
)
from src.qaoa_o1 import cut_weight, solve_classical_maxcut, build_qaoa_circuit, EDGES, NUM_QUBITS

os.makedirs("results/tables", exist_ok=True)
os.makedirs("results/figures", exist_ok=True)

print("--- 1. Validating Processor D ---")
D = load_processor("processors/processor_D.json")
errs = validate_processor_d(D, required_qubits=NUM_QUBITS)
assert len(errs) == 0, f"Processor D rule check failed: {errs}"
print("Processor D: PASSED")

print("--- 2. Objective 1: Bell-State Verification ---")
bell_rows = []
for pair in [(0, 2), (1, 2)]:
    for noisy in [False, True]:
        res = bell_experiment(D, physical_pair=pair, noisy=noisy)
        bell_rows.append(res)
        print(f"Pair {pair} (noisy={noisy}): F={res['fidelity']:.4f} +/- {res['fidelity_se']:.4f}")

with open("results/tables/bell.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=bell_rows[0].keys())
    writer.writeheader()
    writer.writerows(bell_rows)
print("Saved results/tables/bell.csv")

print("--- 3. Classical Optimum ---")
C_star, optimal_set, random_r, random_p_opt = solve_classical_maxcut()
print(f"C* = {C_star}")
print(f"Optimal Set: {optimal_set}")
print(f"Random Baseline -> r: {random_r:.4f}, P_opt: {random_p_opt:.4f}")

sample_sol = next(iter(optimal_set))
G = nx.Graph()
for u, v, w in EDGES:
    G.add_edge(u, v, weight=w)

colors = ['#1f77b4' if sample_sol[i] == 1 else '#ff7f0e' for i in G.nodes()]
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(6, 4))
nx.draw(G, pos, with_labels=True, node_color=colors, node_size=600, font_color='white')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title(f"PS-O1 Optimal Partition (C* = {C_star})")
plt.savefig("results/figures/optimal_partition.png")
plt.close()
print("Saved results/figures/optimal_partition.png")

print("--- 4. QAOA Parameter Optimization ---")
sim_ideal = AerSimulator(seed_simulator=SEED)

def cost_fn(angles):
    g, b = angles
    qc = build_qaoa_circuit(gamma=g, beta=b, measure=True)
    cnts = sim_ideal.run(qc, shots=SHOTS).result().get_counts()
    mean_val = sum(cut_weight(counts_to_x(k)) * v for k, v in cnts.items()) / SHOTS
    return -mean_val

runs = []
for seed in [0, 1, 2, 3, 4]:
    rng = np.random.default_rng(seed)
    guess = rng.uniform(0, np.pi, size=2)
    res = minimize(cost_fn, guess, method="COBYLA", options={"maxiter": 60})
    runs.append((res.x[0], res.x[1], -res.fun))
    print(f"Seed {seed}: gamma={res.x[0]:.4f}, beta={res.x[1]:.4f}, exp_cut={-res.fun:.4f}")

best_gamma, best_beta, best_score = max(runs, key=lambda x: x[2])
print(f"Selected Angles: gamma={best_gamma:.4f}, beta={best_beta:.4f}")

print("--- 5. Hardware Benchmarks ---")
qc_opt = build_qaoa_circuit(gamma=best_gamma, beta=best_beta, measure=True)
metrics_B = circuit_metrics(qc_opt, PROCESSOR_B)
metrics_D = circuit_metrics(qc_opt, D)

def evaluate(sim, tqc):
    cnts = sim.run(tqc, shots=SHOTS).result().get_counts()
    tot, opt_hits = 0, 0
    for k, v in cnts.items():
        x = counts_to_x(k)
        tot += cut_weight(x) * v
        if x in optimal_set:
            opt_hits += v
    return (tot / SHOTS) / C_star, opt_hits / SHOTS

t_B = transpile_for(qc_opt, PROCESSOR_B)
t_D = transpile_for(qc_opt, D)

r_B_id, p_B_id = evaluate(simulator(False), t_B)
r_B_ny, p_B_ny = evaluate(simulator(True, PROCESSOR_B), t_B)

r_D_id, p_D_id = evaluate(simulator(False), t_D)
r_D_ny, p_D_ny = evaluate(simulator(True, D), t_D)

print(f"Processor B Noisy: r={r_B_ny:.4f}, P_opt={p_B_ny:.4f}")
print(f"Processor D Noisy: r={r_D_ny:.4f}, P_opt={p_D_ny:.4f}")

print("--- 6. Exporting results/tables/results.csv ---")
csv_cols = [
    "problem_id", "processor", "condition", "executable",
    "logical_qubits", "physical_qubits", "logical_cx", "cx",
    "depth", "two_q_depth", "swaps", "cx_overhead", "shots",
    "quality_metric", "quality_value", "p_opt", "classical_optimum", "random_baseline"
]

rows = [
    {"problem_id": "PS-O1", "processor": "A", "condition": "ideal", "executable": "false",
     "logical_qubits": 6, "physical_qubits": 5, "classical_optimum": C_star, "random_baseline": f"{random_r:.4f}"},
    {"problem_id": "PS-O1", "processor": "A", "condition": "noisy", "executable": "false",
     "logical_qubits": 6, "physical_qubits": 5, "classical_optimum": C_star, "random_baseline": f"{random_r:.4f}"},

    {"problem_id": "PS-O1", "processor": "B", "condition": "ideal", "executable": "true",
     "logical_qubits": 6, "physical_qubits": 9, "logical_cx": metrics_B["logical_cx"], "cx": metrics_B["cx"],
     "depth": metrics_B["depth"], "two_q_depth": metrics_B["two_q_depth"], "swaps": metrics_B["swaps"],
     "cx_overhead": metrics_B["cx_overhead"], "shots": SHOTS, "quality_metric": "approx_ratio",
     "quality_value": f"{r_B_id:.4f}", "p_opt": f"{p_B_id:.4f}", "classical_optimum": C_star, "random_baseline": f"{random_r:.4f}"},
    {"problem_id": "PS-O1", "processor": "B", "condition": "noisy", "executable": "true",
     "logical_qubits": 6, "physical_qubits": 9, "logical_cx": metrics_B["logical_cx"], "cx": metrics_B["cx"],
     "depth": metrics_B["depth"], "two_q_depth": metrics_B["two_q_depth"], "swaps": metrics_B["swaps"],
     "cx_overhead": metrics_B["cx_overhead"], "shots": SHOTS, "quality_metric": "approx_ratio",
     "quality_value": f"{r_B_ny:.4f}", "p_opt": f"{p_B_ny:.4f}", "classical_optimum": C_star, "random_baseline": f"{random_r:.4f}"},

    {"problem_id": "PS-O1", "processor": "D", "condition": "ideal", "executable": "true",
     "logical_qubits": 6, "physical_qubits": 6, "logical_cx": metrics_D["logical_cx"], "cx": metrics_D["cx"],
     "depth": metrics_D["depth"], "two_q_depth": metrics_D["two_q_depth"], "swaps": metrics_D["swaps"],
     "cx_overhead": metrics_D["cx_overhead"], "shots": SHOTS, "quality_metric": "approx_ratio",
     "quality_value": f"{r_D_id:.4f}", "p_opt": f"{p_D_id:.4f}", "classical_optimum": C_star, "random_baseline": f"{random_r:.4f}"},
    {"problem_id": "PS-O1", "processor": "D", "condition": "noisy", "executable": "true",
     "logical_qubits": 6, "physical_qubits": 6, "logical_cx": metrics_D["logical_cx"], "cx": metrics_D["cx"],
     "depth": metrics_D["depth"], "two_q_depth": metrics_D["two_q_depth"], "swaps": metrics_D["swaps"],
     "cx_overhead": metrics_D["cx_overhead"], "shots": SHOTS, "quality_metric": "approx_ratio",
     "quality_value": f"{r_D_ny:.4f}", "p_opt": f"{p_D_ny:.4f}", "classical_optimum": C_star, "random_baseline": f"{random_r:.4f}"}
]

with open("results/tables/results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=csv_cols)
    writer.writeheader()
    writer.writerows(rows)
print("Saved results/tables/results.csv")
print("DONE! All deliverables produced.")
