#!/usr/bin/env python3
"""Link checker for the course (stdlib only).

  python scripts/check_links.py            internal links only (fast)
  python scripts/check_links.py --external also fetch every external URL (slow; writes a report)

Internal links are root-relative (docsify): `lessons/stage-04/lesson-01.md`, `sims/x/index.html`,
optionally with `#anchor` or docsify `?id=`. External results go to curriculum/link-report.md.
"""
from __future__ import annotations

import concurrent.futures as cf
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD_LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+'[^']*')?\)")
HTML_REF = re.compile(r"(?:href|src)=\"([^\"]+)\"")
URL = re.compile(r"https?://(?:[^\s()<>\"'`|\]]|\([^\s()<>]*\))+")
SKIP_DIRS = {".git", "node_modules", ".claude", "research"}


def files():
    for p in ROOT.rglob("*"):
        if p.suffix in {".md", ".html"} and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS):
            yield p


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def internal_targets(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix == ".md":
        text = strip_code(text)
        links = MD_LINK.findall(text) + HTML_REF.findall(text)
    else:
        links = HTML_REF.findall(text)
    for link in links:
        if re.match(r"^(https?:|mailto:|#|javascript:|data:)", link) or "${" in link or "' +" in link:
            continue
        yield link


def resolve(src: Path, link: str) -> Path | None:
    link = link.split("#")[0].split("?")[0]
    if not link or link == "/":
        return ROOT / "README.md"
    if src.suffix == ".html" and "sims" in src.parts:
        base = src.parent  # simulator pages use relative paths
    else:
        base = ROOT        # docsify: root-relative
    target = (base / link.lstrip("/")).resolve()
    return target


def check_internal() -> list[str]:
    bad = []
    for f in files():
        for link in internal_targets(f):
            t = resolve(f, link)
            if t is None:
                continue
            if not t.exists() and not (t.suffix == "" and t.with_suffix(".md").exists()):
                bad.append(f"{f.relative_to(ROOT)} -> {link}")
    return bad


def fetch(url: str) -> tuple[str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (course link checker)"}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return url, str(r.status)
    except urllib.error.HTTPError as e:
        return url, f"HTTP {e.code}"
    except Exception as e:  # noqa: BLE001
        return url, type(e).__name__


def check_external() -> dict[str, str]:
    urls = set()
    for f in files():
        for u in URL.findall(f.read_text(encoding="utf-8", errors="replace")):
            u = u.rstrip(".,;:*")
            if "cdn.jsdelivr.net" in u or "localhost" in u or "github.com/tal-giladi" in u:
                continue
            urls.add(u)
    with cf.ThreadPoolExecutor(16) as ex:
        return dict(ex.map(fetch, sorted(urls)))


if __name__ == "__main__":
    bad = check_internal()
    print(f"internal: {len(bad)} broken")
    for b in bad:
        print("  ", b)
    if "--external" in sys.argv:
        res = check_external()
        ok = {u: s for u, s in res.items() if s.startswith("2")}
        blocked = {u: s for u, s in res.items() if s in ("HTTP 403", "HTTP 429", "HTTP 401", "HTTP 405")}
        broken = {u: s for u, s in res.items() if u not in ok and u not in blocked}
        lines = ["# External link report", "", f"Checked {len(res)} URLs: {len(ok)} OK, {len(blocked)} refused automated access "
                 f"(403/429/401/405 — usually bot protection; verify in a browser), {len(broken)} failing.", ""]
        if broken:
            lines += ["## Failing", "", "| URL | Result |", "|---|---|"] + [f"| {u} | {s} |" for u, s in sorted(broken.items())] + [""]
        if blocked:
            lines += ["## Refused automated access", "", "| URL | Result |", "|---|---|"] + [f"| {u} | {s} |" for u, s in sorted(blocked.items())] + [""]
        (ROOT / "curriculum" / "link-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print(f"external: {len(ok)} ok, {len(blocked)} blocked, {len(broken)} failing -> curriculum/link-report.md")
    sys.exit(1 if bad else 0)
