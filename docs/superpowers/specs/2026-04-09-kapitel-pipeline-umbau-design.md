# Kapitel-Pipeline Umbau — Design

**Datum:** 2026-04-09
**Status:** Spec — bereit für Umsetzung
**Ziel:** Token-Verbrauch der Kapitel-Pipeline drastisch reduzieren durch Phasen-Trennung, kompakte Referenzfiles und gezielte Modell-Wahl.

## Problem

Die aktuelle `/kapitel`-Pipeline lädt pro Durchlauf ~40-50k Wörter Kontext (Weltbibel, Magie-System, Stilregeln, mehrere fertige Kapitel als Referenz, ganzer Aktplan). Jeder Subagent (Council, Logik-Check, Stil-Check) lädt seinen Kontext erneut. Die Hauptsession schreibt sowohl Plot-Beats als auch ausgearbeitete Prosa in einem Durchgang. Folge: hoher Token-Verbrauch, lange Sessions, wenig kontrollierbare Übergänge zwischen Plot-Arbeit und Sprach-Arbeit.

## Lösung (Übersicht)

Zwei strukturelle Umbauten parallel:

**A. Kontext-Diät durch kompakte Referenzfiles.** Drei neue Artefakt-Typen reduzieren den Lade-Kontext von ~40-50k auf ~6-20k Wörter pro Phase, je nach Aufgabe.

**B. Drei separate Pipeline-Phasen mit harten Session-Breaks.** Statt einer langen `/kapitel`-Pipeline gibt es drei eigenständige Commands. Jede Phase läuft in einer eigenen Session, mit eigenem Modell, eigenem Kontext, eigenen Gates. Phasen-Übergänge laufen über Handoff-Files. Sessions werden bei Übergang erzwungen abgebrochen.

```
Session 1: /entwurf B1-K12       → Handoff → STOP, neue Session mit Sonnet
Session 2: /ausarbeitung B1-K12  → Handoff → STOP, neue Session mit Sonnet/Haiku
Session 3: /lektorat-fix B1-K12  → Loop bis "final"
```

## Parameter-Format

Alle drei Commands akzeptieren genau einen Parameter:

- `B{N}-K{KK}` für Kapitel (z.B. `B1-K12`)
- `B{N}-I{N}` für Interludien (z.B. `B1-I3`)

Der Command parst den Parameter, schlägt in `status.json` unter `buch{N}` nach und findet die Datei-Pfade. Bestehende Kapitel-Dateien werden NICHT umbenannt — das Parameter-Format ist nur die externe ID. Wenn Buch 2 später startet, entscheiden wir dann über physische Umbenennung oder eigenen Ordner.

Neue Kapitel-Dateien (ab Inkrafttreten dieser Pipeline) verwenden den Prefix:
- `buch/kapitel/B1-K12-entwurf.md` (Phase-1-Artefakt)
- `buch/kapitel/B1-K12-{figur}.md` (Phase-2-Artefakt, finales Kapitel)
- `buch/kapitel/B1-K12-handoff.md` (Übergabe zwischen Phasen)

## Status-Kette (neu)

```
idee
  → entwurf          (Fließprosa-Exposé geschrieben, noch nicht geprüft)
  → entwurf-checked  (Logik-Check + Entwurfs-Council bestanden, Autor liest online)
  → entwurf-ok       (Autor hat Entwurf freigegeben, bereit für Ausarbeitung)
  → ausarbeitung     (Prosa wird ausgearbeitet, Session 2 läuft)
  → lektorat         (Stil-Check + Final-Council bestanden, Autor liest online)
  → final            (Autor hat Lektorat freigegeben)
```

`status.json` bekommt zwei Datei-Felder pro Kapitel:
- `entwurfs_datei` — Pflicht ab Status `entwurf`
- `datei` — Pflicht ab Status `lektorat`

## Phase 1 — `/entwurf B{N}-K{KK}`

**Ziel:** Plot, Struktur, Logik, Charakter-Dynamik als Fließprosa-Exposé festklopfen. Kein Prosa-Ton, kein Rhythmus, keine Stil-Arbeit.

**Modell-Soll:** Sonnet (Hauptsession). Subagenten explizit per Override.

### Ablauf

1. **Guard am Start.**
   - Prüfen: Läuft die Session auf Sonnet? Wenn nicht → Warnung + Abbruch-Vorschlag.
   - Parameter parsen, Status aus `status.json` lesen, prüfen dass nur `idee` oder fehlend ist.
   - Prüfen ob `buch/kapitel/B1-K12-handoff.md` existiert (Rücksprung-Fall).

