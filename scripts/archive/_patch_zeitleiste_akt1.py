"""
Einmal-Skript: Pflegt Akt-1-Events in buch/zeitleiste.json nach.

- Ergaenzt tz_tag + datum_text an bestehenden Events fuer Kap 1-11, I1, I2
- Korrigiert die Akt-1-Grenze: Alt-Kap 12 (Alphina+Sorel Erste Begegnung) -> Neu-Kap 11
- Fuegt wohnort / begegnung / wissen Events fuer Akt 1 hinzu
- Sortiert die thalassien-Event-Liste in monat[10] nach (tz_tag, kapitel-position)
- Schreibt JSON mit indent=2 zurueck (reformatiert die Datei einheitlich)

Soll nach einmaligem Lauf geloescht oder archiviert werden.
"""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ZEITLEISTE = REPO / "buch" / "zeitleiste.json"
STATUS = REPO / "buch" / "status.json"

# Tagesplan (Option B, 6 Wochen Akt 1)
TAGE = {
    "01": (80, "21. März"),
    "02": (80, "21. März"),
    "03": (80, "21. März"),
    "04": (95, "5. April"),
    "I1": (None, "1423 (Interludium)"),  # eigene Zeit
    "05": (88, "29. März"),
    "06": (95, "5. April"),
    "07": (100, "10. April"),
    "08": (107, "17. April"),
    "I2": (None, "1423 (Interludium)"),
    "09": (115, "25. April"),
    "10": (120, "30. April"),
    "11": (125, "5. Mai"),
}


def with_tage(event):
    """Setzt tz_tag / datum_text an einem Event basierend auf seinem kapitel-Feld."""
    kap = event.get("kapitel")
    if kap in TAGE:
        tag, text = TAGE[kap]
        if tag is not None:
            event["tz_tag"] = tag
        event["datum_text"] = text
    return event


# ---------------------------------------------------------------------------
# Neue Events fuer Akt 1 (Kap 1-11 + I1, I2)
# ---------------------------------------------------------------------------

def make_event(kapitel, typen, titel, **kwargs):
    """Baut ein Event mit tz/mz/kapitel/typen/titel plus Zusatzfelder."""
    tag, text = TAGE.get(kapitel, (None, ""))
    ev = {
        "tz": 551,
        "mz": 0,
        "kapitel": kapitel,
        "typen": typen,
        "titel": titel,
    }
    if tag is not None:
        ev["tz_tag"] = tag
    if text:
        ev["datum_text"] = text
    ev.update(kwargs)
    return ev


# WOHNORT-EVENTS
# Vor Vael: die Herkunftsorte (aus den ersten Kapiteln)
# In Vael: die tatsaechlichen Quartiere

WOHNORT_EVENTS = [
    # Ausgangsorte (Kap 1-4 POV-Heimat)
    make_event("01", ["wohnort"],
               "Alphina wohnt in Velde",
               figur="Alphina",
               ort="Wohnung im vierten Stock, chaotisch, grün",
               stadt="Velde"),
    make_event("02", ["wohnort"],
               "Sorel wohnt in Nachtholm",
               figur="Sorel",
               ort="Kellerwohnung in der Schluchtstadt, Dunkelkammer",
               stadt="Nachtholm"),
    make_event("03", ["wohnort"],
               "Vesper wohnt in Karst",
               figur="Vesper",
               ort="Werkstatt, zwei Räume, Schlafraum schmal wie eine Schublade",
               stadt="Karst"),

    # Vael-Quartiere
    make_event("04", ["wohnort"],
               "Maren bezieht den Anker",
               figur="Maren",
               ort="Gasthaus Zum Anker, Hafengasse",
               stadt="Vael",
               detail="Der Wirt — breit, grau, Kinn aus Purpurstein — gibt ihr einen Schlüssel und fragt nicht wie lange sie bleibt."),
    make_event("05", ["wohnort"],
               "Alphina bezieht den Anker",
               figur="Alphina",
               ort="Gasthaus Zum Anker, Hafengasse",
               stadt="Vael",
               detail="Kleines Zimmer, drei Schritte breit. Wochenpreis im Voraus."),
    make_event("06", ["wohnort"],
               "Sorel bezieht das Lichthaus",
               figur="Sorel",
               ort="Lichthaus am Hafen, Speichergebäude, Keller als Dunkelkammer",
               stadt="Vael",
               detail="Keller riecht nach Fixierer und Salz."),
    make_event("07", ["wohnort"],
               "Vesper bezieht den Anker",
               figur="Vesper",
               ort="Gasthaus Zum Anker, Hafengasse, zweiter Stock",
               stadt="Vael",
               detail="Selber Wirt, selbes Haus wie Alphina und Maren. Arbeitet tagsüber im Tidemoor-Haus an der Standuhr."),
]


