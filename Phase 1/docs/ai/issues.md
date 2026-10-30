# Technical Issues & Resolutions

## Issue 1: PowerShell Command String Escaping
- **Symptom:** Running one-liner scripts containing LaTeX expressions (`$|\psi\rangle$`) resulted in PowerShell parameter parsing errors.
- **Resolution:** Replaced inline string passing with dedicated temporary `.py` script generators and PowerShell here-strings (`@' ... '@`).

## Issue 2: Processor B Qubit Topology Clarification
- **Symptom:** Architecture diagram presented 9 visible vertices while text metadata originally referenced a 7-qubit specification.
- **Resolution:** Updated configurations to support the 9-qubit heavy-hex coupling map in response to official organizer guidance.
