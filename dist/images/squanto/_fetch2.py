"""Fetch additional Wikimedia Commons period images for the Squanto route.

All sources are public-domain period art (de Bry 1590, John White 1585,
Champlain 1605-1612, Braun's Malaga 1572, 19th-c. period engravings
where no contemporary art exists). NO racist 19th-c. cliches; the
romanticized "noble savage" pieces have been deliberately avoided.

Usage (from this folder):
    python _fetch2.py
"""

import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))

# (filename, wikimedia URL, one-line description)
# Use full-size /commons/X/YY/ paths (NOT /thumb/) to get full resolution.
IMAGES = [
    # ---- Patuxet pre-1614 / Wampanoag village daily life ----
    (
        "patuxet-village-life.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/bb/Village_of_Secotan.jpg",
        "John White 1585 — Algonquian village daily life (Patuxet stand-in)",
    ),
    (
        "algonquian-fishing.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/d/df/North_carolina_algonkin-fischen.jpg",
        "John White / de Bry — Algonquian fishing in dugout canoe",
    ),
    (
        "algonquian-cookfish.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/4/48/How_they_cook_their_fish_%281590%29.jpg",
        "de Bry 1590 — drying / cooking fish on racks (Patuxet daily life)",
    ),
    (
        "algonquian-canoe-build.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/7/78/How_they_build_boats_%281590%29.jpg",
        "de Bry 1590 — building a dugout canoe",
    ),
    (
        "algonquian-dress.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/4/49/North_carolina_algonkin-kleidung02.jpg",
        "John White / de Bry — period-correct Algonquian dress (no Plains stereotype)",
    ),

    # ---- Champlain New England maps ----
    (
        "champlain-1612-newfrance.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/a/ad/Detail_of_Carte_Geographique_de_la_Nouelle_Franse_by_Samuel_de_Champlain_%281612%29.jpg",
        "Champlain 1612 — Carte Geographique de la Nouvelle France (detail)",
    ),
    (
        "purchas-new-england-map.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/f/fc/Purchas_Map_of_New_England.jpg",
        "Purchas — early New England map",
    ),

    # ---- Hunt's capture / Atlantic crossing in chains ----
    (
        "caravel-armada.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/9/9c/Caravela_de_armada_of_Joao_Serrao.jpg",
        "Period caravel — Hunt's-class English ship boarding/anchored",
    ),
    (
        "elmina-slaving-fort.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/4/4a/ElMina_AtlasBlaeuvanderHem.jpg",
        "Elmina Castle — Atlantic slaving infrastructure (hold/crossing stand-in)",
    ),

    # ---- Spanish friars / Malaga ----
    (
        "ribalta-san-francisco.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/7/7f/Ribalta-san_francisco-prado.jpg",
        "Ribalta — Franciscan friar, brown robe, Spanish period painting",
    ),
    (
        "franciscan-monastery-lopud.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/3b/Franciscan_monastery_Lopud.JPG",
        "Franciscan monastery courtyard (period architecture)",
    ),
    (
        "gozzoli-st-francis-rule.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/4/42/Dream_of_Innocent_III_and_the_Confirmation_of_the_Rule_of_St_Francis_Benozzo_Gozzoli.jpg",
        "Gozzoli — friars in courtyard council (friars' bargain stand-in)",
    ),

    # ---- London 1615 / Thames docks ----
    (
        "thames-london-17c.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/9/9d/Copyrighted_and_Published_by_A_S_Burbank%2C_The_Mayflower_at_Sea_%28NBY_21340%29.jpg",
        "English ship at sea — London/Atlantic crossing stand-in",
    ),
    (
        "leiden-wool-trade.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/f/fd/Isaac_Claesz._Van_Swanenburg_Washing_the_Skins_and_Grading_the_Wool.jpg",
        "Van Swanenburg — period merchant counting-house / trade interior",
    ),

    # ---- Empty Patuxet 1619 / plague ----
    (
        "southern-ne-1620-map.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c4/Southern_New_England%2C_1620%E2%80%9322_%28rev%29.jpg",
        "Southern New England 1620-22 — territories after the Great Dying",
    ),
    (
        "fiske-southern-ne.png",
        "https://upload.wikimedia.org/wikipedia/commons/e/ea/Fiske%2C_Map_of_Southern_New_England.png",
        "Fiske — Southern New England nations map (epilogue infographic)",
    ),

    # ---- Mayflower / Pilgrim arrival / first contact ----
    (
        "mayflower-at-sea.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/1c/The_Mayflower_at_sea.jpg",
        "Mayflower at sea — 1620 arrival",
    ),
    (
        "pilgrims-landing-1620.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/33/The_landing_of_the_Pilgrims_at_Plymouth%2C_Mass._Dec._22nd_1620_LCCN2002707741.jpg",
        "Landing of the Pilgrims at Plymouth, Dec 1620",
    ),
    (
        "samoset-interview.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/4/45/Interview_of_Samoset_with_the_Pilgrims.jpg",
        "Samoset walks into Plymouth (1853 cover, period-respectful)",
    ),

    # ---- Squanto teaches / Plymouth alliance ----
    (
        "squanto-teaching.png",
        "https://upload.wikimedia.org/wikipedia/commons/b/bc/Squantoteaching.png",
        "Squanto teaches Pilgrims the mound-and-fish (1911 illustration)",
    ),
    (
        "carver-massasoit-meeting.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/2/2a/Meeting_of_Governor_Carver_and_Massasoit_-_drawn_by_H.L._Stevens_%3B_eng%27d._by_Augustus_Robin%2C_N.Y._LCCN89707285_%28cropped%29.jpg",
        "Governor Carver and Massasoit — Plymouth alliance / treaty signing",
    ),
    (
        "wampanoag-pipe-council.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b1/Wampanoag2.jpg",
        "Wampanoag ceremonial pipe / council scene",
    ),
    (
        "thanksgiving-brownscombe.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/9/98/Thanksgiving-Brownscombe.jpg",
        "Brownscombe 1914 — First Thanksgiving at Plymouth",
    ),

    # ---- Massasoit / Wampanoag long game ----
    (
        "wampanoag-wigwam.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/6/69/Plimoth_Plantation_Native_American_Wigwam.jpg",
        "Wampanoag wetu interior (Plimoth Patuxet — dignified reference)",
    ),
    (
        "sowams-map.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c8/Sowams_-_with_ancient_records_of_Sowams_and_parts_adjacent-illustrated_%281908%29_%2814784453735%29.jpg",
        "Sowams / Pokanoket — Massasoit's seat (council location)",
    ),
    (
        "massasoit-portrait.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/0/0a/Indian_history_for_young_folks_%281919%29_%2814752985292%29.jpg",
        "Massasoit period portrait illustration",
    ),

    # ---- Eastern North America landscape / pre-contact ----
    (
        "pomeiock-village-bry.jpg",
        # Already have pomeiock-town.jpg; this is a different de Bry view if needed.
        "https://upload.wikimedia.org/wikipedia/commons/c/c8/North_carolina_algonkin-kleidung03.jpg",
        "de Bry — Algonquian pre-contact landscape figures",
    ),
]


def fetch_one(filename: str, url: str, desc: str) -> bool:
    out = os.path.join(HERE, filename)
    if os.path.exists(out) and os.path.getsize(out) > 5000:
        print(f"  skip  {filename} (exists)")
        return True
    print(f"  GET   {filename}")
    print(f"        {url}")
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "TimeWarpEdu/1.0 (educational, school project)"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        with open(out, "wb") as f:
            f.write(data)
        size_kb = len(data) // 1024
        print(f"        OK ({size_kb} KB) — {desc}")
        return True
    except Exception as e:
        print(f"        FAIL: {e}")
        return False


def main():
    ok = 0
    fail = 0
    for fn, url, desc in IMAGES:
        if fetch_one(fn, url, desc):
            ok += 1
        else:
            fail += 1
    print(f"\nDone. {ok} ok, {fail} failed.  Folder: {HERE}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
