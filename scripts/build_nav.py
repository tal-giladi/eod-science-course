#!/usr/bin/env python3
"""Regenerate _sidebar.md and curriculum/module-specs.md from the files on disk.

Stdlib only. Run from anywhere:  python scripts/build_nav.py
- Sidebar: stage READMEs + lessons (titles from each file's first H1), simulators, projects,
  case studies, capstones, assessments, references. course.py reads lesson links from it.
- Module specs (plan.md §20 deliverable): one section per lesson with prerequisites, time, level,
  objectives, simulations, projects, reading count, assessment and "next", parsed from the lesson.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STAGES = {
    0: "Orientation", 1: "Physics foundations", 2: "Chemistry & energetic materials",
    3: "Hazards & ordnance recognition", 4: "Blast effects", 5: "Detection", 6: "Robotics",
    7: "EOD decision-making", 8: "Forensics & post-blast investigation", 9: "AI & computer vision",
}
SIMS = [
    ("A", "scene-assessment", "Scene Assessment (3D)"), ("B", "eod-robot", "EOD Robot"),
    ("C", "sensor-fusion", "Sensor Fusion"), ("D", "blast-physics", "Blast Physics"),
    ("E", "post-blast", "Post-Blast Investigation"), ("F", "incident-command", "Incident Command"),
    ("G", "robotics-engineering", "Robotics Engineering"), ("H", "recognition-trainer", "Recognition Trainer"),
    ("I", "shock-tube", "Shock Tube & Hugoniot"), ("J", "detection-theory", "Detection-Theory Lab"),
]


def h1(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def short(title: str) -> str:
    """'04.1 · Anatomy of a blast wave' -> ('04.1', 'Anatomy of a blast wave')"""
    return title


def sidebar() -> str:
    L = ["- [Home](/)", "- [How to study this course](curriculum/how-to-study.md)",
         "- [Progress dashboard](dashboard.md)", "- [Curriculum outline & dependency graph](curriculum/course-outline.md)",
         "- [Module specifications](curriculum/module-specs.md)", ""]
    for n, name in STAGES.items():
        d = ROOT / "lessons" / f"stage-{n:02d}"
        if not d.exists():
            continue
        L.append(f"- **{n} · {name}**")
        if (d / "README.md").exists():
            L.append(f"  - [Stage {n} overview](lessons/stage-{n:02d}/README.md)")
        for f in sorted(d.glob("lesson-*.md")):
            L.append(f"  - [{short(h1(f))}](lessons/stage-{n:02d}/{f.name})")
        g = ROOT / "assessments" / f"stage-{n:02d}.md"
        if g.exists():
            L.append(f"  - [Stage {n} gate assessment](assessments/stage-{n:02d}.md)")
    L += ["", "- **Simulators**", "  - [All simulators](sims/index.md)"]
    for sid, slug, name in SIMS:
        if (ROOT / "sims" / slug / "index.html").exists():
            L.append(f"  - [{sid} · {name}](sims/{slug}/index.html ':ignore')")
    L += ["", "- **Programming projects**", "  - [All projects](projects/index.md)"]
    for p in sorted((ROOT / "projects").glob("p*/README.md")):
        L.append(f"  - [{h1(p)}](projects/{p.parent.name}/README.md)")
    L += ["", "- **Case studies**", "  - [All case studies](case-studies/index.md)"]
    for c in sorted((ROOT / "case-studies").glob("cs*.md")):
        L.append(f"  - [{h1(c)}](case-studies/{c.name})")
    L += ["", "- **Capstones**", "  - [Overview](capstones/index.md)"]
    for c in sorted((ROOT / "capstones").glob("c[0-9]*.md")):
        L.append(f"  - [{h1(c)}](capstones/{c.name})")
    L += ["", "- **References**",
          "  - [Sources & reading list](curriculum/sources.md)", "  - [Glossary](references/glossary.md)",
          "  - [Standards & doctrine map](references/standards.md)", "  - [Bibliography by stage](references/bibliography.md)",
          "", "- **Course design**",
          "  - [How the curriculum was derived](curriculum/research-synthesis.md)",
          "  - [Simulation plan](curriculum/simulation-plan.md)", "  - [Project plan](curriculum/project-plan.md)",
          "  - [Assessment plan](curriculum/assessment-plan.md)", "  - [Technology & architecture](curriculum/tech-stack-and-architecture.md)",
          "  - [Quality-control report](curriculum/qc-report.md)", "  - [Authoring brief](curriculum/AUTHORING.md)", ""]
    return "\n".join(L)


def section(text: str, heading: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}[^\n]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def card_field(card: str, name: str) -> str:
    m = re.search(rf"\*\*{name}\*\*\s*(.*?)(?=\*\*[A-Z][a-z]+\*\*|<p class|$)", card, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip(" ·") if m else ""


def module_specs() -> str:
    out = ["# Module specifications", "",
           "Deliverable **3** (`plan.md` §20): for every module — prerequisites, learning objectives, theory,",
           "reading, visual explanation, practical exercise, simulation, programming, assessment, time and",
           "what comes next. Generated from the lessons by `scripts/build_nav.py`; the lesson itself is the",
           "full specification.", ""]
    for n, name in STAGES.items():
        d = ROOT / "lessons" / f"stage-{n:02d}"
        if not d.exists():
            continue
        out += [f"## Stage {n} · {name}", ""]
        for f in sorted(d.glob("lesson-*.md")):
            t = f.read_text(encoding="utf-8")
            card = re.search(r'<div class="module-card">(.*?)</div>', t, re.S)
            card = card.group(1) if card else ""
            theory = [re.sub(r"^#+\s*", "", l) for l in section(t, "Theory").splitlines() if l.startswith("### ")]
            sims = sorted(set(re.findall(r"sims/([a-z-]+)/", t)) - {"common"})
            projs = sorted(set(re.findall(r"projects/(p\d\d-[a-z-]+)/", t)))
            objectives = [l.strip() for l in section(t, "Learning objectives").splitlines() if re.match(r"\s*\d+\.", l)]
            reading = [l for l in section(t, "Reading").splitlines() if l.strip().startswith(("-", "*", "1", "2", "3", "4", "5", "6"))]
            assess = len([l for l in section(t, "Assessment").splitlines() if re.match(r"\s*\d+\.", l)])
            out += [f"### [{h1(f)}](lessons/stage-{n:02d}/{f.name})", "",
                    "| Field | Specification |", "|---|---|",
                    f"| Prerequisites | {card_field(card, 'Prerequisites') or '—'} |",
                    f"| Estimated time | {card_field(card, 'Estimated time') or '—'} |",
                    f"| Level | {card_field(card, 'Level') or '—'} |",
                    f"| Learning objectives | {'<br>'.join(objectives) or '—'} |",
                    f"| Theory | {' · '.join(theory) or '—'} |",
                    f"| Visual explanation | {'mermaid diagram' if '```mermaid' in t else ''}{' + embedded simulator' if '<iframe' in t else ''} |",
                    f"| Simulation | {', '.join(f'[{s}](sims/{s}/index.html)' for s in sims) or '—'} |",
                    f"| Programming | {', '.join(f'[{p}](projects/{p}/README.md)' for p in projs) or 'in-lesson exercises'} |",
                    f"| Reading | {len(reading)} selected items (see lesson) |",
                    f"| Assessment | {assess} questions + hidden-answer exercises; stage gate [assessments/stage-{n:02d}.md](assessments/stage-{n:02d}.md) |",
                    f"| Next | {card_field(card, 'Next') or '—'} |", ""]
    return "\n".join(out).replace("\r", "") + "\n"


if __name__ == "__main__":
    (ROOT / "_sidebar.md").write_text(sidebar(), encoding="utf-8", newline="\n")
    (ROOT / "curriculum" / "module-specs.md").write_text(module_specs(), encoding="utf-8", newline="\n")
    print("wrote _sidebar.md and curriculum/module-specs.md")
