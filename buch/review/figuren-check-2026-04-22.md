# Figuren-Check — Buch 1 (22./23. April 2026)

**Erzeugt durch:** 8 parallele Explore-Agenten (`/figuren-check alle`)
**Scope:** Alle finalen Kapitel (K1–K22, I1–I3), Entwürfe K23–K25, Aktpläne Akt 3+4, Welt-Bibel, Magie-Canon, Positioning, Memory-Canons.
**Status nach:** Kalender-Canon (OLD wiederhergestellt) + Schemen-Canon (offene Intelligenz-Frage) + Aktplan/Szenenplan-Cleanup vom 22. April.

## Übersicht (Stand nach Verifikation 23. Apr)

| Schwere | Gesamt | Gelöst durch Canon/Autor | Gefixt | Fehlalarm | Offen |
|---|---|---|---|---|---|
| Kritisch (A) | 8 | 7 (A2, A3, A4, A5, A6, A7, A8) | 0 | 1 (A1) | 0 |
| Mittel (B) | 18 | 2 | 1 (B17) | 2 (B3, B10) | 13 |
| Klein (C) | ~12 | 1 | 0 | 1 (C3) | 10 |
| **Summe** | **~38** | **10** | **1** | **4** | **23** |

**Alle A-Findings abgearbeitet.** 23 offene Findings verteilt auf B (13) und C (10) — alle Plot-/Prosa-Entscheidungen ohne kritische Konsistenzverletzung.

## Verifikations-Lektion (23. Apr)

**4 von 5 verifizierten Befunden waren Fehlalarme** (B17 war der einzige echte Fund):
- A1 "K15-Dunkelkammer-Rückblick" → Agent hat Zitat halluziniert
- B3 "Dom-Ton Behalte diesen Schlag" → Uhrmacherischer Fachbegriff missverstanden
- B10 "Halvard-Namenskonflikt" → Drei Figuren über 1500 TZ-Jahre verteilt
- C3 "wächsern = Alphina-Vokabular" → Allgemeinsprache

**Konsequenz für `/figuren-check`:** Agenten-Befunde **immer verifizieren** bevor gefixt wird. Hohe False-Positive-Rate bei Stil-Register- und Wissen-Behauptungen — der Agent sieht das Zitat im Kontext des Prompts und kann eigene Projektionen machen. **Jeder gemeldete Textbefund muss mit Grep oder Read gegengeprüft werden.**

## Root-Cause-Cluster

Drei Canon-Infrastruktur-Entscheidungen lösen zusammen viele Folge-Findings:

1. **Kalender-Mathematik** → A2, B12, teilweise Harons Zeitleiste (A6). **Erledigt** 22. Apr.
2. **Schemen-Typologie** → A4, B14. **Erledigt** 22. Apr.
3. **Varen-Biografie** (Alter in MZ, Signatur-Frequenz 4:33, Plan-Motivation) → A3, A5, A8. **Teilweise erledigt** (A3) durch MZ-Kalender; A5/A8 bleiben Plot-Entscheidung.

---

## A. KRITISCH

### A1 · Alphina · Rückblick K15 auf K21 (Temporaler Anachronismus)
- **Status:** ❌ **Fehlalarm — verifiziert 23. Apr**
- **Ergebnis der Textprüfung:** In `B1-K15-alphina.md` gibt es KEINEN Dunkelkammer-Rückblick. Sorel steht in K15 am Steg und fotografiert (erste Wiederbegegnung nach K12). Das vom Agenten zitierte "Gestern Abend lag die Dunkelkammer hinter ihnen…" ist nicht im Text. Agent hat halluziniert oder aus einem Entwurf-Fragment zitiert.

### A2 · Alle · Kalender/Monatslängen nicht dokumentiert
- **Befund:** Unterschiedliche Agenten rechneten mit verschiedenen Monatslängen; Wochen-Rechnungen waren nicht verifizierbar.
- **Status:** ✅ **Gelöst** 22. Apr — TZ-Canon ist Gregorianisch + thalass. Namen (`buch/00-zeitrechnung.md`). MZ = 8×36×26h. Tool `scripts/zeitrechnung.py`.

### A3 · Varen · Altersparadox (Mitte 40 vs. "400 Jährlein")
- **Befund:** `19-varen.md` sagt Mitte-Ende 40; K37-Plan "Über vierhundert Jährlein erspüret".
- **Status:** ✅ **Gelöst** 22. Apr — Varen ist Mitte 40 in MZ-Jahren. 1 MZ-Jahr = 400 TZ-Jahre. "400 Jährlein" = TZ-gerechnet 1 MZ-Jahr = Zeit seit Elke (I3 = MZ 3634, B1 = MZ 3635). Canon-konsistent.

