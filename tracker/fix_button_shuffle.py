"""Patch each character HTML's renderSlide to shuffle buttons (Fisher-Yates) on every render.
Skips slides with only 1 button (no shuffle needed) and respects an optional `shuffle: false` slide flag.
Idempotent. Run from repo root: python tracker/fix_button_shuffle.py
"""
import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
TARGETS = ["smith.html", "rolfe.html", "powhatan.html", "bradford.html",
           "squanto.html", "massasoit.html", "chilton.html"]
# tutorial typically has linear CONTINUE buttons only — skipping unless needed

MARK = "/* === BUTTON SHUFFLE PATCHED === */"

OLD = """  const btnWrap = document.createElement('div');
  btnWrap.className = 'buttons';
  slide.buttons.forEach(b => {"""

NEW = """  const btnWrap = document.createElement('div');
  btnWrap.className = 'buttons';
  /* === BUTTON SHUFFLE PATCHED === */
  let _btns = slide.buttons.slice();
  if (_btns.length > 1 && slide.shuffle !== false) {
    for (let i = _btns.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [_btns[i], _btns[j]] = [_btns[j], _btns[i]];
    }
  }
  _btns.forEach(b => {"""

def patch(path: Path):
    text = path.read_text(encoding="utf-8")
    if MARK in text:
        print(f"  [skip] {path.name} — already patched")
        return
    if OLD not in text:
        print(f"  [WARN] {path.name} — button block not matched")
        return
    new = text.replace(OLD, NEW, 1)
    path.write_text(new, encoding="utf-8")
    print(f"  [done] {path.name}")

def main():
    print(f"Patching button shuffle in {DOCS}")
    for name in TARGETS:
        p = DOCS / name
        if p.exists():
            patch(p)
        else:
            print(f"  [missing] {name}")
    print("Done.")

if __name__ == "__main__":
    main()
