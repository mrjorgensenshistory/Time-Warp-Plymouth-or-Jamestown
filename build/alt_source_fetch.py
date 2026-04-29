"""Alt-source fallback for images that Wikimedia 429'd.

For each missing image, tries multiple sources in priority order:
  1. Wikimedia thumbnail (direct)
  2. Wikimedia thumbnail via Wayback Machine snapshot
  3. Wikipedia REST API File endpoint (different CDN path)
  4. Bing Visual Search reverse-lookup (skipped — no auth)

Run this AFTER thumbnail_fetch.py to fill any remaining gaps.
"""
import os
import re
import time
import urllib.request
import urllib.error
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow needed: pip install Pillow")
    exit(1)

ROOT = Path(r"F:\Michael's\ACE\US History\Time-Warp-Plymouth-or-Jamestown\dist\images")
UA = "Mozilla/5.0 (compatible; TimeWarpEdu/1.0; mr.jorgensen@school.org)"

CHARACTERS = ["bradford", "massasoit", "powhatan", "squanto"]


def fetch(url, dest, timeout=30):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            if not data or len(data) < 5000:
                return False
            dest.write_bytes(data)
            return True
    except Exception:
        return False


def try_wayback(orig_url, dest):
    """Try Wayback Machine snapshot of the original Wikimedia URL."""
    # Get latest snapshot via availability API
    api = f"https://archive.org/wayback/available?url={orig_url}"
    try:
        req = urllib.request.Request(api, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as resp:
            import json
            data = json.loads(resp.read().decode("utf-8"))
            snapshot = data.get("archived_snapshots", {}).get("closest", {})
            if snapshot.get("available"):
                snap_url = snapshot["url"]
                # Use the raw image (id_/) variant of Wayback to skip the toolbar
                snap_url_raw = snap_url.replace("/web/", "/web/").replace("/http", "if_/http", 1)
                # Actually Wayback raw image format is `/web/TIMESTAMP/im_/URL`
                # Add im_ to the timestamp portion
                snap_url_raw = re.sub(r"/web/(\d+)/", r"/web/\1im_/", snap_url)
                if fetch(snap_url_raw, dest):
                    return True
                if fetch(snap_url, dest):
                    return True
    except Exception:
        pass
    return False


def parse_downloads(script_path):
    text = script_path.read_text(encoding="utf-8")
    pattern = re.compile(r'\(\s*"([^"]+\.(?:jpg|png|jpeg|gif))"\s*,\s*"(https://[^"]+)"\s*\)')
    return pattern.findall(text)


def to_thumb(url, w=1280):
    if "/thumb/" in url:
        return url
    m = re.match(r"(https://upload\.wikimedia\.org/wikipedia/commons/)([0-9a-f]/[0-9a-f]{2})/([^/?]+)$", url)
    if not m:
        return url
    base, h, fn = m.groups()
    ext = fn.lower().rsplit(".", 1)[-1] if "." in fn else ""
    if ext in ("svg",):
        thumb = f"{w}px-{fn}.png"
    elif ext in ("tif", "tiff"):
        thumb = f"lossy-page1-{w}px-{fn}.jpg"
    else:
        thumb = f"{w}px-{fn}"
    return f"{base}thumb/{h}/{fn}/{thumb}"


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
    total_missing = 0
    total_recovered = 0
    for char in CHARACTERS:
        char_dir = ROOT / char
        script = char_dir / "_fetch2.py"
        if not script.exists():
            continue
        downloads = parse_downloads(script)
        missing = []
        for filename, url in downloads:
            dest = char_dir / filename
            if not dest.exists() or dest.stat().st_size < 5000:
                missing.append((filename, url))
        if not missing:
            print(f"[skip] {char}: all images present")
            continue
        print(f"\n=== {char} ({len(missing)} missing) ===")
        total_missing += len(missing)
        for filename, orig_url in missing:
            dest = char_dir / filename
            # Try thumbnail again (may have cooled down)
            thumb = to_thumb(orig_url)
            print(f"  trying thumb: {filename}", end=" ")
            if fetch(thumb, dest):
                compress(dest)
                print(f"OK ({dest.stat().st_size//1024}KB)")
                total_recovered += 1
                time.sleep(4)
                continue
            print("FAIL — trying Wayback", end=" ")
            if try_wayback(thumb, dest):
                compress(dest)
                print(f"OK via Wayback ({dest.stat().st_size//1024}KB)")
                total_recovered += 1
                time.sleep(3)
                continue
            print("FAIL — trying Wayback on original", end=" ")
            if try_wayback(orig_url, dest):
                compress(dest)
                print(f"OK via Wayback-orig ({dest.stat().st_size//1024}KB)")
                total_recovered += 1
                time.sleep(3)
                continue
            print("ALL SOURCES FAILED")
            time.sleep(2)
    print(f"\nTotal missing: {total_missing}  Recovered: {total_recovered}")


if __name__ == "__main__":
    main()
