"""
Generates Resume_Susano Kevin Amala.docx from resume.json.
Font: Times New Roman, black throughout. Target: 1 page.
"""

import json
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BLACK  = RGBColor(0, 0, 0)
FONT   = "Times New Roman"
BODY   = 10.5   # pt — body text
HEAD   = 10.5   # pt — section headers
NAME_S = 14     # pt — name
CONT_S = 9.5    # pt — contact line
USABLE_W_TWIPS = int(Inches(7.5).pt * 20)  # right tab stop

with open("/Users/susanokevinamalamahilmaran/Downloads/Projects/Resume/resume.json") as f:
    data = json.load(f)

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun",
          "Jul","Aug","Sep","Oct","Nov","Dec"]

def fmt_date(d):
    if not d:
        return ""
    y, m = d.split("-")
    return f"{MONTHS[int(m)-1]}. {y}"


# ── helpers ──────────────────────────────────────────────────────

def setup_doc():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width    = Inches(8.5)
    sec.page_height   = Inches(11)
    sec.top_margin    = Inches(0.5)
    sec.bottom_margin = Inches(0.5)
    sec.left_margin   = Inches(0.5)
    sec.right_margin  = Inches(0.5)
    s = doc.styles["Normal"]
    s.paragraph_format.space_before = Pt(0)
    s.paragraph_format.space_after  = Pt(0)
    s.font.name  = FONT
    s.font.color.rgb = BLACK
    s.font.size  = Pt(BODY)
    return doc


def run(para, text, bold=False, size=BODY, italic=False):
    r = para.add_run(text)
    r.bold   = bold
    r.italic = italic
    r.font.name      = FONT
    r.font.size      = Pt(size)
    r.font.color.rgb = BLACK
    return r


def para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, sb=0, sa=0):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(sb)
    p.paragraph_format.space_after  = Pt(sa)
    return p


def section_head(doc, title, sb=4):
    p = para(doc, sb=sb, sa=1)
    # bottom border rule
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bot = OxmlElement("w:bottom")
    bot.set(qn("w:val"),   "single")
    bot.set(qn("w:sz"),    "4")
    bot.set(qn("w:space"), "1")
    bot.set(qn("w:color"), "000000")
    pBdr.append(bot)
    pPr.append(pBdr)
    run(p, title, bold=True, size=HEAD)


def right_tab_para(doc, left, right, lb=True, rb=False, sb=0, sa=0):
    p = para(doc, sb=sb, sa=sa)
    pPr = p._p.get_or_add_pPr()
    tabs = OxmlElement("w:tabs")
    tab  = OxmlElement("w:tab")
    tab.set(qn("w:val"), "right")
    tab.set(qn("w:pos"), str(USABLE_W_TWIPS))
    tabs.append(tab)
    pPr.append(tabs)
    run(p, left,        bold=lb, size=BODY)
    run(p, "\t" + right, bold=rb, size=BODY)


def bullet(doc, text, sb=0, sa=0):
    p = para(doc, sb=sb, sa=sa)
    p.paragraph_format.left_indent        = Inches(0.22)
    p.paragraph_format.first_line_indent  = Inches(-0.16)
    run(p, "•  " + text, size=BODY)


# ── Build ────────────────────────────────────────────────────────

doc = setup_doc()

# NAME
p = para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, sa=1)
run(p, data["personal"]["name"], bold=True, size=NAME_S)

# CONTACT
p = para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, sa=3)
contact = (f"{data['personal']['phone']}  |  {data['personal']['email']}  |  "
           f"linkedin.com/in/susano-kevin  |  github.com/SusanoKevin  |  Milwaukee, WI")
run(p, contact, size=CONT_S)

# ── PROFESSIONAL SUMMARY ─────────────────────────────────────────
section_head(doc, "PROFESSIONAL SUMMARY", sb=2)
p = para(doc, sa=1)
summary = (
    "M.S. candidate in Information Technology Management (Data Analytics & AI) at "
    "UW-Milwaukee, currently leading all Agentic AI development for the Excelsis360 "
    "education platform. Experienced in machine learning, predictive modeling, and "
    "autonomous agent design using Python, scikit-learn, and Snowflake."
)
run(p, summary)

