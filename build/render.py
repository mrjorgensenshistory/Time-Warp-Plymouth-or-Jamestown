"""
Time Warp - Plymouth or Jamestown — markdown → HTML renderer.

Reads character route markdowns from content/, produces standalone HTML files
matching the locked visual standard (full-bleed bg, 78% white text-box centered,
mid-slide buttons, Bangers font, partial transparency, growing timeline bar).

Usage: python render.py
"""
import os
import re
import json
import html
from pathlib import Path

PROJECT = Path(r"F:\Michael's\ACE\US History\Time-Warp-Plymouth-or-Jamestown")
CONTENT = PROJECT / "content"
# Output directly to project root (sibling of audio/) so relative audio paths "audio/X.mp3" work
# This matches Civil War's deployable structure.
OUTPUT = PROJECT / "dist"
OUTPUT.mkdir(parents=True, exist_ok=True)

# Per-character config — accent color, audio file, display name
CHARACTERS = {
    "roanoke_tutorial": {
        "title": "Roanoke Tutorial",
        "color": "#5b6770",
        "audio": "audio/tutorial/tutorial_main.mp3",
        "html": "tutorial.html",
        "side": "tutorial",
        "hub_href": "analyzer.html",  # tutorial hand-off goes to the side-quiz
        "default_bg": "images/tutorial/01_white_arrives.jpg",
        # Per-slide image overrides for the tutorial (matching the demo's image set)
        "slide_images": {
            "slide_1": "images/tutorial/01_white_arrives.jpg",
            "slide_2": "images/tutorial/02_raleigh_charter.jpg",
            "slide_3": "images/tutorial/10_dawn_ships.jpg",  # ship sailing east (Mayflower-at-sea reused as period ship)
            "slide_4": "images/tutorial/04_spanish_armada.jpg",
            "slide_5": "images/tutorial/04_spanish_armada.jpg",  # three years lost in war (reuse Armada)
            "slide_6": "images/tutorial/01_white_arrives.jpg",  # empty settlement (reuse colonist scene)
            "slide_7": "images/tutorial/08_outer_banks_map.jpg",  # where to look — map gives geography
            "slide_8": "images/tutorial/07_croatoan_carving.jpg",
            "slide_9": "images/tutorial/08_outer_banks_map.jpg",  # what it might mean — Croatoan map
            "slide_10": "images/tutorial/04_spanish_armada.jpg",  # storm reused (chaotic ships)
            "slide_11": "images/tutorial/10_dawn_ships.jpg",
        },
    },
    "smith_route": {
        "title": "John Smith — Jamestown",
        "color": "#8b3a1a",
        "audio": "audio/smith/smith_main.mp3",
        "html": "smith.html",
        "side": "jamestown",
        "hub_href": "index.html?back=1",
        "default_bg": "images/hub/jamestown_smith.jpg",
    },
    "rolfe_route": {
        "title": "John Rolfe — Jamestown",
        "color": "#7a5a2e",
        "audio": "audio/rolfe/rolfe_main.mp3",
        "html": "rolfe.html",
        "side": "jamestown",
        "hub_href": "index.html?back=1",
        "default_bg": "images/hub/jamestown_rolfe.jpg",
        # Per-slide period art for Rolfe (45 slides covered)
        "slide_images": {
            "slide_1": "images/rolfe/ship_at_sea.jpg",
            "slide_2": "images/rolfe/storm_at_sea.jpg",
            "slide_3": "images/rolfe/storm_at_sea.jpg",
            "slide_4": "images/rolfe/ship_at_sea.jpg",
            "slide_7": "images/rolfe/jamestown_setting.jpg",
            "slide_8": "images/rolfe/jamestown_setting.jpg",
            "slide_9": "images/rolfe/jamestown_setting.jpg",
            "slide_11": "images/rolfe/ship_at_sea.jpg",
            "slide_13": "images/rolfe/jamestown_setting.jpg",
            "slide_14": "images/rolfe/tobacco_rolfe_1874.jpg",
            "slide_15": "images/rolfe/tobacco_rolfe_1874.jpg",
            "slide_18": "images/rolfe/tobacco_rolfe_1874.jpg",
            "slide_19": "images/rolfe/jamestown_setting.jpg",
            "slide_20": "images/rolfe/pocahontas_van_de_passe.jpg",
            "slide_21": "images/rolfe/pocahontas_baptism.jpg",
            "slide_23": "images/rolfe/pocahontas_baptism.jpg",
            "slide_25": "images/rolfe/pocahontas_baptism.jpg",
            "slide_26": "images/rolfe/portrait_marriage.jpg",
            "slide_29": "images/rolfe/ship_at_sea.jpg",
            "slide_30": "images/rolfe/pocahontas_van_de_passe.jpg",
            "slide_31": "images/rolfe/pocahontas_van_de_passe.jpg",
            "slide_33": "images/rolfe/ship_at_sea.jpg",
            "slide_34": "images/rolfe/tobacco_rolfe_1874.jpg",
            "slide_35": "images/rolfe/jamestown_setting.jpg",
            "slide_36": "images/rolfe/tobacco_rolfe_1874.jpg",
            "slide_37": "images/rolfe/jamestown_setting.jpg",
            "slide_39": "images/rolfe/jamestown_setting.jpg",
            "slide_40": "images/rolfe/tobacco_rolfe_1874.jpg",
            "slide_41": "images/rolfe/jamestown_setting.jpg",
            "slide_42": "images/rolfe/storm_at_sea.jpg",
            "slide_45": "images/rolfe/portrait_marriage.jpg",
        },
    },
    "powhatan_route": {
        "title": "Powhatan — Jamestown",
        "color": "#3a5a3a",
        "audio": "audio/powhatan/powhatan_main.mp3",
        "html": "powhatan.html",
        "side": "jamestown",
        "hub_href": "index.html?back=1",
        "default_bg": "images/hub/jamestown_powhatan.jpg",
    },
    "bradford_route": {
        "title": "William Bradford — Plymouth",
        "color": "#2a3e5a",
        "audio": "audio/bradford/bradford_main.mp3",
        "html": "bradford.html",
        "side": "plymouth",
        "hub_href": "index.html?back=1",
        "default_bg": "images/hub/plymouth_bradford.jpg",
    },
    "squanto_route": {
        "title": "Squanto — Plymouth",
        "color": "#5a4a2e",
        "audio": "audio/squanto/squanto_main.mp3",
        "html": "squanto.html",
        "side": "plymouth",
        "hub_href": "index.html?back=1",
        "default_bg": "images/hub/plymouth_squanto.png",
    },
    "massasoit_route": {
        "title": "Massasoit — Plymouth",
        "color": "#3e3a2e",
        "audio": "audio/massasoit/massasoit_main.mp3",
        "html": "massasoit.html",
        "side": "plymouth",
        "hub_href": "index.html?back=1",
        "default_bg": "images/hub/plymouth_massasoit.jpg",
    },
}

