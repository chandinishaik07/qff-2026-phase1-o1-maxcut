# Qiskit Fall Fest 2026 — Optimization Track (Phase 2)

**Team Name:** Qubit Nexus  
**Selected Track & Problem Statement:** PS-O1 (Max-Cut Network Partitioning)  
**Submission Repository:** Phase 2 Submission with Archived Phase 1  

---

## 1. Executive Summary & Problem Formulation

This repository contains the complete, reproducible Phase 2 submission for **PS-O1 (Max-Cut Network Partitioning)**. 

The optimization task evaluates max-cut partitioning on a locked 6-vertex, 9-edge weighted network $G = (V, E, w)$ with:
$$E = \{(0,2,1), (0,3,4), (0,4,4), (1,4,3), (1,5,3), (2,3,5), (2,4,1), (3,4,4), (3,5,2)\}$$

We map binary partitioning variables $x_i \in \{0, 1\}$ to Pauli-$Z$ operators to construct the cost Hamiltonian $H_C$, solved using the Quantum Approximate Optimization Algorithm (QAOA, $p=1$) benchmarked across multiple target architectures under ideal and open-system noise models.

### Key Benchmark Summary (Gate G2 Deliverable)

| Metric | Random Baseline | Processor A (5Q) | Processor B (9Q Noisy) | Processor D (6Q Noisy) | Classical Optimal ($C^*$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Status / Executable** | N/A | `false` (Capacity) | `true` | `true` | Ground Truth |
| **Approximation Ratio ($r$)** | $0.6136$ | — | $0.7833$ | **$0.7850$** | $1.0000$ |
| **Optimal Hit Probability ($P_{\text{opt}}$)** | $0.0312$ ($3.12\%$) | — | $0.1257$ | **$0.1274$ ($4.08\times$ Gain)** | N/A |
| **Routing SWAPs** | — | — | 1 | **0** | — |
| **Physical CX Gates** | — | — | 21 | **18 (0 CX Overhead)** | — |

---

## 2. Repository Structure

Per Section 10 guidelines, the root directory is strictly dedicated to Phase 2 deliverables, while Phase 1 materials are fully preserved in `Phase One/`.

```
.
├── Phase One/                       # Archived Phase 1 submission & documentation
│   ├── assets/                      # Phase 1 diagrams & assets
│   ├── docs/                        # Phase 1 architecture logs & writeups
│   ├── main.py                      # Original Phase 1 solver
│   └── README_Phase1.md             # Archived Phase 1 README
│
├── data/
│   └── instance.json                # PS-O1 locked benchmark configuration
│
├── processors/
│   ├── processor_A.json             # 5-qubit linear/tree architecture (official)
│   ├── processor_B.json             # 9-qubit heavy-hex topology (official)
│   └── processor_D.json             # 6-qubit custom application-specific topology
│
├── results/
│   ├── figures/
│   │   └── optimal_partition.png   # 2-partition graph visual ($C^* = 22$)
│   └── tables/
│       ├── bell.csv                 # Bell-state tomography & correlation data
│       └── results.csv              # Official 6-row hardware benchmark table
│
├── src/
│   └── qaoa_o1.py                   # Classical Max-Cut solver & QAOA ansatz builder
│
├── instances.json                   # Competition track problem definitions
├── main.ipynb                       # Runnable end-to-end benchmark notebook
├── qff_phase2.py                    # Official evaluation harness & metric utilities
├── report.md                        # Formal Technical Report (Objectives 1–4)
├── requirements.txt                 # Pinned dependencies for reproduction
└── run_all.py                       # Automated standalone execution pipeline
```

---

## 3. Quick Start & Reproducibility (Gate G3)

All results, tables, and figures can be completely reproduced from scratch in under 3 minutes.

### 3.1 Environment Setup
```bash
# 1. Clone the repository
git clone https://github.com/chandinishaik07/qff-2026-phase1-o1-maxcut.git
cd qff-2026-phase1-o1-maxcut

# 2. Create and activate a clean virtual environment
python -m venv venv
# On Windows (PowerShell):
.\venv\Scripts\activate
# On Linux / macOS:
source venv/bin/activate

# 3. Install pinned dependencies
pip install -r requirements.txt
```

### 3.2 Automated Pipeline Execution
Run the standalone automated script:
```bash
python run_all.py
```

### 3.3 Jupyter Notebook Execution (Gate G3 Audit)
Execute the notebook non-interactively end-to-end:
```bash
jupyter nbconvert --to notebook --execute --inplace main.ipynb
```

---

## 4. Hardware Architectures & Processor D

* **Processor A (5 Qubits):** Non-executable for PS-O1 because the problem requires 6 logical variables, violating hardware capacity constraints.
* **Processor B (9 Qubits):** Heavy-hex topology requiring SABRE routing SWAPs (1 SWAP added, increasing circuit depth to 37 and CX gate count to 21).
* **Processor D (6 Qubits, Custom Design):** An application-specific coupling graph directly mirroring the PS-O1 graph structure ($N=6$, max degree $\Delta = 4$).
  * **Zero SWAPs:** Circuit routes with 0 additional SWAPs.
  * **Zero CX Overhead:** 18 logical CX gates compile directly to 18 physical CX gates.
  * **Validation:** Verified compliant against all `validate_processor_d` rules.

---

## 5. Phase 1 Archive

All historical work, algorithms, and documentation from Phase 1 of Qiskit Fall Fest 2026 remain intact under the [`Phase One/`](./Phase%20One/) directory. This includes the initial problem exploration, exploratory scripts, and legacy documentation.

---

## 6. AI Usage Disclosure

In compliance with Competition Guidelines (Section 10), generative AI assistance (Large Language Models) was used during this phase for:
* Debugging Python script formatting, PowerShell encoding issues, and UTF-8 BOM sanitization.
* Structuring Markdown report boilerplates and LaTeX notation.
* Automating Git submodule decoupling and branch merge troubleshooting.

All quantum algorithmic implementations, QAOA circuits, objective functions, parameter optimizations, and numerical analyses were validated and verified by team members.