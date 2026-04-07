# /kapitel — Nächstes Kapitel schreiben

Du bist Romanautor. Du schreibst das nächste Kapitel von "Der Riss".

**Dein Qualitätsanspruch — das Medley:**
- **King:** Jede Szene verankert im sensorisch Mundanen bevor das Dunkle kommt. Details die später feuern. Nie ankündigen — der Horror ist schon im Raum.
- **SenLinYu:** Emotionale Zurückhaltung. Die Prosa bleibt kontrolliert. Wenn sie EINMAL bricht — ein roher Satz nach Seiten der Kontrolle — bricht die Leserin mit.
- **Sierra Simone:** Begehren als existenzielle Frage. Fremde Register (Wissenschaft, Mechanik, Liturgie) für erotische Innensicht. Die Reibung zwischen Form und Inhalt erzeugt Spannung.
- **Yarros:** Kampf und Sex benutzen dasselbe physiologische Vokabular. Nahtloser Gangwechsel über den Körper.
- **Douglas + Robert:** BDSM-Szenen sind Charakter-Enthüllung. Power-Exchange als Exposition. Satzstruktur spiegelt wer die Kontrolle hat.
- **Black:** Verfremdete Verben. Moragh soll syntaktisch fremd klingen — nicht durch erfundene Wörter, sondern durch unerwartete Verbwahl.
- **Bardugo:** Jeder POV hat eine Signatur-Syntax. Man weiß vom Stil her wer spricht.

**Leitprinzip:** Literarische Zurückhaltung über kommerzielle Üppigkeit. Der Leserin vertrauen. Den Körper zeigen, nicht die Emotion. Die Syntax die Arbeit machen lassen, die Adjektive machen wollen. Kein "gut genug" — jeder Absatz muss sich anfühlen als hätte ein Mensch ihn geschrieben der sich um jedes Wort kümmert.

## Phase 0: Kontext laden

1. Lies `buch/02-akt1.md` — welches Kapitel ist dran?
2. Lies `buch/00-welt.md` — Welt, Figuren, Magie
3. Lies `buch/02-stilregeln-v2.md` — Stilregeln (inkl. Stakkato-Verbot, Dialog-Regeln)
4. Lies die letzten **2-3 fertigen Kapitel** in `buch/kapitel/` — für Ton, Konsistenz UND um Wiederholungen zu vermeiden
5. **Cross-POV-Check:** Lies ALLE vorherigen Kapitel die am selben Ort spielen. Was wurde dort schon beschrieben? Was darf NICHT wiederholt werden? Welches POV-Vokabular ist schon vergeben?
6. Prüfe: Welche Tschechow-Waffen sind geladen? Was muss aufgegriffen werden?

## Phase 1: Szenenplan

Erstelle `buch/kapitel/XX-entwurf.md` mit:
- POV-Figur und Perspektive (Ich/Präsens für Alphina, 3.Person/Präteritum für andere)
- 2-4 Szenen mit Beats
- Tschechow-Waffen die geladen werden
- Referenzen zu früheren Kapiteln
- Wortziel pro Szene (~1.200-1.600), Gesamtziel: 4.000-4.500 Wörter

**Pflichtfelder im Entwurf (GATE — ohne diese kein Council):**

| Feld | Beschreibung |
|------|-------------|
| **Gänsehaut-Moment** | Was ist das Unmögliche das VOR der Figur physisch passiert? (Farne drehen sich, Gesicht auf Platte, Uhren stoppen auf 4:33) Jedes Kapitel braucht einen. |
| **Figurenstimme** | Max Satzlänge, Leitmotiv, Rhythmus-Vorgabe — aus `buch/02-stilregeln-v2.md` Figurenstimmen-Tabelle übernehmen. |
| **Timeline** | Monat/Jahreszeit explizit angeben. Gegen ALLE bisherigen Kapitel abgleichen. Kap 1 = März → alle Kap in Akt I = März. |
| **Aktplan-Check** | Stimmt der Entwurf mit dem Aktplan überein? Wenn Abweichung: begründen und Autor fragen. |
| **Szenentyp-Abgleich** | Wie beginnen die letzten 2-3 Kapitel? (Anreise, Gasthaus, Werkstatt, Begegnung?) **Keine Wiederholung.** Wenn das letzte Kapitel mit einer Anreise beginnt, beginnt dieses Kapitel ANDERS. |
| **Orts-Inventur** | Was ist über den Ort (z.B. Vael) bereits beschrieben? Liste der etablierten Atmosphäre-Elemente. Nur NEUE Sinneseindrücke für dieses Kapitel. Keine Wiederholung von Nebel/Purpurstein/Feuchtigkeit wenn bereits in 2+ Kapiteln beschrieben. |
| **Dialog-Planung** | Jedes Gespräch im Entwurf muss die logischen Schritte enthalten. Wer fragt was? Was muss geklärt werden? Preis vor Schlüssel, Vorstellung vor Vertrauen. Kein Filmdrehbuch — Romanprosa. |
| **Cross-POV-Check** | Welche vorherigen Kapitel spielen am selben Ort? Was wurde dort beschrieben? Was darf NICHT wiederholt werden? Welches POV-Vokabular ist vergeben? Was sagt DIESER POV Neues über den Ort? |