# Pre-1587 historical events (always visible on the timeline bar)
HISTORY_TICKS = [
    {"year": "1492", "label": "1492 — Columbus", "left": 4},
    {"year": "1513", "label": "1513 — Florida found", "left": 11},
    {"year": "1521", "label": "1521 — Aztecs fall", "left": 18},
    {"year": "1533", "label": "1533 — Incas fall", "left": 25},
    {"year": "1565", "label": "1565 — St. Augustine", "left": 32},
]


def slug_button_target(target_text, slide_id_for_self=None):
    """Convert a button-target prose description to a slide ID.

    Examples:
      'advances to Slide 5' → 'slide_5'
      'returns to Slide 12 (DECISION 2)' → 'slide_12'
      'advances to Slide GAMEOVER A' → 'slide_gameover_a'
      'returns to HOME' / 'returns HOME' / 'HOME' → 'HOME'
    """
    t = target_text.strip().lower()
    if "home" in t or "title screen" in t or "another route" in t or "another character" in t:
        return "HOME"
    # GAMEOVER X
    m = re.search(r"slide\s+gameover\s+([a-z])", t)
    if m:
        return f"slide_gameover_{m.group(1)}"
    # numbered slide
    m = re.search(r"slide[_\s]+(\d+)", t)
    if m:
        return f"slide_{m.group(1)}"
    # epilogue / closing card / final slide → keep as next slide if we can't tell
    if "epilogue" in t or "closing card" in t or "final" in t:
        return "_NEXT_"  # resolved post-pass
    return "_NEXT_"


