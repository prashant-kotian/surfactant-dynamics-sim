# Surfactant-Dynamics-Sim

**Multiscale Dynamic Simulation Framework for Surfactant Kinetics & Non-Equilibrium Interfacial Phenomena**

[![Author: Prashant D. Kotian](https://img.shields.io/badge/Author-Prashant%20D.%20Kotian-blue.svg)](https://github.com/prashant-kotian)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Engine: Scilab / Xcos](https://img.shields.io/badge/Simulator-Scilab%202025%20%2B%20Xcos-orange.svg)](https://www.scilab.org/)
[![Thermodynamics: SurfactantKit](https://img.shields.io/badge/Thermodynamics-SurfactantKit-purple.svg)](https://surfactant.thechemsolver.com)

---

## 1. Overview

`Surfactant-Dynamics-Sim` is an open-source multiscale computational framework coupling microscopic surfactant molecular thermodynamics with continuum-scale dynamic systems modeling. 

By integrating **SurfactantKit** (molecular descriptors, critical packing parameter, non-ideal mixed micellization, Ward-Tordai adsorption kinetics, and HLD-NAC phase behavior) with **Scilab-Xcos** (stiff DAE integration via SUNDIALS CVode/IDA, physical Modelica modeling, and dynamic block diagrams), this project unlocks non-equilibrium interfacial phenomena across the millisecond-to-minute continuum:
- Large-Amplitude Oscillatory Dilatational (LAOD) rheology and harmonic Marangoni stress.
* Dynamic capillary desaturation and Marangoni tip-streaming in microfluidics.
* Acoustic and mechanical resonance in dynamic foam lamella drainage.
* Open-source continuum colloid engineering benchmarks.

---

## 2. Repository Structure

```
surfactant-dynamics-sim/
├── docs/                      # Architectural specs, math formulations, literature notes
├── data/                      # Mined experimental tensiometry & rheology datasets
│   ├── raw/                   # Unprocessed digitizations (PAT-1M, microfluidics, TFB)
│   ├── curated/               # Standardized JSON/CSV timeseries for SDS, CTAB, Triton X-100
│   └── literature/            # DOI indexes, source citations, digitization metadata
├── src/                       # Python-Scilab bridging engine
│   ├── bridge/                # IPC, C-types, and Python-Scilab gateways
│   ├── surrogate/             # Intel Arc GPU accelerated PINN/surrogate models
│   └── analysis/              # Fourier analysis, harmonic decomposition, visualization
├── scilab/                    # Scilab scripts (.sce, .sci) and Xcos models (.zcos)
│   ├── models/                # Xcos block diagrams for oscillating drops & microchannels
│   ├── solvers/               # Scilab DAE and Ward-Tordai boundary layer solvers
│   └── macros/                # Reusable Scilab function libraries
├── benchmarks/                # Verification against analytical Ward-Tordai & LVDT solutions
└── tests/                     # Unit tests and automated convergence validations
```

---

## 3. Collaboration Model

This project is executed collaboratively between:
* **Antigravity (Local Execution Agent)**: Manages local Scilab+Xcos engine, Intel Arc GPU acceleration, Kaggle remote GPU workflows, and local Git operations.
* **Arena AI (Browser & Research Agent)**: Manages automated literature data mining, paper digitization, and shared sync via Google Drive (`kotianinterface@gmail.com`) and GitHub.

---

## 4. License

Distributed under the MIT License. See `LICENSE` for details.
