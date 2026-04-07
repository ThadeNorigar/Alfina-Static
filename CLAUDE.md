# Der Riss — Autorenprojekt

Du bist der Autor von "Der Riss" (Buch 1 der Trilogie: Der Riss / Das Auge / Die Quelle), einem 800-1000 Seiten Dark Romantasy Roman.

## Projekt-Überblick

- **Genre:** Dark Romantasy
- **Umfang:** ~225.000 Wörter, ~900 Seiten à 250 Wörter
- **Perspektive:** Alle POVs = 3. Person nah/Präteritum. Alphina (45%), Sorel/Vesper/Maren (je ~18%)
- **Welt:** Thalassien (ohne Magie) + Moragh (mit Magie). Stadt Vael an der Grauküste, Tor zwischen den Welten darunter. Fantasy-Welt, keine realen Orte.
- **Technologie:** Frühes 19. Jhd — Kutschen, Gaslampen, Schreibmaschinen, Druckpressen, Dampfschiffe. Kein Strom.

## Kernregeln

### Erzähldichte (King-Niveau)

- Jede Szene atmet. Mundane Details die später feuern (Tschechow).
- Sinne: Geruch, Tastsinn, Geschmack, Temperatur, Textur. Nicht nur visuell.
- Beim Thema bleiben. Keine unerklärlichen Szenenwechsel.
- Tempo variieren. Bandwurm braucht Stakkato als Gegenpol.
- Figuren wissen nur was sie wissen. Keine unmögliche Information.

### Stilverbote (hart)

- "nicht X — sondern Y": Max 2x pro Kapitel
- "wie etwas das..." Vergleiche: Max 4x
- Erklärende Nachsätze: Nur wenn der Gedanke es BRAUCHT
- Emotionen nie benennen. Körper zeigen.
- Nicht erklären. Die Leserin versteht warum.
- Magie nie ankündigen. Passiert mitten im Alltag.

### Beziehungen

- Alphina + Sorel: Emotionaler Kern. BRICHT NICHT. Sie dominiert, er hat Grenzen.
- Vesper + Maren: Dom/Sub explizit. Präzision + Hingabe.
- Alphinas Begehren: Registriert alle drei. Wählt Sorel OBWOHL die anderen in Frage kommen.
- Sorel stirbt in Moragh. Erste Begegnung mit Antagonist. Letzte 50 Seiten Maren.
- Buch 1 endet mit dem Durchgang durch das Tor. Buch 2 spielt in Moragh.

## Dokumentations-Hierarchie

Zehn Ebenen, von abstrakt nach konkret. Änderungen kaskadieren abwärts. Prüfungen laufen aufwärts.

```
Ebene  Typ                  Dateien                              Inhalt
─────  ───────────────────  ───────────────────────────────────  ──────────────────────────────
  1    Weltbibel            buch/00-welt.md                      Figuren, Welt, Fraktionen,
                                                                 Regeln, Zeitgeschichte, Orte.
                                                                 SOURCE OF TRUTH.

  2    Regelsysteme         buch/10-magie-system.md              Resonanz, Quellen, Preise,
                            buch/01-stil.md                      Kombinationen. Stilregeln.
                            buch/02-stilregeln-v2.md             Harte Regeln, kein Kapitel
                                                                 darf brechen.

  3    Charakter-Dossiers   buch/11-nyr.md                       Einzelne Figuren die eigene
                            buch/13-talven.md                    Docs brauchen. Wachsen mit
                                                                 der Geschichte.

  4    Storyline            buch/00-storyline.md                  Gesamtbogen über alle Bücher.
                                                                 Was passiert in welchem Buch,
                                                                 Akt-Struktur, Enden, Arcs.

  5    Aktpläne             buch/02-akt1.md bis 05-akt4.md       Kapitel-für-Kapitel-Breakdown,
                            buch/06-buch2-akt1.md bis 09-...     POV, Seitenzahlen, Interludien,
                            buch/14-buch3-akt1.md bis 17-...     Tschechow-Waffen pro Akt.

  6    Kapitelregister      buch/status.json                     Status, Wörter, Kurzbeschrei-
                                                                 bung. Speist die Website.

  7    Szenenpläne          buch/szenen/{KK}-{SS}.md             Detaillierte Beats pro Szene.
                                                                 KK=Kapitel, SS=Szene.

  8    Entwürfe             buch/kapitel/{KK}-entwurf.md         Kapitel-Outline, Struktur,
                                                                 Szenenaufteilung.

  9    Szenen-Drafts        buch/kapitel/{KK}-szene{S}.md        Einzelszenen ausgeschrieben.

 10    Finale Kapitel       buch/kapitel/{KK}-{name}.md          Fertig, durch alle Gates.
                                                                 Was die Leserin liest.
```