2. **Kontext laden — schlank.** Nur diese Files, parallel:
   - `buch/00-canon-kompakt.md`
   - `buch/kapitel-summaries.md`
   - `buch/pov/{figur}.md` (POV-Dossier der Ziel-Figur)
   - `buch/zeitleiste.json` (komplett, ohnehin SoT und knapp)
   - Aus dem passenden Aktplan NUR der Abschnitt für dieses Kapitel
   - **NICHT geladen:** `00-welt.md`, `10-magie-system.md`, `02-stilregeln-v2.md`, fertige Kapitel-Volltexte, Referenz-Kapitel 1
   - Gesamt ~6-8k W statt 40-50k W.

3. **Entwurf schreiben** in `buch/kapitel/B1-K12-entwurf.md`. Format:

```markdown
# B1-K12 — [Figur] — Entwurf

**POV:** [Figur] (3. Person nah, Präteritum)
**Timeline:** [Monat/Jahreszeit, Anker zu vorherigem Kapitel]
**Wortziel Ausarbeitung:** 4.000-4.500 W
**Gänsehaut-Moment:** [Was physisch Unmögliches passiert]

## Szene 1 — [Titel/Ort]

**Wortziel:** 1.200-1.600 W (später in Ausarbeitung)

[150-300 W Fließprosa-Exposé: Wer, wo, was passiert, welche
 Bewegung, welche Sinneseindrücke sind dominant, wohin geht
 der Beat am Ende.]

**Dialog-Informationen:**
- A erfährt: [Info 1, Info 2]
- B erfährt: [Info 1]
- A's Erkenntnis am Ende: [innere Wendung]
- B's Erkenntnis am Ende: [innere Wendung]

**Tschechow-Waffen geladen:** [konkrete Gegenstände/Details]
**Tschechow-Waffen abgefeuert:** [was aus früheren Kapiteln zündet]
**Cross-POV-Ankerpunkte:** [Was muss konsistent sein mit Kap X]

## Szene 2 — ...
## Szene 3 — ...

## Kontinuitäts-Notizen
- Was weiß die POV-Figur am Anfang?
- Was weiß sie am Ende?
- Welches Wissen darf sie NICHT haben (Sorel-Prinzip)?
```

4. **Status-Update:** `entwurf` + `entwurfs_datei: "B1-K12-entwurf.md"` in `status.json`. Deploy.

5. **Schlanker Logik-Check** (Subagent, `model: "sonnet"`).
   - Lädt: nur den Entwurf + `00-canon-kompakt.md` + `kapitel-summaries.md`.
   - Prüft: POV-Wissen, Timeline-Sync, Magie-Regeln, Anachronismen, Sorel-Prinzip bei Eigennamen, Cross-POV-Dopplung.

6. **Entwurfs-Council** — 2 Subagenten sequenziell:
   - **Strukturanalyst** (`model: "sonnet"`): Plot-Logik, Tschechow-Ökonomie, Aktplan-Match, Beat-Dichte, Kontinuität.
   - **Beziehungs-Lektorin** (`model: "sonnet"`): Charakter-Arc, Power-Dynamik, Begehren als Unterstrom, emotionale Bogenführung.
   - Jeder lädt: Entwurf + `00-canon-kompakt.md` + POV-Dossier + `kapitel-summaries.md`.

7. **Bericht an Autor.** Konsolidiert. Status `entwurf-checked` + Deploy.

8. **Feedback-Loop** in derselben Session, Fixes einarbeiten, re-deployen. Bei Token-Druck: Handoff-File schreiben + Session-Break anbieten.

9. **Bei Autor-Freigabe ("entwurf ok"):**
   - Status → `entwurf-ok`.
   - Handoff-File generieren (Subagent `model: "haiku"`).
   - Harter Stop: Session beenden, neue Session mit Opus + `/ausarbeitung B1-K12`.

### Gates Phase 1

- Logik-Check + beide Council-Agenten müssen bestanden oder bewusst akzeptiert sein vor `entwurf-checked`.
- Autor-Freigabe Pflicht für `entwurf-ok`.
- Ohne `entwurf-ok` verweigert `/ausarbeitung` den Start.

## Phase 2 — `/ausarbeitung B{N}-K{KK}`

