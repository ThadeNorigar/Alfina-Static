"""
Update zeitleiste.json for Kap 10/11/12 restructure (Akt I Schluss).

Changes:
- Existing event "Sorel: Die Kamera fängt Schemen ein" (Kap 10, tz_tag 120)
  → renamed to "Sorel: Die Kamera sieht mehr als die Linse", tz_tag 133 (13. Mai),
    detail clarified.
- Existing event "Alphina trifft Sorel im Botanischen Garten" (Kap 11, tz_tag 125)
  → Kap 12, tz_tag 135 (15. Mai), Akt-I-Schluss.
- Existing event "Alphina: Pochen unter dem Garten" (Kap 11, tz_tag 125)
  → Kap 9, tz_tag 131 (11. Mai), because the Kap-9 draft already contains the beat.
- New Kap 10 events (3): Tschechow Kamera, fremde Frau auf Platte, Steinkreis Sorel.
- New Kap 11 events (6): Uhren-Netz (Tschechow + Wissen), Runas Flugblatt gesehen,
  Begegnung Alphina-Vesper, Alphina ahnt Vesper resoniert, Vesper kennt Namen.

Preserves Windows CRLF line endings.
"""

import json

PATH = "C:/Users/micro/StudioProjects/Alphina-Static/buch/zeitleiste.json"

with open(PATH, encoding="utf-8") as f:
    d = json.load(f)

events = d["monate"][10]["events"]["thalassien"]
print(f"Vorher: {len(events)} Events")

# --- 1. Modify existing events in place ---
for ev in events:
    t = ev.get("titel", "")
    if t == "Alphina: Pochen unter dem Garten":
        ev["kapitel"] = "09"
        ev["tz_tag"] = 131
        ev["datum_text"] = "11. Mai"
        ev["detail"] = (
            "Hand auf den Purpurstein im Steinkreis des Botanischen Gartens. "
            "Pochen wie unter Marens Werft — aber Alphina kennt Maren nicht. "
            "Einer, Pause, einer. Tief, im Knochen, nicht im Ohr."
        )
        print("  Pochen-Event: Kap 11 -> Kap 9, tz_tag 125 -> 131")
    elif t == "Sorel: Die Kamera fängt Schemen ein":
        ev["tz_tag"] = 133
        ev["datum_text"] = "13. Mai"
        ev["titel"] = "Sorel: Die Kamera sieht mehr als die Linse"
        ev["fakt"] = "kamera-faengt-mehr-ein"
        ev["detail"] = (
            "Erste Vael-Platten entwickelt. Eine Platte zeigt eine schattenhafte "
            "Gestalt mit leuchtenden Augen zwischen den Pollern — Sorel hat sie nicht "
            "gesehen. Eine zweite Platte zeigt eine fremde Frau mit Farnen am Hafen — "
            "er hat sie nicht fotografiert. Die Kamera fängt ein, was seine Augen "
            "nicht erreichen."
        )
        print("  Sorel-Kamera-Event: tz_tag 120 -> 133, Titel präzisiert")
    elif t == "Alphina trifft Sorel im Botanischen Garten":
        ev["kapitel"] = "12"
        ev["tz_tag"] = 135
        ev["datum_text"] = "15. Mai"
        ev["intensitaet"] = "bekannt"
        ev["detail"] = (
            "Maiabend im Steinkreis. Alphina kommt zum zweiten Mal in den Garten, "
            "zielgerichtet. Sorel klettert zum zweiten Mal über die Mauer, weil seine "
            "Platten ihn zurückgezogen haben. Sie sehen einander. Die Farne folgen "
            "einem Gespräch, das noch nicht begonnen hat. Ende Akt I."
        )
        print("  Begegnung-Event: Kap 11 -> Kap 12, tz_tag 125 -> 135")