### A4 · Varen · Schemen-Motivation persönlich vs. atmosphärisch
- **Befund:** `00-storyline.md` sagt Experiment-Aussendung; K37-Plan dramatisiert als persönlich gezielt.
- **Status:** ✅ **Gelöst** 22. Apr — Schemen-Canon (Beschwörer bestimmt Form+Zweck; Intelligenz-Frage offen auch für Moragher). Beides Canon-zulässig: Varen kann gezielt schicken, gleichzeitig ist das Verhalten der Schemen drüben nicht vollständig deterministisch.

### A5 · Varen · 4:33-Signatur (natürlich vs. künstlich)
- **Status:** ✅ **Gelöst 23. Apr** — Canon: 4:33 ist die **Eigenfrequenz der Vaeler Quelle** (= 273 s = 7 Purpursteine × 39-s-Grundschwingung). Baseline seit Generationen in der Tidemoor-Uhr (Purpurstein-Ausläufer amplifiziert lokal; Uhr auf normalem Fels würde weniger driften). Varen nutzt die natürlichen Resonanz-Fenster, erzeugt sie nicht. "SEIN Atem" in K37 wird als Rhythmus IM Takt der Quelle neu formuliert.
- **Files aktualisiert:** `10-magie-system.md` (neuer Abschnitt "Grundfrequenz der Quellen"), `04-akt3.md` (K33-Prosa-Plan), `05-akt4.md` (K37-Plan-Satz).

### A6 · Haron · Drei widersprüchliche Zeitpunkte
- **Status:** ✅ **Gelöst 23. Apr** — Canon: Haron stirbt mit ~70 (nicht 85). Neue Chronologie: Geburt ~TZ 480, Portal-Durchgang + Zuzug Vael TZ 514 (Alter 34, Thalassisch bereits in Moragh gelernt), 30 Jahre Werftlehre/Gesellen-Arbeit, Adoption TZ 544 (Alter 64), Briefe an Maren ab TZ 546, Tod ~TZ 550.
- **Files aktualisiert:** `nebenfiguren/haron-dahl.md` (Chronologie-Tabelle ergänzt, "Über 80" → "~70", "~66 Jahre" → "~37 Jahre").

### A7 · Runa · K9 Halvard-Zugang + Uhrmacher-Zahlen unplausibel
- **Status:** ✅ **Gelöst 23. Apr** — Autor-Entscheidung:
  1. **Halvard-Zugang:** Runa lebt seit Längerem in Vael, darf dort Menschen kennen. Kein Setup nötig.
  2. **Patientengeheimnisse:** implizit über Vertrauens-Beziehung zu Runa, nicht zu fixen.
  3. **Uhrmacher-Zahlen:** Magd hat die 4:33 aus dem Haushalt mitbekommen (Vesper sprach sie laut vor Herrn Tidemoor aus, dienstbotische Kettenweitergabe ist alltagsplausibel). K7-Text bleibt unverändert.
- **Text-Prüfung K7:** Magd ist nicht im Raum beim expliziten Aussprechen, aber als Hausangestellte plausibel durch Gespräche der Herrschaft informiert. Nicht forensisch wasserdicht, aber akzeptabel.

### A8 · Varen + Elke · I3 endet ohne Varen-Empfang
- **Status:** ✅ **Gelöst 23. Apr** — Canon: **Finaler I3-Text ist führend.** Elke kommt allein auf Moragh-Boden an. Kespers Tod unterwegs (Riss schloss einen Atemzug zu kurz). Vael-Feuer-Wesen verblasst aus eigener Kraft nach Stunden, weil Portal zu und Bindung durch Welten-Trennung zu schwach für aktives Kappen. Varens Empfang erfolgt off-page zwischen I3 und B1.
- **Files aktualisiert:** `00-welt.md` (Canon-Memo Portal-Übertritt umformuliert), `10-magie-system.md` (Bindungs-Regel "Portal geschlossen → Bindung erlischt praktisch" ergänzt), `_archiv/02-akt1.md` (Aktplan-I3-Sektion angepasst).

---

## B. MITTEL

### B1 · Runa · Präsenz in K19 (Kampf im Garten) unklar
- **Befund:** Welt-Canon sagt "Runa schlüpft mit durch" (K36); K19-Text/Aktplan nennt sie nicht.
- **Status:** ◻ **Offen** — Plot-Entscheidung: dabei oder nicht?