# BEGEGNUNG-EVENTS
BEGEGNUNG_EVENTS = [
    make_event("03", ["begegnung"],
               "Vesper trifft den reisenden Uhrmacher",
               figuren=["Vesper", "Reisender Uhrmacher"],
               intensitaet="fluechtig",
               ort="Gasthaus in Karst",
               detail="Alte Wörter, seltsamer Akzent. Erwähnt die 4:33-Standuhr in Vael. Tschechow fuer Buch 2."),
    make_event("04", ["begegnung"],
               "Maren trifft Edric Dahl",
               figuren=["Maren", "Edric Dahl"],
               intensitaet="bekannt",
               ort="Werft Dahl, Grauküste",
               detail="Edric zeigt die Werft, erklärt das Boot, Harons Gewohnheiten. 'Ist nachts in den Garten gegangen.'"),
    make_event("05", ["begegnung"],
               "Alphina trifft Runa Kvist",
               figuren=["Alphina", "Runa Kvist"],
               intensitaet="fluechtig",
               ort="Druckerei in Vael, Oberstadt",
               detail="Alphina kauft Papier. Runa warme Hände, lacht zu laut für Vael, gibt Alltagstipps (Bäcker Sievert, Untere Grauwe meiden)."),
    make_event("08", ["begegnung"],
               "Maren trifft Tohl Daverin",
               figuren=["Maren", "Tohl Daverin"],
               intensitaet="bekannt",
               ort="Hafen Vael",
               detail="Tohl, alt, Gesicht wie Treibholz. 'Die Grauwe ist falsch.' Zeigt das rückwärts fließende Wasser."),
    make_event("09", ["begegnung"],
               "Alphina trifft Runa im Botanischen Garten",
               figuren=["Alphina", "Runa Kvist"],
               intensitaet="bekannt",
               ort="Botanischer Garten, Vael",
               detail="Runa druckt Flugblätter über die Phänomene. Alphina registriert Runas warme Hände als mehr als Handwerksgeschick."),
    make_event("11", ["begegnung"],
               "Alphina trifft Sorel im Botanischen Garten",
               figuren=["Alphina", "Sorel"],
               intensitaet="fluechtig",
               ort="Botanischer Garten, Nacht",
               detail="Drei Sätze: 'Die Pflanzen bewegen sich.' — 'Ja.' — 'Seit wann?' — 'Immer.' Keine Namen. Ende Akt 1."),
]


