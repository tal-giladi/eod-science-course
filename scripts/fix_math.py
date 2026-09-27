#!/usr/bin/env python3
"""Normalise math constructs KaTeX rejects: ^\\* -> ^{*}, middle dot inside math -> \\cdot."""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOKEN = re.compile(r"(```[\s\S]*?```|~~~[\s\S]*?~~~)|(`[^`\n]*`)|(\$\$[\s\S]+?\$\$)|(\$(?!\s)[^$\n]+?(?<![\s\\])\$)")
DOT = "\u00b7"


def fixseg(m):
    if m.group(1) or m.group(2):
        return m.group(0)
    s = m.group(0).replace("^\\*", "^{*}").replace("_\\*", "_{*}")
    if DOT in s:
        s = re.sub(r"\\text\{([^{}]*)\}",
                   lambda t: "\\text{" + t.group(1).replace(DOT, "}\\cdot\\text{") + "}" if DOT in t.group(1) else t.group(0), s)
        s = s.replace(DOT, "\\cdot ")
    return s


if __name__ == "__main__":
    for p in ROOT.rglob("*.md"):
        if {".git", "research", "node_modules"} & set(p.parts):
            continue
        t = p.read_text(encoding="utf-8")
        u = TOKEN.sub(fixseg, t)
        if u != t:
            p.write_text(u, encoding="utf-8", newline="\n")
            print("fixed", p.relative_to(ROOT))
