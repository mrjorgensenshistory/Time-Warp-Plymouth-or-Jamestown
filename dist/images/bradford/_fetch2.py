"""Fetch additional Wikimedia Commons period images for Bradford route.

Targets the 18 still-reused slides on bradford_route.md so each scene gets
unique period art. Images chosen for the Bradford voice: quiet, devout,
chronicler — 19th-c history paintings, period engravings, and Stuart-era
portraits. No heroic-lithograph chest-thumping.

Run from anywhere — paths are absolute. Outputs JPEGs into this directory.
"""
import urllib.request, os, io
from PIL import Image

OUT = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (compatible; EduBot/1.0; +https://example.org)"

# (filename, wikimedia upload URL)
DOWNLOADS = [
    # --- ENGLAND, SCROOBY, YORKSHIRE 1606 ---
    ("scrooby_village.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/c/c4/Scrooby_village_addison.PNG"),
    ("scrooby_manor_farm.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/0/06/Former_farmhouse_at_Manor_Farm_-_geograph.org.uk_-_4259585.jpg"),
    ("scrooby_st_wilfrid.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/8/89/St_Wilfrid%27s_Church%2C_Scrooby_-_geograph.org.uk_-_7384566.jpg"),
    ("king_james_i_decritz.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/5/53/John_De_Critz_James_I_of_England_c._1605.jpg"),

    # --- LEIDEN / HOLLAND 1608-1620 ---
    ("leiden_pieterskerk_postcard.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/4/4a/Leiden_Pieterskerk_postcard.jpg"),
    ("leiden_wool_swanenburg.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/d/d5/Isaac_Claesz._Van_Swanenburg_Washing_the_Skins_and_Grading_the_Wool.jpg"),
    ("pilgrims_going_to_church_boughton.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/3/3b/Pilgrims_Going_To_Church.jpg"),

    # --- DEPARTURE / SPEEDWELL / EMBARKATION ---
    ("delfshaven_willaerts.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/d/dd/Het_vertrek_van_de_Pilgrims_uit_Delfshaven%2C_1620._A._Willaerts.jpg"),
    ("embarkation_pilgrims_weir.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/9/94/Robert_Walter_Weir_-_Embarkation_of_the_Pilgrims_-_Google_Art_Project.jpg"),

    # --- MAYFLOWER VOYAGE / CAPE COD ---
    ("mayflower_at_sea_drawing.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/0/0a/The_Mayflower_at_sea.jpg"),
    ("mayflower_in_plymouth_harbor_halsall.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/7/7a/Mayflower_in_Plymouth_Harbor%2C_by_William_Halsall.jpg"),

    # --- MAYFLOWER COMPACT ---
    ("compact_signing_ferris.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/6/63/The_Mayflower_Compact_1620_cph.3g07155.jpg"),
    ("compact_bradford_handwriting.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/2/2c/Mayflower_Compact_Bradford.jpg"),

    # --- LANDING / FIRST WINTER / DEATHS ---
    ("landing_pilgrims_bacon.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/2/26/The_Landing_of_the_Pilgrims_%281877%29_by_Henry_A._Bacon.jpg"),
    ("landing_pilgrims_lucy.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/c/c5/Landing_of_the_Pilgrims%2C_by_Charles_Lucy.tiff"),
    ("provincetown_lost_pilgrims_memorial.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/d/d3/Provincetown_memorial_to_Lost_Pilgrims.JPG"),

    # --- SAMOSET / SQUANTO / MASSASOIT ---
    ("samoset_interview.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/c/cd/Interview_of_Samoset_with_the_Pilgrims.jpg"),
    ("squanto_corn_prospered.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/2/2c/Squantohowwellthecornprospered.png"),
    ("massasoit_carver_meeting.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/0/0d/Meeting_of_Governor_Carver_and_Massasoit_-_drawn_by_H.L._Stevens_%3B_eng%27d._by_Augustus_Robin%2C_N.Y._LCCN89707285.jpg"),

    # --- THANKSGIVING / FIRST HARVEST ---
    ("thanksgiving_brownscombe_1914.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/1/1a/Thanksgiving-Brownscombe.jpg"),
    ("thanksgiving_plymouth_1925.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/1/13/Thanksgiving_at_Plymouth%2C_1925%2C_Brownscombe.jpg"),
    ("first_thanksgiving_ferris.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/0/0a/The_First_Thanksgiving_Jean_Louis_Gerome_Ferris.jpg"),

    # --- BRADFORD / CHRONICLE / LATE LIFE ---
    ("bradford_portrait.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/9/92/Williambradford_bw.jpg"),
    ("of_plymouth_plantation_manuscript.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/5/54/Of_Plimoth_Plantation_First_1900.jpg"),
    ("bradford_signature.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/8/8b/William_Bradford_signature.svg"),

    # --- 1630 MASSACHUSETTS BAY FLEET ---
    ("winthrop_fleet_arrival.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/5/5d/Winthrop%27s_Fleet_from_pp93_of_The_history_of_the_American_Episcopal_Church%2C_1587-1883_%281885%29.jpg"),

    # --- PLYMOUTH ECONOMY / TOWN / FORT ---
    ("plymouth_colony_seal.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/0/03/Plymouth_Colony_seal.png"),
    ("hubbard_map_1677.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/3/30/Hubbard_map_1677.JPG"),
    ("plymouth_law_book.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/4/4f/Plymouth_law_book.jpg"),
]


def fetch():
    for name, url in DOWNLOADS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read()
            img = Image.open(io.BytesIO(data))
            if img.mode in ("RGBA", "P", "LA"):
                img = img.convert("RGB")
            elif img.mode != "RGB":
                img = img.convert("RGB")
            w, h = img.size
            m = max(w, h)
            if m > 1400:
                ratio = 1400 / m
                img = img.resize((int(w*ratio), int(h*ratio)), Image.LANCZOS)
            save_path = os.path.join(OUT, name)
            q = 85
            while q >= 50:
                img.save(save_path, "JPEG", quality=q, optimize=True)
                sz = os.path.getsize(save_path)
                if sz < 600*1024:
                    break
                q -= 5
            print(f"OK {name}  {os.path.getsize(save_path)//1024} KB  ({img.size[0]}x{img.size[1]})")
        except Exception as e:
            print(f"FAIL {name}: {e}")


if __name__ == "__main__":
    fetch()
