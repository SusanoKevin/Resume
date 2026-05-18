"""
Generates Resume_Susano Kevin Amala.docx from resume.json.
Font: Times New Roman, black throughout.
"""

import json
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

BLACK = RGBColor(0, 0, 0)
FONT  = "Times New Roman"
PAGE_W = Inches(8.5)
# usable width: 8.5 - 0.5 - 0.5 = 7.5"
USABLE_W = Inches(7.5)

with open("/Users/susanokevinamalamahilmaran/Downloads/Projects/Resume/resume.json") as f:
    data = json.load(f)


def new_doc():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width  = PAGE_W
    sec.page_height = Inches(11)
    sec.top_margin    = Inches(0.5)
    sec.bottom_margin = Inches(0.5)
    sec.left_margin   = Inches(0.5)
    sec.right_margin  = Inches(0.5)
    # clear default paragraph spacing from Normal style
    doc.styles["Normal"].paragraph_format.space_before = Pt(0)
    doc.styles["Normal"].paragraph_format.space_after  = Pt(0)
    doc.styles["Normal"].font.name  = FONT
    doc.styles["Normal"].font.color.rgb = BLACK
    doc.styles["Normal"].font.size  = Pt(11)
    return doc


def set_run(run, text, bold=False, size=11, italic=False):
    run.text = text
    run.bold = bold
    run.italic = italic
    run.font.name  = FONT
    run.font.size  = Pt(size)
    run.font.color.rgb = BLACK


def add_para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=0):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(space_after)
    return p


def add_section_header(doc, title, space_before=6):
    p = add_para(doc)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(1)
    # bottom border = thin horizontal rule
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "000000")
    pBdr.append(bottom)
    pPr.append(pBdr)
    r = p.add_run(title)
    set_run(r, title, bold=True, size=11)
    return p


def add_right_tab_para(doc, left_text, right_text,
                        left_bold=True, right_bold=False,
                        left_size=11, right_size=11,
                        space_after=0):
    """Paragraph with left text and right-aligned date via tab stop."""
    p = add_para(doc, space_after=space_after)
    # add right tab stop at usable width
    pPr = p._p.get_or_add_pPr()
    tabs = OxmlElement("w:tabs")
    tab = OxmlElement("w:tab")
    tab.set(qn("w:val"), "right")
    tab.set(qn("w:pos"), str(int(USABLE_W.pt * 20)))  # twips
    tabs.append(tab)
    pPr.append(tabs)

    r1 = p.add_run(left_text)
    set_run(r1, left_text, bold=left_bold, size=left_size)
    r2 = p.add_run("\t" + right_text)
    set_run(r2, "\t" + right_text, bold=right_bold, size=right_size)
    return p


def add_bullet(doc, text, indent=Inches(0.25)):
    p = add_para(doc)
    p.paragraph_format.left_indent   = indent
    p.paragraph_format.first_line_indent = Inches(-0.18)
    r = p.add_run("• " + text)
    set_run(r, "• " + text, size=11)
    return p


def fmt_date(d):
    if not d:
        return ""
    months = ["Jan","Feb","Mar","Apr","May","Jun",
              "Jul","Aug","Sep","Oct","Nov","Dec"]
    y, m = d.split("-")
    return f"{months[int(m)-1]}. {y}"


# ── Build document ──────────────────────────────────────────────

doc = new_doc()

# ── HEADER ──────────────────────────────────────────────────────
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after  = Pt(2)
r = p.add_run(data["personal"]["name"])
set_run(r, data["personal"]["name"], bold=True, size=16)

p2 = add_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
contact = (f"{data['personal']['phone']}  |  "
           f"{data['personal']['email']}  |  "
           f"linkedin.com/in/susano-kevin/  |  "
           f"github.com/SusanoKevin  |  "
           f"Milwaukee, WI")
r = p2.add_run(contact)
set_run(r, contact, size=10)

# ── PROFESSIONAL SUMMARY ─────────────────────────────────────────
add_section_header(doc, "PROFESSIONAL SUMMARY", space_before=4)
p = add_para(doc, space_after=2)
summary = (
    "Analytical and detail-oriented professional pursuing a Master's degree in Information "
    "Technology Management with a focus on Data Analytics and Artificial Intelligence. "
    "Currently leading Agentic AI development for the Excelsis360 education platform. "
    "Experienced in building predictive models, designing autonomous agent systems, and "
    "delivering data-driven solutions using Python, scikit-learn, and Snowflake."
)
r = p.add_run(summary)
set_run(r, summary, size=11)

# ── WORK EXPERIENCE ──────────────────────────────────────────────
add_section_header(doc, "WORK EXPERIENCE")

