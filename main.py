import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import json
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from qiskit_aer import AerSimulator

from src.problem import create_problem_graph, compute_classical_max_cut, build_qaoa_circuit
from src.metrics import extract_circuit_metrics, calculate_approximation_ratio
from src.benchmark import run_processor_benchmark
from src.optimizer import optimize_qaoa_angles
from src.routing_benchmark import evaluate_routing_methods
from src.noise_sweep import run_noise_sweep


def plot_graphs():
    configs = [
        ("Processor A", "processors/processor_A.json"),
        ("Processor B", "processors/processor_B.json")
    ]
    for name, path in configs:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        g = nx.Graph()
        g.add_nodes_from(range(data["num_qubits"]))
        g.add_edges_from(data["coupling_map"])
        
        plt.figure(figsize=(4, 3))
        pos = nx.spring_layout(g, seed=42)
        nx.draw(g, pos, with_labels=True, node_color="#3498db", node_size=600, font_color="white", font_weight="bold")
        plt.title(f"{name} Coupling Map")
        slug = name.replace(" ", "_").lower()
        plt.savefig(f"results/figures/{slug}_graph.png", bbox_inches='tight', dpi=200)
        plt.close()


def main():
    print("==================================================")
    print("  QISKIT FALL FEST 2026 - PHASE 1 FULL BENCHMARK  ")
    print("==================================================")
    
    # 1. Classical Baseline & Variational Parameter Optimization
    G = create_problem_graph()
    opt_cut, opt_part = compute_classical_max_cut(G)
    print(f"\n[1] Classical Max-Cut: {opt_cut} (Partition: {opt_part})")
    
    print("    Optimizing QAOA variational angles (COBYLA)...")
    opt_gamma, opt_beta, ideal_opt_cut = optimize_qaoa_angles(G, opt_cut)
    print(f"    Optimal Angles: gamma = {opt_gamma:.4f}, beta = {opt_beta:.4f}")
    
    logical_qc = build_qaoa_circuit(G, gamma=opt_gamma, beta=opt_beta)
    print(f"    Logical Circuit Depth: {logical_qc.depth()} | Logical CX: 12")
    
    plot_graphs()
    print("\n[2] Hardware coupling graphs saved to results/figures/")
    
    # 2. Processor A vs B Baseline Benchmark
    print("\n[3] Running Controlled A/B Benchmark...")
    proc_paths = ["processors/processor_A.json", "processors/processor_B.json"]
    base_results = [{
        "Stage": "Ideal Reference",
        "Depth": logical_qc.depth(),
        "2Q Gates": 12,
        "Equiv SWAPs": 0.0,
        "Expected Cut": round(ideal_opt_cut, 3),
        "Approx Ratio": round(ideal_opt_cut / opt_cut, 3),
        "Std Error": 0.0000
    }]
    
    for path in proc_paths:
        name, compiled, counts = run_processor_benchmark(logical_qc, path)
        metrics = extract_circuit_metrics(compiled, logical_cx_count=12)
        exp_cut, approx_ratio, std_err = calculate_approximation_ratio(counts, G, opt_cut)
        base_results.append({
            "Stage": name,
            "Depth": metrics["depth"],
            "2Q Gates": metrics["two_qubit_gates"],
            "Equiv SWAPs": metrics["equivalent_swaps"],
            "Expected Cut": round(exp_cut, 3),
            "Approx Ratio": round(approx_ratio, 3),
            "Std Error": round(std_err, 4)
        })
        
    df_base = pd.DataFrame(base_results)
    df_base.to_csv("results/tables/AB_comparison.csv", index=False)
    print(df_base.to_string(index=False))

    # 3. Transpiler Routing Benchmark
    print("\n[4] Benchmarking Transpiler Routing Methods (Basic vs Lookahead vs Sabre)...")
    routing_data = []
    for path in proc_paths:
        routing_data.extend(evaluate_routing_methods(logical_qc, path))
    df_routing = pd.DataFrame(routing_data)
    df_routing.to_csv("results/tables/routing_comparison.csv", index=False)
    print(df_routing.to_string(index=False))

    # 4. Noise Sensitivity Sweep
    print("\n[5] Executing 2-Qubit Gate Noise Degradation Sweep...")
    err_rates = [0.002, 0.005, 0.01, 0.02, 0.04, 0.06]
    _, r_A = run_noise_sweep(logical_qc, G, opt_cut, "processors/processor_A.json", err_rates)
    _, r_B = run_noise_sweep(logical_qc, G, opt_cut, "processors/processor_B.json", err_rates)
    
    df_noise = pd.DataFrame({
        "CX_Error_Rate": err_rates,
        "Ratio_Processor_A": r_A,
        "Ratio_Processor_B": r_B
    })
    df_noise.to_csv("results/tables/noise_sweep.csv", index=False)

    # 5. Visualizations
    print("\n[6] Rendering Visual Dashboards...")
    # Plot 1: Performance Bar Charts
    plt.figure(figsize=(9, 4))
    plt.subplot(1, 2, 1)
    plt.bar(df_base["Stage"], df_base["Depth"], color=['#95a5a6', '#e74c3c', '#2ecc71'])
    plt.title("Circuit Depth (Lower is Better)")
    plt.xticks(rotation=15, ha='right')

    plt.subplot(1, 2, 2)
    plt.bar(df_base["Stage"], df_base["Approx Ratio"], color=['#95a5a6', '#e74c3c', '#2ecc71'])
    plt.title("Approx Ratio (Higher is Better)")
    plt.ylim(0, 1.0)
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    plt.savefig("results/figures/AB_performance.png", dpi=300)
    plt.close()

    # Plot 2: Noise Degradation Sweep
    plt.figure(figsize=(6, 4))
    plt.plot(err_rates, r_A, 'o-', color='#e74c3c', label="Processor A (5Q Line)")
    plt.plot(err_rates, r_B, 's-', color='#2ecc71', label="Processor B (7Q Heavy-Hex)")
    plt.title("Noise Resilience: Approx Ratio vs 2Q Error")
    plt.xlabel("Physical CX Error Rate")
    plt.ylabel("Max-Cut Approx Ratio")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/figures/architecture_tradeoffs.png", dpi=300)
    plt.close()

    # Plot 3: Routing Comparison
    plt.figure(figsize=(7, 4))
    for proc in df_routing["Processor"].unique():
        sub = df_routing[df_routing["Processor"] == proc]
        plt.plot(sub["Routing Method"], sub["2Q Gates"], 'o-', label=proc)
    plt.title("Routing Algorithm vs 2Q Gate Count")
    plt.ylabel("Total 2-Qubit Gates")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig("results/figures/routing_comparison.png", dpi=300)
    plt.close()

    print("\n✓ Full benchmark completed! Check results/tables/ and results/figures/.")

if __name__ == "__main__":
    main()