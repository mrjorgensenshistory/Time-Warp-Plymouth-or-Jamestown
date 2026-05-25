import re, json
from pathlib import Path
DOCS = Path(__file__).resolve().parent.parent / "docs"
for fname in ["smith.html"]:
    t = (DOCS / fname).read_text(encoding="utf-8")
    m = re.search(r'const SLIDES = (\[.*?\]);', t, re.DOTALL)
    slides = json.loads(m.group(1))
    types = {}
    for s in slides:
        types[s.get("type","?")] = types.get(s.get("type","?"), 0) + 1
    print(f"{fname} types: {types}")
    # IDs of slides that lead to HOME (those are end states - victory or shame)
    print("\nSlides with target=HOME:")
    for s in slides:
        for b in s.get("buttons", []):
            if b.get("target") == "HOME":
                print(f"  {s['id']:20s} type={s.get('type','?'):15s} title={s.get('title','')[:50]:50s} button=\"{b['text'][:40]}\"")
    print("\nDead/gameover slide IDs:")
    for s in slides:
        if any(k in s["id"].lower() for k in ["dead", "gameover", "fail"]):
            print(f"  {s['id']:25s} title=\"{s.get('title','')[:60]}\"")
