# /refit — Alt-Kapitel auf aktuellen Stil bringen ODER modernes Kapitel pruefen

**Zwei Modi (seit 2026-05-01):**

- **Modus A — Plot-Lock-Refit (klassisch):** Alt-Kapitel (vor April 2026) durch Plot-Lock-Extraktion + Neuausarbeitung. Kein Edit-in-place.
- **Modus B — 4-Subagent-Pipeline-Check (neu):** Modernes finales Kapitel direkt durch die 4-Subagent-Pipeline pruefen, ohne Refit. Findings-Report + autor-getriebene Fixes auf bestehendem Text. Kein Plot-Lock noetig.

**Auto-Detection:** Phase 0.4 (Stil-Gap-Check) entscheidet. Stark Alt-Stil → Modus A. Schwach Alt-Stil → Modus B.

**Warum ein eigener Skill:**
- Modus A: `/ausarbeitung` setzt einen freigegebenen `/entwurf` voraus. Alte Kapitel haben keinen Entwurf mehr — der Plot steckt in der Prosa. Ein Edit-Pass auf der Altprosa produziert Mongrel-Text. `/refit` extrahiert stattdessen die Beats in ein **Plot-Lock-Dokument**, generiert daraus einen regulaeren Entwurf, archiviert das Altkapitel und uebergibt an die bestehende `/ausarbeitung`-Pipeline.
- Modus B: Auch moderne finale Kapitel (z.B. K22, K27) wurden vor der 4-Subagent-Pipeline-Verschaerfung (Mai 2026) geschrieben. Sie haben keinen Stil-Gap im klassischen Sinn, aber moeglicherweise Verquastung, Buehnen-Bugs oder POV-Vokabular-Brueche, die heute aufgefangen wuerden. `/refit` Modus B prueft das — ohne Refit, nur Diagnose + Fix-Liste auf vorhandenem Text.

**Modell-Soll:** Sonnet (Hauptsession). Plot-Extraktion und Pipeline-Konsolidierung sind kognitive Arbeit, keine Prosa. Subagenten explizit per Override.

## Input

`$ARGUMENTS` = Kapitel-ID im alten oder neuen Format:
- `01-alphina` / `02-sorel` (alter Dateiname ohne Endung)
- `B1-K01` (neue Form, wird auf alte Datei aufgeloest)

Wenn kein Argument: frage welches Kapitel.

## Phase 0: Guard-Checks

### 0.1 Modell-Check

Wenn nicht Sonnet:

> WARNUNG: Du bist auf [Modell]. Diese Phase ist Plot-Extraktion, keine Prosa. Auf Opus zahlst du den Aufpreis ohne Mehrwert. Auf Haiku leidet die Qualitaet der Beat-Abstraktion. Empfehlung: Session beenden, neu starten mit `claude --model sonnet`. Trotzdem weiter?

Auf Opus: warten auf explizites "weiter". Auf Haiku: zwei Bestaetigungen.

### 0.2 Altkapitel existiert?

Pruefen: `buch/kapitel/{alte-datei}.md` vorhanden?

- `01-alphina.md`, `02-sorel.md`, ..., `04-maren.md`, `06-sorel.md`, `07-vesper.md`, `08-maren.md` — alte Numerierung
- Wenn nein: HARTER ABBRUCH: "Altkapitel-Datei nicht gefunden. Welches Kapitel willst du refitten? Verfuegbar: [Liste aus ls buch/kapitel/ ohne entwurf/szene/handoff/legacy]"

### 0.3 Status-Check

Aus `status.json` lesen.

| Aktueller Status | Verhalten |
|---|---|
| `final` (modern, post-Mai-2026) | Normal weiter — vermutlich Modus B (Pipeline-Check) |
| `final` oder `lektorat` (Alt-Stil) | Normal weiter — vermutlich Modus A (Plot-Lock-Refit) |
| `entwurf-ok` / `ausarbeitung` | HARTER ABBRUCH: "Kapitel ist schon in der neuen /ausarbeitung-Pipeline. Dort gilt die 4-Subagent-Pipeline pro Block. /refit nur fuer finale oder Alt-Kapitel." |
| `refit` (in Arbeit) | Frage: "Refit laeuft schon. Plot-Lock neu erstellen (ueberschreiben), Pipeline-Check (Modus B) oder weiter?" |

