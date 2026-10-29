# Plan Evolution

## Phase 1.1: Core Implementation
- Constructed baseline 5-qubit graph ($C_5$ + cross-edge).
- Validated classical maximum cut baseline ($C_{\text{max}} = 5$).

## Phase 1.2: Transpiler & Noise Sweep
- Profiled depolarizing noise scaling across error regimes ($0.2\%$ to $6.0\%$).
- Mapped routing trade-offs across Sabre, Lookahead, and Basic passes.

## Phase 1.3: Repository Alignment
- Refactored folder hierarchy to adhere strictly to the automated evaluation specification (`data/raw/`, `assets/`, `src/`).
