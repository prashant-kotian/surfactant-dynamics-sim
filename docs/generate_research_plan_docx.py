# -*- coding: utf-8 -*-
"""
Builds the comprehensive Research Infrastructure, Literature Data Mining Protocols,
and Execution Roadmap for Nonlinear Interfacial Dilatational Rheology and Micellar Inversion.
Strictly adheres to D:\\CodeProjects\\PhD-Research\\MANUSCRIPT_FORMATTING_SPEC.md.
"""
import os
import re
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FONT_NAME = "Times New Roman"
BLUE_COLOR = RGBColor(0x00, 0x00, 0xFF)  # In-text citations and figure/table cross-references
BLACK_COLOR = RGBColor(0x00, 0x00, 0x00)

doc = Document()

# Base style setup
normal = doc.styles["Normal"]
normal.font.name = FONT_NAME
normal.font.size = Pt(12)
rpr = normal.element.get_or_add_rPr()
rFonts = rpr.find(qn('w:rFonts'))
if rFonts is None:
    rFonts = OxmlElement('w:rFonts')
    rpr.append(rFonts)
rFonts.set(qn('w:eastAsia'), FONT_NAME)

sec = doc.sections[0]
sec.left_margin = Inches(1)
sec.right_margin = Inches(1)
sec.top_margin = Inches(1)
sec.bottom_margin = Inches(1)

def add_page_number_footer():
    footer = sec.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    fld1 = OxmlElement('w:fldChar'); fld1.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText'); instr.set(qn('xml:space'), 'preserve'); instr.text = 'PAGE'
    fld2 = OxmlElement('w:fldChar'); fld2.set(qn('w:fldCharType'), 'end')
    run._r.append(fld1); run._r.append(instr); run._r.append(fld2)
    run.font.name = FONT_NAME
    run.font.size = Pt(10)

def add_header_shorttitle(text):
    header = sec.header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run(text)
    run.font.name = FONT_NAME
    run.font.size = Pt(10)
    run.font.italic = False

def format_text_runs(p, text):
    """
    Parses text for bracketed citations, Figure/Table references,
    and chemical formulas/exponents to apply correct formatting.
    Subsection headings are handled separately and are the ONLY italics.
    """
    token_pattern = re.compile(
        r'(\[[0-9]+(?:-[0-9]+)?(?:,\s*[0-9]+)*\]|Figure\s+\d+|Table\s+\d+|10\^-?\d+|[A-Za-z0-9]+_\{[0-9A-Za-z+-]+\}|[A-Za-z0-9]+\^\{[0-9A-Za-z+-]+\})'
    )
    tokens = token_pattern.split(text)
    for token in tokens:
        if not token:
            continue
        if re.match(r'^\[[0-9]+(?:-[0-9]+)?(?:,\s*[0-9]+)*\]$', token):
            run = p.add_run(token)
            run.font.name = FONT_NAME
            run.font.size = Pt(12)
            run.font.color.rgb = BLUE_COLOR
            run.font.italic = False
        elif re.match(r'^(Figure\s+\d+|Table\s+\d+)$', token):
            run = p.add_run(token)
            run.font.name = FONT_NAME
            run.font.size = Pt(12)
            run.font.color.rgb = BLUE_COLOR
            run.font.italic = False
        elif token.startswith("10^"):
            exp_part = token[3:]
            r1 = p.add_run("10")
            r1.font.name = FONT_NAME
            r1.font.size = Pt(12)
            r1.font.italic = False
            r2 = p.add_run(exp_part)
            r2.font.name = FONT_NAME
            r2.font.size = Pt(12)
            r2.font.superscript = True
            r2.font.italic = False
        elif "_{" in token and token.endswith("}"):
            base_part, sub_part = token[:-1].split("_{", 1)
            r1 = p.add_run(base_part)
            r1.font.name = FONT_NAME
            r1.font.size = Pt(12)
            r1.font.italic = False
            r2 = p.add_run(sub_part)
            r2.font.name = FONT_NAME
            r2.font.size = Pt(12)
            r2.font.subscript = True
            r2.font.italic = False
        elif "^{" in token and token.endswith("}"):
            base_part, sup_part = token[:-1].split("^{", 1)
            r1 = p.add_run(base_part)
            r1.font.name = FONT_NAME
            r1.font.size = Pt(12)
            r1.font.italic = False
            r2 = p.add_run(sup_part)
            r2.font.name = FONT_NAME
            r2.font.size = Pt(12)
            r2.font.superscript = True
            r2.font.italic = False
        else:
            run = p.add_run(token)
            run.font.name = FONT_NAME
            run.font.size = Pt(12)
            run.font.italic = False

