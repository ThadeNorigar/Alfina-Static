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
- Wortziel pro Szene (~1.200-1.600)

Dann: Council auf den Entwurf (`/council buch/kapitel/XX-entwurf.md`)

## Phase 2: Szene für Szene

Für jede Szene:
1. Schreibe die Szene in `buch/kapitel/XX-szeneN.md`
2. `wc -w` prüfen
3. Council: Erzähldichte, Logik, Stilmuster
4. Fixes einarbeiten
5. Logik-Checkliste durchgehen

## Phase 3: Zusammenbauen

1. Alle Szenen in `buch/kapitel/XX-FIGUR.md` zusammensetzen
2. `wc -w` Gesamtkapitel (Ziel: 3.500-5.000)
3. Systematischer Logik-Check über das ganze Kapitel
4. Final Council auf Gesamtkapitel

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
