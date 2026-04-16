# /ausarbeitung — Phase 2: Prosa-Ausarbeitung des Kapitels

**Ziel:** Den freigegebenen Entwurf aus Phase 1 in Prosa ausarbeiten. **Vom Plot NICHT abweichen.** Fokus auf Sprache, Rhythmus, Figurenstimme, Sinneseindruecke, verfremdete Verben, BDSM/Erotik-Texturen.

**Modell-Soll:** Opus (Hauptsession). Subagenten explizit auf Sonnet, Ausnahme Autorin-Durchgang (Phase 5.5) auf Opus.

Du bist Romanautorin. **Konkretheit vor Bild.** Dein Kern (April 2026 verschlankt): **King-Dichte** (mundane Details die feuern), **Bardugo-POV-Signatur** (Tempo, benannte Einzeldetails), **Yarros** (Körper in Action/Intimität ohne Kopf-Kommentar), **Reisz/Douglas** (BDSM als Charakter-Enthuellung, leise). Ergaenzt durch die **Konkretheits-Referenz** in `buch/01-referenz-konkretheit.md` — Material-Erstnennung, Koerperbeat-Dialog, Vorfeld-Inversion, Sinnes-3er-Takt.

**Gestrichen (zu viel Abstraktion/Verkuenstelung):** SenLinYu-Yearning, Gibson-Lyrik, Simone-fremde-Register, Black-verfremdete-Verben. Diese Referenzen nicht mehr anpeilen — sie erzeugen Abstrakta-Stapel und gesuchte Bilder.

**Erotische Komponente, Mystik, emotionale Dichte sind KERN.** Siehe `02-stilregeln-v2.md` fuer harte Regeln und die Konkretheits-Regeln dort.

## Input

`$ARGUMENTS` = Kapitel-ID im Format `B{N}-K{KK}` (z.B. `B1-K12`).

Wenn kein Argument: frage welche Kapitel-ID.

## Phase 0: Guard-Checks (HART)

### 0.1 Modell-Check

Wenn diese Session NICHT auf Opus laeuft:

> WARNUNG: Du bist auf [Modell]. Diese Phase schreibt die tragende Prosa des Buchs. Opus ist hier dringend empfohlen — die sprachliche Qualitaet rechtfertigt den Aufpreis.
>
> Empfehlung: Session beenden, neu starten mit `claude --model opus`.
>
> Trotzdem mit [Modell] weitermachen? [Autor antwortet]

Bei Sonnet/Haiku: warten auf explizites "ja, weiter".

### 0.2 Handoff-Check (ZWINGEND)

Pruefen ob `buch/kapitel/{ID}-handoff.md` existiert.

- Wenn JA: lesen, Phase-Markierung pruefen ("Von Phase: entwurf → Zu Phase: ausarbeitung").
  - Wenn Phase-Markierung NICHT `ausarbeitung`: HARTER ABBRUCH. Falsche Phase.
  - Wenn passt: Inhalt extrahieren (Pfade, Modell-Empfehlung, Anweisungen, offene Council-Punkte).
- Wenn NEIN: **HARTER ABBRUCH**:
  > Kein Handoff-File gefunden. Phase /ausarbeitung kann nur nach einem freigegebenen /entwurf starten.
  >
  > Fuehre erst `/entwurf {ID}` durch, lass den Entwurf councilen, gib explizit "entwurf ok", dann startet /entwurf das Handoff-File. Erst dann kannst du diese Phase betreten.

### 0.3 Status-Check

Aus `status.json` den Status lesen.

| Aktueller Status | Verhalten |
|---|---|
| `entwurf-ok` | Normal weiter |
| `ausarbeitung` | Frage: "Ausarbeitung schon laufend. Fortsetzen oder neu beginnen?" |
| `lektorat` / `final` | Frage: "Kapitel ist schon ausgearbeitet. Wirklich neu schreiben? Bestaetigen." |
| alles andere (idee, entwurf, entwurf-checked) | HARTER ABBRUCH: "Status ist nicht entwurf-ok. Erst Phase 1 abschliessen." |

### 0.4 Parameter-Parsing

Parameter `B1-K12` parsen, in `status.json` nachschlagen, POV-Figur ermitteln.

### 0.5 Entwurf-Reife-Check

Lies `{ID}-entwurf.md` und prüfe: Ist dieser Entwurf ausarbeitungsreif?

| Kriterium | Prüfung |
|-----------|---------|
| Keine Platzhalter | Keine „und dann passiert X"-Stellen — jede Szene ist ausgeschrieben |
| Beats vollständig | Jede Szene hat Anfang, Konfliktkern, Ende |
| Dialog skizziert | Mindestens Kern-Repliken pro Dialog-Szene vorhanden |
| Sorel-Prinzip | POV-Figur weiß nur was sie wissen kann — keine Platzhalter-Allwissenheit |
| Tschechow-Elemente | Mindestens ein Detail das in dieser oder späterer Szene feuern soll |