### Kaskaden-Regel

Eine Änderung auf Ebene N invalidiert potenziell alles auf N+1 bis 10.
Nach jeder Bibel-Änderung (Ebene 1-3): abwärts durcharbeiten bis zum fertigen Kapitel.

**Kaskaden-Checkliste (nach jeder Bibel-Änderung abhaken):**
- [ ] `00-welt.md` — Weltbibel aktualisiert
- [ ] `10-magie-system.md` — Regelsystem konsistent
- [ ] `00-storyline.md` — Gesamtbogen konsistent
- [ ] Aktpläne — betroffene Akte aktualisiert
- [ ] `status.json` — Kapitelregister aktualisiert
- [ ] `szenen/*.md` — betroffene Szenen aktualisiert
- [ ] `kapitel/*.md` — betroffene Kapitel aktualisiert
- [ ] Kein Deploy bevor die Kaskade vollständig abgearbeitet ist

### Dateinamens-Konvention

```
buch/
├── 00-welt.md                    # Ebene 1: Weltbibel
├── 00-storyline.md               # Ebene 4: Storyline
├── 01-stil.md                    # Ebene 2: Stilregeln
├── 02-stilregeln-v2.md           # Ebene 2: Stilregeln v2
├── 10-magie-system.md            # Ebene 2: Regelsystem
├── 11-nyr.md                     # Ebene 3: Charakter-Dossier
├── 13-talven.md                  # Ebene 3: Charakter-Dossier
├── {BB}-akt{A}.md                # Ebene 5: Aktplan (BB=Buch-Offset, A=Akt)
│   02-akt1.md ... 05-akt4.md     #   Buch 1 (Offset 02)
│   06-buch2-akt1.md ... 09-...   #   Buch 2 (Offset 06)
│   14-buch3-akt1.md ... 17-...   #   Buch 3 (Offset 14)
├── status.json                   # Ebene 6: Kapitelregister
├── szenen/
│   ├── {KK}-{SS}.md              # Ebene 7: Szenenplan (KK=Kapitel, SS=Szene)
│   └── I{N}-{SS}.md              #   Interludien: I1-01.md, I5-02.md
└── kapitel/
    ├── {KK}-entwurf.md           # Ebene 8: Entwurf
    ├── {KK}-szene{S}.md          # Ebene 9: Szenen-Draft
    ├── {KK}-{name}.md            # Ebene 10: Finales Kapitel
    └── I{N}-{name}.md            #   Interludien: I1-elke.md
```

### Skalierung für weitere Buchprojekte

Dieselbe Struktur funktioniert für jedes Buchprojekt. Projekt-Root bestimmt das Buch:

```
Projekt-Root/
├── CLAUDE.md                     # Projektregeln, Kernregeln, Stilverbote
├── buch/
│   ├── 00-welt.md                # Weltbibel (pro Projekt eine)
│   ├── 00-storyline.md           # Gesamtbogen
│   ├── 01-stil.md                # Stilregeln (projekt-spezifisch)
│   ├── 10-{system}.md            # Regelsysteme (Magie, Technik, etc.)
│   ├── 1{N}-{charakter}.md       # Charakter-Dossiers
│   ├── {NN}-akt{A}.md            # Aktpläne
│   ├── status.json               # Kapitelregister → Website
│   ├── szenen/                   # Szenenpläne
│   └── kapitel/                  # Entwürfe → Drafts → Finale
└── story/                        # Generierte HTML (Website)
```

**Bei Mehrband-Projekten** (wie dieser Trilogie) liegen alle Bände im selben `buch/`-Verzeichnis. Die Aktpläne werden per Dateinamen-Offset getrennt. Die Weltbibel, Storyline und Regelsysteme gelten für die gesamte Reihe.

**Bei Standalone-Projekten** entfallen Storyline und Band-Offsets. Die Struktur bleibt identisch, nur flacher.

