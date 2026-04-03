# /council — Fiction Council Review

Reviewe ein Kapitel oder eine Szene von "Die Schwelle" mit 3 spezialisierten Agenten.

## Input

Argument: Pfad zur Datei (z.B. `buch/kapitel/02-szene1.md`)

## Reviewer

1. **Romantasy-Leserin** — Sog, Emotion, Einsamkeit, Tension, will ich weiterlesen?
2. **Strukturanalyst** — Pacing, Tschechow, Logikfehler, Konsistenz mit früheren Kapiteln
3. **Stilkritiker** — King-Dichte, Stilverbote (buch/02-stilregeln-v2.md), Sinne, Rhythmus

## Ablauf

3 Agenten sequenziell (jeder sieht vorherige Kritik). Jeder Agent:
- Liest die zu reviewende Datei
- Liest `buch/02-stilregeln-v2.md`
- Liest das vorherige fertige Kapitel für Konsistenz
- Max 1000 Zeichen Output

## Prüf-Schwerpunkte

- **Erzähldichte:** King-Niveau? Sinne aktiv? Details spezifisch?
- **Logik:** Tageszeit, Wetter, Ort, Figurenwissen, Technologie, Puls-Konsistenz
- **Stil:** Max 2x "nicht X — Y", Max 4x "wie"-Vergleiche, keine benannten Emotionen
- **Tschechow:** Waffen geladen? Unsichtbar genug? Zu viele?
- **Szenenübergänge:** Fließt es? Kein Sprung ohne Brücke?

## Output

VERDIKT: Bereit? Ja/Nein + konkrete Fixes.

$ARGUMENTS
