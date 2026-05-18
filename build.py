#!/usr/bin/env python3
"""Build script: reads resume.json and renders index.html via Jinja2."""

import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def fmt_month_year(date_str):
    """Convert 'YYYY-MM' to 'Month YYYY', or return None."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m").strftime("%B %Y")
    except ValueError:
        return date_str


def fmt_year(date_str):
    """Extract year from 'YYYY-MM', or return None."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m").strftime("%Y")
    except ValueError:
        return date_str


def main():
    src = Path("resume.json")
    if not src.exists():
        print("Error: resume.json not found.", file=sys.stderr)
        sys.exit(1)

    with src.open() as f:
        data = json.load(f)

    # Pre-format dates so the template never calls strftime
    for exp in data.get("experience", []):
        exp["start_date_fmt"] = fmt_month_year(exp.get("start_date"))
        exp["end_date_fmt"] = fmt_month_year(exp.get("end_date"))

    for edu in data.get("education", []):
        edu["start_year"] = fmt_year(edu.get("start_date"))
        edu["end_year"] = fmt_year(edu.get("end_date"))

    for proj in data.get("projects", []):
        proj["start_date_fmt"] = fmt_month_year(proj.get("start_date"))
        proj["end_date_fmt"] = fmt_month_year(proj.get("end_date"))

    for cert in data.get("certifications", []):
        cert["date_fmt"] = fmt_month_year(cert.get("date"))

    # Group skills by category (preserve insertion order)
    skills_by_category = defaultdict(list)
    for skill in data.get("skills", []):
        skills_by_category[skill.get("category", "Other")].append(skill)

    env = Environment(loader=FileSystemLoader("templates"), autoescape=False)
    template = env.get_template("index.html")

    html = template.render(
        personal=data.get("personal"),
        experience=data.get("experience", []),
        education=data.get("education", []),
        certifications=data.get("certifications", []),
        skills_by_category=dict(skills_by_category),
        projects=data.get("projects", []),
    )

    out = Path("index.html")
    out.write_text(html, encoding="utf-8")
    print(f"Built {out} successfully.")


if __name__ == "__main__":
    main()
