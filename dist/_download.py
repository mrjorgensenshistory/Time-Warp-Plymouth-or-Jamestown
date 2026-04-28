"""
Music Hunter download script for Time-Warp-Plymouth-or-Jamestown.
Pulls royalty-free / CC-BY tracks from incompetech.com (Kevin MacLeod)
and Pixabay CDN where direct media URLs are known.
Run: python _download.py [tutorial|all]
"""
import os
import sys
import urllib.request
import urllib.error
import ssl

# Allow self-signed/older TLS just in case
ctx = ssl.create_default_context()
ctx.check_hostname = True

ROOT = os.path.dirname(os.path.abspath(__file__))

JOBS = {
    # PRIORITY 1: Roanoke tutorial — eerie ambient, no drum.
    # Kevin MacLeod "Anguish" is a sparse haunting bed.
    # Backup: "Sad Cyclops" / "Mesmerize" / "Phantom from Space"
    "tutorial/tutorial_main.mp3": [
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Anguish.mp3",
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Mesmerize.mp3",
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Phantom%20from%20Space.mp3",
    ],

    # PRIORITY 2: Hub — storm + atlantic shanty bed
    "hub/main.mp3": [
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Sneaky%20Adventure.mp3",
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Constance.mp3",
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Long%20Note%20Two.mp3",
    ],
    "hub/quiz_bed.mp3": [
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Long%20Note%20One.mp3",
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Hidden%20Past.mp3",
    ],

    # PRIORITY 3: Smith — swashbuckling adventure orchestral
    "smith/smith_main.mp3": [
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Hitman.mp3",
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Impact%20Andante.mp3",
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/The%20Pyre.mp3",
    ],

    # PRIORITY 4: Rolfe — Spanish/Latin guitar
    "rolfe/rolfe_main.mp3": [
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Spanish%20Summer.mp3",
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Mexican%20Plaza.mp3",
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Latin%20Industries.mp3",
    ],

    # PRIORITY 5: Powhatan — cedar drum + low flute, dignified
    # Kevin's catalog leans cinematic; "Tabuik" and "Marty Gots a Plan" feel wrong.
    # Better: "Long Note Two" + flute layer. We'll try "Constance Variation" or "Heavy Heart".
    "powhatan/powhatan_main.mp3": [
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Heavy%20Heart.mp3",
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Long%20Note%20Three.mp3",
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Constance.mp3",
    ],

    # PRIORITY 6: Bradford — jazz piano trio, Vince Guaraldi cousin
    "bradford/bradford_main.mp3": [
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Acid%20Jazz.mp3",
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Bossa%20Antigua.mp3",
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Dewdrop%20Fantasy.mp3",
    ],

    # PRIORITY 7: Squanto — wood flute solo, dignified
    "squanto/squanto_main.mp3": [
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Meditation%20Impromptu%2003.mp3",
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Awkward%20Meeting.mp3",
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Daydream%20in%20Blue.mp3",
    ],

    # PRIORITY 8: Massasoit — communal drum + fire-circle
    "massasoit/massasoit_main.mp3": [
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Long%20Note%20Four.mp3",
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Magic%20Forest.mp3",
        "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Heartbreaking.mp3",
    ],
}

# SFX — try Pixabay direct CDN, fall back to incompetech
SFX = {
    "sfx/cannon_distant.mp3": [
        "https://cdn.pixabay.com/download/audio/2022/03/15/audio_d3a32a7ea1.mp3",
    ],
    "sfx/organ_chord.mp3": [
        "https://cdn.pixabay.com/download/audio/2022/04/14/audio_a82e7b7e16.mp3",
    ],
    "sfx/cedar_drum_3beats.mp3": [
        "https://cdn.pixabay.com/download/audio/2021/08/04/audio_c8c8a73467.mp3",
    ],
    "sfx/dinner_bell.mp3": [
        "https://cdn.pixabay.com/download/audio/2022/03/24/audio_71c50b5fd5.mp3",
    ],
    "sfx/wind_howl.mp3": [
        "https://cdn.pixabay.com/download/audio/2021/09/01/audio_b2c8e98f0d.mp3",
    ],
}

def fetch(out_relpath, urls):
    out_path = os.path.join(ROOT, out_relpath)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (compatible; MusicHunter/1.0)"
            })
            with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
                data = r.read()
            if len(data) < 50_000:
                print(f"  TOO SMALL ({len(data)} bytes) — try next: {url}")
                continue
            # Check it's not HTML
            head = data[:200].lower()
            if b"<html" in head or b"<!doctype" in head:
                print(f"  GOT HTML — try next: {url}")
                continue
            with open(out_path, "wb") as f:
                f.write(data)
            print(f"  OK {out_relpath} ({len(data)//1024} KB) <- {url}")
            return True
        except urllib.error.HTTPError as e:
            print(f"  HTTP {e.code} — try next: {url}")
        except urllib.error.URLError as e:
            print(f"  URL ERR {e.reason} — try next: {url}")
        except Exception as e:
            print(f"  ERR {type(e).__name__}: {e} — try next: {url}")
    print(f"  FAILED {out_relpath} (all candidates exhausted)")
    return False


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "tutorial"
    if mode == "tutorial":
        targets = {"tutorial/tutorial_main.mp3": JOBS["tutorial/tutorial_main.mp3"]}
    elif mode == "all":
        targets = dict(JOBS)
        targets.update(SFX)
    elif mode == "music":
        targets = dict(JOBS)
    elif mode == "sfx":
        targets = dict(SFX)
    else:
        print("Usage: _download.py [tutorial|music|sfx|all]")
        return
    for rel, urls in targets.items():
        print(f"=> {rel}")
        fetch(rel, urls)


if __name__ == "__main__":
    main()