def parse_slide_block(block_text, slide_index_in_file):
    """Parse a single slide markdown block into a slide dict."""
    # Extract header — `## Slide N — Title` OR `## Slide GAMEOVER X — Title`
    header_match = re.match(r"##\s+Slide\s+(GAMEOVER\s+[A-Za-z]|[\dA-Za-z]+)\s*[—–-]?\s*(.*)", block_text)
    if not header_match:
        return None
    raw_id = header_match.group(1).strip()
    title = header_match.group(2).strip()

    if raw_id.upper().startswith("GAMEOVER"):
        letter = raw_id.split()[-1].lower()
        slide_id = f"slide_gameover_{letter}"
        slide_type = "gameover"
        # Override gameover title to consistent series stinger
        title = "WRONG LEVERRRR!"
    else:
        slide_id = f"slide_{raw_id}"
        slide_type = "story"
        if "DECISION" in title.upper():
            slide_type = "decision"
        # Strip writer's organizational prefixes from displayed title
        title = re.sub(r"^DECISION\s+\d+:\s*", "", title, flags=re.IGNORECASE)
        # Hide stage-direction titles ("Title / Cold Open", "Cold Open", etc.)
        if re.match(r"^(title\s*/?\s*cold\s+open|cold\s+open|title)$", title, re.IGNORECASE):
            title = ""

    # Body text — paragraphs starting with `> `
    body_section = re.search(r"\*\*Body text:\*\*\s*\n((?:>\s.*\n?)+)", block_text)
    body_paragraphs = []
    if body_section:
        for line in body_section.group(1).split("\n"):
            line = line.strip()
            if line.startswith(">"):
                body_paragraphs.append(line.lstrip("> ").strip())

    # Image brief — used as image alt / aria description, not displayed
    image_match = re.search(r"\*\*Image brief:\*\*\s*(.+?)(?:\n\*\*|\Z)", block_text, re.DOTALL)
    image_brief = image_match.group(1).strip() if image_match else ""

    # Timeline bar — extract years mentioned and detect pulsing/active states
    timeline_match = re.search(r"\*\*Timeline bar:\*\*\s*(.+?)(?:\n\*\*|\Z)", block_text, re.DOTALL)
    timeline_text = timeline_match.group(1).strip() if timeline_match else ""

    # Heuristic timeline state extraction
    active_years = []
    pulsing_years = []
    # Years mentioned in text (after 1587 — character-route events)
    for m in re.finditer(r"(\d{4})", timeline_text):
        year = m.group(1)
        if int(year) < 1492 or int(year) > 1700:
            continue
        # Check if this year is described as pulsing/illuminating-now
        # by looking for keywords near the year
        context = timeline_text[max(0, m.start()-40):m.end()+60]
        if re.search(rf"{year}.*?(?:pulse|illuminat|enters|appears|new tick|reveal)", context, re.IGNORECASE):
            pulsing_years.append(year)
        else:
            active_years.append(year)

    # Buttons — `- \`[TEXT]\` — target prose`
    buttons = []
    button_section = re.search(r"\*\*Buttons:\*\*\s*\n((?:[-*]\s+`?\[.*\n?)+)", block_text)
    if button_section:
        for line in button_section.group(1).split("\n"):
            line = line.strip()
            if not line.startswith("-") and not line.startswith("*"):
                continue
            # Find the button text inside [ ... ]
            txt_match = re.search(r"\[(.+?)\]", line)
            if not txt_match:
                continue
            btn_text = txt_match.group(1).strip()
            # Find target prose (after the closing bracket / em-dash)
            after = line[txt_match.end():]
            target = slug_button_target(after, slide_id)
            buttons.append({"text": btn_text, "target": target})

    # Default fallback: if no buttons parsed, add a single CONTINUE
    if not buttons:
        buttons = [{"text": "→ Continue", "target": "_NEXT_"}]

    # Gameover slides should have a fullscreen GIF
    gif = None
    if slide_type == "gameover":
        gif = "https://media.tenor.com/mcS-PaTlDawAAAAM/pull-the-lever-wrong-lever.gif"

    return {
        "id": slide_id,
        "type": slide_type,
        "title": title,
        "body": body_paragraphs,
        "buttons": buttons,
        "image_brief": image_brief,
        "timeline": {"active": active_years, "pulsing": pulsing_years},
        "gif": gif,
    }


