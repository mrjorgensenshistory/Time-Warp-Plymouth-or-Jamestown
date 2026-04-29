"""Fetch images using Wikimedia's Special:FilePath endpoint.

Special:FilePath?width=1280 is the friendliest high-volume path —
Wikimedia auto-redirects to the right thumbnail without us guessing
hash prefixes or file extensions.

Targets massasoit and squanto _fetch2 scripts, which use
Wikimedia filename-only references (not direct upload URLs).
"""
import os
import re
import time
import urllib.request
import urllib.parse
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow required")
    exit(1)

ROOT = Path(r"F:\Michael's\ACE\US History\Time-Warp-Plymouth-or-Jamestown\dist\images")
UA = "Mozilla/5.0 (compatible; TimeWarpEdu/1.0; mr.jorgensen@school.org)"

# Manual extraction from massasoit and squanto fetch2 scripts.
# Each entry: (character, filename, wikimedia_filename)
JOBS = [
    # MASSASOIT
    ("massasoit", "debry-secoton-village.jpg", "Village_of_Secoton_Theodor_de_Bry_1590.jpg"),
    ("massasoit", "debry-pomeiooc-village.jpg", "Indian_Village_of_Pomeiooc_Theodor_de_Bry_1590.jpg"),
    ("massasoit", "debry-indian-fishing.jpg", "Their_manner_of_fishing_in_Virginia_LCCN2001695730.jpg"),
    ("massasoit", "debry-three-sisters.jpg", "Florida_Indians_planting_seeds_of_beans_or_maize_LCCN2001695741.jpg"),
    ("massasoit", "debry-corn-prosper.jpg", "Squantohowwellthecornprospered.png"),
    ("massasoit", "mayflower-halsall.jpg", "Mayflower_in_Plymouth_Harbor,_by_William_Halsall.jpg"),
    ("massasoit", "massasoit-palace-1857.jpg", "The_Palace_of_Massasoit_LCCN89707226.jpg"),
    ("massasoit", "wampanoag-wigwam-interior.jpg", "Wetu.jpg"),
    ("massasoit", "thanksgiving-wyeth.jpg", "First_Thanksgiving_cph.3g04961.jpg"),
    ("massasoit", "thanksgiving-ferris.jpg", "The_First_Thanksgiving_cph.3g04961.jpg"),
    ("massasoit", "mystic-massacre-19c.jpg", "Mystic_Massacre_1637_Destruction_Of_The_Pequots_in_Connecticut.png"),
    ("massasoit", "fairfield-swamp-fight.jpg", "Battle_of_Bloody_Brook_-_NARA_-_532909.jpg"),
    ("massasoit", "night-attack-waldron.jpg", "Indians_Attacking_a_Garrison_House.jpg"),
    ("massasoit", "sowams-1908.jpg", "Sowams_-_with_ancient_records_of_Sowams_and_parts_adjacent-illustrated_(1908)_(14784453735).jpg"),
    ("massasoit", "squanto-travels-map.jpg", "Tisquantum_travels.png"),

    # SQUANTO
    ("squanto", "algonquian-cookfish.jpg", "How_they_cook_their_fish_(1590).jpg"),
    ("squanto", "algonquian-canoe-build.jpg", "How_they_build_boats_(1590).jpg"),
    ("squanto", "algonquian-dress.jpg", "A_weroans,_or_chieftain,_of_Virginia_LCCN2001696964.jpg"),
    ("squanto", "elmina-slaving-fort.jpg", "Elmina_castle_1668.jpg"),
    ("squanto", "franciscan-monastery-lopud.jpg", "Lopud_Monastery_courtyard.jpg"),
    ("squanto", "ribalta-san-francisco.jpg", "Francisco_Ribalta_-_Saint_Francis_with_a_Friar_-_Wikipedia.jpg"),
    ("squanto", "gozzoli-st-francis-rule.jpg", "Benozzo_gozzoli,_san_francesco,_predella_03_morte_e_funerali.jpg"),
    ("squanto", "leiden-wool-trade.jpg", "Isaac_Claesz._Van_Swanenburg_-_Het_volscheren_-_The_fulling_-_The_dyeing.jpg"),
    ("squanto", "wampanoag-wigwam.jpg", "Wetu_replica_at_Plimoth_Patuxet.jpg"),
    ("squanto", "wampanoag-pipe-council.jpg", "Wampanoag_chief_with_pipe.jpg"),
    ("squanto", "sowams-map.jpg", "Sowams.jpg"),
    ("squanto", "pilgrims-landing-1620.jpg", "Pilgrims_landing.jpg"),
    ("squanto", "carver-massasoit-meeting.jpg", "Meeting_of_Governor_Carver_and_Massasoit_-_drawn_by_H.L._Stevens_;_eng%27d._by_Augustus_Robin,_N.Y._LCCN89707285.jpg"),
    ("squanto", "thanksgiving-brownscombe.jpg", "Thanksgiving-Brownscombe.jpg"),
    ("squanto", "champlain-1612-newfrance.jpg", "Carte_geographique_de_la_Nouvelle_Franse_(1612).jpg"),
    ("squanto", "fiske-southern-ne.jpg", "Southern_New_England,_1620%E2%80%9322_(rev).jpg"),
    ("squanto", "purchas-new-england-map.jpg", "Purchas_Map_of_New_England.jpg"),
    ("squanto", "pomeiock-village-bry.jpg", "The_town_of_Pomeiock)_-_T.B_LCCN2001696973.jpg"),
    ("squanto", "massasoit-portrait.jpg", "Massasoit_statue_Plymouth.jpg"),
]


def fetch_via_filepath(filename, dest, width=1280):
    """Use Wikimedia's Special:FilePath redirect."""
    encoded = urllib.parse.quote(filename, safe="")
    url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{encoded}?width={width}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            if not data or len(data) < 5000:
                return False, len(data)
            dest.write_bytes(data)
            return True, len(data)
    except Exception as e:
        return False, str(e)[:60]


def compress(path, max_dim=1400):
    try:
        img = Image.open(path)
        if img.mode in ("RGBA", "P", "LA"):
            img = img.convert("RGB")
        if img.size[0] > max_dim or img.size[1] > max_dim:
            img.thumbnail((max_dim, max_dim), Image.LANCZOS)
        out = path.with_suffix(".jpg")
        img.save(out, "JPEG", quality=80, optimize=True)
        if out != path and path.exists():
            path.unlink()
        return out.stat().st_size
    except Exception as e:
        return -1


def main():
    ok, fail = 0, 0
    for char, filename, wmf in JOBS:
        dest = ROOT / char / filename
        if dest.exists() and dest.stat().st_size > 5000:
            print(f"  [skip-exists] {char}/{filename}")
            continue
        success, info = fetch_via_filepath(wmf, dest)
        if success:
            final = compress(dest)
            print(f"  [ok] {char}/{filename} ({(final if final > 0 else info)//1024}KB)")
            ok += 1
        else:
            print(f"  [FAIL] {char}/{filename}: {info}")
            fail += 1
            if dest.exists() and dest.stat().st_size < 5000:
                dest.unlink()
        time.sleep(5)
    print(f"\nOK: {ok}  FAIL: {fail}")


if __name__ == "__main__":
    main()
