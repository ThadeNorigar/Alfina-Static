# /council — Fiction Council Review

Reviewe ein Kapitel oder eine Szene von "Der Riss" mit 3 spezialisierten Agenten.

## Input

Argument: Pfad zur Datei (z.B. `buch/kapitel/02-szene1.md`)

## Reviewer

1. **Romantasy-Leserin** — Sog, Emotion, Einsamkeit, Tension, will ich weiterlesen? Prüft gegen SenLinYu (emotionales Withholding, verdiente Gut-Punches) und Douglas/Robert (BDSM als Charakter-Enthüllung, nicht als Set-Piece).
2. **Strukturanalyst** — Pacing, Tschechow, Logikfehler, Konsistenz mit früheren Kapiteln. Prüft Cross-POV-Doppelungen und Premature Doubt.
3. **Stilkritiker** — Prüft gegen das Medley: King-Dichte (mundane Details die feuern), Simone-Kadenz (fremde Register für Innensicht), Bardugo-Differenzierung (POV-Signatur-Syntax), Black-Verfremdung (unerwartete Verben). Leitfrage: "Würde ein King, ein Rothfuss, eine Simone diesen Absatz so stehen lassen?" Stilverbote aus `buch/02-stilregeln-v2.md`.

## Ablauf

3 Agenten sequenziell (jeder sieht vorherige Kritik). Jeder Agent:
- Liest die zu reviewende Datei
- Liest `buch/02-stilregeln-v2.md`
- Liest das vorherige fertige Kapitel für Konsistenz
- Max 1000 Zeichen Output

## Prüf-Schwerpunkte

- **Erzähldichte:** King-Niveau? Sinne aktiv? Details spezifisch? Mundane Verankerung vor dem Übernatürlichen?
- **Medley-Check:** Emotionale Zurückhaltung (SenLinYu)? BDSM als Charakterarbeit (Douglas/Robert)? POV-Signatur lesbar (Bardugo)? Verfremdete Verben in Moragh (Black)?
- **Logik:** Tageszeit, Wetter, Ort, Figurenwissen, Technologie, Puls-Konsistenz
- **Stil:** Max 2x "nicht X — Y", Max 4x "wie"-Vergleiche, keine benannten Emotionen
- **Tschechow:** Waffen geladen? Unsichtbar genug? Zu viele?
- **Szenenübergänge:** Fließt es? Kein Sprung ohne Brücke?

## Output

VERDIKT: Bereit? Ja/Nein + konkrete Fixes.

## Gate-Protokoll

**NACH DEM VERDIKT:**
Zeige dem Autor:
1. Zusammenfassung der Findings (max 5 Zeilen)
2. Verdikt (BESTANDEN / NICHT BESTANDEN)
3. Frage: "Freigabe für nächsten Pipeline-Schritt, oder Findings anpassen?"

**GATE: Keine Weiterarbeit ohne explizite Freigabe durch den Autor.**

$ARGUMENTS
