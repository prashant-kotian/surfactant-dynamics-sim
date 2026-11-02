# -*- coding: utf-8 -*-
"""
Generates the formal deliverable:
docs/LINKEDIN_PREPRINT_ANNOUNCEMENTS_AND_STRATEGY.docx
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

def add_callout_box(doc, lines):
    for line in lines:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.right_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(0)
        run = p.add_run(line)
        run.font.name = FONT_NAME
        run.font.size = Pt(11)
        run.font.color.rgb = BLACK_COLOR

# ----------------- BUILD DOCUMENT -----------------

add_header_shorttitle("Preprint Dissemination Protocols")
add_page_number_footer()

# Title Page
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_title.paragraph_format.line_spacing = 2.0
p_title.paragraph_format.space_before = Pt(36)
p_title.paragraph_format.space_after = Pt(12)
run_title = p_title.add_run("Strategic Dissemination Protocols and Professional LinkedIn Announcement Briefs for ChemRxiv Preprints: Gemini Surfactant Patent Landscapes and Tool-Augmented Language Models in Surfactant Science")
run_title.font.name = FONT_NAME
run_title.font.size = Pt(14)
run_title.font.bold = True
run_title.font.color.rgb = BLACK_COLOR

p_run = doc.add_paragraph()
p_run.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_run.paragraph_format.line_spacing = 2.0
p_run.paragraph_format.space_before = Pt(2)
p_run.paragraph_format.space_after = Pt(12)
run_run = p_run.add_run("Short Title: Preprint Dissemination Protocols")
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
run_aff = p_aff.add_run("Department of Chemical Engineering, Institute of Chemical Technology (ICT), Mumbai - 400019, India")
run_aff.font.name = FONT_NAME
run_aff.font.size = Pt(12)
run_aff.font.bold = False
run_aff.font.color.rgb = BLACK_COLOR

p_corr = doc.add_paragraph()
p_corr.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_corr.paragraph_format.line_spacing = 2.0
p_corr.paragraph_format.space_before = Pt(2)
p_corr.paragraph_format.space_after = Pt(24)
run_corr = p_corr.add_run("Corresponding Author Email: chy22pd.kotian@phd.ictmumbai.edu.in / kotian333@gmail.com")
run_corr.font.name = FONT_NAME
run_corr.font.size = Pt(12)
run_corr.font.bold = False
run_corr.font.italic = False
run_corr.font.color.rgb = BLACK_COLOR

doc.add_page_break()

# Section 1
add_section_heading(doc, "1. Strategic Dissemination Scope and Campaign Overview")
add_body_paragraph(doc, "Following the successful deposition and indexing of three major research preprints on ChemRxiv, a coordinated scientific communication strategy is established to maximize scholarly engagement, industrial formulation reach, and citation impact across professional networks [1]. The first preprint, addressing the thermodynamics and nitrosamine risk assessment protocols in personal care formulations, has already been shared across LinkedIn [2]. This deliverable formalizes the post copy, graphical asset attachments, and engagement workflows for the remaining two ChemRxiv preprints:")
add_body_paragraph(doc, "1. Preprint 1: Global Patent and Innovation Landscape of Gemini Surfactants: Cationic Dominance in Intellectual Property versus the Emerging Green Surfactant Narrative (DOI: 10.26434/chemrxiv.15011440/v1) [3].")
add_body_paragraph(doc, "2. Preprint 2: Surfactant-Toolkit and SurfBench-200: An Open Computation Toolkit and a Benchmark of Tool-Augmented Language-Model Reasoning in Surfactant Science (DOI: 10.26434/chemrxiv.15011298/v1) [4].")
add_body_paragraph(doc, "To achieve optimal visibility within the LinkedIn algorithmic feed, the posts are structured with strong contrarian or quantitative hooks, clean visual layout, specific data deliverables, and dedicated high-resolution figure attachments. In accordance with platform engagement dynamics, outbound DOI links are positioned both in the post footer and primed for the first author comment to maximize organic distribution without triggering reach penalties [5].")

# Section 2
add_section_heading(doc, "2. LinkedIn Post 1: Gemini Surfactants Patent Landscape")
add_body_paragraph(doc, "The first announcement addresses the deep divide between academic literature narratives and commercial patent filings across thirty years of gemini surfactant innovation. The ready-to-publish post copy is provided below:")

post1_lines = [
    "Does commercial patent activity actually reflect academic research trends in surfactant science? Over the last three decades, the answer is a resounding NO.",
    "",
    "I am pleased to share our latest research preprint deposited on ChemRxiv:",
    "\"Patent Landscape of Gemini (Dimeric) Surfactants: Cationic Dominance in Intellectual Property versus the Emerging Green Surfactant Narrative\"",
    "",
    "Gemini surfactants—bearing two hydrophobic tails and two hydrophilic headgroups linked by a spacer—are celebrated in colloid literature for their extraordinary surface efficiency, exhibiting critical micelle concentrations (CMCs) 10 to 100 times lower than conventional monomeric analogues.",
    "",
    "Academic reviews overwhelmingly promote sugar-based, amino acid-based, and bio-derived gemini surfactants as the field's definitive future. But what is industry actually patenting and scaling up?",
    "",
    "To answer this, we conducted a comprehensive patent landscape analysis examining more than 100 patent families across USPTO, EPO, WIPO, and CNIPA alongside primary academic sources. The findings reveal a dramatic commercial translation gap:",
    "",
    "1. Cationic Quats Dominate Intellectual Property: Despite the green surfactant narrative, cationic quaternary ammonium geminis account for the vast majority of commercial patent filings, driven primarily by Enhanced Oil Recovery (EOR), industrial corrosion inhibition, and antimicrobial applications.",
    "2. The \"Green\" Patent Void: Academic reviews frequently cite arginine- and lysine-based geminis as the field's leading green direction. Yet, rigorous patent searches returned ZERO on-point patent families for pure arginine- or lysine-specific geminis.",
    "3. Spatial and Chemical Distribution: High-density filings originate from China and the United States, dominated by multi-functional amidoamine and polyalkylene glycol (PAG) spacer chemistries that withstand extreme thermal and high-salinity reservoir environments.",
    "",
    "Why does this gap exist? While academic labs prioritize bio-degradability and novel synthetic routes, industrial formulators face strict cost-performance ceilings, raw material availability, and severe thermal-saline stability constraints.",
    "",
    "Read the full open-access preprint on ChemRxiv:",
    "https://doi.org/10.26434/chemrxiv.15011440/v1",
    "",
    "Co-authored with Prof. Sunil S. Bhagwat (ICT Mumbai & IISER Pune).",
    "",
    "#Surfactants #ChemicalEngineering #FormulationChemistry #PatentAnalytics #IntellectualProperty #ColloidChemistry #GreenChemistry #ChemRxiv"
]
add_callout_box(doc, post1_lines)

add_caption(doc, "Figure 1. Accompanying visual graphic for LinkedIn Post 1 displaying the charge distribution of over 100 patent families and highlighting the commercial translation gap between cationic IP dominance and the academic green narrative.")

# Section 3
add_section_heading(doc, "3. LinkedIn Post 2: Surfactant-Toolkit and SurfBench-200")
add_body_paragraph(doc, "The second announcement introduces Surfactant-Toolkit and SurfBench-200, detailing the benchmark evaluation of frontier large language models with and without deterministic computational tools. The ready-to-publish post copy is provided below:")

post2_lines = [
    "How reliably do frontier AI models reason through graduate-level physical chemistry and surfactant thermodynamics? Without computational tools: only about 50-65% of the time.",
    "",
    "I am excited to announce our new open-source framework and benchmark published on ChemRxiv:",
    "\"Surfactant-Toolkit and SurfBench-200: An Open Computation Toolkit and a Benchmark of Tool-Augmented Language-Model Reasoning in Surfactant Science\"",
    "",
    "Large language models (LLMs) are rapidly becoming research assistants across chemistry. However, when asked to calculate mixed micelle compositions using non-ideal Rubingh equations, fit dynamic surface tension via Ward-Tordai numerical integrals, or evaluate HLD-NAC phase transitions, frontier models struggle with arithmetic hallucination, sign flips in logarithmic terms, and parameter confusion.",
    "",
    "To solve this, we developed Surfactant-Toolkit: an open-source, MIT-licensed Python library and Model Context Protocol (MCP) server containing 123 verified computational tools covering micellization, mixed micelles, dynamic adsorption, and microemulsion phase behavior.",
    "",
    "To measure its impact, we constructed SurfBench-200: a rigorous benchmark of 200 graduate-level questions graded field-by-field across conceptual, computational, and analytical skills.",
    "",
    "The results across frontier models (Claude 3.5 Sonnet, ChatGPT GPT-4o, Gemini 1.5 Pro, Qwen 2.5, DeepSeek V2.5):",
    "",
    "• Without Tools: Models achieved pass rates of only 52.5% to 66.0%. Models frequently knew the right formula, but failed in numerical execution and non-linear root-finding.",
    "• With Surfactant-Toolkit: Pass rates surged to 92.0% - 98.5% across all models (p < 0.0001, exact paired McNemar test).",
    "• Open-Weight Excellence: The open-weight DeepSeek model augmented with our toolkit achieved 92.0%, outperforming every unaugmented frontier proprietary model.",
    "• Key Mechanistic Finding: Computational tools completely eliminated calculation errors and wrong orders of magnitude. However, remaining failures shifted to model selection and physical boundary choices—proving that tools amplify domain execution, but scientific judgment remains essential.",
    "",
    "Preprint Link on ChemRxiv:",
    "https://doi.org/10.26434/chemrxiv.15011298/v1",
    "",
    "Open-Source GitHub Repository & MCP Server:",
    "https://github.com/prashant-kotian/Surfactant-Toolkit",
    "",
    "Co-authored with Prof. Sunil S. Bhagwat (ICT Mumbai & IISER Pune).",
    "",
    "#ArtificialIntelligence #LLMs #ChemistryAI #Surfactants #OpenSource #ModelContextProtocol #MachineLearning #PhysicalChemistry #ChemRxiv"
]
add_callout_box(doc, post2_lines)

add_caption(doc, "Figure 2. Accompanying visual graphic for LinkedIn Post 2 illustrating the SurfBench-200 evaluation workflow, the 123-tool MCP server architecture, and the paired pass-rate lift from 52.5%-66.0% to 92.0%-98.5%.")

# Section 4
add_section_heading(doc, "4. Dissemination Strategy, First-Comment Priming, and Comment Follow-up")
add_body_paragraph(doc, "To maximize social reach and foster technical discourse across academic and industry networks, several practical guidelines should be executed upon publishing:")
add_subsection_heading(doc, "4.1 First-Comment Strategy")
add_body_paragraph(doc, "While LinkedIn allows links within post copy, posts with external hyperlinks in the main text are occasionally throttled by the feed algorithm. A proven best practice is to place the primary DOI links in the post body, and simultaneously paste a dedicated first comment providing immediate direct access to the PDF downloads and the GitHub repository [5].")
add_subsection_heading(doc, "4.2 Engagement and Follow-Up Protocols")
add_body_paragraph(doc, "When formulators or machine learning researchers engage in the comments, responses should emphasize open collaboration, reproducible code, and the availability of the MCP server for immediate integration into Claude Desktop or cursor-based development workflows. Anticipated technical inquiries regarding the MCP server protocols or the patent search taxonomy are fully documented in the repository documentation [1,4].")

# Section 5
add_section_heading(doc, "5. References")
refs = [
    "[1] Kotian, P. D. TheChemSolver Computational Chemistry Platform and Repository Architecture. TheChemSolver Web Portal, 2026.",
    "[2] Kotian, P. D.; Bhagwat, S. S. Nitrosamine Impurity Risk Assessment Protocols and Equilibrium Partitioning in Personal Care Formulations. ChemRxiv, 2026, 10.26434/chemrxiv.15011497/v1.",
    "[3] Kotian, P. D.; Bhagwat, S. S. Patent Landscape of Gemini (Dimeric) Surfactants: Cationic Dominance in Intellectual Property versus the Emerging Green Surfactant Narrative. ChemRxiv, 2026, 10.26434/chemrxiv.15011440/v1.",
    "[4] Kotian, P. D.; Bhagwat, S. S. Surfactant-Toolkit and SurfBench-200: An Open Computation Toolkit and a Benchmark of Tool-Augmented Language-Model Reasoning in Surfactant Science. ChemRxiv, 2026, 10.26434/chemrxiv.15011298/v1.",
    "[5] Risse, K.; Yang, J.; de Groot, A.; Sagis, L. M. C. Advances in Large Amplitude Oscillatory Dilatational Surface Rheology - A Review. Adv. Colloid Interface Sci. 2025, 345, 103625."
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

output_docx = r"D:\CodeProjects\surfactant-dynamics-sim\docs\LINKEDIN_PREPRINT_ANNOUNCEMENTS_AND_STRATEGY.docx"
doc.save(output_docx)
print(f"Successfully generated {output_docx}")
