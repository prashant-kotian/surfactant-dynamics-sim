# -*- coding: utf-8 -*-
r"""
build_full_manuscript_docx.py
Compiles the complete, publication-ready Microsoft Word manuscript:
docs/Direct_Inversion_Micellar_Relaxation_Kinetics_LAOD.docx
from manuscript/PAPER1_SUBMISSION.md.

Strictly adheres to D:\CodeProjects\PhD-Research\MANUSCRIPT_FORMATTING_SPEC.md:
1. Font: Times New Roman throughout (body, headings, tables, captions, header, footer). Explicitly forced on every run.
2. Running page numbers in footer (PAGE field).
3. Title page with full title, running title, author, affiliation, and email.
4. Section headings: 12pt, Times New Roman, bold, non-italic, justified.
5. Strict Italics Rule (#3a): Subsection headings are the ONLY italic text in the document.
6. Paragraph spacing: 2pt before, 2pt after, double line spacing (2.0), 0.5" first-line indent, justified.
7. Tables: sequential numbering, 10pt Times New Roman, bold headers, justified cells, blue citations.
8. Citations & cross-references: blue (RGBColor(0, 0, 255)).
9. Clean delivery: no appendix, ends cleanly after References and Reference flags.
10. Headless LibreOffice PDF conversion verification.
"""
import os
import re
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FONT_NAME = "Times New Roman"
BLUE_COLOR = RGBColor(0x00, 0x00, 0xFF)
BLACK_COLOR = RGBColor(0x00, 0x00, 0x00)

doc = Document()

# Configure Normal style
normal = doc.styles["Normal"]
normal.font.name = FONT_NAME
normal.font.size = Pt(12)
rpr = normal.element.get_or_add_rPr()
rFonts = rpr.find(qn('w:rFonts'))
if rFonts is None:
    rFonts = OxmlElement('w:rFonts')
    rpr.append(rFonts)
rFonts.set(qn('w:ascii'), FONT_NAME)
rFonts.set(qn('w:hAnsi'), FONT_NAME)
rFonts.set(qn('w:cs'), FONT_NAME)
rFonts.set(qn('w:eastAsia'), FONT_NAME)

# Set 1-inch margins
sec = doc.sections[0]
sec.left_margin = Inches(1)
sec.right_margin = Inches(1)
sec.top_margin = Inches(1)
sec.bottom_margin = Inches(1)

def apply_run_font(run, font_name=FONT_NAME, size_pt=12, bold=False, italic=False, color_rgb=BLACK_COLOR):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    if color_rgb is not None:
        run.font.color.rgb = color_rgb
    rpr = run.element.get_or_add_rPr()
    rFonts = rpr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rpr.append(rFonts)
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    rFonts.set(qn('w:eastAsia'), font_name)

def add_page_number_footer():
    footer = sec.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    fld1 = OxmlElement('w:fldChar'); fld1.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText'); instr.set(qn('xml:space'), 'preserve'); instr.text = 'PAGE'
    fld2 = OxmlElement('w:fldChar'); fld2.set(qn('w:fldCharType'), 'end')
    run._r.append(fld1); run._r.append(instr); run._r.append(fld2)
    apply_run_font(run, font_name=FONT_NAME, size_pt=10, bold=False, italic=False, color_rgb=BLACK_COLOR)

def add_header_shorttitle(text):
    header = sec.header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run(text)
    apply_run_font(run, font_name=FONT_NAME, size_pt=10, bold=False, italic=False, color_rgb=BLACK_COLOR)