### 0.4 Stil-Gap-Check (Modus-Switch)

Kurzer Grep-Check auf typische Alt-Stil-Marker im Kapitel:
- `nicht X — sondern Y` / `nicht X, sondern Y`
- `sie dachte` / `er fragte sich`
- `Das war` am Absatz-Anfang oder -Ende
- Abstrakta-Stapel: `der/die/das [Stille|Kaelte|Schwere|Leere|Ferne] des/der`
- Satz mit `wie etwas, das...`

**Verzweigung:**

| Treffer-Summe | Modus | Begruendung |
|---|---|---|
| ≥ 5 | **Modus A** (Plot-Lock-Refit) | starker Alt-Stil-Gap, Kapitel braucht Neuausarbeitung |
| 1-4 | **Modus B** (Pipeline-Check) | moderner Stil mit moeglichen Bugs, kein Refit noetig |
| 0 | Modus B mit Hinweis "Kapitel sieht sauber aus, evtl. nur diagnostischer Run" |

Dem Autor anzeigen: Treffer-Liste + Empfehlung + Frage **„Modus A oder B?"**. Autor-Override moeglich (z.B. „Modus A trotzdem", weil tieferer Refit gewuenscht).

**Bei Modus A:** weiter mit Phase 1-9 (Plot-Lock-Workflow).
**Bei Modus B:** direkt zu **Phase B1** springen (siehe unten, nach Phase 9).

### 0.5 Parameter-Normalisierung

Aus Dateiname `NN-figur.md` → `B1-K{NN}` ableiten. POV-Figur aus Dateiname (`01-alphina` → Alphina). Fuer Interludien gesondert.

## Phase 1: Kontext laden — Extraktions-Setup

**Schritt 1: Kontext-Extraktor ausfuehren (Bash):**

```bash
python scripts/kapitel-kontext.py {ID} --phase entwurf
```

Liefert Timeline-Anker, Nachbar-Kapitel, Events, Wissensstand der POV-Figur an diesem Datum. Ersetzt direkte zeitleiste.json/status.json-Reads.

**Schritt 2: Parallel mit Read laden:**

1. **`buch/00-positioning.md` ZUERST** (~800 W — Marktposition, Heat-Regeln, 95%-Gate)
2. `buch/02-stilregeln-v2.md` (~5k W — harte und dosierte Limits, Konkretheits-Regeln, POV-Vokabular)
3. `buch/01-autorin-stimme.md` (~4.5k W — Autor-Stimme, Begehren-Vokabular, Anti-Patterns)
4. `buch/kapitel/{alte-datei}.md` — **Extraktions-Quelle**, der Altkapitel-Text
5. `buch/pov/{figur}.md` — POV-Dossier (~500 W)
6. `buch/00-canon-kompakt.md` (~800 W — Welt/Figuren auf einen Blick, fuer Canon-Abgleich)

**NICHT laden (kommen spaeter):**
- Andere Altkapitel — nur das zu refittende
- Leseproben-Volltexte — erst in Phase 4 (Anker-Auswahl)
- Voice-Referenz-Kapitel — erst in `/ausarbeitung`
- `buch/zeitleiste.json`, `buch/status.json` direkt — Extraktor liefert das
- `buch/kapitel-summaries.md` — redundant zum Extraktor-Output
- Aktplaene komplett — Extraktor liefert Snippet

**Ziel-Kontext: ~13-16k W.** Extraktor (~3k) + Positioning (~800) + Stilregeln (~5k) + Autor-Stimme (~4.5k) + Altkapitel (~3-6k je nach Laenge) + POV (~500) + Canon-Kompakt (~800).

## Phase 2: Plot-Lock schreiben

Datei: `buch/kapitel/{ID}-plot-lock.md`

Der Plot-Lock ist **Canon-Dokument** — er bleibt nach dem Refit liegen als definitive Referenz fuer den Kapitel-Inhalt. Jeder darin notierte Beat und jedes Tschechow-Element MUSS im refitteten Kapitel landen.

