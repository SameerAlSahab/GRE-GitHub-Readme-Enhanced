#!/usr/bin/env python3
"""GRE | lint_readme.py

Check a README for (1) things GitHub will silently break and (2) writing that reads like an AI.
Run it before handing a README to the user.

Usage:
  python lint_readme.py README.md
  python lint_readme.py README.md --strict     # exit 1 if any ERR is found

Severity: ERR = will render wrong on GitHub, WARN = probably wrong/fragile, TIP = polish.
"""
import argparse
import re
import sys

AI_PHRASES = [
    "passionate about", "leverag", "crafting", "crafted", "delve", "tapestry", "cutting-edge", "cutting edge",
    "seamless", "robust", "innovative", "journey", "game-changer", "game changer", "unlock", "elevate",
    "empower", "synerg", "in today's", "ever-evolving", "dive into", "let's connect", "feel free to",
    "stands as", "a testament", "realm", "landscape", "navigate the", "fostering", "harness", "holistic",
    "state-of-the-art", "best-in-class", "world-class", "end-to-end solutions", "i'm a passionate",
    "i am a passionate", "dedicated to", "committed to", "strive to", "no stone unturned",
]
STRIPPED_TAGS = ["script", "style", "iframe", "form", "input", "button", "marquee", "link", "object", "embed", "canvas"]
PAIRED = ["details", "summary", "p", "div", "table", "tr", "td", "th", "picture", "a", "h1", "h2", "h3", "h4", "sub", "sup", "kbd", "pre", "code"]
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u2B06\u2194-\u21AA]")


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    text = re.sub(r"`[^`\n]+`", "``", text)
    return text


