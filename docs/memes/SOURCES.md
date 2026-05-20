# Cutscene GIF Sources & Attribution

**Time Warp: Plymouth or Jamestown** &mdash; ACE 8th-grade US History
Compiled 2026-04-28. All URLs verified to return valid `image/gif` content on this date.

These animated GIFs are embedded directly from Tenor's CDN as fair-use commentary in an educational classroom context (17 U.S.C. &sect;107). The original works belong to their respective rights-holders, listed below. The Time Warp does not redistribute or self-host these clips; it links to Tenor's hosted copies.

## Attribution table

| Cutscene | Original work | Rights-holder | Year | Use in game |
|---|---|---|---|---|
| Yzma "Wrong Lever" | *The Emperor's New Groove* | Walt Disney Pictures | 2000 | Universal dumb-choice gameover (most-used cutscene) |
| Bobby Boucher tackle | *The Waterboy* | Touchstone Pictures / Walt Disney Studios | 1998 | Physical-confrontation, ambush, raid-loss fails |
| Terry Tate, Office Linebacker | *Terry Tate: Office Linebacker* | Reebok / Rawson Marshall Thurber | 2003 | Lazy / unprepared / skipped-the-prep fails |
| Tulio &amp; Miguel scheming | *The Road to El Dorado* | DreamWorks Animation | 2000 | "You got conned" fails &mdash; broken treaty / fake promise |
| Rickroll cherry | *Never Gonna Give You Up* music video | Rick Astley / RCA Records | 1987 | Universal 3-second outro on comedic gameovers only |

## Embed source

All five clips are embedded from **Tenor** (https://tenor.com), Google's GIF platform. Tenor maintains its own licensing arrangements with rights-holders for hosted content. The Time Warp uses direct `media.tenor.com` URLs in standard `<img>` tags &mdash; no Tenor SDK, no tracking pixels, no third-party JavaScript.

Direct URLs are listed in `manifest.json` alongside this file.

## Tone rule (locked from THEME &sect;4)

These GIFs are **prohibited** on Native-character TERMINAL endgame cards:

- Powhatan's terminal card
- Squanto's terminal card
- Massasoit's terminal card

Those cards use period-art portraits with a clean cedar-drum or wood-flute tail &mdash; no comedic cast, no Rickroll cherry. Universal cast (Yzma, Bobby, Terry Tate, Tulio/Miguel) **is** allowed on early-route minor wrong-choice fails for those characters; the dignity rule applies only to terminal endgame cards. See THEME &sect;4 "Symmetric brutality rule" and &sect;6 "Cherry-on-top rule" for full text.

## Fallbacks

Each entry in `manifest.json` includes 2&ndash;3 fallback URLs in case Tenor rotates or removes a primary URL. If a primary URL 404s in classroom playtest, swap to the first fallback and re-verify. The build pipeline should periodically re-check all URLs (a quick HEAD-request script in `dist/_check_memes.py` would be a good follow-up).

## Educational fair-use rationale

- **Purpose:** non-commercial educational use in a single classroom of 8th-grade US History students.
- **Nature:** transformative commentary &mdash; the GIFs annotate historical decisions and consequences, not entertainment for its own sake.
- **Amount:** 1&ndash;3 second clip per use, embedded (not redistributed).
- **Market effect:** none &mdash; classroom embedding does not substitute for the original work.

If a rights-holder objects to a specific clip, swap to the fallback URL or remove the cutscene entirely. Email contact: see project README.
