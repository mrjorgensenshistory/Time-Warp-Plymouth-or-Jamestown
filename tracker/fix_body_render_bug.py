"""URGENT FIX: removes the broken _boldTerms regex in renderSlide that was throwing
SyntaxError and blanking the game. Restores plain body render. Key terms still show
below as **Name:** def.

Run from repo root: python tracker/fix_body_render_bug.py
"""
from pathlib import Path
import re

DOCS = Path(__file__).resolve().parent.parent / "docs"
TARGETS = ["smith.html", "rolfe.html", "powhatan.html", "bradford.html",
           "squanto.html", "massasoit.html", "chilton.html", "tutorial.html"]

# Match the entire broken _boldTerms block + the body forEach (multi-line, flexible whitespace)
BROKEN_BLOCK = re.compile(
    r'/\* === KEY-TERM RENDER PATCHED === \*/\s*\n'
    r'\s*const body = document\.createElement\(\'div\'\);\s*\n'
    r'\s*body\.className = \'body\';\s*\n'
    r'.*?'  # eat the broken _boldTerms helper
    r'slide\.body\.forEach\(p => \{\s*\n'
    r'\s*const para = document\.createElement\(\'p\'\);\s*\n'
    r'\s*para\.innerHTML = .*?;\s*\n'
    r'\s*body\.appendChild\(para\);\s*\n'
    r'\s*\}\);\s*\n'
    r'\s*card\.appendChild\(body\);',
    re.DOTALL
)

CLEAN_BLOCK = '''/* === KEY-TERM RENDER PATCHED (body bug fix) === */
  const body = document.createElement('div');
  body.className = 'body';
  slide.body.forEach(p => {
    const para = document.createElement('p');
    para.innerHTML = p;
    body.appendChild(para);
  });
  card.appendChild(body);'''

MARK = "KEY-TERM RENDER PATCHED (body bug fix)"

def fix(path: Path):
    text = path.read_text(encoding="utf-8")
    if MARK in text:
        print(f"  [skip] {path.name} — already fixed")
        return
    new = BROKEN_BLOCK.sub(CLEAN_BLOCK, text)
    if new == text:
        print(f"  [WARN] {path.name} — broken block pattern not matched")
        return
    path.write_text(new, encoding="utf-8")
    print(f"  [fixed] {path.name}")

def main():
    print(f"Fixing body render bug in {DOCS}")
    for n in TARGETS:
        p = DOCS / n
        if p.exists(): fix(p)
    print("Done.")

if __name__ == "__main__":
    main()