**Format strikt:**

```markdown
# {ID} — {Figur} — Plot-Lock

**Quelle:** buch/kapitel/{alte-datei}.md
**Extraktionsdatum:** {ISO-Datum}
**POV:** {Figur} (3. Person nah, Praeteritum)
**Timeline-Anker:** {Tag. Monat 551} · {N Wochen M Tage in Vael / Ort}
**Wortziel Refit:** 4.000-4.500 W

## Canon-Gewaehr

Ein Absatz (50-120 W): Was muss aus dem alten Kapitel zwingend ueberleben? Worum geht es in diesem Kapitel im Plot-Canon? Welches Tschechow-Element feuert hier oder wird hier geladen?

## Szenen-Struktur

- Szene 1: {Kurztitel} · {Ort} · {Uhrzeit} · {Register-Soll} · {Heat-Level}
- Szene 2: ...
- Szene 3: ...
- (2-4 Szenen)

---

## Szene 1 — {Titel}

**Ort:** {exakt — Wohnung 4. Stock, Garten der Gesellschaft, etc.}
**Zeit:** {Tageszeit, wenn im Text genannt: "12 Minuten nach drei"}
**Register-Soll:** {Mischung aus langsam/normal/schnell}
**Heat-Level:** {keine / leise / commercial / explizit non-BDSM / explizit BDSM / Drohung / Gewalt}
**Wortziel:** {~1.200-1.600}

### Plot-Beats (harte Reihenfolge)

1. {Beat 1 — was passiert konkret, in einem Satz}
2. {Beat 2}
...
N. {Beat N}

### Tschechow-Elemente

Konkrete Dinge/Details aus dem Altkapitel, die als Tschechow-Waffen fungieren — entweder hier geladen oder hier abgefeuert.

| Element | Zeile alt | Funktion | Zuendet in | Bleibt? |
|---------|-----------|----------|------------|---------|
| Wetterfahne Hand-nach-Norden | 19 | Vael-Unheimlichkeit | K?? | ja |
| 49 Pflanzen | 15 | Figurentreue | laufend | ja |
| Laris-Hand-am-Bauch | 55 | Beziehungs-Backstory | K?? | ja |
| Oolong 85°C | 47 | Kontroll-Tic | laufend | ja |

### Sinnes-Inventar (spezifische, nicht-generische Details)

Liste aller im Altkapitel benannten konkreten Details mit Zahlen/Namen/Material. Nicht "die Nacht war dunkel", sondern "vier Stockwerke unter ihr", "drei violette Bluete", "fuenfundvierzig Turmuhren, das Gildehaus geschlossen seit achtzig Jahren".

- {Detail 1}
- ...

### Gefühls-Wirkung (wechselseitig) — PFLICHT

**Gegenpol zur emotionalen Einseitigkeit.** In jeder Szene mit zwei oder mehr Figuren muss sichtbar werden, **dass und wie die Figuren einander verändern** — durch Körper, nicht durch benannte Gefühle.

- **Was macht das Gegenüber mit der POV-Figur?** Min. 2 Körper-Beats in ihr, die zeigen: eine Geste/Äußerung/Reaktion des anderen landet. Unterbauch, Kehle, Gesicht, Atem, Hand-die-länger-bleibt-als-nötig, Puls, Hitze, Zittern, Stimme, die durchbricht.
- **Was macht die POV-Figur mit dem Gegenüber?** Min. 2 sichtbare Reaktionen im anderen, die die POV-Figur wahrnehmen kann (Atmen-tiefer, Zucken, Haltung, Geräusch, Blick, Finger-die-greifen-ohne-Ziel). Kein Mindreading — nur was sichtbar ist.
- **Bei Alleinszenen (Alphina allein in K01):** Wirkung der Welt/Magie/Erinnerung auf die Figur. Laris-Erinnerung → Körper. Warme Erde → Unterbauch, Hand-zieht-sich-weg. Mindestens 2 Körper-Beats, die zeigen, dass die Figur von etwas bewegt wird.

**Pflicht-Frage beim Refit:** Wo ist {POV-Figur} emotional getroffen in dieser Szene? Wenn die Antwort "wird geführt, beobachtet, registriert" ist — **Defizit**. Auch ohne benannte Emotionen muss Wirkung sichtbar sein.

Hintergrund: Commercial Dark Romantasy lebt von wechselseitiger Verletzbarkeit. Wenn eine Figur Regisseur/Beobachter ist und die andere alle Körperreaktionen trägt, kippt es in einseitiges BDSM-Register (auch wenn kein BDSM-Canon gilt). Gegenmittel: Körper-Spiegel-Beats, Wirkung aus Gesten-des-anderen, Heat an ungewohnten Stellen (Gesicht, Kehle, Ohren).

### Dialog-Beats (falls Dialog)

- {Figur A} sagt/erfaehrt: {Info}
- {Figur B} sagt/erfaehrt: {Info}
- {Innere Wendung am Szenen-Ende}

### Canon-Wissensstand am Ende der Szene

- **Weiss:** {was die POV-Figur jetzt sicher weiss}
- **Weiss nicht (Sorel-Prinzip):** {was ihr kuenftig begegnet, aber hier noch nicht}

---

## Szene 2 — ...

{analog}

---

## Szene 3 — ...

## Refit-Hinweise (Stil-Gap-Diagnose)

Konkrete Befunde aus dem Altkapitel, die beim Refit dringend anders werden muessen. Pro Befund: Zeile + Zitat + Problem + Richtung-des-Fixes. Pflicht-Kategorien zu pruefen:

- **Abstrakta-Stapel** (`Stille, Kaelte, Schwere, Leere, Ferne, Ewigkeit, Abgrund` in Ketten)
- **Scharnier-Aphorismen** (`X. Das war Y.` am Absatz-Ende)
- **Figur-redet-ueber-sich** (Selbstkommentar statt Koerperbeat)
- **Metapher + Erklaer-Nachsatz** (Bild wird verdoppelt)
- **Mindreading** (POV liest Motive anderer)
- **Benannte Emotionen als Substantiv** (Sehnsucht, Obsession, Scham, das Unheimliche)
- **Premature Doubt** (Figur zweifelt bevor Ausloeser da ist)
- **Chroniken-Prophezeiung** (Erzaehler weiss die Zukunft)
- **95%-Gate** (Eroeffnung: Hook, Wollen, Kipp-Moment, Koerper)
- **Berufslinsen-Ueberzug** (Linse als Karikatur statt 15-20% Anteil)
- **Komma-Listen-Katalog** (Koerperbeschreibung als Liste)
- **Emotionale Einseitigkeit** (eine Figur reagiert mit Koerper, die andere beobachtet nur — bei 2+ Figuren in einer Szene Defizit. Wirkung muss wechselseitig sein, siehe Gefühls-Wirkung oben.)

Wichtige Faelle konkret zitieren. Keine erschoepfende Tabelle — nur die, die beim Rewrite ins Auge fallen muessen.

## Gaensehaut-Moment

Was ist das Unmoegliche, das vor der Figur physisch passiert? Ein Satz. Pflicht pro Kapitel.

## Anker-Kandidaten (werden in Phase 4 finalisiert)

- **Register-Anker (Leseprobe(n)):** {Vorschlag aus buch/leseproben/}
- **Voice-Anker (Kapitel):** {letztes fertiges Kapitel derselben POV im neuen Stil}

```

