# /kommentare — Kommentare zu einem Kapitel abrufen

Ruft alle Anmerkungen ab die Leser:innen auf der WIP-Seite hinterlassen haben.

## Nutzung

- `/kommentare B1-K17` — Alle Kommentare zu Kapitel 17 (Entwurf + Final)
- `/kommentare B1-K17 entwurf` — Nur Entwurfs-Kommentare
- `/kommentare B1-K17 final` — Nur Kommentare zur finalen Fassung
- `/kommentare` — Kommentare aller Kapitel (Übersicht)

## Was der Skill tut

### Mit Kapitel-Argument (`/kommentare B1-K17`)

1. Kapitel-ID aus Argument ableiten: `B1-K17` → Slug `17`, `B1-KI3` → Slug `I3`
2. API-Aufruf via Bash (Admin-Key für alle Kommentare aller Nutzer):
   ```bash
   curl -s "https://alphina.net/api/comments?kapitel=17&modus=entwurf" -H "X-User-Id: 21c7ef896af35a6ce31b79c1f712b94a4f1d523b911de20e"
   curl -s "https://alphina.net/api/comments?kapitel=17&modus=final" -H "X-User-Id: 21c7ef896af35a6ce31b79c1f712b94a4f1d523b911de20e"
   ```
3. Ergebnisse zusammenführen und nach `absatz_idx` gruppieren
4. Ausgabe als übersichtliche Liste:
   - Überschrift mit Kapitel-ID und Gesamtanzahl
   - Pro Absatz: Index, Absatz-Anker (erste 80 Zeichen), dann alle Kommentare mit Datum
   - Wenn kein Kommentar: kurze Meldung "Noch keine Anmerkungen."

### Ohne Argument (`/kommentare`)

1. Alle Kapitel-IDs aus `buch/status.json` sammeln die `entwurfs_datei` oder `datei` haben
2. Pro Kapitel: `curl -s "https://alphina.net/api/comments?kapitel={id}&modus=entwurf" -H "X-User-Id: 21c7ef896af35a6ce31b79c1f712b94a4f1d523b911de20e"` + `modus=final`
3. Nur Kapitel mit mindestens einem Kommentar anzeigen
4. Format: `K17 · 3 Anmerkungen (entwurf)`, `K21 · 1 Anmerkung (final)`

## Ausgabe-Format

```
K17 — Entwurf · 3 Anmerkungen

  Absatz 2 · "Die Gasse roch nach Kohle und altem Regen…"
    → Das klingt sehr dicht, gefällt mir gut (12.04.26 · 14:23)
    → Warum Kohle? Gaslampen wären passender (12.04.26 · 15:01)

  Absatz 7 · "Sorel lehnte die Stirn gegen das Glas…"
    → Hier fehlt mir die Reaktion auf das was er sieht (12.04.26 · 16:42)
```

## Regeln

- Datum im Format `TT.MM.JJ · HH:MM`
- Absatz-Anker auf 80 Zeichen kürzen, mit `…` wenn abgeschnitten
- Wenn modus-Filter angegeben: nur diesen Modus abfragen
- Keine leeren Sections ausgeben
- Bei API-Fehler: klare Fehlermeldung, nicht stilllschweigend scheitern

$ARGUMENTS