### B2 · Vesper · K11 Oberstadt-Geografie ohne Ortsbesuch
- **Befund:** Vesper kennt in K11 den Botanischen Garten genau genug, um dessen Position auf selbst gezeichneter Karte zu markieren — obwohl er nie in der Oberstadt war.
- **Status:** ◻ **Offen** — Prosa-Fix: Mittelpunkt-Ermittlung via Runas Flugblatt-Adressen, nicht aus eigener Kartografie.

### B3 · Vesper · K11 Dom-Ton gegen Alphina ("Schlag")
- **Status:** ❌ **Fehlalarm — verifiziert 23. Apr**
- **Ergebnis:** "Behalte diesen Schlag" ist Vespers rückblickende Erzählung an Alphina über einen internen uhrmacherischen Moment. "Schlag" = Halbschwung-Frequenz einer Ankerhemmung (2 Halbschwünge/Sekunde = Fachbegriff). "Behalte" ist an das Uhrwerk gerichtet, nicht an Alphina. Kein Dom-Register, kein BDSM-Bezug.

### B4 · Vesper · K18 Marens Magie-Beschreibung zu vage
- **Befund:** "Sie hat gezeigt, wie sie einen Strudel in eine Tasse Tee bringt, ohne sie anzufassen" — "sie" mehrdeutig (Becher? Wasser?).
- **Status:** ◻ **Offen** — Formulierungs-Fix.

### B5 · Maren · Magie-Wendepunkt K8→K17 fehlt
- **Befund:** K8 Maren leugnet aktiv ("waren die Gezeiten"); K17 sie weiß es; K20 sie benennt es stumm. Der innere Kippmoment fehlt.
- **Status:** ◻ **Offen** — Innerer Beat in K8-Ende oder K17-Anfang.

### B6 · Maren · K4 Haron-Adoption nicht vorbereitet
- **Befund:** K4 Edric sagt "Dahl heißt die Werft. Den Namen übernimmt man, wenn man bleibt." K20 offenbart Adoption — dazwischen keine Einordnung.
- **Status:** ◻ **Offen** — Edric-Dialog in K4 erweitern.

### B7 · Jara · Motivation springt K20 → K24
- **Befund:** K20 passive Archivarin; K24 aktive Forscherin mit neuen Funden ohne Setup.
- **Status:** ◻ **Offen** — Setup-Satz in K20-Ende oder K24-Eröffnung.

### B8 · Esther · "Weiß mehr" bleibt unaufgelöst
- **Befund:** Esther reagiert kontrolliert und informiert in K20/K24, ohne Klärung. Wenn in Buch 1 nicht gelöst, braucht es einen expliziten Marker.
- **Status:** ◻ **Offen** — 1-Satz-Marker.

### B9 · Magd Tidemoor · Verschwindet K7 → K11
- **Befund:** K7 zentrale Ansprechperson; K11 fehlt sie unerklärt.
- **Status:** ◻ **Offen** — 1-Satz-Erklärung oder Nicht-Erwähnen.

### B10 · Halvard · Namenskonflikt mit Familie-Halvard
- **Status:** ❌ **Fehlalarm — verifiziert 23. Apr**
- **Ergebnis:** Drei Figuren mit Nachname Halvard, aber klar getrennt durch Zeit und Buch:
  - **Dr. Halvard** (Arzt Vael, Buch 1, TZ 551) — Nebenfigur in K9
  - **Tyra Halvard** (Linguistin Expedition 1, Buch 3, TZ 2020+) — Marens Ur-Großtante
  - **Dr. Syra Halvard** (Institutsleiterin Buch 3, TZ 2110–2152) — Tyras Ur-Großnichte (Seitenlinie)
  - Zwischen Buch 1 und Buch 3 liegen ~1500 TZ-Jahre; keine Verwechslung möglich.

### B11 · Maren · K20 verbindet Haron-Akzent (K4) nicht rückwirkend
- **Befund:** Edrics K4-Satz "Akzent, Woanders her" bleibt in K20 ungenutzt, obwohl Maren liest "verfügte über Landessprache nur eingeschränkt".
- **Status:** ◻ **Offen** — 1 Erinnerungssatz in K20.

### B12 · Elke · I1-I2 "6 Wochen"-Angabe stimmig?
- **Status:** ✅ **Gelöst** — Gregorianisch: 1. Oktober → 15. November = 45 Tage = 6 Wochen 3 Tage. Passt.