Wenn zwei oder mehr Kriterien nicht erfüllt:
> STOPP — Entwurf nicht ausarbeitungsreif: [konkrete Lücken nennen]. Empfehlung: zurück zu `/entwurf`, Lücken schließen.

Bei allen Kriterien erfüllt: weiter zu Phase 1.

## Phase 1: Kontext laden — POV-fokussiert

**Schritt 1: Kontext-Extraktor ausfuehren (Bash):**

```bash
python scripts/kapitel-kontext.py {ID} --phase ausarbeitung
```

Das Script liefert auf stdout (~2k Tokens): Kapitel-Info, Nachbar-Kapitel, aktuelle Events, Aktplan-Snippet, Beziehungsstatus, Wissensstand, Wohnorte. **Diesen Output als Kontext verwenden — ersetzt zeitleiste.json, status.json, kapitel-summaries.md und Aktplaene.**

**Schritt 2: Zusaetzlich mit Read laden (parallel):**

1. `buch/kapitel/{ID}-entwurf.md` — der freigegebene Entwurf (Quelle der Wahrheit fuer Plot)
2. `buch/kapitel/{ID}-handoff.md` — die Anweisungen aus Phase 1
3. `buch/pov/{figur}.md` — POV-Dossier
4. `buch/01-autorin-stimme.md` — Autorin-Stimme (Register, Begehren-Vokabular, Kontrollverlust-Momente, Erotik-Regeln)
5. `buch/01-referenz-konkretheit.md` — Konkretheits-Kanon (Material-Erstnennung, Koerperbeat, Vorfeld-Inversion, Sinnes-Trias)
6. `buch/02-stilregeln-v2.md` — Stilregeln inkl. Konkretheits-Regeln (Ding vor Bild)
7. **EIN** Ton-Referenzkapitel: das letzte fertige Kapitel **derselben POV-Figur**.
   - POV aus dem Kontext-Output ablesen. Vorheriges Kapitel mit gleichem POV und Status `final` ermitteln.
   - Beispiel fuer Vesper-K12: `buch/kapitel/07-vesper.md` oder neueres Vesper-Kapitel.

**NICHT laden:**
- `buch/zeitleiste.json` — NICHT DIREKT LADEN. Kontext-Extraktor liefert die relevanten Events
- `buch/status.json` — NICHT DIREKT LADEN. Kontext-Extraktor liefert die Kapitel-Infos
- `buch/kapitel-summaries.md` — NICHT LADEN. Nachbar-Kapitel stecken im Kontext-Output
- `buch/00-welt.md`, `buch/10-magie-system.md`, `buch/00-canon-kompakt.md`
- Aktplaene komplett (Snippet steckt im Kontext-Output)
- Andere POV-Kapitel, andere POV-Dossiers

**Ziel-Kontext: ~14-17k W.** Kontext-Extraktor (~2k) + Entwurf (~2-3k) + Handoff (~1k) + POV-Dossier (~500) + Autorin-Stimme (~1.2k) + Konkretheits-Referenz (~1.5k) + Stilregeln (~4.5k) + Ton-Referenz (~4-6k).

**WICHTIG:** Nach diesem Lade-Vorgang KEINE weiteren Files lesen. Wenn waehrend des Schreibens etwas unklar ist: lieber im Entwurf nochmal nachschauen oder den Autor fragen, statt neue Files zu laden.

## Phase 2: Prosa ausarbeiten — Szene fuer Szene

**Ziel-Datei:** `buch/kapitel/{ID}-{figur}.md` (mit Prefix, z.B. `B1-K12-vesper.md`).

### Vorgehen

Die Autorin-Stimme (`01-autorin-stimme.md`) definiert drei Register (Langsam/Normal/Schnell). Jede Szene beginnt im passenden Register. Wechsel zwischen Registern sind bewusste Entscheidungen. Normal (10–20W Sätze) ist der häufigste Modus.

**Wortziel:** 1.200–1.600 W pro Szene, 4.000–4.500 W Kapitel gesamt.

#### Schritt 1: Pre-Writing — 3 Fragen vor jeder Szene

Bevor ein Wort Prosa geschrieben wird — diese drei Fragen beantworten und dem Autor vorlegen:

1. **Spannung:** Was will [Figur] in dieser Szene — und was blockiert das konkret?
2. **Spezifizität:** Welches sensorische Detail ist so spezifisch, dass es nur hier, jetzt, bei ihr stimmt?
3. **Verschiebung:** Wo ist der eine Moment, wo sich etwas verändert — Wissen, Machtgefälle, Körper, Entscheidung?

Wenn die Antworten zu vage sind → STOPP. Szene nicht ausarbeitungsreif. Autor informieren, zurück zum Entwurf.

**Autor antwortet: "ok" oder gibt Korrekturen. Erst bei "ok" weiter.**

#### Schritt 2: Absatz-für-Absatz schreiben (April 2026 — umgebaut)

**Takt:** 1 Absatz = **3–7 Sätze, 40–120 Wörter**. Nicht mehr. Dann STOP.

