# Scientific Report: Architecture Benchmarking of QAOA on Constrained Coupling Maps
**Problem Statement:** O1 — Max-Cut
**Track:** Quantum Optimization
**Benchmark Suite:** Qiskit Fall Fest 2026 Phase 1

---

## 0. Problem Statement Specification Sheet

| Specification Item | Participant Value |
|---|---|
| **PS Code** | O1 |
| **PS Name** | Max-Cut |
| **Track** | Quantum Optimization |
| **Input / Instance** | 5-node cyclic graph ($C_5$) with cross-edge $(0, 3)$ |
| **Core Algorithm** | Single-layer QAOA ($p=1$) with classical COBYLA variational optimization |
| **Required Output** | Optimal bitstring partition, expected cut $\langle C \rangle$, approximation ratio $r$ |
| **Primary Metric** | Max-Cut Approximation Ratio ($r = \langle C \rangle / C_{\text{max}}$) |
| **Reference / Classical Baseline** | Classical brute-force maximum cut = 5 |
| **Processor A Requirements** | 5 physical qubits, branched star coupling map (edges: `(0,1), (1,2), (1,3), (3,4)`) |
| **Processor B Requirements** | 9 physical qubits, heavy-hex-inspired 12-edge coupling map |
| **Key Architecture Metrics** | Transpiled depth, CX gate count, equivalent SWAPs, noise sensitivity |

---

## 1. Problem Formulation & Theoretical Reference

- **Problem Topology:** 5-node cyclic graph ($C_5$) augmented with cross-edge $(0, 3)$, yielding $\vert{}V\vert{}=5$ and $\vert{}E\vert{}=6$.
- **Classical Baseline:** Computed via brute-force partition evaluation; true maximum cut value = **5** (partition: `[1, 0, 1, 0, 0]`).
- **Algorithmic Formulation:** Single-layer QAOA ($p=1$). The cost Hamiltonian encodes each edge $(u, v) \in E$ into $ZZ$-interactions ($2 \times \text{CX}$ gates per edge), requiring an unconstrained logical circuit of **12 CX gates** and **Depth 18**.
- **Variational Optimization:** Variational angles were optimized using classical COBYLA on an unconstrained simulator, converging at $\gamma^* = 2.7916$ and $\beta^* = 0.3508$, yielding an ideal expectation cut of $\langle C \rangle = 4.104$ (Approximation Ratio $r = 0.821$).

---

## 2. Quantitative Architecture Benchmark (Processor A vs Processor B)

Simulations were executed with $N = 4096$ shots on `qiskit-aer` using a fixed seed (`seed=42`). The hardware noise model incorporates single-qubit depolarizing error ($0.1\%$), two-qubit CX depolarizing error ($1.0\%$), and readout error ($2.0\%$).

| Platform | Circuit Depth | 2Q Gates (CX) | Equivalent SWAPs | Expected Cut $\langle C \rangle$ | Approx Ratio ($r$) | Std Error ($\sigma_r$) |
|---|---|---|---|---|---|---|
| **Ideal Reference** | 18 | 12 | 0.00 | 4.104 | 0.821 | 0.0000 |
| **Processor A (5Q Branched)** | 30 | 18 | 2.00 | 3.919 | 0.784 | 0.0161 |
| **Processor B (9Q Heavy-Hex)** | 24 | 12 | 0.00 | 3.986 | 0.797 | 0.0157 |

*Routing Overhead Accounting:* SWAP operations unroll into $3 \times \text{CX}$ gates:

$$
\text{Equivalent SWAPs} = \frac{\text{Compiled CX} - \text{Logical CX}}{3}
$$

---

## 3. Transpiler Routing Analysis

We evaluated three distinct transpiler routing heuristics (`Basic`, `Lookahead`, `Sabre`) across both processor coupling maps:

| Processor | Routing Heuristic | Circuit Depth | 2Q Gates (CX) | Equivalent SWAPs |
|---|---|---|---|---|
| **Processor A (5Q Branched)** | Basic | 36 | 24 | 4.00 |
| **Processor A (5Q Branched)** | Lookahead | 30 | 18 | 2.00 |
| **Processor A (5Q Branched)** | Sabre | 30 | 18 | 2.00 |
| **Processor B (9Q Heavy-Hex)** | Basic | 24 | 12 | 0.00 |
| **Processor B (9Q Heavy-Hex)** | Lookahead | 24 | 12 | 0.00 |
| **Processor B (9Q Heavy-Hex)** | Sabre | 24 | 12 | 0.00 |

### Key Architectural Insights:

1. **Topology Embedding Advantage:** On Processor B, the 9-qubit heavy-hex architecture possesses subgraphs isomorphic to the target $C_5 + (0,3)$ problem instance. All three routing algorithms achieved **0.0 equivalent SWAPs**, executing the problem with exactly 12 CX gates and Depth 24.
2. **Routing Bottlenecks on Processor A:** In Processor A's 5-qubit topology, node 1 serves as a high-degree junction. Lookahead and Sabre successfully restricted overhead to 2 SWAPs (18 CX gates), whereas the greedy Basic heuristic introduced 4 SWAPs (24 CX gates).
3. **Fidelity Under Noise:** Because Processor B requires no additional routing CX gates, its final approximation ratio under depolarizing noise reached $r = 0.797$, outperforming Processor A ($r = 0.784$).

---

## 4. Noise Resilience & Error Scaling

Sweeping physical two-qubit gate error rates ($p_2 \in [0.2\%, 6.0\%]$) demonstrates that Processor B maintains higher solution fidelity across error regimes because zero routing overhead limits cumulative depolarizing channel exposure.

---

## 5. Artifacts & Reproducibility

- Machine-readable result tables: `results/tables/AB_comparison.csv`, `results/tables/routing_comparison.csv`, and `results/tables/noise_sweep.csv`.
- Generated visual dashboards: `results/figures/AB_performance.png`, `results/figures/architecture_tradeoffs.png`, and `results/figures/routing_comparison.png`.

---

## 6. Limitations & Technical Boundaries

1. **Algorithmic Depth:** The present evaluation benchmarked QAOA at depth $p=1$. While $p=1$ reveals clear initial routing overheads, higher circuit depths ($p \ge 2$) compound two-qubit gate depth, where multi-qubit crosstalk and coherent phase errors may behave non-linearly.
2. **Synthetic Noise Model:** Simulations employed an idealized depolarizing error channel and symmetric readout confusion matrix. Physical superconducting QPUs feature localized spectator-qubit crosstalk, anisotropic relaxation times, and frequency collisions that can shift optimal qubit placement beyond static coupling graph analysis.
3. **Finite Problem Scale:** A 5-node graph maps compactly onto 5-qubit and 9-qubit systems. In Phase 2, scaling to larger instances on larger architectures will test whether branched tree topologies introduce bottleneck congestion during multi-qubit routing passes.