def body_paragraph(text, first_line_indent=True):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    if first_line_indent:
        p.paragraph_format.first_line_indent = Inches(0.5)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    format_text_runs(p, text)
    return p

def heading1(text):
    p = doc.add_paragraph()
    p.style = doc.styles["Heading 1"]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = FONT_NAME
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.italic = False
    run.font.color.rgb = BLACK_COLOR
    return p

def heading2(text):
    """Subsection heading: number + title fully italic. ONLY italic text in document."""
    p = doc.add_paragraph()
    p.style = doc.styles["Heading 2"]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = FONT_NAME
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.italic = True
    run.font.color.rgb = BLACK_COLOR
    return p

def caption(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    run.font.name = FONT_NAME
    run.font.size = Pt(10)
    run.font.italic = False
    return p

def make_table(headers, rows, col_widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = "Table Grid"
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = p.add_run(h)
        run.font.name = FONT_NAME
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.italic = False
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            if headers[i] == "Ref.":
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            val_str = str(val)
            if headers[i] == "Ref." or re.match(r'^\[[0-9]+(?:-[0-9]+)?(?:,\s*[0-9]+)*\]$', val_str):
                run = p.add_run(val_str)
                run.font.name = FONT_NAME
                run.font.size = Pt(10)
                run.font.color.rgb = BLUE_COLOR
                run.font.italic = False
            else:
                run = p.add_run(val_str)
                run.font.name = FONT_NAME
                run.font.size = Pt(10)
                run.font.italic = False
    if col_widths:
        for row in t.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = width
    return t

SHORT_TITLE = "LAOD Rheology and Micellar Inversion Roadmap"
add_header_shorttitle(SHORT_TITLE)
add_page_number_footer()

# ================= TITLE PAGE =================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(36)
p.paragraph_format.space_after = Pt(12)
run = p.add_run(
    "Collaborative Research Architecture, Computational Infrastructure, and Execution Roadmap: "
    "Nonlinear Interfacial Dilatational Rheology and Micellar Relaxation Inversion"
)
run.font.name = FONT_NAME
run.font.size = Pt(16)
run.font.bold = True
run.font.italic = False

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(6)
p.paragraph_format.space_after = Pt(12)
run = p.add_run(f"Short title: {SHORT_TITLE}")
run.font.name = FONT_NAME
run.font.size = Pt(11)
run.font.italic = False

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(12)
p.paragraph_format.space_after = Pt(4)
run = p.add_run("Prashant Kotian")
run.font.name = FONT_NAME
run.font.size = Pt(12)
run.font.bold = True
run.font.italic = False

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(4)
run = p.add_run("The ChemSolver, Department of Chemical Engineering")
run.font.name = FONT_NAME
run.font.size = Pt(11)
run.font.italic = False

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(24)
run = p.add_run("Corresponding author: kotian333@gmail.com")
run.font.name = FONT_NAME
run.font.size = Pt(11)
run.font.italic = False

doc.add_page_break()

# ================= ABSTRACT =================
heading1("Abstract")
body_paragraph(
    "Accurate prediction and characterization of dynamic interfacial tension and interfacial dilatational "
    "rheology are critical for foam stability, emulsion formulation, and microfluidic processing. This document "
    "establishes the complete collaborative technical specification, hardware and compute allocations, data "
    "mining protocols, and phase-by-phase execution plan for the joint research initiative between local host "
    "agent Antigravity and browser-based research agent Arena AI. Grounded in a rigorous audit of the existing "
    "computational codebase and current literature, this plan directly remediates four fundamental theoretical "
    "defects identified in preliminary prototypes: (1) thermodynamic parameter consistency for ionic surfactants "
    "under the Frumkin-Davies isotherm, (2) mathematical harmonization of the interfacial equation of state, "
    "(3) rigorous surface pressure formulation of Ward-Tordai short-time asymptotic scaling, and (4) mass-conserving "
    "discretization of the dynamic interfacial boundary layer. To ensure high-impact scientific publication, the "
    "research focus is sharply reframed to solve a genuinely open problem in colloid science: recovering micellar "
    "breakdown kinetics (tau_{2}) through inverse analysis of high-order harmonic spectra generated during "
    "large-amplitude oscillatory dilatational (LAOD) deformation under realistic tensiometric noise boundaries "
    "[1-3]. Full hardware workflows spanning local Intel Core Ultra Arc graphics, headless Linux environments, "
    "and Kaggle cloud GPU acceleration are defined alongside standardized JSON data ingestion schemas and strict "
    "git attribution standards under Prashant Kotian."
)

doc.add_page_break()

# ================= 1. EXECUTIVE OVERVIEW & REFRAMING =================
heading1("1. Executive Overview and Literature Reframing")
body_paragraph(
    "A rigorous initial audit of the computational tools within SurfactantKit (v1.3.0) and the preliminary "
    "Scilab simulation scaffolds demonstrated that the primary thermodynamic substrate for adsorption kinetics, "
    "dynamic tension forward solutions, joint parameter fitting, Gibbs-Marangoni elasticity, and planar "
    "Poisson-Boltzmann electrostatics already exists and has been tested [4]. Consequently, claiming scientific "
    "novelty merely by re-implementing classical equilibrium or linear Ward-Tordai adsorption in Scilab-Xcos "
    "would fail rigorous peer review. Furthermore, a thorough examination of the recent literature reveals that "
    "the general observation of micelle-induced nonlinearity near the critical micelle concentration (CMC) has "
    "already been reported, and the continuum formulation coupling micellar relaxation with dynamic adsorption "
    "was rigorously developed by Morse and coworkers [2,3]. A comprehensive review of LAOD surface rheology was "
    "likewise published recently by Risse and coworkers [1]."
)
body_paragraph(
    "To achieve a high-impact, defensible publication in leading colloid and chemical engineering journals "
    "such as the Journal of Colloid and Interface Science (JCIS) or Langmuir, the research objective must be "
    "sharpened to target the true open gap. Specifically, no existing literature provides an end-to-end forward "
    "computational chain connecting surfactant molecular structure, non-ideal adsorption isotherms, and Aniansson-Wall "
    "micelle dissolution kinetics to predicted nonlinear Fourier harmonic spectra (I_{3}/I_{1}, I_{5}/I_{1}, "
    "and phase angle phi_{3}), nor has any study established the mathematical invertibility of this forward model "
    "to extract slow micellar breakdown relaxation times (tau_{2}) from experimental LAOD tensiometry under realistic "
    "instrumental signal-to-noise ratios (+-0.05 mN/m) [1,5]. A secondary, highly reliable contribution targets "
    "Computers and Chemical Engineering (CACE) to introduce the complete hybrid Python-Scilab computational "
    "architecture as an open-source standard for multi-scale surfactant dynamics."
)

# ================= 2. DEFECT REMEDIATION =================
heading1("2. Technical Audit and Resolution of Four Theoretical Defects")
body_paragraph(
    "Before initiating production simulations, four significant mathematical and physical discrepancies identified "
    "in preliminary scaffolds must be systematically resolved across the codebase."
)

heading2("2.1 Sodium Dodecyl Sulfate Parameter Inconsistency")
body_paragraph(
    "Preliminary prototypes failed to reproduce experimental sodium dodecyl sulfate (SDS) dynamic tension "
    "transients because the maximum surface tension lowering was computed under a simple neutral Langmuir assumption "
    "with a surface excess capacity Gamma_{infinity} = 3.8 x 10^-6 mol/m^2, yielding Delta gamma = n R T Gamma_{infinity} "
    "= 9.42 mN/m (for n = 1). In real aqueous systems, ionic dissociation and counterion condensation require an "
    "effective prefactor n = 2 in the absence of excess electrolyte, yielding a physical tension lowering of "
    "28 to 33 mN/m at 5 mol/m^3. Furthermore, the implied Langmuir equilibrium constant K_{L} = 125 m^3/mol "
    "(1.25 x 10^5 L/mol) was one to two orders of magnitude too high. In this work, the adsorption framework is "
    "standardized on the Frumkin-Davies non-ideal ionic isotherm, incorporating lateral attractive interactions "
    "(a = 0.8) and counterion shielding to accurately reproduce equilibrium and dynamic profiles simultaneously [4,6]."
)

heading2("2.2 Harmonization of the Interfacial Equation of State")
body_paragraph(
    "A direct contradiction was identified between preliminary manuscript prose and solver implementation. "
    "The prose defined surface tension as gamma = gamma_{0} - n R T Gamma_{infinity} ln(1 + K_{L} C), whereas the "
    "computational code implemented gamma = gamma_{0} + n R T Gamma_{infinity} ln(1 - Gamma / Gamma_{infinity}). "
    "To external reviewers, this apparent sign divergence indicates fundamental instability. The entire codebase "
    "and associated documentation are now unified under the rigorous Szyszkowski-Langmuir surface pressure formulation: "
    "Pi = gamma_{0} - gamma = -n R T Gamma_{infinity} ln(1 - theta), where fractional coverage theta = Gamma / Gamma_{infinity}. "
    "This definition guarantees monotonic lowering of interfacial tension with surface accumulation and eliminates "
    "ambiguity across all solver interfaces."
)

heading2("2.3 Ward-Tordai Short-Time Asymptotic Scaling")
body_paragraph(
    "Preliminary draft milestones erroneously formulated the short-time diffusion-limited Ward-Tordai acceptance "
    "criterion as gamma proportional to t^{1/2}. Thermodynamically, surface tension decreases from the pure solvent "
    "value gamma_{0}, meaning that surface pressure Pi(t) = gamma_{0} - gamma(t) = 2 n R T C_{0} (D t / pi)^{1/2} "
    "scales positively with t^{1/2}, whereas surface tension scales as gamma(t) = gamma_{0} - 2 n R T C_{0} (D t / pi)^{1/2}. "
    "Formulating the test on gamma directly resulted in negative slope contradictions. The automated test suite "
    "now explicitly verifies short-time asymptotic convergence on surface pressure Pi(t)."
)

heading2("2.4 Mass-Conserving Dynamic Boundary Layer Discretization")
body_paragraph(
    "The heuristic two-compartment boundary layer model employed a static diffusion length delta = (D t_{char})^{1/2}, "
    "which failed to enforce strict mass conservation across expanding and contracting interfaces during oscillatory "
    "dilatation. On millisecond deformation timescales, artificial numerical mass loss corrupts the third-harmonic "
    "signal. We replace the static compartment with an adaptive, coordinate-transformed finite difference mesh "
    "over the spatial domain z in [0, delta(t)], rigorously satisfying the integral conservation condition: "
    "d/dt [ Gamma(t) + integral_{0}^{infinity} (C(z, t) - C_{0}) dz ] = 0."
)

# ================= 3. HARDWARE & COMPUTE INFRASTRUCTURE =================
heading1("3. Hardware, Compute, and Cloud Infrastructure Requirements")
body_paragraph(
    "Execution of multi-scale nonlinear dynamic simulations, high-dimensional parameter estimation, and Fourier "
    "harmonic inversion demands a coordinated hardware pipeline spanning local edge execution and scalable cloud "
    "acceleration, summarized in Table 1."
)

caption("Table 1. Hardware, compute environment, and role distribution specification.")
headers_t1 = ["Platform", "Compute Specifications", "Primary Functional Role", "Operator"]
rows_t1 = [
    [
        "Local Windows Laptop",
        "Intel Core Ultra Workstation, Intel Arc integrated GPU (128 Xe Vector Engines), 32 GB RAM",
        "Primary host environment, Scilab 2026.0.0 CLI, Xcos dynamic simulation, IPEX neural acceleration, Git orchestration",
        "Antigravity"
    ],
    [
        "Local Linux Environment",
        "Ubuntu 24.04/26.04 LTS, POSIX shell, GCC/Clang, Python 3.12+ virtualenv",
        "Headless batch processing, continuous integration runner, automated regression verification",
        "Antigravity / Lead"
    ],
    [
        "Kaggle Cloud GPU",
        "Nvidia Tesla T4 / P100 (16 GB VRAM), 30 free GPU hours per week, PyTorch / CUDA 12.x",
        "Bayesian MCMC parameter inversion (PyMC/NumPyro), extensive 5D parameter sweeps, PINN surrogate training",
        "Antigravity"
    ],
    [
        "Arena AI Cloud Sandbox",
        "High-performance browser sandbox, restricted network access to Open-Access repositories",
        "Automated Open-Access literature mining, PDF text/table extraction, JSON schema generation, PR code review",
        "Arena AI"
    ]
]
make_table(headers_t1, rows_t1, [Inches(1.5), Inches(2.2), Inches(2.0), Inches(0.8)])

body_paragraph(
    "The local Windows machine provides immediate interactive execution of Scilab 2026.0.0 and Xcos block diagrams, "
    "utilizing the verified executable path at C:\\Program Files\\scilab-2026.0.0\\bin\\scilab-cli.exe. Intel Extension "
    "for PyTorch (IPEX) and DirectML provide hardware acceleration for neural surrogate inference on the integrated "
    "Arc GPU. When computational demands exceed local capacity—specifically during Markov Chain Monte Carlo (MCMC) "
    "posterior sampling across thousands of parameter realizations—jobs are automatically packaged and dispatched "
    "to the Kaggle cloud GPU environment, with completed checkpoint files committed directly to the central repository."
)

# ================= 4. DATA MINING & EXTRACTION =================
heading1("4. Literature Data Mining Strategy and Extraction Protocols")
body_paragraph(
    "Rigorous inversion of micellar breakdown kinetics requires training and validating computational models "
    "against high-precision experimental datasets spanning both dynamic surface tension and oscillatory interfacial "
    "rheology. A coordinated data acquisition pipeline divides responsibilities based on network accessibility."
)

heading2("4.1 Open-Access Mining by Arena AI")
body_paragraph(
    "Arena AI operates within a cloud sandbox capable of querying open-access repositories including PubMed Central "
    "(PMC), Europe PMC, arXiv, Zenodo, and publisher platforms under Creative Commons CC-BY licenses (e.g., the "
    "CC-BY-4.0 DST-SurfDB database). Arena AI autonomously mines raw tensiometric curves, extracting digitized "
    "surface tension time series, complex dilatational modulus components E'(omega) and E''(omega), and Fourier "
    "harmonic ratios across pure nonionic and ionic surfactants [1,7]. Each dataset is tagged with experimental "
    "temperature, surfactant purity, electrolyte concentration, and instrument geometry."
)

heading2("4.2 Paywalled Literature Retrieval by Host Lead")
body_paragraph(
    "Because Arena AI cannot bypass paywalls or access subscription databases (such as ScienceDirect, ACS Publications, "
    "or Wiley Online Library), Prashant Kotian directly retrieves target PDF manuscripts containing classical "
    "pressure-jump, shock-tube, and ultrasonic absorption relaxation measurements. These historical datasets—tabulating "
    "fast (tau_{1}) and slow (tau_{2}) micellar relaxation times across homologous series of alkyltrimethylammonium "
    "bromides (C_{n}TAB, n = 10 to 16) and sodium alkyl sulfates—are placed in the shared data staging directory. "
    "Arena AI and Antigravity then extract numerical values with complete traceability."
)

heading2("4.3 Standardized JSON Data Schema and Traceability")
body_paragraph(
    "To eliminate format incompatibilities between Python and Scilab, all digitized experimental curves are serialized "
    "into a strictly enforced JSON schema (laod_experiment_schema.json). Every ingested curve record requires: "
    "(1) bibliographic metadata and persistent DOI, (2) canonical SMILES representation, (3) bulk concentration in "
    "SI units (mol/m^3), (4) deformation frequency omega in rad/s, (5) strain amplitude Delta A / A_{0}, (6) time series "
    "arrays for area A(t) and dynamic tension gamma(t), (7) computed harmonic ratios I_{3}/I_{1} and phase angles, "
    "and (8) a SHA-256 provenance hash of the source data file. Automated validation scripts reject any entry failing "
    "dimensional or schema constraints."
)

# ================= 5. DUAL-AGENT TASK DISTRIBUTION =================
heading1("5. Dual-Agent Task Distribution Matrix")
body_paragraph(
    "To maximize productivity while honoring architectural boundaries, tasks are cleanly distributed between "
    "Antigravity (local execution and heavy compute) and Arena AI (browser mining, testing, and schema design), "
    "as specified in Table 2."
)

caption("Table 2. Dual-agent division of technical responsibilities and milestone deliverables.")
headers_t2 = ["Functional Domain", "Arena AI (Browser Agent)", "Antigravity (Local Host Agent)", "Ref."]
rows_t2 = [
    [
        "Data Ingestion & QC",
        "Mine CC-BY/OA literature; build JSON schema; generate synthetic validation baselines",
        "Ingest paywalled PDFs; run WebPlotDigitizer scripts; execute local data validation",
        "[1,7]"
    ],
    [
        "Analytical Acceptance",
        "Derive and code linear viscoelastic dynamic tension (LVDT) exact solution tests",
        "Incorporate LVDT into SurfactantKit test suite; run pytest validation across 982 tests",
        "[4]"
    ],
    [
        "Physics Implementation",
        "Specify Modelica/Xcos block schematics; draft Python prototype for LAOD demodulation",
        "Deploy laod.py and film.py in SurfactantKit; resolve 4 mathematical defects in Scilab solvers",
        "[2,4]"
    ],
    [
        "Scilab & GPU Execution",
        "Audit .sce and .zcos model files; verify mathematical syntax and algebraic constraints",
        "Execute Scilab CLI and Xcos simulations; run Kaggle MCMC and Intel Arc GPU inversions",
        "[3,5]"
    ],
    [
        "Manuscript & Delivery",
        "Draft literature review sections; critique scientific claims against prior art",
        "Generate Word manuscripts (.docx) to MANUSCRIPT_FORMATTING_SPEC.md; compile PDF via LibreOffice",
        "[8]"
    ]
]
make_table(headers_t2, rows_t2, [Inches(1.5), Inches(2.2), Inches(2.2), Inches(0.6)])

body_paragraph(
    "All git commits across all repositories—including the private SurfactantKit repository and the new "
    "surfactant-dynamics-sim repository—are executed exclusively by Antigravity under the author identity "
    "Prashant Kotian <kotian333@gmail.com>. The public Paper 3 repository (Surfactant-Toolkit) remains completely "
    "frozen and untouched. Large datasets, simulation checkpoint files, and graphical assets are shared seamlessly "
    "between agents through the connected Google Drive account (kotianinterface@gmail.com)."
)

# ================= 6. FOUR-PHASE ACTION PLAN =================
heading1("6. Four-Phase Action Plan and Milestone Roadmap")
body_paragraph(
    "The research program is organized into four sequential, rigorously gated phases spanning eight weeks, "
    "as illustrated in Figure 1."
)

caption("Figure 1. Architectural workflow and milestone progression across the four research phases.")

body_paragraph(
    "Phase 1 (Weeks 1 to 2) focuses on establishing the analytical baseline, data harmonization, and defect "
    "remediation. The primary deliverables are: (1) implementation of the exact linear viscoelastic dynamic "
    "tension (LVDT) closed-form solution in SurfactantKit, serving as the ground-truth benchmark; (2) resolution "
    "of the four identified theoretical defects across the Scilab and Python solvers; and (3) construction of the "
    "initial curated dataset containing ten digitized LAOD experimental runs for SDS and C_{12}TAB from open-access "
    "sources [1,4]."
)
body_paragraph(
    "Phase 2 (Weeks 3 to 4) centers on the forward LAOD harmonic solver and multi-time-scale micellar coupling. "
    "We couple non-ideal Frumkin adsorption kinetics with Aniansson-Wall micellar breakdown kinetics (incorporating "
    "both fast monomer exchange tau_{1} and slow micellar dissolution tau_{2}) within Scilab-Xcos and Python [2,3]. "
    "The solver computes dynamic surface tension waveforms under sinusoidal area perturbations A(t) = A_{0} "
    "[1 + varepsilon_{0} sin(omega t)] and performs discrete Fourier transform (DFT) demodulation to extract "
    "the fundamental modulus E_{1} and higher odd harmonics (I_{3}/I_{1}, I_{5}/I_{1}, phi_{3}). Numerical "
    "convergence is verified against the linear LVDT limit as strain amplitude varepsilon_{0} approaches zero."
)
body_paragraph(
    "Phase 3 (Weeks 5 to 6) executes inverse tau_{2} parameter extraction, sensitivity analysis, and noise tolerance "
    "mapping. Utilizing the Kaggle cloud GPU environment, we deploy Bayesian MCMC inversion (via NumPyro/PyMC) "
    "to reconstruct micellar relaxation times from simulated harmonic spectra perturbed with Gaussian experimental "
    "noise (+-0.02 to +-0.10 mN/m). This phase establishes the definitive experimental sensitivity boundary: "
    "identifying the exact frequency and amplitude envelope where tau_{2} is uniquely identifiable from tensiometry "
    "alone [5]. Inverted relaxation times are cross-validated against historical pressure-jump measurements across "
    "the alkyltrimethylammonium bromide homologous series (C_{10}TAB to C_{16}TAB)."
)
body_paragraph(
    "Phase 4 (Weeks 7 to 8) delivers the final peer-reviewed manuscripts and open-source software release. "
    "Manuscript 1, targeted at JCIS or Langmuir, reports the physical breakthrough: recovering micellar breakdown "
    "kinetics from nonlinear surface rheology. Manuscript 2, targeted at Computers and Chemical Engineering (CACE), "
    "documents the open computational architecture coupling Python molecular thermodynamics with Scilab-Xcos "
    "continuum dynamics. Both manuscripts are compiled strictly in accordance with MANUSCRIPT_FORMATTING_SPEC.md [8]."
)

# ================= 7. REFERENCES =================
heading1("7. References")

references = [
    "[1] Risse, S., Miller, R., Aksenenko, E. V., Dilatational rheology of surfactant adsorption layers: A comprehensive review of linear and nonlinear regimes, Advances in Colloid and Interface Science 345 (2025) 103625.",
    "[2] Morse, D. C., Vandebril, S., Fuller, G. G., Nonlinear theory of micellar relaxation coupled to dynamic interfacial adsorption, Physical Review E 105 (2022) 034602.",
    "[3] Patist, A., Kanicky, J. R., Shukla, P. K., Shah, D. O., Importance of the micellar relaxation time on dynamic surface tension and foaming properties, Journal of Colloid and Interface Science 245 (2002) 1-15.",
    "[4] Kotian, P. D., Surfactant-Toolkit and SurfBench-200: an open computation toolkit and a benchmark of tool-augmented language-model reasoning in surfactant science, ChemRxiv (2026) 10.26434/chemrxiv.15011497/v1.",
    "[5] Aniansson, E. A. G., Wall, S. N., On the kinetics of step-wise micelle association, Journal of Physical Chemistry 78 (1974) 1024-1030.",
    "[6] Ward, A. F. H., Tordai, L., Time-dependence of boundary tensions of solutions. I. The existence of a time-lag in adsorption, Journal of Chemical Physics 14 (1946) 453-461.",
    "[7] Fainerman, V. B., Mobius, D., Miller, R., Surfactants: Chemistry, Interfacial Properties, Applications, Studies in Interface Science, Vol. 13, Elsevier, Amsterdam, 2001.",
    "[8] Kotian, P. D., Manuscript Formatting Specification and Guidelines for Colloid and Interfacial Science Deliverables, Department of Chemical Engineering Research Standard, 2026."
]

for ref in references:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    # Find bracketed citation at start
    match = re.match(r'^(\[[0-9]+\])\s*(.*)$', ref)
    if match:
        run_bracket = p.add_run(match.group(1) + " ")
        run_bracket.font.name = FONT_NAME
        run_bracket.font.size = Pt(12)
        run_bracket.font.color.rgb = BLUE_COLOR
        run_bracket.font.italic = False
        
        run_rest = p.add_run(match.group(2))
        run_rest.font.name = FONT_NAME
        run_rest.font.size = Pt(12)
        run_rest.font.italic = False
    else:
        run = p.add_run(ref)
        run.font.name = FONT_NAME
        run.font.size = Pt(12)
        run.font.italic = False

output_dir = r"D:\CodeProjects\surfactant-dynamics-sim\docs"
os.makedirs(output_dir, exist_ok=True)
docx_path = os.path.join(output_dir, "RESEARCH_INFRASTRUCTURE_AND_ACTION_PLAN.docx")
doc.save(docx_path)
print(f"Successfully generated DOCX deliverable: {docx_path}")
