"""
_fetch2.py — Wikimedia Commons period art for Powhatan route, batch 2.
Run: python _fetch2.py
Saves into the same directory. Skips files that already exist (idempotent).
After running, eyeball each file; if any are <30KB or fail, swap the URL
and re-run.
"""
import urllib.request, ssl, os, io
from PIL import Image

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

OUT = os.path.dirname(os.path.abspath(__file__))

# (filename, wikimedia upload URL)
# Sources: Theodor de Bry's America (1590, after John White), John White
# watercolors (British Museum / Wikimedia), Simon van de Passe 1616 engraving,
# 19th-c. history-painting engravings, Robert Vaughan's 1624 illustrations
# from Smith's Generall Historie, Mattheus Merian 1622 engraving.
images = [
    # --- John White / de Bry 1590 series (pre-contact / village life / agriculture) ---
    ("village_secoton.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/c/c6/North_carolina_algonkin-dorf.jpg"),
    ("village_pomeiooc.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/2/24/Pomeiooc.jpg"),
    ("indians_fishing_white.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/d/df/North_carolina_algonkin-fischen.jpg"),
    ("cooking_fish_white.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/4/48/How_they_cook_their_fish_%281590%29.jpg"),
    ("how_they_build_boats.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/7/78/How_they_build_boats_%281590%29.jpg"),
    ("dugout_canoe_debry.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/3/35/The_manner_of_makinge_their_boates_by_John_White.jpg"),
    ("praying_around_fire.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/e/ea/Praying_around_the_fire_with_rattles_%281590%29.jpg"),
    ("indians_dancing_white.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/9/96/North_carolina_algonkin-rituale01.jpg"),
    ("planting_corn_florida.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Florida_Indians_planting_seeds_of_beans_or_maize_LCCN2001695741.jpg/1280px-Florida_Indians_planting_seeds_of_beans_or_maize_LCCN2001695741.jpg"),
    ("hunting_deerskins.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Florida_Indians%2C_disguised_under_deerskins%2C_hunting_deer_LCCN2001695742.jpg/1280px-Florida_Indians%2C_disguised_under_deerskins%2C_hunting_deer_LCCN2001695742.jpg"),

    # --- Chiefs / regalia ---
    ("chief_herowan_white.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/6/66/A_chiefe_Herowan.jpg"),
    ("weroan_virginia_debry.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/A_weroans%2C_or_chieftain%2C_of_Virginia_LCCN2001696964.jpg/1024px-A_weroans%2C_or_chieftain%2C_of_Virginia_LCCN2001696964.jpg"),
    ("herowans_wife_white.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/e/ed/A_Cheife_Herowans_Wyfe.jpg"),

    # --- Smith captured / brought to Powhatan / coronation ---
    ("smith_captured_vaughan.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/0/03/John_Smith_taking_the_King_of_Pamavnkee_prisoner_-_etching.jpg"),
    ("smith_before_powhatan.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/9/9e/Powhatan_john_smith_map.jpg"),  # cartouche shows Powhatan in longhouse
    ("pocahontas_saves_smith.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/a/a9/Pocahontas_saving_the_life_of_Capt._John_Smith_-_New_England_Chromo._Lith._Co._LCCN95507872.jpg"),

    # --- Pocahontas as Lady Rebecca / marriage ---
    ("pocahontas_van_de_passe.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/b/b4/Pocahontas_by_Simon_van_de_Passe_%281616%29.png"),
    ("baptism_pocahontas.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/8/89/Baptism_of_Pocahontas.jpg"),
    ("marriage_pocahontas_hohenstein.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Anton_Hohenstein_-_The_marriage_of_Pocohontas_to_John_Rolfe_-_lithography_-_Philadelphia%2C_1860s.jpg/1024px-Anton_Hohenstein_-_The_marriage_of_Pocohontas_to_John_Rolfe_-_lithography_-_Philadelphia%2C_1860s.jpg"),

    # --- Opechancanough / 1622 / war ---
    ("opechancanough_portrait.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Ope-Chan-Ca-Nough_Chilberg_livesoffamousind00bowk_0075.jpg/800px-Ope-Chan-Ca-Nough_Chilberg_livesoffamousind00bowk_0075.jpg"),
    ("opechancanough_warriors.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Opechankanough_leading_his_warriors_circa_1644_History_of_virginia_1873.jpg/1024px-Opechankanough_leading_his_warriors_circa_1644_History_of_virginia_1873.jpg"),
    ("anger_opechancanough.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Anger_of_Opechancanough_with_Gov_Wyatt_ourcountryhistor01loss_0364.jpg/1024px-Anger_of_Opechancanough_with_Gov_Wyatt_ourcountryhistor01loss_0364.jpg"),
    ("massacre_1622_merian.jpg",  # already on disk; re-fetched in case of re-run
     "https://upload.wikimedia.org/wikipedia/commons/7/7c/Matth%C3%A4us_Merian_d%C3%86%2C_S%C3%A5ledes_blev_ogs%C3%A5_denne_fred_brudt_p%C3%A5_grund_af_bedrag%2C_KKSgb10894-5%2C_Statens_Museum_for_Kunst.jpg"),

    # --- Maps / landscape ---
    ("smith_map_virginia_1612.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/9/9e/Powhatan_john_smith_map.jpg"),
    ("chesapeake_landscape.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Chesapeake_bay_map_1670.jpg/1280px-Chesapeake_bay_map_1670.jpg"),

    # --- Trade / copper / English fleet / fort ---
    ("trade_indians_europeans.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Indians_trading_with_Europeans.jpg/1024px-Indians_trading_with_Europeans.jpg"),
    ("jamestown_fort_reconstruction.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Jamestown_fort.jpg/1280px-Jamestown_fort.jpg"),
    ("english_ships_fleet.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/3/38/JamestownShips.jpg"),

    # --- Late-life / death of chief / succession ---
    ("powhatan_death_engraving.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/The_burial_of_Powhatan.jpg/1024px-The_burial_of_Powhatan.jpg"),
    ("powhatan_mantle.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Powhatan%27s_mantle.jpg/800px-Powhatan%27s_mantle.jpg"),
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 EduFetch"})
    return urllib.request.urlopen(req, context=ctx, timeout=60).read()


def main():
    results = []
    for name, url in images:
        out = os.path.join(OUT, name)
        if os.path.exists(out) and os.path.getsize(out) > 30_000:
            results.append((name, os.path.getsize(out), "SKIP-exists", url))
            continue
        try:
            data = fetch(url)
            img = Image.open(io.BytesIO(data))
            if img.mode != "RGB":
                img = img.convert("RGB")
            img.thumbnail((1400, 1400), Image.LANCZOS)
            img.save(out, "JPEG", quality=80, optimize=True)
            results.append((name, os.path.getsize(out), "OK", url))
        except Exception as e:
            results.append((name, 0, f"FAIL {e}", url))

    print(f"\n{'STATUS':14} {'SIZE':>10}  FILE")
    print("-" * 70)
    for name, size, status, _ in results:
        print(f"{status:14} {size:>10}  {name}")
    fails = [r for r in results if r[2].startswith("FAIL")]
    if fails:
        print(f"\n{len(fails)} failures — try alternate URLs:")
        for r in fails:
            print(" ", r[0], "<-", r[3])


if __name__ == "__main__":
    main()
