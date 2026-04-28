# Time Warp: Plymouth or Jamestown — Theme Spec

**Audience:** 8th grade US History (ACE charter, Mr. Jorgensen's class)
**Series slot:** Standalone Time Warp — **OUTSIDE the Roughton I–VII canon.** No Roughton credit on title screen or character pages. A single thank-you reference is permitted on the credits page only.
**Era covered:** 1607–1640, founding of the first permanent English colonies in North America.
**Visual baseline:** https://mrjorgensenshistory.github.io/Time-Warp-IV-Civil-War/ (engine pattern only — visual mood is its own beast, see §2)
**Public deploy target:** GitHub Pages (royalty-free assets only)
**Educational goal:** Students leave with concrete, comparable evidence to write an ARE-paragraph thesis on **three differences between Plymouth and Jamestown**: motivation, settler type, geography→economy, Native relationship, disease/famine.

---

## 1. Theme Spine

**Elevator pitch:** *Two boats. Two reasons. Two endings. Pick a side, pick a person, find out why one English colony ate its neighbors and the other one ate corn.*

**Mood / tone.** This is not Conquest's swashbuckle. This is colder, quieter, more morally serious — a survival drama with comedy windows, not a comedy with survival drama. Ships arrive in winter. People die of disease. People take food at gunpoint. People share food across a language barrier. People eventually fight each other over land. The game tells what happened, in plain language, from the perspective of the person who lived it.

The visual mood is **1995 Disney *Pocahontas*** for Jamestown (water, leaves, wind, "Colors of the Wind" energy) and a **hybrid** for Plymouth: *A Charlie Brown Thanksgiving* (1973) Vince Guaraldi piano warmth on the Pilgrim slides, *Brother Bear* respectful Native scoring on the Squanto and Massasoit slides. The hybrid is intentional — when the camera is on the Pilgrim, you hear hearth-and-home jazz piano; when the camera is on the Wampanoag, you hear cedar drum and flute. The character is the scoring rule.

**The philosophical frame, locked.** "Either side would have done the same to the other if they could have." Both sides did what they had to do to survive. The game does not paint colonists as bad white men. The game does not paint Natives as noble savages. The game teaches the **choices** people made under survival pressure, and the **consequences** that followed for centuries. Powhatan and Massasoit narrate their own decline in their own voices — they are not lectured *over* by a moralizing narrator. Settlers narrate their own famine in their own voices. The student does the moral math.

**The comedy is windowed, not constant.** Cutscene game-overs still get the Bobby Boucher / Yzma / Rickroll cherry — 8th graders need the candy — but the slides themselves are not jokey. We earn the laughs by holding the history straight first. The ratio is roughly **70% straight history, 30% comedic cutscene release**.

**Why this matters for 8th graders.** They will not sit through 30 sober slides. They WILL sit through a story where they pick a person, that person lives or dies, and at the end they can write a paragraph that says "Jamestown was X, Plymouth was Y, here's the evidence" — and feel like they earned it.

---

## 1.5. Voice & Immersion (HARD RULE)

**Time Warps are GAMES, not presentations.** The slide voice must be strict first-person — the player IS the character. This is a non-negotiable constraint that overrides any other writing instinct.

### Locked rules

1. **Strict first-person, present tense.** "You wade ashore. The salt water stings your cuts. You can see the stockade through the trees." NOT "Smith waded ashore." NOT "imagine what it must have felt like."
2. **NO Brain Snack breaks.** Brain Snacks are a presentation device — a mid-slideshow PvZ-template audio break for *teacher-led* slideshows. They break gameplay flow and pull the player out of character. They do not appear in this Time Warp. If any earlier draft references a Brain Snack, remove it.
3. **NO meta-analogies in slide copy.** No "Jamestown was like a frat house," no "imagine the colonies as teenagers," no "this is just like when…" Those are teacher analogies for lesson planning. They MUST NOT appear in slide text. The player lives the story; they do not watch a teacher compare it to something.
4. **NO author intrusion / narrator summary.** History is taught through the consequences of the player's choices, not through teacher voice-overs. No "as you can see, this shows that…" No "the lesson here is…" No "historians believe…" The character's lived experience IS the lesson.
5. **In-world devices are fine.** Stacking review slides, growing timeline bars, ship's log entries, journal pages — these all read as *the player's own chronicle*, not as 4th-wall teacher voice. Use them freely.
6. **The theme is the FRAME, not the content.** Disney *Pocahontas* visual mood and *Charlie Brown* audio cues set tone and atmosphere. They never overwrite historical voice. A slide can *feel* like Vince Guaraldi piano without the slide *text* mentioning Charlie Brown. Pop culture is the wallpaper, not the wallpaper's text.

### What the PPTX writer should hear

If a slide draft contains the words "imagine," "it's like," "just as," "similar to," "you can think of this as," "the lesson is," or any third-person past-tense narration of the player character, **rewrite it.** The player is the character. The character is doing the thing right now.

---

## 1.6. Engine Conventions Borrowed from the Revolution Unit

The Liberty or Death (Revolution unit) game is the depth template Michael wants to match. Plymouth-or-Jamestown borrows four conventions from that engine. These are the depth signals that separate a Time Warp from a slideshow.

### 1. Growing timeline bar (1607–1640) — REQUIRED

A persistent strip across the bottom of every story slide that **accumulates events as the player makes decisions**. Every character's storyline ticks events onto the *same* shared timeline shape (1607 — Jamestown founded; 1619 — first enslaved Africans brought to Virginia; 1620 — Mayflower lands; 1621 — first Thanksgiving; 1622 — Powhatan uprising; 1636 — Pequot War; etc.). By the end of any single route, the player sees their character's life across the period — and on replay with a different character, the bar fills in differently.

This is the **#1 depth signal** in the engine. It is the in-world "ship's log / chronicle" for the player and reads as immersive (not 4th-wall teacher voice). Roanoke tutorial seeds it with `1587 / 1590` events before the hub.

### 2. Stacking review slide at end of each character's storyline — TENTATIVE (build it, flag for QC)

A visual summary slide at the end of each character's route showing their decisions and consequences stacked together — echoing the "snowball of causes" review pattern from the Revolution unit. The player sees the chain of choices that produced their ending.

**Status:** Build it. Flag it for Michael's QC review. He wants to see how it looks before committing — if it reads as in-world chronicle, it stays. If it feels like a pop quiz, it gets cut.

### 3. Sound-effect anchor moments — LOCKED

Specific sound cues tied to specific narrative beats. These are the anchor SFX; more can be layered per character, but these five are non-negotiable:

| Beat | Cue | Notes |
|---|---|---|
| Jamestown landing | **Cannon report** | Single distant cannon, period-appropriate. Smith / Rolfe routes. |
| Mayflower Compact signing | **Organ chord** | Single sustained low organ chord on the signature reveal. Bradford route. |
| Powhatan war council | **Cedar drum** | Slow ceremonial drum, three beats. Powhatan route. |
| First Thanksgiving | **Dinner-bell** | Bright bell tone on the food-shared reveal. Plymouth side (Bradford / Squanto / Massasoit). |
| Mayflower winter / death-toll slide | **Wind-howl** | Low howling wind, sparse. Bradford route — the half-the-ship-died moment. |

Music-hunter and SFX-hunter: source these CC0 / royalty-free. Loop or one-shot as appropriate. They sit ABOVE the music bed in the mix.

### 4. Theme is the FRAME, not the content — LOCKED

Disney *Pocahontas* visual mood and *Charlie Brown* audio cues set audio + atmosphere + tone. **History stays accurate.** Pop culture never overwrites historical voice. The Vince-Guaraldi-cousin piano under Bradford's first-winter slide makes the slide *feel* warm-and-melancholy; the slide's *text* still narrates the actual death toll in Bradford's actual voice. The frame is the lighting; the content is the script.

This is the same rule as §1.5 rule 6 (theme = frame, not content), restated here because it governs how the engine conventions assemble: the timeline bar, stacking review, and SFX anchors are all *in-world* devices, never theme-overlays masquerading as gameplay.

---

## 1.7. Character-Specific Timeline Anchors (REQUIRED for the writer)

Each character's route MUST tick these specific historical events onto the timeline bar in their own voice. Pre-1587 events are pre-revealed as "history John White / Smith / Squanto already knows." Post-arrival events are revealed only as the character lives them.

### Pre-revealed historical context (visible on every character's timeline from slide 1)

These read as "history everyone knows" — not the player's lived events. Dimmer styling on the timeline bar.

| Year | Event | Why it's on the bar |
|---|---|---|
| 1492 | Columbus reaches the Caribbean | The starting gun for European colonization |
| 1513 | Ponce de León reaches Florida | First European foot on what becomes the U.S. mainland |
| 1521 | Fall of the Aztecs (Cortés) | The Spanish gold model that drives Jamestown's "find gold" hopes |
| 1533 | Fall of the Incas (Pizarro) | More Spanish gold — sets the Virginia Company's expectations |
| 1565 | St. Augustine founded (Spanish, Florida) | First permanent European settlement on the continent. Predates Jamestown by 42 years. |

### Squanto music — Last of the Mohicans handling (parallel to Drake's special spec)

Michael flagged that the **Last of the Mohicans theme** ("Promentory" by Trevor Jones, 1992) would land hard for Squanto's route. It is COPYRIGHTED. Same handling pattern as Drake's actual rap tracks in Conquest:

- **Public deploy (`squanto.html`):** Royalty-free **uilleann pipes / Native flute / cedar drum** track. Carries the same sparse, melancholy, dignified energy without the legal exposure. Search: `uilleann pipes lament cc0`, `native american flute slow royalty free`, `pixabay celtic pipes mourning`.
- **Classroom-only variant (`squanto_classroom.html`, NEVER PUSHED):** Real "Promentory" track. Played live in Michael's classroom under **17 U.S.C. §110(1)** face-to-face teaching exception. Same gitignore + pre-commit-hook discipline as Drake's classroom variant in Conquest.
  - `.gitignore`: `squanto_classroom.html`, `audio/squanto_classroom/`
  - CI script: `grep -r "squanto_classroom"` and fail build if found
  - README pre-commit reminder

### Squanto (Tisquantum) — required timeline anchors for HIS route

Squanto's life is one of the most dramatic arcs in the period. His route MUST include these beats, lived in first-person:

| Year | Event | Voice notes |
|---|---|---|
| ~1585 | Born Patuxet, Wampanoag confederation | Established as the homeland — small fishing village, future site of Plymouth |
| 1605 | First taken by an English captain (briefly, brought to England then home) | NOT the famous capture; the warm-up. Establishes English contact |
| 1614 | **Captured by Thomas Hunt** with 26 other Patuxet/Wampanoag men | Hunt was supposed to be trading. He kidnapped them instead. Squanto's voice: "He shook our hands and put us in chains." |
| 1614–1615 | **Sold into slavery in Málaga, Spain** | Spanish friars buy him, refuse to enslave a baptized soul. He becomes their student — learns Spanish, religion, and most importantly that the English have rivals |
| 1615–1619 | Makes his way home — Spain → London → Newfoundland → Patuxet | Years lost crossing back. Learns English in London. Working passage on fishing ships. |
| 1616–1619 | **Plague decimates Patuxet** while he is away | Smallpox / leptospirosis epidemic kills ~90% of his people. He returns to find empty villages. |
| 1619 | **Squanto returns to Patuxet — finds it empty** | The single most devastating moment of his life. The reason he eventually helps the Pilgrims who land in 1620: there is literally no one left to come home to. |
| 1620 | Mayflower lands at the abandoned Patuxet site (now called Plymouth) | The colonists settle on his people's grave |
| 1621 | Teaches Pilgrims corn / fertilizer / fishing — first Thanksgiving | His most famous beat. Frame it as "I had no village left. They were what I had." |
| 1622 | **Dies of Indian fever** while guiding Bradford on a diplomatic trip | Per the THEME spec gameover catalog — dignified, "I taught them. They lived. I did not." |

**The educational point this teaches:** Squanto's "helping the Pilgrims" wasn't naïve goodwill or "noble savage" service. It was a pragmatic, traumatized survivor who had lost everything and found use in being a bridge. Both sides survival math — exactly the THEME tone bar.

### Other characters — anchors to be expanded by the writer

(Smith / Rolfe / Powhatan / Bradford / Massasoit each get their own anchor list when their writer agent spins up. Roanoke tutorial already locked: 1587 / 1588 / 1590.)

---

## 2. Visual Identity

### Fonts (Google Fonts)

```html
<link href="https://fonts.googleapis.com/css2?family=Bangers&family=Share+Tech&family=IM+Fell+English&family=IM+Fell+English+SC&display=swap" rel="stylesheet">
```

| Use | Font | Notes |
|---|---|---|
| Game title / hub headers / cutscene shouts | `Bangers` | Series consistency. All-caps comic-impact. |
| Body text on slides (PPTX-derived) | `Share Tech` | Matches Civil War / Conquest engine. |
| Decorative parchment / Mayflower Compact / "ye olde" overlays | `IM Fell English SC` | 17th-century period feel. **ONLY** for hub flair, compact reveal slide, character-card name plates. NOT in PPTX content. |
| Date stamps, journal entries, small UI | `IM Fell English` | Bradford-journal feel. Optional. |

**Rule:** Decorative fonts ONLY on hub, title screen, game-over headlines, and cutscene cards. PPTX-derived slides keep `Share Tech`. No exceptions.

### Color palette

The palette splits into a shared neutral ground plus a **Jamestown warm/southern** swatch and a **Plymouth cool/northern** swatch. The hub uses the neutrals; each character side uses its swatch.

| Role | Hex | Use |
|---|---|---|
| `bg-parchment` | `#f1e6c8` | Hub background, card backgrounds, scroll overlays |
| `bg-deep-atlantic` | `#0a1f3a` | Title screen, character-select overlay, stormy water |
| `ink` | `#1a1a1a` | All body text, button text on light bg |
| `bone-white` | `#fefefe` | Slide text-box fill, button text on dark bg |
| `overlay-dark` | `rgba(0,0,0,0.18)` | Subtle darken on background images |
| **Jamestown warm** | | |
| `jt-river-green` | `#3a5a3a` | Jamestown route accents — James River, Virginia forest |
| `jt-tobacco-gold` | `#b88a3e` | Rolfe accent, cash-crop highlights |
| `jt-blood-clay` | `#7a2e1f` | Game-over titles on Jamestown side, Virginia red soil |
| **Plymouth cool** | | |
| `pl-slate-blue` | `#3d5a78` | Plymouth route accents — North Atlantic, slate sky |
| `pl-hearth-orange` | `#c97a3b` | Hearth fire warmth, Charlie Brown autumn glow |
| `pl-pine-green` | `#1f3a2e` | Wampanoag accent, New England pine |

### Slide CSS (engine-consistent with Civil War / Conquest)

```css
.slide-textbox {
  background: #fefefe;
  border: 2px solid #000;
  border-radius: 0;          /* NO rounded corners */
  padding: 18px 22px;
  font-family: 'Share Tech', sans-serif;
  color: #1a1a1a;
  box-shadow: none;
}

/* Parchment overlay text (Mayflower Compact, journal entries, etc.) */
/* IMPORTANT: parchment text must render ABOVE non-bg images. */
/* z-index discipline: bg = 0, parchment image = 1, parchment TEXT = 10. */
.parchment-text {
  position: relative;
  z-index: 10;
  font-family: 'IM Fell English', serif;
}

.slide-button {
  display: block;
  width: 100%;
  background: #000;
  color: #fff;
  border: none;
  border-radius: 0;
  padding: 14px 0;
  font-family: 'Bangers', sans-serif;
  font-size: 1.4rem;
  letter-spacing: 1px;
  cursor: pointer;
  transition: background 120ms;
}
.slide-button:hover { background: #7a2e1f; } /* clay on hover */

.slide-bg {
  position: absolute; inset: 0;
  background-size: cover; background-position: center;
}
.slide-bg::after {
  content: ''; position: absolute; inset: 0;
  background: rgba(0,0,0,0.18);
  pointer-events: none;
}

.slide { transition: opacity 250ms ease; }
.slide.fade-out { opacity: 0; }

/* Buttons centered at top:55% per engine rule, NOT bottom-pinned. */
.slide-button-stack {
  position: absolute;
  top: 55%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: min(560px, 80%);
}

/* Educational disclaimer bottom-left of every character page. */
.edu-disclaimer {
  position: absolute;
  bottom: 12px; left: 12px;
  font-family: 'Share Tech', sans-serif;
  font-size: 11px;
  color: rgba(255,255,255,0.7);
  max-width: 320px;
}
```

### Hub layout pattern

- **Title screen first** (full-bleed Atlantic storm at dusk, Mayflower silhouette, royalty-free).
- **Hub second** — analyzer-style personality quiz routes the player to one of 6 characters.
- Character cards do NOT all show on hub by default. The quiz reveals 2–3 candidates after Q2, then the student picks.
- Bottom strip: How to Play | Credits | Skip Quiz (opens full 6-card grid for replay).

---

## 3. Per-Character Music Brief

**Universal rules for music-hunter:**
- Royalty-free / CC-BY / public domain ONLY. Sources: Pixabay, Kevin MacLeod (incompetech.com), Internet Archive, Freesound, YouTube Audio Library, Free Music Archive, Musopen, Filmmusic.io.
- Loopable, 2–5 min, instrumental (no lyrics).
- Mix at -18 LUFS so it sits behind narration.
- Volume 0.5, fade in from 0 over 2 seconds. Lower further on game-over slides.
- **Chromebook AudioContext unlock on first click required** — engine handles, but every track must be playable post-unlock.
- **NO copyrighted source tracks.** No actual Disney *Pocahontas* score, no actual "Linus and Lucy", no Bear McCreary, no Hans Zimmer. Vibe-inspired only.
- **NO "war whoop" cartoon Native stereotypes.** Cedar drum and wood flute are dignified instrumentation; mock-tribal yelps are banned.

### Hub track

Storm-and-sail bed. Searches: `north atlantic storm ambient royalty free`, `pixabay tall ship wind`, `mayflower ocean loop cc0`, `period instrumentation atlantic free`. Layer wind/wave SFX low underneath.

### Title-screen sting

3–4 second cinematic bell-and-low-string fade in. Searches: `cinematic intro cc0`, `pixabay historical opener`, `colonial intro royalty free`.

### Per-character tracks

| # | Side | Character | Vibe | Search terms (try in this order) |
|---|---|---|---|---|
| 1 | Jamestown | **John Smith** | Swashbuckling adventure orchestral — soldier-of-fortune, Captain-with-a-musket energy. Big strings, brass stabs, a little Master & Commander cousin (vibe only, never sourced). | `swashbuckling orchestral royalty free`, `colonial adventure cc-by`, `pixabay 17th century strings`, Kevin MacLeod `Hitman`, `Impact Andante`, `The Pyre`, `epic orchestral exploration cc0` |
| 2 | Jamestown | **John Rolfe** | Latin / Spanish nylon-string guitar — tobacco came from Trinidad, the cash-crop spine carries Caribbean DNA. Warm, mercantile, slowly turning anxious as the labor question rises. | `spanish guitar instrumental cc0`, `latin nylon guitar royalty free`, `pixabay caribbean acoustic`, `colonial trade guitar free`, Kevin MacLeod `Spanish Summer`, `Mexican Plaza` |
| 3 | Jamestown | **Powhatan** | **Cedar drum + low wood flute, dignified, slow, sovereign.** This is a chief's leitmotif, NOT cartoon "Indian music." Sparse percussion, sustained flute melody, room to breathe. Treat with the same gravity Conquest gives Magellan. | `native american flute royalty free`, `cedar flute ambient cc0`, `pixabay indigenous flute respectful`, `tribal drum slow cc-by`, Musopen `flute solo public domain`. **AVOID:** anything tagged "war chant," "tribal war," "savage," "exotic." If a track has those tags, skip it. |
| 4 | Plymouth | **William Bradford** | **Charlie Brown Thanksgiving Vince Guaraldi piano cousin** — warm jazz piano trio, hearth-and-home, autumn afternoon, slightly melancholy because half his shipmates are dead. NEVER actual "Linus and Lucy." Find a CC0 jazz piano trio that lives in the same emotional zip code. | `jazz piano trio cc0`, `pixabay vintage jazz piano`, `cool jazz instrumental royalty free`, `mellow piano trio cc-by`, `autumn jazz piano free`, Free Music Archive `piano trio`. **AVOID:** anything that quotes the actual Linus theme. |
| 5 | Plymouth | **Squanto (Tisquantum)** | Wood flute solo + light hand drum + occasional acoustic guitar. **Brother Bear respect template** — borrowing the dignity, NOT the geography (Brother Bear is Inuit/Alaska; Squanto is Patuxet/Wampanoag, Northeast). Hopeful, patient, tinged with grief because he is the last of his village. | `native american flute solo royalty free`, `wood flute meditation cc0`, `pixabay indigenous acoustic`, `respectful flute free`, Musopen `traditional flute`. **AVOID:** "shamanic," "vision quest," "exotic." |
| 6 | Plymouth | **Massasoit** | Cedar drum, slightly deeper than Squanto's, plus low flute and ambient forest. A leader's track — measured, watchful. Same dignity bar as Powhatan. The track gets quieter and more spare in the late game as Massasoit narrates dependency and decline. | `native american drum slow cc0`, `cedar drum royalty free`, `pixabay forest ambient flute`, `respectful indigenous instrumental cc-by`. **AVOID:** "war drum," "tribal war," "battle." |

### Game-over sting (universal)

Short (3–5 sec) royalty-free fail stinger, then the Rickroll-cherry on every cutscene's tail (per series signature). Searches: `fail trombone royalty free`, `cinematic fail sting pixabay`, `game over stinger cc0`. The Rickroll cherry is a 3-second royalty-free MIDI/parody arrangement of "Never Gonna Give You Up" — search `rick astley never gonna give you up midi free`, `8-bit rickroll cc0`, or commission a quick MIDI render.

### Hub quiz audio bed

Quiz slides use a quieter, lower-energy version of the hub track — same instrumentation, half the volume, no percussion. This is the "thinking" bed.

---

## 4. Game-Over Cast Catalog

Every game-over pairs a **failure type** with a **cutscene character** so the comedy reads. Use the cutscene character whose vibe matches the failure. GIFs MUST be royalty-free / fair-use commentary, ideally embedded via Tenor/Giphy rather than self-hosted.

### Universal cast (works for any character on either side)

| Cutscene | Source | When to use | Headline / shout |
|---|---|---|---|
| **Yzma WRONG LEVERRR** | Emperor's New Groove | Pure dumb-choice fails — picked the obviously wrong option | "WRONG LEVERRRRR!" |
| **Bobby Boucher tackle** | The Waterboy | Physical-confrontation fails, getting raided, brawls, ambushes | "MAMA SAYS WINTER IS THE DEVIL!" |
| **Terry Tate "Colonial Enforcer"** | Office Linebacker (reskinned) | Lazy / unprepared / skipped-the-prep fails | "YOU CAN'T STARVE ON COMPANY TIME!" |
| **Rickroll / "Pilgrim Rick"** | Rick Astley | Universal cherry on every game-over — final 3-sec sting | "Never gonna give you up… *to dysentery*" |
| **Tulio & Miguel laughing** | Road to El Dorado | "You got conned" fails — believed a false promise, fake gold, fake guide | "It's tough to be a god…" |
| **El Dorado "Both? Both. Both is good."** | El Dorado | Indecision fails — refused to pick a side | "Both? Both? Both is good." |
| **Charlie Brown "AAUGH!"** | Peanuts | Pilgrim-side embarrassment / plan-falls-through fails | "AAUGH!" |

**Rule:** Charlie Brown cast members (Charlie, Linus, Lucy) are reserved for **Plymouth side only**. Yzma / Tulio-Miguel run universally. Bobby Boucher works both sides — winter/famine tackles equally well in Virginia and Massachusetts.

### Character-specific death cutscenes

| Character | Death cutscene | Visual / GIF target | Notes / tone |
|---|---|---|---|
| **John Smith** | Captured by Powhatan / wounded by gunpowder accident (real history — he left Virginia early after a powder bag exploded on his thigh) | Period-art still + comic spark/explosion overlay | Comic. Smith survived the real one and went home. Frame as "the colony lost its enforcer." |
| **John Rolfe** | Dies of illness ~1622 after Pocahontas dies in England — OR fails by overextending tobacco labor demand and triggering 1622 Powhatan uprising | Period-art portrait + tobacco-leaf wilt animation | Somber-comic. Rolfe is the spine of the slavery throughline; his bad ending is "the cash crop got too big." |
| **Powhatan** | **Powhatan does NOT die graphically.** Game-over for Powhatan is a dignity card: he narrates "the strangers kept coming, my people kept dying of their sicknesses, my brother Opechancanough fought them and lost." Period-art portrait, slow fade, cedar-drum tail. | Period art ONLY. NO comedic death. Bobby Boucher / Yzma do NOT appear on Powhatan's failure slides. | **Critical tone rule.** Powhatan's failures use the universal Yzma/Terry-Tate cast for comic relief on minor wrong choices, but the **terminal endgame card** is dignified factual narration, not a meme. |
| **William Bradford** | Winter death on the Mayflower / starvation in first winter | Snow-falling-on-a-ship loop + Charlie Brown "AAUGH!" + Rickroll tail | Comic. Half the Mayflower passengers really did die first winter — the joke is on the Pilgrims' bad planning, not on death. |
| **Squanto** | Falls ill on a 1622 expedition (real history — he died of "Indian fever" while guiding Bradford) — OR fails by being caught playing both Wampanoag and English politics | Period-art portrait, autumn leaves falling, wood-flute tail | **Dignified.** Squanto's terminal card narrates his own death the way he might tell it: "I taught them. They lived. I did not." NO comedic cast on the terminal card. Universal cast OK on minor wrong-choice fails earlier in the route. |
| **Massasoit** | **Massasoit lives a long life and dies in old age (~1661).** His "game-over" is the slow-decline narration card: he watches the English population grow, watches his sons take over, knows what's coming. Epilogue references **King Philip's War (1675)** as factual context — what happened to his son Metacom — NOT played out. | Period art ONLY. Forest ambient + cedar drum tail. | **Critical.** Massasoit's terminal card is the moral spine of the Plymouth side. It is delivered in his voice, factually, with dignity. NO meme cast on this card. NO graphic violence. NO moralizing narrator. |

### Failure-type → cast mapping (for gif-hunter quick reference)

- **Greedy / over-reaching (took too much, demanded too much)** → Yzma
- **Unprepared / lazy / skipped the prep** → Terry Tate (Colonial Enforcer reskin)
- **Outmuscled / raided / ambushed** → Bobby Boucher
- **Conned / tricked / believed a false promise** → Tulio & Miguel
- **Indecisive / refused to pick a side** → "Both is good"
- **Pilgrim-specific embarrassment / plan-falls-through** → Charlie Brown "AAUGH!"
- **Frozen / starved / died of disease** → comedic skeleton + Rickroll tail
- **Native-character TERMINAL endgame fails** → **NO comedic cast.** Period-art portrait + dignified voiceover card. Drum/flute tail. Always.
- **Native-character minor wrong-choice fails (early-route)** → Universal cast (Yzma, Terry Tate, etc.) is fine — these are still comedic, they're just not the endgame.

### Symmetric brutality rule (Michael's locked tone bar — read carefully)

If a Native gameover involves starvation/disease consequence, then the corresponding settler-side gameover MUST include factual reference to Native raids, captives, and inter-tribal violence. This is **not** to demonize Natives — it is to teach that survival pressure produced violence on both sides.

- **Powhatan side:** factual reference to Powhatan Confederacy raids on Jamestown (1622 uprising — ~350 settlers killed), framed as Powhatan's brother Opechancanough's strategic decision under pressure, not as savagery.
- **Massasoit side:** factual reference to Wampanoag-Narragansett rivalries that pre-date the English, and to Plymouth militia aiding Wampanoag against rival tribes — both groups using the other for their own survival math.
- **Settler sides:** factual reference to Starving Time cannibalism (Jamestown 1609–10, ~80% dead) and Mayflower winter death (~50% dead). Settlers also suffered.

The rule: **show the math, not the villain.** Both sides did what they had to do. The student does the moral work.

---

## 4.5. Roanoke Tutorial (pre-game onboarding)

**Plays BEFORE the analyzer hub quiz.** A ~10-slide "History Mystery" intro that uses the lost colony of 1587 to (a) establish that 1607–1640 isn't England's first attempt at colonization, (b) set up "England keeps trying" as the meta-frame, and (c) teach the engine — click mechanics, the timeline bar, the tone bar — before the player commits to a character.

**Roanoke is NOT a 7th playable character.** It is onboarding only. No character card. No analyzer route. The player passes through it once on first run; on replay, "Skip Tutorial" is offered alongside "Skip Quiz."

### Beat sheet (~10 slides)

1. **Hook.** Foggy island at dawn. Narration in first-person ship's log voice: "We sailed for Roanoke. The colony we left here three years ago. Our families. Our friends."
2. **Setup.** 1587. Sir Walter Raleigh's charter. Governor John White's colony. ~115 men, women, children. White returns to England for supplies.
3. **Delay.** The Spanish Armada (1588). White cannot return. England needs every ship.
4. **Return — 1590.** Three years late. White lands. The settlement is empty.
5. **The clue.** A single word carved into a tree post: **CROATOAN.**
6. **What it might mean.** Brief click-reveal: the Croatoan were a nearby tribe. A friendly one. The colonists may have moved there. Or been taken there. Or worse.
7. **The unresolved mystery.** No bodies. No struggle. No second message. To this day, no one knows what happened to the Lost Colony of Roanoke.
8. **The hand-off.** "England tried. England lost. England will try again."
9. **Engine teach.** A small timeline bar appears at the bottom for the first time: `1587 — Roanoke founded. 1590 — Roanoke lost.` Narration: "This bar will follow you. It remembers what you do."
10. **Transition to hub.** "Twenty years pass. England tries again. You cross the Atlantic. *Why?*" → cuts to Q1.

### Visual mood

- Foggy island, low-saturation greens and grays. Coastal scrub, dunes, single carved post.
- Parchment ship's-log overlay for narration text (uses `IM Fell English` per parchment-fix pattern — text baked into the PNG).
- One key prop image: the CROATOAN tree carving (period-style illustration or Wikimedia engraving).

### Music

Ominous lone wood-flute over distant surf and wind. Sparse, period-appropriate. NOT a cedar drum (drum is reserved for Native-character leitmotifs). Search terms for music-hunter: `lone wood flute ambient cc0`, `mystery historical ambient royalty free`, `pixabay foggy ambient flute`, `period sparse flute cc-by`.

### Voice & tone

First-person, present tense, ship's-log register. NO meta-analogies. NO "imagine if." The player IS John White stepping ashore in 1590.

### Outputs to engine

- Sets initial timeline bar to `1587 / 1590` events (visible underneath the hub quiz too).
- Establishes the click mechanic + reveal pattern + tone bar (somber-but-curious) before any character commits.
- Skippable on replay via "Skip Tutorial" link on title screen, alongside "Skip Quiz."

---

## 5. Hub Design

### Title screen (loads first)

- Full-bleed background: stormy Atlantic at dusk, Mayflower or three-ships silhouette (royalty-free — try `pixabay tall ship storm`, `wikimedia mayflower painting`).
- Center: **TIME WARP** in Bangers, 96px, `bone-white` with 2px black stroke.
- Below: **PLYMOUTH OR JAMESTOWN** in Bangers, 120px, `pl-hearth-orange`-to-`jt-tobacco-gold` gradient (visual hint that the game has two sides).
- Sub-tagline (Share Tech, 18px, white): "1607. 1620. Two boats. Two reasons. Pick your side."
- Single button: **CLICK HERE TO PLAY** (Bangers, black bg, gold border). Engine rule: NOT "Begin," NOT "Start" — "Click Here to Play" per series.
- Footer corner small (Share Tech, 11px): "A Time Warp by Mr. Jorgensen — for ACE 8th grade US History."
- **Replay-only links** (small, bottom-center, only visible on second-and-later visits as detected by localStorage):
  - "Skip Tutorial" — bypasses the Roanoke onboarding (§4.5).
  - "Skip Quiz" — opens the 6-card character grid directly.
- **NO Mr. Roughton credit on title screen.** This is outside the I–VII canon.

### Hub: analyzer-style personality quiz

This hub is **different** from Conquest's 7-card grid. Plymouth-or-Jamestown uses a 2-question quiz that funnels the player to a specific character.

**Q1 slide.** Background: split-screen — left side is a galleon at warm sunrise (Jamestown), right side is the Mayflower at cold dusk (Plymouth). Text overlay (Michael's exact framing, locked):

> **"Are you here to practice your own religion, or for riches and adventure?"**

- **Button A:** "To practice my own religion." → routes to Plymouth side
- **Button B:** "For riches and adventure." → routes to Jamestown side

This is a side-selector with character voice — the player is already speaking *as* the character at Q1. Q2 then routes within the chosen side to one of three characters.

**Q2 slide (Jamestown branch).** Background: Virginia coastline, James River, period art. Text: "What kind of person are you?"

- **Button A:** "I am a soldier. I have killed men in Hungary. I will kill men here." → John Smith
- **Button B:** "I am a planter. I will turn a profit out of dirt and leaves." → John Rolfe
- **Button C:** "Wait — *you* are crossing *my* Atlantic. *I was here first.*" → Powhatan

**Q2 slide (Plymouth branch).** Background: Plymouth Rock, autumn forest, period art. Text: "What kind of person are you?"

- **Button A:** "I am a leader. My people need a written compact and a roof before snow." → William Bradford
- **Button B:** "I speak both languages. I have been to Spain and back. The English need me." → Squanto
- **Button C:** "Wait — *you* are landing on *my* shore. *We have lived here for generations.*" → Massasoit

After Q2, the player sees a single character card with portrait + tagline + **"BEGIN VOYAGE"** button. A small **"Pick Someone Else"** link returns to Q1.

### Bypass / replay grid

A "Skip Quiz" button on the title screen opens a 6-card grid for students replaying. Layout 3 + 3 — Jamestown row warm-toned, Plymouth row cool-toned. Each card:

```
┌─────────────────────────┐
│  [Historical portrait]  │  ← real period-art, 2px black frame
│      NAME (Bangers)     │
│  Tagline (Share Tech)   │
│      [BEGIN VOYAGE]     │
└─────────────────────────┘
```

**Tagline drafts (writer can refine):**
1. **John Smith** — "Soldier. Survivor. Wrote the book — literally."
2. **John Rolfe** — "Tobacco. Marriage. Built the cash crop that built a country."
3. **Powhatan** — "Chief of thirty tribes. Watched the strangers arrive."
4. **William Bradford** — "Governor. Chronicler. Wrote everything down."
5. **Squanto** — "Captured. Shipped to Spain. Came home. Stayed useful."
6. **Massasoit** — "Sachem of the Wampanoag. Made peace. Lived to see the cost."

### How-to-Play page

- Parchment scroll background, `IM Fell English SC` for the heading.
- Bullet list (Share Tech, 18px):
  - Read the slide. Make a choice.
  - Wrong choices end the journey. Watch the cutscene.
  - Right choices push the journey forward.
  - Survive your character's full story to earn their epilogue card.
  - Try all 6 characters to see the full picture of 1607–1640.
- "Try Again" returns to slide_0 of current character. "Select Another Character" returns to HOME (the title screen). Engine rule.
- "BACK TO HUB" button bottom.

### Credits page

- Parchment scroll, `IM Fell English SC` headers.
- Sections (Bangers headers, Share Tech body):
  - **Created by** — Mr. Jorgensen, ACE
  - **Source material** — Bradford's *Of Plymouth Plantation*, Smith's *Generall Historie*, Library of Congress, Wikimedia Commons, National Archives
  - **Music** — list each track + composer + license (Kevin MacLeod / Pixabay / Free Music Archive / etc.)
  - **GIFs / cutscenes** — fair-use commentary; embed source links
  - **Fonts** — Bangers, Share Tech, IM Fell English (Google Fonts, OFL)
  - **Built with** — HTML/CSS/JS, no frameworks
  - **Inspired by the Time Warp series** — *small line, bottom of page:* "With thanks to Mr. Roughton (mrroughton.com) whose Time Warp concept inspired this and many other lessons. This game is outside the original Time Warp I–VII canon."
- Bottom: "For 8th grade US History. Classroom use."

---

## 6. Meme Vocabulary

### What FITS the colonial-survival energy (use freely)

- **Charlie Brown / Peanuts (Plymouth side ONLY):** "AAUGH!", Linus's blanket, Lucy's psychiatry booth, Snoopy on the doghouse. Pairs with the Vince Guaraldi audio mood.
- **Yzma + Kronk** universally — wrong-lever fails work in any era.
- **Bobby Boucher / Waterboy** universally — winter tackles, famine tackles, raid tackles.
- **Terry Tate** universally as "Colonial Enforcer" reskin.
- **Tulio & Miguel from Road to El Dorado** — fits the "you got conned by a promise of gold" beat (especially Jamestown).
- **Animaniacs map sequences** for the Atlantic crossing tutorial.
- **Schoolhouse Rock** "No More Kings" energy works for Plymouth's religious-freedom motivation.
- **Spongebob "3 hours later" / "200 years later" cards** for time skips between slides.
- **Pocahontas (1995 Disney) visual mood** for Jamestown's hub and slide aesthetic — leaves blowing, water motif, painted backgrounds. **VISUAL ONLY. NO Disney audio.**
- **Brother Bear visual respect template** for Squanto and Massasoit slides — dignity, scale, forest. **TEMPLATE ONLY. NO Disney audio.**
- **Veggie Tales pirates / silly cherries** for absurd cutscene caps.
- **BrainPOP Tim & Moby** low-key narrator inserts for clarification slides.

### What does NOT fit (avoid)

- **Modern political memes.** No Trump, no Biden, no current immigration debate, no "this is just like today" overlays. Dates the game and risks parents.
- **"Stolen land" rhetoric in slide copy.** Use neutral language: "settlers," "newcomers," "the Wampanoag," "the Powhatan Confederacy." The historical fact of displacement is shown via the characters' own narration, not via narrator moralizing.
- **"Noble savage" rhetoric.** Squanto and Massasoit are smart, strategic, ordinary humans making survival math. They are not magical. They are not pure. They are people.
- **"White men bad" framing.** Settlers are not painted as evil. They are painted as desperate and sometimes brutal — as were their counterparts. The game shows the choices; the student does the math.
- **"Funny accent" stereotype voices.** No mock-Indigenous accents. No mock-British "thee/thou" mockery. Period-appropriate vocabulary in earnest, not mocked.
- **"War whoop" cartoon Native audio.** Banned outright. Cedar drum and wood flute only.
- **Live-action graphic violence.** No on-screen scalping, no on-screen disease corpses, no graphic Starving Time depictions. Cannibalism is *referenced* (one comic-abstract line, e.g. "the Starving Time was so bad that some settlers… well, you'll read about it") and never depicted.
- **King Philip's War as gameplay.** Referenced in Massasoit's epilogue card as factual context — what happened to his son Metacom and the Wampanoag in 1675 — and never played out as a level.
- **Edgy / horror imagery.** No skulls-on-spikes, no gore, no realistic disease imagery. Cartoonish even when fatal.
- **Crude humor.** Conquest got a Drake-dysentery joke. This game does not have that license. The closest we get is "Pilgrim Rick" on Bradford's winter death cutscene.

### Cherry-on-top rule

Every game-over ends with a 3-second Rickroll-or-equivalent musical sting. Series signature.

- **Jamestown side cherry:** "Pilgrim Rick" / "Sea Shanty Rick" parody MIDI 3-sec sting.
- **Plymouth side cherry:** Same sting, optionally pitched into the Vince-Guaraldi-cousin jazz piano key on the Bradford route.
- **Native-character TERMINAL cards (Powhatan endgame, Massasoit endgame, Squanto endgame):** **NO Rickroll.** These cards end on a clean cedar-drum tail, full stop. The sting would undermine the dignity. Universal cast comic-fail slides earlier in the route still get the cherry.

---

## 7. Out of Scope / Hard NOs

- **Modern politics.** No 2020s political figures, no current events, no "this is just like today" overlays.
- **Real movie/TV soundtracks on public deploy.** No actual Disney *Pocahontas* score, no actual "Linus and Lucy", no Bear McCreary, no Hans Zimmer, no Brother Bear score. Vibe-inspired, never sourced.
- **Disney audio of any kind on public deploy.** Visual mood references are commentary/parody fair use; audio is not.
- **"War whoop" cartoon Native audio or visuals.** Banned. Cedar drum and wood flute only. No "exotic" tagged tracks.
- **Graphic violence.** Cannons fire offscreen. Disease deaths are narrated, not depicted. King Philip's War referenced, never played.
- **"Stolen land" framing.** Neutral language: "settlers," "newcomers," "the Wampanoag," "the Powhatan Confederacy." The historical reality of displacement comes through the characters' own narration.
- **"Noble savage" framing.** Native characters are strategic humans, not magical archetypes.
- **"White men bad" framing.** Settlers are desperate humans under survival pressure, not cartoon villains.
- **Punching-down stereotypes.** No mock accents. No "savage" gags. Indigenous resistance (e.g., the 1622 uprising under Opechancanough) is shown as historical fact and strategic competence, not as savagery.
- **Real student/teacher/school names** in the public deploy. Footer says "Mr. Jorgensen" only — no school name, no student names.
- **Loaded scolding language** in any game-over: NO "you should have known," NO "stupid choice," NO "this is why you fail." Frame as comedic karma on the universal cast cutscenes; frame as factual consequence on the Native-character terminal cards.
- **Mr. Roughton credit on title screen, hub, or character pages.** This game is **outside the I–VII canon.** A single thank-you reference at the bottom of the credits page is the only acknowledgment.
- **PPTX educational content alterations.** Slides are 1:1 from Michael's source. Theming overlays audio + cutscenes + hub — does NOT rewrite slide text, NOT reorder slides, NOT add/remove choices.
- **Crude humor beyond what's in the meme vocabulary.** No bathroom jokes here (Conquest got Drake's dysentery; this game doesn't have that license).
- **Disney **Pocahontas** narrative whitewashing.** Visual mood ONLY (water, leaves, wind, painted backgrounds). The game's Pocahontas-as-recurring-NPC arc tells the *historical* version: kidnapped by the English, baptized, married Rolfe, died at 21 in England. Not the Disney love story. Treated with dignity, factually.
- **Pocahontas as a playable route.** She is woven through Smith / Rolfe / Powhatan storylines as a recurring NPC. Not a character pick. This protects her from being reduced to a player avatar.

---

## 8. Build-Pipeline Notes for Downstream Agents

### Folder structure

```
Time-Warp-Plymouth-or-Jamestown/
├── THEME_plymouth_or_jamestown.md   (this file)
├── index.html                       (title screen)
├── tutorial.html                    (Roanoke onboarding — §4.5)
├── hub.html                         (quiz)
├── characters/
│   ├── smith.html
│   ├── rolfe.html
│   ├── powhatan.html
│   ├── bradford.html
│   ├── squanto.html
│   └── massasoit.html
├── audio/
│   ├── hub/
│   │   ├── main.mp3
│   │   └── quiz_bed.mp3
│   ├── tutorial/
│   │   └── roanoke_flute.mp3        (lone wood-flute + wind bed)
│   ├── smith/
│   │   ├── smith_main.mp3
│   │   └── smith_gameover.mp3
│   ├── rolfe/
│   ├── powhatan/
│   ├── bradford/
│   ├── squanto/
│   ├── massasoit/
│   ├── sfx/                         (anchor SFX, §1.6 rule 3)
│   │   ├── cannon_jamestown.mp3
│   │   ├── organ_compact.mp3
│   │   ├── drum_council.mp3
│   │   ├── bell_thanksgiving.mp3
│   │   └── wind_winter.mp3
│   └── stings/
│       ├── rickroll_cherry.mp3
│       ├── fail_sting.mp3
│       └── title_intro.mp3
├── memes/
│   ├── manifest.json                (Tenor/Giphy embed URLs)
│   ├── yzma/
│   ├── bobby/
│   ├── terrytate/
│   ├── rickroll/
│   ├── tulio_miguel/
│   ├── charliebrown/                (Plymouth side only)
│   └── per_character_endcards/      (period art for terminal Native cards)
├── images/
│   ├── backgrounds/
│   ├── tutorial/                    (Roanoke fog, Croatoan tree)
│   ├── portraits/                   (period-art portraits, Wikimedia)
│   └── parchment/                   (baked-in text PNGs — see below)
└── credits.html
```

### For music-hunter

- One folder per character: `audio/smith/`, `audio/rolfe/`, etc.
- Filename pattern: `{character}_main.mp3` (loop), `{character}_gameover.mp3` (lower-volume loop on fail slides).
- Hub: `audio/hub/main.mp3` and `audio/hub/quiz_bed.mp3`.
- Tutorial: `audio/tutorial/roanoke_flute.mp3` — lone wood-flute over distant surf and wind, sparse and ominous. NOT a cedar drum (drum is reserved for Native-character leitmotifs).
- SFX anchors (§1.6 rule 3): `audio/sfx/{name}.mp3` for the five locked anchor cues — cannon, organ chord, cedar drum (council), dinner-bell, wind-howl.
- Stings: `audio/stings/{name}.mp3`.
- Each folder needs a `LICENSE.txt` listing source URL + license + composer for each file.
- **Volume rule:** all tracks should master at -18 LUFS so the engine's 0.5 volume sits behind narration. Game-over tracks should be 6dB lower than main tracks. SFX anchors sit ABOVE the music bed in the mix.
- **Native character tracks (Powhatan, Squanto, Massasoit):** triple-check every license source and every track tag. If a track is tagged "war chant," "exotic," "savage," or anything pejorative, skip it even if technically free. Dignity bar.

### For gif-hunter

- One folder per cutscene character: `memes/yzma/`, `memes/bobby/`, etc.
- Plymouth-only cast (`memes/charliebrown/`) clearly labeled.
- **Period-art portraits for Native terminal cards** go in `images/portraits/` — Wikimedia / public-domain only. These are NOT "memes" — they are the dignified end cards.
- Prefer Tenor/Giphy embed URLs in `memes/manifest.json` so we're not redistributing copyrighted clips — fair-use commentary embed is safer than self-hosting.
- For self-hosted assets (cartoon executioner, parchment, period backgrounds), Pixabay / Pexels / Wikimedia / OpenGameArt only.
- Each meme folder needs `LICENSE.txt` or `SOURCES.md` with attribution.

### For gameover-designer

- Use the failure-type → cast mapping in §4.
- **Native-character terminal-card rule:** terminal endgame cards for Powhatan, Squanto, and Massasoit use period-art portraits + dignified voiceover text + drum/flute tail. **NO meme cast.** **NO Rickroll cherry.** This is the locked tone bar.
- Universal cast (Yzma, Bobby, Terry Tate, Charlie Brown) is fine on EARLY-route minor wrong-choice fails for Native characters — these are still comedic.
- Game-over slide structure: full-bleed cutscene GIF or period-art still (CSS class `fullscreen-gif` or `fullscreen-art`), Bangers headline overlay top, "TRY AGAIN" + "SELECT ANOTHER CHARACTER" buttons centered at top:55%.
- "Try Again" → slide_0 of current character. "Select Another Character" → HOME (title screen). Engine rule.
- Headline copy must follow tone rules in §7 (no scolding).

### For PPTX writer / slide writer

- **READ §1.5 (Voice & Immersion HARD RULE) AND §1.6 (Engine Conventions) BEFORE WRITING ANY SLIDE.** Strict first-person present tense. No Brain Snacks. No meta-analogies. No teacher voice-overs. Timeline bar accumulates events. Stacking review at end of each route (tentative — flag for QC). Five locked SFX anchor moments.
- **Educational beats every character must hit** (so the writer can target them, and the student leaves with the ARE-paragraph evidence):
  1. **Motivation** — Jamestown = profit/glory/Virginia Company; Plymouth = religious freedom from Church of England
  2. **Settler type** — Jamestown = single young men, soldiers of fortune, no women in early years; Plymouth = families with women and children, Mayflower Compact signed before landing
  3. **Native relationship** — Jamestown started hostile (took Powhatan land/food at gunpoint, 1622 uprising in retaliation); Plymouth started cooperative (Squanto's agriculture lessons, first Thanksgiving 1621, Wampanoag-English mutual defense pact) but the Wampanoag became dependent on Plymouth military aid against the Narragansett, and the relationship eventually broke in King Philip's War (1675)
  4. **Geography → economy** — Jamestown warm + fertile + navigable rivers → tobacco → labor demand → indentured servants → enslaved Africans (1619). Plymouth rocky soil + short growing season → subsistence farming + fishing + shipbuilding → no economic engine for plantation slavery.
  5. **Disease & famine** — Jamestown "Starving Time" 1609–10, ~80% dead, cannibalism documented (referenced, not depicted); Plymouth ~50% of Mayflower passengers died first winter, Squanto's agriculture mentorship saved the survivors.
- **Pocahontas as recurring NPC** woven through Smith / Rolfe / Powhatan storylines — Smith's rescue arc (which Smith later wrote about and may have embellished), Rolfe's marriage and her conversion / baptism / death at 21 in England, Powhatan's grief as her father. Treat with dignity. Historical facts only.
- **Mayflower Compact reveal** is a key Bradford slide — should use a parchment overlay with `IM Fell English` font, text baked into the PNG (per the parchment-fix pattern) so it renders correctly across browsers.
- **Educational disclaimer** bottom-left of every character page (engine rule). Suggested text: "This game uses comedic cutscenes to teach historical events. All deaths and conflicts depicted occurred. Sources on Credits page."

### For hub-builder

- **Flow on first run:** title screen → "Click Here to Play" → Roanoke Tutorial (§4.5, ~10 slides) → Hub Q1 (Michael's exact framing) → Q2 → character card → BEGIN VOYAGE.
- **Flow on replay** (localStorage flag): title screen shows extra "Skip Tutorial" + "Skip Quiz" links beneath the main button.
- Title screen: full-bleed Atlantic storm + Mayflower silhouette. "Click Here to Play" button (engine rule — NOT "Begin," NOT "Start").
- Tutorial: see §4.5. Lone wood-flute audio, parchment ship's-log overlays, ends by seeding the timeline bar with `1587 / 1590` events.
- Quiz hub: 2-question funnel per §5. Q1 wording is locked: "Are you here to practice your own religion, or for riches and adventure?"
- **NO Mr. Roughton credit on title screen.** Single thank-you reference on credits page only.
- Music: hub track plays on title + quiz at volume 0.5, fades in from 0 over 2 seconds. Chromebook AudioContext unlock on first click.
- Background images: full-bleed JPG (1920x1080 minimum). Compress to <400KB each.

### Engine constraints (locked from existing Time Warp building rules)

- **Parchment/scroll text z-index:** parchment text must render ABOVE non-bg images. Recurring bug — use the documented parchment-fix pattern (bake text into PNG with Pillow, do NOT fix via CSS).
- **Buttons centered at top:55%, NOT bottom-pinned.** See `.slide-button-stack` CSS in §2.
- **Music volume 0.5, fade in from 0 over 2 seconds.**
- **Chromebook AudioContext unlock on first click.** Engine handles; every track must be playable post-unlock.
- **Title screen button text:** "Click Here to Play" — not "Begin," not "Start," not "Play."
- **Educational disclaimer** bottom-left of every character page.
- **Try Again** → slide_0 of current character. **Select Another Character** → HOME.
- **PPTX-derived backgrounds** are full-bleed JPG (NOT cropped, NOT letterboxed).

---

*End of THEME spec. Questions or scope changes go through Mr. Jorgensen before any agent kicks off downloads. Tone bar (§4 symmetric brutality, §7 hard NOs) is non-negotiable — the entire educational frame depends on it.*
