# Qiskit Fall Fest 2026 — Phase 1: Architecture Benchmark
**Problem Statement:** O1 — Max-Cut  
**Track:** Quantum Optimization  
**Author / Team:** Shaik Chandini  
**Phase:** 1 (Online Qualification Stage)

---

## 1. Executive Summary
This project investigates the impact of physical qubit connectivity and transpiler routing on the execution of the Quantum Approximate Optimization Algorithm (QAOA, $p=1$) for the Max-Cut problem. We evaluate the exact same logical quantum circuit across two target hardware architectures:
- **Processor A:** 5-qubit linear chain topology ($\text{deg} \le 2$).
- **Processor B:** 7-qubit heavy-hex-inspired branching topology ($\text{deg} \le 3$).

Our empirical benchmark demonstrates that while both processors achieve comparable approximation ratios ($r \approx 0.785$ to $0.788$) under moderate depolarizing noise, **Processor B reduces two-qubit gate overhead by up to 23.8%** due to its alternative routing cycles, significantly reducing accumulation of multi-qubit physical noise channels.

---

## 2. Problem Formulation & Classical Baseline
- **Target Instance:** 5-node cyclic graph ($C_5$) with an internal cross edge $(0, 3)$, yielding $\vert{}V\vert{} = 5$ and $\vert{}E\vert{} = 6$.
- **Classical Brute-Force Baseline:** The exact maximum cut is **5** (partition: `[1, 0, 1, 0, 0]`).
- **Logical QAOA Circuit ($p=1$):**
  - Problem Hamiltonian: $H_C = \sum_{(u,v) \in E} \frac{1}{2} (I - Z_u Z_v)$ implemented using $2 \times \text{CX}$ gates per edge.
  - Mixer Hamiltonian: $H_M = \sum_{v \in V} X_v$ implemented via $R_X(2\beta)$.
  - **Logical Resource Footprint:** 12 CX gates, critical-path depth = 18.
- **Variational Optimization:** Angles were optimized classically via COBYLA on a noiseless statevector simulator, converging at $\gamma^* = 2.7916$ and $\beta^* = 0.3508$ with an ideal expectation cut of $\langle C \rangle = 4.104$ (Approximation Ratio $r = 0.821$).

---

## 3. Quantitative Results & Comparison

### A. Controlled Hardware Benchmark
Executed with $N = 4096$ shots on `qiskit-aer` using fixed seed (`seed=42`).  
Noise model: 1-qubit depolarizing ($0.1\%$), 2-qubit CX depolarizing ($1.0\%$), readout error ($2.0\%$).

| Architecture Stage | Circuit Depth | 2Q Gates (CX) | Equivalent SWAPs | Expected Cut $\langle C \rangle$ | Approx Ratio ($r$) | Std Error ($\sigma_r$) |
|---|---|---|---|---|---|---|
| **Ideal Reference** | 18 | 12 | 0.00 | 4.104 | 0.821 | 0.0000 |
| **Processor A (5Q Line)** | 27 | 19 | 2.33 | 3.925 | 0.785 | 0.0161 |
| **Processor B (7Q Heavy-Hex)** | 30 | 18 | 2.00 | 3.940 | 0.788 | 0.0162 |

$$\text{Equivalent SWAPs} = \frac{\text{Compiled CX} - \text{Logical CX}}{3}$$

### B. Transpiler Routing Heuristic Comparison
We tested the interaction between topology and compilation using three routing strategies:

| Processor | Routing Heuristic | Circuit Depth | 2Q Gates (CX) | Equivalent SWAPs |
|---|---|---|---|---|
| **Processor A (5Q Line)** | Basic | 30 | 21 | 3.00 |
| **Processor A (5Q Line)** | Lookahead | 27 | 21 | 3.00 |
| **Processor A (5Q Line)** | Sabre | 27 | 19 | 2.33 |
| **Processor B (7Q Heavy-Hex)** | Basic | 28 | 16 | 1.33 |
| **Processor B (7Q Heavy-Hex)** | Lookahead | 30 | 18 | 2.00 |
| **Processor B (7Q Heavy-Hex)** | Sabre | 30 | 18 | 2.00 |

---

## 4. Visual Dashboards

### Processor Topologies
| Processor A (5-Qubit Line) | Processor B (7-Qubit Heavy-Hex) |
|:---:|:---:|
| ![Processor A](results/figures/processor_a_graph.png) | ![Processor B](results/figures/processor_b_graph.png) |

### Performance & Trade-offs
| Depth & Ratio Comparison | Noise Sensitivity Sweep | Routing Heuristic Trade-offs |
|:---:|:---:|:---:|
| ![Performance](results/figures/AB_performance.png) | ![Noise Sweep](results/figures/architecture_tradeoffs.png) | ![Routing](results/figures/routing_comparison.png) |

---

## 5. Architectural Findings
1. **Connectivity Saves Two-Qubit Overhead:** On Processor A, non-adjacent edges $(0, 3)$ and $(0, 4)$ require at least 2 to 3 SWAP operations (6–9 CX gates), increasing 2Q gate overhead by 58.3% over logical formulation. Processor B’s branching topology allows routing with only 1.33 equivalent SWAPs.
2. **Critical Path vs. Gate Density:** On Processor B, lookahead and heuristic search serialized routing along vertex 1 and 3, increasing depth to 30 despite requiring fewer total gates.
3. **Noise Resilience:** Sweeping two-qubit error rate $p_2 \in [0.2\%, 6.0\%]$ confirms that topologies requiring fewer physical routing gates decay significantly slower under physical gate noise.

---

## 6. Project Structure
```text
├── processors/
│   ├── processor_A.json       # 5-qubit linear architecture
│   └── processor_B.json       # 7-qubit heavy-hex architecture
├── src/
│   ├── problem.py             # Max-Cut graph, brute force solver & QAOA circuit
│   ├── metrics.py             # Equivalent SWAPs, gate count, approx ratio & SE
│   ├── benchmark.py           # Noise model & hardware execution
│   ├── optimizer.py           # Classical COBYLA variational angle optimizer
│   ├── routing_benchmark.py   # Multi-heuristic routing comparison (Basic, Lookahead, Sabre)
│   └── noise_sweep.py         # Two-qubit gate error degradation sweep
├── results/
│   ├── tables/                # CSV exported metrics
│   └── figures/               # Generated PNG visualization dashboards
├── main.py                    # Standalone reproducible runner script
├── main.ipynb                 # Executable Jupyter notebook with inline outputs
├── report.md                  # Comprehensive scientific report
└── requirements.txt           # Python package dependencies