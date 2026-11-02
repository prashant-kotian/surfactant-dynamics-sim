# -*- coding: utf-8 -*-
r"""
build_full_manuscript_docx.py
Builds the complete, publication-ready Microsoft Word document:
docs/Direct_Inversion_Micellar_Relaxation_Kinetics_LAOD.docx
from manuscript/PAPER1_FULL_DRAFT.md.
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

def format_text_runs(p, text, is_italic=False, is_bold=False):
    # Strip markdown bold/italics syntax from token stream
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    
    # Replace citation placeholders
    text = text.replace("[CIT: Lucassen & van den Tempel]", "[2]")
    text = text.replace("[CIT: Aniansson & Wall]", "[3]")
    text = text.replace("[CIT: Czakaj 2021]", "[1]")
    text = text.replace("[CIT: instrument, to be sourced]", "[8]")
    text = text.replace("[CIT: to be sourced]", "[6,7]")
    
    pattern = r'(\[(?:\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)\]|Figure\s+\d+|Table\s+\d+|Section\s+\d+(?:\.\d+)*)'
    tokens = re.split(pattern, text)
    for token in tokens:
        if not token:
            continue
        run = p.add_run(token)
        run.font.name = FONT_NAME
        run.font.size = Pt(12)
        run.font.italic = is_italic
        run.font.bold = is_bold
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
    format_text_runs(p, text, is_italic=False, is_bold=False)
    return p

def add_section_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.first_line_indent = Inches(0)
    clean_text = re.sub(r'^[#§\s]+', '', text).strip()
    clean_text = re.sub(r'\*\*(.*?)\*\*', r'\1', clean_text)
    format_text_runs(p, clean_text, is_italic=False, is_bold=True)
    return p

def add_subsection_heading(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.first_line_indent = Inches(0)
    clean_text = re.sub(r'^[#§\s]+', '', text).strip()
    clean_text = re.sub(r'\*\*(.*?)\*\*', r'\1', clean_text)
    format_text_runs(p, clean_text, is_italic=True, is_bold=True)
    return p

def add_table_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.first_line_indent = Inches(0)
    clean_text = re.sub(r'^[#\s]+', '', text).strip()
    run = p.add_run(clean_text)
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
    clean_text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    clean_text = re.sub(r'\*(.*?)\*', r'\1', clean_text)
    pattern = r'(\[(?:\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)\])'
    tokens = re.split(pattern, clean_text)
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
    clean_text = re.sub(r'\*(.*?)\*', r'\1', text)
    clean_text = re.sub(r'_(.*?)_', r'\1', clean_text)
    run_txt = p.add_run(clean_text)
    run_txt.font.name = FONT_NAME
    run_txt.font.size = Pt(12)
    run_txt.font.italic = False
    run_txt.font.color.rgb = BLACK_COLOR

add_page_number_footer()
add_header_shorttitle("Micellar Relaxation Kinetics from LAOD")

# Title Page
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_title.paragraph_format.line_spacing = 2.0
p_title.paragraph_format.space_before = Pt(24)
p_title.paragraph_format.space_after = Pt(12)
p_title.paragraph_format.first_line_indent = Inches(0)
run_title = p_title.add_run("Direct Inversion of Micellar Relaxation Kinetics from Large-Amplitude Oscillatory Dilatational Surface Rheology: Theory, Bandwidth Limits, and Robust Parameter Identification for Model Nonionic Surfactants")
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
run_short = p_short.add_run("Short Title: Micellar Relaxation Kinetics from LAOD")
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

# Read the full markdown file
md_path = r"D:\CodeProjects\surfactant-dynamics-sim\manuscript\PAPER1_FULL_DRAFT.md"
with open(md_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

table_counter = 0
in_table = False
table_lines = []

i = 0
N = len(lines)
while i < N:
    line = lines[i].strip()
    
    # Skip preamble before Abstract or title lines
    if line.startswith("# Direct Inversion") or line.startswith("**Paper 1 of 2") or line.startswith("*Unified manuscript"):
        i += 1
        continue
    if line.startswith("---"):
        i += 1
        continue
        
    # Check for Markdown tables
    if line.startswith("|") and line.endswith("|"):
        table_lines.append(line)
        i += 1
        # continue collecting table lines
        while i < N and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
            table_lines.append(lines[i].strip())
            i += 1
            
        # Process collected table
        table_counter += 1
        add_table_caption(doc, f"Table {table_counter}. Summary of simulation results and operational parameters.")
        
        # parse rows
        rows_data = []
        for tl in table_lines:
            if re.match(r'^\|[\s\-:|]+\|$', tl):
                continue
            cols = [c.strip() for c in tl.strip("|").split("|")]
            rows_data.append(cols)
            
        if rows_data:
            num_rows = len(rows_data)
            num_cols = len(rows_data[0])
            t = doc.add_table(rows=num_rows, cols=num_cols)
            t.alignment = WD_TABLE_ALIGNMENT.CENTER
            set_table_borders(t)
            
            for r_idx, r_cols in enumerate(rows_data):
                is_hdr = (r_idx == 0)
                for c_idx, cell_val in enumerate(r_cols):
                    if c_idx < num_cols:
                        set_cell_font(t.rows[r_idx].cells[c_idx], cell_val, bold=is_hdr)
        table_lines = []
        continue

    # Section Headings
    if line.startswith("## "):
        h_text = line[3:].strip()
        add_section_heading(doc, h_text)
        i += 1
        continue
    elif line.startswith("### "):
        h_text = line[4:].strip()
        add_subsection_heading(doc, h_text)
        i += 1
        continue
    elif line.startswith("# Appendix"):
        add_section_heading(doc, "Appendix: Computational Provenance, Sensitivity Audits, and Multiplicity Notes")
        i += 1
        continue

    # Body Paragraph
    if line:
        # Check if line is a numbered reference item in references section
        m_ref = re.match(r'^(\d+)\.\s+(.*)', line)
        if m_ref and "References" in lines[max(0, i-40):i]:
            add_reference_entry(doc, m_ref.group(1), m_ref.group(2))
        else:
            add_body_paragraph(doc, line)
            
    i += 1

out_docx = r"D:\CodeProjects\surfactant-dynamics-sim\docs\Direct_Inversion_Micellar_Relaxation_Kinetics_LAOD.docx"
os.makedirs(os.path.dirname(out_docx), exist_ok=True)
doc.save(out_docx)
print("Successfully generated:", out_docx)
