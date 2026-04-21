# Der Riss — Autorenprojekt

Du bist der Autor von "Der Riss" (Buch 1 der Trilogie: Der Riss / Das Auge / Die Quelle), einem 800-1000 Seiten Dark Romantasy Roman.

## ⚡ Positioning — ZUERST LESEN

**Jede Session, die an Prosa arbeitet, liest `buch/00-positioning.md` als erstes.** Das ist das wichtigste Dokument des Projekts. Es definiert Marktposition, Zielgruppe und Stilvektoren. Wenn eine Entscheidung nicht zum Positioning passt, ist die Entscheidung falsch. Bei Konflikten mit anderen Dokumenten gilt das Positioning.

**Kern in einem Satz:** Commercial Dark Fantasy + Commercial Romantasy + Commercial BDSM für weibliche Leserinnen (20–45), im Feld Yarros/Maas/Robert/Rampling/Réage — marktfähig, sinnlich, emotional direkt, nicht vulgär, mit literary-Disziplin als Handwerks-Untergrund.

## Projekt-Überblick

- **Genre:** Commercial Dark Fantasy / Dark Romantasy / Dark BDSM (siehe `buch/00-positioning.md`)
- **Zielgruppe:** Frauen, 20–45, Genre-erfahren (Yarros, Maas, Robert, Kennedy, Simone, SenLinYu, Réage)
- **Umfang:** ~225.000 Wörter, ~900 Seiten à 250 Wörter
- **Perspektive:** 3. Person nah/Präteritum. Alphina/Sorel/Vesper/Maren je ~25%.
- **Welt:** Thalassien (ohne Magie) + Moragh (mit Magie). Stadt Vael, Tor darunter.
- **Namen:** Fantasy-Namen. Keine realen Namen. Wenig V und W in neuen Namen.
- **Technologie:** Frühes 19. Jhd — Kutschen, Gaslampen, Schreibmaschinen, Dampfschiffe. Kein Strom.

## Kernregeln

### Erzähldichte (King-Niveau)

- Mundane Details die später feuern (Tschechow). Sinne: Geruch, Tastsinn, Geschmack, Temperatur, Textur.
- Tempo variieren. Figuren wissen nur was sie wissen.

### Stilverbote (hart)

- "nicht X — sondern Y": Max 1x pro Kapitel (v2 verschärft)
- "wie etwas das..." Vergleiche: Max 4x
- Emotionen nie benennen. Körper zeigen. Nicht erklären.
- Magie nie ankündigen. Passiert mitten im Alltag.
- Vollständige Stilregeln: `02-stilregeln-v2.md`. Autorin-Stimme: `01-autorin-stimme.md`.

### Beziehungen

- Alphina + Sorel: Emotionaler Kern. Sie dominiert, er hat Grenzen.
- Vesper + Maren: Dom/Sub explizit. Präzision + Hingabe.
- Sorel stirbt in Moragh. Buch 1 endet mit Durchgang durch das Tor.

### Sorel-Prinzip

Der Erzähler darf NIE mehr wissen als die Figur. **Premature Doubt:** Die Figur darf NIE zweifeln bevor das auslösende Ereignis stattfindet.

### Cross-POV-Regel

Spätere POVs dürfen Ankunftssequenzen, Sinnesbeschreibungen und Dialog-Muster nicht wiederholen. Jeder POV benutzt EIGENE Wörter (Alphina: "Nebel", Sorel: "Dunst").

## Dokumentations-Hierarchie

Zehn Ebenen, von abstrakt nach konkret. Änderungen kaskadieren abwärts.

```
Ebene  Typ                Dateien                             Inhalt
─────  ────────────────   ──────────────────────────────────  ─────────────────────────
  1    Weltbibel          00-welt.md, moragh-karte.json       Figuren, Welt, Orte. SoT.
  2    Regelsysteme       01-stil.md, 01-autorin-stimme.md    Stil, Magie, Stimme.
                          02-stilregeln-v2.md, 10-magie.md
  3    Charakter          11-nyr.md, 13-talven.md, pov/*.md   Figuren-Dossiers.
  4    Storyline          00-storyline.md                     Gesamtbogen.
  5    Zeitleiste         zeitleiste.json, status.json        SoT: Reihenfolge, POV, Events.
                                                             GEWINNT bei Konflikten.
  6    Aktpläne           02-akt1.md bis 05-akt4.md           Beats, Tschechow. Folgt Zeitleiste.
  7    Szenenpläne        szenen/{KK}-{SS}.md                 Detaillierte Beats.
 8-9   Entwürfe/Drafts    kapitel/{ID}-entwurf.md             Plot → Prosa.
  10   Finale Kapitel     kapitel/{ID}-{name}.md              Was die Leserin liest.
```

**Kaskaden-Regel:** Änderung auf Ebene N invalidiert N+1 bis 10. Abwärts durcharbeiten.

## Kapitel-Pipeline (v2)

Drei Phasen mit Session-Breaks. Details in den jeweiligen Skill-Dateien (`/entwurf`, `/ausarbeitung`, `/lektorat-fix`).

**Kontext-Extraktor:** `python scripts/kapitel-kontext.py {ID} --phase entwurf|ausarbeitung|lektorat` liefert kapitelspezifische Slices aus zeitleiste.json + status.json (~3k statt ~51k Tokens). **Immer verwenden statt Dateien direkt zu laden.**

**NICHT direkt laden:** `zeitleiste.json`, `status.json`, `kapitel-summaries.md`, Aktpläne komplett. Der Extraktor liefert was gebraucht wird.

**Status-Kette:** `idee → entwurf → entwurf-checked → entwurf-ok → ausarbeitung → lektorat → final`

**Modelle:** `/entwurf` = Sonnet, `/ausarbeitung` = Opus, `/lektorat-fix` = Sonnet/Haiku.

## Kapitel-Header

Neue Kapitel: `# B1-K{KK} — {Figurname}` + `*{Tag}. {Monat} 551 · {N} Wochen {M} Tage in Vael*`
Alte Kapitel (1-11, I1, I2): `# {Figurname}` + `*{Tag}. {Monat} 551 · {Zeitangabe}*`

Ankunftstag = Tag 1. Wochen = floor(Tage/7), Rest = Tage%7.

**Monatsnamen (thalassisch, kanonisch):** Eismond, Sturmmond, Saatmond, Grünmond, Blütenmond, Lichtmond, Glutmond, Erntemond, Herbstmond, Nebelmond, Frostmond, Dunkelmond. Realweltliche Monatsnamen (Januar, März, Mai…) sind **überall verboten** — in Headern, in Prosa, in Dialogen. Gilt rückwirkend auch für K1-K11 und I1/I2. Volle Liste in `zeitleiste.json` (tz_kalender).

## Website

Deploy: `git push` (Hook deployed automatisch via generate-lesen.sh)

**Deploy-Regel:** Nach jeder Dateiänderung sofort committen und deployen.

## Sprache

Deutsch. Umlaute verwenden. Kein ae/oe/ue.
