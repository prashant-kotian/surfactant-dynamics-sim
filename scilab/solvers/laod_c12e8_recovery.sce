// =========================================================================
// laod_c12e8_recovery.sce
// Scilab Forward Solver for C12E8 LAOD at Optimal Design Window
// Verifies phase lag Delta phi and second harmonic I2 in Scilab 2025
// =========================================================================

mprintf("\n============================================================\n");
mprintf("SCILAB 2025: C12E8 LAOD FORWARD SIMULATION (Antigravity Engine)\n");
mprintf("============================================================\n\n");

// Thermodynamic & Kinetic Parameters for pure C12E8
CMC = 0.071;         // mol/m^3 (mM)
c0 = 1.5 * CMC;      // 0.1065 mol/m^3 (1.5x CMC optimal design point)
n_bar = 95.0;
Cm = (c0 - CMC) / CMC * n_bar; // 47.5
tau2 = 4.0;          // s (Patist 2002 ground-truth benchmark)

K_ads = 140.0;       // m^3/mol (Langmuir)
Gamma_inf = 2.80e-6; // mol/m^2
D = 3.8e-10;         // m^2/s
gamma0 = 72.0;       // mN/m
T_K = 295.15;
R_GAS = 8.314462618;

w = 6.283185;        // rad/s (1.0 Hz PAT-1M limit)
eps_strain = 0.20;   // 20% area strain

mprintf("System: pure C12E8 (monodisperse nonionic)\n");
mprintf("  c0 = %.4f mol/m^3 (1.5x CMC)\n", c0);
mprintf("  Capacity Cm = %.1f (n_bar = %.0f)\n", Cm, n_bar);
mprintf("  Relaxation time tau2 = %.2f s (omega*tau2 = %.2f)\n", tau2, w*tau2);
mprintf("  Frequency omega = %.2f rad/s (f = 1.0 Hz), Strain eps = %.2f\n\n", w, eps_strain);

// Grid generation (48 cells geometrically stretched)
n_cells = 48;
stretch = 4.0;
extent_factor = 8.0;
L = extent_factor * sqrt(D / w);
idx = (1:n_cells)' / n_cells;
s = (exp(stretch * idx) - 1.0) / (exp(stretch) - 1.0);
edges = [0.0; L * s];
centres = 0.5 * (edges(2:$) + edges(1:$-1));
widths = edges(2:$) - edges(1:$-1);
h_surf = centres(1);
h_face = centres(2:$) - centres(1:$-1);
n_int = n_cells - 1;
dV = widths(1:n_int);

// Equilibrium initial states
theta0 = K_ads * c0 / (1.0 + K_ads * c0);
G_eq = Gamma_inf * theta0;
c10 = c0;
M0 = Cm * c0;
y0 = [G_eq; c10 * ones(n_int, 1); M0 * ones(n_int, 1)];

function dy = f_pde(t, y)
    G = y(1);
    c = y(2 : n_int + 1);
    M = y(n_int + 2 : 2 * n_int + 1);
    
    denom = max(Gamma_inf - G, 1e-12 * Gamma_inf);
    cs = G / (K_ads * denom);
    
    j_in = D * (c(1) - cs) / h_surf;
    
    A = 1.0 + eps_strain * sin(w * t);
    dlnA = eps_strain * w * cos(w * t) / A;
    
    dG = j_in - G * dlnA;
    
    fluxes = zeros(n_int, 1);
    fluxes(1:$-1) = D * (c(2:$) - c(1:$-1)) ./ h_face(1:n_int-1);
    fluxes($) = D * (c0 - c($)) / h_face(n_int);
    
    dc = zeros(n_int, 1);
    dc(1) = (fluxes(1) - j_in) / dV(1);
    dc(2:$) = (fluxes(2:$) - fluxes(1:$-1)) ./ dV(2:$);
    
    dM = -((M - Cm * c) - (M0 - Cm * c10)) / tau2;
    dc = dc - dM;
    
    dy = [dG; dc; dM];
endfunction

mprintf("Integrating stiff PDE system over 5 oscillation cycles...\n");
period = 2.0 * %pi / w;
n_cycles = 5;
t_eval = linspace(0, n_cycles * period, 500);

// Stiff LSODA / BDF ODE solver in Scilab
y_sol = ode("stiff", y0, 0, t_eval, f_pde);

// Select last 2 steady-state cycles
idx_steady = find(t_eval >= (n_cycles - 2) * period);
t_ss = t_eval(idx_steady);
G_ss = y_sol(1, idx_steady);
theta_ss = G_ss / Gamma_inf;
sigma_ss = gamma0 + R_GAS * T_K * Gamma_inf * log(1.0 - theta_ss);

// Fourier decomposition
dt = t_ss(2) - t_ss(1);
N = size(t_ss, "*");
harm1 = sum(sigma_ss .* exp(-%i * w * t_ss)) * 2.0 / N;
harm2 = sum(sigma_ss .* exp(-%i * 2.0 * w * t_ss)) * 2.0 / N;

I1 = abs(harm1);
I2 = abs(harm2);
phi1_deg = atan(imag(harm1), real(harm1)) * 180.0 / %pi;
phi2_deg = atan(imag(harm2), real(harm2)) * 180.0 / %pi;
delta_phi_deg = pmodulo(phi2_deg - 2.0 * phi1_deg, 360.0);

mprintf("\n============================================================\n");
mprintf("SCILAB RESULTS FOR C12E8 (c = 1.5x CMC, omega = 6.28 rad/s):\n");
mprintf("============================================================\n");
mprintf("  Fundamental Harmonic I1: %.3f mN/m\n", I1);
mprintf("  Second Harmonic I2:      %.3f mN/m (Noise floor: 0.050 mN/m)\n", I2);
mprintf("  Harmonic Ratio I2/I1:    %.4f\n", I2 / I1);
mprintf("  Nonlinear Phase Lag:     %.1f deg\n", delta_phi_deg);
if I2 > 0.05 then
    mprintf("  >> STATUS: I2 CLEARS NOISE FLOOR (%.2fx above 0.05 mN/m) - SIGNAL IS DETECTABLE!\n", I2 / 0.05);
else
    mprintf("  >> STATUS: BELOW NOISE FLOOR\n");
end
mprintf("============================================================\n\n");
