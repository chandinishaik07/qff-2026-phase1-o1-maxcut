# Scientific Report: Architecture Benchmarking of QAOA on Constrained Coupling Maps
**Problem Statement:** O1 — Max-Cut[cite: 15, 36]  
**Track:** Quantum Optimization[cite: 15, 36]  
**Benchmark Suite:** Qiskit Fall Fest 2026 Phase 1[cite: 1, 15]  

---

## 0. Problem Statement Specification Sheet
| Specification Item | Participant Value |
|---|---|
| **PS Code** | O1[cite: 15, 36] |
| **PS Name** | Max-Cut[cite: 15, 36] |
| **Track** | Quantum Optimization[cite: 15, 36] |
| **Input / Instance** | 5-node cyclic graph ($C_5$) with cross-edge $(0, 3)$[cite: 36] |
| **Core Algorithm** | Single-layer QAOA ($p=1$) with classical COBYLA variational optimization[cite: 36] |
| **Required Output** | Optimal bitstring partition, expected cut $\langle C \rangle$, approximation ratio $r$[cite: 36] |
| **Primary Metric** | Max-Cut Approximation Ratio ($r = \langle C \rangle / C_{\text{max}}$)[cite: 36] |
| **Reference / Classical Baseline** | Classical brute-force maximum cut = 5[cite: 36] |
| **Processor A Requirements** | 5 physical qubits, linear chain coupling map[cite: 4, 36] |
| **Processor B Requirements** | 7 physical qubits, heavy-hex-inspired branched coupling map[cite: 4, 36] |
| **Key Architecture Metrics** | Transpiled depth, CX gate count, equivalent SWAPs, noise sensitivity[cite: 10, 36] |

---

## 1. Problem Formulation & Theoretical Reference
- **Problem Topology:** 5-node cyclic graph ($C_5$) augmented with a cross-edge $(0, 3)$, yielding $\vert{}V\vert{}=5$ and $\vert{}E\vert{}=6$.
- **Classical Baseline:** Computed via brute-force partition evaluation; true maximum cut value = **5** (partition: `[1, 0, 1, 0, 0]`).
- **Algorithmic Formulation:** Single-layer QAOA ($p=1$). The cost Hamiltonian encodes each edge $(u, v) \in E$ into $ZZ$-interactions ($2 \times \text{CX}$ gates per edge), requiring an unconstrained logical circuit of **12 CX gates** and **Depth 18**.
- **Variational Optimization:** Variational angles were optimized using classical COBYLA on an unconstrained simulator, converging at $\gamma^* = 2.7916$ and $\beta^* = 0.3508$, yielding an ideal expectation cut of $\langle C \rangle = 4.104$ (Approximation Ratio $r = 0.821$).

---

## 2. Quantitative Architecture Benchmark (A vs B)
Simulations were executed with $N = 4096$ shots on `qiskit-aer` using a fixed seed (`seed=42`). The hardware noise model incorporates single-qubit depolarizing error ($0.1\%$), two-qubit CX depolarizing error ($1.0\%$), and readout error ($2.0\%$).

| Platform | Circuit Depth | 2Q Gates (CX) | Equivalent SWAPs | Expected Cut $\langle C \rangle$ | Approx Ratio ($r$) | Std Error ($\sigma_r$) |
|---|---|---|---|---|---|---|
| **Ideal Reference** | 18 | 12 | 0.00 | 4.104 | 0.821 | 0.0000 |
| **Processor A (5Q Line)** | 27 | 19 | 2.33 | 3.925 | 0.785 | 0.0161 |
| **Processor B (7Q Heavy-Hex)** | 30 | 18 | 2.00 | 3.940 | 0.788 | 0.0162 |

*Routing Overhead Accounting:* SWAP operations unroll into $3 \times \text{CX}$ gates:
$$\text{Equivalent SWAPs} = \frac{\text{Compiled CX} - \text{Logical CX}}{3}$$

---

## 3. Transpiler Routing Analysis
We evaluated three distinct transpiler routing heuristics (`Basic`, `Lookahead`, `Sabre`) across both processor coupling maps:

| Processor | Routing Heuristic | Circuit Depth | 2Q Gates (CX) | Equivalent SWAPs |
|---|---|---|---|---|
| **Processor A (5Q Line)** | Basic | 30 | 21 | 3.00 |
| **Processor A (5Q Line)** | Lookahead | 27 | 21 | 3.00 |
| **Processor A (5Q Line)** | Sabre | 27 | 19 | 2.33 |
| **Processor B (7Q Heavy-Hex)** | Basic | 28 | 16 | 1.33 |
| **Processor B (7Q Heavy-Hex)** | Lookahead | 30 | 18 | 2.00 |
| **Processor B (7Q Heavy-Hex)** | Sabre | 30 | 18 | 2.00 |

### Key Architectural Insights:
1. **Connectivity Advantage:** On the 7-qubit branched architecture (Processor B), `Basic` routing achieved the lowest overall two-qubit gate count (16 CX, 1.33 equivalent SWAPs), outperforming all configurations on Processor A (which required at least 19 CX gates).
2. **Algorithmic Heuristics:** Sabre routing achieved the best SWAP reduction on the linear topology (Processor A), lowering CX gate count from 21 down to 19 by optimizing forward and reverse placement passes.
3. **Critical Path vs. Gate Volume:** On Processor B, Lookahead and Sabre introduced 2 additional CX gates compared to Basic routing to satisfy layout lookahead constraints, resulting in a slightly higher critical-path depth (30 vs 28).

---

## 4. Noise Resilience & Error Scaling
Sweeping physical two-qubit gate error rates ($p_2 \in [0.2\%, 6.0\%]$) demonstrates that Processor B maintains higher solution fidelity across error regimes because lower two-qubit gate overhead directly reduces cumulative depolarizing channel exposure[cite: 2, 8, 12].

---

## 5. Artifacts & Reproducibility
- Machine-readable result tables: `results/tables/AB_comparison.csv`, `results/tables/routing_comparison.csv`, and `results/tables/noise_sweep.csv`[cite: 24, 25, 41].
- Generated visual dashboards: `results/figures/AB_performance.png`, `results/figures/architecture_tradeoffs.png`, and `results/figures/routing_comparison.png`[cite: 24, 25, 41].

---

## 6. Limitations & Technical Boundaries
1. **Algorithmic Depth:** The present evaluation benchmarked QAOA at depth $p=1$. While $p=1$ reveals clear initial routing overheads, higher circuit depths ($p \ge 2$) compound two-qubit gate depth, where multi-qubit crosstalk and coherent phase errors may behave non-linearly[cite: 10, 12].
2. **Synthetic Noise Model:** Simulations employed an idealized depolarizing error channel and symmetric readout confusion matrix[cite: 4, 32]. Physical superconducting QPUs feature localized spectator-qubit crosstalk, anisotropic relaxation times, and frequency collisions that can shift optimal qubit placement beyond static coupling graph analysis[cite: 3, 12].
3. **Finite Problem Scale:** A 5-node graph maps compactly onto 5-qubit and 7-qubit systems[cite: 4, 28]. In Phase 2, scaling to larger instances on Processors C and D will test whether branched tree topologies introduce bottleneck congestion during multi-qubit routing passes[cite: 4, 5, 9].