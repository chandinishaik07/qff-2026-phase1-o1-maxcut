import pandas as pd
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Create a Bell state circuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Simulate using Aer
simulator = AerSimulator()
job = simulator.run(qc, shots=1024)
result = job.result()
counts = result.get_counts(qc)

# Format and save to results/tables/bell.csv
df_bell = pd.DataFrame(list(counts.items()), columns=['State', 'Count'])
df_bell.to_csv("results/tables/bell.csv", index=False)
print("[SUCCESS] Bell state results saved to results/tables/bell.csv")
print(df_bell)