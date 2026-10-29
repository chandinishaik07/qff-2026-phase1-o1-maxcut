# Qiskit Fall Fest 2026 — Phase 2 Technical Report

**Problem Track:** PS-O1 — Max-Cut Network Partitioning
**Team Name:** Qubit Nexus
**Report Type:** Phase 2 Technical Report

---

## Abstract

This report presents a Quantum Approximate Optimization Algorithm (QAOA)-based approach to the PS-O1 weighted Max-Cut problem. Exhaustive enumeration establishes the classical optimum, while Bell-state experiments compare ideal and noisy simulation. Processor A, Processor B, and a custom six-qubit Processor D are compared using circuit depth, CX gate count, and routing overhead. In the latest benchmark run, Processor D achieves a noisy approximation ratio of 0.7850 with no routing SWAPs. These results apply to the specified graph and simulation configuration and do not establish a general quantum advantage.

## 1. Introduction and Problem Definition

### 1.1 Problem Statement

The objective is to partition a weighted graph into two groups such that the total weight of edges connecting different groups is maximized.

The graph contains six vertices, numbered from 0 to 5, and nine weighted edges.

### 1.2 Weighted Edge Set

**Edge set:**

E = {(0, 2, 1), (0, 3, 4), (0, 4, 4), (1, 4, 3), (1, 5, 3), (2, 3, 5), (2, 4, 1), (3, 4, 4), (3, 5, 2)}

Each tuple (u, v, w) represents an edge between vertices u and v with weight w.

### 1.3 Mathematical Formulation

Each vertex is assigned to one of two partitions using a binary variable.

**Binary variable:**

xᵢ ∈ {0, 1}

* xᵢ = 0: Vertex i belongs to Partition 0.
* xᵢ = 1: Vertex i belongs to Partition 1.

**Contribution of an edge:**

Cᵤᵥ = wᵤᵥ |xᵤ − xᵥ|

An edge contributes its weight only when its endpoints belong to different partitions.

**Total cut value:**

C(x) = Σ₍ᵤ,ᵥ₎∈E wᵤᵥ |xᵤ − xᵥ|

**Optimization objective:**

x* = arg max C(x), where x ∈ {0, 1}⁶

The objective is to find the partition assignment that maximizes the total cut value.

**Cost Hamiltonian:**

H꜀ = Σ₍ᵤ,ᵥ,ʷ₎∈E (w/2)(ZᵤZᵥ − I)

Here, Zᵤ and Zᵥ represent Pauli-Z operators, and I represents the identity operator. With this sign convention, minimizing the Hamiltonian expectation corresponds to maximizing the cut value.

## 2. Classical Baseline and Optimal Solution

### 2.1 Exhaustive Search

All possible bitstrings were evaluated.

Number of possible states:

N = 2⁶ = 64

| Metric                     | Result |
| -------------------------- | -----: |
| Number of vertices         |      6 |
| Number of weighted edges   |      9 |
| Total edge weight          |     27 |
| Candidate bitstrings       |     64 |
| Classical optimal cut, C*  |     22 |
| Expected random cut        |  13.50 |
| Random approximation ratio | 0.6136 |

### 2.2 Optimal Bitstrings

The two complementary optimal solutions are:

* x* = (1, 1, 0, 1, 0, 0)
* Complement of x* = (0, 0, 1, 0, 1, 1)

These represent the same bipartition with the two sides exchanged.

### 2.3 Random Baseline Calculation

Each edge has a probability of 1/2 of crossing the cut under uniform random assignment.

**Expected random cut:**

Expected Cut = Total Edge Weight / 2

Expected Cut = 27 / 2 = 13.5

**Random approximation ratio:**

r_random = Expected Cut / Classical Optimal Cut

r_random = 13.5 / 22 ≈ 0.6136

The probability of randomly selecting one of the two optimal bitstrings is:

P(optimal) = 2 / 64 = 0.03125 = 3.125%

## 3. Objective 1 — Bell-State Verification and Noise Analysis

### 3.1 Method

The Bell-state experiment uses the state:

|Φ⁺⟩ = (|00⟩ + |11⟩) / √2

The Pauli correlations ⟨XX⟩, ⟨YY⟩, and ⟨ZZ⟩ are estimated using 4,096 shots per measurement basis.

**Fidelity formula:**

F = [1 + ⟨XX⟩ − ⟨YY⟩ + ⟨ZZ⟩] / 4

### 3.2 Results

| Qubit Pair | Distance | Condition |   ⟨XX⟩ |    ⟨YY⟩ |   ⟨ZZ⟩ | CX Count | Fidelity |
| ---------- | -------: | --------- | -----: | ------: | -----: | -------: | -------: |
| (0, 2)     |        1 | Ideal     | 1.0000 | −1.0000 | 1.0000 |        1 |   1.0000 |
| (0, 2)     |        1 | Noisy     | 0.9458 | −0.9521 | 0.9551 |        1 |   0.9633 |
| (1, 2)     |        2 | Ideal     | 1.0000 | −1.0000 | 1.0000 |        4 |   1.0000 |
| (1, 2)     |        2 | Noisy     | 0.9443 | −0.9341 | 0.9385 |        4 |   0.9542 |

