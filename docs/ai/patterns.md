# Architectural & Engineering Patterns

## Pattern 1: Decoupled JSON Hardware Topologies
- Stored hardware definitions (coupling maps, basis gates, and noise parameters) in modular JSON files under `processors/` to enable rapid swapping of hardware backends without modifying core transpilation scripts.

## Pattern 2: Analytic SWAP Accounting
- Derived equivalent SWAPs from raw CX gate unrolling:
  $$\text{Equivalent SWAPs} = \frac{\text{Compiled CX} - \text{Logical CX}}{3}$$
