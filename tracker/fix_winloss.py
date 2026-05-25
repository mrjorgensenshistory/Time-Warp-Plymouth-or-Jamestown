"""Patch each character HTML so the tracker correctly distinguishes WIN vs LOSS.

Changes:
  1. Each time showSlide renders a slide with type='gameover', call TimeWarp.recordRestart()
  2. Track the type of the last-rendered slide
  3. When goToSlide('HOME') is called:
      - lastType === 'gameover'  ->  submit "abandoned" (NOT marked as character_complete)
      - otherwise (won)          ->  submit "character_complete"
  4. Do NOT add to completed-character list if abandoned

Idempotent. Run from repo root: python tracker/fix_winloss.py
"""
import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
CHARACTERS = ["Smith", "Rolfe", "Powhatan", "Bradford", "Squanto", "Massasoit", "Chilton"]

MARK = "/* === WINLOSS TRACKING PATCHED === */"

def build_init_block(char):
    return f"""
/* === COMPLETION TRACKER INIT === */
TimeWarp.init({{
  game: "Plymouth or Jamestown — {char}",
  webhookUrl: window.TIMEWARP_CONFIG && window.TIMEWARP_CONFIG.webhookUrl,
  requireIdentity: true,
}});
TimeWarp.recordPath("{char}");

/* === WINLOSS TRACKING PATCHED === */
let _lastSlideType = null;
const _origShowSlide = showSlide;
showSlide = function(idx) {{
  const slide = SLIDES[idx];
  if (slide) {{
    _lastSlideType = slide.type;
    if (slide.type === 'gameover') {{
      TimeWarp.recordRestart();
    }}
  }}
  return _origShowSlide(idx);
}};

const _origGoToSlide = goToSlide;
goToSlide = function(target) {{
  if (target === 'HOME') {{
    if (_lastSlideType === 'gameover') {{
      // Player retreated to hub after dying. NOT a completion.
      TimeWarp.submit("abandoned").finally(() => {{
        setTimeout(() => {{ window.location.href = HUB_HREF; }}, 1500);
      }});
    }} else {{
      // Player reached HUB from a non-gameover slide -> they won.
      TimeWarp.recordCharacterComplete("{char}");
      TimeWarp.submit("character_complete").finally(() => {{
        setTimeout(() => {{ window.location.href = HUB_HREF; }}, 1500);
      }});
    }}
    return;
  }}
  return _origGoToSlide(target);
}};
"""

# Match the existing injected block (from inject_tracker.py)
# Replace it wholesale with the new winloss-aware version
OLD_PATTERN = re.compile(
    r'/\* === COMPLETION TRACKER INIT === \*/\s*\n'
    r'TimeWarp\.init\(\{\s*\n'
    r'\s*game: "Plymouth or Jamestown — (\w+)",.*?'
    r'goToSlide = function\(target\) \{.*?'
    r'\};\s*\n',
    re.DOTALL
)

def patch(path: Path):
    text = path.read_text(encoding="utf-8")
    if MARK in text:
        print(f"  [skip] {path.name} — already patched")
        return
    m = OLD_PATTERN.search(text)
    if not m:
        print(f"  [WARN] {path.name} — old tracker block not found, can't patch")
        return
    char = m.group(1)
    new_block = build_init_block(char)
    new_text = text[:m.start()] + new_block + text[m.end():]
    path.write_text(new_text, encoding="utf-8")
    print(f"  [done] {path.name} (char={char})")

def main():
    print(f"Patching win/loss tracking in {DOCS}")
    for c in CHARACTERS:
        p = DOCS / f"{c.lower()}.html"
        if p.exists():
            patch(p)
        else:
            print(f"  [missing] {p.name}")
    print("Done.")

if __name__ == "__main__":
    main()
