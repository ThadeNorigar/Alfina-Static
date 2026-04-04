# /kapitel — Nächstes Kapitel schreiben

Du schreibst das nächste Kapitel von "Die Schwelle".

## Phase 0: Kontext laden

1. Lies `buch/02-akt1.md` — welches Kapitel ist dran?
2. Lies `buch/00-welt.md` — Welt, Figuren, Magie
3. Lies `buch/02-stilregeln-v2.md` — Stilregeln
4. Lies das letzte fertige Kapitel in `buch/kapitel/` — für Ton und Konsistenz
5. Prüfe: Welche Tschechow-Waffen sind geladen? Was muss aufgegriffen werden?

## Phase 1: Szenenplan

Erstelle `buch/kapitel/XX-entwurf.md` mit:
- POV-Figur und Perspektive (Ich/Präsens für Alphina, 3.Person/Präteritum für andere)
- 2-4 Szenen mit Beats
- Tschechow-Waffen die geladen werden
- Referenzen zu früheren Kapiteln
- Wortziel pro Szene (~1.200-1.600), Gesamtziel: 4.000-4.500 Wörter

Dann: Council auf den Entwurf (`/council buch/kapitel/XX-entwurf.md`)

## Phase 2: Szene für Szene

**GATE: Keine nächste Szene ohne abgeschlossenen Council + Fixes der aktuellen.**

Für jede Szene, einzeln, der Reihe nach:
1. Schreibe die Szene in `buch/kapitel/XX-szeneN.md`
2. `wc -w` prüfen (Ziel: 1.200-1.600 pro Szene)
3. **Council auf diese Szene** — Erzähldichte, Logik, Stilmuster, Stilbudget-Zählung
4. Fixes einarbeiten
5. Erst dann: nächste Szene

## Phase 3: Zusammenbauen

1. Alle Szenen in `buch/kapitel/XX-FIGUR.md` zusammensetzen
2. `wc -w` Gesamtkapitel — **Minimum 4.000 Wörter.** Unter 4.000 → zurück und verdichten.
3. **Logik-Checkliste (manuell, jeden Punkt einzeln):**
   - Tageszeit? (konsistent über alle Szenen)
   - Wetter? (Jahreszeit, Temperatur)
   - Ort? (Figur verlässt nie den Raum ohne Grund)
   - Wissen der Figur? (weiß nur was sie wissen kann)
   - Puls/Körper? (nie Emotionen benannt, immer gezeigt)
   - Referenzen zu früheren Kapiteln?
   - Technologie? (frühes 19. Jhd, kein Strom)

## Phase 3.5: Automatische Prüfung

Starte einen Agent (Sonnet) der das Gesamtkapitel prüft UND Fixes direkt einarbeitet.

**Input für den Agent:**
- Das Gesamtkapitel (`buch/kapitel/XX-FIGUR.md`)
- Die Weltbibel (`buch/00-welt.md`)
- Die Stilregeln (`buch/02-stilregeln-v2.md`)
- Das vorherige fertige Kapitel (für Konsistenz)

**Agent-Prompt (alle Checks in einem Durchlauf):**

```
Du bist der Lektor von "Die Schwelle". Lies das Kapitel, die Weltbibel, die Stilregeln und das vorherige Kapitel. Führe ALLE folgenden Checks durch und arbeite Fixes DIREKT in die Datei ein.

HARTE CHECKS (mit Grep zählen, dann fixen):
1. "nicht X — sondern Y" Konstruktionen: Max 2x pro Kapitel. Überzählige umschreiben.
2. "wie etwas das..." Vergleiche: Max 4x pro Kapitel. Überzählige umschreiben.
3. Wort/Phrase die >7x vorkommt: Variieren oder streichen.
4. Ortsnamen und Himmelsrichtungen: Gegen Weltbibel prüfen. Fixes einarbeiten.
5. Technologie: Frühes 19. Jhd. Kein Strom, keine Motoren. Anachronismen fixen.

WEICHE CHECKS (LLM-Urteil, dann fixen):
6. Erklärende Nachsätze ("weil...", "nicht weil... sondern weil..."): Streichen wenn der Leser es ohne versteht.
7. Emotionen benannt statt gezeigt ("Er war traurig"): Durch Körperreaktion ersetzen.
8. Zusammenfassende Sätze die wiederholen was gerade passiert ist: Streichen.
9. Figurenwissen: Weiß die Figur etwas das sie nicht wissen kann? Fixen.
10. Magie angekündigt ("Plötzlich geschah etwas Seltsames"): Mitten in den Alltag einbauen.

NACH ALLEN FIXES:
- wc -w auf die Datei
- Erstelle einen Prüfbericht als Antwort:

## Prüfbericht Kapitel XX
- Fixes: N eingearbeitet
- Wörter: vorher → nachher
- Verbleibende Findings (falls etwas nicht auto-fixbar):
| # | Typ | Stelle | Problem |
```

**Nach dem Agent:** Prüfbericht lesen. Wenn verbleibende Findings → manuell entscheiden. Dann weiter.

## Phase 3.6: Final Council

Final Council auf das geprüfte Gesamtkapitel.

## Phase 4: Deploy

```bash
# Kapitel zusammenbauen, committen, deployen
git add -A && git commit -m "feat: Kapitel XX — [Figur], [Seitenzahl]S, [Wörter]W" && git push
ssh adrian@adrianphilipp.de "cd ~/apps/Alphina-Static && git pull"
```

## Regeln

- Lies IMMER das vorherige Kapitel vor dem Schreiben
- Jede Szene wird einzeln gecounciled
- Kein Kapitel ohne Logik-Check
- Wortzählung nach JEDER Szene
- Umlaute verwenden (ä, ö, ü, ß)

$ARGUMENTS
