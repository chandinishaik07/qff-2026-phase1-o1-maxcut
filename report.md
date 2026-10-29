# Qiskit Fall Fest 2026 — Phase 2 Technical Report

**Problem Track:** PS-O1 — Max-Cut Network Partitioning  
**Team Name:** Qubit Nexus  
**Report Type:** Phase 2 Technical Report

---

## Abstract

This report presents a QAOA-based approach to the PS-O1 weighted Max-Cut problem. It defines the graph objective, establishes a classical reference through exhaustive enumeration, summarizes Bell-state verification under ideal and noisy simulation, compares processor configurations, and discusses the QAOA benchmark results. The supplied results report that the custom six-qubit Processor D eliminates routing SWAP overhead for the target graph and achieves a noisy approximation ratio of 0.7850. These results apply to the supplied graph and simulation setup and do not establish a general quantum advantage over optimized classical methods.

## 1. Introduction and Problem Definition

### 1.1 Problem Statement

The objective is to divide the vertices of a weighted graph into two groups so that the total weight of edges crossing between the groups is maximized. This is the weighted Max-Cut problem.

The graph has six vertices and nine weighted edges. Vertices are indexed from 0 to 5.

### 1.2 Weighted Edge Set

`E = {(0,2,1), (0,3,4), (0,4,4), (1,4,3), (1,5,3), (2,3,5), (2,4,1), (3,4,4), (3,5,2)}`

Each tuple `(u, v, w)` represents an edge between vertices `u` and `v` with weight `w`.

### 1.3 Mathematical Objective

Let `x_i` be a binary variable:

- `x_i = 0` means vertex `i` belongs to partition 0.
- `x_i = 1` means vertex `i` belongs to partition 1.

An edge contributes its weight when its endpoints belong to different partitions. The cut value is:

`C(x) = sum over edges (u, v, w) of w * (x_u + x_v - 2*x_u*x_v)`

The goal is to find the bitstring `x*` that maximizes `C(x)`.

For the quantum formulation, the binary variables are mapped to Pauli-Z operators. The cost Hamiltonian used in the supplied report is:

`H_C = sum over edges (u, v, w) of (w/2) * (Z_u*Z_v - I)`

With this sign convention, minimizing the Hamiltonian energy corresponds to maximizing the cut value, up to the constant and sign convention used in the implementation.

## 2. Classical Baseline and Optimal Solution

### 2.1 Exhaustive Search

All `2^6 = 64` possible bitstrings were evaluated classically to establish a reference optimum.

| Metric | Reported result |
|---|---:|
| Number of vertices | 6 |
| Number of weighted edges | 9 |
| Total edge weight | 27 |
| Candidate bitstrings | 64 |
| Optimal cut value, `C*` | 22 |
| Uniform-random expected cut | 13.50 |
| Uniform-random approximation ratio | 0.6136 |
| Uniform-random probability of an optimal bitstring | 2/64 = 3.125% |

### 2.2 Optimal Bitstrings

The two reported optimal, complementary solutions are:

- `x* = (1, 1, 0, 1, 0, 0)`
- `complement(x*) = (0, 0, 1, 0, 1, 1)`

They represent the same bipartition with the two sides exchanged.

The uniform-random expected cut is half the total edge weight:

`Expected cut = 27/2 = 13.5`

The approximation ratio is:

`r_random = 13.5/22 ≈ 0.6136`

## 3. Objective 1 — Bell-State Verification and Noise Analysis

### 3.1 Method

Bell-state verification was reported for the state `|Phi+> = (|00> + |11>)/sqrt(2)`.

The Pauli expectation values `<XX>`, `<YY>`, and `<ZZ>` were sampled over 4,096 shots. The reported fidelity formula is:

`F = (1 + <XX> - <YY> + <ZZ>)/4`

### 3.2 Results

| Physical pair | Reported distance | Condition | `<XX>` ± SE | `<YY>` ± SE | `<ZZ>` ± SE | CX count | Fidelity `F` ± SE |
|---|---:|---|---:|---:|---:|---:|---:|
| (0, 2) | 1 | Ideal | 1.0000 ± 0.0000 | -1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 1 | 1.0000 ± 0.0000 |
| (0, 2) | 1 | Noisy | 0.9458 ± 0.0051 | -0.9521 ± 0.0048 | 0.9551 ± 0.0046 | 1 | 0.9633 ± 0.0021 |
| (1, 2) | 2 | Ideal | 1.0000 ± 0.0000 | -1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 4 | 1.0000 ± 0.0000 |
| (1, 2) | 2 | Noisy | 0.9443 ± 0.0051 | -0.9341 ± 0.0056 | 0.9385 ± 0.0054 | 4 | 0.9542 ± 0.0023 |

