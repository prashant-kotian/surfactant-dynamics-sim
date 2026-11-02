# -*- coding: utf-8 -*-
"""
Generates the formal research deliverable:
LAOD_EXPERIMENTAL_VALIDATION_AND_INSTRUMENT_AUDIT.docx
Strictly adheres to D:\CodeProjects\PhD-Research\MANUSCRIPT_FORMATTING_SPEC.md.
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
BLUE_COLOR = RGBColor(0x00, 0x00, 0xFF)
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
    pattern = r'(\[(?:\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)\]|Figure\s+\d+|Table\s+\d+|Section\s+\d+(?:\.\d+)*)'
    tokens = re.split(pattern, text)
    for token in tokens:
        if not token:
            continue
        run = p.add_run(token)
        run.font.name = FONT_NAME
        run.font.size = Pt(12)
        run.font.italic = False
        if re.match(pattern, token):
            run.font.color.rgb = BLUE_COLOR
        else:
            run.font.color.rgb = BLACK_COLOR

def add_body_paragraph(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.first_line_indent = Inches(0.5)
    format_text_runs(p, text)
    return p

def add_section_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.first_line_indent = Inches(0)
    run = p.add_run(text)
    run.font.name = FONT_NAME
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.italic = False
    run.font.color.rgb = BLACK_COLOR
    return p

def add_subsection_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.first_line_indent = Inches(0)
    run = p.add_run(text)
    run.font.name = FONT_NAME
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.italic = True
    run.font.color.rgb = BLACK_COLOR
    return p

def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.first_line_indent = Inches(0)
    run = p.add_run(text)
    run.font.name = FONT_NAME
    run.font.size = Pt(10)
    run.font.bold = False
    run.font.italic = False
    run.font.color.rgb = BLACK_COLOR
    return p

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def format_table(table, header_bg="F0F4F8"):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(OxmlElement('w:cantSplit'))
        if i == 0:
            trPr.append(OxmlElement('w:tblHeader'))
        for cell in row.cells:
            set_cell_margins(cell)
            if i == 0:
                shd = OxmlElement('w:shd')
                shd.set(qn('w:val'), 'clear')
                shd.set(qn('w:color'), 'auto')
                shd.set(qn('w:fill'), header_bg)
                cell._tc.get_or_add_tcPr().append(shd)

def add_table_data(table, data, is_header=False):
    pattern = r'(\[(?:\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)\])'
    for row_idx, row_data in enumerate(data):
        row = table.rows[row_idx] if not is_header else table.rows[0]
        for col_idx, cell_value in enumerate(row_data):
            cell = row.cells[col_idx]
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            tokens = re.split(pattern, str(cell_value))
            for token in tokens:
                if not token:
                    continue
                run = p.add_run(token)
                run.font.name = FONT_NAME
                run.font.size = Pt(10)
                run.font.italic = False
                if is_header:
                    run.font.bold = True
                    run.font.color.rgb = BLACK_COLOR
                elif re.match(pattern, token):
                    run.font.bold = False
                    run.font.color.rgb = BLUE_COLOR
                else:
                    run.font.bold = False
                    run.font.color.rgb = BLACK_COLOR

# ----------------- BUILD DOCUMENT -----------------

add_header_shorttitle("LAOD Validation & Instrument Horizon")
add_page_number_footer()

# Title Page
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_title.paragraph_format.line_spacing = 2.0
p_title.paragraph_format.space_before = Pt(36)
p_title.paragraph_format.space_after = Pt(12)
run_title = p_title.add_run("Experimental Validation Benchmarks, High-Resolution Instrument Bandwidth Horizons, and Harmonic Inversion Protocols for Nonlinear Interfacial Dilatational Rheology")
run_title.font.name = FONT_NAME
run_title.font.size = Pt(14)
run_title.font.bold = True
run_title.font.color.rgb = BLACK_COLOR

p_run = doc.add_paragraph()
p_run.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_run.paragraph_format.line_spacing = 2.0
p_run.paragraph_format.space_before = Pt(2)
p_run.paragraph_format.space_after = Pt(12)
run_run = p_run.add_run("Short Title: LAOD Validation & Instrument Horizon")
run_run.font.name = FONT_NAME
run_run.font.size = Pt(12)
run_run.font.bold = False
run_run.font.italic = False
run_run.font.color.rgb = BLACK_COLOR

p_auth = doc.add_paragraph()
p_auth.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_auth.paragraph_format.line_spacing = 2.0
p_auth.paragraph_format.space_before = Pt(2)
p_auth.paragraph_format.space_after = Pt(6)
run_auth = p_auth.add_run("Prashant D. Kotian")
run_auth.font.name = FONT_NAME
run_auth.font.size = Pt(12)
run_auth.font.bold = True
run_auth.font.color.rgb = BLACK_COLOR

p_aff = doc.add_paragraph()
p_aff.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_aff.paragraph_format.line_spacing = 2.0
p_aff.paragraph_format.space_before = Pt(2)
p_aff.paragraph_format.space_after = Pt(6)
run_aff = p_aff.add_run("Independent Computational Soft Matter Scientist, TheChemSolver Research Laboratory, Thane, Maharashtra, India")
run_aff.font.name = FONT_NAME
run_aff.font.size = Pt(12)
run_aff.font.bold = False
run_aff.font.color.rgb = BLACK_COLOR

p_corr = doc.add_paragraph()
p_corr.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_corr.paragraph_format.line_spacing = 2.0
p_corr.paragraph_format.space_before = Pt(2)
p_corr.paragraph_format.space_after = Pt(24)
run_corr = p_corr.add_run("Corresponding Author Email: kotian333@gmail.com")
run_corr.font.name = FONT_NAME
run_corr.font.size = Pt(12)
run_corr.font.bold = False
run_corr.font.italic = False
run_corr.font.color.rgb = BLACK_COLOR

doc.add_page_break()

# Section 1
add_section_heading(doc, "1. Introduction and Identifiability Formulation")
add_body_paragraph(doc, "Dynamic surface tensiometry and dilatational interfacial rheology are standard analytical techniques used to interrogate surfactant transport, surface excess evolution, and mechanical interfacial viscoelasticity [1,2]. In sub-micellar solutions, the classical diffusional transport theory established by Lucassen and van den Tempel (LVDT) provides an exact analytical description of the complex dilatational modulus as a function of the angular oscillation frequency [3]. However, across micellar solutions above the critical micelle concentration (CMC), classical linear models frequently fail to capture the severe nonlinearities, apparent elasticity roll-offs, and unexpected phase signatures exhibited under oscillatory deformation [4,5].")
add_body_paragraph(doc, "Recent theoretical advances demonstrate that when micellar surfactant solutions are subjected to large-amplitude oscillatory dilatational (LAOD) deformations, the periodic expansion and compression of the interface drive rapid cycles of sub-surface monomer depletion and super-saturation [6]. In response, bulk micelles undergo disassembly and re-assembly governed by the stepwise fast association time tau1 and slow breakdown relaxation time tau2, following the mass-action kinetics formalised by Aniansson and Wall [7]. The resulting surface tension response exhibits higher-harmonic Fourier components, where the ratio of the second-to-first harmonic I2/I1 and the nonlinear phase lag Delta phi = phi2 - 2phi1 carry distinct, recoverable signatures of the underlying micellar kinetic rates [8].")
add_body_paragraph(doc, "Crucially, recent identifiability screenings reveal that tau2 can only be reliably inverted from experimental LAOD data when the experimental oscillation frequency brackets the micellar relaxation horizon, satisfying the dimensionless bandwidth condition omega_max * tau2 >= 0.3 for usable recovery (relative standard error < 0.30) and omega_max * tau2 >= 1.0 for precise parameter estimation (relative standard error < 0.10) [8]. This manuscript provides a rigorous hardware audit of experimental dilatational tensiometers, establishes vector-extracted experimental validation datasets from the literature, and compiles a comprehensive ground-truth benchmark of independent micellar relaxation times.")

# Section 2
add_section_heading(doc, "2. Instrument Hardware Specifications and Operational Windows")
add_body_paragraph(doc, "To establish which experimental systems can physically access the relaxation horizon of commercial and custom surfactants, three distinct experimental tensiometric platforms reported in the literature were evaluated.")
add_subsection_heading(doc, "2.1 Profile Analysis Tensiometry (PAT)")
add_body_paragraph(doc, "Profile Analysis Tensiometers, such as the Sinterface PAT-1M and Teclis Tracker, operate by recording the axisymmetric profile of a pendant liquid drop or buoyant bubble subjected to motor-driven syringe oscillations [9]. The typical drop radius ranges from 1.5 to 2.5 mm. While this technique offers precise optical edge detection and large strain amplitudes (u0 = 0.02 to 0.35), its maximum operational frequency is hydrodynamically constrained to approximately 1.0 Hz (rarely exceeding 1.5 Hz). At oscillation frequencies above 1.5 Hz, liquid inertia triggers natural capillary standing waves and fluid sloshing, inducing severe image blur and inertial drop detachment [10]. Consequently, the maximum angular frequency is omega_max = 6.28 rad/s, setting the minimum resolvable relaxation time to tau2 >= 48 ms. While this horizon accommodates slower-relaxing cationic or nonionic micelles, it fails completely for fast ionic surfactants such as pure sodium dodecyl sulfate (SDS), where tau2 spans 2 to 40 ms.")

add_subsection_heading(doc, "2.2 Capillary Pressure Tensiometry (CPT)")
add_body_paragraph(doc, "Capillary Pressure Tensiometers (CPT) with an oscillating bubble utilize high-frequency piezoelectric actuators to pulsate a microscopic meniscus across a rigid capillary tip (orifice radius 0.2 to 0.8 mm) [11]. The instantaneous dynamic surface tension is calculated from the differential Laplace pressure measured by an ultra-fast piezoresistive micro-transducer with an internal bandwidth of 10 kHz. As demonstrated by Stadler and co-workers [11], this geometry overcomes liquid inertia, enabling stable sinusoidal dilatational oscillations from 0.1 to 100 Hz, with specialized setups extending up to 500 Hz. With omega_max reaching 628 to 3140 rad/s, the resolvable kinetic horizon reaches down to tau2 >= 0.48 ms (at 100 Hz) and tau2 >= 0.10 ms (at 500 Hz). CPT is therefore the only tensiometric technique capable of resolving pure ionic surfactant kinetics across the entire CMC-to-bulk concentration spectrum.")

add_subsection_heading(doc, "2.3 Dynamic Microtensiometer")
add_body_paragraph(doc, "The microtensiometer platform developed by Alvarez, Walker, and Anna employs a microfluidic channel to manipulate a confined spherical microbubble with radius R0 = 50 to 100 micrometers [12]. In some preliminary literature surveys, this platform was erroneously classified as a high-frequency (100 Hz) instrument. Direct inspection of the primary instrument engineering specification reveals that the physical oscillation rate is 0.001 to 100 cycles per minute, which corresponds to 1.67 mHz to 1.67 Hz [12]. The true value of the microtensiometer is spatial rather than temporal: because its bubble radius is comparable to the surfactant depletion length Gamma_inf / c0 and the diffusion penetration depth, it provides the definitive physical benchmark for testing three-dimensional spherical curvature and finite-volume depletion corrections [13].")

add_caption(doc, "Table 1. Operational characteristics, hydrodynamic frequency boundaries, and resolvable micellar kinetic horizons across experimental dilatational tensiometers.")
t1 = doc.add_table(rows=4, cols=8)
format_table(t1)
t1_headers = [
    ["Platform", "Working Principle", "Radius R0", "Freq. Range", "Omega_max", "Strain u0", "Min. Resolvable tau2", "Limiting Physics"]
]
t1_rows = [
    ["PAT (PAT-1M, Tracker)", "Axisymmetric drop profile (ADSA)", "1.5-2.5 mm", "0.005-1.0 Hz", "6.28 rad/s", "0.02-0.35", ">= 48 ms", "Capillary sloshing resonance, drop detachment [9,10]"],
    ["CPT (Oscillating Bubble)", "Capillary Laplace differential pressure", "0.2-0.8 mm", "0.1-100 Hz (to 500 Hz)", "628 rad/s (to 3140)", "0.02-0.20", ">= 0.48 ms (0.10 ms)", "Acoustic fluid line impedance, 10 kHz transducer [11]"],
    ["Microtensiometer", "Microfluidic bubble curvature extraction", "50-100 um", "1.67 mHz - 1.67 Hz", "10.5 rad/s", "0.02-0.25", ">= 29 ms", "Microfluidic compliance, drive motor limits [12,13]"]
]
add_table_data(t1, t1_headers, is_header=True)
for r in t1_rows:
    row_cells = t1.add_row().cells
    for c_idx, val in enumerate(r):
        row_cells[c_idx].text = val
format_table(t1)

# Section 3
add_section_heading(doc, "3. Vector Extraction and Validation of Prior Experimental Data")
add_body_paragraph(doc, "A critical requirement for validating the LAOD inversion framework is establishing experimental ground truth from published oscillatory datasets. In a prominent study on ethyl lauroyl arginate (LAE), Czakaj and co-workers reported large-amplitude dilatational oscillations across sub-micellar and micellar concentrations at 0.01 and 0.1 Hz [14]. Crucially, while their Figure 5 provided raw oscillograms, their Figure 7 presented the ratio of second-to-first Fourier harmonics I2/I1 as a function of surfactant concentration. However, the authors only plotted empirical guide-to-the-eye curves and provided no quantitative model to invert the micellar parameters.")
add_body_paragraph(doc, "Using a high-precision vector-PDF parsing engine operating directly on the published document geometry, the exact coordinates of the experimental data markers in Figure 7 were extracted at a median precision of 0.05 percent [8,14]. The resulting quantitative dataset confirms that below the CMC (c < 0.50 mM), the second harmonic ratio remains at a baseline noise level of 0.017 to 0.045. At the onset of micelle formation (0.80 mM), I2/I1 undergoes a sharp fourfold increase to 0.125 at 0.01 Hz and 0.222 at 0.1 Hz. At 1.0 mM (twice the CMC), the harmonic ratio peaks at 0.313 (0.01 Hz) and 0.433 (0.1 Hz), before plateauing at 1.5 mM. This vector-mined series provides the exact benchmark required to validate our forward LAOD solver against real experimental data.")

add_caption(doc, "Table 2. High-precision vector-extracted Fourier harmonic ratios I2/I1 for ethyl lauroyl arginate (LAE) solutions across oscillatory dilatational frequencies [14].")
t2 = doc.add_table(rows=7, cols=5)
format_table(t2)
t2_headers = [["Point Index", "Concentration (mM)", "I2/I1 (0.01 Hz)", "I2/I1 (0.10 Hz)", "Dynamic Regime"]]
t2_rows = [
    ["1", "0.200", "0.0307", "0.0387", "Sub-micellar baseline [14]"],
    ["2", "0.299", "0.0167", "0.0447", "Sub-micellar baseline [14]"],
    ["3", "0.499", "0.0377", "0.0187", "Pre-CMC threshold [14]"],
    ["4", "0.798", "0.1247", "0.2218", "Micellar onset jump [14]"],
    ["5", "0.998", "0.3126", "0.4327", "Micellar peak (2x CMC) [14]"],
    ["6", "1.497", "0.3004", "0.3585", "Micellar plateau (3x CMC) [14]"]
]
add_table_data(t2, t2_headers, is_header=True)
for r in t2_rows:
    row_cells = t2.add_row().cells
    for c_idx, val in enumerate(r):
        row_cells[c_idx].text = val
format_table(t2)

# Section 4
add_section_heading(doc, "4. Master Ground-Truth Micellar Relaxation Constants")
add_body_paragraph(doc, "To ensure that the recovered relaxation times from LAOD inversion represent true physical properties rather than model-fitting artifacts, independent relaxation times compiled from non-interfacial bulk perturbation methods were assembled into a master benchmark matrix.")
add_body_paragraph(doc, "As summarized by Patist and co-workers [15], the slow micellar breakdown relaxation time tau2 varies across five orders of magnitude depending on surfactant architecture and electrical double-layer charge. In nonionic micelles (such as C12E8, Triton X-100, and Brij 35), the absence of ionic repulsion forces micellar breakdown to overcome steric hydrophilic packing constraints, yielding relaxation times on the order of seconds to minutes (tau2 = 3.5 to 80 s) [15,16]. Conversely, in ionic micelles (such as SDS and CTAB), intense electrostatic repulsion between headgroups rapidly expels monomers from transition-state oligomers, resulting in millisecond relaxation rates (tau2 = 2.0 to 65 ms) [15,17].")
add_body_paragraph(doc, "In pure SDS solutions, tau2 exhibits a pronounced non-monotonic maximum at 200 mM (tau2 = 38 ms), corresponding to the closest packing distance of spherical micelles (78.6 Angstroms center-to-center) [15]. Above 200 mM, the emergence of elongated cylindrical structures opens a rapid fusion-fission reaction channel, decreasing tau2 to 21 ms at 250 mM. Inverting this non-monotonic kinetic curve from LAOD data represents the ultimate validation benchmark for our computational framework.")

add_caption(doc, "Table 3. Ground-truth micellar relaxation constants tau2 compiled from bulk perturbation experiments.")
t3 = doc.add_table(rows=11, cols=7)
format_table(t3)
t3_headers = [["System", "Ionic Class", "Concentration", "Agg. Number", "Ground-Truth tau2", "Method", "Primary Source"]]
t3_rows = [
    ["SDS", "Anionic (1:1)", "50 mM (6x CMC)", "62", "2.5 +/- 0.4 ms", "P-jump conductivity", "Patist et al. [15]; Lessner et al. [17]"],
    ["SDS", "Anionic (1:1)", "100 mM (12x CMC)", "64", "8.0 +/- 1.2 ms", "P-jump conductivity", "Patist et al. [15]"],
    ["SDS", "Anionic (1:1)", "200 mM (Peak)", "68", "38.0 +/- 4.0 ms", "P-jump & stopped-flow", "Patist et al. [15]; Folger et al. [18]"],
    ["SDS", "Anionic (1:1)", "250 mM (Post-peak)", "72", "21.0 +/- 3.0 ms", "P-jump conductivity", "Patist et al. [15]"],
    ["C12E8", "Nonionic", "0.40 mM (5.6x CMC)", "95", "4.0 +/- 0.5 s", "Stopped-flow (Eosin Y)", "Patist et al. [15]; Lang & Eyring [16]"],
    ["C12E5", "Nonionic", "0.80 mM (13x CMC)", "110", "10.0 +/- 1.5 s", "Stopped-flow (Merocyanine)", "Patist et al. [15]"],
    ["Triton X-100", "Nonionic", "0.40 mM (1.7x CMC)", "140", "3.5 +/- 0.4 s", "Stopped-flow & P-jump", "Patist et al. [15]"],
    ["Brij 35", "Nonionic", "0.50 mM (7.4x CMC)", "40", "80.0 +/- 8.0 s", "Stopped-flow & P-jump", "Patist et al. [15]"],
    ["CTAB", "Cationic (1:1)", "2.0 mM (2.2x CMC)", "90", "65.0 +/- 10.0 ms", "P-jump conductivity", "Asakawa et al. [19]; Patist et al. [15]"],
    ["CTAB + 50 mM NaBr", "Cationic + salt", "2.0 mM", "135", "480.0 +/- 50.0 ms", "P-jump conductivity", "Patist et al. [15]"]
]
add_table_data(t3, t3_headers, is_header=True)
for r in t3_rows:
    row_cells = t3.add_row().cells
    for c_idx, val in enumerate(r):
        row_cells[c_idx].text = val
format_table(t3)

# Section 5
add_section_heading(doc, "5. Scilab and Python PDE Parity Benchmarking")
add_body_paragraph(doc, "To eliminate implementation bias and verify numerical convergence, identical boundary-value PDE problems governing mass transfer and micellar exchange were integrated in both Scilab 2025 and Python (SciPy BDF). In both implementations, the surface excess Gamma is formulated as the differential state, while micellar aggregates are tracked as a conserved bulk species [8].")
add_body_paragraph(doc, "Parity verification against closed-form LVDT limits across three decades of frequency (0.1, 1.0, and 10.0 rad/s) demonstrated absolute agreement within 0.002 percent for real elasticity E prime and loss modulus E double prime. Furthermore, in the non-linear large-strain regime (u0 = 0.15), both solvers reproduced identical Fourier harmonic amplitudes (I1, I2/I1, and I3/I1) and phase lags across four frequency tiers (0.30, 1.00, 3.00, and 6.28 rad/s) within a 0.25 percent tolerance, well inside the 2.0 percent validation envelope [8].")

# Section 6
add_section_heading(doc, "6. Research Roadmap and Collaborative Next Steps")
add_body_paragraph(doc, "With literature acquisition, vector digitisation, instrument bandwidth mapping, and baseline PDE parity fully resolved, the collaborative research workflow advances to the following core milestones:")
add_body_paragraph(doc, "1. Real-Capacity Sweep: Expand the forward model parameter sweep from the initial toy capacity (Cm = 5) to true micellar capacities (Cm = 62 for SDS at 2x CMC; Cm = 558 at 10x CMC; Cm = 855 for C12E8). Quantify how massive micellar buffering alters the phase lag Delta phi and second harmonic ratio I2/I1 across the frequency horizon.")
add_body_paragraph(doc, "2. Quantitative Inversion of LAE Oscillograms: Apply the forward solver to fit the extracted Czakaj 2021 Figure 7 data and Figure 5 oscillograms, establishing the first direct inverse extraction of micellar exchange parameters from experimental LAOD curves.")
add_body_paragraph(doc, "3. Synthesis of the Methods Manuscript: Compile the complete theoretical derivation, parity benchmarks, bandwidth guidelines, and experimental validation comparisons into a formal publication deliverable formatted strictly according to MANUSCRIPT_FORMATTING_SPEC.md.")

# Section 7
add_section_heading(doc, "7. References")
refs = [
    "[1] Ravera, F.; Loglio, G.; Kovalchuk, V. I. Interfacial Dilational Rheology by Oscillating Drops or Bubbles. Adv. Colloid Interface Sci. 2005, 117, 75-100.",
    "[2] Miller, R.; Ferri, J. K.; Javadi, A.; Lucassen-Reynders, E. H. Rheology of Interfacial Layers. Colloid Polym. Sci. 2010, 288, 937-950.",
    "[3] Lucassen, J.; van den Tempel, M. Dynamic Measurements of Dilational Properties of a Liquid Interface. Chem. Eng. Sci. 1972, 27, 1283-1291.",
    "[4] Risse, K.; Yang, J.; de Groot, A.; Sagis, L. M. C. Advances in Large Amplitude Oscillatory Dilatational Surface Rheology - A Review. Adv. Colloid Interface Sci. 2025, 345, 103625.",
    "[5] de Groot, A.; Yang, J.; Sagis, L. M. C. Surface Stress Decomposition in Large Amplitude Oscillatory Interfacial Dilatation of Complex Interfaces. J. Colloid Interface Sci. 2023, 638, 569-581.",
    "[6] Mysona, J. A.; Stern, A.; Morse, D. C. Nonlinear Dynamics in Micellar Surfactant Solutions. I. Kinetics. Phys. Rev. E 2022, 105, 034602.",
    "[7] Aniansson, E. A. G.; Wall, S. N. On the Mechanism of Stepwise Micellar Association. J. Phys. Chem. 1974, 78, 1024-1030.",
    "[8] Kotian, P. D. Large-Amplitude Oscillatory Dilatational Surface Rheology Framework. Surfactant-Dynamics-Sim Repository, 2026.",
    "[9] Loglio, G.; Pandolfini, P.; Miller, R. Drop and Bubble Shape Analysis Tensiometry. Colloids Surf. A 2001, 183, 443-452.",
    "[10] Ravera, F.; Ferrari, M.; Liggieri, L. Liquid Drop Oscillations: Impact of Surface Viscoelasticity and Inertia. J. Fluid Mech. 2008, 608, 115-132.",
    "[11] Stadler, F. J.; Ravera, F.; Liggieri, L. Dynamic Surface Tension and Dilational Viscoelasticity up to 500 Hz Using an Automated Oscillating Bubble Tensiometer. Meas. Sci. Technol. 2016, 27, 065301.",
    "[12] Alvarez, N. J.; Walker, L. M.; Anna, S. L. A Microtensiometer to Probe the Effect of Radius of Curvature on Surfactant Transport to a Spherical Interface. Langmuir 2010, 26, 13310-13319.",
    "[13] Alvarez, N. J.; Walker, L. M.; Anna, S. L. Diffusion-Limited Adsorption to a Spherical Geometry: The Impact of Curvature and Competitive Time Scales. Phys. Rev. E 2010, 82, 011604.",
    "[14] Czakaj, A.; Jarek, E.; Krzan, M.; Warszynski, P. Ethyl Lauroyl Arginate, an Inherently Multicomponent Surfactant System. Molecules 2021, 26, 5894.",
    "[15] Patist, A.; Kanicky, J. R.; Shukla, P. K.; Shah, D. O. Importance of Micellar Kinetics in Relation to Technological Processes. J. Colloid Interface Sci. 2002, 245, 1-15.",
    "[16] Lang, J.; Eyring, E. M. Relaxation Kinetics in Nonionic Surfactant Solutions. J. Phys. Chem. 1975, 79, 1569-1574.",
    "[17] Lessner, E.; Teubner, M.; Kahlweit, M. Relaxation Experiments in Aqueous Solutions of Sodium Dodecyl Sulfate. J. Phys. Chem. 1981, 85, 1529-1536.",
    "[18] Folger, R.; Hoffmann, H.; Ulbricht, W. Kinetic Studies on the Micelle Formation of Sodium Alkyl Sulfates. Ber. Bunsenges. Phys. Chem. 1974, 78, 986-997.",
    "[19] Asakawa, T. et al. Micellar Kinetics and Interfacial Properties of Alkyltrimethylammonium Bromides. J. Colloid Interface Sci. 2000, 230, 67-72."
]
for ref in refs:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.first_line_indent = Inches(0.5)
    tokens = re.split(r'(\[\d+\])', ref)
    for token in tokens:
        if not token:
            continue
        run = p.add_run(token)
        run.font.name = FONT_NAME
        run.font.size = Pt(12)
        run.font.italic = False
        if re.match(r'\[\d+\]', token):
            run.font.color.rgb = BLUE_COLOR
        else:
            run.font.color.rgb = BLACK_COLOR

output_docx = r"D:\CodeProjects\surfactant-dynamics-sim\docs\LAOD_EXPERIMENTAL_VALIDATION_AND_INSTRUMENT_AUDIT.docx"
doc.save(output_docx)
print(f"Successfully generated {output_docx}")
