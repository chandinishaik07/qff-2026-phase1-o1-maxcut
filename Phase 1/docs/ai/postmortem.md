# Engineering Postmortem

## What Went Well
- Modularizing `src/` modules made running reproducible benchmarks straightforward across CLI and Jupyter environments.
- Rendering equation PNGs with opaque backgrounds ensured cross-theme readability on both light and dark GitHub interfaces.

## Key Bottleneck
- Discrepancy between visual hardware topologies and text labels required flexible architectural design in JSON backend loaders.

## Lessons Learned
- Always isolate transpilation seeds (`seed=42`) to guarantee reproducible gate counts during heuristic compilation sweeps.
