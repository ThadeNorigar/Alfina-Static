# /logik-check — POV-Konsistenz und Logikprüfung

Du prüfst ein Kapitel von "Der Riss" auf Logikfehler. Absatz für Absatz. Brutal.

## Input

`$ARGUMENTS` = Pfad zur Kapitel-Datei (z.B. `buch/kapitel/02-sorel.md`)

Wenn kein Argument: frage welche Datei.

## Phase 0: Kontext laden

Lies parallel:
1. Die Kapitel-Datei
2. `buch/00-welt.md` — Welt, Orte, Figuren
3. `buch/10-magie-system.md` — Magie-Regeln
4. Das VORHERIGE Kapitel (für Kontinuität)

Bestimme:
- **POV-Figur** des Kapitels (aus dem Titel oder ersten Absätzen)
- **Perspektive** (ALLE POVs = 3. Person nah/Präteritum)
- **Wissensstand** der Figur zu Beginn des Kapitels (was weiß sie aus vorherigen Kapiteln?)

## Phase 1: Wissens-Audit (der Hauptcheck)

Gehe JEDEN Absatz durch. Für jeden Absatz frage:

**1. Weiß die Figur das?**
- Geografie: Kennt sie den Ort? Woher? Hat sie eine Karte gesehen? Hat jemand es ihr gesagt?
- Namen: Kennt sie den Namen? Wurde er eingeführt?
- Fakten über andere Figuren: Kann sie das wissen? Hat sie es beobachtet/gehört?
- Hintergrundwissen: Ist das Allgemeinwissen in dieser Welt oder Spezialwissen?

**2. Kann die Figur das wahrnehmen?**
- Sicht: Ist es hell genug? Ist sie nah genug? Steht etwas im Weg?
- Geräusche: Ist es still genug um das zu hören?
- Geruch: Ist sie nah genug?
- Ist die Figur im richtigen Raum? Hat sie den Raum betreten/verlassen?

**3. Erzählt der Narrator mehr als die Figur weiß?**
- 3. Person nah = der Narrator weiß NUR was die Figur weiß
- Alphina = engste 3. Person nah, NUR ihre Wahrnehmung
- Keine auktorialen Einschübe. Kein "Sie wusste nicht dass..."
- Der Narrator darf NICHT vorgreifen: keine Info die erst später im Kapitel etabliert wird
- **Premature Doubt:** Die Figur darf NICHT zweifeln oder hinterfragen bevor das auslösende Ereignis stattfindet. Wenn Sorel erst in Szene 3 sein Gesicht auf dem Schemen sieht, darf er in Szene 1 nicht fragen ob die Platte "wirklich sein Gesicht" zeigt.

**4. Timeline im Absatz:**
- Tageszeit: konsistent mit dem vorherigen Absatz?
- Wetter: hat es sich geändert? Warum?
- Zeitsprünge: markiert? (Szenenwechsel, Einschlafen, Aufwachen)

## Phase 2: Technologie-Check

- Frühes 19. Jahrhundert (Buch 1, Thalassien): Gaslampen, Kutschen, Glasplatten, Druckpressen, Dampfschiffe. KEIN Strom, keine Motoren, keine Telefone, keine Fotografie mit Film (nur Nassplatten/Daguerreotypien).
- Moragh: Mittelalter/Frühe Neuzeit + Magie. Keine Thalassien-Technik außer was mitgebracht wird.
- Buch 3 Thalassien: ~2250. Dann ja: Elektrizität, KI, etc.

## Phase 3: Magie-Check

- Buch 1 (Thalassien): Magie ist SUBTIL. Könnte Zufall sein. Keine Gewächshäuser, keine Flutwellen.
- Buch 2 (Moragh): Thalassier zahlen KEINEN persönlichen Preis. Moragh zahlt.
- Moragh-Geborene: zahlen mit Müdigkeit/Muskelkater (normal), Nasenbluten nur bei Übergebrauch.
- Kombinationen: prüfe gegen `10-magie-system.md`.

## Phase 4: Kontinuitäts-Check

- Referenzen zu früheren Kapiteln: stimmen sie?
- Figur-Positionen: ist die Figur dort wo sie sein sollte?
- Gegenstände: hat die Figur das Objekt bei sich? Wurde es erwähnt?
- Beziehungen: Weiß Figur A schon von Figur B? Haben sie sich getroffen?
- **Tschechow-Beat:** Wenn ein Tschechow-Detail eingeführt wird (ein Vormieter, ein Nagel, ein Geruch) — reagiert die Figur mit mindestens einem körperlichen Beat? Null Reaktion = Finding.
- **Cross-POV-Dopplung:** Wiederholt dieses Kapitel Beschreibungen oder Szenentypen aus einem früheren POV-Kapitel am selben Ort? (Ankunft, Unterkunft-Dialog, Geruchsbeschreibung) → Finding.

## Phase 5: Timeline-Sync + Gänsehaut-Check

**Timeline-Sync:**
- Welcher Monat/Jahreszeit ist dieses Kapitel?
- Gegen ALLE bisherigen Kapitel prüfen. Kap 1 (Alphina) = März. Alle Akt-I-Kapitel müssen synchron sein.
- Wetter, Vegetation, Tageslänge — passen sie zur Jahreszeit?
- Finding wenn Monat/Jahreszeit nicht explizit bestimmbar oder widersprüchlich.

**Gänsehaut-Check:**
- Gibt es im Kapitel einen Moment wo etwas physisch Unmögliches VOR der Figur passiert?
- Nicht intellektuell (eine Zahl die nicht passt). Physisch (Uhren stoppen, Farne drehen sich, Gesicht auf alter Platte).
- Wenn kein Gänsehaut-Moment: **KRITISCHES FINDING.**

## Output

Erstelle einen Bericht:

```
## Logik-Check: [Dateiname]
POV: [Figur] | Perspektive: [Ich/3.P] | Wissensstand: [kurz]

### Findings

| # | Zeile | Typ | Problem | Fix-Vorschlag |
|---|-------|-----|---------|---------------|
| 1 | ~43 | WISSEN | Sorel weiß dass Vael an der Grauküste liegt bevor er den Atlas aufschlägt | Geografie erst NACH Atlas-Szene |
| 2 | ~67 | WAHRNEHMUNG | "Er sah das Schiff am Horizont" — es ist Nacht, kein Mond | Stattdessen: er HÖRT das Schiff |

### Sauber
- [Was keine Probleme hat]

### Zusammenfassung
- Findings: N
- Kritisch (Wissen/Timeline): N
- Leicht (Wahrnehmung/Stil): N
```

## Gate-Protokoll

**NACH DEM BERICHT:**
Frage den Autor: "Bericht gelesen? Freigabe oder Findings anpassen?"

**GATE: Keine Weiterarbeit ohne explizite Freigabe durch den Autor.**

Wenn Freigabe erteilt:
- Arbeite die vereinbarten Fixes ein
- Zeige Zusammenfassung der Änderungen
- Frage erneut: "Fixes OK? Weiter mit nächstem Pipeline-Schritt?"

## Regeln

- JEDEN Absatz prüfen. Nicht überfliegen.
- Im Zweifel: Finding erstellen. Lieber zu viel flaggen als zu wenig.
- Keine Fixes ohne Freigabe. Nur Bericht.
- Fokus auf das Sorel-Problem: "Erzähler weiß mehr als die Figur."
