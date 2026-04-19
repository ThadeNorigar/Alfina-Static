# Vael — Bildgenerator-Prompt für Stadtkarte

## 0. Quelle der Wahrheit

Alle Koordinaten und Fakten stammen aus `buch/vael-karte.json` (viewBox 1200×800,
1 Einheit ≈ 4 m → Stadt ≈ 4,8 × 3,2 km). Kanon: `buch/00-welt.md`, Kapitel K1–K24.

---

## 1. Welt-Atmosphäre

- **Genre:** Dark Romantasy, Buch 1 von „Der Riss"
- **Technikzeitalter:** frühes 19. Jahrhundert — Kutschen, Gaslampen, Schreibmaschinen,
  Dampfschiffe. **Kein elektrisches Licht.**
- **Region:** Hafenstadt an der Grauküste (Nordküste Thalassiens, ~51. Breitengrad)
- **Bevölkerung:** ~70.000
- **Klima:** ~190 Nebeltage/Jahr, schwerer reglos liegender Nebel; aktuell Blütenmond (Mai-äquivalent)
- **Baustoff:** Purpurstein — dunkel, fast schwarz-violett, speichert Restwärme
- **Charakter:** gotisch, feucht, eng, düster-elegant; Kanäle und Gassen ziehen sich
  durch die Stadt; Geruch von Salz, Rauch, Teer, im Frühling Geißblatt

---

## 2. Karten-Geometrie (aus JSON)

### Orientierung

- **Norden = oben** (Landseite, Inland)
- **Süden = unten** (Meer, die Grauküste / Nordmeer Thalassiens)
- **Küstenlinie:** durchgängige Linie West→Ost, zwei Haupt-Einbuchtungen
  - Kleine Westbucht bei x≈370 (Tidemoor-Ufer)
  - Große zentrale Bucht bei x≈580–820 (Hafenbecken + Grauwe-Mündung)
- **Grauwe (Fluss):** kommt aus dem Nordost-Inland, schlängelt sich durch die Stadt,
  mündet im Süden bei der tiefsten Küsteneinbuchtung (ungefähr Bildmitte leicht links)

### Höhenschichten

1. **Oberstadt (Klippenplateau)** — nördliche Hälfte, hoch gelegen. Purpurstein-Fassaden,
   Verwaltung, Wohlhabende, Handelshäuser, Marktplatz, Rathaus, Druckerei, Botanischer Garten.
2. **Klippenkante** — horizontaler Absatz zwischen y=355 und y=395. Steiler Abhang, nur
   über die **Oberstadt-Treppe** zu passieren (und ein paar schmalere Gassen).
3. **Unterstadt (Hafenebene)** — südliche Hälfte, tief gelegen. Werften, Speicher, Fischer-Quartier,
   Gasthäuser, Kai-Promenade. Feuchter, dichter, lauter.
4. **Grauwe / Meer** — Wasser überall südlich der Küstenlinie; Fluss durchschneidet die Stadt.

---

## 3. Register aller Locations (15 Orte)

Format: **Name** (id) — Koordinaten — Quartier/Höhe — Kapitel — Rahmen/Rolle

### Oberstadt (hoch, Purpurstein-Blöcke, breitere Straßen)

1. **Botanischer Garten** (`botanischer_garten`) — (820, 260) — Oberstadt-Ostrand —
   K1/K5/K12/K13/K15/K17/K19/K22
   - Vier Jahrhunderte alt, grünes Haupttor, Purpurstein-Mauer rund um das Gelände
   - Kastanie, Hortensien, Farnkolonie, Treibhäuser, Komposthaufen, Wegenetz
   - Gärtner Henrik; am Ostrand oberhalb der Klippe
2. **Steinkreis** (`steinkreis`) — (830, 240) — Oberstadt, im Gartengelände —
   K12/K15/K17/K19
   - Sieben Purpursteine hüfthoch auf kleinem Hügel in der nordwestlichen Gartenhälfte
   - Kahlboden in der Mitte, Puls im 4:33-Takt, **Riss-Quelle** darunter, Portal öffnet hier
3. **Handelshaus** (`handelshaus`) — (740, 285) — Oberstadt —
   K13/K20
   - **Direkt neben dem Botanischen Garten** (westlich, wenige Minuten entfernt)
   - Großer Purpursteinbau, Hauptbezugspunkt in Stadtkarten, kein Sakralbau