## Phase 3: Plot-Lock mit Autor pruefen

**GATE: Dies ist der wichtigste Schritt des Refits. Hier wird entschieden, was der Plot des Kapitels tatsaechlich IST.**

Dem Autor zeigen:
1. Szenen-Struktur (Ueberblick)
2. Pro Szene: **Plot-Beats als nummerierte Liste** (nicht Prosa, sondern nackte Beats)
3. Tschechow-Tabelle (was bleibt, was kann weg)
4. Sinnes-Inventar komplett
5. Refit-Hinweise (Top-5 kritische Stil-Gaps)
6. Gaensehaut-Moment

**Fragen an den Autor:**

- Sind alle Plot-Beats erfasst? Fehlt einer?
- Stimmt die Szenen-Anzahl? Soll eine Szene geteilt/zusammengefasst werden?
- Welche Tschechow-Elemente bleiben? Welche fliegen raus? Gibt es neue, die nach heutigem Canon hinzukommen (z.B. Bezug auf spaetere Kapitel, die beim urspruenglichen Schreiben noch nicht existierten)?
- Heat-Level pro Szene OK?
- Register-Soll pro Szene OK?
- Gaensehaut-Moment trifft?
- Refit-Hinweise: noch was vergessen?

Aenderungen direkt im Plot-Lock einarbeiten, bis Autor "plot-lock ok" sagt.

