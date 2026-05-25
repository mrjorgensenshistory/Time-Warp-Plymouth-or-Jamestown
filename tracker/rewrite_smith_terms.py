"""Rewrite specific Smith slides so key_terms appear in the body prose, not just below.
Per-slide hand-crafted rewrites. Run once. Idempotent (skips if already rewritten).
"""
from pathlib import Path
import json, re

DOCS = Path(__file__).resolve().parent.parent / "docs"
SMITH = DOCS / "smith.html"

# Each entry: (slide_id, original_body_lines, new_body_lines)
# Match is by exact body content so this is safe to re-run.
REWRITES = [
    {
        "slide_id": "slide_1",
        "old_body": [
            "My name is John Smith. I am twenty-seven. I have killed men in Hungary for pay.",
            "The Virginia Company says there is gold up this river. They say a great many things.",
            "I crossed the Atlantic in chains, accused of mutiny. Today they unlock me.",
        ],
        "new_body": [
            "My name is John Smith. I am twenty-seven. I have killed men in Hungary for pay.",
            "The Virginia Company is a joint-stock company — English investors pooled their gold on a royal charter from King James, hoping for more of it up this river.",
            "I crossed the Atlantic in chains, accused of mutiny. Today they unlock me.",
        ],
    },
    {
        "slide_id": "slide_4",
        "old_body": [
            "Of the 104 men who landed, more than half are gentlemen. They came for gold, not corn.",
            "A gentleman in England does not work with his hands. A gentleman in Virginia does not either.",
            "I am not a gentleman. That may be the only thing that saves us.",
        ],
        "new_body": [
            "Of the 104 men who landed, more than half are gentlemen. They came for gold, not corn.",
            "A gentleman in England does not work with his hands. A gentleman in Virginia does not either.",
            "The rest of us are indentured servants — bound to work four to seven years for the cost of our passage.",
            "I am not a gentleman. That may be the only thing that saves us.",
        ],
    },
]


def rewrite():
    text = SMITH.read_text(encoding="utf-8")
    changed = 0
    for r in REWRITES:
        old_json = json.dumps(r["old_body"], ensure_ascii=False)[1:-1]  # strip outer brackets
        new_json = json.dumps(r["new_body"], ensure_ascii=False)[1:-1]
        if new_json in text and old_json not in text:
            print(f"  [skip] {r['slide_id']} — already rewritten")
            continue
        if old_json not in text:
            print(f"  [WARN] {r['slide_id']} — original body not matched")
            continue
        text = text.replace(old_json, new_json, 1)
        changed += 1
        print(f"  [done] {r['slide_id']}")
    if changed:
        SMITH.write_text(text, encoding="utf-8")
        print(f"\nRewrote {changed} slide(s) in smith.html")
    else:
        print("\nNothing changed.")


if __name__ == "__main__":
    rewrite()