4. **Rathaus / Archiv** (`rathaus`) — (530, 260) — Oberstadt-Zentrum —
   K5/K21/K22
   - Am Kanalplatz (Marktplatz), Registerbücher im Keller
   - Archivarinnen Esther und Jara Voss
5. **Marktplatz / Kanalplatz** (`marktplatz`) — (500, 290) — Oberstadt-Zentrum —
   K1/K5/K15
   - Zentraler Platz, Fischstände, Graukorn, Gewürze, Fischhändlerin
   - Rathaus unmittelbar angrenzend, Druckerei westlich
6. **Druckerei Kvist** (`druckerei_kvist`) — (380, 220) — Oberstadt-Nordwest —
   K1/K2
   - Drei Stockwerke, Dach-Wetterfahne (eiserne Hand, zeigt immer nach Norden)
   - Runa Kvist; Tinte, Handelsregister, Flugblätter
7. **Nordtor** (`stadttor_nord`) — (460, 135) — Oberstadt-Nordkante —
   K1/K3
   - Landseitiger Zugang zur Stadt, Kutschen aus Velde und Karst kommen hier an

### Übergang (Klippe + Treppen + Brücke)

8. **Oberstadt-Treppe** (`oberstadt_treppe`) — (560, 410) — Übergang zwischen Ober-/Unterstadt
   - Lange Purpurstein-Treppe, Haupt-Verbindung hoch/runter, 10–15 Minuten bergauf
9. **Grauwe-Brücke** (`grauwe_bruecke`) — (690, 430) — Übergang, überspannt die Grauwe —
   K4/K20
   - Einzige Brücke im Stadtbereich; Wasser messbar rückwärts-strömend ab K20
10. **Der Anker** (`anker`) — (590, 460) — Übergang, Fuß der Oberstadt-Treppe —
    K4/K8/K12–K22 (zentraler Treffpunkt)
    - Gasthaus mit schmiedeeisernem Anker an Kette über niedriger Tür
    - Schankraum mit Eichen-Dielen und alter Kohle-Feuerstelle; hinten ein Nebenraum mit
      schmalem Fenster zur Grauwe (Vespers Reparaturtisch)
    - Zimmer im Obergeschoss für Alphina, Sorel, Maren, Vesper

### Unterstadt (niedrig, Hafenebene, enge Gassen)

11. **Lichthaus** (`lichthaus`) — (670, 555) — Unterstadt, am Kai —
    K2/K10/K13/K21/K22
    - Speicherbau, fensterloses Purpurstein-Mauerwerk
    - Schmale Kellertür mit Efeu überwachsen, darunter Sorels Dunkelkammer (Rotlicht, Pyrogallol)
12. **Hafen / Kai / Stege** (`hafen_kai`) — (610, 600) — Unterstadt, am Wasser —
    K2/K4/K15/K19/K20
    - Kaimauer aus dunklem Stein, mehrere Stege (2., 3., 4. Steg)
    - Pollerbaum, Netzflicker, Salzkessel; Fischer Tohl sieht dort Wesen auf Pollern
13. **Werft Dahl** (`werft_dahl`) — (720, 570) — Unterstadt, **am Grauwe-Ostufer kurz vor der Mündung** —
    K4/K8/K14/K20/K21/K22
    - Grauer Holzschuppen, verwittertes Brett, Salzwind
    - Halbfertiges Boot auf Böcken, Werkzeuge, Schiffsuhr
    - Gegründet TZ 151 von Lene Dahl; Maren Ilves erbt
14. **Tidemoor-Haus** (`tidemoor_haus`) — (380, 540) — Unterstadt, Grauwe-Westufer —
    K15/K18/K19
    - Wohnhaus am Fluss; Standuhr im Salon verliert 4:33 Sek/Stunde (Portal-Frequenz)

### Straße als Referenzpunkt

15. **Hafengasse** (`hafengasse`) — Marker (720, 490) — Hauptader der Unterstadt

---

## 4. Straßen & kürzeste Wege (menschliche Bewegungslogik)

**Grundprinzip:** Figuren wählen immer den kürzest möglichen Weg, der nicht
durch Wasser oder über die Klippe führt. Der Kartograph zeichnet Straßen entsprechend.

### Fünf kanonische Routen aus `streets`