**Noisy measurement standard errors:**

| Qubit Pair | SE of XX | SE of YY | SE of ZZ | Fidelity SE |
| ---------- | -------: | -------: | -------: | ----------: |
| (0, 2)     |   0.0051 |   0.0048 |   0.0046 |      0.0021 |
| (1, 2)     |   0.0051 |   0.0056 |   0.0054 |      0.0023 |

### 3.3 Noise Model

The simulation uses the following noise parameters:

* Single-qubit depolarizing rate: p₁ = 0.001
* Two-qubit CX depolarizing rate: p₂ = 0.005
* Readout bit-flip probability: pᵣₒ = 0.01

### 3.4 Discussion

The adjacent pair (0, 2) achieves a noisy fidelity of 0.9633, while pair (1, 2), at distance 2, achieves 0.9542.

The second experiment uses four CX gates instead of one, increasing exposure to two-qubit gate errors. This is consistent with its lower measured fidelity.

For the ideal Bell state, the expected correlations are:

* ⟨XX⟩ = +1
* ⟨YY⟩ = −1
* ⟨ZZ⟩ = +1

The ideal simulation matches these expected values.

## 4. Objective 2 — Custom Hardware Architecture: Processor D

### 4.1 Design Motivation

The problem contains six logical variables and therefore requires at least six physical qubits to execute the complete circuit.

Processor D uses six physical qubits and a coupling topology aligned with the nine interactions in the target graph.

### 4.2 Processor D Specifications

| Specification             | Value         |
| ------------------------- | ------------- |
| Physical qubits           | 6             |
| Coupling edges            | 9             |
| Maximum node degree       | 4             |
| Basis gates               | rz, sx, x, cx |
| Single-qubit noise rate   | 0.001         |
| Two-qubit CX noise rate   | 0.005         |
| Readout error probability | 0.01          |

**Undirected coupling edges:**

Eᴅ = {(0, 2), (0, 3), (0, 4), (1, 4), (1, 5), (2, 3), (2, 4), (3, 4), (3, 5)}

The benchmark reports no routing SWAPs for Processor D on this problem instance.

### 4.3 Transpilation Comparison

| Metric            | Processor A | Processor B | Processor D |
| ----------------- | ----------: | ----------: | ----------: |
| Physical qubits   |           5 |           9 |           6 |
| Executable        |          No |         Yes |         Yes |
| Logical CX gates  |           — |          18 |          18 |
| Physical CX gates |           — |          21 |          18 |
| Circuit depth     |           — |          37 |          29 |
| Two-qubit depth   |           — |          17 |          14 |
| Routing SWAPs     |           — |           1 |           0 |
| CX overhead       |           — |           3 |           0 |

**Processor A:** It has only five physical qubits and cannot execute the circuit requiring six logical qubits.

**Processor B:** The transpilation introduces one SWAP, equivalent to three additional CX gates. The reported circuit depth is 37, and the two-qubit depth is 17.

**Processor D:** The circuit uses 18 physical CX gates, has depth 29, and has two-qubit depth 14. No routing SWAPs are reported.

**Two-qubit depth reduction:**

Reduction = [(17 − 14) / 17] × 100%

Reduction ≈ 17.6%

### 4.4 Hardware Trade-offs

A topology tailored to a particular graph can reduce routing overhead. However, increased connectivity may increase chip area and complicate coupler and control-line routing. Crosstalk and frequency-allocation constraints must also be considered. These are general engineering considerations rather than effects measured directly by this benchmark.

## 5. Objectives 3 and 4 — QAOA Optimization and Benchmarking

### 5.1 Optimization Setup

The experiment uses QAOA at depth p = 1, a transverse-field Pauli-X mixer, and the COBYLA optimizer with five initializations.

The latest run produced the following expected-cut values:

| Seed | Gamma (γ) | Beta (β) | Expected Cut |
| ---: | --------: | -------: | -----------: |
|    0 |    3.2257 |   2.7821 |      17.7170 |
|    1 |    2.7045 |   4.2368 |      15.5750 |
|    2 |    0.7541 |   0.9485 |      15.2305 |
|    3 |    0.0822 |   1.2088 |      17.7200 |
|    4 |    2.9330 |   0.5898 |      15.1287 |

The selected parameters for the subsequent benchmark were γ = 0.0822 and β = 1.2088.

### 5.2 Mean Expected Cut

The mean expected cut is calculated as:

Mean Expected Cut = Sum of Expected Cuts / Number of Initializations

C̄ = (17.7170 + 15.5750 + 15.2305 + 17.7200 + 15.1287) / 5

**Mean Expected Cut = 16.2742**

### 5.3 Sample Standard Deviation

The sample standard deviation measures the variation across the five expected-cut values.

Sample Standard Deviation = √[Σ(Cᵢ − C̄)² / (N − 1)]

where:

* Cᵢ is the expected cut for initialization i.
* C̄ is the mean expected cut.
* N = 5 is the number of initializations.

**Sample standard deviation ≈ 1.3288**

### 5.4 Mean Approximation Ratio

The approximation ratio is the expected cut divided by the classical optimum.

Approximation Ratio = Expected Cut / Classical Optimal Cut

rᵢ = Cᵢ / C*

Since C* = 22:

Mean Approximation Ratio = 16.27424 / 22

**Mean Approximation Ratio ≈ 0.7397**

The sample standard deviation of the approximation ratio is:

Standard Deviation of Ratio = 1.3288 / 22

**Standard Deviation of Ratio ≈ 0.0604**

### 5.5 Best Expected-Cut Result

The highest expected cut among the five QAOA initializations is 17.7200, obtained with seed 3.

Best Expected-Cut Ratio = Best Expected Cut / Classical Optimal Cut

r_expected,best = 17.7200 / 22

**Best Expected-Cut Ratio ≈ 0.8055**

This is the best expected-cut ratio. It is not necessarily the best sampled-cut ratio.

### 5.6 Processor Benchmark Results

The following values are from the latest successful execution of `run_all.py` and its generated `results/tables/results.csv`.

| Processor | Condition | Executable | Logical / Physical Qubits | Logical CX | Physical CX | Depth | Two-Qubit Depth | SWAPs | Approximation Ratio | P(opt) |
| --------- | --------- | ---------- | ------------------------: | ---------: | ----------: | ----: | --------------: | ----: | ------------------: | -----: |
| A         | Ideal     | No         |                     6 / 5 |          — |           — |     — |               — |     — |                   — |      — |
| A         | Noisy     | No         |                     6 / 5 |          — |           — |     — |               — |     — |                   — |      — |
| B         | Ideal     | Yes        |                     6 / 9 |         18 |          21 |    37 |              17 |     1 |              0.8045 | 0.1399 |
| B         | Noisy     | Yes        |                     6 / 9 |         18 |          21 |    37 |              17 |     1 |              0.7833 | 0.1257 |
| D         | Ideal     | Yes        |                     6 / 6 |         18 |          18 |    29 |              14 |     0 |              0.8055 | 0.1414 |
| D         | Noisy     | Yes        |                     6 / 6 |         18 |          18 |    29 |              14 |     0 |              0.7850 | 0.1274 |

The executable benchmark conditions use 4,096 shots. Processor A is non-executable because it has fewer physical qubits than the six logical qubits required.

### 5.7 Benchmark Interpretation

Under the latest noisy simulation:

* Processor D achieves an approximation ratio of 0.7850, compared with the random baseline of 0.6136.
* Processor D's optimal-bitstring probability is 0.1274, compared with the random baseline of 0.03125.
* Processor D's noisy approximation ratio is slightly higher than Processor B's: 0.7850 versus 0.7833.
* Processor D uses 18 physical CX gates and zero routing SWAPs, compared with 21 physical CX gates and one SWAP for Processor B.
* Processor D's circuit depth is 29, compared with 37 for Processor B.

The approximation ratios are close, so the primary demonstrated advantage of Processor D is reduced circuit and routing overhead rather than a substantial improvement in solution quality. The results apply to this graph and simulation configuration and do not establish a general quantum advantage.

## 6. Limitations and Future Work

### 6.1 Topology Generalization

Processor D's coupling map is tailored to the target graph. A topology that avoids routing for one graph may not be suitable for another graph with different connectivity.

### 6.2 Circuit Depth and Noise

Increasing QAOA depth to p = 2 or p = 3 may improve ideal optimization results, but it also increases circuit cost and exposure to noise. The effect should be measured rather than assumed.

### 6.3 Future Work

Future work could include benchmarking additional graphs and QAOA depths, investigating noise-aware parameter optimization, and evaluating error-mitigation methods where supported by the simulation or hardware workflow.

## 7. Conclusion

This report formulates PS-O1 as a weighted Max-Cut problem on a six-vertex, nine-edge graph and uses exhaustive enumeration to establish a classical optimum of 22. Across five QAOA initializations, the mean expected cut is 16.2742, with a sample standard deviation of approximately 1.3288. The best expected cut is 17.7200, corresponding to an expected-cut approximation ratio of approximately 0.8055.

The custom six-qubit Processor D matches the target interaction graph and eliminates routing SWAPs in the reported transpilation. In the latest noisy benchmark, it achieves an approximation ratio of 0.7850 and an optimal-bitstring probability of 0.1274. The Bell-state results show lower estimated fidelity for the pair requiring more CX operations under the noisy simulation.

Overall, these results demonstrate the value of topology-aware benchmarking for this particular instance. They do not establish a general quantum advantage.

## 8. Result Files

The project repository includes the following result artifacts:

* `results/tables/results.csv` — processor-level QAOA benchmark results.
* `results/tables/bell.csv` — Bell-state verification measurements.
* `results/figures/` — generated figures used to explain the problem and benchmark results.