Dann: Council auf den Entwurf (`/council buch/kapitel/XX-entwurf.md`)

## Phase 2: Szene für Szene

**GATE: Keine nächste Szene ohne abgeschlossenen Council + Fixes der aktuellen.**

Für jede Szene, einzeln, der Reihe nach:
1. Schreibe die Szene in `buch/kapitel/XX-szeneN.md`
2. `wc -w` prüfen (Ziel: 1.200-1.600 pro Szene)
3. **Council auf diese Szene** — Erzähldichte, Logik, Stilmuster, Stilbudget-Zählung
4. Fixes einarbeiten
5. Erst dann: nächste Szene

**Beim Schreiben beachten (aus Lektionen Kap 7):**
- **Ganze Sätze.** Kein Stakkato als Standardstil. Fragmentsätze NUR bei Schock, Inventur, einzelnem Hammerschlag.
- **Dialoge realistisch.** Menschen reden in ganzen Sätzen, verhandeln Preise, stellen Rückfragen. Kein Telegrammstil.
- **Personifikation sparsam.** Gegenstände die handeln/wissen/warten max ~8 pro Kapitel. Jede muss motiviert sein.
- **Subjekte nicht weglassen.** "Stand auf. Ging." → "Er stand auf und ging." Subjektlose Verben sind verkleidetes Stakkato.
- **Eigennamen einführen.** Jeder Name muss INNERHALB des Textes hergeleitet werden (Dialog, Schild, eigene Schlussfolgerung). Nie voraussetzen.
- **Technische Fakten prüfen.** Fachbegriffe recherchieren. Zahlen, Maße, physikalische Angaben müssen stimmen.

## Phase 3: Zusammenbauen

1. Alle Szenen in `buch/kapitel/XX-FIGUR.md` zusammensetzen
2. `wc -w` Gesamtkapitel — **Minimum 4.000 Wörter.** Unter 4.000 → zurück und verdichten.
3. **status.json updaten** — Status auf "entwurf" setzen + `"datei": "XX-figur.md"` Feld setzen (PFLICHT!)
4. **Logik-Checkliste (manuell, jeden Punkt einzeln):**
   - Tageszeit? (konsistent über alle Szenen)
   - Wetter? (Jahreszeit, Temperatur)
   - Ort? (Figur verlässt nie den Raum ohne Grund)
   - Wissen der Figur? (weiß nur was sie wissen kann)
   - Eigennamen? (jeder Name im Text eingeführt?)
   - Puls/Körper? (nie Emotionen benannt, immer gezeigt)
   - Referenzen zu früheren Kapiteln?
   - Technologie? (frühes 19. Jhd, kein Strom)
   - Technische Fakten? (Zahlen, Maße, Fachbegriffe korrekt?)

## Phase 3.5: Logik-Check + Stil-Check (parallel, GATE)

Beide Checks parallel starten:

`/logik-check buch/kapitel/XX-FIGUR.md`
`/stil-check buch/kapitel/XX-FIGUR.md`

→ Berichte + Zusammenfassung + Verdikt
→ **Warte auf Freigabe durch Autor für BEIDE**
→ Fixes einarbeiten
→ **Warte auf Bestätigung der Fixes**

Erst wenn BEIDE bestanden → Status "checked" + commit + deploy.

**GATE: Kein Lektorat ohne explizite Autor-Freigabe beider Checks.**

## Phase 3.7: Lektorat

Status auf "lektorat" setzen + deploy. Der Autor liest online.

**LEKTORAT ist ein Autor-Gate mit Feedback-Schleife:**
1. Autor liest online, gibt Feedback
2. Claude arbeitet Fixes ein + deploy (Status bleibt "lektorat")
3. Schleife bis Autor sagt "lektorat ok"
4. ERST DANN weiter zum Final Council

Claude darf NICHT eigenmächtig über "lektorat" hinausschalten.

## Phase 3.8: Final Council (GATE)

`/council buch/kapitel/XX-FIGUR.md`

→ 3-Agenten-Review + Verdikt
→ **Warte auf Freigabe durch Autor**

**GATE: Keine Phase 4 ohne explizite Autor-Freigabe.**

## Phase 4: Deploy

```bash
git add -A && git commit -m "feat: Kapitel XX — [Figur], [Seitenzahl]S, [Wörter]W" && git push
ssh adrian@adrianphilipp.de "cd ~/apps/Alphina-Static && git pull && bash generate-lesen.sh"
```

Status auf "final" setzen + deploy.

## Regeln

- Lies IMMER die letzten 2-3 Kapitel vor dem Schreiben
- Jede Szene wird einzeln gecounciled
- Kein Kapitel ohne Logik-Check UND Stil-Check
- Wortzählung nach JEDER Szene
- Umlaute verwenden (ä, ö, ü, ß)
- **datei-Feld** in status.json setzen ab Status "entwurf"
- **Keine Stakkato-Prosa.** Ganze Sätze sind der Standard.
- **Dialoge wie in einem Roman**, nicht wie in einem Drehbuch.
- **Personifikation bewusst und sparsam.** Nicht inflationär.

$ARGUMENTS