**Ziel:** Den freigegebenen Entwurf in Prosa ausarbeiten. Vom Plot NICHT abweichen. Fokus auf Sprache, Rhythmus, Figurenstimme, Sinneseindrücke.

**Modell-Soll:** Opus (Hauptsession). Subagenten explizit auf Sonnet.

### Ablauf

1. **Guard am Start.**
   - Prüfen: Opus aktiv? Wenn nicht → Warnung.
   - Handoff-Check (zwingend): `buch/kapitel/B1-K12-handoff.md` muss existieren mit Phase-Markierung `ausarbeitung`. Sonst harter Abbruch.
   - Status muss `entwurf-ok` sein.

2. **Kontext laden — POV-fokussiert.**
   - `buch/kapitel/B1-K12-entwurf.md`
   - `buch/kapitel/B1-K12-handoff.md`
   - `buch/pov/{figur}.md`
   - `buch/02-stilregeln-v2.md`
   - **Ein** Ton-Referenzkapitel: das letzte fertige Kapitel **derselben POV-Figur**
   - `buch/kapitel-summaries.md` (nur Kontinuität)
   - **NICHT geladen:** `00-welt.md`, `10-magie-system.md`, `00-storyline.md`, Aktpläne, andere POV-Kapitel
   - Gesamt ~15-20k W.

3. **Prosa ausarbeiten — Szene für Szene, direkt im Final-File** `buch/kapitel/B1-K12-{figur}.md`.
   - Szenenweise, nicht alles auf einmal.
   - `wc -w` nach jeder Szene (Ziel 1.200-1.600 W).
   - Kurzer Selbst-Check pro Szene (Adverb-Tags, Denk-Tags, Emotionen, Stakkato-Limit, POV-Berufslinse).
   - **Kein Szenen-Council zwischendurch.** Checks am Ende.
   - **Harte Regel:** Kein Plot-Beat darf verloren gehen. Jeder Dialog-Info-Punkt aus dem Entwurf muss in der Prosa landen. Keine Plot-Änderung ohne Rücksprung zu `/entwurf`.

4. **Status:** `ausarbeitung` + `datei: "B1-K12-{figur}.md"` + Deploy.

5. **Stil-Check** (Subagent, `model: "sonnet"`). Lädt nur Kapitel + `02-stilregeln-v2.md`. Harte Zählungen.

6. **Final-Council** — 3 Subagenten sequenziell:
   - **Stilkritiker** (`model: "sonnet"`, optional `opus` auf Wunsch): Medley-Prüfung. Lädt Kapitel + Stilregeln + Ton-Referenz.
   - **Dark-Romance/BDSM-Leserin** (`model: "sonnet"`): Power-Dynamik, Begehren, Hingabe/Kontrolle. Lädt Kapitel + POV-Dossier.
   - **Romantasy-Leserin** (`model: "sonnet"`): Sog, Emotion, Tension. Lädt nur Kapitel.

7. **Konsolidierter Bericht.** Stil-Check + drei Council-Stimmen + Verdikt.

8. **Fixes** in derselben Opus-Session bis Stil-Check + Council OK + Autor bestätigt.

9. **Status → `lektorat`** + Deploy. Autor liest online.

10. **Handoff für Lektorat-Fixes generieren** (Subagent `model: "haiku"`).
    - Überschreibt `B1-K12-handoff.md`.
    - Phase-Ziel `lektorat-fix`.
    - Modell-Empfehlung: Sonnet/Haiku.

11. **Harter Stop:** Session beenden. Bei Feedback: neue Session mit Sonnet + `/lektorat-fix B1-K12`.

### Wichtige Regeln Phase 2

- **Kein Zurück zum Entwurf still in der Prosa.** Wenn ein Plot-Beat nicht trägt: stoppen, Hinweis im Handoff, zurück zu `/entwurf`.
- **Keine Neu-Laderunde mitten in der Session.** Einmal laden, dann schreiben.

## Phase 3 — `/lektorat-fix B{N}-K{KK}`

**Ziel:** Kleinere textuelle Änderungen nach Lektorats-Feedback. Token-sparsamst. Kein Neuschreiben.

**Modell-Soll:** Sonnet (Default) oder Haiku (für Mikro-Fixes).

### Ablauf

1. **Guard am Start.**
   - Handoff-Check zwingend, Phase-Markierung `lektorat-fix`.
   - Status muss `lektorat` sein. Bei `final` → Bestätigung. Bei früheren → Abbruch.
   - Modell-Warnung (nicht Abbruch).