### B13 · Elke · Kespers Hafenbild vs. K24-Manuskript
- **Befund:** I3 zeigt Kesper gibt Lene sein Bild für das Manuskript. K24 zeigt Lenes Manuskript mit Feuer-Wesen-Zeichnung — Kespers Hafenbild fehlt.
- **Status:** ◻ **Offen** — entweder K24 beide Zeichnungen oder I3-Text entschärfen.

### B14 · Elke · Schemen-Eskalation I1→I2→I3 (Typen konsistent?)
- **Befund:** I1 tierhafte kleine Schemen, I3 mannshohe Feuer-Wesen. Unterschiedliche Arten?
- **Status:** ✅ **Gelöst** 22. Apr — Schemen-Canon erlaubt Form-Variabilität durch Beschwörer.

### B15 · Varen · K26-Prosa als Tschechow-Basis für K37 fehlt
- **Befund:** K37-Plan referenziert K26-Schem-Geste; K26 existiert nur als Entwurf.
- **Status:** ◻ **Offen** — K26 ausarbeiten.

### B16 · Varen · K21-Schem Hand-an-Kinn-Geste nicht vorbereitet
- **Befund:** K37-Plan sagt "dieselbe Geste wie der Schem im Lichthaus-Keller (K21)". K21-Text hat andere Schem-Haltung.
- **Status:** ◻ **Offen** — K21-Prosa erweitern ODER K37-Plan anpassen.

### B17 · Maren · K8 "Jackentaschen" ×2 (Kleidungs-Canon)
- **Status:** ✅ **Gefixt 23. Apr** — Beide Treffer in `08-maren.md` von "Jackentaschen" auf "Manteltaschen" geändert.

### B18 · Runa · K25 Zeitspanne Szene 1 → Szene 2 unklar
- **Status:** ◻ **Offen** — 1 Zeitmarker im Szene-2-Eröffnungs-Beat.

---

## C. KLEIN (Auswahl)

| ID | Figur | Kurz | Status |
|---|---|---|---|
| C1 | Sorel | K6 Falkensand-Kassette nicht explizit eingepackt | ◻ offen |
| C2 | Maren | K8 Tohl kennt sie ohne Setup | ◻ offen |
| C3 | Maren | K22 "wächsern" (Alphina-Vokabular) | ❌ Fehlalarm — Allgemeinsprache, kein Fach-Vokabular. Maren arbeitet mit Wachs. |
| C4 | Runa | K5 Kerze-Beobachtung nicht weitergeführt bis K25 | ◻ offen |
| C5 | Elke | I3 "zwei Monde" nicht explizit in Prosa | ◻ offen |
| C6 | Sorel | Bart-Canon, Chemie-Geruch in Nähe — in finaler Prosa eingehalten | ✅ gelöst |
| C7 | Alphina | K15 Halvard-Daten-Verbindung fehlt intern | ◻ offen |
| C8 | Runa | Herkunft/Familie in Buch 1 nicht etabliert (Absicht?) | ◻ offen |

---

## Priorisierte Empfehlung

**Sofort (Text-Fixes, ~30 Min gesamt):**
1. B17 Jackentaschen → Manteltaschen
2. B3 "Schlag" → "Takt"
3. C3 "wächsern" → "ölige Oberfläche"

**Verifikation zuerst (~15 Min):**
4. A1 K15-Text gegen K21 lesen — ist der Rückblick wirklich drin?
5. B10 Halvard-Namen grep — kollidieren sie?

**Canon-Entscheidung nötig (je 15–30 Min mit Autor):**
6. A5 4:33: natürlich oder Varens Atem?
7. A6 Haron-Zeitleiste konsolidieren
8. A8 I3-Schluss: Varen-Moment ergänzen?
9. B1 K19 Runa dabei?

**Prosa-Ergänzungen (je 30–60 Min):**
10. A7 Runa-Halvard-Vorkontakt (K5 oder K9)
11. B2 Vesper-Geografie via Flugblatt
12. B5 Marens Magie-Kippmoment
13. B6 Haron-Adoption in K4 vorbereiten
14. B15 K26 ausarbeiten (eigener Kapitel-Entwurf-Lauf)
15. B16 K21 Schem-Geste setzen oder K37 anpassen

## Reproduktion

```
/figuren-check alle
```

Startet denselben Lauf. Findings landen als `buch/review/figuren-check-{JJJJ-MM-TT}.md`.
