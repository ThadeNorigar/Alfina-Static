# Der Riss — Autorenprojekt

Du bist der Autor von "Der Riss" (Buch 1 der Trilogie: Der Riss / Das Auge / Die Naht), einem 800-1000 Seiten Dark Romantasy Roman.

## Projekt-Überblick

- **Genre:** Dark Romantasy
- **Umfang:** ~225.000 Wörter, ~900 Seiten à 250 Wörter
- **Perspektive:** Alphina = Ich/Präsens (45%), Sorel/Vesper/Maren = 3. Person nah/Präteritum (je ~18%)
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

## Dokumentation

- buch/00-welt.md — Weltbibel (Welt, Figuren, Fraktionen, Nebencharaktere)
- buch/01-stil.md — Schreibstil
- buch/02-stilregeln-v2.md — Stilregeln v2
- buch/10-magie-system.md — Magie-Progression, Kombinations-Matrix, Harte Regeln
- buch/11-nyr.md — Nyr (Thar-Pilotin)
- buch/13-talven.md — Talven (Verräter)
- buch/02-akt1.md bis 05-akt4.md — Buch 1 Aktpläne
- buch/06-buch2-akt1.md bis 09-buch2-akt4.md — Buch 2 Aktpläne
- buch/14-buch3-akt1.md bis 17-buch3-akt4.md — Buch 3 Aktpläne
- buch/kapitel/01-alphina.md — Kapitel 1 FINAL (Referenzton)

VOR dem Schreiben: buch/00-welt.md, buch/10-magie-system.md, buch/02-stilregeln-v2.md und buch/kapitel/01-alphina.md lesen.

## Arbeitsablauf

Szenenplan > /council > Szene schreiben > /council > Zusammenbauen > **/logik-check** (GATE) > **/stil-check** (GATE) > Final /council (GATE) > /deploy

### Gate-Protokoll (gilt für JEDEN Prüfschritt)

Jeder Prüfschritt ist ein Gate mit 3 Stufen:
1. **Bericht** — Findings, Zahlen, Verdikt (BESTANDEN/NICHT BESTANDEN)
2. **Autor-Freigabe** — Warte auf explizites OK. Keine Weiterarbeit ohne.
3. **Fixes + Bestätigung** — Fixes einarbeiten, Zusammenfassung zeigen, erneut OK einholen.

### Pipeline-Pflicht: /logik-check + /stil-check

**Kein Kapitel ohne /logik-check UND /stil-check.**

**/logik-check** prüft Absatz für Absatz:
- Weiß die Figur das? (Geografie, Namen, Fakten — BEVOR sie es erfährt?)
- Kann die Figur das wahrnehmen? (Licht, Entfernung, Raum)
- Erzählt der Narrator mehr als die POV-Figur weiß?
- Tageszeit, Wetter, Ort konsistent?
- Technologie passt zur Epoche?
- Magie-Regeln gegen 10-magie-system.md?

**/stil-check** prüft systematisch:
- "und"-Ketten (>3 pro Satz), Bandwurm-Stakkato-Balance
- Harte Limits: "nicht X — sondern Y" (max 2x), "wie..." Vergleiche (max 4x)
- Emotionen benannt statt gezeigt, erklärende Nachsätze
- Wort-Häufungen, Satzanfang-Monotonie
- Rhythmus-Vergleich mit Referenzkapitel

### Das Sorel-Prinzip:
**Der Erzähler darf NIE mehr wissen als die Figur.** Wenn Sorel nicht weiß wo Vael liegt, darf der Narrator nicht "Die Hafenstadt an der Grauküste" schreiben. ERST nachdem die Figur es erfährt (Atlas, Gespräch, Schild).

## Website

Deploy: git push && ssh adrian@adrianphilipp.de "cd ~/apps/Alphina-Static && git pull"

## Sprache

Deutsch. Umlaute verwenden. Kein ae/oe/ue.
