"""Fetch Smith fort/work/stockade scene images.

Michael flagged: too many pics of just John Smith's face, nothing about
the work, the fort, the stockades. These URLs were verified live on
Wikipedia article pages, so they're real (unlike guessed Special:FilePath).
"""
import time
import urllib.request
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow required")
    exit(1)

ROOT = Path(r"F:\Michael's\ACE\US History\Time-Warp-Plymouth-or-Jamestown\dist\images\smith")
UA = "Mozilla/5.0 (compatible; TimeWarpEdu/1.0; mr.jorgensen@school.org)"

# Verified-live Wikipedia article images — full-resolution upload paths
JOBS = [
    ("jamestown_fort_interior.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/e/e1/Jamestown_Settlement_fort_interior.jpg"),
    ("jamestown_barracks_reconstruction.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/8/88/JamestownBarracksReconstruction.jpg"),
    ("jamestown_recreated_house.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/5/51/Jamestown_Settlement_(48813195).jpg"),
    ("jamestown_ships_replica.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/e/ee/Line0771_-_Flickr_-_NOAA_Photo_Library.jpg"),
    ("jamestown_exposition_hall.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/0/0d/Jamestown_Virginia_350th_Exposition_Hall_(5209651593).jpg"),
]


def to_thumb(url, w=1280):
    """Convert /commons/X/YZ/file.jpg → /commons/thumb/X/YZ/file.jpg/1280px-file.jpg"""
    import re
    m = re.match(r"(https://upload\.wikimedia\.org/wikipedia/commons/)([0-9a-f])/([0-9a-f]{2})/([^/?]+)$", url)
    if not m:
        return url
    base, h1, h2, fn = m.groups()
    return f"{base}thumb/{h1}/{h2}/{fn}/{w}px-{fn}"


def fetch(url, dest):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            if not data or len(data) < 10000:
                return False, len(data)
            dest.write_bytes(data)
            return True, len(data)
    except Exception as e:
        return False, str(e)[:80]


def compress(path, max_dim=1400):
    try:
        img = Image.open(path)
        if img.mode in ("RGBA", "P", "LA"):
            img = img.convert("RGB")
        if img.size[0] > max_dim or img.size[1] > max_dim:
            img.thumbnail((max_dim, max_dim), Image.LANCZOS)
        img.save(path, "JPEG", quality=82, optimize=True)
        return path.stat().st_size
    except Exception as e:
        return -1


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    ok = fail = 0
    for filename, url in JOBS:
        dest = ROOT / filename
        if dest.exists() and dest.stat().st_size > 10000:
            print(f"  [skip] {filename}")
            continue
        thumb = to_thumb(url)
        success, info = fetch(thumb, dest)
        if not success:
            print(f"  [retry full] {filename} (thumb said: {info})")
            success, info = fetch(url, dest)
        if success:
            sz = compress(dest)
            print(f"  [OK] {filename} ({sz//1024}KB)")
            ok += 1
        else:
            print(f"  [FAIL] {filename}: {info}")
            fail += 1
            if dest.exists() and dest.stat().st_size < 10000:
                dest.unlink()
        time.sleep(5)
    print(f"\nOK: {ok}  FAIL: {fail}")


if __name__ == "__main__":
    main()