# ── WORK EXPERIENCE ──────────────────────────────────────────────
section_head(doc, "WORK EXPERIENCE")

exp_bullets = {
    "Excellerate Education Solutions": [
        "Lead all Agentic AI initiatives for Excelsis360, architecting autonomous agent systems that automate complex, multi-step educational workflows end-to-end",
        "Developed the Excelsis Attendance Agent — a production AI agent that fully eliminates manual attendance tracking across the platform",
    ],
    "Carroll University": [
        "Delivered first-level technical support and end-user training for campus software applications",
        "Managed help desk ticket queue; configured workstations and assisted in system upgrades",
    ],
    "Cardinal Stritch University": [
        "Trained and supervised student workers; resolved system and technology issues for faculty and staff",
    ],
}

for i, exp in enumerate(data["experience"]):
    end      = "Present" if exp["current"] else fmt_date(exp["end_date"])
    date_str = f"{fmt_date(exp['start_date'])} – {end}"
    label    = f"{exp['position']}  |  {exp['company']}, {exp['location']}"
    sb = 2 if i > 0 else 0
    right_tab_para(doc, label, date_str, lb=True, sb=sb)
    for b in exp_bullets.get(exp["company"], []):
        bullet(doc, b)

# ── EDUCATION ────────────────────────────────────────────────────
section_head(doc, "EDUCATION")

edu_lines = [
    ("M.S., Information Technology Management — Data Analytics & AI",
     "University of Wisconsin – Milwaukee", "Dec. 2025"),
    ("B.B.A., Communication Minor",
     "Carroll University", "May 2024"),
]

for i, (degree, institution, date) in enumerate(edu_lines):
    sb = 1 if i > 0 else 0
    right_tab_para(doc, degree, date, lb=True, sb=sb, sa=0)
    p = para(doc, sa=0)
    run(p, institution, size=BODY)

# ── SKILLS ───────────────────────────────────────────────────────
section_head(doc, "SKILLS")

skill_lines = [
    ("Programming Languages", "Python, SQL, JavaScript, HTML, CSS"),
    ("Machine Learning",      "Random Forest, scikit-learn, SMOTE, GridSearchCV"),
    ("Data Analysis & Visualization", "Pandas, NumPy, Matplotlib, Seaborn, Streamlit"),
    ("Cloud & Data Platforms", "Snowflake"),
    ("Business Intelligence", "Power BI, Excel, Access"),
]
for category, items in skill_lines:
    p = para(doc, sa=0)
    run(p, category + ": ", bold=True)
    run(p, items)

# ── PROJECTS ─────────────────────────────────────────────────────
section_head(doc, "PROJECTS")

project_content = [
    {
        "name": "Churn Predictor Bot",
        "tech": "Python, scikit-learn, Streamlit, SMOTE, Pandas",
        "bullet": "Random Forest classifier tuned with GridSearchCV and SMOTE achieving 80%+ accuracy; deployed as an interactive Streamlit app for real-time churn prediction.",
    },
    {
        "name": "Excelsis Attendance Agent",
        "tech": "Python",
        "bullet": "Production AI agent automating end-to-end attendance tracking for the Excelsis360 education platform, eliminating manual overhead.",
    },
    {
        "name": "LangrisserBot",
        "tech": "Python",
        "bullet": None,
    },
]

for i, proj in enumerate(project_content):
    sb = 1 if i > 0 else 0
    p = para(doc, sb=sb, sa=0)
    run(p, f"{proj['name']}  ", bold=True)
    run(p, f"({proj['tech']})", bold=False)
    if proj["bullet"]:
        bullet(doc, proj["bullet"])

# ── CERTIFICATIONS ───────────────────────────────────────────────
section_head(doc, "CERTIFICATIONS")
right_tab_para(doc,
               "Snowflake Platform Training  —  Snowflake",
               "Jun. 2025",
               lb=False)

# ── Save ─────────────────────────────────────────────────────────
out = ("/Users/susanokevinamalamahilmaran/Downloads/Projects/Resume/"
       "Resume_Susano Kevin Amala_032026 (1).docx")
doc.save(out)
print(f"Saved: {out}")
