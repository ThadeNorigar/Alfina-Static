# /stil-check — Stilprüfung und Rhythmus-Analyse

Du prüfst ein Kapitel von "Der Riss" auf Stilprobleme. Systematisch, mit Zahlen.

## Input

`$ARGUMENTS` = Pfad zur Kapitel-Datei (z.B. `buch/kapitel/02-sorel.md`)

Wenn kein Argument: frage welche Datei.

## Phase 0: Kontext laden

Lies parallel:
1. Die Kapitel-Datei
2. `buch/02-stilregeln-v2.md` — Stilregeln
3. `buch/kapitel/01-alphina.md` — Referenzton (Kapitel 1 ist der Maßstab)
4. Das VORHERIGE Kapitel (für Stil-Konsistenz)

Bestimme:
- **POV-Figur** und **Perspektive** (ALLE POVs = 3. Person nah/Präteritum)
- **Figurenstimme** aus `buch/02-stilregeln-v2.md` Figurenstimmen-Tabelle laden:
  - Max Satzlänge (Alphina ~40W, Sorel ~50W, Vesper ~20W, Maren ~35W)
  - Leitmotiv (Puls, Hände, Turm/Finger, ?)
  - Rhythmus-Erwartung

## Phase 1: Harte Zählungen (mit Grep)

Zähle mit Grep/Bash — keine Schätzungen:

| Muster | Max | Aktion wenn über Limit |
|--------|-----|----------------------|
| "nicht X — sondern Y" / "nicht X, sondern Y" | 2x pro Kapitel | Überzählige markieren |
| "wie etwas das..." / "wie ein..." Vergleiche | 4x pro Kapitel | Überzählige markieren |
| "und" als Satzverbinder (Hauptsatz und Hauptsatz) | Meldung ab >3 in einem Satz | Ketten markieren |
| Wort/Phrase die >7x vorkommt (außer Artikeln/Pronomen) | 7x | Häufung markieren |
| Markante Phrase (z.B. "dreizehn Jahre", "die Routine") | 4x | Jede über 4 markieren |
| "als hätte/wäre/könnte..." Hypothetische Konstruktionen | ~6 | Dichte-Warnung |
| Sätze über figurenspezifischem Limit | Alphina >40W, Sorel >50W, Vesper >20W, Maren >35W | Überlängen markieren |
| Sätze >60 Wörter | Meldung | Bandwurm-Kandidaten markieren (alle Figuren) |

## Phase 2: Rhythmus-Analyse

Gehe das Kapitel Absatz für Absatz durch:

**1. Bandwurm-Stakkato-Balance:**
- Folgen zwei Bandwurm-Sätze (>40 Wörter) direkt aufeinander? → Finding
- Gibt es Passagen >500 Wörter ohne einen Einwortsatz oder Fragment? → Finding
- Unter Druck/Schock: bricht die Syntax? (Einwortsätze, Fragmente, Abbrüche) → Wenn nicht: Finding

**2. "und"-Ketten:**
- Sätze mit >3 "und"-Verbindungen als Hauptsatz-Reiher identifizieren
- Absätze mit >5 "und"-Verbindungen markieren
- Vergleich: wie viele "und"-Ketten hat Kapitel 1 pro 1000 Wörter vs. dieses Kapitel?

**3. Satzanfänge:**
- Gleicher Satzanfang >3x in einem Absatz? → Finding
- "Er/Sie/Ich" als Satzanfang >40% der Sätze? → Finding

## Phase 3: Stilregeln-Check

**1. Emotionen benannt statt gezeigt:**
- Suche nach: "war traurig", "fühlte Angst", "war wütend", "spürte Freude", "war nervös", "war einsam"
- Auch indirekt: "kein Schmerz, keine Angst" (benennt durch Negation)
- → Markieren. Körperreaktion stattdessen.

