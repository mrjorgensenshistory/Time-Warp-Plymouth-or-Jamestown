import re, json, sys
from pathlib import Path
DOCS = Path(__file__).resolve().parent.parent / "docs"
for fname in ["smith.html", "rolfe.html", "powhatan.html", "bradford.html", "squanto.html", "massasoit.html", "chilton.html"]:
    f = DOCS / fname
    if not f.exists(): continue
    t = f.read_text(encoding="utf-8")
    m = re.search(r'const SLIDES = (\[.*?\]);', t, re.DOTALL)
    if not m: print(f"{fname}: SLIDES not found"); continue
    slides = json.loads(m.group(1))
    multi = [s for s in slides if len(s.get("buttons", [])) > 1]
    if not multi: continue
    # count correct-answer positions
    pos_counts = {}
    for s in multi:
        for i, b in enumerate(s["buttons"]):
            target = b.get("target", "")
            # heuristic: "correct" = goes to next slide_N+1 (story continues), "wrong" = goes to dead_*/gameover_*
            is_dead = "dead" in target.lower() or "gameover" in target.lower() or "death" in target.lower() or "fail" in target.lower()
            if not is_dead:
                pos_counts[i] = pos_counts.get(i, 0) + 1
                break  # only count first non-dead per slide
    print(f"{fname}: {len(multi)} decision slides | correct-answer position counts: {dict(sorted(pos_counts.items()))}")