**GATE: Ohne explizites "plot-lock ok" kein Phase-Wechsel.**

## Phase 4: Anker-Auswahl

Parallel drei Dateien lesen und vergleichen:

1. Vorschlag Register-Anker (Leseprobe) lesen
2. Vorschlag Voice-Anker (Kapitel) lesen
3. Plot-Lock lesen

**Pro POV-Figur Standard-Kandidaten:**

| POV | Voice-Anker (Kapitel) | Register-Anker (Leseproben) |
|-----|----------------------|------------------------------|
| Alphina | K05 oder K09 | 01 (Banter), 08 (Magie-Kontrollverlust), 09 (Vael warm), 11 (Moragh-Ankunft) |
| Sorel | K10 | 02 (erster Kuss), 03 (Heat explizit), 09 (Vael warm) |
| Vesper | K11 | 04 (BDSM-Alltag), 06 (Aftercare), 10 (Vael kalt) |
| Maren | noch keiner — Leseproben-Mix | 04 + 05 (BDSM), 09 (Werft warm), 06 (Aftercare) |

Passend zur Plot-Lock-Szene waehlen. **Heat-Level muss matchen** — keine explizit-BDSM-Leseprobe fuer Alltagsszene.

Dem Autor Vorschlag mit Begruendung vorlegen. **GATE: Autor bestaetigt Anker.**

## Phase 5: Entwurf im /entwurf-Format generieren

Datei: `buch/kapitel/{ID}-entwurf.md`

Aus Plot-Lock + Anker einen regulaeren Entwurf generieren (exakt im Format von `/entwurf` Phase 2). Kritisch: **Die Dialog-Info-Listen pro Szene muessen die Beats aus dem Plot-Lock 1:1 tragen.** Kein Beat darf still verloren gehen.

Zusaetzlich pro Szene ein Feld **Register-Vorgabe** mit Verweis auf konkrete Anker-Stellen:

> Register-Vorgabe: NORMAL-Mittelbau dominant, LANGSAM-Passage an Garten-Eintritt (vgl. Leseprobe 09 "Welt Vael warm" Zeilen X-Y), SCHNELL-Passage nur am Gaensehaut-Moment (vgl. K09-alphina Zeilen X-Y).

## Phase 6: Altkapitel archivieren

```bash
mkdir -p buch/kapitel/legacy
git mv buch/kapitel/{alte-datei}.md buch/kapitel/legacy/{alte-datei}.md
```

Anschliessend: Banner in der archivierten Datei einfuegen (Edit-Tool):

```markdown
> **LEGACY — REFIT DURCH /refit**
> Dieses Kapitel ist im alten Stil. Der Plot-Canon lebt in
> `buch/kapitel/{ID}-plot-lock.md`. Das neue Kapitel entsteht
> unter `buch/kapitel/{ID}-{figur}.md` durch `/ausarbeitung`.
> Diese Datei ist ab sofort **nicht mehr Canon** und wird nur
> als Tschechow-Referenz fuer den Refit gehalten.
```

## Phase 7: status.json aktualisieren

Felder fuer dieses Kapitel:
- `state: "entwurf-ok"` (damit /ausarbeitung starten kann)
- `entwurfs_datei: "{ID}-entwurf.md"`
- `plot_lock_datei: "{ID}-plot-lock.md"`
- `legacy_datei: "legacy/{alte-datei}.md"`
- `refit_gestartet: "{ISO-Datum}"`
- `datei: "{ID}-{figur}.md"` (fuer spaetere /ausarbeitung-Ausgabe)

## Phase 8: Handoff fuer /ausarbeitung

Datei: `buch/kapitel/{ID}-handoff.md`