**2. Erklärende Nachsätze:**
- Sätze die enden mit "weil..." wo die Handlung für sich spricht
- Sätze die zusammenfassen was gerade passiert ist
- "als hätte/wäre/könnte..." Anhänge die nur das Offensichtliche erklären
- → Markieren. Braucht die Leserin das?

**3. Magie-Ankündigungen:**
- "Plötzlich geschah etwas Seltsames/Unerwartetes"
- "Etwas war anders"
- Jede Meta-Kommentierung von Magie durch den Erzähler
- → Magie passiert mitten im Alltag. Nie ankündigen.

## Phase 3.5: Cross-POV und Aftermath

**1. Cross-POV-Vokabular:**
- Benutzt dieser POV dieselben Beschreibungen wie ein anderer POV für denselben Ort?
- Prüfe gegen `02-stilregeln-v2.md` POV-Vokabular-Tabelle
- Finding wenn identische Formulierungen für Stein, Nebel, Geruch etc.

**2. Aftermath-Pacing:**
- Nach einem Climax-Moment (Horror, Enthüllung, Gänsehaut): gibt es mindestens 3 Beats?
- Körper → Raum → Stille → Frage
- Finding wenn direkt nach dem Peak zum Kapitelende gesprungen wird

## Phase 4: Vergleich mit Referenzkapitel

Kurzer Abgleich mit Kapitel 1:
- Stimmt die Erzähldichte? (Sinne pro Absatz, spezifische Details)
- Stimmt das Tempo? (Kapitel 1 hat ~200 Wörter pro Minute Lesezeit, Pausen durch Fragmente)
- Stimmt der Figurenton? (Alphina = Kontrolle + Risse. Sorel = Stille + Hände.)

## Output: Gate-Bericht

```
## Stil-Check: [Dateiname]
POV: [Figur] | Perspektive: [Ich/3.P] | Wörter: [N]

### Harte Zählungen
| Muster | Gefunden | Limit | Status |
|--------|----------|-------|--------|
| "nicht X — sondern Y" | N | 2 | OK/ÜBER |
| "wie..." Vergleiche | N | 4 | OK/ÜBER |
| "und"-Ketten (>3 pro Satz) | N | — | Meldung |
| Wort-Häufungen (>7x) | [Wort]: Nx | 7 | OK/ÜBER |
| Bandwurm-Sätze (>60W) | N | — | Meldung |

### Findings

| # | Zeile | Typ | Problem | Fix-Vorschlag |
|---|-------|-----|---------|---------------|
| 1 | ~63 | UND-KETTE | 7x "und" in einem Satz | Aufbrechen: Punkte statt "und" |
| 2 | ~37 | BANDWURM | 2 Bandwürmer hintereinander, kein Stakkato | Fragment einfügen |
| 3 | ~67 | EMOTION | "kein Schmerz, keine Angst" benennt Emotionen | Nur Körperbild: "der Moment bevor man fällt" |

### Sauber
- [Was gut funktioniert — Leitmotive, Sinne, Rhythmus-Stellen die sitzen]

### Zusammenfassung
- Findings gesamt: N
- Kritisch (Harte Limits überschritten): N
- Rhythmus (und-Ketten, Bandwürmer): N
- Stil (Emotionen, Nachsätze, Ankündigungen): N

### Verdikt
**BESTANDEN** / **NICHT BESTANDEN** — [Begründung in einem Satz]
```

**NACH DEM BERICHT:**
Frage den Autor: "Bericht gelesen? Soll ich die Fixes einarbeiten, oder willst du Findings streichen/anpassen?"

**GATE: Keine Weiterarbeit ohne explizite Freigabe durch den Autor.**

## Regeln

- JEDEN Absatz prüfen. Nicht überfliegen.
- Harte Zählungen mit Grep — keine Schätzungen.
- Im Zweifel: Finding erstellen.
- Keine Fixes ohne Freigabe. Nur Bericht.
- Der Autor entscheidet was gefixt wird und was bleibt.

$ARGUMENTS