def parse_markdown(md_path):
    """Parse a route markdown into an ordered list of slide dicts."""
    text = md_path.read_text(encoding="utf-8")
    # Split on `## Slide` boundaries
    blocks = re.split(r"\n(?=##\s+Slide)", text)
    slides = []
    for i, block in enumerate(blocks):
        if not block.strip().startswith("## Slide"):
            continue
        slide = parse_slide_block(block, i)
        if slide:
            slides.append(slide)
    return slides


def resolve_next_targets(slides):
    """Resolve any '_NEXT_' button targets to the next non-gameover slide_id."""
    # Build ordered list of story-type IDs only (gameovers are jump targets, not in the chain)
    story_ids = [s["id"] for s in slides if s["type"] != "gameover"]
    for i, s in enumerate(slides):
        for btn in s["buttons"]:
            if btn["target"] == "_NEXT_":
                if s["type"] != "gameover" and s["id"] in story_ids:
                    idx = story_ids.index(s["id"])
                    if idx + 1 < len(story_ids):
                        btn["target"] = story_ids[idx + 1]
                    else:
                        btn["target"] = "HOME"
                else:
                    btn["target"] = "HOME"
    # Also: if any button target is a slide ID that doesn't exist in this file, point to HOME
    all_ids = {s["id"] for s in slides}
    for s in slides:
        for btn in s["buttons"]:
            if btn["target"] not in all_ids and btn["target"] != "HOME":
                btn["target"] = "HOME"
    return slides


