import json
from qiskit import transpile
from qiskit.transpiler import CouplingMap
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError
from src.metrics import calculate_approximation_ratio

def run_noise_sweep(circuit, graph, opt_cut, config_path, rates=None):
    if rates is None:
        rates = [0.002, 0.005, 0.01, 0.02, 0.04, 0.06]
        
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
        
    cmap = CouplingMap(cfg["coupling_map"])
    transpiled = transpile(
        circuit,
        coupling_map=cmap,
        basis_gates=cfg["basis_gates"],
        optimization_level=1,
        seed_transpiler=42
    )
    
    ratios = []
    for p in rates:
        noise = NoiseModel()
        noise.add_all_qubit_quantum_error(depolarizing_error(p / 10.0, 1), ["x", "sx"])
        noise.add_all_qubit_quantum_error(depolarizing_error(p, 2), ["cx"])
        noise.add_all_qubit_readout_error(ReadoutError([[0.98, 0.02], [0.02, 0.98]]))
        
        sim = AerSimulator(noise_model=noise)
        counts = sim.run(transpiled, shots=2048, seed_simulator=42).result().get_counts()
        _, ratio, _ = calculate_approximation_ratio(counts, graph, opt_cut)
        ratios.append(ratio)
        
    return rates, ratios