1. **Hafengasse** — Ader der Unterstadt, West→Ost am Kai entlang
   - Pfad: Tidemoor-Haus (380, 540) → Anker-Fuß (570, 570) → Lichthaus (670, 555) →
     **über Werft-Brücke** → Werft Dahl (720, 570)
   - Im Terrain: folgt flach dem Meerufer/Grauwe-Westufer, biegt am Anker nach Osten,
     überquert am südlichsten Punkt die Grauwe-Mündung (Kai-Brücke oder Fähre)
2. **Böttchergasse** — Hoch zur Oberstadt
   - Pfad: Anker (590, 460) → bergauf → Marktplatz (500, 290)
   - Vermutlich eine enge Gasse mit Treppen (die Haupt-Treppe ist separat)
3. **Obere Gasse** — Ader der Oberstadt, West→Ost
   - Pfad: Druckerei Kvist (380, 220) → Marktplatz (500, 290) → Handelshaus (740, 285) →
     Botanischer Garten (820, 260)
4. **Werftweg** — Zur Werft via Grauwe-Brücke
   - Pfad: Anker (590, 460) → Grauwe-Brücke (690, 430)-Region → Ostufer → Werft (720, 570)
5. **Gartenweg** — Oberstadt-Pfad durchs Villenviertel
   - Pfad: Anker (590, 460) → Oberstadt-Treppe → am Handelshaus vorbei → Botanischer Garten

### Implizite Logik für den Bildgenerator

- **Kürzeste Wege:** Alle stark genutzten Verbindungen (Anker ↔ Garten, Werft ↔ Anker, Hafen ↔ Markt)
  sollten erkennbar geradlinig sein. Umwege nur wo Topographie (Klippe, Fluss) zwingt.
- **Klippen-Barriere:** Vom Anker zur Oberstadt gibt es **nur drei** praktikable Aufstiege:
  Oberstadt-Treppe, Böttchergasse, Gartenweg (über den bewachsenen Hang).
- **Fluss-Barriere:** Grauwe trennt Ost- von West-Unterstadt. **Eine Hauptbrücke**
  (Grauwe-Brücke bei 690,430) im Norden plus **kleinere Querungen** am Kai möglich.
- **Gassen-Netz:** Zwischen den großen Straßen ist es ein enges, unregelmäßiges Geflecht
  (Stadt ist mittelalterlich gewachsen, nicht geplant).

### Distanzen (Minuten zu Fuß)

- Hafen → Botanischer Garten: 25 min (bergauf)
- Werft → Anker: 8 min (Hafengasse)
- Anker → Marktplatz: 15 min (Böttchergasse hoch)
- Anker → Lichthaus: 5 min (Hafengasse hinab)
- Anker → Botanischer Garten: 20 min (Gartenweg hoch)
- Unterstadt ↔ Oberstadt (nur Treppe): 12 min

---

## 5. Rahmenbedingungen für den Bildgenerator

**Darstellungsart:**
- **Top-down view** (Vogelperspektive) — klassische Fantasy-Stadtkarte
- **Alter Manuskript-Look** — Sepia, verwittertes Pergament ODER dunkler Schiefer mit goldenen Linien
- **Handgezeichnet** — feine Tuschelinien, leicht ungenaue Geometrie, keine Computergrafik-Klarheit
- **Labels in eleganter Serif-Schrift** (Blackletter vermeiden, eher altdeutsch-klassizistisch)

**Visuelle Hierarchie:**
- Küstenlinie + Grauwe: dunkelblau-grau, stärkste Konturlinie
- Klippenkante: sichtbare Schraffur/Ticks nach Unterstadt-Seite
- Ober-/Unterstadt: leichte Patina-Unterschiede (Oberstadt heller Purpur, Unterstadt feuchter, mooriger)
- Gebäude: nur die 15 gelisteten Orte als eigene Icons mit Label
- Gassen: dünnes Netz, aber die 5 Hauptstraßen deutlich hervorgehoben

**Atmosphäre:**
- Nebelschwaden über der Grauwe-Mündung und dem Hafen
- Subtile Purpurstein-Tönung in den Oberstadt-Gebäuden
- Nordtor dominant am nördlichen Bildrand
- Kein maschineller Schmutz (frühes 19. Jhd, vor Industriezeit)