# WISSEN-EVENTS
WISSEN_EVENTS = [
    # Alphina
    make_event("01", ["wissen"],
               "Alphina: Farn dreht sich nach ihr",
               figur="Alphina", fakt="pflanzen-reagieren-auf-mich", stufe="gesehen",
               detail="3 Uhr morgens, der Farn dreht seinen Wedel zurück als sie wegschaut. Zehn Minuten Test."),
    make_event("05", ["wissen"],
               "Alphina: Kaminfeuer ohne Brennstoff",
               figur="Alphina", fakt="kaminfeuer-ohne-brennstoff", stufe="gesehen",
               detail="Erste Nacht im Anker. Feuer brennt AUF den Scheiten, nicht aus ihnen. Morgens keine Asche."),
    make_event("05", ["wissen"],
               "Alphina: Schattentiere in Vael",
               figur="Alphina", fakt="schattentiere-in-vael", stufe="gesehen",
               detail="Aus dem Fenster: katzengroß, falsch proportioniert, leuchtende Augen."),
    make_event("09", ["wissen"],
               "Alphina: Pflanzen folgen ihr systematisch",
               figur="Alphina", fakt="pflanzen-reagieren-auf-mich", stufe="versteht",
               detail="27 Pflanzen im Botanischen Garten, alle auf sie gerichtet. Mannshohe Farne im späten Frühling. Asplenium aus der Fußnote — hier."),
    make_event("09", ["wissen"],
               "Alphina: Schemen folgen ihr persönlich",
               figur="Alphina", fakt="schemen-folgen-mir-persoenlich", stufe="ahnt",
               detail="Drei Schattentiere folgen ihr durch Gassen und auf Dächern. Nicht Runa, nicht anderen — nur ihr. Jemand beobachtet sie DURCH die Tiere."),
    make_event("11", ["wissen"],
               "Alphina: Pochen unter dem Garten",
               figur="Alphina", fakt="pochen-unter-vael", stufe="gesehen",
               detail="Hand auf den Boden des Steinkreises im Garten. Pochen wie unter Marens Werft — aber Alphina kennt Maren nicht. Die Stadt atmet."),

    # Sorel
    make_event("02", ["wissen"],
               "Sorel: Sein eigenes Gesicht auf fremder Glasplatte",
               figur="Sorel", fakt="sein-gesicht-auf-vael-platte", stufe="gesehen",
               detail="Platte 7 aus der Vael-Auktion. Sein Gesicht, Stadt die er nie betreten hat, Bild älter als er. Dreizehn Jahre Suche."),
    make_event("02", ["wissen"],
               "Sorel: Hinweis Vael Lichthaus Keller",
               figur="Sorel", fakt="lichthaus-keller-vael", stufe="gesehen",
               detail="Rückseite der Platte, verblasste Tinte."),
    make_event("06", ["wissen"],
               "Sorel: Kratzspuren am Hafenpoller",
               figur="Sorel", fakt="kratzspuren-heisse-schnitte", stufe="gesehen",
               detail="Ein Tier beobachtet ihn, verschwindet. Am Poller: tiefe, saubere Kratzspuren wie mit heißem Messer durch Holz geschnitten."),
    make_event("10", ["wissen"],
               "Sorel: Die Kamera fängt Schemen ein",
               figur="Sorel", fakt="kamera-faengt-schemen-ein", stufe="gesehen",
               detail="Erste Vael-Platten: Hafen bei Nacht zeigt schattenhafte Gestalt mit leuchtenden Augen die er nicht gesehen hat. Zweite Platte: Frau mit Farnen, die er nicht fotografiert hat."),

    # Vesper
    make_event("07", ["wissen"],
               "Vesper: Standuhr verliert 4:33 pro Tag",
               figur="Vesper", fakt="standuhr-4-33", stufe="gesehen",
               detail="Tidemoor-Haus. Gehäuse, Messing, Pendel mechanisch perfekt. Jeder Zahnrad geprüft, keine Erklärung."),
    make_event("07", ["wissen"],
               "Vesper: Die Uhr reagiert auf seine Hand",
               figur="Vesper", fakt="standuhr-reagiert-auf-mich", stufe="gesehen",
               detail="Hand drauf: Null Verlust. Hand weg: 4:33 wieder."),
    make_event("07", ["wissen"],
               "Vesper: Heißes Wasser ohne Kessel",
               figur="Vesper", fakt="heisses-wasser-ohne-kessel", stufe="gesehen",
               detail="Tidemoor-Bad. Keine Warmwasseranlage im Haus, Rohre kalt. Wasser aus der Leitung dampfend heiß."),
    make_event("07", ["wissen"],
               "Vesper: Kratzspuren am Kellerfenster",
               figur="Vesper", fakt="kratzspuren-heisse-schnitte", stufe="gesehen",
               detail="Nachts Kratzen im Keller. Spuren am Kellerfenster — dieselben sauberen, heißen Schnitte wie an Sorels Poller."),

    # Maren
    make_event("04", ["wissen"],
               "Maren: Haron ging nachts in den Garten",
               figur="Maren", fakt="haron-nachtgaenge-garten", stufe="gesehen",
               detail="Edric erzählt es: 'Hat nie gesagt warum.' Tschechow-Setup."),
    make_event("04", ["wissen"],
               "Maren: Das Boot ist dreiviertel fertig",
               figur="Maren", fakt="boot-dreiviertel-fertig", stufe="gesehen",
               detail="Haron hat es gebaut und ist gestorben. Kein Umschlag, keine Karte."),
    make_event("08", ["wissen"],
               "Maren: Das Boot wächst nachts weiter",
               figur="Maren", fakt="boot-waechst-nachts", stufe="gesehen",
               detail="Neue Holzspäne am Morgen. Planken die gestern nicht da waren. Sie misst, prüft, hält sich für verrückt, dann wartet sie nachts."),
    make_event("08", ["wissen"],
               "Maren: Schemen arbeiten am Boot",
               figur="Maren", fakt="schemen-am-boot", stufe="gesehen",
               detail="Zwei Uhr morgens. Drei schattenhafte Gestalten, humanoid, Haut raucht, schwarze leuchtende Augen. Arbeiten ohne Geräusch. Sehen sie nicht oder ignorieren sie. Nach einer Stunde lösen sie sich auf."),
    make_event("08", ["wissen"],
               "Maren: Wasser fließt rückwärts in die Werft",
               figur="Maren", fakt="wasser-fliesst-rueckwaerts", stufe="gesehen",
               detail="Tohl zeigt es. Gegen das Gefälle. 'Seit drei Wochen. Erst nur nachts. Jetzt auch tagsüber.'"),
    make_event("08", ["wissen"],
               "Maren: Pochen unter der Werft",
               figur="Maren", fakt="pochen-unter-vael", stufe="gesehen",
               detail="Nachts, einmal, wie ein Herzschlag. Dasselbe Pochen das Alphina später unter dem Garten-Steinkreis spürt."),
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    with open(ZEITLEISTE, encoding="utf-8") as f:
        z = json.load(f)

    m10 = z["monate"][10]
    assert "Buch 1" in m10.get("label", ""), f"Erwartete Buch 1 in monat[10], fand: {m10.get('label')}"

    thal = m10["events"]["thalassien"]

    # 1) Alte Kap-12 (Alphina+Sorel Erste Begegnung) auf Kap 11 umstellen
    #    und aus dem Text loeschen, weil er vom neuen begegnung-Event ersetzt wird
    patched = []
    alt_akt1_grenz_event_entfernt = False
    for ev in thal:
        kap = ev.get("kapitel")
        if kap == "12" and "Garten" in ev.get("titel", "") and "Alphina" in ev.get("titel", ""):
            # Alt-Kap 12 (Erste Begegnung) verwerfen -> wird durch neues begegnung-Event fuer Kap 11 ersetzt
            alt_akt1_grenz_event_entfernt = True
            continue
        patched.append(ev)
    thal = patched

    # 2) tz_tag / datum_text an bestehende Kap 1-11 Events ergaenzen
    for ev in thal:
        kap = ev.get("kapitel")
        if kap in TAGE:
            tag, text = TAGE[kap]
            if tag is not None and "tz_tag" not in ev:
                ev["tz_tag"] = tag
            if text and "datum_text" not in ev:
                ev["datum_text"] = text

    # 3) Neue Events hinzufuegen (wohnort, begegnung, wissen)
    #    Nicht duplizieren: pruefen ob schon vorhanden via (kapitel, titel)-Key
    existing_keys = {(e.get("kapitel"), e.get("titel")) for e in thal}
    new_events = WOHNORT_EVENTS + BEGEGNUNG_EVENTS + WISSEN_EVENTS
    added = 0
    for ev in new_events:
        key = (ev["kapitel"], ev["titel"])
        if key not in existing_keys:
            thal.append(ev)
            existing_keys.add(key)
            added += 1

    # 4) Sortieren: nach tz_tag (fehlt -> 999 ans Ende), dann nach kapitel-Lesereihenfolge
    #    Lesereihenfolge aus status.json laden
    with open(STATUS, encoding="utf-8") as f:
        status = json.load(f)
    reihenfolge = []
    for akt in status["buch1"]["akte"]:
        reihenfolge.extend(akt["kapitel"])
    pos_map = {k: i for i, k in enumerate(reihenfolge)}

    def sortkey(e):
        tag = e.get("tz_tag", 999)
        kap = e.get("kapitel", "")
        pos = pos_map.get(kap, 999)
        return (tag, pos)

    thal.sort(key=sortkey)
    m10["events"]["thalassien"] = thal

    # 5) Zurueckschreiben
    with open(ZEITLEISTE, "w", encoding="utf-8") as f:
        json.dump(z, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"OK: {added} neue Events hinzugefuegt.")
    print(f"    Alt-Kap12-Event entfernt: {alt_akt1_grenz_event_entfernt}")
    print(f"    thalassien-Events in monat[10] jetzt: {len(thal)}")


if __name__ == "__main__":
    main()