# --- 2. New events to add ---
new_kap10 = [
    {
        "tz": 551, "mz": 0, "kapitel": "10",
        "typen": ["tschechow"],
        "titel": "Sorels Kamera als Resonanz-Leiter",
        "tz_tag": 133, "datum_text": "13. Mai",
        "detail": (
            "Platte 7 (das eigene Gesicht), eine Platte mit Schem am Hafen, eine "
            "Platte mit fremder Frau die nicht vor der Linse stand — drei Bilder an "
            "einer Wand im Lichthaus-Keller. Tschechow: die Kamera sieht in andere "
            "Schichten. Feuert in Akt III (Steg-Fotos) und Akt IV (Schwelle)."
        )
    },
    {
        "tz": 551, "mz": 0, "kapitel": "10",
        "typen": ["wissen"],
        "titel": "Sorel: Fremde Frau auf der Hafen-Platte",
        "tz_tag": 133, "datum_text": "13. Mai",
        "figur": "Sorel", "fakt": "fremde-frau-auf-platte", "stufe": "gesehen",
        "detail": (
            "Dunkles Haar, Farne im Arm, Hafen im Hintergrund. Er hat sie nie gesehen. "
            "Er weiß ihren Namen nicht. Er hängt die Platte neben Platte 7 an die Wand."
        )
    },
    {
        "tz": 551, "mz": 0, "kapitel": "10",
        "typen": ["wissen"],
        "titel": "Sorel: Steinkreis im Botanischen Garten",
        "tz_tag": 133, "datum_text": "13. Mai",
        "figur": "Sorel", "fakt": "steinkreis-garten-gesehen", "stufe": "gesehen",
        "detail": (
            "Nächtlicher Einbruch über die Mauer. Mondlicht auf Farnen. Sieben Steine "
            "im Mittelhügel. Er fasst den Stein nicht an — er fotografiert ihn. "
            "Für Sorel ist der Kreis ein Bild, kein Körper."
        )
    },
]

new_kap11 = [
    {
        "tz": 551, "mz": 0, "kapitel": "11",
        "typen": ["tschechow", "erkenntnis"],
        "titel": "Vespers Uhren-Netz über Vael",
        "tz_tag": 134, "datum_text": "14. Mai",
        "detail": (
            "Fünf Wochen systematische Kartografie abweichender Uhren. Die Punkte "
            "ergeben ein geometrisches Netz. Die Mitte des Netzes liegt unter dem "
            "Botanischen Garten. Tschechow für Akt III: das Netz zeigt auf den Steinkreis."
        )
    },
    {
        "tz": 551, "mz": 0, "kapitel": "11",
        "typen": ["wissen"],
        "titel": "Vesper: Das geometrische Netz abweichender Uhren",
        "tz_tag": 134, "datum_text": "14. Mai",
        "figur": "Vesper", "fakt": "vesper-uhren-netz", "stufe": "versteht",
        "detail": (
            "Fünf Wochen Adressen gesammelt von Häusern in denen Uhren anders laufen. "
            "Die Punkte sind nicht zufällig. Sie liegen auf einem Muster, das er noch "
            "nicht benennen kann, aber sehen."
        )
    },
    {
        "tz": 551, "mz": 0, "kapitel": "11",
        "typen": ["wissen"],
        "titel": "Vesper sieht Runas Flugblatt",
        "tz_tag": 134, "datum_text": "14. Mai",
        "figur": "Vesper", "fakt": "runas-flugblatt-ueberlap", "stufe": "gesehen",
        "detail": (
            "Runas 'Vaels Geister' liegt in der Druckerei aus. Vesper registriert: "
            "die Adressen mit heißem Wasser und Kaminfeuer aus Runas Flugblatt "
            "überschneiden sich teilweise mit seinen eigenen Uhren-Punkten. Zwei "
            "unabhängige Beobachter, dasselbe Raster."
        )
    },
    {
        "tz": 551, "mz": 0, "kapitel": "11",
        "typen": ["begegnung"],
        "titel": "Alphina spricht Vesper im Anker an",
        "tz_tag": 134, "datum_text": "14. Mai",
        "figuren": ["Alphina", "Vesper"],
        "intensitaet": "fluechtig",
        "ort": "Gasthaus Zum Anker, Vespers Zimmer",
        "detail": (
            "Sie klopft an seine Tür. Er öffnet einen Spalt. Drei Sätze, vielleicht "
            "vier. Keine von beiden weiß, was man sagen darf. Sie geht. Aber sie "
            "kennen jetzt die Namen."
        )
    },
    {
        "tz": 551, "mz": 0, "kapitel": "11",
        "typen": ["wissen"],
        "titel": "Alphina: Vesper resoniert auch",
        "tz_tag": 134, "datum_text": "14. Mai",
        "figur": "Alphina", "fakt": "vesper-resoniert", "stufe": "ahnt",
        "detail": (
            "Das erste Mal, dass Alphina weiß: sie ist nicht die einzige in Vael, "
            "in deren Händen etwas geschieht, das keinen Namen hat."
        )
    },
    {
        "tz": 551, "mz": 0, "kapitel": "11",
        "typen": ["wissen"],
        "titel": "Vesper: Die Frau heißt Alphina",
        "tz_tag": 134, "datum_text": "14. Mai",
        "figur": "Vesper", "fakt": "alphina-wissen", "stufe": "gesehen",
        "detail": (
            "Er hatte sie vorher schon im Schankraum bemerkt — die Frau mit Erde unter "
            "den Nägeln. Jetzt hat sie einen Namen und eine Tür zwischen ihnen."
        )
    },
]