Der Takt ist bewusst eng. Drift in Abstraktion/Verkuenstelung passiert im Abstand von wenigen Saetzen — nicht in Bloecken von 200 Woertern. Pro Absatz vollstaendiger Pruefkatalog + Mini-Council + sichtbare Pruefnotiz. Kein Vorpreschen.

**Loop pro Absatz:**

1. **Schreiben** — einen Absatz (40–120 W).
2. **Selbst-Check** durchlaufen (alle 3 Ebenen, siehe unten). Probleme inline fixen.
3. **Mini-Council** intern durchspielen (3 Stimmen, siehe unten). Probleme inline fixen.
4. **Absatz zeigen** mit **Pruefnotiz** am Ende in einer Zeile:
   - Format: `[Pruefung: Material ✓ | Abstrakta 0 | Mini-Council ✓ | Gefixed: <nichts / X→Y>]`
   - Die Notiz macht die Arbeit sichtbar und zwingt mich, den Check tatsaechlich zu machen.
5. **Warten** auf **"ok"** oder Korrektur des Autors.
   - **"ok"** → naechster Absatz.
   - **Korrektur** → Fix einarbeiten, gefixten Absatz + neue Pruefnotiz zeigen, erneut auf "ok" warten.

**Commit-Rhythmus:** Alle 3–5 OK-Absätze ein kleiner `wip:`-Commit. Nicht pro Absatz (zu laut), nicht pro Szene (zu weit weg).

---

**Selbst-Check pro Absatz (3 Ebenen, intern, VOR dem Zeigen)**

### Ebene A — Konkretheits-Check (NEU April 2026, ZWINGEND)

| Check | Frage | Fix |
|-------|-------|-----|
| Material | Ist min. 1 benanntes Material/Ding im Absatz (Kupfer, Leinen, Kalk, Messing, Birkenrinde, Tusche, Talg...)? | Wenn nein → konkretes Ding einfuegen, generische Phrase streichen |
| Abstrakta | Mehr als 1 abstraktes Nomen (Stille, Kaelte, Schwere, Leere, Ferne, Dunkelheit, Abgrund, Ewigkeit, Unheimliches)? | Reduzieren auf max. 1. Andere durch Ding/Koerper/Handlung ersetzen |
| Abstrakta-Stapel | Abstraktum+Abstraktum in einer Phrase? ("die Stille des Abgrunds", "die Kaelte der Leere") | Hartes Verbot. Umschreiben |
| Bild-Boden | Jede Metapher steht auf einem im selben Absatz benannten Ding? | Wenn nein → erden oder streichen |
| Vergleich | "wie etwas das...", "wie ein..." | Max 2 pro Kapitel. Nur wenn Vergleichsbild konkreter als Verglichenes |
| Vorfeld | Beginnt der Absatz mit dem Figurennamen UND der vorherige Absatz auch? | Invertieren (Ort, Zeit, Objekt, Adverb im Vorfeld) |

### Ebene B — Stilregel-Check (Bestand)

- Adverb-Tag? (`sagte sie wuetend`) → streichen
- Denk-Tag? (`sie dachte, dass`) → in erlebte Rede
- Benannte Emotion im Narrator? (`sie war traurig`) → Koerperbild
- ERKLAERT-Pattern? (Urteil vor Daten) → Urteil streichen oder hinter die Daten
- Scharnier-Aphorismus? (letzter Satz deutet das Bild) → streichen
- Begehren deklariert? → Koerperbild
- Weasel-Word? (`schien`, `wirkte`, `war irgendwie`) → starkes Verb
- Grammatik: Doppelrelativpronomen, KonjunktivII-Kette, verschachtelte Relativkette → aufbrechen
- Sorel-Prinzip: behauptet Narrator etwas ueber das Unbewusste der Figur? → streichen
- Cross-POV-Mindreading: liest Figur Absichten anderer? (`als wollte sie pruefen, ob...`) → streichen
- Dialog-Handlung: Was TUT die Replik? (schieben/blockieren/preisgeben/annehmen) → sonst streichen

### Ebene C — POV-/Figuren-Check

- Berufslinse passt? Alphina darf nicht in Belichtung denken, Sorel nicht in Wurzeln.
- Satzlaenge unter Figur-Limit? (Alphina ~40W, Sorel ~50W, Vesper ~30W, Maren ~35W)
- POV-Vokabular? (Alphina: "Nebel"; Sorel: "Dunst"; Vesper: "Dunst")

---

**Mini-Council pro Absatz (intern, 3 Stimmen)**

Nach dem Selbst-Check drei Rollen einnehmen, jeweils 1 Satz Urteil. Probleme fixen, Mini-Council wiederholen, bis alle 3 Stimmen OK sagen.

1. **Autorin** (Haltungs-Check):
   > Traegt jeder Satz? Klingt es wie {Figur} oder wie eine Schreiberin, die ueber {Figur} schreibt? Ist ein Bild da, das beim zweiten Lesen nicht haelt?

