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
        "default_bg": "images/smith/portrait_smith.jpg",
        # Per-slide period art covering all 27 narrative slides
        "slide_images": {
            "slide_1": "images/smith/portrait_smith.jpg",
            "slide_2": "images/smith/ships_at_sea.jpg",
            "slide_3": "images/smith/jamestown_zuniga_1608.jpg",
            "slide_4": "images/smith/jamestown_zuniga_1608.jpg",
            "slide_5": "images/smith/first_contact.jpg",        # Decision 1: First Contact
            "slide_6": "images/smith/smith_armed.jpg",          # Captured (Smith taken)
            "slide_7": "images/smith/pocahontas_saves_smith.jpg", # The Rescue
            "slide_8": "images/smith/jamestown_zuniga_1608.jpg",
            "slide_9": "images/smith/portrait_smith.jpg",
            "slide_10": "images/smith/portrait_smith.jpg",
            "slide_11": "images/smith/first_contact.jpg",        # Opening trade
            "slide_12": "images/smith/smith_armed.jpg",          # How Do I Get Corn (taking)
            "slide_13": "images/smith/smith_armed.jpg",          # When Do We Strike
            "slide_14": "images/smith/pocahontas_saves_smith.jpg",
            "slide_15": "images/smith/first_contact.jpg",        # Trust Powhatan — diplomacy scene
            "slide_16": "images/smith/powhatan_village.jpg",     # Warning in the Dark
            "slide_17": "images/smith/ships_at_sea.jpg",
            "slide_18": "images/smith/storm_chaos.jpg",          # Powder Bag
            "slide_19": "images/smith/storm_chaos.jpg",          # The Burn
            "slide_20": "images/smith/ships_at_sea.jpg",
            "slide_21": "images/smith/ships_at_sea.jpg",
            "slide_22": "images/smith/starving_time_burial.jpg",
            "slide_23": "images/smith/starving_time_burial.jpg",
            "slide_24": "images/smith/pocahontas_saves_smith.jpg",
            "slide_25": "images/smith/portrait_smith.jpg",
            "slide_26": "images/smith/portrait_smith.jpg",
            "slide_27": "images/smith/portrait_smith.jpg",
        },
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
            "slide_2": "images/rolfe/ship_at_sea.jpg",
            "slide_3": "images/rolfe/ship_at_sea.jpg",
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
        "slide_images": {
            # Cold open + setup
            "slide_1": "images/powhatan/chief_herowan_white.jpg",
            "slide_2": "images/powhatan/powhatan_smith_map.jpg",
            "slide_3": "images/powhatan/coronation_powhatan.jpg",
            "slide_4": "images/powhatan/village_secoton.jpg",
            "slide_5": "images/powhatan/jamestown_ships.jpg",
            # First contact
            "slide_6": "images/powhatan/english_ships_fleet.jpg",
            "slide_6_fail": "images/powhatan/smith_taking_pamunkey.jpg",
            "slide_7_delegation": "images/powhatan/praying_around_fire.jpg",
            "slide_7": "images/powhatan/algonquin_village_debry.jpg",
            "slide_8": "images/powhatan/indians_dancing_white.jpg",
            "slide_8_fail": "images/powhatan/smith_taking_pamunkey.jpg",
            "slide_9": "images/powhatan/village_secoton.jpg",
            # Trade
            "slide_10": "images/powhatan/cooking_fish_white.jpg",
            "slide_11": "images/powhatan/indians_fishing_white.jpg",
            "slide_11_fail": "images/powhatan/chief_herowan_white.jpg",
            # Smith captured
            "slide_12": "images/powhatan/smith_captured_vaughan.jpg",
            "slide_13": "images/powhatan/smith_before_powhatan.jpg",
            "slide_13_fail_a": "images/powhatan/algonquin_village_debry.jpg",
            "slide_13_fail_b": "images/powhatan/how_they_build_boats.jpg",
            "slide_14": "images/powhatan/pocahontas_saves_smith.jpg",
            # War + escalation
            "slide_15": "images/powhatan/smith_taking_pamunkey.jpg",
            "slide_16": "images/powhatan/herowans_wife_white.jpg",
            "slide_17": "images/powhatan/indians_dancing_white.jpg",
            "slide_17_fail_a": "images/powhatan/algonquin_village_debry.jpg",
            "slide_17_fail_b": "images/powhatan/village_secoton.jpg",
            "slide_18": "images/powhatan/cooking_fish_white.jpg",
            "slide_19": "images/powhatan/jamestown_ships.jpg",
            "slide_20": "images/powhatan/english_ships_fleet.jpg",
            "slide_21": "images/powhatan/massacre_1622_merian.jpg",
            "slide_21_fail": "images/powhatan/herowans_wife_white.jpg",
            "slide_22": "images/powhatan/indians_fishing_white.jpg",
            "slide_23": "images/powhatan/massacre_1622_merian.jpg",
            # Pocahontas captured + marriage
            "slide_24": "images/powhatan/abduction_pocahontas.jpg",
            "slide_25": "images/powhatan/praying_around_fire.jpg",
            "slide_25_fail": "images/powhatan/herowans_wife_white.jpg",
            "slide_26": "images/powhatan/abduction_pocahontas.jpg",
            "slide_27": "images/powhatan/pocahontas_van_de_passe.jpg",
            "slide_28": "images/powhatan/marriage_pocahontas.jpg",
            "slide_28_fail": "images/powhatan/village_secoton.jpg",
            "slide_29": "images/powhatan/marriage_pocahontas.jpg",
            "slide_29_hard": "images/powhatan/marriage_pocahontas.jpg",
            # England + death + succession
            "slide_30": "images/powhatan/pocahontas_van_de_passe.jpg",
            "slide_31": "images/rolfe/pocahontas_baptism.jpg",
            "slide_32": "images/powhatan/chief_herowan_white.jpg",
            "slide_32_fail": "images/powhatan/massacre_1622_merian.jpg",
            "slide_33": "images/powhatan/coronation_powhatan.jpg",
            "slide_34": "images/powhatan/chief_herowan_white.jpg",
            "slide_35_peace": "images/powhatan/massacre_1622_merian.jpg",
            "slide_35_strike": "images/powhatan/massacre_1622_merian.jpg",
            "slide_35_open": "images/powhatan/massacre_1622_merian.jpg",
            "slide_36": "images/powhatan/powhatan_smith_map.jpg",
        },
    },
    "bradford_route": {
        "title": "William Bradford — Plymouth",
        "color": "#2a3e5a",
        "audio": "audio/bradford/bradford_main.mp3",
        "html": "bradford.html",
        "side": "plymouth",
        "hub_href": "index.html?back=1",
        "default_bg": "images/hub/plymouth_bradford.jpg",
        "slide_images": {
            # Yorkshire / England (1606-08)
            "slide_1": "images/hub/plymouth_bradford.jpg",
            "slide_2": "images/bradford/bradford_portrait.jpg",
            "slide_3": "images/bradford/embarkation_pilgrims_weir.jpg",
            # Holland (1608-19)
            "slide_4": "images/hub/plymouth_pilgrims.jpg",
            "slide_5": "images/hub/plymouth_pilgrims.jpg",
            "slide_6": "images/bradford/king_james_i_decritz.jpg",
            "slide_7": "images/bradford/king_james_i_decritz.jpg",
            # Departure (1620)
            "slide_8": "images/bradford/delfshaven_willaerts.jpg",
            "slide_9": "images/bradford/embarkation_pilgrims_weir.jpg",
            "slide_10": "images/bradford/mayflower_at_sea.jpg",
            "slide_11": "images/bradford/mayflower_at_sea.jpg",
            "slide_12": "images/bradford/mayflower_in_plymouth_harbor_halsall.jpg",
            # Compact + landing
            "slide_13": "images/plymouth_shared/landing_pilgrims_bacon.jpg",
            "slide_14": "images/plymouth_shared/mayflower_compact_period.jpg",
            "slide_15": "images/plymouth_shared/mayflower_compact_period.jpg",
            "slide_16": "images/bradford/compact_signing_ferris.jpg",
            # First winter
            "slide_17": "images/plymouth_shared/landing_pilgrims_bacon.jpg",
            "slide_18": "images/bradford/bradford_portrait.jpg",
            "slide_19": "images/bradford/bradford_portrait.jpg",
            # Samoset / Squanto / Massasoit
            "slide_20": "images/plymouth_shared/samoset_interview.jpg",
            "slide_21": "images/plymouth_shared/samoset_interview.jpg",
            "slide_22": "images/bradford/squanto_teaching_corn.jpg",
            "slide_23": "images/bradford/squanto_teaching_corn.jpg",
            "slide_24": "images/bradford/squanto_teaching_corn.jpg",
            "slide_25": "images/bradford/massasoit_carver_meeting.jpg",
            # First Thanksgiving
            "slide_26": "images/plymouth_shared/thanksgiving_brownscombe.jpg",
            "slide_27": "images/plymouth_shared/thanksgiving_brownscombe.jpg",
            "slide_28": "images/bradford/squanto_teaching_corn.jpg",
            "slide_29": "images/hub/plymouth_squanto.png",
            # Governance + chronicle (1622-57)
            "slide_30": "images/bradford/bradford_portrait.jpg",
            "slide_31": "images/bradford/of_plymouth_plantation_manuscript.jpg",
            "slide_32": "images/bradford/king_james_i_decritz.jpg",
            "slide_33": "images/bradford/of_plymouth_plantation_manuscript.jpg",
            "slide_34": "images/bradford/bradford_portrait.jpg",
            "slide_35": "images/bradford/of_plymouth_plantation_manuscript.jpg",
            "slide_36": "images/bradford/of_plymouth_plantation_manuscript.jpg",
            "slide_38": "images/bradford/embarkation_pilgrims_weir.jpg",
        },
    },
    "squanto_route": {
        "title": "Squanto — Plymouth",
        "color": "#5a4a2e",
        "audio": "audio/squanto/squanto_main.mp3",
        "html": "squanto.html",
        "side": "plymouth",
        "hub_href": "index.html?back=1",
        "default_bg": "images/hub/plymouth_squanto.png",
        "slide_images": {
            # Patuxet pre-1614
            "slide_1": "images/squanto/patuxet-village-life.jpg",
            "slide_2": "images/squanto/champlain-plymouth-1605.jpg",
            "slide_3": "images/squanto/weymouth-captain.jpg",
            # 1614 Hunt capture
            "slide_4": "images/squanto/algonquian-canoe-build.jpg",
            "slide_5": "images/squanto/caravel-armada.jpg",
            "slide_6": "images/squanto/caravel-armada.jpg",
            # Spain (Málaga friars)
            "slide_7": "images/squanto/malaga-1572.jpg",
            "slide_8": "images/squanto/malaga-1572.jpg",
            "slide_9": "images/squanto/malaga-1572.jpg",
            "slide_10": "images/squanto/algonquian-dress.jpg",
            # London + crossing
            "slide_11": "images/squanto/thames-london-17c.jpg",
            "slide_12": "images/squanto/thames-london-17c.jpg",
            "slide_13": "images/squanto/algonquian-fishing.jpg",
            # Empty Patuxet 1619
            "slide_14": "images/squanto/pomeiock-town.jpg",
            "slide_15": "images/squanto/pomeiock-village-bry.jpg",
            "slide_16": "images/squanto/secoton-village.jpg",
            "slide_17": "images/hub/plymouth_massasoit.jpg",
            "slide_18": "images/squanto/algonquian-cookfish.jpg",
            # Mayflower 1620
            "slide_19": "images/bradford/mayflower_at_sea.jpg",
            "slide_20": "images/bradford/mayflower_in_plymouth_harbor_halsall.jpg",
            "slide_21": "images/squanto/algonquian-dress.jpg",
            "slide_22": "images/squanto/samoset-interview.jpg",
            "slide_23": "images/squanto/samoset-interview.jpg",
            # Teaching corn
            "slide_24": "images/squanto/squanto-teaching.png",
            "slide_25": "images/squanto/squanto-teaching.png",
            "slide_26": "images/hub/plymouth_massasoit.jpg",
            # Thanksgiving
            "slide_27": "images/squanto/algonquian-cookfish.jpg",
            "slide_28": "images/squanto/thanksgiving-brownscombe.jpg",
            "slide_29": "images/squanto/champlain-plymouth-1605.jpg",
            # 1622 expedition + death
            "slide_30": "images/squanto/algonquian-fishing.jpg",
            "slide_31": "images/squanto/squanto-billington-1922.jpg",
            "slide_32": "images/squanto/squanto-billington-1922.jpg",
            # Epilogues
            "slide_33": "images/squanto/new-england-smith-1614.jpg",
            "slide_34": "images/squanto/purchas-new-england-map.jpg",
            "slide_35": "images/squanto/purchas-new-england-map.jpg",
            "slide_36": "images/squanto/pomeiock-town.jpg",
            "slide_37": "images/squanto/new-england-smith-1614.jpg",
            "slide_38": "images/squanto/pomeiock-village-bry.jpg",
        },
    },
    "massasoit_route": {
        "title": "Massasoit — Plymouth",
        "color": "#3e3a2e",
        "audio": "audio/massasoit/massasoit_main.mp3",
        "html": "massasoit.html",
        "side": "plymouth",
        "hub_href": "index.html?back=1",
        "default_bg": "images/hub/plymouth_massasoit.jpg",
        "slide_images": {
            # Pre-Plymouth (plague + consolidation)
            "slide_1": "images/massasoit/massasoit-relief.jpg",
            "slide_2": "images/massasoit/debry-secoton-village.jpg",
            "slide_2b": "images/massasoit/debry-pomeiooc-village.jpg",
            "slide_2c": "images/massasoit/sowams-1908.jpg",
            "slide_2d": "images/massasoit/debry-three-sisters.jpg",
            # First contact 1620
            "slide_3": "images/massasoit/mayflower-halsall.jpg",
            "slide_3b": "images/massasoit/debry-pomeiooc-village.jpg",
            "slide_3c": "images/massasoit/night-attack-waldron.jpg",
            "slide_4": "images/massasoit/squanto-teaching.png",
            "slide_4b": "images/massasoit/squanto-teaching.png",
            "slide_4c": "images/massasoit/sowams-1908.jpg",
            "slide_5": "images/massasoit/massasoit-palace-1857.jpg",
            # Decisions + alliance
            "slide_6": "images/massasoit/massasoit-warriors.jpg",
            "slide_8": "images/massasoit/debry-secoton-village.jpg",
            "slide_10": "images/massasoit/massasoit-warriors.jpg",
            "slide_11": "images/massasoit/bradford-portrait.jpg",
            "slide_13": "images/massasoit/carver-massasoit.jpg",
            # Thanksgiving
            "slide_14": "images/massasoit/thanksgiving-brownscombe.jpg",
            "slide_14b": "images/massasoit/massasoit-palace-1857.jpg",
            "slide_14c": "images/massasoit/sowams-1908.jpg",
            "slide_14d": "images/massasoit/debry-indian-fishing.jpg",
            "slide_14e": "images/massasoit/thanksgiving-ferris.jpg",
            # Squanto death + decade
            "slide_15": "images/massasoit/squanto-teaching.png",
            "slide_15b": "images/massasoit/massasoit-palace-1857.jpg",
            "slide_16": "images/massasoit/sowams-1908.jpg",
            # Pequot War 1637
            "slide_17": "images/massasoit/mystic-massacre-19c.jpg",
            "slide_18": "images/massasoit/mystic-massacre.jpg",
            "slide_19": "images/massasoit/indian-history-1919.jpg",
            # Land pressure
            "slide_20": "images/massasoit/debry-three-sisters.jpg",
            "slide_20b": "images/massasoit/sowams-1908.jpg",
            "slide_21": "images/massasoit/debry-corn-prosper.jpg",
            "slide_22": "images/massasoit/debry-three-sisters.jpg",
            # Sons + Wamsutta
            "slide_23": "images/massasoit/philip-church-1827.jpg",
            "slide_23b": "images/massasoit/massasoit-palace-1857.jpg",
            "slide_23c": "images/massasoit/night-attack-waldron.jpg",
            "slide_24": "images/massasoit/philip-appleton.jpg",
            "slide_25": "images/massasoit/philip-appleton.jpg",
            "slide_26": "images/massasoit/philip-church-1827.jpg",
            "slide_27": "images/massasoit/massasoit-relief.jpg",
            "slide_28": "images/massasoit/philip-revere.jpg",
            "slide_29": "images/massasoit/massasoit-palace-1857.jpg",
        },
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
      'advances to Slide 14b' / 'Slide 13-FAIL-A' → 'slide_14b' / 'slide_13_fail_a' (resolved later by alias)
      'returns to HOME' / 'returns HOME' / 'HOME' → 'HOME'
    """
    t = target_text.strip().lower()
    if "home" in t or "title screen" in t or "another route" in t or "another character" in t:
        return "HOME"
    # GAMEOVER X (dedicated gameover slide)
    m = re.search(r"slide\s+gameover\s+([a-z])", t)
    if m:
        return f"slide_gameover_{m.group(1)}"
    m = re.search(r"\bgameover\s+([a-z])\b", t)
    if m:
        return f"slide_gameover_{m.group(1)}"
    # FAIL pattern (Powhatan: 11-FAIL, 13-FAIL-A) — check BEFORE plain numbered
    m = re.search(r"slide[_\s]+(\d+)[-\s]*fail(?:[-\s]*([a-z]))?", t)
    if m:
        n, sub = m.group(1), m.group(2)
        return f"slide_{n}_fail_{sub}" if sub else f"slide_{n}_fail"
    # Hyphenated tag (Powhatan: 7-DELEGATION, 7-PEACE)
    m = re.search(r"slide[_\s]+(\d+)-(\w+)", t)
    if m:
        return f"slide_{m.group(1)}_{m.group(2).lower()}"
    # numbered slide with letter suffix (Bradford 3a, 6a; Massasoit 2b)
    m = re.search(r"slide[_\s]+(\d+[a-z]+)\b", t)
    if m:
        return f"slide_{m.group(1)}"
    # plain numbered slide
    m = re.search(r"slide[_\s]+(\d+)", t)
    if m:
        return f"slide_{m.group(1)}"
    # epilogue / closing card / final slide → keep as next slide if we can't tell
    if "epilogue" in t or "closing card" in t or "final" in t:
        return "_NEXT_"
    return "_NEXT_"


def parse_slide_block(block_text, slide_index_in_file, gameover_alias_map=None):
    """Parse a single slide markdown block into a slide dict.

    gameover_alias_map: dict mutated in-place. Maps "gameover_x" letter -> slide_id
    for slides whose title contains GAMEOVER N pattern. Used so button targets
    that reference 'GAMEOVER F' resolve to the actual slide_id.
    """
    # Extract header — accept many slide-ID conventions used by writers:
    #  Slide 1 — title
    #  Slide GAMEOVER A — title
    #  Slide 6-FAIL — title
    #  Slide 13-FAIL-A — title
    #  Slide 7-DELEGATION — title
    #  Slide 14b — title (Bradford / Massasoit)
    #  GAMEOVER A1 — title (Squanto, no "Slide" prefix)
    # Separator must be em-dash (—) or en-dash (–), NOT plain hyphen.
    first_line = block_text.split("\n", 1)[0]

    # Squanto-style: "## GAMEOVER A1 — title" (no "Slide" prefix)
    standalone_go = re.match(r"##\s+GAMEOVER\s+([A-Za-z][\w]*)\s+[—–]\s+(.*)", first_line)
    if standalone_go:
        raw_id = "gameover_" + standalone_go.group(1).lower()
        title = standalone_go.group(2).strip()
    else:
        header_match = re.match(r"##\s+Slide\s+(GAMEOVER\s+[A-Za-z]|[\w\-]+?)\s+[—–]\s+(.*)", block_text)
        if not header_match:
            # Fallback for headers without an em-dash separator
            header_match = re.match(r"##\s+Slide\s+([\w\-]+)\s*$", first_line)
            if not header_match:
                return None
            raw_id = header_match.group(1).strip()
            title = ""
        else:
            raw_id = header_match.group(1).strip()
            title = header_match.group(2).strip()

    is_gameover = False
    gameover_letter = None

    # Sanitize slide ID: lowercase + hyphens to underscores
    raw_id_norm = raw_id.lower().replace("-", "_")

    if raw_id.upper().startswith("GAMEOVER") or raw_id.lower().startswith("gameover_"):
        # Squanto: raw_id = "gameover_a1" → slide_id = "slide_gameover_a1"
        # Smith: raw_id = "GAMEOVER A" → slide_id = "slide_gameover_a"
        if raw_id.lower().startswith("gameover_"):
            letter = raw_id[len("gameover_"):].lower()
        else:
            letter = raw_id.split()[-1].lower()
        slide_id = f"slide_gameover_{letter}"
        is_gameover = True
        gameover_letter = letter
        # KEEP the writer's specific title (e.g., "I Saved the Cargo") rather than
        # overriding to "WRONG LEVERRRR!" — the big red GAME OVER banner already
        # plays the universal stinger role. Each gameover gets its own descriptive name.
        # Strip the writer's own dash-prefixed "GAMEOVER X — " or quote markers if present
        title = re.sub(r'^(?:GAMEOVER\s+\w+\s*[—–-]\s*)?["“]?(.+?)["”]?$', r'\1', title).strip()
        if not title:
            title = "WRONG LEVERRRR!"
    else:
        slide_id = f"slide_{raw_id_norm}"
        # FAIL pattern in slide ID (Powhatan: 6_fail, 13_fail_a)
        fail_in_id = re.search(r"_fail(?:_([a-z]))?$", raw_id_norm)
        # Title check for "GAMEOVER X"
        title_go_match = re.search(r"GAMEOVER\s+([A-Za-z])\b", title, re.IGNORECASE)
        # Title says "(gameover, ...)" — Powhatan style
        title_paren_go = re.search(r"\(gameover[,)]", title, re.IGNORECASE)

        if fail_in_id or title_go_match or title_paren_go:
            is_gameover = True
            if fail_in_id:
                suffix = fail_in_id.group(1)
                gameover_letter = f"{raw_id_norm}" if not suffix else f"{raw_id_norm}"
            elif title_go_match:
                gameover_letter = title_go_match.group(1).lower()
            else:
                gameover_letter = raw_id_norm
            # Strip "GAMEOVER X" prefix from title if present, but KEEP the descriptive part
            title = re.sub(r'^GAMEOVER\s+\w+\s*[—–-]\s*', '', title, flags=re.IGNORECASE).strip()
            # Strip parenthetical "(gameover, ...)" annotations
            title = re.sub(r'\s*\([^)]*gameover[^)]*\)\s*$', '', title, flags=re.IGNORECASE).strip()
            # Strip surrounding quotes
            title = title.strip('"“”').strip()
            if not title:
                title = "WRONG LEVERRRR!"
        # Bradford/Massasoit: slide IDs like 3a, 6a, 8a where title says "DECISION", "Off-Ramp",
        # or contains gameover-like content. Don't auto-flag these as gameovers anymore — let
        # the title content (or the writer's explicit decision marker) decide.
        elif re.match(r"^\d+[a-z]+$", raw_id_norm):
            # Treat as story unless title explicitly says gameover/fail/wrong-lever
            if re.search(r"\b(gameover|wrong\s+lever|fail|the\s+\w+\s+kills?)\b", title, re.IGNORECASE):
                is_gameover = True
                gameover_letter = raw_id_norm
                title = "WRONG LEVERRRR!"

    slide_type = "gameover" if is_gameover else "story"
    if not is_gameover:
        if "DECISION" in title.upper():
            slide_type = "decision"
        # Strip writer's organizational prefixes from displayed title
        title = re.sub(r"^DECISION\s+\d+:?\s*", "", title, flags=re.IGNORECASE)
        title = re.sub(r"\s*\(Decision\s+\d+\)\s*$", "", title, flags=re.IGNORECASE)
        # Hide stage-direction titles ("Title / Cold Open", "Cold Open", etc.)
        if re.match(r"^(title\s*/?\s*cold\s+open|cold\s+open|title)$", title, re.IGNORECASE):
            title = ""

    # Register alias so "GAMEOVER F" button-targets resolve to this slide_id
    if is_gameover and gameover_alias_map is not None and gameover_letter:
        gameover_alias_map[gameover_letter] = slide_id
        gameover_alias_map[f"slide_gameover_{gameover_letter}"] = slide_id

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
    # Accept "**Buttons:**" or "**Buttons (with anything):**" headers
    buttons = []
    button_section = re.search(r"\*\*Buttons[^*]*\*\*\s*\n((?:[-*]\s+.*\n?)+)", block_text)
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
            # Trim trailing arrows that some writers added inside brackets
            btn_text = re.sub(r"\s*[→←↺]+\s*$", "", btn_text)
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
    # Split on `## Slide` OR `## GAMEOVER` boundaries (Squanto uses standalone GAMEOVER headers)
    blocks = re.split(r"\n(?=##\s+(?:Slide|GAMEOVER)\b)", text)
    slides = []
    gameover_alias_map = {}
    for i, block in enumerate(blocks):
        stripped = block.strip()
        if not (stripped.startswith("## Slide") or stripped.startswith("## GAMEOVER")):
            continue
        slide = parse_slide_block(block, i, gameover_alias_map)
        if slide:
            slides.append(slide)
    # After all slides parsed, resolve any button targets that reference gameover aliases
    all_ids = {s["id"] for s in slides}
    for s in slides:
        for btn in s["buttons"]:
            t = btn["target"]
            if t in all_ids or t in ("HOME", "_NEXT_"):
                continue
            # Try gameover alias map (lookup by alias key, e.g., "slide_gameover_f" or just "f")
            if t in gameover_alias_map:
                btn["target"] = gameover_alias_map[t]
                continue
            # Try lowercase letter alias
            letter = t.replace("slide_gameover_", "").replace("slide_", "").lower()
            if letter in gameover_alias_map:
                btn["target"] = gameover_alias_map[letter]
                continue
    return slides


def resolve_next_targets(slides):
    """Resolve _NEXT_ targets and auto-skip story-slide CONTINUE buttons over gameovers.

    Critical fix: writers sometimes write 'advances to Slide 5' from a story slide
    where Slide 5 is actually the next-numbered slide — but that slide may be a
    gameover (because the wrong-choice gameover sits between two narrative slides).
    For STORY slides with single-button or CONTINUE-style buttons, if the target
    is a gameover, advance past gameover slides to find the next narrative slide.
    """
    story_ids = [s["id"] for s in slides if s["type"] != "gameover"]
    all_slides_by_id = {s["id"]: s for s in slides}
    all_ids = set(all_slides_by_id)

    # Pass 1: resolve _NEXT_ targets
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

    # Pass 2: drop button targets that don't exist
    for s in slides:
        for btn in s["buttons"]:
            if btn["target"] not in all_ids and btn["target"] != "HOME":
                btn["target"] = "HOME"

    # Pass 3: STORY-slide CONTINUE buttons that land on a gameover →
    # auto-skip past gameovers to next narrative slide
    # Heuristic: if a story slide has exactly ONE button AND that button targets
    # a gameover slide, the writer meant "next narrative slide" not "the gameover"
    for s in slides:
        if s["type"] == "gameover":
            continue
        if len(s["buttons"]) != 1:
            continue  # multi-button = real branching, leave alone
        btn = s["buttons"][0]
        if btn["target"] == "HOME":
            continue
        target_slide = all_slides_by_id.get(btn["target"])
        if target_slide and target_slide["type"] == "gameover":
            # Walk forward in slide order until we find a non-gameover slide
            target_idx = next((i for i, x in enumerate(slides) if x["id"] == btn["target"]), -1)
            if target_idx >= 0:
                for j in range(target_idx + 1, len(slides)):
                    if slides[j]["type"] != "gameover":
                        btn["target"] = slides[j]["id"]
                        break
                else:
                    btn["target"] = "HOME"

    # Pass 4: gameover Try Again buttons → restart at slide_1 (per Time Warp engine rule)
    # Per memory feedback_timewarp_building.md: "Try Again buttons: ALWAYS go to slide_0
    # (the very beginning), never the next slide." Use slide_1 as the canonical start.
    first_story_id = next((s["id"] for s in slides if s["type"] != "gameover"), "slide_1")
    for s in slides:
        if s["type"] != "gameover":
            continue
        # Find Try Again button (first non-HOME button) and retarget to start
        had_retry = False
        for btn in s["buttons"]:
            if btn["target"] != "HOME":
                btn["target"] = first_story_id
                # Make button text say "↺ Try Again" if it's just a Continue
                if "again" not in btn["text"].lower() and "try" not in btn["text"].lower():
                    btn["text"] = "↺ Try Again"
                had_retry = True
        # If no non-HOME button existed, prepend a Try Again
        if not had_retry:
            s["buttons"].insert(0, {"text": "↺ Try Again", "target": first_story_id})

    # Pass 5: decision slides with NO button leading forward (all buttons → gameover or HOME)
    # are dead ends in narrative flow. Auto-redirect the FIRST gameover-targeted button
    # to the next narrative slide so the route is at least playable.
    for i, s in enumerate(slides):
        if s["type"] == "gameover":
            continue
        if len(s["buttons"]) < 2:
            continue
        # Are any buttons leading to a non-gameover, non-HOME slide?
        forward_btns = [
            btn for btn in s["buttons"]
            if btn["target"] != "HOME"
            and btn["target"] in all_slides_by_id
            and all_slides_by_id[btn["target"]]["type"] != "gameover"
        ]
        if forward_btns:
            continue  # has at least one forward path, OK
        # Find next narrative slide after this one
        next_narrative_id = None
        for j in range(i + 1, len(slides)):
            if slides[j]["type"] != "gameover":
                next_narrative_id = slides[j]["id"]
                break
        if not next_narrative_id:
            continue
        # Redirect the first gameover-targeted button (the writer's intended "good" choice)
        for btn in s["buttons"]:
            if btn["target"] in all_slides_by_id and all_slides_by_id[btn["target"]]["type"] == "gameover":
                btn["target"] = next_narrative_id
                break

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
  background-position: center; /* true center — works for both portraits and ships */
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

/* Right-side panel — wraps card + buttons in a flex column, stacked from top */
.panel {
  position: absolute;
  top: 2vh;
  right: 2vw;
  bottom: 76px; /* clear timeline */
  width: 42%;
  max-width: 480px;
  z-index: 5;
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* card + buttons hug the top, no empty gap */
  gap: 1.5vh;
  pointer-events: none;
}
.panel > * { pointer-events: auto; }

/* Text card: sizes to content (flex 0 0 auto), more transparent */
.card {
  position: relative;
  z-index: 5;
  width: 100%;
  background: rgba(255,255,255,0.55);
  backdrop-filter: blur(3px);
  -webkit-backdrop-filter: blur(3px);
  border: 2px solid rgba(0,0,0,0.85);
  border-radius: 8px;
  padding: 1.1vh 1.5vw;
  box-shadow: 0 6px 24px rgba(0,0,0,0.55);
  font-family: 'Bangers', 'Arial Black', sans-serif;
  color: #000;
  line-height: 1.3;
  letter-spacing: 0.5px;
  text-align: left;
  flex: 0 0 auto;
}
.card h2 {
  font-size: clamp(1rem, 1.8vw, 1.35rem);
  margin-bottom: 0.6vh;
  color: #000;
  letter-spacing: 1px;
  text-align: center;
  border-bottom: 1px solid rgba(0,0,0,0.2);
  padding-bottom: 0.5vh;
}
.card .body p {
  font-size: clamp(0.95rem, 1.45vw, 1.25rem);
  margin-bottom: 0.5vh;
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 600ms ease, transform 600ms ease;
}
.card .body p.shown { opacity: 1; transform: translateY(0); }
.card .body p:last-child { margin-bottom: 0; }

/* Buttons: bottom of the right-side panel column */
.buttons {
  position: relative;
  z-index: 11;
  display: flex;
  flex-direction: column;
  gap: 1vh;
  align-items: stretch;
  width: 100%;
  flex: 0 0 auto;
  opacity: 0;
  transition: opacity 600ms ease;
}
.buttons.shown { opacity: 1; }

button.choice {
  background: rgba(255,255,255,0.6);
  backdrop-filter: blur(3px);
  -webkit-backdrop-filter: blur(3px);
  color: #000;
  border: 2px solid rgba(0,0,0,0.85);
  border-radius: 6px;
  padding: 1.1vh 1.4vw;
  font-family: 'Bangers', sans-serif;
  font-size: clamp(0.95rem, 1.35vw, 1.2rem);
  cursor: pointer;
  transition: all 150ms ease;
  min-width: 0;
  width: 100%;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.4);
  line-height: 1.2;
}
button.choice:hover {
  background: rgba(255,255,255,0.92);
  border-color: #000;
  transform: scale(1.02);
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
.slide.gameover-slide .panel {
  /* Center the gameover panel under the GAME OVER banner */
  top: 16vh;
  right: auto;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  max-width: 700px;
  bottom: 100px;
  align-items: center;
  text-align: center;
}
.slide.gameover-slide .card {
  background: rgba(20,5,5,0.85);
  border-color: #6a0000;
  border-width: 3px;
  color: #fff8e0;
  text-align: center;
  width: 100%;
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
      if (slide.bg_position) {
        div.style.backgroundPosition = slide.bg_position;
      }
    }
  }

  if (slide.gif) {
    const gifImg = document.createElement('img');
    gifImg.className = 'fullscreen-gif';
    gifImg.src = slide.gif;
    gifImg.alt = 'gameover';
    div.appendChild(gifImg);
  }

  // Right-side panel wraps card + buttons in a flex column so they never overlap
  const panel = document.createElement('div');
  panel.className = 'panel';

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
  panel.appendChild(card);

  const btnWrap = document.createElement('div');
  btnWrap.className = 'buttons';
  slide.buttons.forEach(b => {
    const btn = document.createElement('button');
    btn.className = 'choice';
    btn.textContent = b.text;
    btn.addEventListener('click', () => goToSlide(b.target));
    btnWrap.appendChild(btn);
  });
  panel.appendChild(btnWrap);

  div.appendChild(panel);

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
  const buttons = slideEl.querySelector('.panel > .buttons');
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
  const bw = el.querySelector('.panel > .buttons');
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