# === HTML TEMPLATE ===
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__ — Time Warp: Plymouth or Jamestown</title>
<link href="https://fonts.googleapis.com/css2?family=Bangers&family=IM+Fell+English&family=IM+Fell+English+SC&family=Share+Tech&display=swap" rel="stylesheet">
<style>
:root {
  --accent: __ACCENT__;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { height: 100%; width: 100%; overflow: hidden; background: #0a0a1a; color: #fff; font-family: 'Bangers', sans-serif; }
.stage { position: absolute; inset: 0; overflow: hidden; }

.slide {
  position: absolute; inset: 0;
  opacity: 0;
  transition: opacity 700ms ease;
  pointer-events: none;
  background-size: cover;
  background-position: center;
  background-color: #1a1a28;
}
.slide.active { opacity: 1; pointer-events: auto; }
.slide.has-image::after {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(0,0,0,0.35) 0%, rgba(0,0,0,0.15) 40%, rgba(0,0,0,0.55) 100%);
  z-index: 1; pointer-events: none;
}

/* Default no-image gradient using accent color */
.slide:not(.has-image) {
  background: radial-gradient(ellipse at 50% 30%, var(--accent) 0%, #0a0a1a 70%);
}

.card {
  position: absolute;
  top: 3vh; left: 50%;
  transform: translateX(-50%);
  z-index: 5;
  max-width: 60%;
  background: rgba(255,255,255,0.78);
  border: 2px solid #000;
  border-radius: 8px;
  padding: 2.2vh 2.6vw;
  box-shadow: 0 6px 24px rgba(0,0,0,0.5);
  font-family: 'Bangers', 'Arial Black', sans-serif;
  color: #000;
  line-height: 1.5;
  letter-spacing: 0.5px;
  text-align: center;
}
.card h2 {
  font-size: clamp(1.5rem, 3vw, 2.2rem);
  margin-bottom: 1.5vh;
  color: #000;
  letter-spacing: 1.2px;
}
.card .body p {
  font-size: clamp(1.1rem, 2vw, 1.6rem);
  margin-bottom: 1vh;
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 600ms ease, transform 600ms ease;
}
.card .body p.shown { opacity: 1; transform: translateY(0); }

.buttons {
  position: absolute;
  top: 60%; left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  gap: 2vh;
  z-index: 11;
  align-items: center;
  max-width: 80%;
  opacity: 0;
  transition: opacity 600ms ease;
}
.buttons.shown { opacity: 1; }

button.choice {
  background: rgba(255,255,255,0.85);
  color: #000;
  border: 3px solid #000;
  border-radius: 6px;
  padding: 1.8vh 4vw;
  font-family: 'Bangers', sans-serif;
  font-size: clamp(1.1rem, 2vw, 1.6rem);
  cursor: pointer;
  transition: all 150ms ease;
  min-width: 32vw;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.4);
}
button.choice:hover { background: #fff; transform: scale(1.03); }

/* === GAMEOVER STYLING — dramatic, immersive, period-respectful === */
.slide.gameover-slide {
  background-image: none !important;
  background:
    radial-gradient(ellipse at 50% 40%, rgba(180,30,30,0.28) 0%, transparent 60%),
    linear-gradient(180deg, #2a0808 0%, #0a0204 100%) !important;
  animation: screenShake 0.6s ease;
}
.slide.gameover-slide::after { background: rgba(0,0,0,0.45) !important; }
@keyframes screenShake {
  0%,100% { transform: translate(0,0); }
  10%,30%,50%,70%,90% { transform: translate(-6px,2px); }
  20%,40%,60%,80% { transform: translate(6px,-2px); }
}
/* Big bold "GAMEOVER" banner above the card */
.slide.gameover-slide::before {
  content: 'GAME OVER';
  position: absolute;
  top: 4vh; left: 50%;
  transform: translateX(-50%);
  font-family: 'Bangers', sans-serif;
  font-size: clamp(2.4rem, 6.5vw, 5rem);
  letter-spacing: 8px;
  color: #ff2222;
  text-shadow: 4px 4px 0 #000, 6px 6px 18px rgba(180,30,30,0.7), 0 0 30px rgba(255,40,40,0.5);
  z-index: 6;
  animation: pulse-red 1.6s ease-in-out infinite;
  pointer-events: none;
}
@keyframes pulse-red {
  0%,100% { text-shadow: 4px 4px 0 #000, 6px 6px 18px rgba(180,30,30,0.7), 0 0 30px rgba(255,40,40,0.5); }
  50% { text-shadow: 4px 4px 0 #000, 6px 6px 18px rgba(180,30,30,0.9), 0 0 60px rgba(255,80,80,0.9); }
}
.slide.gameover-slide .card {
  top: 18vh;
  background: rgba(20,5,5,0.85);
  border-color: #6a0000;
  border-width: 3px;
  color: #fff8e0;
  max-width: 56%;
}
.slide.gameover-slide .card h2 {
  color: #ff5555;
  font-size: clamp(1.6rem, 3.5vw, 2.6rem);
  letter-spacing: 3px;
  animation: shake 0.5s ease;
  text-shadow: 2px 2px 0 #6a0000;
}
.slide.gameover-slide .card .body p {
  color: #fff8e0;
  font-size: clamp(1rem, 1.7vw, 1.4rem);
}
@keyframes shake {
  0%,100%{transform:translateX(0);}
  20%{transform:translateX(-12px);}
  40%{transform:translateX(12px);}
  60%{transform:translateX(-6px);}
  80%{transform:translateX(6px);}
}
.slide.gameover-slide button.choice {
  background: rgba(204,0,0,0.85);
  color: #fff;
  border-color: #6a0000;
  border-width: 3px;
  text-shadow: 1px 1px 0 #000;
}
.slide.gameover-slide button.choice:hover {
  background: rgba(255,51,51,0.95);
  border-color: #ff8888;
}
.fullscreen-gif {
  position: absolute;
  top: 60%; left: 50%;
  transform: translate(-50%, -50%);
  z-index: 3;
  max-width: 70vw; max-height: 55vh;
  border: 4px solid #6a0000;
  border-radius: 8px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.9), 0 0 40px rgba(255,40,40,0.3);
}

/* Timeline bar */
.timeline {
  position: fixed;
  bottom: 0; left: 0; right: 0;
  height: 64px;
  background: linear-gradient(180deg, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0.8) 100%);
  border-top: 2px solid var(--accent);
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 30px;
}
.timeline-track {
  position: relative;
  width: min(1100px, 90%);
  height: 2px;
  background: #6a5a44;
}
.tick {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  visibility: hidden;
  opacity: 0;
  pointer-events: none;
}
.tick.revealed { visibility: visible; opacity: 1; }
.tick .dot {
  width: 14px; height: 14px;
  border-radius: 50%;
  background: #4a3a28;
  border: 2px solid #6a5a44;
  margin: 0 auto;
}
.tick .label {
  font-family: 'IM Fell English SC', serif;
  font-size: 11px;
  margin-top: 6px;
  white-space: nowrap;
  color: #f4d166;
  opacity: 0.85;
}
.tick.history .dot {
  background: #8a7a64;
  border-color: #8a7a64;
  width: 10px; height: 10px;
}
.tick.history .label { color: #8a7a64; opacity: 0.7; font-size: 10px; }
.tick.active .dot {
  background: #d4af37;
  border-color: #f4d166;
  box-shadow: 0 0 12px rgba(212,175,55,0.7);
}
.tick.pulsing .dot { animation: pulse 1.4s ease-in-out infinite; }
@keyframes pulse {
  0%,100%{box-shadow:0 0 8px rgba(212,175,55,0.5);}
  50%{box-shadow:0 0 22px rgba(212,175,55,1.0);}
}

.header-tag {
  position: fixed; top: 12px; left: 16px;
  font-family: 'Bangers', sans-serif;
  font-size: 14px;
  color: rgba(255,255,255,0.5);
  letter-spacing: 2px;
  z-index: 11;
}
.counter {
  position: fixed; top: 12px; right: 16px;
  font-family: 'Share Tech', monospace;
  font-size: 12px;
  color: rgba(255,255,255,0.4);
  z-index: 11;
}
.credits {
  position: fixed; bottom: 70px; left: 10px;
  font-size: 0.6rem; color: #888;
  z-index: 11;
}
</style>
</head>
<body>

<div class="header-tag">__HEADER_TAG__</div>
<div class="counter" id="counter"></div>
<div class="credits">Music: __MUSIC_CREDIT__ · Mr. Jorgensen 2026</div>

<audio id="bg-music" loop preload="auto"><source src="__AUDIO_SRC__" type="audio/mpeg"></audio>

<div class="stage" id="stage"></div>

<div class="timeline">
  <div class="timeline-track" id="timeline-track">
    __HISTORY_TICKS__
    __PLAYER_TICKS__
  </div>
</div>

<script>
const SLIDES = __SLIDES_JSON__;
const HUB_HREF = "__HUB_HREF__";
const DEFAULT_BG = "__DEFAULT_BG__";

const stage = document.getElementById('stage');
const counter = document.getElementById('counter');

function renderSlide(slide) {
  const div = document.createElement('div');
  let cls = 'slide';
  if (slide.type === 'gameover') cls += ' gameover-slide';
  div.className = cls;
  div.id = slide.id;

  // Image priority: per-slide explicit image > DEFAULT_BG (character portrait) > gradient
  // Gameovers skip bg image entirely (they have their own dark bg + GIF center)
  if (slide.type !== 'gameover') {
    const bgImg = slide.image || DEFAULT_BG;
    if (bgImg) {
      div.classList.add('has-image');
      div.style.backgroundImage = `url('${bgImg}')`;
    }
  }

  if (slide.gif) {
    const gifImg = document.createElement('img');
    gifImg.className = 'fullscreen-gif';
    gifImg.src = slide.gif;
    gifImg.alt = 'gameover';
    div.appendChild(gifImg);
  }

  const card = document.createElement('div');
  card.className = 'card';
  if (slide.title && slide.title.trim()) {
    const h2 = document.createElement('h2');
    h2.textContent = slide.title;
    card.appendChild(h2);
  }
  const body = document.createElement('div');
  body.className = 'body';
  slide.body.forEach(p => {
    const para = document.createElement('p');
    para.innerHTML = p;
    body.appendChild(para);
  });
  card.appendChild(body);
  div.appendChild(card);

  const btnWrap = document.createElement('div');
  btnWrap.className = 'buttons';
  slide.buttons.forEach(b => {
    const btn = document.createElement('button');
    btn.className = 'choice';
    btn.textContent = b.text;
    btn.addEventListener('click', () => goToSlide(b.target));
    btnWrap.appendChild(btn);
  });
  div.appendChild(btnWrap);

  stage.appendChild(div);
  return div;
}

function updateTimeline(state) {
  document.querySelectorAll('.tick').forEach(tick => {
    const year = tick.dataset.year;
    const isHistory = tick.classList.contains('history');
    tick.classList.remove('active', 'pulsing');
    if (!isHistory) tick.classList.remove('revealed');
    if (state.active && state.active.includes(year)) {
      tick.classList.add('active', 'revealed');
    }
    if (state.pulsing && state.pulsing.includes(year)) {
      tick.classList.add('active', 'pulsing', 'revealed');
    }
  });
}

function revealCard(slideEl) {
  const paras = slideEl.querySelectorAll('.card .body p');
  const buttons = slideEl.querySelector(':scope > .buttons');
  paras.forEach((p, i) => setTimeout(() => p.classList.add('shown'), 250 + i * 600));
  if (buttons) setTimeout(() => buttons.classList.add('shown'), 250 + paras.length * 600 + 200);
}

function showSlide(idx) {
  document.querySelectorAll('.slide').forEach(s => s.classList.remove('active'));
  const slide = SLIDES[idx];
  if (!slide) return;
  let el = document.getElementById(slide.id);
  if (!el) el = renderSlide(slide);
  el.querySelectorAll('.card .body p').forEach(p => p.classList.remove('shown'));
  const bw = el.querySelector(':scope > .buttons');
  if (bw) bw.classList.remove('shown');
  el.classList.add('active');
  updateTimeline(slide.timeline || {});
  counter.textContent = `${idx + 1} / ${SLIDES.length}`;
  setTimeout(() => revealCard(el), 200);
}

function goToSlide(target) {
  if (target === 'HOME') { window.location.href = HUB_HREF; return; }
  const idx = SLIDES.findIndex(s => s.id === target);
  if (idx === -1) return;
  showSlide(idx);
}

// Audio unlock + fade-in
const bgMusic = document.getElementById('bg-music');
let audioStarted = false;
function startMusic() {
  if (audioStarted || !bgMusic) return;
  audioStarted = true;
  bgMusic.volume = 0;
  bgMusic.play().then(() => {
    let v = 0;
    const fade = setInterval(() => {
      v += 0.03;
      if (v >= 0.45) { bgMusic.volume = 0.45; clearInterval(fade); }
      else bgMusic.volume = v;
    }, 100);
  }).catch(() => {});
}
document.addEventListener('click', startMusic, { once: true });
document.addEventListener('keydown', startMusic, { once: true });

showSlide(0);
</script>
</body>
</html>
"""


def render_route(md_name, config):
    md_path = CONTENT / f"{md_name}.md"
    if not md_path.exists():
        print(f"  [SKIP] {md_name}: no markdown")
        return None

    slides = parse_markdown(md_path)
    slides = resolve_next_targets(slides)
    if not slides:
        print(f"  [WARN] {md_name}: no slides parsed")
        return None

    # Apply per-slide image overrides from config
    slide_images = config.get("slide_images", {})
    for s in slides:
        if s["id"] in slide_images:
            s["image"] = slide_images[s["id"]]

    # History ticks (always visible)
    history_html = ""
    for h in HISTORY_TICKS:
        history_html += (
            f'<div class="tick history revealed" data-year="{h["year"]}" '
            f'style="left: {h["left"]}%;">'
            f'<div class="dot"></div><div class="label">{h["label"]}</div></div>\n    '
        )

    # Player ticks — collect all years used in any slide's timeline
    all_years = set()
    for s in slides:
        for y in s["timeline"].get("active", []) + s["timeline"].get("pulsing", []):
            try:
                yi = int(y)
                if 1587 <= yi <= 1700:
                    all_years.add(y)
            except ValueError:
                pass

    sorted_years = sorted(all_years, key=int)
    if sorted_years:
        # Spread player years from 40% to 95%
        span_lo, span_hi = 40, 95
        if len(sorted_years) > 1:
            year_min = int(sorted_years[0])
            year_max = int(sorted_years[-1])
            year_range = max(1, year_max - year_min)
        else:
            year_min, year_max, year_range = int(sorted_years[0]), int(sorted_years[0]), 1

        player_html = ""
        for y in sorted_years:
            yi = int(y)
            if year_range > 0 and len(sorted_years) > 1:
                pct = span_lo + (yi - year_min) * (span_hi - span_lo) / year_range
            else:
                pct = (span_lo + span_hi) / 2
            player_html += (
                f'<div class="tick" data-year="{y}" style="left: {pct:.1f}%;">'
                f'<div class="dot"></div><div class="label">{y}</div></div>\n    '
            )
    else:
        player_html = ""

    # dist/ sits next to audio/, so plain relative path
    audio_src = config['audio']

    music_credit = "Kevin MacLeod / incompetech.com (CC-BY 4.0)"

    html_out = HTML_TEMPLATE
    html_out = html_out.replace("__TITLE__", config["title"])
    html_out = html_out.replace("__ACCENT__", config["color"])
    html_out = html_out.replace("__HEADER_TAG__", config["title"].upper())
    html_out = html_out.replace("__MUSIC_CREDIT__", music_credit)
    html_out = html_out.replace("__AUDIO_SRC__", audio_src)
    html_out = html_out.replace("__HISTORY_TICKS__", history_html.strip())
    html_out = html_out.replace("__PLAYER_TICKS__", player_html.strip())
    html_out = html_out.replace("__SLIDES_JSON__", json.dumps(slides, ensure_ascii=False))
    html_out = html_out.replace("__HUB_HREF__", config["hub_href"])
    html_out = html_out.replace("__DEFAULT_BG__", config.get("default_bg") or "")

    out_path = OUTPUT / config["html"]
    out_path.write_text(html_out, encoding="utf-8")
    print(f"  [OK] {md_name} -> {out_path.name} ({len(slides)} slides)")
    return slides


def main():
    print(f"Rendering Time Warp: Plymouth or Jamestown to {OUTPUT}")
    rendered = {}
    for md_name, config in CHARACTERS.items():
        result = render_route(md_name, config)
        if result:
            rendered[md_name] = {"slides": len(result), "config": config}
    print(f"\nRendered {len(rendered)} routes total.")
    print("\nSlide counts:")
    for name, info in rendered.items():
        print(f"  {name}: {info['slides']}")


if __name__ == "__main__":
    main()
