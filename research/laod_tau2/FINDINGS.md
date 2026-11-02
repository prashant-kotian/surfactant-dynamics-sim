# LAOD / τ₂ research record — findings so far

**Status:** kill-criterion study complete. Verdict: **viable, but only within a
bandwidth-bounded window** — and the bound is now quantified, which is itself the
publishable result.
**Date:** 2026-11-02 · Branch `arena/fa2f9ecf-surfactant-toolkit`
**Code:** `research/laod_tau2/` (research code, deliberately outside `src/`; not
shipped, not tiered). Anchors: 8 passing tests. Existing suite: 982 passed.

---

## 1. The question, restated operationally

Not "can harmonics be computed" — that is trivial. The question that decides the paper:

> Given a real instrument (bounded frequency window, finite strain amplitude,
> ~0.05 mN/m tension noise), can the micellar slow relaxation time τ₂ be
> **recovered with a useful uncertainty** from the harmonic content of a
> large-amplitude oscillatory dilatational response?

"Useful" was fixed in advance at **relative standard error < 30%**, and the study
was designed to fail. It partly did — which is the most valuable thing that
happened.

---

## 2. What the forward model is (and is not)

`model.py`: 1D monomer diffusion to a planar interface, finite-volume,
geometric grid; Langmuir isotherm at local equilibrium; surface mass balance
including the dilatational term `−Γ dlnA/dt`; and the micelles carried as an
**explicit conserved species** with a linearised Aniansson–Wall exchange

    M_eq(c) = C_m · c ,     dM/dt = −(M − M_eq(c))/τ₂

