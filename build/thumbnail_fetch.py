"""Unified Wikimedia thumbnail downloader.

Reads all 4 character _fetch2.py scripts, extracts URLs, converts each
to its 1280px thumbnail form (Wikimedia's high-volume-friendly path),
downloads only files that don't already exist on disk, throttles 5s
between requests, compresses to under 600KB.

Usage:  python thumbnail_fetch.py
"""
import os
import re
import sys
import time
import urllib.request
import urllib.error
from io import BytesIO
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow not installed. Run: pip install Pillow")
    sys.exit(1)

ROOT = Path(r"F:\Michael's\ACE\US History\Time-Warp-Plymouth-or-Jamestown\dist\images")
UA = "Mozilla/5.0 (compatible; TimeWarpEdu/1.0; mr.jorgensen@school.org) educational use Wikimedia"

CHARACTERS = ["bradford", "massasoit", "powhatan", "squanto"]


def to_thumbnail_url(orig_url: str, width: int = 1280) -> str:
    """Convert a Wikimedia upload URL to its 1280px thumbnail variant.

    Original: https://upload.wikimedia.org/wikipedia/commons/X/XY/Filename.jpg
    Thumb:    https://upload.wikimedia.org/wikipedia/commons/thumb/X/XY/Filename.jpg/1280px-Filename.jpg

    PNG/SVG variants get .png appended.
    """
    if "/thumb/" in orig_url:
        # already a thumbnail URL — leave as-is
        return orig_url
    m = re.match(r"(https://upload\.wikimedia\.org/wikipedia/commons/)([0-9a-f]/[0-9a-f]{2})/([^/?]+)$", orig_url)
    if not m:
        return orig_url  # unknown shape, return original
    base, hash_dir, filename = m.group(1), m.group(2), m.group(3)
    # Wikimedia thumbnail format requires the filename appended after /thumb path
    ext_lower = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    if ext_lower in ("svg",):
        # SVGs render to PNG thumbnails
        thumb_filename = f"{width}px-{filename}.png"
    elif ext_lower in ("tif", "tiff"):
        # TIFFs render to JPG thumbnails
        thumb_filename = f"lossy-page1-{width}px-{filename}.jpg"
    else:
        thumb_filename = f"{width}px-{filename}"
    return f"{base}thumb/{hash_dir}/{filename}/{thumb_filename}"


def parse_downloads_from_script(script_path: Path):
    """Extract (filename, URL) tuples from a _fetch2.py file's DOWNLOADS list."""
    text = script_path.read_text(encoding="utf-8")
    # Match `("filename.jpg", "https://...")`
    pattern = re.compile(r'\(\s*"([^"]+\.(?:jpg|png|jpeg|gif))"\s*,\s*"(https://[^"]+)"\s*\)')
    return pattern.findall(text)


def fetch_one(url: str, dest: Path, timeout: int = 30):
    """Download one URL to disk. Returns (status, size, message)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            if not data or len(data) < 2000:
                return ("fail", len(data), "tiny response (likely error page)")
            dest.write_bytes(data)
            return ("ok", len(data), "downloaded")
    except urllib.error.HTTPError as e:
        return ("fail", 0, f"HTTP {e.code}")
    except Exception as e:
        return ("fail", 0, str(e)[:80])


def compress(path: Path, max_dim: int = 1400):
    try:
        img = Image.open(path)
        if img.mode in ("RGBA", "P", "LA"):
            img = img.convert("RGB")
        if img.size[0] > max_dim or img.size[1] > max_dim:
            img.thumbnail((max_dim, max_dim), Image.LANCZOS)
        # Always save as JPEG for consistency (some thumbnails come as PNG with alpha)
        out = path.with_suffix(".jpg")
        img.save(out, "JPEG", quality=80, optimize=True)
        if out != path and path.exists():
            path.unlink()
        return out.stat().st_size
    except Exception as e:
        return -1


def main():
    total_attempted = 0
    total_ok = 0
    total_fail = 0

    for char in CHARACTERS:
        char_dir = ROOT / char
        script = char_dir / "_fetch2.py"
        if not script.exists():
            print(f"[skip] {char}: no _fetch2.py")
            continue
        downloads = parse_downloads_from_script(script)
        print(f"\n=== {char} ({len(downloads)} URLs) ===")

        for filename, orig_url in downloads:
            dest = char_dir / filename
            # Skip if already a real image on disk
            if dest.exists() and dest.stat().st_size > 5000:
                print(f"  [skip-exists] {filename} ({dest.stat().st_size // 1024}KB)")
                continue

            thumb_url = to_thumbnail_url(orig_url, 1280)
            total_attempted += 1
            status, size, msg = fetch_one(thumb_url, dest)
            if status == "ok":
                # Compress + finalize
                final_size = compress(dest)
                size_kb = (final_size if final_size > 0 else size) // 1024
                print(f"  [ok] {filename} ({size_kb}KB)")
                total_ok += 1
            else:
                print(f"  [FAIL] {filename}: {msg}")
                total_fail += 1
                # Clean up empty/tiny file
                if dest.exists() and dest.stat().st_size < 5000:
                    dest.unlink()
            time.sleep(5)  # 5s between requests — friendly to Wikimedia

    print(f"\n=== SUMMARY ===")
    print(f"Attempted: {total_attempted}  OK: {total_ok}  Failed: {total_fail}")


if __name__ == "__main__":
    main()