### 3.3 Noise Model

The supplied noise parameters are:

- Single-qubit depolarizing rate: `p1 = 0.001`
- Two-qubit CX depolarizing rate: `p2 = 0.005`
- Symmetric readout bit-flip probability: `p_ro = 0.01`

### 3.4 Discussion

Under the reported noisy simulation, the adjacent pair `(0, 2)` has fidelity `0.9633 ± 0.0021`, while the routed pair `(1, 2)` has fidelity `0.9542 ± 0.0023`. The routed operation uses four CX gates instead of one, giving the circuit more opportunities for gate errors. This is consistent with the lower reported fidelity for the routed pair.

**Important verification note:** the supplied source also contains a secondary Bell-state paragraph with different pair labels and fidelity values. Confirm the final numbers against `results/tables/bell.csv` before submission.

## 4. Objective 2 — Custom Hardware Architecture: Processor D

### 4.1 Design Motivation

The problem has six logical variables, so at least six physical qubits are required. The supplied material compares Processor A, Processor B, and custom Processor D. Processor D is designed so its physical coupling map matches the nine interactions in the target graph.

### 4.2 Processor D Specifications

| Specification | Reported value |
|---|---|
| Physical qubits | 6 |
| Physical coupling edges | 9 |
| Maximum node degree | 4 |
| Native basis gates | `rz`, `sx`, `x`, `cx` |
| Single-qubit depolarizing rate | 0.001 |
| Two-qubit CX depolarizing rate | 0.005 |
| Readout bit-flip probability | 0.01 |

The coupling map is:

`{(0,2), (0,3), (0,4), (1,4), (1,5), (2,3), (2,4), (3,4), (3,5)}`

This matches the endpoint pairs in the problem graph, allowing the required pairwise interactions to be implemented without routing SWAPs for this particular instance.

### 4.3 Transpilation Comparison

| Metric | Processor A | Processor B | Processor D |
|---|---:|---:|---:|
| Physical qubits | 5 | 9 | 6 |
| Executable for this problem | No | Yes | Yes |
| Logical CX gates | — | 18 | 18 |
| Physical CX gates | — | 21 | 18 |
| Circuit depth | — | 37 | 29 |
| Two-qubit depth | — | 17 | 14 |
| Routing SWAPs | — | 1 | 0 |

**Processor A:** Its five physical qubits are insufficient for the six logical variables, so the supplied results mark the circuit as non-executable.

**Processor B:** The reported transpilation adds one SWAP, equivalent to three CX gates, increasing the physical CX count from 18 to 21. The reported circuit depth is 37 and the two-qubit depth is 17.

**Processor D:** The reported transpilation adds no SWAPs and retains 18 physical CX gates. Its two-qubit depth is 14, approximately 17.6% lower than Processor B's reported two-qubit depth of 17.

### 4.4 Hardware Trade-offs

A custom topology can reduce routing for a known graph, but higher connectivity may complicate physical chip layout. In superconducting transmon designs, additional couplers and control-line routing can increase footprint and parasitic coupling. Crosstalk and frequency-allocation constraints also need to be considered. These are design considerations, not measurements established by the supplied benchmark table.

## 5. Objectives 3 and 4 — QAOA Optimization and Benchmarking

### 5.1 Optimization Setup

The supplied report evaluates QAOA at depth `p = 1`, using a transverse-field Pauli-X mixer and cost-phase operations. COBYLA was run from five reported initializations.

| Seed | Gamma | Beta | Expected cut |
|---:|---:|---:|---:|
| 0 | 3.2257 | 2.7821 | 17.7170 |
| 1 | 2.7045 | 4.2368 | 15.5750 |
| 2 | 0.7541 | 0.9485 | 15.2305 |
| 3 | 0.0822 | 1.2088 | 17.7200 |
| 4 | 2.9330 | 0.5898 | 15.1287 |