```markdown
# Handoff — {ID}

**Von Phase:** refit → **Zu Phase:** ausarbeitung
**Erstellt:** {ISO-Datum}
**Status beim Handoff:** entwurf-ok

## Modell-Empfehlung

claude --model opus

## Aufruf fuer naechste Session

/ausarbeitung {ID}

## Kontext fuer naechste Session

- POV: {Figur}
- Wortziel: 4.000-4.500
- Timeline-Anker: {aus Plot-Lock}
- Freigegebener Entwurf: buch/kapitel/{ID}-entwurf.md
- **Plot-Lock (PFLICHT-READ in /ausarbeitung Phase 1):** buch/kapitel/{ID}-plot-lock.md
- **Register-Anker:** {Leseprobe(n)-Pfade}
- **Voice-Anker:** {Kapitel-Pfad}
- **Legacy-Referenz (nur fuer Tschechow-Beats, NICHT fuer Stil):** buch/kapitel/legacy/{alte-datei}.md

## Besondere Anweisungen

- Dies ist ein **REFIT**, keine Neuschrift aus dem Nichts. Jeder Plot-Beat aus dem Plot-Lock MUSS landen.
- Die Legacy-Datei darf **nicht** als Stil-Vorlage benutzt werden. Sie ist Tschechow-Spickzettel, mehr nicht.
- Bei Konflikt zwischen Plot-Lock und Legacy-Datei gilt Plot-Lock (er ist autorisiert durch "plot-lock ok").
- 95%-Gate (Positioning 9) pruefen, besonders fuer K01 (Buch-Oeffnung).
- Wenn `/ausarbeitung` findet, dass Plot-Lock luecken hat: **STOPP und Rueckkehr zu /refit**. Niemals Plot still anpassen.
```

## Phase 9: Harter Stop

```
REFIT VORBEREITET. Status: entwurf-ok.

Plot-Lock: buch/kapitel/{ID}-plot-lock.md
Entwurf: buch/kapitel/{ID}-entwurf.md
Legacy archiviert: buch/kapitel/legacy/{alte-datei}.md

Naechster Schritt: NEUE SESSION mit Opus.

1. Diese Session beenden
2. claude --model opus
3. /ausarbeitung {ID}

Das Handoff-File wird automatisch gelesen.

Diese Session schreibt jetzt nichts mehr.
```

---

# MODUS B — 4-Subagent-Pipeline-Check (modernes finales Kapitel)

**Wann:** Phase 0.4 hat „Modus B" als Empfehlung ausgegeben (1-4 Alt-Stil-Marker), oder Autor hat Modus B explizit gewaehlt.

**Ziel:** Bestehendes Kapitel gegen den heutigen Setup-Stand pruefen (Hebel 1-5 aus `/ausarbeitung`-Skill). Findings-Report + autor-getriebene Fixes auf vorhandenem Text. **Kein Refit, kein Plot-Lock, kein Edit-in-place ohne Autor-Freigabe.**

## Phase B1 — Kontext laden

Parallel mit Read laden (~12-15k W):

1. `buch/00-positioning.md` — Marktposition + 95%-Gate
2. `buch/02-stilregeln-v2.md` — Stilregeln inkl. Verquastungs-Test
3. `buch/01-autorin-stimme.md` — Stimme + Anti-Patterns
4. `buch/01-referenz-konkretheit.md` — Konkretheits-Kanon
5. `buch/pov/{figur}-schreibblatt.md` — Magie-Mechanik, Adult-Stellen, POV-Anti-Patterns
6. `buch/pov/{figur}.md` — POV-Dossier (Wissensstand)
7. **Kapitel selbst:** `buch/kapitel/B1-K{NN}-{figur}.md`

**Kontext-Extraktor zusaetzlich** fuer Nachbar-Kapitel + Wissensstand:

```bash
python scripts/kapitel-kontext.py B1-K{NN} --phase ausarbeitung
```

## Phase B2 — Vier parallele Spezialisten-Subagenten

Identisch zu Phase 2 in `/ausarbeitung` (4-Subagent-Pipeline-Sektion), aber auf das **ganze Kapitel** statt einzelne Bloecke.

