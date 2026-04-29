import urllib.request, ssl, os
from PIL import Image
import io

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

OUT = os.path.dirname(os.path.abspath(__file__))

images = [
    ("powhatan_smith_map.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/9e/Powhatan_john_smith_map.jpg"),
    ("smith_taking_pamunkey.jpg", "https://upload.wikimedia.org/wikipedia/commons/0/03/John_Smith_taking_the_King_of_Pamavnkee_prisoner_-_etching.jpg"),
    ("coronation_powhatan.jpg", "https://upload.wikimedia.org/wikipedia/commons/8/8f/The_Coronation_of_Powhatan_John_Gadsby_Chapman.jpeg"),
    ("pocahontas_van_de_passe.jpg", "https://upload.wikimedia.org/wikipedia/commons/b/b4/Pocahontas_by_Simon_van_de_Passe_%281616%29.png"),
    ("pocahontas_saves_smith.jpg", "https://upload.wikimedia.org/wikipedia/commons/a/a9/Pocahontas_saving_the_life_of_Capt._John_Smith_-_New_England_Chromo._Lith._Co._LCCN95507872.jpg"),
    ("abduction_pocahontas.jpg", "https://upload.wikimedia.org/wikipedia/commons/2/26/Abduction_of_Pocahontas_Engraving_by_Johann_Theodore_de_Bry.jpg"),
    ("marriage_pocahontas.jpg", "https://upload.wikimedia.org/wikipedia/commons/8/8f/Marriage_of_Pocahontas.png"),
    ("jamestown_ships.jpg", "https://upload.wikimedia.org/wikipedia/commons/3/38/JamestownShips.jpg"),
    ("massacre_1622_merian.jpg", "https://upload.wikimedia.org/wikipedia/commons/7/7c/Matth%C3%A4us_Merian_d%C3%86%2C_S%C3%A5ledes_blev_ogs%C3%A5_denne_fred_brudt_p%C3%A5_grund_af_bedrag%2C_KKSgb10894-5%2C_Statens_Museum_for_Kunst.jpg"),
    ("algonquin_village_debry.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/97/De_Bry_-_America_Part_1_-_Algonquin_village_-_HLABG.png"),
    # try Secoton variants
    ("village_secoton.jpg", "https://upload.wikimedia.org/wikipedia/commons/0/04/Village_of_Secoton_Theodor_de_Bry_1590.jpg"),
    ("smith_1612_map.jpg", "https://upload.wikimedia.org/wikipedia/commons/4/4a/Smith_Virginia_Map.JPG"),
]

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 EduFetch"})
    return urllib.request.urlopen(req, context=ctx, timeout=60).read()

results = []
for name, url in images:
    try:
        data = fetch(url)
        # Open with PIL, resize, save jpg q80
        img = Image.open(io.BytesIO(data))
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.thumbnail((1400, 1400), Image.LANCZOS)
        out = os.path.join(OUT, name)
        img.save(out, "JPEG", quality=80, optimize=True)
        size = os.path.getsize(out)
        results.append((name, size, "OK", url))
    except Exception as e:
        results.append((name, 0, f"FAIL {e}", url))

for r in results:
    print(r)
