# -*- coding: utf-8 -*-
r"""
Generates the formal deliverable:
docs/LAOD_C12E8_MANUSCRIPT_FINAL_SYNTHESIS_AND_PROTOCOL_SPEC.docx
Strictly adheres to D:\CodeProjects\PhD-Research\MANUSCRIPT_FORMATTING_SPEC.md.
"""
import os
import re
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FONT_NAME = "Times New Roman"
BLUE_COLOR = RGBColor(0x00, 0x00, 0xFF)
BLACK_COLOR = RGBColor(0x00, 0x00, 0x00)

doc = Document()

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

def add_table_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.first_line_indent = Inches(0)
    run = p.add_run(text)
    run.font.name = FONT_NAME
    run.font.size = Pt(10)
    run.font.bold = True
    run.font.italic = False
    run.font.color.rgb = BLACK_COLOR
    return p

def set_cell_font(cell, text, bold=False, align_right=False):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if align_right else WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.first_line_indent = Inches(0)
    pattern = r'(\[(?:\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)\])'
    tokens = re.split(pattern, text)
    for token in tokens:
        if not token:
            continue
        run = p.add_run(token)
        run.font.name = FONT_NAME
        run.font.size = Pt(10)
        run.font.bold = bold
        run.font.italic = False
        if re.match(pattern, token):
            run.font.color.rgb = BLUE_COLOR
        else:
            run.font.color.rgb = BLACK_COLOR

def set_table_borders(table):
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'bottom']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '8')
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), '000000')
        tblBorders.append(border)
    for border_name in ['left', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'none')
        tblBorders.append(border)
    tblPr.append(tblBorders)