2. **Kontext laden — Minimum.**
   - `buch/kapitel/B1-K12-{figur}.md`
   - `buch/02-stilregeln-v2.md` (nur falls Autor eine Regel anspricht)
   - **NICHTS ANDERES.**
   - Gesamt ~5-8k W.

3. **Arbeitsmodus — Autor-getrieben.**
   - Autor gibt konkrete Rückmeldungen.
   - Claude wendet **minimale Edits** an, bevorzugt per Edit-Tool.
   - **Kein ungefragtes Umformulieren.** Auffälligkeiten flaggen, nicht selbst ändern.
   - **Keine Stil-Prüfung ohne Auftrag.** Kein neuer Stil-Check, kein Council.

4. **Deploy nach jeder Fix-Runde.** Status bleibt `lektorat`.

5. **Feedback-Loop.** Session bleibt offen, Kontext wächst nur langsam.

6. **Autor-Freigabe für `final`.**
   - Nie eigenmächtig setzen.
   - Bei Freigabe: Status → `final`, commit, deploy, **Handoff-File löschen**.

### Wichtige Regeln Phase 3

- **Keine Checks/Council mehr.**
- **Kein Prosa-Neu-Schreiben.** Bei großen Bitten: Hinweis auf Rückstufung.
- **Edit-Tool bevorzugt vor Write-Tool.**

## Neue Artefakte (einmalige Erstellung)

### Kompakte Referenzfiles

| Datei | Größe | Quelle | Pflege |
|---|---|---|---|
| `buch/00-canon-kompakt.md` | ~800 W | Destillat aus `00-welt.md` + `10-magie-system.md` | Manuell bei Bibel-Änderungen |
| `buch/kapitel-summaries.md` | ~150 W × Kapitelzahl | Einmalig rückwirkend Kap 1-11, danach pro neues final-Kapitel | Beim Setzen von `final` Hinweis an Autor |
| `buch/pov/alphina.md` | ~400 W | Destillat aus Weltbibel + Kapitel | Manuell, selten |
| `buch/pov/sorel.md` | ~400 W | dto | dto |
| `buch/pov/vesper.md` | ~400 W | dto | dto |
| `buch/pov/maren.md` | ~400 W | dto | dto |

### POV-Dossier-Template

```markdown
# POV — {Figur}

## Berufslinse
{Was sieht die Figur zuerst? Welche Metapher-Felder nutzt sie?}

## Körper-Leitmotiv
{Puls, Hände, Turm/Finger, etc. — was kehrt im Körperbild wieder?}

## Sprach-Signatur
{Verweis auf Stilregeln-Tabelle: Max Satzlänge, Rhythmus, typische Syntax}

## Wissensstand-Anker
{Was weiß die Figur seit welchem Kapitel? Was darf sie NICHT wissen?}

## Aktive Tschechow-Waffen
{Welche geladenen Details gehören zu dieser Figur? Wann feuern sie?}

## Beziehungs-Dynamik
{Zu wem wie? Aktueller Stand der Beziehungen.}
```

### Handoff-File-Schema

```markdown
# Handoff — B1-K12

**Von Phase:** entwurf → **Zu Phase:** ausarbeitung
**Erstellt:** 2026-04-09 14:32
**Status beim Handoff:** entwurf-ok

## Modell-Empfehlung
claude --model opus

## Aufruf für nächste Session
/ausarbeitung B1-K12

## Kontext für nächste Session
- POV: Vesper
- Wortziel: 4.000-4.500
- Timeline-Anker: Mitte März, nach K11
- Freigegebener Entwurf: buch/kapitel/B1-K12-entwurf.md
- Ton-Referenz: buch/kapitel/07-vesper.md (letztes Vesper-Kapitel)

## Anweisungen
- Prosa aus dem Entwurf ausarbeiten, Plot nicht verändern
- Jeder Dialog-Info-Punkt aus dem Entwurf muss in der Prosa landen
- Figurenstimme: max 20 W Satzlänge, Turm/Finger-Motiv, Zahnrad-Präzision

## Offene Punkte vom Entwurfs-Council
- {Findings die in der Ausarbeitung berücksichtigt werden sollen}
```

## Website-Änderung (`generate-lesen.sh`)

Die Website entscheidet anhand des Status, welches File sie anzeigt — und ob sie einen oder zwei Lese-Buttons zeigt:

