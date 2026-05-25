"""Inject the completion tracker into every Plymouth/Jamestown HTML.
Idempotent: detects existing injection markers and skips.
Run from repo root: python tracker/inject_tracker.py
"""
import re, sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"

CHARACTERS = ["Smith", "Rolfe", "Powhatan", "Bradford", "Squanto", "Massasoit", "Chilton"]

# Scripts injected before </head> in every game HTML
HEAD_SCRIPTS = '''
<!-- COMPLETION TRACKER -->
<script src="tracker/config.js"></script>
<script src="tracker/completionTracker.js"></script>
'''

# Init call + goToSlide wrapper for character HTMLs
def character_init_js(char_name):
    return f'''
/* === COMPLETION TRACKER INIT === */
TimeWarp.init({{
  game: "Plymouth or Jamestown — {char_name}",
  webhookUrl: window.TIMEWARP_CONFIG && window.TIMEWARP_CONFIG.webhookUrl,
  requireIdentity: true,
}});
TimeWarp.recordPath("{char_name}");
const _origGoToSlide = goToSlide;
goToSlide = function(target) {{
  if (target === 'HOME') {{
    TimeWarp.recordCharacterComplete("{char_name}");
    TimeWarp.submit("character_complete").finally(() => {{
      setTimeout(() => {{ window.location.href = HUB_HREF; }}, 1500);
    }});
    return;
  }}
  return _origGoToSlide(target);
}};
'''

# Hub init + progress display
HUB_INIT_JS = '''
/* === COMPLETION TRACKER (HUB) === */
TimeWarp.init({
  game: "Plymouth or Jamestown",
  webhookUrl: window.TIMEWARP_CONFIG && window.TIMEWARP_CONFIG.webhookUrl,
  requireIdentity: true,
}).then(() => {
  const REQUIRED = ["Smith", "Rolfe", "Powhatan", "Bradford", "Squanto", "Massasoit", "Chilton"];
  const done = TimeWarp.getCompletedCharacters();

  // Visual progress badge in top-right
  const badge = document.createElement("div");
  badge.id = "tw-progress-badge";
  badge.style.cssText = "position:fixed;top:14px;right:14px;z-index:9999;background:rgba(0,0,0,.7);color:#fdf6e3;border:2px solid #b8860b;border-radius:10px;padding:10px 16px;font-family:'Bangers',sans-serif;letter-spacing:2px;font-size:18px;box-shadow:0 4px 16px rgba(0,0,0,.5);";
  badge.innerHTML = `PROGRESS: <span style="color:#b8860b">${done.length}/${REQUIRED.length}</span> COMPLETE`;
  document.body.appendChild(badge);

  // Mark completed character cards with a ✓
  setTimeout(() => {
    document.querySelectorAll("[data-character]").forEach(el => {
      const name = el.getAttribute("data-character");
      if (done.includes(name)) {
        const tick = document.createElement("div");
        tick.textContent = "✓";
        tick.style.cssText = "position:absolute;top:8px;right:12px;font-size:42px;color:#4ade80;text-shadow:2px 2px 0 #000;font-family:'Bangers',sans-serif;z-index:5;";
        el.style.position = "relative";
        el.appendChild(tick);
      }
    });
  }, 300);

  // Full-game completion submission (fires once when last character ticks over)
  if (TimeWarp.isFullyComplete(REQUIRED) && !localStorage.getItem("twpoj_final_submitted")) {
    localStorage.setItem("twpoj_final_submitted", "1");
    TimeWarp.submit("completed");
    // Victory overlay
    const v = document.createElement("div");
    v.style.cssText = "position:fixed;inset:0;z-index:99997;background:rgba(0,0,0,.92);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Bangers',sans-serif;color:#fdf6e3;text-align:center;padding:40px;";
    v.innerHTML = `
      <div style="font-size:96px;color:#b8860b;letter-spacing:6px;text-shadow:4px 4px 0 #000;">VICTORY</div>
      <div style="font-size:32px;margin-top:20px;max-width:800px;">You have lived all seven lives. The story of the first English in America — settled, lost, and remembered — is yours now.</div>
      <button onclick="this.parentElement.remove()" style="margin-top:40px;padding:14px 36px;font-family:'Bangers',sans-serif;font-size:24px;letter-spacing:3px;background:#b8860b;color:#000;border:none;border-radius:8px;cursor:pointer;">CLOSE</button>
    `;
    document.body.appendChild(v);
  }
});
'''

# Tutorial init - identity-optional, no submit
TUTORIAL_INIT_JS = '''
/* === COMPLETION TRACKER (TUTORIAL — no submit, identity optional) === */
TimeWarp.init({
  game: "Plymouth or Jamestown — Tutorial",
  webhookUrl: window.TIMEWARP_CONFIG && window.TIMEWARP_CONFIG.webhookUrl,
  requireIdentity: false,
});
'''

MARK = "/* === COMPLETION TRACKER"   # idempotency marker
HEAD_MARK = "<!-- COMPLETION TRACKER -->"


def inject(path: Path, init_js: str):
    text = path.read_text(encoding="utf-8")
    if MARK in text or HEAD_MARK in text:
        print(f"  [skip] {path.name} — already injected")
        return False

    # Add scripts before </head>
    if "</head>" not in text:
        print(f"  [WARN] {path.name} — no </head>, skipping")
        return False
    text = text.replace("</head>", HEAD_SCRIPTS + "</head>", 1)

    # Add init JS at the START of the LAST <script> block (the inline JS one)
    # Find last <script> opening tag (not src="...")
    matches = list(re.finditer(r'<script>\s*\n', text))
    if not matches:
        print(f"  [WARN] {path.name} — no inline <script>, only head injected")
        path.write_text(text, encoding="utf-8")
        return True
    m = matches[-1]
    insert_at = m.end()
    text = text[:insert_at] + init_js + "\n" + text[insert_at:]

    path.write_text(text, encoding="utf-8")
    print(f"  [done] {path.name}")
    return True


def main():
    print(f"Injecting tracker into {DOCS}")
    if not DOCS.exists():
        print(f"  ERROR: {DOCS} does not exist")
        sys.exit(1)

    # Characters
    for c in CHARACTERS:
        p = DOCS / f"{c.lower()}.html"
        if p.exists():
            inject(p, character_init_js(c))
        else:
            print(f"  [missing] {p.name}")

    # Hub
    hub = DOCS / "index.html"
    if hub.exists():
        inject(hub, HUB_INIT_JS)

    # Tutorial
    tut = DOCS / "tutorial.html"
    if tut.exists():
        inject(tut, TUTORIAL_INIT_JS)

    print("Done.")


if __name__ == "__main__":
    main()
