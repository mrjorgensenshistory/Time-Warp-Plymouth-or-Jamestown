"""
Massasoit route — second image fetch pass.
Pulls 18 additional period images (Wikimedia Commons) for the Massasoit route slides.

Run from this folder:
    python _fetch2.py

All sources public domain unless noted. Uses Special:FilePath redirect so we don't
have to compute MD5 hash prefixes manually.
"""

import os
import sys
import urllib.request
import urllib.parse

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# (output_filename, wikimedia_commons_filename_or_full_url, description)
IMAGES = [
    # --- Pre-1616 Wampanoag homeland / village life ---
    ("debry-secoton-village.jpg",
     "Village of Secoton Theodor de Bry 1590.jpg",
     "de Bry 1590, Village of Secoton — bark houses, corn fields, ceremony fire. Wampanoag homeland analog."),
    ("debry-pomeiooc-village.jpg",
     "Indian_Village_of_Pomeiooc_Theodor_de_Bry_1590.jpg",
     "de Bry 1590, palisaded Pomeiooc village — longhouses, central fire."),
    ("debry-indian-fishing.jpg",
     "Their manner of fishing in Virginia LCCN2001695730.jpg",
     "de Bry / White, 'Their manner of fishing in Virginia' — weirs and canoes. Wampanoag coastal life pre-plague."),
    ("debry-three-sisters.jpg",
     "Florida_Indians_planting_seeds_of_beans_or_maize_LCCN2001695741.jpg",
     "Le Moyne / de Bry, planting corn and beans — Three Sisters agriculture analog."),
    ("debry-corn-prosper.png",
     "Squantohowwellthecornprospered.png",
     "Squanto — how well the corn prospered (1911 textbook engraving). Squanto / fish-fertilizer scene."),

    # --- Mayflower arrival, 1620 ---
    ("mayflower-halsall.jpg",
     "Mayflower_in_Plymouth_Harbor,_by_William_Halsall.jpg",
     "William Halsall, 1882 — Mayflower at anchor at Plymouth, view from shore."),

    # --- 1621 alliance / Plymouth fort ---
    ("massasoit-palace-1857.jpg",
     "The_Palace_of_Massasoit_LCCN89707226.jpg",
     "Harper's 1857, 'The Palace of Massasoit' — Pokanoket sachem's residence, period engraving."),
    ("bradford-portrait.jpg",
     "Williambradford_bw.jpg",
     "William Bradford — Plymouth governor, treaty counterpart at signing."),
    ("squanto-teaching.png",
     "Squantoteaching.png",
     "Squanto teaching Pilgrims to plant corn — translator scene."),
    ("squanto-travels-map.jpg",
     "SquantoTravels.jpg",
     "Map of Squanto's travels — Patuxet → Spain → London → home. Useful for slide 4."),

    # --- First Thanksgiving variants ---
    ("thanksgiving-brownscombe.jpg",
     "Thanksgiving-Brownscombe.jpg",
     "Brownscombe, 1914 — canonical First Thanksgiving painting. Slide 14e."),
    ("thanksgiving-ferris.png",
     "The_First_Thanksgiving_Jean_Louis_Gerome_Ferris.png",
     "Jean Louis Gerome Ferris — First Thanksgiving alternate."),
    ("thanksgiving-wyeth.jpg",
     "N.C._Wyeth_-_Thanksgiving_with_Indians.jpg",
     "N.C. Wyeth, 1940 — Thanksgiving with Indians. Long, mural-style composition."),

    # --- Pequot War 1637 ---
    ("mystic-massacre-19c.png",
     "Mystic_Massacre_1637_Destruction_Of_The_Pequots_in_Connecticut.png",
     "19th-c. wood engraving, Mystic Massacre — burning Pequot fort."),
    ("fairfield-swamp-fight.png",
     "FairfieldSwampFight.png",
     "DeForest 1853 — Fairfield Swamp Fight (Pequot War endgame)."),

    # --- Sowams / Massasoit territory ---
    ("sowams-1908.jpg",
     "Sowams_-_with_ancient_records_of_Sowams_and_parts_adjacent-illustrated_(1908)_(14784453735).jpg",
     "Bicknell 1908, Sowams map — Wampanoag territory, Mount Hope, period cartography."),

    # --- King Philip's War / Metacom ---
    ("king-philip-1827-drake.jpg",
     "KingPhilip_1827_BenjaminChurch_SamuelDrake04264001.jpg",
     "Drake's 1827 King Philip frontispiece — Metacom with musket, wampum, headdress."),
    ("garrison-attack.jpg",
     "Indians_Attacking_a_Garrison_House.jpg",
     "Early-1800s engraving — Native warriors attacking English garrison house. King Philip's War."),
    ("night-attack-waldron.jpg",
     "Night_Attack_of_Indians.jpg",
     "Wood engraving — night raid on Waldron's House, Dover NH. Late King Philip's-era conflict."),

    # --- Wampanoag wigwam interior (deathbed scene) ---
    ("wampanoag-wigwam-interior.jpg",
     "Wampanoag_Wigwam_Plimoth_Patuxet.jpg",
     "Wigwam interior at Plimoth Patuxet — reference for Slide 23b/24 deathbed scene. CC-BY-SA 4.0, EgorovaSvetlana."),
]


def fetch(filename, source):
    """source is either a Commons filename or a full https URL."""
    out_path = os.path.join(OUT_DIR, filename)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 5000:
        print(f"  [skip] {filename} (exists)")
        return True
    if source.startswith("http"):
        url = source
    else:
        url = "https://commons.wikimedia.org/wiki/Special:FilePath/" + urllib.parse.quote(source)
    req = urllib.request.Request(url, headers={"User-Agent": "TimeWarp/1.0 (educational)"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        with open(out_path, "wb") as f:
            f.write(data)
        kb = len(data) / 1024
        print(f"  [ok]   {filename}  ({kb:,.0f} KB)")
        return True
    except Exception as e:
        print(f"  [FAIL] {filename}  -> {e}")
        return False


def main():
    print(f"Massasoit fetch2 — {len(IMAGES)} images -> {OUT_DIR}")
    ok = 0
    for fn, src, desc in IMAGES:
        if fetch(fn, src):
            ok += 1
    print(f"\n{ok}/{len(IMAGES)} succeeded.")
    return 0 if ok == len(IMAGES) else 1


if __name__ == "__main__":
    sys.exit(main())
