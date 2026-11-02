// ==============================================================================
// dynamic_surface_tension_oscillatory.sce
// Simulation of Dynamic Surface Tension Under Oscillatory Area Dilation
// Engine: Scilab 2025.0.0 (SUNDIALS CVode Integrator)
// Authors: Prashant D. Kotian (The ChemSolver / DevSwarm)
// ==============================================================================

clear; clc;

printf("====================================================================\n");
printf("  Surfactant-Dynamics-Sim: Non-linear Oscillatory Dilatational Solver\n");
printf("====================================================================\n\n");

// ------------------------------------------------------------------------------
// 1. Surfactant Thermodynamic Properties (from SurfactantKit)
// ------------------------------------------------------------------------------
gamma0    = 72.8;     // Solvent (water) surface tension (mN/m) at 298.15 K
Gamma_inf = 3.8e-6;   // Saturated monolayer surface excess (mol/m^2)
n_ion     = 1.0;      // Molecular charge factor (1 for nonionic, 2 for 1:1 ionic)
R_gas     = 8.314;    // Universal gas constant (J / mol K)
Temp      = 298.15;   // Temperature (K)
ka        = 1.5e-1;   // Kinetic adsorption rate constant (m^3 / mol s)
kd        = 1.2e-3;   // Kinetic desorption rate constant (1 / s)
C0        = 5.0e-3;   // Bulk surfactant concentration (mol / m^3)
D_diff    = 4.5e-10;  // Molecular diffusion coefficient (m^2 / s)

// ------------------------------------------------------------------------------
// 2. Oscillatory Forcing Parameters (Large Amplitude Regime)
// ------------------------------------------------------------------------------
omega     = 0.5;      // Oscillation angular frequency (rad / s)
eps       = 0.20;     // Strain amplitude (20% dilation/compression)

// ------------------------------------------------------------------------------
// 3. State-Space Dynamical System Formulation
// State vector: x = [Gamma(t); C_sub(t)]
// ------------------------------------------------------------------------------
function dxdt = surfactant_dynamics(t, x)
    Gamma_t = x(1);
    C_sub   = x(2);
    
    // Dynamic area dilation rate: d(ln A)/dt
    A_t      = 1.0 + eps * sin(omega * t);
    dlnA_dt  = (eps * omega * cos(omega * t)) / A_t;
    
    // Kinetic Langmuir adsorption flux
    j_ads    = ka * C_sub * (Gamma_inf - Gamma_t) - kd * Gamma_t;
    
    // Diffusion sublayer transport approximation
    // Characteristic oscillatory diffusion boundary layer thickness: delta = sqrt(pi * D / omega)
    delta    = sqrt(%pi * D_diff / omega);
    j_diff   = (2.0 * D_diff / delta) * (C0 - C_sub);
    
    // Conservation differential equations
    dGamma   = j_ads - Gamma_t * dlnA_dt;
    dC_sub   = (j_diff - j_ads) / delta;
    
    dxdt     = [dGamma; dC_sub];
endfunction

// ------------------------------------------------------------------------------
// 4. Time Grid and Numerical Integration
// ------------------------------------------------------------------------------
t_span = linspace(0, 60, 1200); // 60 seconds, 1200 sampling steps
x0     = [0.85 * Gamma_inf; C0]; // Initial condition at t=0

printf("Executing SUNDIALS CVode integration across %d steps...\n", length(t_span));
sol = ode(x0, 0, t_span, surfactant_dynamics);

// ------------------------------------------------------------------------------
// 5. Post-Processing: Compute Dynamic Tension & Surface Pressure
// ------------------------------------------------------------------------------
Gamma_res = sol(1, :);
C_sub_res = sol(2, :);

// Clamp surface coverage theta = Gamma / Gamma_inf to physical monolayer regime [0.001, 0.995]
theta     = min(0.995, max(0.001, Gamma_res / Gamma_inf));
RT_factor = n_ion * R_gas * Temp * Gamma_inf * 1e3; // Unit: mN/m
gamma_t   = gamma0 + RT_factor * log(1.0 - theta);
Pi_t      = gamma0 - gamma_t; // Surface pressure (mN/m)

printf("Simulation complete.\n");
printf("  Minimum Surface Tension: %.2f mN/m\n", min(gamma_t));
printf("  Maximum Surface Tension: %.2f mN/m\n", max(gamma_t));
printf("  Peak-to-Peak Tension Amplitude: %.2f mN/m\n", max(gamma_t) - min(gamma_t));

// Clean exit for headless batch runs
quit;
