import json
from qiskit import transpile
from qiskit.transpiler import CouplingMap
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError

def build_noise_model(processor_cfg):
    noise_cfg = processor_cfg.get("noise", {})
    noise_model = NoiseModel()

    single_q_err = noise_cfg.get("single_qubit_error", 0.001)
    two_q_err = noise_cfg.get("cx_error", 0.01)
    readout_err = noise_cfg.get("readout_error", 0.02)

    noise_model.add_all_qubit_quantum_error(depolarizing_error(single_q_err, 1), ["x", "sx"])
    noise_model.add_all_qubit_quantum_error(depolarizing_error(two_q_err, 2), ["cx"])
    noise_model.add_all_qubit_readout_error(
        ReadoutError([[1.0 - readout_err, readout_err], [readout_err, 1.0 - readout_err]])
    )
    return noise_model

def run_processor_benchmark(qc, processor_json_path, shots=4096, seed=42):
    with open(processor_json_path, 'r', encoding='utf-8') as f:
        proc = json.load(f)

    coupling = CouplingMap(proc["coupling_map"])
    noise_model = build_noise_model(proc)

    compiled_qc = transpile(
        qc,
        coupling_map=coupling,
        basis_gates=proc["basis_gates"],
        optimization_level=1,
        seed_transpiler=seed
    )

    sim = AerSimulator(noise_model=noise_model)
    job = sim.run(compiled_qc, shots=shots, seed_simulator=seed)
    counts = job.result().get_counts()

    return proc["name"], compiled_qc, counts
