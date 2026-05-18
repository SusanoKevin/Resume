"""
Generates Resume_Susano Kevin Amala.docx from resume.json.
Font: Times New Roman, black throughout. Target: 1 full page.
"""

import json
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BLACK  = RGBColor(0, 0, 0)
FONT   = "Times New Roman"
BODY   = 11.25  # pt — body / bullets
HEAD   = 11.25  # pt — section headers
NAME_S = 14     # pt — name
CONT_S = 9.5    # pt — contact line
USABLE_W_TWIPS = int(Inches(7.5).pt * 20)

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
    s.font.name      = FONT
    s.font.color.rgb = BLACK
    s.font.size      = Pt(BODY)
    return doc


def run(p, text, bold=False, size=BODY, italic=False):
    r = p.add_run(text)
    r.bold        = bold
    r.italic      = italic
    r.font.name   = FONT
    r.font.size   = Pt(size)
    r.font.color.rgb = BLACK
    return r


def para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, sb=0, sa=0):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(sb)
    p.paragraph_format.space_after  = Pt(sa)
    return p


def section_head(doc, title, sb=6):
    p = para(doc, sb=sb, sa=1)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bot  = OxmlElement("w:bottom")
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
    run(p, left,         bold=lb, size=BODY)
    run(p, "\t" + right, bold=rb, size=BODY)


def bullet(doc, text, sa=1):
    p = para(doc, sa=sa)
    p.paragraph_format.left_indent       = Inches(0.22)
    p.paragraph_format.first_line_indent = Inches(-0.16)
    run(p, "•  " + text, size=BODY)


# ── Build ────────────────────────────────────────────────────────

doc = setup_doc()

# ── HEADER ───────────────────────────────────────────────────────
p = para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, sa=2)
run(p, data["personal"]["name"], bold=True, size=NAME_S)

p = para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, sa=0)
contact = (f"{data['personal']['phone']}  |  {data['personal']['email']}  |  "
           f"linkedin.com/in/susano-kevin  |  github.com/SusanoKevin  |  Milwaukee, WI")
run(p, contact, size=CONT_S)

# ── PROFESSIONAL SUMMARY ─────────────────────────────────────────
section_head(doc, "PROFESSIONAL SUMMARY", sb=6)
p = para(doc, sa=1)
summary = (
    "M.S. graduate in Information Technology Management (Data Analytics & AI) from "
    "UW–Milwaukee, currently heading all Agentic AI development for the Excelsis360 "
    "education platform. Skilled in machine learning, autonomous agent design, and "
    "delivering data-driven solutions using Python, scikit-learn, and Snowflake."
)
run(p, summary)

# ── WORK EXPERIENCE ──────────────────────────────────────────────
section_head(doc, "WORK EXPERIENCE")

exp_bullets = {
    "Excellerate Education Solutions": [
        "Head all Agentic AI initiatives for the Excelsis360 platform, architecting autonomous agent systems that automate complex, multi-step educational workflows end-to-end",
        "Designing and developing the Excelsis Attendance Agent — an AI agent to fully automate attendance tracking and eliminate manual data entry across the platform",
        "Define the Agentic AI roadmap by identifying high-value automation targets, designing agent pipelines, and delivering working solutions directly into the live product",
    ],
    "Carroll University": [
        "Provided first-level technical support and conducted end-user training sessions for campus software applications used by faculty, staff, and students",
        "Managed help desk ticket queue, diagnosing and resolving hardware and software issues within defined SLA deadlines",
        "Configured new workstations, maintained accurate service records, and assisted in system upgrade deployments across campus",
    ],
    "Cardinal Stritch University": [
        "Trained and supervised student workers on essential job functions and task completion within the Track-IT help desk system",
        "Served as primary escalation point for complex technology issues, providing guided resolution and clear communication to clients",
    ],
}

for i, exp in enumerate(data["experience"]):
    end      = "Present" if exp["current"] else fmt_date(exp["end_date"])
    date_str = f"{fmt_date(exp['start_date'])} – {end}"
    label    = f"{exp['position']}  |  {exp['company']}, {exp['location']}"
    sb = 4 if i > 0 else 0
    right_tab_para(doc, label, date_str, lb=True, sb=sb, sa=0)
    for b in exp_bullets.get(exp["company"], []):
        bullet(doc, b)

# ── EDUCATION ────────────────────────────────────────────────────
section_head(doc, "EDUCATION")

edu_entries = [
    ("M.S., Information Technology Management — Data Analytics & AI",
     "University of Wisconsin – Milwaukee", "Dec. 2025"),
    ("B.S., Business Administration — Communication Minor",
     "Carroll University", "May 2024"),
]

for i, (degree, institution, date) in enumerate(edu_entries):
    sb = 3 if i > 0 else 0
    right_tab_para(doc, degree, date, lb=True, sb=sb, sa=0)
    p = para(doc, sa=0)
    run(p, institution, italic=True)

# ── SKILLS ───────────────────────────────────────────────────────
section_head(doc, "SKILLS")

skill_lines = [
    ("Programming Languages", "Python, TypeScript, JavaScript, SQL, HTML, CSS"),
    ("Agentic AI",            "LangChain, LangGraph, MCP, Ollama"),
    ("Frontend & APIs",       "React, Tailwind CSS, FastAPI, Streamlit"),
    ("Machine Learning",      "scikit-learn, Random Forest, SMOTE, GridSearchCV, Pandas, NumPy"),
    ("Cloud & BI",            "Snowflake, SQL Server, Power BI, Excel, Microsoft Access"),
]
for category, items in skill_lines:
    p = para(doc, sa=1)
    run(p, category + ": ", bold=True)
    run(p, items)

# ── PROJECTS ─────────────────────────────────────────────────────
section_head(doc, "PROJECTS")

projects = [
    {
        "name":   "Churn Predictor Bot",
        "tech":   "Python, scikit-learn, Streamlit, SMOTE, Pandas",
        "github": "github.com/SusanoKevin/Churn-Predictor",
        "bullets": [
            "Built a Random Forest classifier tuned with GridSearchCV and SMOTE to handle class imbalance, achieving 80%+ accuracy on customer churn prediction",
            "Developed a full preprocessing pipeline (missing data handling, encoding, scaling) and deployed the model as an interactive Streamlit app for real-time prediction and visualization",
        ],
    },
    {
        "name":   "Excelsis Attendance Agent",
        "tech":   "Python, LangChain, LangGraph, FastAPI, MCP, Ollama",
        "github": "github.com/SusanoKevin/Excelsis-Attendance-Agent",
        "bullets": [
            "Building an AI agent to automate end-to-end attendance tracking for the Excelsis360 platform, designing multi-step agentic pipelines to handle workflows autonomously",
        ],
    },
]

for i, proj in enumerate(projects):
    sb = 3 if i > 0 else 0
    p = para(doc, sb=sb, sa=0)
    run(p, proj["name"] + "  ", bold=True)
    run(p, f"({proj['tech']})  —  {proj['github']}", italic=True)
    for b in proj["bullets"]:
        bullet(doc, b)

# ── CERTIFICATIONS ───────────────────────────────────────────────
section_head(doc, "CERTIFICATIONS")
right_tab_para(doc,
               "Snowflake Platform Training  —  Snowflake, Inc.",
               "Jun. 2025",
               lb=False)

# ── Save ─────────────────────────────────────────────────────────
out = ("/Users/susanokevinamalamahilmaran/Downloads/Projects/Resume/"
       "Resume_Susano Kevin Amala_032026 (1).docx")
doc.save(out)
print(f"Saved: {out}")