2. **Konkretheits-Pruefer** (Ding-Check):
   > Kann eine Handwerkerin das Ding im Absatz greifen, wiegen, riechen? Gibt es mehr als 1 Abstraktum? Schwebt eine Metapher ohne Boden?

3. **Leserin** (Stolper-Check):
   > Stolpere ich beim Lesen? Verstehe ich, was gemeint ist? Oder klingt es nur klug? Wuerde ich an dieser Stelle umblaettern wollen?

**Output in der Pruefnotiz:** `Mini-Council ✓` wenn alle 3 OK. Sonst: `Mini-Council: Leserin stolperte bei X → gefixed`.

**KEIN externer Subagent-Council zwischendurch.** Das Mini-Council laeuft rein intern in der Opus-Session. Externe Subagents erst in Phase 5.

**KEIN "Szenen-Council" zwischendurch.**

#### Schritt 3: Post-Scene Dialog-Check

Nach Abschluss jeder Szene die Dialog enthält — 2 Fragen dem Autor vorlegen:

1. **Stimmdifferenzierung:** Erkennst du jede Figur am Satz ohne den Namen? Wenn nein → welche Stelle klingt falsch, welche Figur?
2. **Subtext:** Was wird in diesem Dialog NICHT gesagt? Wenn alles direkt ausgesprochen wird → kein Subtext. Konkrete Stelle nennen.

Bei Problemen: Fixes einarbeiten, Autor-Freigabe abwarten.

### Anti-Patterns waehrend des Schreibens aktiv vermeiden

Siehe `buch/01-autorin-stimme.md` Kapitel 8. Die folgenden Muster entstehen beim Schreiben unbewusst und mussten bei 8 Kapiteln (K09–K16) rueckwirkend in ~200 Findings korrigiert werden. Beim Schreiben aktiv vermeiden:

1. **Scharnier-Aphorismen:** Letzter Satz nach einem starken Bild, der das Bild deutet. Wenn das Bild arbeitet, braucht es keinen Schlusskommentar. `X. Das war Y.` am Absatz-Ende ist verdaechtig.
2. **Figur redet ueber sich:** "Sie war eine von diesen." / "Er wusste, dass er im Weg stand. Er wusste, dass sie wusste, dass er im Weg stand." Statt Selbstkommentar: Koerper, Handlung, Ellipse.
3. **Metapher + Erklaer-Nachsatz:** Bild, dann Nachsatz der das Bild wiederholt. HARTES VERBOT. Das Bild arbeitet allein.
4. **Anaphern-Kaskade >3:** "Darunter... Darunter... Darunter..." Max 2 in Folge.
5. **Emotionen als Substantiv** im Erzaehler: "Sehnsucht", "Obsession", "Scham", "Fuersorge", "das Unheimliche", "die Neugier". VERBOTEN, auch als Nomen.
6. **Mind-Reading:** Die POV-Figur darf Gesten sehen, aber nicht Absichten anderer deuten. "als wollte sie pruefen, ob..." → streichen.
7. **"Es gab Dinge, die..."** / "Manche [X], und sie war eine von diesen." → VERBOTEN (generalisierender Aphorismus).
8. **Doppelpunkt-Pointe-Tic:** `X. Das war Y.` max 2/Kapitel, nie zwei in 10 Zeilen.
9. **Chroniken-Prophezeiung:** "wuerde ein Datum in den Chroniken werden" / "wuerde er sich spaeter erinnern" — Sorel-Prinzip.
10. **Announced Interpretation (ERKLÄRT):** Das Urteil steht vor den Daten. `"Die Stille war zu sauber."` → dann kommen drei Zeilen spaeter die konkreten Details (keine Eidechse, keine Wespe). Das ist rueckwaerts. Entweder: Urteil streichen (Details leisten die Arbeit), oder: Details zuerst, Urteil kommt aus ihnen. NIEMALS: Urteil → Daten.
11. **Spezifizitaets-Test (ABSTRACT):** Kann dieser Satz durch einen generischeren ersetzt werden ohne Informationsverlust? `"Die Stille war seltsam."` = kein Informationsverlust = zu vage. Ein konkretes Bild muss so spezifisch sein, dass es NUR in diesem Raum, NUR bei dieser Figur, NUR in diesem Moment stimmt. Test: Koennte dieser Satz unveraendert in einem anderen Dark-Fantasy-Roman stehen? Wenn ja → zu generisch.
12. **Weasel-Words:** `schien`, `wirkte`, `war irgendwie`, `fuehlte sich an als` — verweigern Information statt sie zu geben. Max 2 pro Kapitel. Starkes Verb > Weasel-Word + Adjektiv.
13. **Begehren deklariert (BEGEHREN):** Die POV-Figur sagt explizit was sie fuehlt (`"Sie wollte ihn so sehr"`, `"Er zog sie an wie..."` als direktes Label). Koerper liefert die Daten — Kopf liefert keine Auswertung. Der Leser zieht die Schlussfolgerung, nicht die Figur.
14. **Generic-Darkness-Test:** Atmosphaere-Saetze pruefen: Klingt dieser Satz nach diesem spezifischen Garten / dieser Figur / diesem Moment? Oder nach Dark Fantasy im Allgemeinen? Bardugo: `"yellowy blister in need of lancing"` — das ist nur Ketterdam, nicht jede dunkle Stadt. Wenn der Satz austauschbar ist: konkreter.

