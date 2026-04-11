#!/usr/bin/env python3
"""Comprehensive zeitleiste.json fix script.

Fixes:
1. Add TZ calendar (12 fantasy month names) to meta
2. Add missing typen (resonanz, gaensehaut, verabredung)
3. Convert all datum_text to fantasy month names (DD. Monatsname YYYY)
4. Add K23 (Sorel, missing from zeitleiste)
5. Fix K36-41 ordering (remove thal duplicates K39/K40, add proper moragh K39/K40)
6. Tag fire event as I3 in TZ 154 section
7. Remove old I3, I7 from Buch 1 moragh
8. Remove I9 from Buch 2 moragh
9. Add I4-I6 (Varen interludes, Buch 2)
10. Add I7-I9 (Maren interludes, Buch 3)
11. Remove misplaced "Kap 39" dornen event from moragh
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZL_PATH = ROOT / "buch" / "zeitleiste.json"

with open(ZL_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# ── 1. Add TZ calendar to meta ──────────────────────────────────────────────
data["meta"]["zeitrechnung"]["tz_kalender"] = {
    "tag": "24 Stunden",
    "jahr": "365 Tage = 12 Monate",
    "monate": [
        {"nr": 1, "name": "Eismond", "entspricht": "Januar"},
        {"nr": 2, "name": "Sturmmond", "entspricht": "Februar"},
        {"nr": 3, "name": "Saatmond", "entspricht": "März"},
        {"nr": 4, "name": "Grünmond", "entspricht": "April"},
        {"nr": 5, "name": "Blütenmond", "entspricht": "Mai"},
        {"nr": 6, "name": "Lichtmond", "entspricht": "Juni"},
        {"nr": 7, "name": "Glutmond", "entspricht": "Juli"},
        {"nr": 8, "name": "Erntemond", "entspricht": "August"},
        {"nr": 9, "name": "Herbstmond", "entspricht": "September"},
        {"nr": 10, "name": "Nebelmond", "entspricht": "Oktober"},
        {"nr": 11, "name": "Frostmond", "entspricht": "November"},
        {"nr": 12, "name": "Dunkelmond", "entspricht": "Dezember"},
    ],
}

# ── 2. Add missing typen ────────────────────────────────────────────────────
data["typen"].setdefault("resonanz", {"label": "Resonanz", "farbe": "#6a8a5a"})
data["typen"].setdefault("gaensehaut", {"label": "Gänsehaut", "farbe": "#8b6a8b"})
data["typen"].setdefault("verabredung", {"label": "Verabredung", "farbe": "#5a8a7a"})

# ── 3. Convert datum_text ───────────────────────────────────────────────────
MONTH_MAP = {
    "01": "Eismond",
    "02": "Sturmmond",
    "03": "Saatmond",
    "04": "Grünmond",
    "05": "Blütenmond",
    "06": "Lichtmond",
    "07": "Glutmond",
    "08": "Erntemond",
    "09": "Herbstmond",
    "10": "Nebelmond",
    "11": "Frostmond",
    "12": "Dunkelmond",
}


def convert_datum(dt):
    if not dt:
        return dt
    m = re.match(r"(\d{1,2})\.(\d{2})\.(\d+)\s*TZ(.*)", dt)
    if m:
        day = str(int(m.group(1)))
        month_name = MONTH_MAP.get(m.group(2), m.group(2))
        year = m.group(3)
        suffix = m.group(4).strip()
        result = f"{day}. {month_name} {year}"
        if suffix:
            result += f" {suffix}"
        return result
    return dt


def process_events(events):
    for ev in events:
        if isinstance(ev, dict) and "datum_text" in ev:
            ev["datum_text"] = convert_datum(ev["datum_text"])


for monat in data["monate"]:
    if "events" in monat:
        for side in ("thalassien", "moragh"):
            if side in monat["events"]:
                process_events(monat["events"][side])

# ── 4-7. Structural fixes in Buch 1 ────────────────────────────────────────
buch1 = None
for monat in data["monate"]:
    if monat.get("buch") == "Buch 1: Der Riss":
        buch1 = monat
        break

assert buch1, "Buch 1 month not found!"
thal = buch1["events"]["thalassien"]
moragh = buch1["events"]["moragh"]

# 4a. Remove K39 duplicate and K40 AUDIT from thalassien
thal[:] = [
    ev
    for ev in thal
    if not (isinstance(ev, dict) and ev.get("kapitel") in ("39", "40"))
]

# 4b. Add K23 before K24
k23 = {
    "tz": 551,
    "mz": 3635,
    "kapitel": "23",
    "typen": ["erkenntnis", "tschechow"],
    "titel": "Sorel allein — erste bewusste Projektion, Geheimnis bleibt",
    "pov": "Kap 23 · Sorel",
    "tz_tag": 175,
    "datum_text": "24. Lichtmond 551",
    "figur": "Sorel",
    "fakt": "sorel-bewusste-projektion",
    "stufe": "versteht",
    "detail": "Sorel weiß jetzt: er selbst formt das Licht auf den Platten. Versucht bewusst zu projizieren — Alphina zeigen, nicht zeigen. Beides misslingt halb. Er entscheidet, das Geheimnis zu behalten: dass die Projektionen Wochen zurückreichen. Das wird die Grenzverletzung in K25.",
    "buch": "B1",
    "kapitel_status": "szenenplan",
}

# Find first K24 event and insert K23 before it
for i, ev in enumerate(thal):
    if isinstance(ev, dict) and ev.get("kapitel") == "24":
        thal.insert(i, k23)
        break

# 5. Fix moragh: remove old I3, I7, and misplaced dornen event
moragh[:] = [
    ev
    for ev in moragh
    if not (
        isinstance(ev, dict)
        and (
            ev.get("kapitel") in ("I3", "I7")
            or (
                ev.get("titel", "").startswith("Alphinas Trauer wird Hass")
                and ev.get("pov", "").startswith("Kap 39")
            )
        )
    )
]

# 5b. Add proper K39 and K40 to moragh
k39 = {
    "tz": 551,
    "mz": 3635,
    "kapitel": "39",
    "typen": ["begegnung"],
    "titel": "Eine Moragh-Stadt — größere Menschen, purpurne Augen",
    "pov": "Kap 39 · Maren",
    "tz_tag": 275,
    "datum_text": "2. Nebelmond 551 — Moragh",
    "detail": "Maren POV. Eine Moragh-Stadt. Größere Menschen, dunkle Augen, feingliedrig. Ein älterer Mann mit purpurnen Augen mustert sie. Sagt in gebrochenem Thalassisch: 'Elke?' Führt sie durch die Stadt.",
    "buch": "B1",
    "kapitel_status": "szenenplan",
}

k40 = {
    "tz": 551,
    "mz": 3635,
    "kapitel": "40",
    "typen": ["begegnung", "schlüssel"],
    "titel": "Elkes Garten — Alphina bricht zusammen, Buch 1 Cliffhanger",
    "pov": "Kap 40 · Alphina",
    "tz_tag": 276,
    "datum_text": "3. Nebelmond 551 — Moragh",
    "figuren": ["Alphina", "Vesper", "Maren", "Runa", "Elke"],
    "intensitaet": "bekannt",
    "ort": "Moragh, Elkes Garten",
    "detail": "Ein Garten. Pflanzen aus beiden Welten. Eine Frau mit erdigen Händen. altes Thalassisch. 'Woher—' Alphina fällt auf die Knie. Sorel ist tot. Die Welt ist fremd. Und jemand spricht ihre Sprache.",
    "buch": "B1",
    "kapitel_status": "szenenplan",
}

# Insert before K41 (which is in thalassien) — append to moragh
moragh.append(k39)
moragh.append(k40)

# Also add the dornen event as part of K40
dornen = {
    "tz": 551,
    "mz": 3635,
    "kapitel": "40",
    "typen": ["erkenntnis", "tschechow"],
    "titel": "Alphinas Trauer wird Hass — Dornen statt Farne",
    "pov": "Kap 40 · Alphina",
    "tz_tag": 276,
    "datum_text": "3. Nebelmond 551 — Moragh",
    "detail": "Um sie herum wächst ein Kreis aus Dornen, nicht Farnen. Zum ersten Mal. Ihr Hass verändert ihre Resonanz.",
    "buch": "B1",
    "kapitel_status": "szenenplan",
}
moragh.append(dornen)

# ── 6. Tag fire event as I3 in TZ 154 section ──────────────────────────────
for monat in data["monate"]:
    if monat.get("label") == "MZ Monat -12":
        for ev in monat["events"].get("thalassien", []):
            if isinstance(ev, dict) and "Große Feuer" in ev.get("titel", ""):
                ev["kapitel"] = "I3"
                ev["pov"] = "I3 · Elke"
                ev["kapitel_status"] = "szenenplan"
                break
        break

# ── 7. Remove I9 from Buch 2 section ───────────────────────────────────────
for monat in data["monate"]:
    if monat.get("buch", "").startswith("Buch 2"):
        mo = monat["events"].get("moragh", [])
        mo[:] = [
            ev
            for ev in mo
            if not (isinstance(ev, dict) and ev.get("kapitel") == "I9")
        ]
        break

# ── 8. Add I4-I6 (Varen) to Buch 2 moragh ──────────────────────────────────
i4 = {
    "tz": None,
    "mz": 3635.05,
    "kapitel": "I4",
    "typen": ["schlüssel", "erkenntnis"],
    "titel": "Das Experiment — Varen zerstört drei Quellen",
    "pov": "I4 · Varen",
    "detail": "Rückblende. Varen unter Mar-Keth, drei Quellen, das Coupling-Experiment. Er will helfen — magiefreie Flächen besiedelbar machen. Durchschlag. Stille. Staub. 200.000 Menschen heimatlos. Kein Kalkül — Hybris. Velmar stößt ihn aus, verdeckt. Er steht allein in den Ruinen.",
    "buch": "B2",
    "kapitel_status": "szenenplan",
}

i5 = {
    "tz": None,
    "mz": 3636.35,
    "kapitel": "I5",
    "typen": ["erkenntnis", "erotik"],
    "titel": "Vierhundert Jahre — Elke weg, Portal-Forschung beginnt",
    "pov": "I5 · Varen",
    "detail": "Rückblende. Elke ist weg. Varen allein. Die Quellen sind tot, endgültig. Er findet die alten Portal-Aufzeichnungen. 350 Verschwundene vor 200 MZ-Jahren. Verbotene Magie. Er beginnt trotzdem. Lernt Thalassisch aus Elkes zurückgelassenen Notizbüchern. Ihr Name in seiner Handschrift. Vierhundert Jahre allein.",
    "buch": "B2",
    "kapitel_status": "szenenplan",
}

i6 = {
    "tz": None,
    "mz": 3637.25,
    "kapitel": "I6",
    "typen": ["erkenntnis", "schlüssel"],
    "titel": "Der Atem — Varen sieht Alphinas Farbe kippen",
    "pov": "I6 · Varen",
    "detail": "Gegenwart. Varen beobachtet durch Schemen wie der Bund Alphina zur Waffe schult. Er sieht ihre Farbe kippen — grün zu schwarz/rot. Dieselbe Überladung die er selbst ausgelöst hat, jetzt in einem Menschen. Er könnte warnen. Müsste sich offenbaren. Tut es nicht. Auf seiner Karte: die nächsten Quellen auf der Bund-Todesliste. Er entscheidet zu handeln.",
    "buch": "B2",
    "kapitel_status": "szenenplan",
}

# Insert I4 after B2-Akt I events, I5 after Akt II, I6 before Akt IV
# Find the Buch 2 months and insert
for monat in data["monate"]:
    label = monat.get("label", "")
    buch = monat.get("buch", "")
    mo = monat["events"].get("moragh", []) if "events" in monat else []

    if buch.startswith("Buch 2"):
        # I4 goes at start of B2 (after first few events = Akt I)
        # Insert after B2-04, before B2-07
        idx = 0
        for j, ev in enumerate(mo):
            if isinstance(ev, dict) and ev.get("kapitel") == "B2-07":
                idx = j
                break
        mo.insert(idx, i4)
        break

# I5 in MZ Monat 2 (after B2-16, before B2-18)
for monat in data["monate"]:
    if monat.get("label") == "MZ Monat 2":
        mo = monat["events"].get("moragh", [])
        idx = len(mo)
        for j, ev in enumerate(mo):
            if isinstance(ev, dict) and ev.get("kapitel") == "B2-18":
                idx = j
                break
        mo.insert(idx, i5)
        break

# I6 in MZ Monat 3 (before B2-25 = Quellen-Zerstörung)
for monat in data["monate"]:
    if monat.get("label") == "MZ Monat 3":
        mo = monat["events"].get("moragh", [])
        idx = len(mo)
        for j, ev in enumerate(mo):
            if isinstance(ev, dict) and ev.get("kapitel") == "B2-25":
                idx = j
                break
        mo.insert(idx, i6)
        break

# ── 9. Add I7-I9 (Maren) to Buch 3 ────────────────────────────────────────
i7 = {
    "tz": 651,
    "mz": 3635.25,
    "kapitel": "I7",
    "typen": ["schlüssel", "erkenntnis"],
    "titel": "Maren in Thalassien ~1910 — Ankunft in einer fremden Welt",
    "pov": "I7 · Maren",
    "detail": "Maren tritt durch das Portal in ein Vael das sie nicht erkennt. Elektrizität. Dampfschiffe. Automobile. Der Botanische Garten ist ein Park mit Eisengitter. Der Purpurstein im Steinkreis ist noch warm — der einzige Beweis. Sie trägt Kleidung von 1820. Der Anker existiert nicht mehr. An seiner Stelle ein Kontorhaus. Unter dem Pflaster, Hand aufgelegt — ein Herzschlag. Schwächer als damals.",
    "buch": "B3",
    "kapitel_status": "szenenplan",
}

i8 = {
    "tz": None,
    "mz": 3638.5,
    "kapitel": "I8",
    "typen": ["erkenntnis"],
    "titel": "Das Institut ~1960 — Maren altert, Vespers Brief",
    "pov": "I8 · Maren",
    "detail": "Maren ist alt. Das Schwellenforschungsinstitut hat 40 Mitarbeiter, einen Lehrstuhl, Messgeräte die Resonanz-Restfelder kartieren. Vael-Anomalien schwächer aber messbar. Sie hat alles aufgeschrieben — Vespers Ringe, die 4:33, das Boot, die Schemen. Die Wissenschaftler halten es für Mikrogravitations-Anomalien. Sie vermisst Vespers Hände. Schreibt ihm einen Brief den sie nie abschicken kann.",
    "buch": "B3",
    "kapitel_status": "szenenplan",
}

i9 = {
    "tz": None,
    "mz": 3640.0,
    "kapitel": "I9",
    "typen": ["schlüssel", "tschechow"],
    "titel": "Das Testament ~2200 — Marens letzter Eintrag, die Expedition beginnt",
    "pov": "I9 · Maren",
    "detail": "Maren ist lange tot. Ihr Portrait im Foyer. Eine junge Forscherin liest Marens letzten Eintrag: 'Der Stein ist kälter geworden. Aber er schlägt noch. Wenn ihr es schafft ihn zu öffnen — sagt Vesper, dass die Uhr auf dem Nachttisch immer noch null Drift hat.' Die Expedition wird vorbereitet. Resonanz-Mathematik die Maren nicht mehr erlebt hat. Sie öffnen das Portal. Auf der anderen Seite: Thar-Späher.",
    "buch": "B3",
    "kapitel_status": "szenenplan",
}

# I7: insert into Buch 3 thalassien section (Maren arrives ~1910)
# Find MZ Monat 3 which has Maren's arrival, add I7 there
for monat in data["monate"]:
    if monat.get("label") == "MZ Monat 3":
        th = monat["events"].get("thalassien", [])
        # Add I7 after the existing "Maren kommt an" event
        th.append(i7)
        break

# I8: find a suitable B3 section (after Akt II events)
for monat in data["monate"]:
    label = monat.get("label", "")
    if "3.639" in label or "3639" in label:
        th = monat["events"].setdefault("thalassien", [])
        th.append(i8)
        break
else:
    # If no matching section, add to the Buch 3 main section
    for monat in data["monate"]:
        if monat.get("buch") == "Buch 3: Die Quelle":
            th = monat["events"].setdefault("thalassien", [])
            th.append(i8)
            break

# I9: find section near Buch 3 Akt IV
for monat in data["monate"]:
    if monat.get("buch") == "Buch 3: Die Quelle":
        th = monat["events"].setdefault("thalassien", [])
        th.append(i9)
        break

# ── Write back ──────────────────────────────────────────────────────────────
with open(ZL_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✓ zeitleiste.json updated successfully")
print("  - TZ calendar added to meta")
print("  - Missing typen added (resonanz, gaensehaut, verabredung)")
print("  - All datum_text converted to fantasy month names")
print("  - K23 added")
print("  - K39/K40 thal duplicates removed, proper moragh events added")
print("  - I3 tagged on fire event in TZ 154")
print("  - Old I3/I7 removed from Buch 1 moragh")
print("  - I9 removed from Buch 2 moragh")
print("  - I4-I6 (Varen) added to Buch 2")
print("  - I7-I9 (Maren) added to Buch 3")
