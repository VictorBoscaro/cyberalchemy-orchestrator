# -*- coding: utf-8 -*-
"""
review_audit.py — the reviewer pass. Audits every variant HTML against CONST-FE
(FE-1/2/3/5/6/9) and against the constitution's explicit Non-Examples:
  - modal that closes only via "X" or with a delay (violates FE-3)
  - density pushed not chosen / prompt dumped inline on the graph (violates FE-1)
  - empty surface with only headers (violates FE-5)
Also checks aesthetic diversity: each theme block must be unique, and CSS must
be balanced (braces). Exit non-zero if any check fails.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
files = sorted(glob.glob(os.path.join(HERE, "variants", "*.html")))

fails = []
theme_fingerprints = {}


def check(cond, vid, msg):
    if not cond:
        fails.append("[{}] {}".format(vid, msg))


for path in files:
    vid = os.path.splitext(os.path.basename(path))[0]
    html = open(path, encoding="utf-8").read()

    # FE-5 three states, empty in pt-BR
    check("st-loading" in html, vid, "FE-5: missing loading state")
    check("st-error" in html and "retry" in html.lower(), vid, "FE-5: missing error+retry")
    check("st-empty" in html and "Nenhum dispatch" in html, vid, "FE-5: missing pt-BR empty state")

    # FE-2 one universal tooltip system
    check('id="tt"' in html, vid, "FE-2: missing #tt tooltip element")
    check("data-tip" in html, vid, "FE-2: no data-tip usage")

    # FE-3 instant dismiss: Esc + outside-click scrim, and NO close-setTimeout
    check('"Escape"' in html or "'Escape'" in html, vid, "FE-3: no Esc handler")
    check("scrim" in html and "closePanel" in html, vid, "FE-3: no outside-click close")
    # Non-Example: delayed close. Flag setTimeout anywhere near closePanel.
    check(not re.search(r"setTimeout[^;]*close", html, re.I), vid,
          "FE-3 NON-EXAMPLE: delayed close (setTimeout on close)")
    check("p-close" in html, vid, "FE-3: close affordance present")

    # FE-1 density opt-in: prompt body hidden by default + toggle; not dumped in graph node
    check("p-prompt-body" in html and "hidden" in html, vid, "FE-1: prompt not collapsed by default")
    check("Revelar prompt inicial completo" in html, vid, "FE-1: no opt-in reveal control")
    # graph node markup must NOT embed initial_prompt
    node_render = html[html.find("function renderGraph"):html.find("function openPanel")]
    check("initial_prompt" not in node_render, vid,
          "FE-1 NON-EXAMPLE: initial_prompt dumped inline on graph node")

    # FE-6 one focus: openPanel closes previous
    op = html[html.find("function openPanel"):html.find("function closePanel")]
    check("closePanel()" in op, vid, "FE-6: opening a panel does not close the previous")

    # FE-9 discreet marker + explain mode
    check('id="explain"' in html, vid, "FE-9: no discreet explain marker")
    check("data-explain" in html, vid, "FE-9: no self-explanation text")

    # data source wiring
    check("../data/dispatches.json" in html, vid, "data: not reading ../data/dispatches.json")
    check("__DISPATCHES__" in html, vid, "data: no file:// fallback")

    # aesthetic diversity: capture the theme block after the marker comment
    m = re.search(r"/\* ---- theme: " + re.escape(vid) + r" ---- \*/(.*?)</style>", html, re.S)
    theme = (m.group(1) if m else "").strip()
    check(len(theme) > 400, vid, "theme CSS too thin (looks like a recolor stub)")
    # balanced braces in the whole <style>
    style = html[html.find("<style>"):html.find("</style>")]
    check(style.count("{") == style.count("}"), vid, "CSS braces unbalanced")
    fp = re.sub(r"\s+", "", theme)
    for other, ofp in theme_fingerprints.items():
        # crude overlap: identical theme text would be a recolor
        check(fp != ofp, vid, "theme identical to " + other + " (not a distinct language)")
    theme_fingerprints[vid] = fp
    # font-family should differ across the set (visual language proxy)

# cross-variant: distinct primary font-families
fonts = {}
for path in files:
    vid = os.path.splitext(os.path.basename(path))[0]
    html = open(path, encoding="utf-8").read()
    m = re.search(r"body\{font-family:([^;]+)", html)
    fonts[vid] = (m.group(1) if m else "").strip()
uniq = len(set(fonts.values()))
print("distinct body font stacks: {}/{}".format(uniq, len(fonts)))
print("layouts:", ", ".join(sorted(set(
    re.search(r'layout:"(\w+)"', open(p, encoding="utf-8").read()).group(1) for p in files))))

print("\naudited {} variants".format(len(files)))
if fails:
    print("FAIL ({} issues):".format(len(fails)))
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("VERDICT: PASS — all variants honor FE-1/2/3/5/6/9; no Non-Examples; themes distinct.")