**Test nach jeder Szene — Inhalt:** Letzten Satz jedes Absatzes anschauen. Wenn er das vorhergehende Bild kommentiert, generalisiert oder bewertet bevor die Daten da waren — streichen.

**Hinweis:** Der Absatz-Selbst-Check (3–7 Saetze, 40–120 W) loest den Block-Check (5–10 Saetze) und den frueheren 500-Woerter-Check ab. Durch den engeren Takt + Mini-Council wird Drift in Abstraktion/Verkuenstelung im Moment des Entstehens abgefangen, nicht nachtraeglich.

### Grammatik-Klarheits-Test (nach jeder Szene, ZWINGEND)

Dieser Test fängt **accidentelle** Satzbrüche — nicht inhaltliche Anti-Patterns, sondern Konstruktionen, die während der Generierung grammatisch oder logisch kaputt gegangen sind. 60 Sekunden, jeden Satz über 20 Wörtern:

1. **Doppeltes Relativpronomen:** `[Nomen], [die/der/das] [die/der/das]` in einem Satz? Fast immer gebrochen. → Zwei Sätze.
   - Beispiel-Bruch: *"eine Stille zwischen sich, die die Grillen weitersangen"* — "die" referiert auf Stille, aber "Grillen sangen" braucht Grillen als Subjekt → zerfällt.

2. **Tautologie / Zirkellogik:** Sagt der Satz etwas, das sich zwingend aus sich selbst ergibt?
   - Beispiel-Bruch: *"ein Farn wächst nicht, an dem er nicht steht"* — natürlich nicht, wo er nicht steht, steht er nicht. Konkretisieren.

3. **Sinnfrage:** Was sagt dieser Satz konkret? Auf 5 Wörter komprimieren — was bleibt? Wenn nichts Substanzielles bleibt → streichen.
   - Beispiel-Bruch: *"wie etwas, das schon unterwegs war, bevor ich es bestellt habe"* — bedeutet: ich hab es nicht gewollt. Dann das schreiben.

4. **Konjunktiv-II-Erklär-Klausel:** Endet der Satz mit `weil [X] nicht [Y] hätte/wäre/könnte`? → In 90% der Fälle Füllmaterial. Streichen.
   - Beispiel-Bruch: *"stieg nicht in den Kopf, weil der Kopf ihn nicht gebraucht hätte"* → *"stieg nicht in den Kopf."*

5. **Berufslinsen-Metapher:** Woher kommt dieses Bild? Gehört es zum Beruf dieser POV-Figur?
   - Alphina (Botanikerin): Wachstum, Wurzeln, Triebe, Druck. KEIN Kran, keine Belichtung, kein Takt.
   - Sorel (Fotograf): Licht, Belichtung, Tonwert, Winkel. KEIN Pflanzenwachstum.
   - Vesper (Uhrmacher): Takt, Toleranz, Passung, Frequenz. KEINE Strömung.
   - Maren (Schiffbauerin): Strömung, Holz, Zug, Gezeiten. KEINE Sterndeutung.

6. **Verschachtelte Relativkette:** Mehr als zwei Einschübe in einem Satz? → Aufbrechen. Jeder Einschub kostet Leserin-Kapazität; die zweite Verschachtelung fast immer zu viel.

### Harte Regeln waehrend der Ausarbeitung

- **Jeder Plot-Beat aus dem Entwurf MUSS in der Prosa landen.** Dialog-Info-Punkte werden in echten Dialog/Aktion umgesetzt — keine darf verloren gehen.
- **Keine Plot-Aenderung still in der Prosa.** Wenn waehrend des Schreibens auffaellt dass ein Beat nicht funktioniert:
  1. SOFORT stoppen
  2. Dem Autor das Problem nennen
  3. Im Handoff-File einen "Rueckkehr noetig"-Vermerk schreiben
  4. Vorschlagen: Status zurueck auf `entwurf`, neue `/entwurf`-Session
  - **Niemals den Plot still anpassen.**
- **Die Tuer bleibt offen, die Kamera bleibt im Raum.** BDSM/Erotik wird explizit, praezise, koerperlich. Keine Fade-to-Black.
- **Verfremdete Verben in Moragh-Szenen** (falls Kapitel in Moragh spielt): unerwartete Verbwahl ohne erfundene Woerter.
- **POV-Vokabular respektieren** (siehe `02-stilregeln-v2.md` POV-Vokabular-Tabelle): Alphina sagt "Nebel", Sorel sagt "Dunst", etc.

### Datei-Aufbau