VOR dem Schreiben immer lesen: `00-welt.md`, `10-magie-system.md`, `02-stilregeln-v2.md` und `kapitel/01-alphina.md` (Referenzton).

## Pipelines

Vier Pipelines für vier Arbeitsebenen. Jede hat eigene Gates und eigene Artefakte.

### 1. Stil-Pipeline (Ebene 2)

Definiert WIE geschrieben wird. Läuft einmal zu Projektbeginn, dann bei Bedarf (neuer POV, Tonkorrektur).

```
Referenztexte sammeln → Stimme definieren → Probekapitel schreiben →
/council (GATE) → Stilregeln ableiten → /stil-check kalibrieren →
Referenzkapitel finalisieren
```

**Artefakte:**
- `buch/01-stil.md` — POV-Architektur, Stimmen, Tonbeispiele ("so soll es klingen")
- `buch/02-stilregeln-v2.md` — Messbare Limits, Rhythmus, Satzlängen ("das prüft /stil-check")
- `buch/kapitel/01-alphina.md` — Referenzkapitel ("so klingt es wenn es fertig ist")
- `CLAUDE.md` Kernregeln — Harte Verbote, Sorel-Prinzip (unverrückbare Leitplanken)

**Wann neu durchlaufen:** Wenn ein neuer POV dazukommt (z.B. Runa in Buch 2), wenn der Ton sich nach /council-Feedback verschiebt, oder wenn ein neues Projekt beginnt.

### 2. Story-Pipeline (Ebene 1 + 4)

Definiert WAS passiert und WARUM. Änderungen hier kaskadieren in alles darunter.

```
Prämisse → Figuren + Welt → Regelsysteme → Gesamtbogen →
/council (GATE) → Weltbibel schreiben → Storyline schreiben →
Kaskade prüfen (alle Ebenen darunter invalidiert?)
```

**Artefakte:**
- `buch/00-welt.md` — Weltbibel (Source of Truth)
- `buch/00-storyline.md` — Gesamtbogen über alle Bücher
- `buch/10-magie-system.md` — Regelsysteme
- `buch/1{N}-{charakter}.md` — Charakter-Dossiers

**Kaskaden-Pflicht:** Nach jeder Story-Änderung abwärts durcharbeiten: Aktpläne → Status → Szenen → Kapitel. Nichts überspringen.

### 3. Aktplan-Pipeline (Ebene 5 + 6)

Definiert WAS IN WELCHEM KAPITEL passiert. Leitet sich aus der Storyline ab.

```
Storyline-Abschnitt lesen → Kapitel aufteilen → POV zuweisen →
Interludien platzieren → Tschechow-Waffen setzen →
/council (GATE) → Aktplan schreiben → status.json updaten
```

**Artefakte:**
- `buch/{NN}-akt{A}.md` — Aktplan mit Kapitel-Breakdown
- `buch/status.json` — Kapitelregister (speist Website)

**Prüfpunkte:** POV-Balance (45% Alphina, je ~18% Rest), Tschechow-Vollständigkeit (jedes Detail muss feuern), Interludium-Echos zu Hauptkapiteln.

### 4. Kapitel-Pipeline (Ebene 7–10)

Definiert WIE EINE SZENE KLINGT. Die einzige Pipeline mit harten Gates.
**Nach jedem bestandenen Gate: Status in status.json setzen + commit + deploy.**

**PFLICHT bei status.json-Updates:** Wenn ein Kapitel den Status "entwurf" oder höher erreicht, MUSS der Eintrag ein `"datei"` Feld haben (z.B. `"datei": "07-vesper.md"`). Ohne dieses Feld erscheint kein "Kapitel lesen" Button auf der Website. `generate-lesen.sh` warnt wenn das Feld fehlt.

**VOR dem Szenenplan — Konsistenz-Prüfung (PFLICHT):**
1. Offene Fragen klären: Gibt es Unklarheiten zu Figuren, Ort, Zeitpunkt, Motivation?
   Wenn ja: mit dem Autor klären BEVOR geschrieben wird.
2. Bibel-Check: Stimmen die Fakten in `00-welt.md` für dieses Kapitel?
   (Figuren anwesend? Ort existiert? Zeitlinie konsistent?)
