"""Patch each character HTML so endings cannot be skipped.

Any slide that has a button targeting HOME (i.e., the "Return to Hub" / ending slide)
gets a hard delay before the HOME button becomes clickable. Students MUST sit and
read the historical reveal — they cannot speed-escape to the hub.

Defaults:
  - Non-gameover endings (the "what really happened" reveal): 12 seconds
  - Gameover endings (showing why they failed): 8 seconds
  - Configurable per slide via `homeDelay: <ms>` in the JSON.

Plus a visible countdown badge on the button: "Read (8)... (7)... (6)..."

Idempotent. Run from repo root: python tracker/fix_ending_lockout.py
"""
import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
TARGETS = ["smith.html", "rolfe.html", "powhatan.html", "bradford.html",
           "squanto.html", "massasoit.html", "chilton.html"]

MARK = "/* === ENDING LOCKOUT PATCHED === */"

# After all prior patches, the button forEach block looks like the BUTTON REVEAL block.
OLD = """  /* === BUTTON REVEAL PATCHED === */
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

NEW = """  /* === ENDING LOCKOUT PATCHED === */
  const _REVEAL_INITIAL = (slide.revealInitial != null) ? slide.revealInitial : (_btns.length > 1 ? 1000 : 0);
  const _REVEAL_STAGGER = (slide.revealStagger != null) ? slide.revealStagger : (_btns.length > 1 ? 2000 : 0);
  const _isEnding = _btns.some(b => b.target === 'HOME');
  const _homeDelay = slide.homeDelay != null
    ? slide.homeDelay
    : (slide.type === 'gameover' ? 8000 : 12000);

  _btns.forEach((b, i) => {
    const btn = document.createElement('button');
    btn.className = 'choice';
    const _origText = b.text;
    btn.textContent = _origText;
    btn.addEventListener('click', () => goToSlide(b.target));

    // Multi-button stagger (existing behavior)
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

    // Ending lockout: HOME-target buttons get an extra delay + countdown badge
    if (b.target === 'HOME' && _homeDelay > 0) {
      btn.style.pointerEvents = 'none';
      btn.style.opacity = '0.45';
      btn.style.filter = 'grayscale(0.6)';
      btn.style.cursor = 'wait';
      const startTime = Date.now();
      const tick = () => {
        const remaining = Math.ceil((_homeDelay - (Date.now() - startTime)) / 1000);
        if (remaining > 0) {
          btn.textContent = _origText + '  (' + remaining + ')';
          setTimeout(tick, 250);
        } else {
          btn.textContent = _origText;
          btn.style.pointerEvents = 'auto';
          btn.style.opacity = '1';
          btn.style.filter = 'none';
          btn.style.cursor = 'pointer';
        }
      };
      tick();
    }
    btnWrap.appendChild(btn);
  });"""

def patch(path: Path):
    text = path.read_text(encoding="utf-8")
    if MARK in text:
        print(f"  [skip] {path.name} — already patched")
        return
    if OLD not in text:
        print(f"  [WARN] {path.name} — reveal block not matched (run fix_button_reveal.py first)")
        return
    text = text.replace(OLD, NEW, 1)
    path.write_text(text, encoding="utf-8")
    print(f"  [done] {path.name}")

def main():
    print(f"Patching ending lockout in {DOCS}")
    for name in TARGETS:
        p = DOCS / name
        if p.exists():
            patch(p)
        else:
            print(f"  [missing] {name}")
    print("Done.")

if __name__ == "__main__":
    main()