| Status | Button-Anzeige | Verlinktes File |
|---|---|---|
| `idee` | kein Button | — |
| `entwurf` / `entwurf-checked` / `entwurf-ok` | "Entwurf lesen" | `entwurfs_datei` |
| `ausarbeitung` | "Entwurf lesen" + *(wird ausgearbeitet)* Label | `entwurfs_datei` |
| `lektorat` | "Entwurf lesen" + "Lektorat lesen" | beide Files |
| `final` | "Kapitel lesen" (primär) + "Entwurf ansehen" (sekundär) | `datei` (primär), `entwurfs_datei` (sekundär) |

**Pflichtfelder pro Status:**
- Ab `entwurf`: `entwurfs_datei` muss gesetzt sein
- Ab `lektorat`: `datei` muss gesetzt sein
- `final` ohne `datei` ist ein Fehler

## Modell-Matrix

| Command / Subagent | Modell | Begründung |
|---|---|---|
| `/entwurf` Hauptsession | **Sonnet** | Plot/Struktur, keine Prosa |
| Entwurf Logik-Check | Sonnet (Haiku optional) | Analyse |
| Entwurf Strukturanalyst | Sonnet | Analyse |
| Entwurf Beziehungs-Lektorin | Sonnet | Analyse |
| `/ausarbeitung` Hauptsession | **Opus** | Prosa, tragende Sprach-Arbeit |
| Stil-Check | Sonnet | Formale Zählungen |
| Final Stilkritiker | Sonnet (Opus auf Wunsch) | Medley-Check |
| Final Dark-Romance-Leserin | Sonnet | Genre-Check |
| Final Romantasy-Leserin | Sonnet | Genre-Check |
| `/lektorat-fix` Hauptsession | **Sonnet** (Haiku bei Mikro) | Punktuelle Edits |
| Handoff-Generator | **Haiku** | Format/Summary |
| Vorarbeit-Subagenten | Sonnet | Destillation |

**Subagenten-Dispatch:** Jeder Task-Call setzt `model:` explizit. Kein Verlass auf Default-Vererbung.

## Risiken & Mitigations

| Risiko | Mitigation |
|---|---|
| Kompakte Files driften von Bibel ab | Kaskaden-Regel in CLAUDE.md erweitern: bei Änderung in `00-welt.md` oder `10-magie-system.md` muss `00-canon-kompakt.md` aktualisiert werden |
| POV-Dossiers werden alt | In CLAUDE.md aufnehmen: Nach jedem `final`-Kapitel POV-Dossier-Update prüfen |
| Autor startet Phase 2 auf Sonnet statt Opus | Guard warnt beim Start. Modell-Hinweis im Handoff-File |
| Entwurf-Plot trägt nicht, Prosa-Phase entdeckt es zu spät | Phase 2 hat explizite Stop-Regel: zurück zu `/entwurf` |
| Kapitel-Summaries-File wächst ins Unbrauchbare | Bei > 40 Kapiteln in `kapitel-summaries-buch1.md` etc. splitten |
| Handoff-File verwaist | Jeder Command prüft beim Start ob Handoff zur aktuellen Phase passt |

## Vorarbeit (einmalig, vor Pipeline-Start)

1. `buch/00-canon-kompakt.md` erstellen (Subagent, Sonnet)
2. POV-Dossiers `buch/pov/{figur}.md` für Alphina, Sorel, Vesper, Maren erstellen
3. `buch/kapitel-summaries.md` rückwirkend für Kap 1-11 erstellen (teuerster Schritt, einmalig)
4. Neue Commands schreiben (`entwurf.md`, `ausarbeitung.md`, `lektorat-fix.md`)
5. `generate-lesen.sh` anpassen
6. `status.json` migrieren (neue Status-Liste)
7. `CLAUDE.md` aktualisieren mit neuer Pipeline
8. Alten `/kapitel`-Command archivieren (`kapitel-legacy.md` oder löschen)

## Out of Scope

- **Migration alter Kapitel-Dateien** auf das `B1-K12-{figur}.md`-Schema. Bestehende Files bleiben wie sie sind. Nur neue Kapitel ab jetzt verwenden den Prefix.
- **Eigene Buch-2/3-Ordner.** Solange wir in Buch 1 sind, bleibt alles in `buch/`. Bei Buch 2 wird neu entschieden.
- **Visuelle Website-Überarbeitung** über das Schalt-Verhalten hinaus. Layout bleibt wie es ist.
- **Automatisches Modell-Switching mitten in der Session.** Geht in Claude Code nicht; Workaround sind die Session-Breaks.
