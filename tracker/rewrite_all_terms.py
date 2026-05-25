"""Integrate key terms into slide bodies across all character HTMLs.
17 orphan slides across rolfe/powhatan/bradford/squanto/massasoit/chilton.
Each rewrite naturally introduces the term name into the prose.
Idempotent.
"""
from pathlib import Path
import json

DOCS = Path(__file__).resolve().parent.parent / "docs"

REWRITES = [
    # ----- ROLFE -----
    {"file": "rolfe.html", "slide_id": "slide_18",
     "old": ["I plant the Spanish seeds and crossbreed with the local strain.",
             "Local plants are hardier in this soil. Spanish leaves are sweeter on the tongue.",
             "The first harvest comes in. It smells like sugar and pine.",
             "I send a single barrel back to England and I wait."],
     "new": ["I plant the Spanish seeds and crossbreed with the local strain.",
             "Local plants are hardier in this soil. Spanish leaves are sweeter on the tongue.",
             "The first harvest comes in. It smells like sugar and pine.",
             "I send a single barrel back to England and I wait. If it sells, tobacco becomes our cash crop — grown not for food, but for gold."]},
    {"file": "rolfe.html", "slide_id": "slide_34",
     "old": ["Tobacco needs hands. More than the colony has.",
             "The Company sends indentured servants — young men who sign seven-year contracts for passage.",
             "They work the leaves. Many die before their contract ends.",
             "The harvest doubles every year. The Company writes asking how soon we can triple."],
     "new": ["Tobacco needs hands. More than the colony has.",
             "The Company sends indentured servants — young men who sign seven-year contracts for passage.",
             "Under the new headright system, any settler who pays a man's passage gets fifty acres. The more servants you bring, the more land you claim.",
             "They work the leaves. Many die before their contract ends.",
             "The harvest doubles every year. The Company writes asking how soon we can triple."]},
    {"file": "rolfe.html", "slide_id": "slide_39",
     "old": ["The same summer the Dutch ship lands, twenty-two of us form the first elected assembly in English America.",
             "We pass laws on tobacco prices, drunkenness, church attendance, servant contracts.",
             "We do not pass any law on the twenty Africans. We do not yet know what to call what we have done.",
             "The silence in the records is its own answer."],
     "new": ["The same summer the Dutch ship lands, twenty-two of us form the first elected assembly in English America. We call it the House of Burgesses.",
             "We pass laws on tobacco prices, drunkenness, church attendance, servant contracts.",
             "We do not pass any law on the twenty Africans. 1619 will be remembered as two histories — the birth of representative government in America, and the arrival of African slavery on these shores. We do not yet know what to call what we have done.",
             "The silence in the records is its own answer."]},

    # ----- POWHATAN -----
    {"file": "powhatan.html", "slide_id": "slide_1",
     "old": ["My name is Wahunsenacah. The English call me Powhatan, after my birth village.",
             "I am paramount chief of about thirty tribes along these rivers.",
             "I am sixty years old. I have ruled longer than most of these English have been alive."],
     "new": ["My name is Wahunsenacah. The English call me Powhatan, after my birth village.",
             "I am the paramount chief of about thirty tribes along these rivers — what the English will name the Powhatan Confederacy.",
             "I am sixty years old. I have ruled longer than most of these English have been alive."]},
    {"file": "powhatan.html", "slide_id": "slide_35_peace",
     "old": ["I tell him to keep the peace.",
             "Four years after my death, on a single morning in March 1622, his runners reach every English plantation on the James at the same hour.",
             "About 347 settlers die before noon.",
             "He does not listen to me. He listens to the next twenty burned villages.",
             "The confederation I built does not survive thirty more years."],
     "new": ["I tell him to keep the peace.",
             "Four years after my death, on a single morning in March 1622, his runners reach every English plantation on the James at the same hour. History will call it the 1622 Uprising.",
             "About 347 settlers die before noon.",
             "He does not listen to me. He listens to the next twenty burned villages.",
             "The confederation I built does not survive thirty more years."]},

    # ----- BRADFORD -----
    {"file": "bradford.html", "slide_id": "slide_16",
     "old": ["*In the name of God, Amen. We whose names are underwritten… do by these presents solemnly and mutually, in the presence of God and of one another, covenant and combine ourselves together into a civil Body Politick…*",
             "",
             "Forty-one of us sign. Saints and Strangers. The first written agreement on this coast that says: the people who live here will obey the laws the people who live here together make.",
             "",
             "No king signs this page. No bishop signs this page. We sign this page.",
             "",
             "*(BROAD path closing line):* Hopkins signs first.",
             "*(NEGOTIATED path closing line):* Hopkins signs grudgingly, third from last."],
     "new": ["*In the name of God, Amen. We whose names are underwritten… do by these presents solemnly and mutually, in the presence of God and of one another, covenant and combine ourselves together into a civil Body Politick…*",
             "",
             "We will call it the Mayflower Compact. Forty-one of us sign. Saints and Strangers. The first written agreement on this coast that says: the people who live here will obey the laws the people who live here together make. It is self-government in its rawest form.",
             "",
             "No king signs this page. No bishop signs this page. We sign this page.",
             "",
             "*(BROAD path closing line):* Hopkins signs first.",
             "*(NEGOTIATED path closing line):* Hopkins signs grudgingly, third from last."]},
    {"file": "bradford.html", "slide_id": "slide_32",
     "old": ["Ten years after we landed, a much larger English colony plants itself north of us. Massachusetts Bay. Boston. Salem.",
             "We are a small town beside their great one. They are Puritan but not Separatists — they meant to reform the Church of England from inside it.",
             "Our story will get folded into theirs. I do not mind. I want the story to be told."],
     "new": ["Ten years after we landed, a much larger English colony plants itself north of us. Massachusetts Bay. Boston. Salem.",
             "We are a small town beside their great one. This is the difference between Pilgrims and Puritans — we left the Church of England behind; they meant to reform it from inside.",
             "Our story will get folded into theirs. I do not mind. I want the story to be told."]},

    # ----- SQUANTO -----
    {"file": "squanto.html", "slide_id": "slide_16",
     "old": ["The Pokanoket tell me what came. A sickness the English ships carried. The healers had no name for it.",
             "Nine of every ten Patuxet are gone. Nine of every ten Massachusett. Whole villages, empty.",
             "The survivors call it the Great Dying. The English will call the empty land *a gift from God.*"],
     "new": ["The Pokanoket tell me what came. A sickness the English ships carried from 1616 through 1619. The healers had no name for it.",
             "Nine of every ten Patuxet are gone. Nine of every ten Massachusett. Whole villages, empty.",
             "The survivors call it the Great Dying. Historians will name it the 1616–19 Plague. The English will call the empty land *a gift from God.*"]},

    # ----- MASSASOIT -----
    {"file": "massasoit.html", "slide_id": "slide_1",
     "old": ["I am Ousamequin — Massasoit, \"great chief\" of the Wampanoag.",
             "Forty villages answered to me. Some still do.",
             "Three winters ago, sickness came off an English ship.",
             "Ten thousand of my people are dead.",
             "The bones are still in the houses."],
     "new": ["I am Ousamequin. My people call me a sachem — a chief among chiefs. The English will know me as Massasoit, \"great chief\" of the Wampanoag.",
             "Forty villages answered to me. Some still do.",
             "Three winters ago, sickness came off an English ship.",
             "Ten thousand of my people are dead.",
             "The bones are still in the houses."]},
    {"file": "massasoit.html", "slide_id": "slide_13",
     "old": ["We sign. Mutual defense.",
             "I have allies with guns against the Narragansett.",
             "Bradford has warriors against any tribe that would push his fort into the sea.",
             "Neither of us trusts the other yet. The treaty does not require trust.",
             "It requires that we both still need each other in the morning."],
     "new": ["We sign. Mutual defense. History will call it the Wampanoag–Plymouth Treaty of 1621.",
             "I have allies with guns against the Narragansett.",
             "Bradford has warriors against any tribe that would push his fort into the sea.",
             "Neither of us trusts the other yet. The treaty does not require trust.",
             "It requires that we both still need each other in the morning."]},

    # ----- CHILTON -----
    {"file": "chilton.html", "slide_id": "slide_6",
     "old": ["The shallop grinds against a flat shore-stone. I step off — early, if not first. The boys will tell that story different ways for the rest of my life. The stone under my shoe is the coldest thing I have ever stood on.",
             "Before they let us off, forty-one of the men signed a paper in the cabin. They called it a Compact. I am thirteen. I do not yet understand what they have done."],
     "new": ["The shallop grinds against a flat shore-stone. I step off — early, if not first. The boys will tell that story different ways for the rest of my life. The stone under my shoe is the coldest thing I have ever stood on.",
             "Before they let us off, forty-one of the men signed a paper in the cabin. They called it the Mayflower Compact. Saints and Strangers both put their names to it — the religious Pilgrims and the hired travelers, agreeing to live under the same laws. I am thirteen. I do not yet understand what they have done."]},
    {"file": "chilton.html", "slide_id": "slide_9b",
     "old": ["I am not alone. That is the part the books leave out.",
             "By February, only six or seven of us can still stand. Six or seven, to care for all the rest.",
             "Elder Brewster carries broth. Captain Standish — a Stranger, his wife already buried — washes the sick. They tend people who are not their family. I am thirteen, and I can still stand. So I carry water too.",
             "When four die in one night and the ground is frozen too hard to bury them, we sing. Psalm 23. Low, so the woods won't count our voices.",
             "We suffer together. We praise God together. Half of us go into the ground. The other half goes on — bound to each other by a winter no king ordered and no king ended."],
     "new": ["I am not alone. That is the part the books leave out.",
             "We call it the General Sickness — fever, scurvy, lungs filling up. By February, only six or seven of us can still stand. Six or seven, to care for all the rest.",
             "This is communal care: Elder Brewster carries broth. Captain Standish — a Stranger, his wife already buried — washes the sick. They tend people who are not their family. I am thirteen, and I can still stand. So I carry water too.",
             "When four die in one night and the ground is frozen too hard to bury them, we sing. Psalm 23. Low, so the woods won't count our voices. The psalm-singing is the one thing the sickness cannot take.",
             "We suffer together. We praise God together. Half of us go into the ground. The other half goes on — bound to each other by a winter no king ordered and no king ended."]},
]


def rewrite():
    total = 0
    by_file = {}
    for r in REWRITES:
        by_file.setdefault(r["file"], []).append(r)
    for fname, rs in by_file.items():
        path = DOCS / fname
        text = path.read_text(encoding="utf-8")
        changed = 0
        for r in rs:
            old_json = json.dumps(r["old"], ensure_ascii=False)[1:-1]
            new_json = json.dumps(r["new"], ensure_ascii=False)[1:-1]
            if new_json in text:
                print(f"  [skip] {fname} {r['slide_id']} — already done")
                continue
            if old_json not in text:
                print(f"  [WARN] {fname} {r['slide_id']} — old body not matched")
                continue
            text = text.replace(old_json, new_json, 1)
            changed += 1
            print(f"  [done] {fname} {r['slide_id']}")
        if changed:
            path.write_text(text, encoding="utf-8")
            total += changed
    print(f"\nRewrote {total} slide(s) across {len(by_file)} files.")


if __name__ == "__main__":
    rewrite()
