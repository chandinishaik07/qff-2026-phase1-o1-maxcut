# Qiskit Fall Fest 2026 — Optimization Track (Phase 2)

**Team Name:** Qubit Nexus
**Selected Track & Problem Statement:** PS-O1 (Max-Cut Network Partitioning)
**Submission Repository:** Phase 2 Submission with Archived Phase 1

---

## 1. Executive Summary & Problem Formulation

This repository contains our Phase 2 submission for **PS-O1 (Max-Cut Network Partitioning)**.

The optimization task evaluates Max-Cut partitioning on a 6-vertex, 9-edge weighted network \(G = (V, E, w)\):

$$
E = \{(0,2,1), (0,3,4), (0,4,4), (1,4,3), (1,5,3), (2,3,5), (2,4,1), (3,4,4), (3,5,2)\}
$$

We map binary partitioning variables \(x_i \in \{0,1\}\) to Pauli-\(Z\) operators to construct the cost Hamiltonian \(H_C\). We solve the problem using the Quantum Approximate Optimization Algorithm (QAOA, \(p=1\)) and benchmark the results across multiple target architectures under ideal and noisy simulation conditions.

### Key Benchmark Summary

| Metric                                           | Random Baseline | Processor A (5Q) | Processor B (9Q, Noisy) | Processor D (6Q, Noisy) | Classical Optimum |
| :----------------------------------------------- | :-------------: | :--------------: | :---------------------: | :---------------------: | :---------------: |
| **Executable**                                   |       N/A       |        No        |           Yes           |           Yes           |        N/A        |
| **Approximation Ratio (\(r\))**                  |      0.6136     |        N/A       |          0.7833         |        **0.7850**       |       1.0000      |
| **Optimal Hit Probability (\(P_{\text{opt}}\))** |  0.0312 (3.12%) |        N/A       |          0.1257         |        **0.1274**       |        N/A        |
| **Routing SWAPs**                                |       N/A       |        N/A       |            1            |          **0**          |        N/A        |
| **Physical CX Gates**                            |       N/A       |        N/A       |            21           |          **18**         |        N/A        |
| **Classical Optimum (\(C^*\))**                  |       N/A       |        N/A       |            22           |            22           |       **22**      |

Processor D achieves approximately **4.08× the random baseline's optimal-hit probability**, while using three fewer physical CX gates and requiring no routing SWAPs compared with Processor B.

---

## 2. Repository Structure

The root directory contains the Phase 2 deliverables, while the original Phase 1 materials are preserved in `Phase 1/`.

```text
.
├── Phase 1/                    # Archived Phase 1 work
├── data/
│   └── instances.json           # Problem instance data
├── processors/
│   └── processor_D.json         # Custom six-qubit processor
├── results/
│   ├── figures/
│   │   └── optimal_partition.png
│   └── tables/
│       ├── bell.csv
│       └── results.csv
├── src/                         # Supporting source files
├── main.ipynb                   # End-to-end benchmark notebook
├── qff_phase2.py                # Evaluation and metric utilities
├── generate_processor.py        # Processor generation utility
├── report.md                    # Technical report
├── requirements.txt             # Pinned Python dependencies
└── run_all.py                   # Automated execution pipeline
```

---

## 3. Quick Start & Reproducibility (Gate G3)

The benchmark pipeline generates the results tables and figures using the provided problem and processor configuration files.

### 3.1 Environment Setup

Clone the repository and enter its directory:

```bash
git clone https://github.com/chandinishaik07/qff-2026-phase1-o1-maxcut.git
cd qff-2026-phase1-o1-maxcut
```

Create and activate a virtual environment:

```bash
python -m venv .qff2026-venv
```

On Windows PowerShell:

```powershell
.\.qff2026-venv\Scripts\Activate.ps1
```

On Linux or macOS, use:

```bash
source .qff2026-venv/bin/activate
```

Install the pinned dependencies:

```bash
pip install -r requirements.txt
```

### 3.2 Automated Pipeline Execution

Run the standalone pipeline:

```bash
python run_all.py
```

The script validates Processor D, performs the Bell-state verification and classical Max-Cut calculation, optimizes QAOA parameters, and exports the benchmark results.

### 3.3 Jupyter Notebook Execution

Open `main.ipynb` in Jupyter or VS Code and execute all cells from beginning to end.

To execute it non-interactively, use:

```bash
jupyter nbconvert --to notebook --execute --inplace main.ipynb
```

---

## 4. Hardware Architectures & Processor D

* **Processor A (5 qubits):** Non-executable for PS-O1 because the problem requires six logical qubits, exceeding the processor's capacity.
* **Processor B (9 qubits):** The target topology requires one routing SWAP, resulting in 21 physical CX gates and a circuit depth of 37.
* **Processor D (6 qubits):** A custom application-specific coupling graph designed to support the PS-O1 problem structure.

### Processor D Advantages

* **Zero routing SWAPs:** The circuit maps without additional routing SWAPs.
* **Zero CX overhead:** The 18 logical CX gates compile to 18 physical CX gates.
* **Reduced circuit depth:** Processor D has a circuit depth of 29, compared with 37 for Processor B.
* **Validation:** Processor D passes the validation performed by `run_all.py`.

In the current noisy simulation, Processor D achieves an approximation ratio of 0.7850, compared with 0.7833 for Processor B. These results are close; the primary demonstrated advantage of Processor D is reduced circuit overhead rather than a substantial improvement in solution quality.

---

## 5. Phase 1 Archive

The original Phase 1 work is preserved in the `Phase 1/` directory. It contains earlier project materials and documentation.

The Phase 2 implementation and deliverables are maintained separately at the repository root.

---

## 6. AI Usage Disclosure

Generative AI assistance was used during development for debugging, documentation formatting, LaTeX notation, and troubleshooting development and Git workflows.

The team is responsible for reviewing and validating the submitted implementation, experimental results, and documentation.