```markdown
# {ID} — {Figur}

{Optional: Untertitel}

{Szene 1, ~1.200-1.600 W, voll ausgearbeitete Prosa}

---

{Szene 2, ~1.200-1.600 W}

---

{Szene 3, ~1.200-1.600 W}
```

## Phase 3: Status setzen + Deploy

```bash
# status.json updaten:
# - state: "ausarbeitung"
# - datei: "{ID}-{figur}.md"
git add buch/status.json buch/kapitel/{ID}-{figur}.md
git commit -m "feat({ID}): Ausarbeitung — {Figur}, {Wörter}W"
git push
ssh adrian@adrianphilipp.de "cd ~/apps/Alphina-Static && git pull && bash generate-lesen.sh"
```

Status: `ausarbeitung`.

## Phase 4: Stil-Check (Subagent, sonnet)

Dispatch:
- `subagent_type: "general-purpose"`
- `model: "sonnet"`
- Prompt:

```
Du pruefst ein Kapitel von "Der Riss" auf Stilfehler. Brutal, mit Zahlen.

Lies parallel:
1. buch/kapitel/{ID}-{figur}.md (das Kapitel)
2. buch/02-stilregeln-v2.md (Stilregeln)

Pruefe (mit Grep wo moeglich):
- "nicht X — sondern Y" / "nicht X, sondern Y" — max 1x
- "wie etwas das..." / "wie ein..." Vergleiche — **max 2x** (verschaerft April 2026)
- Adverb-Tags ("sagte er wuetend") — max 0
- Denk-Tags ("sie dachte, dass") — max 0
- Direkte Emotionsbenennung ("er war traurig", "sie fuehlte Wut") — max 0
- Flashback-Rampe ("sie erinnerte sich an den Tag") — max 0
- Praemature Ahnung ("sie wusste noch nicht, dass") — max 0
- Komma-Listen mit 3+ Substantivphrasen ohne Verb — markieren
- "und"-Ketten >3 pro Satz — markieren
- Saetze ueber Figur-Limit (Alphina ~40W, Sorel ~50W, Vesper ~20W, Maren ~35W)
- Stakkato-Passagen: max 2-3, je max 3 Fragmente in Folge
- Personifikationen: max ~8 pro Kapitel
- POV-Vokabular-Bruch (Alphina sagt "Dunst" statt "Nebel" o.ae.)
- **Konkretheits-Check (NEU):** Absaetze zaehlen, bei wie vielen KEIN benanntes Material (Kupfer, Leinen, Kalk, Messing, Birkenrinde, Tusche, Talg...) vorkommt — bei mehr als 20% aller Absaetze: FINDING "zu abstrakt"
- **Abstrakta-Dichte (NEU):** Grep auf "Stille", "Kaelte", "Schwere", "Leere", "Ferne", "Dunkelheit", "Ewigkeit", "Unheimliches", "Abgrund" — pro Absatz max 1, pro Kapitel max ~15 gesamt; bei >20: FINDING
- **Abstrakta-Stapel (NEU):** Grep auf Muster "der/die/das [Abstraktum] des/der [Abstraktum]" ("die Stille des Abgrunds", "die Kaelte der Leere") — max 0

Output: Tabelle mit Findings (Zeile, Typ, Problem, Fix-Vorschlag). Max 1.5k Token.

Verdikt: BESTANDEN / NICHT BESTANDEN.
```

## Phase 5: Final Council (3 Subagenten, sequenziell)

### Subagent 1: Stilkritiker (sonnet)

Dispatch:
- `subagent_type: "general-purpose"`
- `model: "sonnet"` (auf Autor-Wunsch optional `opus` fuer kritische Kapitel)
- Prompt:

```
Du bist Stilkritiker fuer "Der Riss". Du pruefst gegen das Medley.

Lies parallel:
1. buch/kapitel/{ID}-{figur}.md
2. buch/02-stilregeln-v2.md
3. buch/kapitel/{letztes-fertiges-{figur}-kapitel}.md (Ton-Referenz)

Leitfrage: "Wuerde ein King, ein SenLinYu, eine Simone diesen Absatz so stehen lassen?"

Pruefe:
- King-Dichte: Mundane Details die feuern? Sinne aktiv? Spezifisch?
- SenLinYu-Zurueckhaltung: Bleibt die Prosa kontrolliert? Bricht sie an EINER Stelle hart?
- Simone-Kadenz: Werden fremde Register (Botanik, Mechanik) fuer Innensicht benutzt?
- Bardugo-POV-Signatur: Erkennt man am Stil wer spricht?
- Black-Verfremdung (nur in Moragh-Szenen): Unerwartete Verbwahl?

Vergleich mit Ton-Referenz: Stimmt der Figurenton ueberein?

Max 1k Token. Verdikt + 3-5 konkrete Findings.
```

### Subagent 2: Dark-Romance/BDSM-Leserin (sonnet)

Dispatch:
- `subagent_type: "general-purpose"`
- `model: "sonnet"`
- Prompt:

```
Du bist eine erfahrene Leserin von Dark Romance, BDSM-Romantik (Sierra Simone, Tiffany Reisz, Cara Dee). Du liest ein Kapitel von "Der Riss".

Lies:
1. buch/kapitel/{ID}-{figur}.md
2. buch/pov/{figur}.md (POV-Dossier)

Pruefe als Genre-Leserin:
- Power-Dynamik: Wer hat die Kontrolle? Wo verschiebt sie sich?
- Begehren als Unterstrom: Brennt es zwischen den Figuren? Auch ohne Sexszene?
- BDSM (falls relevant): Ist es Beziehungsarbeit, Charakter-Enthuellung — oder Dekoration?
- Hingabe und Kontrolle: Wer gibt was hin? Was bekommt sie/er zurueck?
- Erotische Zurueckhaltung DAVOR vs. Praezision DARIN
- Funktioniert es fuer dich als Genre-Leserin? Wirst du feucht/angeregt/herausgefordert?

Sei direkt. Keine Hoeflichkeit. Sag wenn es nur Plot ist und keine Spannung hat.

Max 1k Token. Verdikt + konkrete Findings.
```

### Subagent 3: Romantasy-Leserin (sonnet)

Dispatch:
- `subagent_type: "general-purpose"`
- `model: "sonnet"`
- Prompt:

```
Du bist eine erfahrene Romantasy-Leserin (Yarros, Maas, SenLinYu). Du liest ein Kapitel von "Der Riss".

Lies: buch/kapitel/{ID}-{figur}.md

Pruefe als Leserin:
- Sog: Will ich weiterlesen? Was zieht mich rein?
- Emotion: Fuehle ich was? Wo? Wo nicht?
- Tension: Wo ist die Spannung? Wo flacht sie ab?
- Mystik: Habe ich das Gefuehl dass unter dem Text noch eine Schicht liegt?
- Ueberraschung: Werde ich ueberrascht? Oder sehe ich alles kommen?

Sei ehrlich. Wenn es zaeh ist, sag es. Wenn ein Moment sitzt, sag warum.

Max 1k Token. Verdikt + konkrete Findings.
```

## Phase 5.5: Autorin-Durchgang (Subagent, opus)

**Warum:** Stil-Check fängt formale Verstoesse, Council fängt Genre- und Leser-Probleme. Die Autorin faengt **Haltungs-Verstoesse** — Aphorismen an Scharnieren, Pointen-Tics, benannte Emotionen durch die Hintertuer, Metaphern die beim zweiten Lesen nicht halten, Saetze die klug klingen wollen aber nichts sagen. Die drei Leser-Subagenten sehen das seltener. Die Autorin ist der schaerfste Blick.

Dispatch:
- `subagent_type: "general-purpose"`
- `model: "opus"` (nicht sonnet — Haltung braucht Sprachgefuehl)
- Prompt:

```
Du bist die Autorin von "Der Riss". Deine Stimme und Regeln stehen in:
- buch/01-autorin-stimme.md

Lies diese Datei ZUERST, vollstaendig. Du schreibst nicht "nach" der Autorin — du BIST sie. Verinnerliche ihre Prinzipien: King-Erzaehldichte, SenLinYu-Zurueckhaltung, Berufslinse als Filter, kein Adverb-Tag, keine benannten Emotionen, erlebte Rede als Default, POV-Register, Kontrollverlust-Momente, Anti-Patterns.

Dann lies das Kapitel:
- buch/kapitel/{ID}-{figur}.md

**Deine Aufgabe — nicht Stil-Check formal, sondern Autor-Lesen:**

Gehe Satz fuer Satz durch. Bei jedem Satz frage dich:
1. Traegt der Satz? Transportiert er etwas (Bild, Information, Koerperzustand, Spannung)? Oder ist er Fuellmaterial?
2. Versteht die Leserin, was gemeint ist? Oder stolpert sie?
3. Ist der Satz *wahr* in der Figur? Klingt er wie etwas, das {Figur} tatsaechlich denken wuerde? Oder wie eine Schreiberin, die aus der Figur heraus schreibt?
4. Stolpert der Rhythmus? Bandwurm wo Hammer gebraucht wuerde. Bild + Nachsatz der erklaert.

**Besonders achten auf:**
- Saetze, die klug klingen wollen aber nichts sagen (Aphorismen an Scharnieren)
- Metaphern, die beim zweiten Lesen nicht halten
- Doppelpunkt-Pointen ("X. Das war Y.") — Tic, wenn mehr als 1-2x im Kapitel
- Wiederholungen derselben Erkenntnis in verschiedenen Formulierungen
- Saetze wo die Figur "ueber sich redet" statt zu sein
- Benannte Emotionen als Substantive (Obsession, Sehnsucht, Angst, Scham)
- Verb-Fehler mit Bedeutung (haengte/hing, schwoll/schwellte, etc.)
- **Verkuenstelung (NEU April 2026):** Abstrakta-Stapel ("die Stille des Abgrunds"), Bild auf Bild ohne Material-Boden, Metaphern die schweben weil das Referenz-Ding nicht benannt ist, Absaetze ohne ein einziges benanntes Material. Pruefe: Kann eine Handwerkerin das Ding im Absatz greifen? Siehe `01-referenz-konkretheit.md`.

**Output:**
Liste KONKRETE Saetze (mit Zeilenverweis und Zitat), die:
- (A) GESTRICHEN werden sollten (tragen nicht / Autoren-Pointen)
- (B) UMFORMULIERT werden sollten (mit konkretem Fix-Vorschlag)
- (C) BLEIBEN MUESSEN (besonders stark — 3-6 Passagen)

Begruende jedes Finding aus Autorin-Perspektive. Sei ehrlich und streng.

Max 2.5k Token.
```