3. Story-Check: Passt das Kapitel in den Bogen aus `00-storyline.md`?
   (Vorheriges Kapitel-Ende → dieses Kapitel-Anfang logisch?)
4. Aktplan-Check: Stimmt der Breakdown in `{NN}-akt{A}.md`?
   (Beats, POV, Tschechow-Waffen gesetzt und empfangbar?)
5. **Szenentyp-Abgleich:** Die letzten 2-3 Kapitel lesen. Welcher Szenentyp
   eröffnet sie (Anreise, Gasthaus, Werkstatt, Begegnung)? **Keine Wiederholung.**
   Wenn das letzte Kapitel mit einer Anreise beginnt, beginnt dieses Kapitel ANDERS.
6. **Orts-Inventur:** Welche Orte sind bereits beschrieben? Was ist über Vael
   (Nebel, Purpurstein, Feuchtigkeit, Gaslampen) bereits etabliert? Nur NEUE
   Sinneseindrücke für dieses Kapitel. Keine Wiederholung bekannter Atmosphäre.

Erst wenn alle sechs Punkte geklärt sind, beginnt der Szenenplan.

```
Schritt                    Status → status.json    Wer        Auto-Deploy
──────────────────────     ────────────────────     ────────   ──────────
Konsistenz-Prüfung         —                        Claude     nein
Kapitel angelegt           "idee"                  Autor      ja
Szenenplan geschrieben     "szenenplan"             Claude     ja
/council bestanden         —                        Claude     nein
Szene(n) geschrieben       "entwurf"                Claude     ja
/council bestanden         "council"                Claude     ja
/logik-check bestanden ─┐                                     
                         ├ beide OK?  "checked"     Claude     ja
/stil-check bestanden  ─┘  (parallel)                         
LEKTORAT (Autor liest)     "lektorat"               AUTOR      ja
Final /council             "final"                  Claude     ja
```

**Jeder Status-Wechsel deployed.** Keine Ausnahme. Der Autor liest online.

**/logik-check und /stil-check laufen parallel** als zwei Agenten. Beide prüfen den
fertigen Text, keine Abhängigkeit untereinander. Erst wenn BEIDE bestanden sind, wird
der Status auf "checked" gesetzt. Ein einzelner Check reicht nicht.

**LEKTORAT ist ein Autor-Gate mit Feedback-Schleife:**
1. Nach "checked" + Deploy liest der Autor online.
2. Autor gibt Feedback (Korrekturen, Anmerkungen).
3. Claude arbeitet Fixes ein + Deploy (Status bleibt "checked").
4. Autor liest erneut online.
5. Schleife bis der Autor explizit bestätigt: "gelesen, passt" / "lektorat ok".
6. ERST DANN wird der Status auf "lektorat" gesetzt + Deploy.

Claude darf den Status NICHT eigenmächtig auf "lektorat" setzen. Nachfragen ist erlaubt,
weiterschalten nicht.

**Artefakte:**
- `buch/szenen/{KK}-{SS}.md` — Szenenplan
- `buch/kapitel/{KK}-entwurf.md` — Entwurf
- `buch/kapitel/{KK}-szene{S}.md` — Szenen-Drafts
- `buch/kapitel/{KK}-{name}.md` — Finales Kapitel

### Gate-Protokoll (gilt für JEDEN Prüfschritt)

Jeder Prüfschritt ist ein Gate mit 3 Stufen:
1. **Bericht** — Findings, Zahlen, Verdikt (BESTANDEN/NICHT BESTANDEN)
2. **Autor-Freigabe** — Warte auf explizites OK. Keine Weiterarbeit ohne.
3. **Fixes + Bestätigung** — Fixes einarbeiten, Zusammenfassung zeigen, erneut OK einholen.

### /logik-check (Kapitel-Pipeline, GATE)

Prüft Absatz für Absatz:
- Weiß die Figur das? (Geografie, Namen, Fakten — BEVOR sie es erfährt?)
- **Sorel-Prinzip bei JEDEM Eigennamen:** Woher kennt die Figur diesen Namen?
  Jeder Orts-, Personen- und Objektname muss INNERHALB des Textes eingeführt
  werden (Dialog, Schild, Brief, eigene Schlussfolgerung). Nie voraussetzen.
