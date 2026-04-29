import urllib.request, os, sys
from PIL import Image
import io

OUT = os.path.dirname(os.path.abspath(__file__))

DOWNLOADS = [
    ("bradford_portrait.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/92/Williambradford_bw.jpg"),
    ("bradford_birthplace.jpg", "https://upload.wikimedia.org/wikipedia/commons/4/46/WilliamBradfordBirthplace.jpg"),
    ("leiden_hooglandse.jpg", "https://upload.wikimedia.org/wikipedia/commons/b/ba/20070617hooglandsekerk.jpg"),
    ("bradford_house_plymouth.jpg", "https://upload.wikimedia.org/wikipedia/commons/a/a0/Governor_Bradford%27s_house%2C_Plymouth.jpg"),
    ("of_plymouth_plantation_manuscript.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/54/Of_Plimoth_Plantation_First_1900.jpg"),
    ("mayflower_at_sea.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/9d/Copyrighted_and_Published_by_A_S_Burbank%2C_The_Mayflower_at_Sea_%28NBY_21340%29.jpg"),
    ("squanto_teaching_corn.png", "https://upload.wikimedia.org/wikipedia/commons/b/bc/Squantoteaching.png"),
    ("samoset_enters_plymouth.jpg", "https://upload.wikimedia.org/wikipedia/commons/2/20/A_popular_history_of_the_United_States_-_from_the_first_discovery_of_the_western_hemisphere_by_the_Northmen%2C_to_the_end_of_the_first_century_of_the_union_of_the_states%3B_preceded_by_a_sketch_of_the_%2814597125217%29.jpg"),
    ("massasoit_dallin.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/58/Massasoit%2C_KC_MO_-_detail.JPG"),
    ("embarkation_pilgrims_weir.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/94/Robert_Walter_Weir_-_Embarkation_of_the_Pilgrims_-_Google_Art_Project.jpg"),
    ("delfshaven_departure_willaerts.jpg", "https://upload.wikimedia.org/wikipedia/commons/d/dd/Het_vertrek_van_de_Pilgrims_uit_Delfshaven%2C_1620._A._Willaerts.jpg"),
]

UA = "Mozilla/5.0 (compatible; EduBot/1.0)"

for name, url in DOWNLOADS:
    out_path = os.path.join(OUT, name)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        # process via PIL
        img = Image.open(io.BytesIO(data))
        if img.mode in ("RGBA","P","LA"):
            img = img.convert("RGB")
        # resize max 1400
        w,h = img.size
        m = max(w,h)
        if m > 1400:
            ratio = 1400/m
            img = img.resize((int(w*ratio), int(h*ratio)), Image.LANCZOS)
        save_name = name.rsplit(".",1)[0] + ".jpg"
        save_path = os.path.join(OUT, save_name)
        # quality loop to stay under 600KB
        q = 85
        while q >= 50:
            img.save(save_path, "JPEG", quality=q, optimize=True)
            sz = os.path.getsize(save_path)
            if sz < 600*1024:
                break
            q -= 5
        if name != save_name and os.path.exists(out_path) and out_path != save_path:
            try: os.remove(out_path)
            except: pass
        print(f"OK {save_name}  {os.path.getsize(save_path)//1024} KB  ({img.size[0]}x{img.size[1]})")
    except Exception as e:
        print(f"FAIL {name}: {e}")
