#!/usr/bin/env python3
"""Fix status.json: update interludes and akt structure."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATUS = ROOT / "buch" / "status.json"

with open(STATUS, "r", encoding="utf-8") as f:
    data = json.load(f)

# ── Buch 1: Akte ──────────────────────────────────────────────────────────
b1 = data["buch1"]
b1["akte"] = [
    {
        "name": "Akt I",
        "kapitel": [
            "01", "02", "03", "04", "I1", "05", "06", "07", "08", "I2",
            "09", "10", "11", "12", "I3"
        ],
    },
    {
        "name": "Akt II",
        "kapitel": [
            "13", "14", "15", "16", "17", "18", "19", "20", "21", "22"
        ],
    },
    {
        "name": "Akt III",
        "kapitel": [
            "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33"
        ],
    },
    {
        "name": "Akt IV",
        "kapitel": [
            "34", "35", "36", "37", "38", "39", "40", "41"
        ],
    },
]

# ── Buch 1: Interludien ───────────────────────────────────────────────────
# Replace I3, delete I4-I9
for key in ["I4", "I5", "I6", "I7", "I8", "I9"]:
    if key in b1["kapitel"]:
        del b1["kapitel"][key]

b1["kapitel"]["I3"] = {
    "titel": "Das Grosse Feuer",
    "pov": "Elke",
    "status": "szenenplan",
    "woerter": None,
    "text": (
        "Varen schickt drei Feuer-Schemen durch den Riss. "
        "In Vael als Feuerdaemonen verstanden. Teile der Stadt brennen. "
        "Kaspar und Keldan sterben im Kampf. Elke oeffnet das Portal und "
        "geht durch nach Moragh. Lene ueberlebt allein, schreibt das Manuskript."
    ),
}

# ── Buch 2: Akte ──────────────────────────────────────────────────────────
b2 = data["buch2"]
b2["akte"] = [
    {
        "name": "Akt I",
        "titel": "Fremde Welt",
        "kapitel": [
            "01", "02", "03", "04", "I1", "05", "06", "07", "08", "09",
            "I2", "10"
        ],
    },
    {
        "name": "Akt II",
        "titel": "Die Fraktionen",
        "kapitel": [
            "11", "12", "13", "14", "I4", "15", "16", "17", "18", "19",
            "20", "20b"
        ],
    },
    {
        "name": "Akt III",
        "titel": "Gefangenschaft",
        "kapitel": [
            "21", "22", "23", "I5", "24", "25", "26", "27", "28"
        ],
    },
    {
        "name": "Akt IV",
        "titel": "Trennung",
        "kapitel": [
            "29", "30", "31", "I6", "32", "33", "34", "35", "36"
        ],
    },
]

# ── Buch 2: Interludien ───────────────────────────────────────────────────
# Remove old I1-I7, add new I4-I6
for key in ["I1", "I2", "I3", "I4", "I5", "I6", "I7"]:
    if key in b2["kapitel"]:
        del b2["kapitel"][key]

b2["kapitel"]["I4"] = {
    "titel": "Das Experiment",
    "pov": "Varen",
    "status": "idee",
    "woerter": None,
    "text": (
        "Rueckblende. Varen unter Mar-Keth, drei Quellen, das Coupling-Experiment. "
        "Er will helfen. Durchschlag. Stille. Staub. 200.000 Menschen heimatlos. "
        "Kein Kalkuel -- Hybris. Velmar stoesst ihn aus, verdeckt. Er steht allein "
        "in den Ruinen."
    ),
}

b2["kapitel"]["I5"] = {
    "titel": "Vierhundert Jahre",
    "pov": "Varen",
    "status": "idee",
    "woerter": None,
    "text": (
        "Rueckblende. Elke ist weg. Varen allein. Die Quellen sind tot, endgueltig. "
        "Er findet die alten Portal-Aufzeichnungen. 350 Verschwundene vor 200 MZ-Jahren. "
        "Verbotene Magie. Er beginnt trotzdem. Lernt Thalassisch aus Elkes "
        "zurueckgelassenen Notizbueechern. Ihr Name in seiner Handschrift. "
        "Vierhundert Jahre allein."
    ),
}

b2["kapitel"]["I6"] = {
    "titel": "Der Atem",
    "pov": "Varen",
    "status": "idee",
    "woerter": None,
    "text": (
        "Gegenwart. Varen beobachtet durch Schemen wie der Bund Alphina zur Waffe "
        "schult. Er sieht ihre Farbe kippen -- gruen zu schwarz/rot. Dieselbe "
        "Ueberladung die er selbst ausgeloest hat, jetzt in einem Menschen. Er koennte "
        "warnen. Muesste sich offenbaren. Tut es nicht. Auf seiner Karte: die "
        "naechsten Quellen auf der Bund-Todesliste. Er entscheidet zu handeln."
    ),
}

# ── Buch 3: Akte ──────────────────────────────────────────────────────────
b3 = data["buch3"]
b3["akte"] = [
    {
        "name": "Akt I",
        "titel": "Technologie",
        "kapitel": [
            "41", "42", "43", "44", "I7", "45", "46", "47", "48"
        ],
    },
    {
        "name": "Akt II",
        "titel": "Kulturkampf",
        "kapitel": [
            "49", "50", "51", "52", "53", "I8", "54", "55", "56"
        ],
    },
    {
        "name": "Akt III",
        "titel": "Quellen und Verlust",
        "kapitel": [
            "57", "58", "59", "60", "I9", "61", "62", "63"
        ],
    },
    {
        "name": "Akt IV",
        "titel": "Die Wahl",
        "kapitel": [
            "64", "65", "66", "67", "68", "69", "EP"
        ],
    },
]

# ── Buch 3: Interludien ───────────────────────────────────────────────────
# Remove old I9-I14, add new I7-I9
for key in ["I9", "I10", "I11", "I12", "I13", "I14"]:
    if key in b3["kapitel"]:
        del b3["kapitel"][key]

b3["kapitel"]["I7"] = {
    "titel": "Die Ankunft",
    "pov": "Maren",
    "status": "idee",
    "woerter": None,
    "text": (
        "~1910. Maren tritt durch das Portal in ein Vael das sie nicht erkennt. "
        "Elektrizitaet. Dampfschiffe. Automobile. Der Botanische Garten ist ein Park "
        "mit Eisengitter. Der Purpurstein im Steinkreis ist noch warm -- der einzige "
        "Beweis. Sie traegt Kleidung von 1820. Der Anker existiert nicht mehr. "
        "Unter dem Pflaster, Hand aufgelegt -- ein Herzschlag. Schwaecher als damals."
    ),
}

b3["kapitel"]["I8"] = {
    "titel": "Das Institut",
    "pov": "Maren",
    "status": "idee",
    "woerter": None,
    "text": (
        "~1960. Maren ist alt. Das Schwellenforschungsinstitut hat 40 Mitarbeiter, "
        "einen Lehrstuhl, Messgeraete die Resonanz-Restfelder kartieren. Vael-Anomalien "
        "schwaecher aber messbar. Sie vermisst Vespers Haende. Schreibt ihm einen Brief "
        "den sie nie abschicken kann."
    ),
}

b3["kapitel"]["I9"] = {
    "titel": "Das Testament",
    "pov": "Maren",
    "status": "idee",
    "woerter": None,
    "text": (
        "~2200. Maren ist lange tot. Ihr Portrait im Foyer. Eine junge Forscherin "
        "liest Marens letzten Eintrag: 'Der Stein ist kaelter geworden. Aber er "
        "schlaegt noch. Wenn ihr es schafft ihn zu oeffnen -- sagt Vesper, dass die "
        "Uhr auf dem Nachttisch immer noch null Drift hat.' Die Expedition wird "
        "vorbereitet. Sie oeffnen das Portal. Auf der anderen Seite: Thar-Spaeher."
    ),
}

# ── Write ──────────────────────────────────────────────────────────────────
with open(STATUS, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("status.json updated successfully")
print("  B1: I1, I2, I3 (Elke)")
print("  B2: I4, I5, I6 (Varen)")
print("  B3: I7, I8, I9 (Maren)")
