# Architecture Decision Records (ADRs)

## ADR-01: Classical Optimization via COBYLA
- **Context:** Variational parameter optimization for QAOA ($p=1$).
- **Decision:** Selected COBYLA because it handles bounded, gradient-free search spaces effectively for low-dimensional angle pairs ($\gamma, \beta$).
- **Consequence:** Converged reliably to $\gamma^* = 2.7916$, $\beta^* = 0.3508$.

## ADR-02: Transpiler Routing Heuristic Benchmark
- **Context:** Mapping the 5-qubit Max-Cut instance onto hardware coupling topologies.
- **Decision:** Benchmarked Basic, Lookahead, and Sabre heuristics across Processors A and B.
- **Consequence:** Sabre minimized SWAP insertion on Processor A (19 CX), while Basic achieved the lowest raw gate overhead on Processor B (16 CX).