Dispatch alle vier in EINEM Tool-Call, parallel, alle Sonnet:

### Subagent 1 — Sprach-TÜV (Kapitel-Scope)

Prompt aus `.claude/commands/ausarbeitung.md` Sektion „Subagent 1 — Sprach-TÜV", aber:
- `{BLOCK_TEXT}` durch ganzes Kapitel ersetzen
- „Max 5 Findings" → „Max 15 Findings"
- „Max 800 Token" → „Max 1.5k Token"

### Subagent 2 — Verquastungs-Detektor (Kapitel-Scope)

Prompt aus `/ausarbeitung` Sektion „Subagent 2", aber:
- Ganzes Kapitel statt Block
- Max 15 Findings, 1.5k Token

### Subagent 3 — Konsistenz-Wächter (Kapitel-Scope)

Prompt aus `/ausarbeitung` Sektion „Subagent 3", aber:
- Ganzes Kapitel statt Block + Vorszene
- Inventar-Verfolgung ueber alle Szenen
- Max 12 Findings, 1.5k Token

### Subagent 4 — Genre-Leserin (Kapitel-Scope)

Prompt aus `/ausarbeitung` Sektion „Subagent 4", aber:
- Ganzes Kapitel statt Block
- Stimme passend zum Heat-/Plot-Charakter (LINA fuer Romantasy-Bloecke, MEIKE fuer Dark-Fantasy, VICTORIA fuer BDSM, KAYA fuer Schock)
- Max 8 Findings, 1.5k Token

## Phase B3 — Konsolidierung

In der Hauptsession:

1. **Verdikt-Block** zeigen:
   - Pro Subagent: BESTANDEN / GRENZWERTIG / NICHT BESTANDEN
   - Marktfaehigkeits-Score (Subagent 4)
   - Gesamt-Stimmung

2. **Master-Tabelle** aller Findings, konsolidiert mit Konflikt-Hierarchie (Konsistenz > Verquastung > Stilregel > Genre-Geschmack):

| # | Zeile | Quelle | alt | neu / [STREICHEN] | warum |
|---|---|---|---|---|---|

3. **Stärkste Beats** (was alle Subagenten loben):

| Zeile | Passage | warum stark |
|---|---|---|

## Phase B4 — Fix-Loop

Frage am Ende der Master-Tabelle: „Soll ich die Findings einarbeiten? Pro Eintrag `ok`, `skip`, oder eigener Fix."

- Autor entscheidet pro Finding
- Fixes per Edit-Tool inline einarbeiten
- Nach Fix-Runde: optionalen Re-Check mit Subagent 2 (Verquastungs-Detektor) laufen lassen, ob neue Verquastung entstanden ist

## Phase B5 — Status-Update + Deploy

- Falls Fixes eingearbeitet: `wc -w` neu zaehlen, status.json `woerter` aktualisieren
- `git add buch/kapitel/B1-K{NN}-{figur}.md buch/status.json`
- Commit-Message: `fix(B1-K{NN}): Modus-B-Pipeline-Check — {N} Fixes aus Subagent-Findings`
- Push (Hook deployed automatisch)