## Phase 6: Konsolidierter Bericht

Zeige dem Autor:
1. Stil-Check Findings (Tabelle)
2. Stilkritiker (Verdikt + Findings)
3. Dark-Romance-Leserin (Verdikt + Findings)
4. Romantasy-Leserin (Verdikt + Findings)
5. **Autorin-Durchgang (A/B/C-Liste mit Zeilenverweisen)**
6. Gesamt-Verdikt

Frage: "Findings einarbeiten oder OK?"

## Phase 7: Fixes-Loop

In derselben Opus-Session:
- Fixes einarbeiten (Edit-Tool wo moeglich, Write nur fuer ganze Szenen-Neufassungen)
- `wc -w` nach jedem Fix
- Re-deploy nach groesseren Fix-Runden
- Loop bis Stil-Check + Council OK + Autor bestaetigt

## Phase 8: Status `lektorat` + Deploy

```bash
# state: "lektorat"
git add ...
git commit -m "feat({ID}): Lektorat — {Figur}, {Wörter}W, Council bestanden"
git push
ssh adrian@adrianphilipp.de "..."
```

Status: `lektorat`. Autor liest online.

## Phase 9: Handoff fuer Lektorat-Fixes (Subagent, haiku)

Dispatch:
- `subagent_type: "general-purpose"`
- `model: "haiku"`
- Prompt:

```
Erstelle ein Handoff-File fuer den Phasen-Uebergang von /ausarbeitung zu /lektorat-fix.

Datei: buch/kapitel/{ID}-handoff.md (UEBERSCHREIBE die alte)

Format:

# Handoff — {ID}

**Von Phase:** ausarbeitung → **Zu Phase:** lektorat-fix
**Erstellt:** {Datum/Uhrzeit}
**Status beim Handoff:** lektorat

## Modell-Empfehlung
claude --model sonnet
(oder claude --model haiku fuer Mikro-Fixes)

## Aufruf fuer naechste Session
/lektorat-fix {ID}

## Kontext
- Datei: buch/kapitel/{ID}-{figur}.md
- Phase: Lektorat-Fixes (Autor-getrieben, kleine Edits)
- Kein neuer Stil-Check, kein Council. Nur was der Autor anfasst.

## Anweisungen
- Edit-Tool bevorzugt vor Write-Tool
- Kein ungefragtes Umformulieren
- Bei groesseren Wuenschen: Hinweis auf Rueckstufung zu /ausarbeitung
- Status final NUR auf explizite Autor-Freigabe

Max 100 Wörter Bericht zurueck.
```

## Phase 10: Harter Stop

Zeige dem Autor:

> KAPITEL AUSGEARBEITET. Status: lektorat.
>
> Naechster Schritt: NEUE SESSION mit Sonnet (oder Haiku).
>
> 1. Diese Session beenden
> 2. Autor liest das Kapitel online auf der Story-in-Work Webseite
> 3. Wenn Feedback kommt: `claude --model sonnet`, dann `/lektorat-fix {ID}`
>
> Diese Session schreibt jetzt nichts mehr.

**WICHTIG:** Nach Phase 10 NICHT weiterarbeiten. Auf Folgefragen: "Diese Phase ist abgeschlossen. Bitte starte eine /lektorat-fix-Session sobald du Feedback hast."

## Sonderfall: Plot-Beat traegt nicht

Wenn waehrend Phase 2 oder 4-7 ein Plot-Problem entdeckt wird das nicht durch Sprach-Arbeit zu loesen ist:

1. SOFORT stoppen
2. Im Handoff-File vermerken: "Rueckstufung noetig — Begruendung: ..."
3. Status zurueck auf `entwurf-ok` oder `entwurf` setzen
4. Dem Autor sagen: "Plot-Problem entdeckt. Beschreibung: ... Vorschlag: zurueck zu /entwurf, neu councilen, dann erneut /ausarbeitung."

**Niemals den Plot still anpassen.**

## Regeln

- Lade NUR die Files aus Phase 1.
- Prosa direkt im Final-File (`{ID}-{figur}.md`), nicht in Szenen-Drafts.
- Kein Szenen-Council zwischendurch.
- Setze NIEMALS `final` (nur `lektorat`).
- Schreib Umlaute aus (ä, ö, ü, ß). KEIN ae/oe/ue.
- Deutsch.

$ARGUMENTS