so total surfactant (bulk + micellar + adsorbed) is conserved *by construction*.
This is the deliberate replacement for the white paper's fixed-δ two-compartment
model, which leaks mass (documented in `model.py`'s module docstring).

Two reservoir parameters, and this distinction turned out to matter more than
anything else in the study:

- **capacity** `C_m = d(micellar)/d(monomer)` — how *much* surfactant is available
- **τ₂** — how *fast* it is released

## 3. Anchors (what makes the numbers trustworthy)

All in `tests/test_anchors.py`, all passing:

| Anchor | Result |
|---|---|
| LVDT closed form reproduced from the PDE, ω = 0.1/1/10 | 4–5 significant figures, no fitting |
| Insoluble limit D → 0 → 2εE₀ | monotone approach, 15% at the grid floor |
| Harmonics → 0 as ε → 0 | second harmonic scales with ε (nonlinear effect, not artefact) |
| Fast reservoir, ωτ₂ → 0 | equals micelle-free system with D_eff = D(1+C_m), 5% |
| Slow reservoir, ωτ₂ → ∞ | equals micelle-free system at same D, 2% |
| ε = 0 stationarity | no spurious drift |

The LVDT anchor was not decorative: it caught a **structural bug** in which I
wrote the subsurface concentration as the differential state instead of Γ. That
version satisfies Γ = f(c_s) at every instant, making the interface infinitely
compressible and reporting ~1/E₀ elasticity — a 300× error that looked like
"physics" until the anchor refuted it. Any group attempting this without the
analytic anchor will publish that bug.

---

## 4. Headline result: the bandwidth rule

`study_bandwidth_rule.py` / `bandwidth_rule.json`. Capacity 5, σ = 0.05 mN/m,
ε = 0.20, one-parameter inversion (capacity known from equilibrium data).

| Instrument window | τ₂ = 1 ms | τ₂ = 10 ms | τ₂ = 100 ms |
|---|---|---|---|
| 1 Hz oscillating drop (2–1000 mHz) | relSE 13.4 ✗ | 3.14 ✗ | 0.97 ✗ |
| 10 Hz capillary-pressure (0.1–62.8 rad/s) | 0.84 ✗ | **0.16 ✓** | **0.23 ✓** |
| 100 Hz oscillating-bubble CPT (1–628 rad/s) | **0.04 ✓** | **0.04 ✓** | **0.07 ✓** |

**Recovery requires the instrument window to bracket ωτ₂ ≈ 1.** Empirically:
usable (relSE < 0.3) needs `ω_max·τ₂ ≳ 0.3`, precise (relSE < 0.1) needs
`ω_max·τ₂ ≳ 3`, and the low-frequency branch must reach `ω_min·τ₂ ≲ 0.05`.

This is the paper's practical deliverable: **an instrument specification per
micellar system**, not a blanket "we can measure it". It also explains, in
advance, why the original white-paper plan (a 1 Hz oscillating drop, ionic
surfactants with τ₂ ≈ ms–s) would have failed — and that negative result is
worth stating in the paper, because it is the failure mode most groups will hit.

## 5. Where recovery is identifiable at all — the map

`study_recoverability_v3.py` / `recoverability_map.json`. Window 0.3–6.28 rad/s
(a deliberately *narrow* case, ωτ₂ never bracketing 1 from below).

| capacity | τ₂ = 1 ms | 10 ms | 100 ms | 300 ms | 1 s |
|---|---|---|---|---|---|
| 5.0 (one-parameter) | ✗ 1.42 | ✗ 0.58 | **✓ 0.19** | ✗ 0.37 | ✗ 14.9 |
| 1.4 (one-parameter) | ✗ 1.37 | ✗ 0.54 | **✓ 0.20** | ✗ 0.40 | ✗ 28.6 |

Two-parameter fits are consistently worse (relSE 0.65–12), i.e. **τ₂ and capacity
are partly degenerate and capacity must come from independent equilibrium data**
(CMC + aggregation number + mass balance). That is a stated protocol requirement,
not a defect — and it is exactly the kind of honest constraint referees reward.

Note τ₂ = 1 s fails here only because the window's *lower* end (0.3 rad/s) is
above 0.05/τ₂; the bandwidth study shows a 1 Hz window covers it fine when the
sweep starts at 0.01 rad/s. Both edges matter.

---

## 6. Two negative results worth recording

**6.1 Strain amplitude is a decoy, and a dangerous one.** A quick probe with a
non-conservative boundary-layer reservoir suggested I₂/I₁ rises steeply with
strain amplitude (0.080 → 0.732 across ε = 0.1→0.4). In the mass-conserving
model, I₂/I₁ at fixed ε is almost *insensitive* to both coverage and reservoir
strength: it sits at 0.066–0.081 for θ = 0.56–0.98, capacity 0.2–5, ω = 0.3–6.3.
**If we had published the probe's "large, distinctive signature", it would have
been an artefact.** The effect lives in the *phase lag* (0.14° → 6.7° per doubling
of τ₂) and in I₃/I₁, not in I₂/I₁.

**6.2 Coverage is not the lever; capacity is.** Sweeping θ = 0.56 → 0.98 at fixed
capacity moved nothing. Sweeping capacity 0.2 → 5 raised τ₂ leverage from 0.9× to
13× the noise floor. Pass 1 of the recoverability study failed *entirely* because
it used capacity 0.2 — a reservoir 25× too weak, which corresponds to "all the
surfactant is monomer", i.e. not a micellar solution at all. Lesson recorded: a
sensitivity study is only as meaningful as the parameter regime it is run in, and
the regime must be justified from equilibrium data before the run.

---

## 7. What this does and does not yet establish

**Established (model-internal, anchored):** the forward physics reaches the
analytic limits; within a bracketed bandwidth the inversion recovers τ₂ to 0.04–0.23
relative SE at realistic tension noise; the recovery is bandwidth-limited by a
quantified rule; τ₂/capacity degeneracy requires independent capacity input.

**Not yet established — required before any submission:**

1. **Real surfactant parameters.** Everything here uses one representative
   parameter set (Γ∞ = 3.5×10⁻⁶ mol/m², K = 5 m³/mol, D = 4×10⁻¹⁰ m²/s,
   capacity 5). Each of these must be sourced or measured per system, and the
   capacity must be derived from an actual aggregation number and CMC.
2. **The C_m ↔ micelle physics link.** Capacity is currently a free number.
   It must be tied to (c_total − CMC)·n̄ / CMC and checked for consistency.
3. **Nonlinear Aniansson–Wall.** The linearised reservoir is fine for LAOD
   amplitudes but must be shown to be, against the stepwise spectrum.
4. **An experimental comparison.** At least one published oscillatory
   dilatational dataset above the CMC, re-analysed, with the inverted τ₂
   compared to an independently measured one. Without this the paper is a
   methods proposal, not a method.
5. **Instrument reality check.** The 100 Hz microtensiometer result must be
   confirmed against a real instrument's specification (radius, acquisition
   rate, strain capability at that frequency), not assumed.

---

## 8. Honest assessment of the paper

The result is **not** "harmonics reveal everything" — it is narrower and better:
*a bounded, quantified regime in which a nonlinear surface-rheology measurement
can replace dedicated relaxation equipment, plus the condition under which it
cannot.* The honest title is about the bound, not the capability.

Realistic outcome: one solid methods paper (JCIS/Langmuir) **if** items 1–5 above
land. The failure mode is now identified precisely enough to avoid: an
under-reservoired parameter set and a bandwidth too narrow to reach ωτ₂ ≈ 1
produce a confident, wrong, unpublishable answer.

**Reproduce:** `PYTHONPATH=src:. python -m pytest research/laod_tau2/tests -q`,
then the three `study_*.py` modules (the bandwidth study takes ~25 min).
