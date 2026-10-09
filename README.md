# Qiskit Fall Fest 2026 - Phase 1: Architecture Benchmark
**Problem Statement:** O1 — Max-Cut  
**Track:** Quantum Optimization  

## Overview
This repository implements an end-to-end benchmark of QAOA ($p=1$) for the Max-Cut problem, comparing execution performance and compilation overhead across two distinct physical processor architectures:
- **Processor A:** 5-qubit linear architecture
- **Processor B:** 7-qubit heavy-hex-inspired branching architecture

## Project Structure
```text
├── processors/             # Physical coupling maps & noise models
├── src/                    # Modular problem, metrics & benchmark scripts
├── results/
│   ├── tables/            # AB_comparison.csv, routing_comparison.csv, noise_sweep.csv
│   └── figures/           # Topology graphs & performance charts
├── main.py                # Standalone benchmark runner
├── main.ipynb             # Executable Jupyter notebook with inline figures
├── report.md              # Detailed scientific report & architecture analysis
└── requirements.txt       # Environment dependencies