"""Patch each character HTML to stagger button reveals.
  - 1 button (CONTINUE) -> appears immediately, no delay
  - 2+ buttons -> first appears at 1s, each subsequent +2s
  - Each appears with a quick fade-in; not clickable until visible
Idempotent. Run from repo root: python tracker/fix_button_reveal.py
"""
import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
TARGETS = ["smith.html", "rolfe.html", "powhatan.html", "bradford.html",
           "squanto.html", "massasoit.html", "chilton.html"]

MARK = "/* === BUTTON REVEAL PATCHED === */"

# After button shuffle patch, the block looks like:
#   _btns.forEach(b => {
#     const btn = document.createElement('button');
#     btn.className = 'choice';
#     btn.textContent = b.text;
#     btn.addEventListener('click', () => goToSlide(b.target));
#     btnWrap.appendChild(btn);
#   });
OLD = """  _btns.forEach(b => {
    const btn = document.createElement('button');
    btn.className = 'choice';
    btn.textContent = b.text;
    btn.addEventListener('click', () => goToSlide(b.target));
    btnWrap.appendChild(btn);
  });"""

NEW = """  /* === BUTTON REVEAL PATCHED === */
  const _REVEAL_INITIAL = (slide.revealInitial != null) ? slide.revealInitial : (_btns.length > 1 ? 1000 : 0);
  const _REVEAL_STAGGER = (slide.revealStagger != null) ? slide.revealStagger : (_btns.length > 1 ? 2000 : 0);
  _btns.forEach((b, i) => {
    const btn = document.createElement('button');
    btn.className = 'choice';
    btn.textContent = b.text;
    btn.addEventListener('click', () => goToSlide(b.target));
    if (_btns.length > 1) {
      btn.style.opacity = '0';
      btn.style.pointerEvents = 'none';
      btn.style.transform = 'translateY(8px)';
      btn.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      setTimeout(() => {
        btn.style.opacity = '1';
        btn.style.pointerEvents = 'auto';
        btn.style.transform = 'translateY(0)';
      }, _REVEAL_INITIAL + i * _REVEAL_STAGGER);
    }
    btnWrap.appendChild(btn);
  });"""

def patch(path: Path):
    text = path.read_text(encoding="utf-8")
    if MARK in text:
        print(f"  [skip] {path.name} — already patched")
        return
    if OLD not in text:
        print(f"  [WARN] {path.name} — button forEach block not matched")
        return
    text = text.replace(OLD, NEW, 1)
    path.write_text(text, encoding="utf-8")
    print(f"  [done] {path.name}")

def main():
    print(f"Patching staggered button reveal in {DOCS}")
    for name in TARGETS:
        p = DOCS / name
        if p.exists():
            patch(p)
        else:
            print(f"  [missing] {name}")
    print("Done.")

if __name__ == "__main__":
    main()