def prose_only(text: str) -> str:
    t = re.sub(r"!\[[^\]\n]*\]\([^)\n]*\)", " ", text)
    t = re.sub(r"`[^`\n]*`", " ", t)
    t = re.sub(r"<[^>\n]+>", " ", t)
    t = re.sub(r"\]\([^)\n]*\)", "]", t)
    t = re.sub(r"https?://\S+", " ", t)
    return t


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--mode", choices=["auto", "profile", "project"], default="auto",
                    help="project mode adds section/badge checks (auto-detected from headings)")
    ap.add_argument("--root", help="repo root for checking relative image paths (default: README's folder)")
    a = ap.parse_args()

    raw = open(a.path, encoding="utf-8").read()
    text = strip_code(raw)
    lines = text.splitlines()
    findings = []  # (sev, line, msg)

    def add(sev, ln, msg):
        findings.append((sev, ln, msg))

    # ---------- GitHub compatibility
    for i, ln in enumerate(lines, 1):
        for tag in STRIPPED_TAGS:
            if re.search(rf"<{tag}\b", ln, re.I):
                add("ERR", i, f"<{tag}> is removed by GitHub's sanitizer")
        for m in re.finditer(r"<(\w+)\b([^>]*)>", ln):
            attrs = m.group(2)
            if re.search(r"\sstyle\s*=", attrs, re.I):
                add("ERR", i, f"style= on <{m.group(1)}> is stripped; use align/width/height attributes or a table")
            if re.search(r"\sclass\s*=", attrs, re.I):
                add("WARN", i, f"class= on <{m.group(1)}> does nothing on GitHub")
            if re.search(r"\son\w+\s*=", attrs, re.I):
                add("ERR", i, f"event handler on <{m.group(1)}> is stripped")
        for m in re.finditer(r'(?:src|srcset|href)="([^"]*)"', ln):
            u = m.group(1)
            if re.search(r"\s", u):
                add("ERR", i, f"space inside URL: {u[:60]}... (encode as + or %20)")
            if u.startswith("http://") and "img" in ln[:m.start()].lower():
                add("WARN", i, "http:// image URL; use https:// (mixed content gets blocked)")
        for m in re.finditer(r"!\[[^\]]*\]\(([^)]*)\)", ln):
            u = m.group(1).strip()
            if re.search(r"\s", u) and not re.search(r'\s"[^"]*"$', u):
                add("ERR", i, f"space inside markdown image URL: {u[:60]}...")
            if u.startswith("http://"):
                add("WARN", i, "http:// image URL; use https://")
        if re.search(r"<img\b(?![^>]*\balt=)", ln, re.I):
            add("WARN", i, "<img> without alt text (accessibility, and shows nothing if the service is down)")
        if re.search(r"!\[\]\(", ln):
            add("WARN", i, "markdown image with empty alt text")
        for m in re.finditer(r"https://readme-typing-svg\.[^\s\"')]+", ln):
            if "lines=" not in m.group(0):
                add("ERR", i, "typing-svg URL has no lines= parameter")
        m = re.search(r"readme-typing-svg\.[^\"')\s]*[?&]width=(\d+)", ln)
        if m and int(m.group(1)) > 900:
            add("WARN", i, f"typing-svg width={m.group(1)} is wider than GitHub's content column (~880px)")
        if re.search(r"</summary>\s*\S", ln):
            add("WARN", i, "text right after </summary>; put a blank line after it or markdown inside won't render")
    for i in range(len(lines) - 1):
        if "</summary>" in lines[i] and lines[i + 1].strip() and not lines[i + 1].lstrip().startswith("<"):
            add("WARN", i + 1, "markdown right after </summary> needs a blank line first or it renders as plain text")

    for tag in PAIRED:
        o = len(re.findall(rf"<{tag}(?:\s[^>]*)?>", text, re.I))
        c = len(re.findall(rf"</{tag}>", text, re.I))
        if o != c:
            add("ERR", 0, f"unbalanced <{tag}>: {o} opening vs {c} closing")

    n_img = len(re.findall(r"<img\b|!\[[^\]]*\]\(", text))
    if n_img > 22:
        add("WARN", 0, f"{n_img} images; each is a third-party request. Slow load and more things to break")
    ext = set(re.findall(r"https://([^/\s\"')]+)", text))
    if len(ext) > 9:
        add("TIP", 0, f"{len(ext)} different external hosts. Fewer services = fewer ways to rot")
    if re.search(r"githubstats\.tech", text) and re.search(r"github-readme-stats\.vercel\.app/api\?", text):
        add("TIP", 0, "two stats-card services at once; pick one so the page stays coherent")


    # ---------- placeholders left behind
    for i, ln in enumerate(lines, 1):
        if re.search(r"\{\{[^}]+\}\}", ln):
            add("ERR", i, "unreplaced {{placeholder}}")
        if re.search(r"\bOWNER/REPO\b|\bYOUR_USERNAME\b|<your name>", ln):
            add("WARN", i, "placeholder-looking text (OWNER/REPO, YOUR_USERNAME, <your name>) still present")
    n_todo = len(re.findall(r"<!--\s*TODO", raw))
    if n_todo:
        add("TIP", 0, f"{n_todo} TODO comment(s) left; resolve or tell the user what is missing")

    # ---------- alerts
    for i, ln in enumerate(lines, 1):
        m = re.match(r"\s*>\s*\[!(\w+)\]", ln)
        if m and m.group(1) not in ("NOTE", "TIP", "IMPORTANT", "WARNING", "CAUTION"):
            add("ERR" if m.group(1).upper() in ("NOTE", "TIP", "IMPORTANT", "WARNING", "CAUTION") else "WARN", i,
                f"alert type [!{m.group(1)}] is not valid; use uppercase NOTE, TIP, IMPORTANT, WARNING or CAUTION")

    # ---------- relative images exist?
    import os
    root = a.root or os.path.dirname(os.path.abspath(a.path))
    for i, ln in enumerate(lines, 1):
        for m in re.finditer(r'(?:src="|!\[[^\]]*\]\()(?!https?://|data:|#|/)([^"\s)]+)', ln):
            rel = m.group(1).split("#")[0].split("?")[0]
            if rel and not os.path.exists(os.path.join(root, rel)):
                add("WARN", i, f"relative image not found in repo: {rel}")

    # ---------- project-README checks
    heads = [h.lower() for h in re.findall(r"^#{1,4}\s+(.+?)\s*$", text, re.M)]
    is_project = a.mode == "project" or (a.mode == "auto" and any(re.search(r"install|usage|getting started|features", h) for h in heads))
    if is_project:
        def has_head(*words):
            return any(any(w in h for w in words) for h in heads)
        if not has_head("install", "getting started", "setup", "quick start", "quickstart"):
            add("WARN", 0, "project README has no Installation / Getting started section")
        if not has_head("usage", "example", "how to use", "quick start", "quickstart"):
            add("WARN", 0, "project README has no Usage section")
        if not has_head("license", "licence"):
            add("WARN", 0, "no License section (people need to see how they may use the code)")
        if re.search(r"img\.shields\.io/github/license", text) and not has_head("license", "licence"):
            add("TIP", 0, "license badge without a License section")
        if not re.search(r"workflow/status|actions/workflows?/|travis-ci|circleci|codecov|coveralls", text):
            add("TIP", 0, "no build-status/CI badge (skip only if the repo has no CI)")
        for i, ln in enumerate(lines, 1):
            if "img.shields.io/github/workflow/status" in ln:
                add("WARN", i, "deprecated shields URL; use /github/actions/workflow/status/OWNER/REPO/FILE.yml?branch=main")
            if re.search(r"workflow/status/[^\s\"')]*[?&]color=", ln):
                add("WARN", i, "color= on a build-status badge hides pass/fail colors; remove it")
        if not has_head("feature", "what it does", "about", "overview") and len(text) > 800:
            add("TIP", 0, "no Features/About section")

    # ---------- human-writing checks (prose only)
    prose = prose_only(text)
    plines = prose.splitlines()
    low = prose.lower()
    for ph in AI_PHRASES:
        for m in re.finditer(re.escape(ph), low):
            ln = low.count("\n", 0, m.start()) + 1
            add("WARN", ln, f"AI-sounding phrase: '{ph}'")
    n_em = prose.count("\u2014")
    if n_em:
        first = next(i for i, l in enumerate(plines, 1) if "\u2014" in l)
        add("WARN" if n_em > 1 else "TIP", first, f"{n_em} em dash(es); they're a top AI tell. Use a comma, period or hyphen")
    bullets = [l for l in plines if re.match(r"\s*[-*]\s", l)]
    if len(bullets) >= 4:
        emo = sum(1 for l in bullets if EMOJI.search(re.sub(r"^\s*[-*]\s*", "", l)[:4]))
        bold = sum(1 for l in bullets if re.match(r"\s*[-*]\s+(\S+\s)?\*\*[^*]+\*\*\s*[:\-]", l))
        if emo / len(bullets) > 0.6:
            add("WARN", 0, f"{emo}/{len(bullets)} bullets start with an emoji; it reads templated")
        if bold / len(bullets) > 0.6:
            add("WARN", 0, f"{bold}/{len(bullets)} bullets are '**Label**: text'; vary the shape")
    if re.search(r"^\s*#*\s*hi there|^\s*#*\s*hello,? (?:world|there)|\U0001F44B", low, re.M):
        add("TIP", 0, "greeting boilerplate ('Hi there', waving hand); open with the interesting sentence")
    if re.search(r"\bnot (?:just|only) [^.\n]{3,40}, but (?:also )?", low):
        add("WARN", 0, "'not just X, but Y' construction")
    if re.search(r"\b\w+, \w+,? and \w+\b", low) and len(re.findall(r"\b\w+, \w+,? and \w+\b", low)) >= 4:
        add("TIP", 0, "lots of 'A, B, and C' triples; real people list two things or five")
    words = len(re.findall(r"\w+", prose))
    if words > 40 and prose.count("!") / max(words, 1) > 0.03:
        add("TIP", 0, "heavy on exclamation marks")

    # ---------- report
    order = {"ERR": 0, "WARN": 1, "TIP": 2}
    findings.sort(key=lambda f: (order[f[0]], f[1]))
    seen = set()
    for sev, ln, msg in findings:
        if (sev, ln, msg) in seen:
            continue
        seen.add((sev, ln, msg))
        print(f"{sev:<4} {('L' + str(ln)) if ln else '  -':>5}  {msg}")
    errs = sum(1 for f in seen if f[0] == "ERR")
    warns = sum(1 for f in seen if f[0] == "WARN")
    print(f"\n{errs} error(s), {warns} warning(s), {len(seen) - errs - warns} tip(s)")
    if a.strict and errs:
        sys.exit(1)


if __name__ == "__main__":
    main()
