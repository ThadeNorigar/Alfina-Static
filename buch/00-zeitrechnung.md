# Zeitrechnung — Canon

**Quelle:** `buch/zeitleiste.json.meta.zeitrechnung` (Canon), wiederhergestellt aus `zeitleiste.OLD.json` am 22. April 2026.

## Drei Zeitsysteme

### UZ (unsere Zeit, Gregorianisch)
- 24 h/Tag, 12 Monate/Jahr (Januar–Dezember, gregorianische Monatslängen 28–31 Tage).
- Schaltjahre nach gregorianischer Regel.

### TZ (Thalassien)
- **Identisch zur UZ-Struktur**: 24 h/Tag, 12 Monate/Jahr, 365/366 Tage/Jahr gregorianisch.
- Nur andere Jahreszählung + andere Monatsnamen.
- **TZ 0 = ~1269 UZ** (Erfindung des Uhrwerks).
- **UZ-Jahr = TZ-Jahr + 1269.** Monat und Tag 1:1 zu Gregorianisch.

| # | TZ-Monat | = UZ-Monat |
|---|---|---|
| 1 | Eismond | Januar |
| 2 | Sturmmond | Februar |
| 3 | Saatmond | März |
| 4 | Grünmond | April |
| 5 | Blütenmond | Mai |
| 6 | Lichtmond | Juni |
| 7 | Glutmond | Juli |
| 8 | Erntemond | August |
| 9 | Herbstmond | September |
| 10 | Nebelmond | Oktober |
| 11 | Frostmond | November |
| 12 | Dunkelmond | Dezember |

Realweltliche Monatsnamen in der Prosa **verboten** — immer thalassisch.

### MZ (Moragh)
- **26 h/Tag** (Eigenrotation).
- **8 Tage/Woche** (Gor-Umlauf, Roter Mond).
- **36 Tage/Monat = 4,5 Wochen** (Nyr-Umlauf, Bleicher Mond).
- **288 Tage/Jahr = 8 Monate** (Orbit ums "Auge").
- **Doppelflut** alle 72 Tage (beide Monde in Konjunktion).
- **MZ 0 = Besiedelung Moragh = TZ-Jahr −1.453.449** (absoluter Nullpunkt).
- **Keine Jahreszeiten im klassischen Sinn** — Halbjahre "Licht" (Monate 1–4) und "Dunkel" (Monate 5–8).

| # | MZ-Monat | Bedeutung | Halbjahr |
|---|---|---|---|
| 1 | Torash | Bogenwende | Licht |
| 2 | Ashral | Glutzeit | Licht |
| 3 | Keldath | Doppelflut | Licht |
| 4 | Reshvan | Ernteschluss | Licht |
| 5 | Dravon | Dämmerfall | Dunkel |
| 6 | Gormath | Rotmond | Dunkel |
| 7 | Nyrath | Bleichmond | Dunkel |
| 8 | Shelkam | Tiefnacht | Dunkel |

## Kopplung TZ ↔ MZ: Zeitdilatation 400:1

**1 MZ-Jahr = 400 TZ-Jahre.**

Das ist erzählerisch. Astronomisch würde 288 MZ-Tage × 26 MZ-Stunden = 7.488 "MZ-Stunden" nur 1/468 von 400 TZ-Jahren (= 3.504.000 Stunden) ausmachen — die Differenz ist eine **Zeitdilatation**: In Moragh fließt Zeit relativ zu Thalassien langsamer. 1 MZ-Stunde "dauert" ~468 TZ-Stunden aus externer Sicht.

**Praktisch für den Plot:**
- 1 MZ-Tag ≈ 1,3 TZ-Jahre
- 1 MZ-Monat ≈ 50 TZ-Jahre (genauer: 400/8 = 50)
- 1 MZ-Jahr = 400 TZ-Jahre (fest)

## Ankerpunkte

| Ereignis | TZ | UZ | MZ |
|---|---|---|---|
| **B1-Start** (K1, 21. Saatmond) | **21. Saatmond 551 TZ** | 21. März 1820 | **1. Torash 3635** |
| K22 (Plot-Gegenwart) | 22. Blütenmond 551 TZ | 22. Mai 1820 | 1. Torash 3635 (selber MZ-Tag!) |
| B1-Ende (K34) | 4. Dunkelmond 551 TZ | 4. Dezember 1820 | 1. Torash 3635 (~7 MZ-Tage später) |
| Elke Portal-Durchgang (I3) | 28. Frostmond 154 TZ | 28. November 1423 | 3. Torash 3634 (~1 MZ-Jahr vor B1) |
| MZ 0 (Besiedelung Moragh) | TZ −1.453.449 | ~UZ −184.180 | 1. Torash 0 |

## Konsequenzen für den Plot

1. **Ganz Buch 1 spielt in MZ 3635, Monat 1 (Torash).** Zwischen B1-Start und B1-Ende vergehen nur ~7 MZ-Tage.
2. **Varens Präsenz seit ~1 MZ-Jahr:** Elke kam in MZ 3634 (3. Torash) an, B1-Start ist MZ 3635 (1. Torash) — das ist praktisch genau 1 MZ-Jahr. Das bestätigt K35-Text "Über vierhundert Jährlein erspüret" (TZ-Jahre = 400 MZ-gerechnet wäre 1 MZ-Jahr ↔ 400 TZ-Jahre).
3. **Varens Alter:** Mitte–Ende 40 (MZ-Jahre). Wenn 1 MZ-Jahr = 400 TZ-Jahre, wäre er aus TZ-Sicht "18.000 TZ-Jahre alt" — aber das ist irrelevant, weil er in MZ lebt und dort ein ganz normaler Mitte-40er ist.
4. **4:33-Canon** (Vespers Uhren-Anomalie): Passt mit Varens "Atem-Signatur" wenn Varens Atemrhythmus in MZ-Zeit fein genug ist, dass er TZ-seitig als 4 min 33 sec/Tag-Drift sichtbar wird.

## Tool

```
python scripts/zeitrechnung.py uz 2026-04-22
python scripts/zeitrechnung.py tz "22. Blütenmond 551"
python scripts/zeitrechnung.py mz "1. Torash 3635"
```

Ausgabe: alle drei Zeitsysteme + Delta zum B1-Anker.

## Validierte Tests (22. Apr 2026)

| Eingabe | → UZ | → TZ | → MZ |
|---|---|---|---|
| TZ "21. Saatmond 551" | 21. März 1820 | 21. Saatmond 551 | 1. Torash 3635, 04h |
| TZ "22. Blütenmond 551" | 22. Mai 1820 | 22. Blütenmond 551 | 1. Torash 3635, 07h |
| TZ "4. Dunkelmond 551" | 4. Dezember 1820 | 4. Dunkelmond 551 | 1. Torash 3635, 17h |
| TZ "28. Frostmond 154" | 28. November 1423 | 28. Frostmond 154 | 3. Torash 3634, 21h |
| UZ "2026-04-22" (real-heute) | 22. April 2026 | 22. Grünmond 757 | 5. Dravon 3635 |