Falls KEINE Fixes eingearbeitet (Autor hat alle „skip"): nur Findings-Report ausgeben, kein Commit.

## Phase B6 — Harter Stop

```
PIPELINE-CHECK ABGESCHLOSSEN.

Kapitel: B1-K{NN}-{figur}.md
Subagent-Verdikt: [Bestanden/Grenzwertig/Durchgefallen pro Stimme]
Findings: {gesamt} | uebernommen: {N} | geskippt: {M}

{Wenn schwer kaputt:} 
  → Empfehlung: Tieferer Refit (Modus A) erwaegen.
  → Erneut /refit aufrufen, Modus A explizit waehlen.

{Wenn ok:}
  → Kapitel auf aktuellem Stand. Naechster /refit-Lauf erst, wenn Setup-Hebel 6+ kommen.

Diese Session schreibt jetzt nichts mehr.
```

## Modus-B-Regeln

- **Kein Plot-Lock erstellen.** Modus B ist diagnostisch + chirurgisch, nicht strukturell.
- **Kein Status-Wechsel.** Status bleibt `final`. Modus B ist Pflege auf finalen Texten.
- **Bei `>50` Findings:** Autor warnen, dass Modus A (Plot-Lock-Refit) sinnvoller sein koennte.
- **Bei Konflikt mit Plot-Canon:** Autor entscheidet. Plot-Aenderungen NIE still.
- **Subagent-Findings sind Vorschlaege, keine Pflicht.** Autor hat letztes Wort.
- **Nicht-aktiv, falls Kapitel in `entwurf-ok` oder `ausarbeitung`:** dort gilt `/ausarbeitung`-Pipeline.

---

## Sonderfall: K01 (Buch-Oeffnung)

K01 traegt besondere Last. 95%-Gate aus `00-positioning.md` Abschnitt 9 ist hier **ueberlebenswichtig**:
- Erster Satz = Hook (Figur in Situation mit Spannung, nicht Atmosphaere-Beobachtung)
- Figur will etwas, deutlich, in den ersten 50 Woertern
- Etwas passiert/kippt in den ersten 200 Woertern
- Koerper oder Emotion hoerbar im ersten Viertel

Im Plot-Lock fuer K01 **zusaetzlich** ein Abschnitt "Oeffnungs-Gate" mit:
- Vorschlag fuer den ersten Satz (Hook-Form)
- Wollen der Figur in Szene 1 (konkret benannt)
- Erster Kipp-Moment: wo?
- Erster Koerper-Marker: wo?

Ein `/book-council`-Durchlauf auf den Opening-Entwurf ist **empfohlen** vor `/ausarbeitung`.

## Sonderfall: POV ohne Voice-Anker (Maren)

Maren hat (Stand April 2026) kein fertiges Kapitel im neuen Stil — K04 und K08 sind beide alt. Bis das erste Maren-Kapitel im neuen Stil existiert, als Voice-Anker die **Leseproben 04 + 05 + 09** kombiniert nutzen, plus einen Satzlaengen-Hinweis aus `02-stilregeln-v2.md` (Maren ~35W, fliessend, Wasser-Metaphorik). Reihenfolge-Empfehlung: K04 refitten **bevor** K08, damit K04-refit dann selbst als Voice-Anker fuer K08 dient.

## Regeln

- **KEIN Edit-in-place.** Kein Satz aus dem Altkapitel darf automatisch ueberleben. Alles laeuft ueber den Plot-Lock.
- **Plot-Lock ist Canon.** Jeder Beat daraus MUSS in der neuen Prosa landen. Verlust = Regression.
- **Anker sind Ton-Referenz, kein 1:1-Vorbild.** Die Leserin erkennt den Ton, nicht Zitate.
- **Bei Beat-Luecke im Plot-Lock:** in Phase 3 den Autor fragen. Niemals still ergaenzen.
- **Bei Stil-Konflikt zwischen Altkapitel und aktuellen Stilregeln:** Stilregeln gewinnen. Das IST der Grund fuer den Refit.
- **Bei Plot-Konflikt zwischen Altkapitel und Plot-Lock:** Autor entscheidet in Phase 3. Plot-Lock ist die Gewalt-Frage, nicht die Stil-Frage.
- Deutsch. Umlaute verwenden (ä, ö, ü, ß). Kein ae/oe/ue in der Zielprosa — innerhalb dieses Skill-Dokuments selbst sind ae/oe/ue tolerierbar, aber der Plot-Lock und der Entwurf werden mit Umlauten geschrieben, weil die /ausarbeitung sie auch so erwartet.
- Setze `entwurf-ok` NUR nach "plot-lock ok" + generiertem Entwurf.
- Das Legacy-Kapitel bleibt fuer Tschechow-Referenz erhalten, aber nicht als Stil-Vorlage.

## Gates (Zusammenfassung)

| Gate | Bedingung |
|---|---|
| Altkapitel existiert | Sonst Abbruch |
| Plot-Lock "ok" | Explizites Autor-"plot-lock ok" vor Phase 4 |
| Anker bestaetigt | Explizites Autor-OK vor Phase 5 |
| Handoff geschrieben | Vor hartem Stop |

$ARGUMENTS
