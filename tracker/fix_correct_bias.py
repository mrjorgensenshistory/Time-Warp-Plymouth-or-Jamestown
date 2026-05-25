"""Patch each character HTML so the CORRECT button rarely appears in position 0.

Heuristic for "correct" = target doesn't route to a dead/gameover/fail slide.

After the existing shuffle:
  - If correct button is at position 0, with 60% probability swap it to a later slot.
  - Net effect: correct option is the first to fade in only ~(1/N)*(0.4) of the time.

So for a 3-button decision:
  - Random shuffle alone: 33% chance correct shows first
  - With this bias: ~13% chance correct shows first
  - Combined with 2-sec stagger -> students must wait & read.

Idempotent. Run from repo root: python tracker/fix_correct_bias.py
"""
import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
TARGETS = ["smith.html", "rolfe.html", "powhatan.html", "bradford.html",
           "squanto.html", "massasoit.html", "chilton.html"]

MARK = "/* === CORRECT-BIAS PATCHED === */"

OLD = """  let _btns = slide.buttons.slice();
  if (_btns.length > 1 && slide.shuffle !== false) {
    for (let i = _btns.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [_btns[i], _btns[j]] = [_btns[j], _btns[i]];
    }
  }"""

NEW = """  let _btns = slide.buttons.slice();
  if (_btns.length > 1 && slide.shuffle !== false) {
    // Fisher-Yates shuffle
    for (let i = _btns.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [_btns[i], _btns[j]] = [_btns[j], _btns[i]];
    }
    /* === CORRECT-BIAS PATCHED === */
    // If the "correct" button (one that DOESN'T target dead/gameover/fail) ended up
    // at position 0, with 60% probability swap it with a later slot. Students can't
    // just click the first option that appears.
    const _isWrong = (t) => /dead|gameover|fail|death/i.test(t || '');
    const _correctIdx = _btns.findIndex(b => !_isWrong(b.target));
    if (_correctIdx === 0 && _btns.length > 1 && Math.random() < 0.6) {
      const _newPos = 1 + Math.floor(Math.random() * (_btns.length - 1));
      [_btns[0], _btns[_newPos]] = [_btns[_newPos], _btns[0]];
    }
  }"""

def patch(path: Path):
    text = path.read_text(encoding="utf-8")
    if MARK in text:
        print(f"  [skip] {path.name} — already patched")
        return
    if OLD not in text:
        print(f"  [WARN] {path.name} — shuffle block not matched")
        return
    text = text.replace(OLD, NEW, 1)
    path.write_text(text, encoding="utf-8")
    print(f"  [done] {path.name}")

def main():
    print(f"Patching correct-answer position bias in {DOCS}")
    for name in TARGETS:
        p = DOCS / name
        if p.exists():
            patch(p)
        else:
            print(f"  [missing] {name}")
    print("Done.")

if __name__ == "__main__":
    main()
