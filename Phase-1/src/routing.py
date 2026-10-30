import json
import pandas as pd
from qiskit import transpile
from qiskit.transpiler import CouplingMap
from src.metrics import extract_circuit_metrics

def evaluate_routing_methods(logical_qc, processor_json_path):
    with open(processor_json_path, 'r', encoding='utf-8') as f:
        proc = json.load(f)

    coupling = CouplingMap(proc["coupling_map"])
    methods = ["basic", "lookahead", "sabre"]
    results = []

    for method in methods:
        compiled = transpile(
            logical_qc,
            coupling_map=coupling,
            basis_gates=proc["basis_gates"],
            routing_method=method,
            optimization_level=1,
            seed_transpiler=42
        )
        metrics = extract_circuit_metrics(compiled, logical_cx_count=12)
        results.append({
            "Processor": proc["name"],
            "Routing Method": method.capitalize(),
            "Depth": metrics["depth"],
            "2Q Gates": metrics["two_qubit_gates"],
            "Equivalent SWAPs": metrics["equivalent_swaps"]
        })

    return results