for exp in data["experience"]:
    end = "Present" if exp["current"] else fmt_date(exp["end_date"])
    date_str = f"{fmt_date(exp['start_date'])} – {end}"
    title_company = f"{exp['position']}  |  {exp['company']}, {exp['location']}"
    add_right_tab_para(doc, title_company, date_str,
                       left_bold=True, right_bold=False, space_after=0)
    for ach in exp["achievements"]:
        add_bullet(doc, ach)
    add_para(doc, space_after=2)  # small gap between roles

# ── EDUCATION ────────────────────────────────────────────────────
add_section_header(doc, "EDUCATION")

for edu in data["education"]:
    end = fmt_date(edu["end_date"])
    degree_line = f"{edu['degree']}, {edu['field_of_study']}"
    add_right_tab_para(doc, degree_line, end,
                       left_bold=True, left_size=11, right_size=11, space_after=0)
    p = add_para(doc, space_after=3)
    r = p.add_run(edu["institution"])
    set_run(r, edu["institution"], size=11)

# ── SKILLS ───────────────────────────────────────────────────────
add_section_header(doc, "SKILLS")

skills_col0 = [
    "Programming Languages: Python, SQL, JavaScript, HTML, CSS",
    "Cloud & Data Platforms: Snowflake",
    "Business Intelligence Tools: Power BI, Excel, Access",
]
skills_col1 = [
    "Machine Learning: Random Forest, scikit-learn, SMOTE, GridSearchCV",
    "Data Analysis & Visualization: Pandas, NumPy, Matplotlib, Seaborn, Streamlit",
    "Data Cleaning & Preprocessing",
]

table = doc.add_table(rows=1, cols=2)
table.style = "Table Grid"
# remove all borders
for row in table.rows:
    for cell in row.cells:
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        tcBdr = OxmlElement("w:tcBdr")
        for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
            el = OxmlElement(f"w:{side}")
            el.set(qn("w:val"), "none")
            el.set(qn("w:sz"), "0")
            el.set(qn("w:space"), "0")
            el.set(qn("w:color"), "auto")
            tcBdr.append(el)
        tcPr.append(tcBdr)

for c, skills in enumerate([skills_col0, skills_col1]):
    cell = table.rows[0].cells[c]
    cell.paragraphs[0]._element.getparent().remove(cell.paragraphs[0]._element)
    for skill in skills:
        cp = cell.add_paragraph()
        cp.paragraph_format.space_before = Pt(0)
        cp.paragraph_format.space_after  = Pt(1)
        cp.paragraph_format.left_indent  = Inches(0.1)
        r = cp.add_run("• " + skill)
        set_run(r, "• " + skill, size=11)

# ── PROJECTS ─────────────────────────────────────────────────────
add_section_header(doc, "PROJECTS")

project_bullets = {
    "Churn Predictor Bot": [
        "Built and optimized a Random Forest churn prediction model using GridSearchCV and SMOTE, achieving 80%+ accuracy on imbalanced customer data.",
        "Developed a robust preprocessing pipeline handling missing data, encoding, and feature scaling with ColumnTransformer.",
        "Deployed an interactive Streamlit app for real-time customer churn prediction and visualization.",
    ],
    "Excelsis Attendance Agent": [
        "Designed and built a production AI agent that fully automates attendance tracking end-to-end for the Excelsis360 education platform.",
        "Architected an agentic pipeline handling multi-step workflow logic, reducing manual attendance overhead across the platform.",
    ],
    "LangrisserBot": [
        "Developed an automated Python bot demonstrating core automation architecture and scripted interaction patterns.",
    ],
}

for proj in data["projects"]:
    stack = ", ".join(proj["technologies"])
    header = f"{proj['name']}  ({stack})"
    p = add_para(doc, space_after=0)
    p.paragraph_format.space_before = Pt(2)
    r = p.add_run(header)
    set_run(r, header, bold=True, size=11)
    for bullet in project_bullets.get(proj["name"], []):
        add_bullet(doc, bullet)

# ── CERTIFICATIONS ───────────────────────────────────────────────
add_section_header(doc, "CERTIFICATIONS")

for cert in data["certifications"]:
    date_str = fmt_date(cert["date"])
    cert_text = f"{cert['name']}  —  {cert['issuer']}"
    add_right_tab_para(doc, cert_text, date_str,
                       left_bold=False, right_bold=False, space_after=0)

# ── SAVE ─────────────────────────────────────────────────────────
out = "/Users/susanokevinamalamahilmaran/Downloads/Projects/Resume/Resume_Susano Kevin Amala_032026 (1).docx"
doc.save(out)
print(f"Saved: {out}")