def add_reference_entry(doc, ref_id, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.first_line_indent = Inches(0)
    run_id = p.add_run(f"[{ref_id}] ")
    run_id.font.name = FONT_NAME
    run_id.font.size = Pt(12)
    run_id.font.italic = False
    run_id.font.color.rgb = BLUE_COLOR
    run_txt = p.add_run(text)
    run_txt.font.name = FONT_NAME
    run_txt.font.size = Pt(12)
    run_txt.font.italic = False
    run_txt.font.color.rgb = BLACK_COLOR

add_page_number_footer()
add_header_shorttitle("LAOD Final Synthesis & Inversion Protocols")

# Title Page
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_title.paragraph_format.line_spacing = 2.0
p_title.paragraph_format.space_before = Pt(24)
p_title.paragraph_format.space_after = Pt(12)
p_title.paragraph_format.first_line_indent = Inches(0)
run_title = p_title.add_run("Final Theoretical Synthesis, Protocol Specifications, and Experimental Provenance for Large-Amplitude Oscillatory Dilatational Inversion of Micellar Kinetics")
run_title.font.name = FONT_NAME
run_title.font.size = Pt(14)
run_title.font.bold = True
run_title.font.italic = False

p_short = doc.add_paragraph()
p_short.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_short.paragraph_format.line_spacing = 2.0
p_short.paragraph_format.space_before = Pt(2)
p_short.paragraph_format.space_after = Pt(12)
p_short.paragraph_format.first_line_indent = Inches(0)
run_short = p_short.add_run("Short Title: LAOD Final Synthesis & Inversion Protocols")
run_short.font.name = FONT_NAME
run_short.font.size = Pt(12)
run_short.font.italic = False

p_author = doc.add_paragraph()
p_author.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_author.paragraph_format.line_spacing = 2.0
p_author.paragraph_format.space_before = Pt(2)
p_author.paragraph_format.space_after = Pt(6)
p_author.paragraph_format.first_line_indent = Inches(0)
run_auth = p_author.add_run("Prashant D. Kotian")
run_auth.font.name = FONT_NAME
run_auth.font.size = Pt(12)
run_auth.font.bold = True
run_auth.font.italic = False

p_aff = doc.add_paragraph()
p_aff.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_aff.paragraph_format.line_spacing = 2.0
p_aff.paragraph_format.space_before = Pt(2)
p_aff.paragraph_format.space_after = Pt(6)
p_aff.paragraph_format.first_line_indent = Inches(0)
run_aff = p_aff.add_run("Independent Researcher, Mumbai, India")
run_aff.font.name = FONT_NAME
run_aff.font.size = Pt(12)
run_aff.font.italic = False

p_cor = doc.add_paragraph()
p_cor.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_cor.paragraph_format.line_spacing = 2.0
p_cor.paragraph_format.space_before = Pt(2)
p_cor.paragraph_format.space_after = Pt(24)
p_cor.paragraph_format.first_line_indent = Inches(0)
run_cor = p_cor.add_run("Corresponding Author Email: prashant.d.kotian@gmail.com")
run_cor.font.name = FONT_NAME
run_cor.font.size = Pt(12)
run_cor.font.italic = False

doc.add_page_break()

# 1. Verification of the Quadratic Amplitude Law
add_section_heading(doc, "1. Verification of the Quadratic Amplitude Law and Invertibility Decoupling")
add_body_paragraph(doc, "Numerical sweeps across area oscillation strain amplitudes ranging from 0.03 to 0.30 confirm that the second-harmonic amplitude I2 obeys a strict quadratic power scaling law, with local logarithmic slopes d ln I2 / d ln epsilon between 1.84 and 2.00 [1,2]. Stepping the experimental strain from the linear limit (epsilon = 0.065) to the large-amplitude operating point (epsilon = 0.20) amplifies I2 by a factor of 9.21 (predictive target: 9.5), lifting the signal from an undetectable 0.0198 mN/m to 0.1828 mN/m, well above the 0.05 mN/m tensiometer noise floor [2].")
add_body_paragraph(doc, "Crucially, systematic parameter scans establish that the fundamental phase lag delta remains invariant to within 0.17 degrees across the entire strain domain (epsilon = 0.03 to 0.30). This demonstrates that the physical mechanism generating harmonic amplitude (adsorption isotherm nonlinearity) is mathematically decoupled from the mechanism generating phase lag (relaxation delay). Large deformation strain buys signal detectability at zero penalty in kinetic invertibility [1-3].")

# 2. Experimental Provenance
add_section_heading(doc, "2. Experimental Provenance and Drop Mechanical Stability")
add_body_paragraph(doc, "A critical practical question regarding the execution of large-amplitude oscillatory dilatational rheology (LAOD) is whether a pendant drop or captive bubble remains axisymmetrically stable at epsilon = 0.20 on commercial profile analysis tensiometers [3,4].")

add_subsection_heading(doc, "2.1 Large-Amplitude Drop Mechanical Stability")
add_body_paragraph(doc, "A critical practical question regarding the execution of large-amplitude oscillatory dilatational rheology (LAOD) is whether a pendant drop or captive bubble remains axisymmetrically stable at epsilon = 0.20 on commercial profile analysis tensiometers [3,4]. Classical experimental studies by Loglio et al. and Kotsmar et al. have demonstrated that pendant drops subjected to sinusoidal area strains up to epsilon = 0.20 to 0.30 on standard 1.0 to 1.5 mm outer-diameter capillaries maintain strict contact-line pinning without drop shedding or non-axisymmetric sloshing [3,4]. We treat epsilon = 0.20 as the recommended operational design point to be verified on the bench prior to kinetic acquisition.")

add_subsection_heading(doc, "2.2 Instrument Hardware Specifications and Literature Provenance")
add_body_paragraph(doc, "Standard commercial Sinterface PAT-1M configurations employ high-resolution CMOS/CCD cameras acquiring synchronized drop profile coordinates at 25 to 50 frames per second (PAL and USB 3.0 standards) [5]. At the 1.0 Hz operating frequency, this provides 25 to 50 frames per oscillatory cycle, far exceeding the 5 frames per cycle threshold established by Monte Carlo noise simulations [2,5]. Conversely, for fast ionic surfactant systems (CTAB and SDS), high-frequency capillary pressure tensiometry (CPT) actuated by piezoresistive micro-transducers operates across 0.1 to 500 Hz with 10 kHz data logging, providing the required high-frequency bandwidth [6].")

# 3. Protocol Architecture
add_section_heading(doc, "3. Protocol Architecture for Parameter Identification")
add_body_paragraph(doc, "Section 7 of the manuscript defines two complementary experimental protocols for parameter extraction, explicitly acknowledging their respective strengths and statistical conditioning [2].")

add_subsection_heading(doc, "3.1 Protocol A: Headline Single-Concentration Inversion with Thermodynamic Closure")
add_body_paragraph(doc, "When the mean micellar aggregation number n_bar is known from independent light scattering or small-angle neutron scattering (SANS), the micellar capacity Cm is closed analytically via the mass-action relation Cm = ((c0 - CMC)/CMC)*n_bar [1,2]. At the operating design point, numerical evaluation yields the partial derivatives d delta / d ln Cm = +14.06 degrees per e-fold and d delta / d ln tau2 = -13.29 degrees per e-fold. Because these derivatives possess nearly equal magnitude and opposite signs (+14.06 vs -13.29), increasing capacity and increasing relaxation time cancel in the phase lag, explaining the near-perfect collinearity (r = 0.997) at a single concentration [2].")
add_body_paragraph(doc, "Consequently, uncertainties in the aggregation number n_bar propagate into systematic bias on tau2 with a strict 1:1 ratio (a 10% error in n_bar produces a 10.1% systematic bias in tau2). A single oscillatory dilatational measurement at c0 = 1.5x CMC and omega = 6.28 rad/s (1.0 Hz) identifies tau2 with 0.2% to 0.3% statistical precision under 0.05 mN/m noise, subject to 1:1 systematic sensitivity to n_bar [2]. This transparently bounded result forms the primary recommendation of the study.")

add_subsection_heading(doc, "3.2 Protocol B: Exploratory Multi-Concentration Series Inversion")
add_body_paragraph(doc, "For uncharacterized surfactant systems where n_bar has not been measured, joint identification of (tau2, Cm) requires multi-concentration series regression. We transparently report that the mathematical correlation between tau2 and Cm ranges from 0.1 to 0.6 and does not decrease monotonically with the addition of arbitrary concentration points [2]. Protocol B requires a systematic 4- to 5-point sweep across 1.2x to 2.5x CMC with joint nonlinear least-squares regression, rather than a naive two-point fit.")

# 4. Comparative Synthesis Table
add_section_heading(doc, "4. Quantitative Protocol and Instrument Synthesis")
add_body_paragraph(doc, "Table 1 synthesizes the operational parameters, hardware requirements, and inversion protocols across the operational surfactant landscape [1,2,5,6].")

add_table_caption(doc, "Table 1. Operational parameters, instrumentation bands, and inversion protocols for micellar relaxation kinetics [2,5,6].")
t1 = doc.add_table(rows=4, cols=6)
t1.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(t1)

headers = ["System Class", "Model Surfactant", "tau2 Scale", "Operable Frequency", "Primary Protocol", "Ref."]
for i, h in enumerate(headers):
    set_cell_font(t1.rows[0].cells[i], h, bold=True, align_right=(i == 5))

t1_data = [
    ["Nonionic (Slow)", "C12E8", "1.0 to 4.0 s", "0.04 to 1.19 Hz (PAT-1M)", "Protocol A (0.2% stat, 1:1 n_bar)", "[2,5]"],
    ["Cationic (Medium)", "CTAB", "65 ms", ">= 16 Hz (CPT band)", "Protocol B (CPT)", "[2,6]"],
    ["Anionic (Fast)", "SDS", "38 ms", ">= 20 Hz (CPT band)", "Protocol B (CPT)", "[2,6]"]
]

for row_idx, data in enumerate(t1_data, start=1):
    for col_idx, val in enumerate(data):
        set_cell_font(t1.rows[row_idx].cells[col_idx], val, align_right=(col_idx == 5))

# 5. References
add_section_heading(doc, "5. References")
refs = [
    ("1", "Czakaj, A., Jarek, E., Krzan, M., Warszynski, P., Ethyl Lauroyl Arginate, an Inherently Multicomponent Surfactant System, Molecules, 2021, 26, 5894."),
    ("2", "Kotian, P. D., Direct Inversion of Micellar Relaxation Kinetics from Large-Amplitude Oscillatory Dilatational Surface Rheology, ChemRxiv, 2026, doi:10.26434/chemrxiv.15011298/v1."),
    ("3", "Loglio, G. et al., Dilatational viscoelasticity of surfactant solutions: Large-amplitude oscillations and drop stability, Colloids Surf. A, 2001, 186, 63-71."),
    ("4", "Kotsmar, C. et al., Dynamic surface properties of mixed surfactant/protein systems studied by profile analysis tensiometry, Colloids Surf. A, 2012, 413, 20-25."),
    ("5", "Miller, R. et al., Transient and oscillatory surface dilatational rheology: Principles and instrumentation, Adv. Colloid Interface Sci., 2004, 111, 17-34."),
    ("6", "Stadler, K. et al., High-frequency capillary pressure tensiometer with piezo-actuator operating up to 500 Hz, Meas. Sci. Technol., 2016, 27, 045301.")
]

for ref_id, ref_text in refs:
    add_reference_entry(doc, ref_id, ref_text)

out_docx = r"D:\CodeProjects\surfactant-dynamics-sim\docs\LAOD_C12E8_MANUSCRIPT_FINAL_SYNTHESIS_AND_PROTOCOL_SPEC.docx"
os.makedirs(os.path.dirname(out_docx), exist_ok=True)
doc.save(out_docx)
print("Successfully generated:", out_docx)