**Was NICHT dargestellt werden soll:**
- Keine Stadtmauern (Vael hat keine Mauern in den Kapiteln)
- Keine Kathedralen/Burgen (keine monumentalen Sakral- oder Herrschaftsbauten)
- Keine Straßenbeleuchtung/Gaslampen in der Darstellung (sie existieren, sind aber auf einer Karte nicht relevant)
- Keine Fraktionsfarben, Wappen, Heraldik

---

## 6. Finaler Prompt-Block (copy-paste in Bildgenerator)

```
A hand-drawn top-down fantasy city map titled "Vael", styled as an aged 19th-century
cartographer's manuscript. Dark-romantic mood, weathered sepia paper with charcoal
ink linework, subtle purple-black tint in stone structures.

CITY LAYOUT: A coastal port city on the northern "Grauküste" of the Thalassien continent.
Sea to the south (bottom of frame). Land extends to the north (top). One continuous
coastline running west-to-east across the lower third of the map, with two bays:
a small western bay at ~30% width, and a large central harbor bay at 50-70% width
where a slow brackish river named "Grauwe" empties into the sea from the northeast.

TWO TERRAIN LEVELS separated by a horizontal cliff edge:
- UPPER TOWN (upper half): cliff-top plateau, orderly purple-black purpurstein buildings,
  wider streets, marketplace and administrative quarter
- LOWER TOWN (between cliff and coast): foggy harbor flat, warehouses, shipyards,
  narrow crooked alleys, fishing quays

PROMINENT LABELED LOCATIONS (place as described):
- Botanischer Garten — far east of upper town, walled garden with stone circle inside
- Steinkreis — seven standing purpurstones within the garden, on a small rise
- Handelshaus — large purpurstein building immediately west of the garden
- Rathaus / Archiv — upper town center, next to marketplace
- Marktplatz (Kanalplatz) — central plaza
- Druckerei Kvist — upper town northwest, three-story building with iron-hand weathervane
- Nordtor — northern land gate, top center of map
- Oberstadt-Treppe — long stone staircase cutting through the cliff
- Grauwe-Brücke — single stone bridge over the Grauwe river
- Der Anker — inn at the base of the staircase, transitional location
- Lichthaus — warehouse on the quay, shadowed
- Hafen / Kai / Stege — harbor with multiple piers and bollards
- Werft Dahl — shipyard directly on the east bank of the Grauwe river near its mouth
- Tidemoor-Haus — residence on the west bank of the Grauwe
- Hafengasse — main harbor-side street running along the quay

ROADS: Draw five visible main streets reflecting how people walk shortest paths:
1. Hafengasse — along the lower quay west-to-east
2. Böttchergasse — climbing from the Anker inn up to the marketplace
3. Obere Gasse — across upper town, Druckerei → Markt → Handelshaus → Botanischer Garten
4. Werftweg — from the Anker over the Grauwe bridge down to the shipyard
5. Gartenweg — from the Anker climbing directly to the Botanischer Garten

Between the main streets: a dense irregular network of narrow medieval alleys.

NO city walls. NO cathedrals. NO monumental castles. NO ornate heraldry.
One single bridge across the Grauwe inside the city. Faint mist trailing off the
river mouth and the open harbor. Small period-appropriate detail: a few tiny sailing
ships in the harbor, stacked fish barrels, a coach at the Nordtor.

Labels in elegant neoclassical serif, NOT blackletter. Compass rose top-right.
Simple scale bar bottom-left showing "0–500 m".
Overall palette: aged parchment cream, charcoal ink, muted purple-black stone,
desaturated sea teal.
```

---

## 7. Feinjustierungs-Anmerkungen (für Re-Prompt bei unbefriedigendem Ergebnis)

- Falls der Generator **Mauern** malt: erneut „NO city walls" betonen, „open harbor city"
- Falls **Turmspitzen/Kathedralen** erscheinen: „no religious monuments, no spires"
- Falls die **Küste zum Rund-Polygon** wird: „coastline as a continuous west-to-east line,
  open sea only at the bottom of the map"
- Falls der **Fluss fehlt**: „the Grauwe river must flow visibly from top-right to the
  central bay"
- Falls **zu modern**: „pre-industrial, early 1800s look, no factories, no machinery"
- Falls die **Straßen zu rechtwinklig**: „organic medieval street network, curves
  following the terrain"