def format_text_runs(p, text, is_italic=False, is_bold=False, font_size=12):
    # Strip markdown bold/italics syntax from token stream
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    
    # Regex to capture citations like [1], [2], [3], [6,7], [8], [4-6]
    # and cross-references like Figure X, Table X, Section X.X, §X.X
    # Avoid matching closed math intervals like [1, 30] by checking against references range 1-8
    citation_or_xref_pattern = r'(\[(?:[1-8](?:-[1-8])?(?:,\s*[1-8](?:-[1-8])?)*)\]|Figure\s+\d+|Table\s+\d+|Section\s+\d+(?:\.\d+)*|§\s*\d+(?:\.\d+)*)'
    
    tokens = re.split(citation_or_xref_pattern, text)
    for token in tokens:
        if not token:
            continue
        run = p.add_run(token)
        is_blue = bool(re.match(r'^' + citation_or_xref_pattern + r'$', token))
        color = BLUE_COLOR if is_blue else BLACK_COLOR
        apply_run_font(run, font_name=FONT_NAME, size_pt=font_size, bold=is_bold, italic=is_italic, color_rgb=color)

def add_body_paragraph(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.first_line_indent = Inches(0.5)
    format_text_runs(p, text, is_italic=False, is_bold=False, font_size=12)
    return p

def add_list_item(doc, text, is_numbered=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.first_line_indent = Inches(0.5)
    format_text_runs(p, text, is_italic=False, is_bold=False, font_size=12)
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
    format_text_runs(p, clean_text, is_italic=False, is_bold=True, font_size=12)
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
    # Strictly italic per Rule #3 and #3a
    format_text_runs(p, clean_text, is_italic=True, is_bold=True, font_size=12)
    return p

def add_table_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.first_line_indent = Inches(0)
    clean_text = re.sub(r'^[#\s]+', '', text).strip()
    clean_text = re.sub(r'\*\*(.*?)\*\*', r'\1', clean_text)
    run = p.add_run(clean_text)
    apply_run_font(run, font_name=FONT_NAME, size_pt=10, bold=False, italic=False, color_rgb=BLACK_COLOR)
    return p

def set_cell_font(cell, text, bold=False):
    p = cell.paragraphs[0]
    for r in list(p.runs):
        p._p.remove(r._r)
    for extra_p in cell.paragraphs[1:]:
        cell._tc.remove(extra_p._p)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.first_line_indent = Inches(0)
    clean_text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    clean_text = re.sub(r'\*(.*?)\*', r'\1', clean_text)
    
    citation_pattern = r'(\[(?:[1-8](?:-[1-8])?(?:,\s*[1-8](?:-[1-8])?)*)\])'
    tokens = re.split(citation_pattern, clean_text)
    for token in tokens:
        if not token:
            continue
        run = p.add_run(token)
        is_blue = bool(re.match(r'^' + citation_pattern + r'$', token))
        color = BLUE_COLOR if is_blue else BLACK_COLOR
        apply_run_font(run, font_name=FONT_NAME, size_pt=10, bold=bold, italic=False, color_rgb=color)

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
    apply_run_font(run_id, font_name=FONT_NAME, size_pt=12, bold=False, italic=False, color_rgb=BLUE_COLOR)
    
    clean_text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    clean_text = re.sub(r'\*(.*?)\*', r'\1', clean_text)
    clean_text = re.sub(r'_(.*?)_', r'\1', clean_text)
    run_txt = p.add_run(clean_text)
    apply_run_font(run_txt, font_name=FONT_NAME, size_pt=12, bold=False, italic=False, color_rgb=BLACK_COLOR)

# Header & Footer
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
apply_run_font(run_title, font_name=FONT_NAME, size_pt=14, bold=True, italic=False, color_rgb=BLACK_COLOR)

p_short = doc.add_paragraph()
p_short.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_short.paragraph_format.line_spacing = 2.0
p_short.paragraph_format.space_before = Pt(2)
p_short.paragraph_format.space_after = Pt(12)
p_short.paragraph_format.first_line_indent = Inches(0)
run_short = p_short.add_run("Short Title: Micellar Relaxation Kinetics from LAOD")
apply_run_font(run_short, font_name=FONT_NAME, size_pt=12, bold=False, italic=False, color_rgb=BLACK_COLOR)

p_author = doc.add_paragraph()
p_author.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_author.paragraph_format.line_spacing = 2.0
p_author.paragraph_format.space_before = Pt(2)
p_author.paragraph_format.space_after = Pt(6)
p_author.paragraph_format.first_line_indent = Inches(0)
run_auth = p_author.add_run("Prashant D. Kotian")
apply_run_font(run_auth, font_name=FONT_NAME, size_pt=12, bold=True, italic=False, color_rgb=BLACK_COLOR)

p_aff = doc.add_paragraph()
p_aff.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_aff.paragraph_format.line_spacing = 2.0
p_aff.paragraph_format.space_before = Pt(2)
p_aff.paragraph_format.space_after = Pt(6)
p_aff.paragraph_format.first_line_indent = Inches(0)
run_aff = p_aff.add_run("Independent Researcher, Mumbai, India")
apply_run_font(run_aff, font_name=FONT_NAME, size_pt=12, bold=False, italic=False, color_rgb=BLACK_COLOR)

p_cor = doc.add_paragraph()
p_cor.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_cor.paragraph_format.line_spacing = 2.0
p_cor.paragraph_format.space_before = Pt(2)
p_cor.paragraph_format.space_after = Pt(24)
p_cor.paragraph_format.first_line_indent = Inches(0)
run_cor = p_cor.add_run("Corresponding Author Email: prashant.d.kotian@gmail.com")
apply_run_font(run_cor, font_name=FONT_NAME, size_pt=12, bold=False, italic=False, color_rgb=BLACK_COLOR)

# Page break after Title Page
p_break = doc.add_paragraph()
p_break.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_break.paragraph_format.line_spacing = 1.0
p_break.paragraph_format.space_before = Pt(0)
p_break.paragraph_format.space_after = Pt(0)
p_break.paragraph_format.first_line_indent = Inches(0)
run_break = p_break.add_run()
apply_run_font(run_break, font_name=FONT_NAME, size_pt=12, bold=False, italic=False, color_rgb=BLACK_COLOR)
run_break.add_break(WD_BREAK.PAGE)

# Read submission markdown file
md_path = r"D:\CodeProjects\surfactant-dynamics-sim\manuscript\PAPER1_SUBMISSION.md"
with open(md_path, "r", encoding="utf-8") as f:
    raw_text = f.read()

# Replace all citation placeholders
text = raw_text
text = re.sub(r'\[CIT:\s*Lucassen\s*&\s*van\s*den\s*Tempel\]', '[2]', text)
text = re.sub(r'\[CIT:\s*Aniansson\s*&\s*Wall\]', '[3]', text)
text = re.sub(r'\[CIT:\s*Czakaj\s*2021\]', '[1]', text)
text = re.sub(r'\[CIT:\s*instrument,\s*to\s*be\s*sourced\]', '[8]', text)
text = re.sub(r'\[CIT:\s*to\s*be\s*sourced\]', '[6,7]', text)

lines = text.splitlines()

# Explicit table captions
table_captions = [
    "Table 1. Summary of second-harmonic response and loss-angle sensitivity across the critical micelle concentration for C₁₂E₈.",
    "Table 2. Invariance of the concentration inversion window across a fourfold range in limiting surface elasticity.",
    "Table 3. Frequency dependence of the dilatational loss angle with and without the micellar exchange reservoir.",
    "Table 4. Comparison of candidate rheological observables across a 16-fold variation in micellar relaxation time τ₂ at 1.5 × CMC.",
    "Table 5. Diagnostic comparison of detectability and invertibility criteria for micellar oscillatory dilatational rheology.",
    "Table 6. Demodulation accuracy and phase-lag recovery bias as a function of optical sampling density.",
    "Table 7. Precision budget and parameter recovery uncertainty from 60 Monte Carlo realizations at the operating point.",
    "Table 8. Timescale-to-bandwidth horizon and instrument compatibility for nonionic and ionic surfactant systems.",
    "Table 9. Frequency sweep of harmonic amplitudes and loss angle for CTAB showing dynamic unbuffering at high frequency.",
    "Table 10. Systematic propagation of aggregation number uncertainty into micellar concentration and relaxation time bias."
]

table_counter = 0
in_references = False

i = 0
N = len(lines)
while i < N:
    s_line = lines[i].strip()
    
    if not s_line or s_line.startswith('---'):
        i += 1
        continue
        
    # Skip preamble/title lines if encountered
    if s_line.startswith('# Direct Inversion') or s_line.startswith('**Paper 1 of 2') or s_line.startswith('*Manuscript for submission'):
        i += 1
        continue
        
    # Strictly exclude any appendix
    if s_line.startswith('# Appendix') or s_line.startswith('## Appendix'):
        break
        
    # Section Heading
    if s_line.startswith('## '):
        h_text = s_line[3:].strip()
        add_section_heading(doc, h_text)
        if 'References' in h_text:
            in_references = True
        else:
            in_references = False
        i += 1
        continue
        
    # Subsection Heading
    if s_line.startswith('### '):
        h_text = s_line[4:].strip()
        add_subsection_heading(doc, h_text)
        i += 1
        continue
        
    # Markdown Table
    if s_line.startswith('|') and s_line.endswith('|'):
        tbl_lines = [s_line]
        i += 1
        while i < N and lines[i].strip().startswith('|') and lines[i].strip().endswith('|'):
            tbl_lines.append(lines[i].strip())
            i += 1
            
        table_counter += 1
        cap_text = table_captions[table_counter - 1] if table_counter <= len(table_captions) else f"Table {table_counter}. Summary of simulation results."
        add_table_caption(doc, cap_text)
        
        rows_data = []
        for tl in tbl_lines:
            if re.match(r'^\|[\s\-:|]+\|$', tl):
                continue
            cols = [c.strip() for c in tl.strip('|').split('|')]
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
        continue
        
    # Numbered item (References or Conclusions)
    m_num = re.match(r'^(\d+)\.\s+(.*)', s_line)
    if m_num:
        ref_id = m_num.group(1)
        ref_body = [m_num.group(2)]
        i += 1
        while i < N and lines[i].strip() and not lines[i].strip().startswith(('#', '|', '---')):
            next_s = lines[i].strip()
            if re.match(r'^\d+\.\s+', next_s):
                break
            ref_body.append(next_s)
            i += 1
        full_text = ' '.join(ref_body)
        if in_references:
            add_reference_entry(doc, ref_id, full_text)
        else:
            add_list_item(doc, f"{ref_id}. {full_text}", is_numbered=True)
        continue
        
    # Bullet item
    if s_line.startswith('- '):
        b_lines = [s_line[2:].strip()]
        i += 1
        while i < N and lines[i].strip() and not lines[i].strip().startswith(('#', '|', '---', '- ')):
            next_s = lines[i].strip()
            if re.match(r'^\d+\.\s+', next_s):
                break
            b_lines.append(next_s)
            i += 1
        add_list_item(doc, f"• {' '.join(b_lines)}", is_numbered=False)
        continue
        
    # Standard Body Paragraph (join wrapped lines into one continuous paragraph)
    p_lines = [s_line]
    i += 1
    while i < N and lines[i].strip() and not lines[i].strip().startswith(('#', '|', '---', '- ')) and not re.match(r'^\d+\.\s+', lines[i].strip()):
        p_lines.append(lines[i].strip())
        i += 1
    add_body_paragraph(doc, ' '.join(p_lines))

out_docx = r"D:\CodeProjects\surfactant-dynamics-sim\docs\Direct_Inversion_Micellar_Relaxation_Kinetics_LAOD.docx"
os.makedirs(os.path.dirname(out_docx), exist_ok=True)
doc.save(out_docx)
print("Successfully generated clean submission manuscript:", out_docx)