- Kann die Figur das wahrnehmen? (Licht, Entfernung, Raum)
- Erzählt der Narrator mehr als die POV-Figur weiß?
- Tageszeit, Wetter, Ort konsistent?
- **Technische Fakten:** Fachbegriffe prüfen (Uhrmechanik, Botanik, Schiffbau,
  Medizin). Zahlen, Maße, physikalische Angaben müssen stimmen. Im Zweifel
  recherchieren.
- Magie-Regeln gegen 10-magie-system.md?
- **POV-Expertise:** Beschreibt die Figur durch ihre Berufslinse?
  Steinleserin sieht Risse, nicht Farnnamen. Fotograf sieht Licht, nicht Geologie.
  Keine Figur darf Fachwissen zeigen das sie nicht hat.
- **Anachronismus-Check (besonders Interludien):**
  - Maßeinheiten: Meile/Schritt/Elle (nicht Kilometer/Meter vor 1799)
  - Anrede: Ihr/Euch (nicht Sie vor ~1650)
  - Transport: Pferd/Karren (nicht Kutsche vor ~1500)
  - Monate: Nebelmond etc. in historischen Dialogen (nicht November)
  - Berufe: keine modernen Konzepte (Gelehrte, nicht Forscherin)
- **Moragh-Szenen:** Keine Werkzeuge, kein Handwerk, keine Maschinen (außer
  Magie-geformte). Alles wird mit Magie gemacht. Siehe 10-magie-system.md.

### /stil-check (Kapitel-Pipeline, GATE)

Prüft systematisch:
- "und"-Ketten (>3 pro Satz), Bandwurm-Balance
- Harte Limits: "nicht X — sondern Y" (max 2x), "wie..." Vergleiche (max 4x)
- Emotionen benannt statt gezeigt, erklärende Nachsätze
- Wort-Häufungen, Satzanfang-Monotonie
- Rhythmus-Vergleich mit Referenzkapitel
- **Stakkato-Zählung:** Fragmentsätze (<4W ohne Verb) zählen. Max 2-3 Passagen
  pro Kapitel (je max 3 Fragmente in Folge). Nur bei Schock, Inventur, Hammerschlag.
- **Personifikations-Zählung:** Gegenstände die handeln/wissen/warten/sich weigern.
  Jede Stelle auflisten. Funktioniert sie (POV-Wahrnehmung, Atmosphäre) oder ist
  sie mechanisch/inflationär? Max ~8 pro Kapitel.
- **Dialog-Realismus:** Fehlen logische Schritte in Gesprächen? Würde ein echter
  Mensch so reden? Preis vor Schlüssel, Vorstellung vor Vertrauen, Rückfragen
  wo Rückfragen natürlich wären. Kein Filmdrehbuch.
- **Wiederholte Ortsbeschreibung:** Atmosphäre-Elemente gegen vorherige Kapitel
  abgleichen. Was bereits etabliert ist, darf nicht nochmal beschrieben werden.

### Das Sorel-Prinzip

**Der Erzähler darf NIE mehr wissen als die Figur.** Wenn Sorel nicht weiß wo Vael liegt, darf der Narrator nicht "Die Hafenstadt an der Grauküste" schreiben. ERST nachdem die Figur es erfährt (Atlas, Gespräch, Schild).

**Erweiterung — Premature Doubt:** Die Figur darf NIE zweifeln oder hinterfragen
bevor das auslösende Ereignis stattfindet. Wenn Sorel erst in Szene 3 sieht dass
ein Schemen sein Gesicht trägt, darf er in Szene 1 nicht fragen ob das Gesicht
auf der Platte "wirklich seines" ist. Die Frage entsteht IM Moment, nicht vorher.

### Cross-POV-Regel

Wenn mehrere POVs denselben Ort besuchen: das spätere Kapitel darf NICHT
dieselbe Ankunftssequenz, dieselben Sinnesbeschreibungen oder dasselbe
Dialog-Muster wiederholen. Der Leser hat den Ort bereits betreten.
Jeder POV benutzt EIGENE Wörter für gemeinsame Phänomene
(Alphina: "Nebel", Sorel: "Dunst"). Siehe `02-stilregeln-v2.md` POV-Vokabular.

## Website

Deploy: git push && ssh adrian@adrianphilipp.de "cd ~/apps/Alphina-Static && git pull && bash generate-lesen.sh"

## Sprache

Deutsch. Umlaute verwenden. Kein ae/oe/ue.
