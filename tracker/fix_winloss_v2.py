"""v2 of winloss patch — moves restart-counting into goToSlide wrapper (which we know fires)
instead of relying on showSlide wrap (which has hoisting issues).
Idempotent. Replaces v1 block.
"""
import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
CHARACTERS = ["Smith", "Rolfe", "Powhatan", "Bradford", "Squanto", "Massasoit", "Chilton"]

MARK_V2 = "/* === WINLOSS V2 PATCHED === */"

def build_block(char):
    return f"""
/* === COMPLETION TRACKER INIT === */
TimeWarp.init({{
  game: "Plymouth or Jamestown — {char}",
  webhookUrl: window.TIMEWARP_CONFIG && window.TIMEWARP_CONFIG.webhookUrl,
  requireIdentity: true,
}});
TimeWarp.recordPath("{char}");

/* === WINLOSS V2 PATCHED === */
let _lastSlideType = null;
const _origGoToSlide = goToSlide;
goToSlide = function(target) {{
  if (target === 'HOME') {{
    if (_lastSlideType === 'gameover') {{
      TimeWarp.submit("abandoned").finally(() => {{
        setTimeout(() => {{ window.location.href = HUB_HREF; }}, 1500);
      }});
    }} else {{
      TimeWarp.recordCharacterComplete("{char}");
      TimeWarp.submit("character_complete").finally(() => {{
        setTimeout(() => {{ window.location.href = HUB_HREF; }}, 1500);
      }});
    }}
    return;
  }}
  // Inspect the upcoming slide BEFORE the engine renders it.
  const _next = (typeof SLIDES !== 'undefined') ? SLIDES.find(s => s.id === target) : null;
  if (_next) {{
    _lastSlideType = _next.type;
    if (_next.type === 'gameover') {{
      TimeWarp.recordRestart();
    }}
  }}
  return _origGoToSlide(target);
}};
"""

# Match the v1 block we previously injected (anything from "COMPLETION TRACKER INIT"
# through the closing "};" of the goToSlide reassignment).
V1_PATTERN = re.compile(
    r'/\* === COMPLETION TRACKER INIT === \*/\s*\n'
    r'TimeWarp\.init\(\{\s*\n'
    r'\s*game: "Plymouth or Jamestown — (\w+)",.*?'
    r'goToSlide = function\(target\) \{.*?'
    r'^\};\s*\n',
    re.DOTALL | re.MULTILINE
)

def patch(path: Path):
    text = path.read_text(encoding="utf-8")
    if MARK_V2 in text:
        print(f"  [skip] {path.name} — v2 already applied")
        return
    m = V1_PATTERN.search(text)
    if not m:
        print(f"  [WARN] {path.name} — v1 block pattern not matched")
        return
    char = m.group(1)
    new_block = build_block(char)
    new_text = text[:m.start()] + new_block + text[m.end():]
    path.write_text(new_text, encoding="utf-8")
    print(f"  [done] {path.name} (char={char})")

def main():
    print(f"Patching winloss v2 in {DOCS}")
    for c in CHARACTERS:
        p = DOCS / f"{c.lower()}.html"
        if p.exists():
            patch(p)
        else:
            print(f"  [missing] {p.name}")
    print("Done.")

if __name__ == "__main__":
    main()