# --- 3. Rearrange: put Kap 10 + Kap 11 new events and the now-Kap-12 event
#        in chronological order around the existing Kap-10-Kamera-Event ---

# Pop the moved events
def pop_by_titel(lst, titel):
    for i, ev in enumerate(lst):
        if ev.get("titel") == titel:
            return lst.pop(i)
    return None

begegnung_ev = pop_by_titel(events, "Alphina trifft Sorel im Botanischen Garten")
pochen_ev    = pop_by_titel(events, "Alphina: Pochen unter dem Garten")
assert begegnung_ev is not None
assert pochen_ev is not None

# Find the Kap-10-Kamera-Event (already renamed) and insert new Kap 10 + Kap 11 after it
kap10_idx = None
for i, ev in enumerate(events):
    if ev.get("titel") == "Sorel: Die Kamera sieht mehr als die Linse":
        kap10_idx = i
        break
assert kap10_idx is not None

# Insert order after the Kamera-Event:
#   new_kap10 (3 events, tz_tag 133, same day as Kamera)
#   new_kap11 (6 events, tz_tag 134)
#   begegnung_ev (tz_tag 135)
insert_at = kap10_idx + 1
events[insert_at:insert_at] = new_kap10 + new_kap11 + [begegnung_ev]

# Insert Pochen-Event at end of Kap-9-block
last_k9_idx = None
for i, ev in enumerate(events):
    if ev.get("kapitel") == "09":
        last_k9_idx = i
assert last_k9_idx is not None
events.insert(last_k9_idx + 1, pochen_ev)

print(f"Nachher: {len(events)} Events")

# --- 4. Write back with CRLF ---
out = json.dumps(d, ensure_ascii=False, indent=2)
out_crlf = out.replace("\n", "\r\n") + "\r\n"
with open(PATH, "w", encoding="utf-8", newline="") as f:
    f.write(out_crlf)

print("zeitleiste.json geschrieben")

# --- 5. Verification ---
with open(PATH, encoding="utf-8") as f:
    d2 = json.load(f)
print()
print("--- Verifikation: Events tz_tag 131-135 ---")
for ev in d2["monate"][10]["events"]["thalassien"]:
    tz = ev.get("tz_tag")
    if tz and 131 <= tz <= 135:
        kap = ev.get("kapitel", "-")
        dt = ev.get("datum_text", "")
        typen = ev.get("typen", [])
        print(f"  Kap {kap:>2} | tz={tz} ({dt:>8}) | {typen}")
        print(f"      {ev.get('titel','')}")