The best reported parameters are `gamma* = 0.0822` and `beta* = 1.2088`, giving an expected cut of `17.7200`.

The approximation ratio is:

`r = expected cut / optimal cut = 17.7200/22 ≈ 0.8055`

**Reproducibility check:** the source says the angles were initialized uniformly in `[0, pi]`, but the reported beta value for seed 1 is `4.2368`, which exceeds pi. Confirm the actual initialization range or whether the optimized angle was wrapped before documenting the range.

### 5.2 Benchmark Results

| Processor | Condition | Executable | Logical / physical qubits | Logical CX | Physical CX | Depth | Two-qubit depth | SWAPs | Approximation ratio `r` | `P_opt` |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | Ideal | No | 6 / 5 | — | — | — | — | — | — | — |
| A | Noisy | No | 6 / 5 | — | — | — | — | — | — | — |
| B | Ideal | Yes | 6 / 9 | 18 | 21 | 37 | 17 | 1 | 0.8045 | 0.1399 |
| B | Noisy | Yes | 6 / 9 | 18 | 21 | 37 | 17 | 1 | 0.7833 | 0.1257 |
| D | Ideal | Yes | 6 / 6 | 18 | 18 | 29 | 14 | 0 | 0.8055 | 0.1414 |
| D | Noisy | Yes | 6 / 6 | 18 | 18 | 29 | 14 | 0 | 0.7850 | 0.1274 |

The values are transcribed from the supplied report and should be cross-checked against `results/tables/results.csv`.

### 5.3 Interpretation

Under the reported noisy simulation:

- Processor D's approximation ratio is `0.7850`, compared with `0.6136` for the uniform-random baseline.
- The relative increase over the random approximation ratio is approximately `27.9%`.
- Processor D's reported optimal-bitstring probability is `12.74%`, compared with `3.125%` for uniform random sampling, approximately `4.08 times` as high.
- Compared with Processor B, Processor D reports a slightly higher noisy approximation ratio (`0.7850` versus `0.7833`) and optimal-bitstring probability (`0.1274` versus `0.1257`).

These comparisons support the claim that Processor D performs better than the random baseline and modestly better than Processor B in the supplied simulation. They do not prove a general quantum advantage over optimized classical algorithms.

## 6. Limitations and Future Work

### 6.1 Topology Generalization

The custom coupling map is tailored to this graph. A topology that removes routing for one graph may not be suitable for another, especially when the target graph has different or non-planar connectivity.

### 6.2 Circuit Depth and Noise

Increasing QAOA depth may improve ideal optimization results, but it also increases gate count and exposure to noise. The supplied material suggests investigating depths `p = 2` and `p = 3`; their performance should be measured rather than assumed to improve under noise.

### 6.3 Recommended Next Steps

1. Verify all reported values against the source CSV files.
2. Repeat benchmarking for multiple graphs and multiple optimizer seeds.
3. Compare ideal and noisy performance at several QAOA depths.
4. Investigate noise-aware parameter optimization.
5. Evaluate error-mitigation methods such as zero-noise extrapolation and Pauli twirling, including their sampling overhead.
6. Investigate dynamical decoupling and gate scheduling to reduce idle-time errors and circuit depth where supported by the hardware.

## 7. Conclusion

This report formulates PS-O1 as a weighted Max-Cut problem on a six-vertex, nine-edge graph and uses exhaustive enumeration to establish the reported optimum of 22. The best supplied `p = 1` QAOA result has an expected cut of `17.7200` and an approximation ratio of approximately `0.8055`.

The custom six-qubit Processor D matches the target interaction graph and, in the reported transpilation results, eliminates routing SWAPs. Its noisy approximation ratio is reported as `0.7850`, with an optimal-bitstring probability of `12.74%`. These results suggest that topology-aware compilation can reduce routing overhead and improve performance for this particular problem instance.

Before final submission, resolve the source inconsistencies noted in the Bell-state section and QAOA initialization range, and confirm the benchmark tables against the underlying CSV files.

## 8. Referenced Result Files

The supplied material references:

- `results/tables/results.csv` — processor-level QAOA benchmark results
- `results/tables/bell.csv` — Bell-state verification measurements

Include these files with the project repository or ensure they are available to the evaluator if reproducibility is required.
