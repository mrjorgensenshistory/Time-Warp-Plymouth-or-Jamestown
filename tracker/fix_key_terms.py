"""Patch the renderSlide function in every Plymouth HTML to:
  1. Auto-bold any key_term name where it appears in body text
  2. Render key_terms below body as <strong>Name:</strong> definition (no KEY TERM chip label)

Idempotent. Run from repo root: python tracker/fix_key_terms.py
"""
import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
TARGETS = ["smith.html", "rolfe.html", "powhatan.html", "bradford.html",
           "squanto.html", "massasoit.html", "chilton.html", "tutorial.html"]

MARK = "/* === KEY-TERM RENDER PATCHED === */"

OLD_BODY_BLOCK = r"""  const body = document.createElement\('div'\);
  body\.className = 'body';
  slide\.body\.forEach\(p => \{
    const para = document\.createElement\('p'\);
    para\.innerHTML = p;
    body\.appendChild\(para\);
  \}\);
  card\.appendChild\(body\);"""

NEW_BODY_BLOCK = """  /* === KEY-TERM RENDER PATCHED === */
  const body = document.createElement('div');
  body.className = 'body';
  // Auto-bold any key_term name found in body text (word-boundary, case-insensitive).
  const _boldTerms = (line) => {
    if (!slide.key_terms) return line;
    let out = line;
    slide.key_terms.forEach(kt => {
      const escaped = kt.name.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&');
      const re = new RegExp('\\\\b(' + escaped + ')\\\\b', 'gi');
      out = out.replace(re, '<strong>$1</strong>');
    });
    return out;
  };
  slide.body.forEach(p => {
    const para = document.createElement('p');
    para.innerHTML = _boldTerms(p);
    body.appendChild(para);
  });
  card.appendChild(body);"""

OLD_KT_BLOCK = r"""  // KEY TERM glossary chips — gold-bordered callouts\. Reveal staggered after body\.
  if \(slide\.key_terms && slide\.key_terms\.length\) \{
    const ktWrap = document\.createElement\('div'\);
    ktWrap\.className = 'keyterms';
    slide\.key_terms\.forEach\(kt => \{
      const chip = document\.createElement\('div'\);
      chip\.className = 'keyterm';
      chip\.innerHTML =
        `<span class="kt-label">KEY TERM</span> ` \+
        `<span class="kt-name">\$\{kt\.name\}</span> — \$\{kt\.def\}`;
      ktWrap\.appendChild\(chip\);
    \}\);
    card\.appendChild\(ktWrap\);
  \}"""

NEW_KT_BLOCK = """  // KEY TERMS - render below body as **Name:** definition
  if (slide.key_terms && slide.key_terms.length) {
    const ktWrap = document.createElement('div');
    ktWrap.className = 'keyterms';
    slide.key_terms.forEach(kt => {
      const defEl = document.createElement('div');
      defEl.className = 'keyterm';
      defEl.innerHTML = `<strong>${kt.name}:</strong> ${kt.def}`;
      ktWrap.appendChild(defEl);
    });
    card.appendChild(ktWrap);
  }"""

# Add CSS overrides so the new layout looks right
CSS_OVERRIDES = """
<style>
/* Patched key-term styling - inline definitions below body */
.keyterms { margin-top: 14px; display: flex; flex-direction: column; gap: 8px; }
.keyterm {
  background: rgba(184, 134, 11, 0.12);
  border-left: 4px solid #b8860b;
  padding: 10px 14px;
  font-size: 0.92em;
  line-height: 1.5;
  color: inherit;
  border-radius: 0 6px 6px 0;
}
.keyterm strong { color: #b8860b; letter-spacing: 0.5px; }
.body strong { color: #b8860b; font-weight: 700; }
</style>
"""

def patch(path: Path):
    text = path.read_text(encoding="utf-8")
    if MARK in text:
        print(f"  [skip] {path.name} — already patched")
        return

    new = re.sub(OLD_BODY_BLOCK, NEW_BODY_BLOCK, text)
    if new == text:
        print(f"  [WARN] {path.name} — body block not matched (file may have already been edited)")
        return

    new2 = re.sub(OLD_KT_BLOCK, NEW_KT_BLOCK, new)
    if new2 == new:
        print(f"  [WARN] {path.name} — keyterm block not matched")
        # Still write the body patch
        path.write_text(new, encoding="utf-8")
        return

    # Inject CSS overrides before </head>
    if "</head>" in new2 and "Patched key-term styling" not in new2:
        new2 = new2.replace("</head>", CSS_OVERRIDES + "</head>", 1)

    path.write_text(new2, encoding="utf-8")
    print(f"  [done] {path.name}")


def main():
    print(f"Patching key-term rendering in {DOCS}")
    for name in TARGETS:
        p = DOCS / name
        if p.exists():
            patch(p)
        else:
            print(f"  [missing] {name}")
    print("Done.")


if __name__ == "__main__":
    main()
