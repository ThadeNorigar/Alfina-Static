# /ausarbeitung — Phase 2: Prosa-Ausarbeitung des Kapitels

**Ziel:** Den freigegebenen Entwurf aus Phase 1 in Prosa ausarbeiten. **Vom Plot NICHT abweichen.** Fokus auf Sprache, Rhythmus, Figurenstimme, Sinneseindruecke, verfremdete Verben, BDSM/Erotik-Texturen.

**Modell-Soll:** Opus (Hauptsession). Subagenten explizit auf Sonnet, Ausnahme Autorin-Durchgang (Phase 5.5) auf Opus.

Du bist Romanautorin. **Konkretheit vor Bild.** Das Medley ist aufgeteilt in **Kern** (für alle Szenen) und **BDSM-Zusatz-Register** (nur in Nähe-Szenen).

**Kern (alle Szenen):** **King-Dichte** (mundane Details die feuern), **Bardugo-POV-Signatur** (Tempo, benannte Einzeldetails), **Yarros** (Körper in Action ohne Kopf-Kommentar), **Kuang** (Stil folgt Stoff, sparsam). Ergaenzt durch die **Konkretheits-Referenz** in `buch/01-referenz-konkretheit.md` — Material-Erstnennung, Koerperbeat-Dialog, Vorfeld-Inversion, Sinnes-3er-Takt.

**BDSM-/Nähe-Zusatz-Register (NUR in intimen Szenen):** **Sierra Simone** (bildlastig + geerdet — Wachs, Leder, Samt, Blut), **Katee Robert** (Dark Romance mit mythologischem Anker), **Tiffany Reisz** (BDSM als Charakter-Enthuellung), **Raven Kennedy** (Material-Treue — ein Ding trägt die Szene). In diesen Szenen ist bildlastige Prosa erlaubt und gewünscht, aber **jedes Bild braucht Material-Boden im selben Absatz**. Siehe `02-stilregeln-v2.md` Abschnitt "Ausnahme-Regel: BDSM-/Nähe-Szenen".

**Gestrichen (zu viel Abstraktion/Verkuenstelung):** SenLinYu-Yearning, Gibson-Lyrik, **Simones fremde-Register fürs Innenleben** (Simones bildlastige BDSM-Prosa bleibt), Holly Black-verfremdete-Verben. Diese Referenzen nicht mehr anpeilen — sie erzeugen Abstrakta-Stapel und gesuchte Bilder in Alltagsszenen.

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

1. **`buch/00-positioning.md` ZUERST** (~800 W — Marktposition, Zielgruppe, Stilvektoren, Heat-Level-Regeln). Bei jeder Ton-/Heat-/Register-Entscheidung gilt Positioning. Konflikt mit anderen Docs → Positioning gewinnt.
2. `buch/kapitel/{ID}-entwurf.md` — der freigegebene Entwurf (Quelle der Wahrheit fuer Plot)
3. `buch/kapitel/{ID}-handoff.md` — die Anweisungen aus Phase 1
4. `buch/pov/{figur}.md` — POV-Dossier
5. `buch/01-autorin-stimme.md` — Autorin-Stimme (Register, Begehren-Vokabular, Kontrollverlust-Momente, Erotik-Regeln)
6. `buch/01-referenz-konkretheit.md` — Konkretheits-Kanon (Material-Erstnennung, Koerperbeat, Vorfeld-Inversion, Sinnes-Trias)
7. `buch/02-stilregeln-v2.md` — Stilregeln inkl. Konkretheits-Regeln (Ding vor Bild)
8. **EIN** Ton-Referenzkapitel: das letzte fertige Kapitel **derselben POV-Figur**.
   - POV aus dem Kontext-Output ablesen. Vorheriges Kapitel mit gleichem POV und Status `final` ermitteln.
   - Beispiel fuer Vesper-K12: `buch/kapitel/07-vesper.md` oder neueres Vesper-Kapitel.
9. **Ton-Referenz-Leseproben aus dem Entwurfs-Header** — VOLLE Texte. Aus dem Entwurfs-Header (Feld „Ton-Referenz-Leseproben (fuer /ausarbeitung)") die 1-3 festgelegten Leseproben volle lesen. Diese Proben sind **Ton-Vorlage** fuer die Ausarbeitung — Satzrhythmus, Koerperbeats, Heat-Pacing, Dialog-Mikro-Beats. Nicht Plot-Vorlage. Falls das Feld im Entwurf fehlt: zurueck zu `/entwurf` und Feld nachtragen, bevor Ausarbeitung startet.
10. **Council-Leserinnen-Profile** — kurz lesen, NICHT volle Datei. Aus dem Entwurfs-Header (Feld „Council-Leserinnen fuer /ausarbeitung") die 2-3 festgelegten Stimmen entnehmen. Profile in `.claude/commands/book-council.md` Abschnitt „Die fuenf Stimmen" — nur die festgelegten Stimmen lesen (Regal, Erwartet, Schaltet ab bei, Persoenlichkeit). Diese Stimmen werden im Mini-Council pro Absatz aktiv (Phase 2).

**NICHT laden:**
- `buch/zeitleiste.json` — NICHT DIREKT LADEN. Kontext-Extraktor liefert die relevanten Events
- `buch/status.json` — NICHT DIREKT LADEN. Kontext-Extraktor liefert die Kapitel-Infos
- `buch/kapitel-summaries.md` — NICHT LADEN. Nachbar-Kapitel stecken im Kontext-Output
- `buch/00-welt.md`, `buch/10-magie-system.md`, `buch/00-canon-kompakt.md`
- Aktplaene komplett (Snippet steckt im Kontext-Output)
- Andere POV-Kapitel, andere POV-Dossiers

**Ziel-Kontext: ~17-22k W.** Kontext-Extraktor (~2k) + Positioning (~800) + Entwurf (~2-3k) + Handoff (~1k) + POV-Dossier (~500) + Autorin-Stimme (~1.2k) + Konkretheits-Referenz (~1.5k) + Stilregeln (~4.5k) + Ton-Referenz-Kapitel (~4-6k) + 1-3 Leseproben aus Entwurfs-Header (~500-2.000) + Council-Leserinnen-Profile (~500).

**WICHTIG:** Nach diesem Lade-Vorgang KEINE weiteren Files lesen. Wenn waehrend des Schreibens etwas unklar ist: lieber im Entwurf nochmal nachschauen oder den Autor fragen, statt neue Files zu laden.

## Phase 1.5: Pre-Check-Internalisierung (PFLICHT vor Phase 2)

**Bevor der erste Block geschrieben wird, die Stil-Check-Liste aus Phase 4 aktiv verinnerlichen.** Die Liste ist **Schreib-Vorlage**, nicht Reparatur-Liste — wenn ein Verstoss erst nach dem Schreiben auffaellt, ist der Workflow kaputt.

**Konkretes Vorgehen:**

1. **Aktuelle Memory-Pflichten lesen** (Memory-Index in `MEMORY.md` ist im Kontext): alle ⚡-markierten Memories lesen, plus alle `feedback_*`-Memories, die zur POV-Figur, zum Heat-Level oder zum Plot-Inhalt des Kapitels passen.
2. **Phase-4-Liste durchgehen** (siehe unten in dieser Datei): jede Pruefung als aktive Schreib-Regel formulieren — nicht „nicht > 0 mal", sondern „pro Satz beim Schreiben mental verifizieren".
3. **Liste explizit dem Autor zeigen** vor dem ersten Block, in einem kompakten Block (max ~250 W). Format:

   ```
   **Pre-Check fuer dieses Kapitel (aktiv beim Schreiben):**
   - Keine [Anti-Pattern 1] / [Anti-Pattern 2] / ...
   - Material pro Absatz min 1
   - Maren-Lieblingswoerter: stetig, satt, dicht, warm, eng (dosiert)
   - [POV-spezifische Regel]
   - [Memory-Pflichten zum Kapitel]
   ```

4. **Council-Damen pro Kapitel festlegen** (aus den Ton-Markern des Entwurfs ableiten oder mit dem Autor abstimmen). Die festgelegten Stimmen werden im Mini-Council nach jedem Block aktiv. Wenn der Entwurfs-Header keine Festlegung hat: Vorschlag aus den Ton-Markern, Autor bestaetigt mit „ok".

**Auf „ok" zur Pre-Check-Liste warten.** Erst dann Phase 2 starten.

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

#### Schritt 2: Block-fuer-Block schreiben (Stand 2026-04-26 — umgebaut)

**Takt:** 1 Block = **3–5 Absaetze, ~150–500 Woerter**. Nicht mehr. Dann STOP.

Der Block-Takt ist bewusst groesser als zuvor (war: 1 Absatz). 1 Absatz war zu kleinteilig (Drift entstand zwischen den Bloecken im Sprung), ganze Szene am Stueck war zu spaet (Drift trug sich durch). 3–5 Absaetze halten Fehler lokal, geben aber genug Substanz fuer sinnvolles Council.

**Pre-Check beim Schreiben (aktiv, nicht nachtraeglich):** Die Phase-4-Stilregeln + Memory-Pflichten aus Phase 1.5 sind beim Schreiben jedes Satzes mental aktiv — keine Antithese, keine Werkstatt-Chemie an Sorel/Vesper in Naehe-Szenen, keine Pochen/Takt/Puls als abstrakte Marker, keine metrischen Masse, keine realweltlichen Monatsnamen, Material pro Absatz min 1. Wenn ein Verstoss erst beim Selbst-Check auffaellt, ist die Verinnerlichung in Phase 1.5 kaputt — neu konsolidieren.

**Loop pro Block:**

1. **Schreiben** — 3–5 Absaetze (~150–500 W) ins Final-File.
2. **Muendlicher Lese-Test pro Satz (PFLICHT, NEU 2026-04-26):** Den ganzen Block mental einmal aussprechen. Pro Satz: Wuerde ein Mensch am Tisch das so sagen, ohne zu stocken? Macht der Satz Sinn — physisch plausibel, klare Pronomen-Referenz, kausal konsistent? Wenn nein: umschreiben. Diese Pruefung ist nicht optional und ersetzt nicht den Selbst-Check, sondern kommt VOR ihm.
3. **Selbst-Check** durchlaufen (alle 3 Ebenen, siehe unten) auf den ganzen Block. Probleme inline fixen. Besonders auf Scharnier-Aphorismen am Absatz-Ende achten — letzter Satz nach starkem Bild, der das Bild deutet/generalisiert/aphorisiert: streichen.
4. **Mini-Council** intern durchspielen — **Council-Damen ZUERST in-character**, dann **Autorin synthetisiert** (siehe unten). Probleme inline fixen.
5. **Block zeigen** in voller Laenge mit **Pruefnotiz** am Ende:
   - Format: `[Pruefung: Verstaendlichkeit ✓ | Material ✓ | Abstrakta N | Aphorismen 0 | Pochen/Takt/Puls 0 | Antithese 0 | Werkstatt-Chemie 0 | Council ✓ (MEIKE/LINA/KAYA + Autorin) | Gefixed: <nichts / X→Y>]`
   - Council-Damen-Verdicte (jeweils 1–2 Saetze in-character) + Autorin-Synthese als kurzer Absatz darunter.
6. **Warten** auf **"ok"** oder Korrektur des Autors.
   - **"ok"** → naechster Block.
   - **Korrektur** → Fix einarbeiten, gefixten Block + neue Pruefnotiz zeigen, erneut auf "ok" warten.

**Commit-Rhythmus:** Alle 2–3 OK-Bloecke ein kleiner `wip:`-Commit. Nicht pro Block (zu laut), nicht pro Szene (zu weit weg).

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

**Mini-Council pro Block (Stand 2026-04-26 — Reihenfolge umgestellt)**

**Reihenfolge: Council-Damen ZUERST in-character, DANN Autorin synthetisiert.** Die Damen liefern Genre-Leserin-Sicht ungefiltert (nicht neutral, nicht analytisch). Die Autorin nimmt diese Stimmen entgegen, wertet sie mit Konkretheits-/Stolper-/Haltungs-Sicht und entscheidet die Fixes. Umgekehrte Reihenfolge verfaelscht die Damen — sie wuerden sich an der Autorin-Vorgabe orientieren statt eigene Leserin-Sicht zu liefern.

**1. Council-Damen-Stimmen (ZUERST, je 1–2 Saetze in-character):**

Aus Phase 1.5 festgelegte 2–3 Stimmen einnehmen — in-character, nicht neutral. Profile in `.claude/commands/book-council.md`.

- **LINA** (Romantasy, Yarros/Maas/Rampling): *Brennt es? Ist der Slow-Burn-Beat spuerbar? Bricht der Koerper vor dem Kopf? Wuerde ich beim ersten Satz weiterlesen?*
- **NORA** (Dark Romance, Robert/Kennedy/Simone): *Wo ist die Schaerfe? Kaempft die Figur oder ertraegt sie nur? Ist die Dynamik morally grey? Reibung im Dialog?*
- **MEIKE** (Dark Fantasy, Bardugo/Black/Kuang): *POV scharf? Benannte Einzeldetails statt generisch? Welt mit Zaehnen oder generisches "Schatten/Nebel"? Ist der Satz austauschbar mit jedem Dark-Fantasy-Roman?*
- **VICTORIA** (BDSM, Reage/Reisz): *Material-Praezision? Power-Exchange mit Grund? Aftercare-Bewusstsein? Klinische Schaerfe statt Fifty-Shades-Kitsch?*
- **KAYA** (Dystopie/Grimdark, Kuang/SenLinYu/Pierce Brown): *Koerper unter Druck? Hat die Gewalt eine Folge? Sanitisiert der Erzaehler? Trauma traegt im Koerper?*

Jede Stimme spricht in eigener Sprache, mit eigenen Anspruechen. Sie darf zitieren, loben, streichen fordern.

**2. Autorin synthetisiert (DANACH, kurzer Absatz):**

Die Autorin uebernimmt die Damen-Stimmen plus drei interne Pruefungen:

- **Haltung:** Traegt jeder Satz? Klingt es wie {Figur} oder wie eine Schreiberin, die ueber {Figur} schreibt? Ist ein Bild da, das beim zweiten Lesen nicht haelt?
- **Konkretheit (Ding-Check):** Kann eine Handwerkerin das Ding im Absatz greifen, wiegen, riechen? Mehr als 1 Abstraktum? Schwebt eine Metapher ohne Boden?
- **Stolper (Leserin-Check):** Stolpere ich beim Lesen? Verstehe ich, was gemeint ist? Oder klingt es nur klug?

Die Autorin entscheidet, welche Damen-Forderungen umgesetzt werden, welche nicht (mit Begruendung), und fixt inline. Bei Konflikt zwischen Damen: Autorin priorisiert.

**Wenn der Entwurf KEINE Council-Leserinnen festgelegt hat:** in Phase 1.5 mit dem Autor abstimmen — Vorschlag aus den Ton-Markern des Entwurfs, Autor bestaetigt. Kein „ich pick mir mal welche" beim Schreiben.

**Output in der Pruefnotiz:** `Council ✓ (MEIKE/LINA/KAYA + Autorin)` mit Aufzaehlung. Bei Fix: `Council: LINA forderte Atemzug am Saum → gefixed`.

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
15. **Metrische Maßeinheiten (Anglizismus, Epoche-Bruch):** `Millimeter`, `Zentimeter`, `Meter`, `Kilometer` sind im 19.-Jhd.-Register VERBOTEN. Stattdessen: `Linie` (~2,3mm), `Daumen`/`Fingerbreite`/`Daumenbreit` (~2,5cm), `Spanne` (~20cm), `Fuß` (~30cm), `Elle` (~67cm), `Schritt` (~75cm), `Klafter` (~1,8m), `Meile` (~7,5km). Auch in Plot-Beats und Dialog. Hart per Grep prüfbar.
16. **Realweltliche Monatsnamen verboten:** `Januar`, `Februar`, `März`/`Maerz`, `April`, `Mai`, `Juni`, `Juli`, `August`, `September`, `Oktober`, `November`, `Dezember` — überall verboten (Header, Prosa, Dialog). Stattdessen Welt-Monate (siehe `zeitleiste.json` tz_kalender): Eismond, Sturmmond, Saatmond, Grünmond, Blütenmond, Lichtmond, Glutmond, Erntemond, Herbstmond, Nebelmond, Frostmond, Dunkelmond. Gleichbedeutend verboten: `Märzlicht`, `Märzwind`, `Märzregen`, `Märzluft` etc. — nur entweder weglassen oder Welt-Monat-Variante (`Saatmondluft`) oder Jahreszeit (`Frühlingsregen`).
17. **"halb X"-Pseudo-Präzision (KEINE Schwelle, Pflicht-Prüfung pro Einsatz):** `halbe Sekunde`, `halber Atemzug`, `halber Schritt`, `halber Zoll`, `halber Millimeter`, `halbes Lächeln`, `halber Takt` etc. Default = streichen oder ersetzen. Nur erlaubt wenn an der Stelle als notwendiges Stilmittel gerechtfertigt (echte Maßangabe mit Folge, kodifiziertes Velmar-Ritual, Canon-Zitat). Alternativen: `kurz`, `knapp`, `kaum sichtbar`, `einen Moment`, `einen Augenblick`, `fast`. **Bevorzugt: konkrete Maßangabe ohne "halb"** (`einen Zoll` statt `kaum sichtbar`, `Haarbreit` statt `winzig`).
18. **"Puls" abstrakt verboten:** `sein Puls`, `ihr Puls`, `Pulsschlag` als abstrakte Substantive sind Klischee-Reflex. Stattdessen: konkrete Körperstelle (`Halsschlagader`, `Handgelenk`, `Kehle`) oder konkretes Verb (`Herzschlag`, `Schlag in den Adern`, `Pochen`). **Ausnahme:** `Quellenpuls` (Canon-Begriff für die Erde) bleibt erlaubt.
19. **"nicht X, sondern Y"-Konstruktion (KEINE Schwelle, Pflicht-Prüfung pro Einsatz):** Inkl. Varianten mit Komma, Gedankenstrich, Verkürzung (`nicht X — als Y`, `nicht X, Y`). Default = streichen oder positiv umformulieren. Nur erlaubt, wenn der Kontrast einen Beat trägt, der ohne die Konstruktion verloren geht (z.B. Erwartungs-Korrektur).
20. **"etwas in X"-Konstruktion verboten:** `etwas in seinem Nacken`, `etwas in ihrem Sehen`, `etwas in seiner Brust` — Erzähler-Glosse statt Körper-Wahrnehmung. Stattdessen direkt: `eine Kälte legte sich auf seinen Nacken`, `ihr Sehen verrutschte`, `in seiner Brust schlug etwas`. Subtext trägt sich durch Körper, nicht durch "etwas in X".
21. **Generische Stand-in-Wörter beim Komprimieren vermeiden:** Wenn beim Streichen eines Tics (halb X, Puls, etc.) generische Wörter wie `kaum sichtbar`, `merklich`, `winzig`, `etwas` als Ersatz auftauchen, verliert der Beat Konkretheit (Bardugo-Disziplin-Bruch). Lieber konkretes Maß ohne "halb" einsetzen (`einen Zoll`, `Haarbreit`, `eine Spanne`, `einen Takt`, `eine Fingerbreite`).

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
- "nicht X — sondern Y" / "nicht X, sondern Y" / "nicht X, Y" — **KEINE Schwelle, Pflicht-Pruefung pro Einsatz**: jedes Vorkommen muss begründbar sein (Kontrast trägt einen Beat). Default = streichen oder positiv umformulieren. Stand 2026-04-26.
- "wie etwas das..." / "wie ein..." Vergleiche — **max 2x** (verschaerft April 2026)
- Adverb-Tags ("sagte er wuetend") — max 0
- Denk-Tags ("sie dachte, dass") — max 0
- Direkte Emotionsbenennung ("er war traurig", "sie fuehlte Wut") — max 0
- Flashback-Rampe ("sie erinnerte sich an den Tag") — max 0
- Praemature Ahnung ("sie wusste noch nicht, dass") — max 0
- Komma-Listen mit 3+ Substantivphrasen ohne Verb — markieren
- "und"-Ketten >3 pro Satz — markieren
- Saetze ueber Figur-Limit (Alphina ~40W, Sorel ~50W, Vesper ~20W, Maren ~35W)
- Stakkato-Passagen / Hammerschlag-Fragmente — **KEINE Schwelle, Pflicht-Pruefung pro Einsatz**: jedes Stakkato muss explizit als notwendiges Stilmittel begründet sein (Schock, Bruch, Empörung). Default = umformulieren zu vollständigem Satz. Stand 2026-04-26.
- Personifikationen: max ~8 pro Kapitel
- POV-Vokabular-Bruch (Alphina sagt "Dunst" statt "Nebel" o.ae.)
- **"halb X"-Pseudo-Praezision (NEU 2026-04-26):** Grep auf `halbe(r/s)? (Sekunde|Atemzug|Schritt|Zoll|Millimeter|Zentimeter|Meter|Lächeln|Kopf|Takt|Punkt|Strich|Finger|Armlänge|Grad|Minute|Stunde|Haar)` — KEINE Schwelle, jedes Vorkommen Pflicht-Pruefung. Default = streichen/ersetzen. Erlaubt nur bei zwingender Funktion.
- **Metrische Maßeinheiten verboten (Anglizismus, Epoche-Bruch):** Grep auf `Millimeter|Zentimeter|Meter|Kilometer` — max 0. Stattdessen: Linie, Daumen/Fingerbreite, Spanne, Fuß, Elle, Schritt, Klafter, Meile.
- **Realweltliche Monatsnamen verboten:** Grep auf `Januar|Februar|März|Maerz|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember|Märzlicht|Märzwind|Märzregen|Märzluft` — max 0. Stattdessen Welt-Monate (Eismond, Saatmond, Blütenmond etc.) oder Jahreszeit.
- **"Puls" abstrakt verboten (Klischee-Reflex):** Grep auf `\bPuls\b|Pulsschlag` — alle Treffer markieren außer `Quellenpuls` (Canon erlaubt). Stattdessen Körperstelle (Halsschlagader, Handgelenk, Kehle) oder konkretes Verb (Herzschlag, Schlag in den Adern).
- **"etwas in X"-Konstruktion verboten:** Grep auf `etwas in (seinem|ihrem|seiner|ihrer) (Brust|Nacken|Sehen|Brustkorb|Rücken|Hals|Kopf|Bauch|Magen)` — max 0. Stattdessen direkter Körper-Beat.
- **Generische Stand-in-Wörter beim Tic-Streichen (Council-Risiko):** Wenn ein "halb X" oder "Puls" durch `kaum sichtbar`, `merklich`, `winzig`, `etwas` ersetzt wurde, prüfen ob konkrete Maßangabe (`einen Zoll`, `Haarbreit`, `eine Spanne`, `einen Takt`) besser wäre. Bardugo-Disziplin verlangt Konkretheit.
- **Konkretheits-Check (NEU):** Absaetze zaehlen, bei wie vielen KEIN benanntes Material (Kupfer, Leinen, Kalk, Messing, Birkenrinde, Tusche, Talg...) vorkommt — bei mehr als 20% aller Absaetze: FINDING "zu abstrakt"
- **Abstrakta-Dichte (NEU):** Grep auf "Stille", "Kaelte", "Schwere", "Leere", "Ferne", "Dunkelheit", "Ewigkeit", "Unheimliches", "Abgrund" — pro Absatz max 1, pro Kapitel max ~15 gesamt; bei >20: FINDING
- **Abstrakta-Stapel (NEU):** Grep auf Muster "der/die/das [Abstraktum] des/der [Abstraktum]" ("die Stille des Abgrunds", "die Kaelte der Leere") — max 0

Output: Tabelle mit Spalten | Zeile | Typ | alt (Original-Zitat, woertlich, max 15 Woerter) | neu (Fix-Vorschlag, vollstaendige Ersetzung) | warum (1 kurzer Satz) |. Wenn das Finding ein „streichen" ist: in der neu-Spalte explizit `[STREICHEN]` schreiben. Keine vagen „umformulieren"-Phrasen — entweder konkreter Fix-Vorschlag oder STREICHEN.

Max 1.5k Token. Verdikt: BESTANDEN / NICHT BESTANDEN.
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

**Output-Format (zwingend):**
- Verdikt: BESTANDEN / NICHT BESTANDEN
- Findings als Tabelle | Zeile | alt (Original-Zitat, woertlich) | neu (Fix-Vorschlag) | warum |
- 3-5 Eintraege. Wenn streichen: `[STREICHEN]` in der neu-Spalte. Keine vagen Empfehlungen — pro Finding ein konkret einsetzbarer Satz.

Max 1k Token.
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

**Output-Format (zwingend):**
- Verdikt (in-character, 2-3 Saetze)
- Findings als Tabelle | Zeile | alt (Original-Zitat) | neu (konkreter Fix-Vorschlag) | warum |
- 3-5 Eintraege. Wenn streichen: `[STREICHEN]` in der neu-Spalte. Wenn ein Finding kein Aenderungs-Vorschlag ist sondern Lob/Kritik ohne Fix (z.B. „Power-Dynamik traegt"), das in einer separaten Liste „Beobachtungen ohne Fix" am Ende.

Max 1k Token.
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

**Output-Format (zwingend):**
- Verdikt (in-character, 2-3 Saetze)
- Findings als Tabelle | Zeile | alt (Original-Zitat) | neu (konkreter Fix-Vorschlag) | warum |
- 3-5 Eintraege. Wenn streichen: `[STREICHEN]` in der neu-Spalte. Lob/Beobachtungen ohne Fix in einer separaten Liste am Ende.

Max 1k Token.
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

**Output-Format (zwingend):**

Tabelle A — Aenderungs-Vorschlaege (Streichungen + Umformulierungen zusammen):

| Zeile | alt (woertliches Zitat) | neu (Fix-Vorschlag oder `[STREICHEN]`) | warum (Autorin-Perspektive, 1 Satz) |
|-------|-------------------------|----------------------------------------|--------------------------------------|

Tabelle B — Bleibt (besonders starke Passagen):

| Zeile | Passage | warum stark |
|-------|---------|-------------|

3-6 Eintraege pro Tabelle. Jede neu-Spalte muss einen einsetzbaren Satz enthalten — keine vagen „verdichten/umstrukturieren"-Floskeln. Bei Streichung explizit `[STREICHEN]` schreiben.

Max 2.5k Token.
```

## Phase 6: Konsolidierter Bericht — Master-Tabelle alt/neu

**Format-Regel (zwingend):** Jeder Aenderungs-Vorschlag aus Stil-Check, Stilkritiker, Dark-Romance, Romantasy oder Autorin-Durchgang wird dem Autor in **einer einzigen konsolidierten Tabelle** gezeigt — mit `alt`-Zitat und `neu`-Vorschlag direkt nebeneinander, sodass der Autor jeden Eintrag mit „ok/skip" akzeptieren oder verwerfen kann.

Format der Master-Tabelle:

| # | Quelle | Zeile | alt (woertliches Zitat) | neu (Fix oder `[STREICHEN]`) | warum |
|---|--------|-------|-------------------------|------------------------------|-------|

- **Quelle:** `Stil-Check`, `Stilkritiker`, `Dark-Romance`, `Romantasy`, `Autorin-A` (streichen), `Autorin-B` (umformulieren).
- **Konsolidierung:** Wenn mehrere Subagenten denselben Satz anfassen, einen Eintrag mit beiden Quellen (z.B. `Stilkritiker + Autorin-A`) und dem strengeren Vorschlag (Streichen schlaegt Umformulierung).
- **Dedup:** Wenn zwei Vorschlaege denselben Satz mit unterschiedlichem `neu` betreffen, beide Eintraege zeigen mit Hinweis „Konflikt — Autor entscheidet".

**Zusaetzlich vor der Master-Tabelle anzeigen:**

1. Verdikt-Block: Pro Subagent eine Zeile mit Verdikt + Score (falls vorhanden)
2. Autorin-„bleibt"-Liste (Tabelle B aus Phase 5.5) — Lob als Kontext
3. Beobachtungen ohne Fix (aus Council-Subagenten) — separate kurze Liste, nicht in der Master-Tabelle

**Frage am Ende:** „Soll ich die Findings der Reihe nach einarbeiten? Du kannst pro Eintrag `ok`, `skip`, oder einen eigenen Fix schreiben."

**Wichtig:** Die Master-Tabelle ist die einzige Stelle wo Aenderungen vorgeschlagen werden — keine prosaische Zusammenfassung der Findings davor, kein Aufweichen durch „insgesamt war das Kapitel solide". Tabelle, dann Frage. Sonst nichts.

## Phase 7: Fixes-Loop

In derselben Opus-Session:
- Fixes einarbeiten (Edit-Tool wo moeglich, Write nur fuer ganze Szenen-Neufassungen)
- `wc -w` nach jedem Fix
- Re-deploy nach groesseren Fix-Runden
- Loop bis Stil-Check + Council OK + Autor bestaetigt

## Phase 8: Status `final` + Deploy + kapitel-summaries.md nachziehen

Seit 2026-04-26 setzt /ausarbeitung direkt `final` — der Zwischenstatus `lektorat` ist entfallen, weil das absatzweise Schreiben mit Mini-Council bereits Final-Niveau liefert. Autor-Mikro-Edits nach Online-Lesen laufen ueber `/lektorat-fix` auf `final`-Kapiteln.

### 8.1 kapitel-summaries.md ergaenzen (PFLICHT)

Bevor `final` gesetzt wird, einen Eintrag fuer das Kapitel in `buch/kapitel-summaries.md` schreiben — damit spaetere `/entwurf`-Sessions wissen, was passiert ist. Format wie bei den vorherigen Eintraegen (3-6 Saetze, was passiert, Wissensstand der POV-Figur am Ende, neue Tschechow-Waffen).

### 8.2 status.json aktualisieren

- `state: "final"`
- `datei: "{ID}-{figur}.md"`
- `woerter: <wc -w>`
- `text`-Plot-Snippet aktualisieren (1-3 Saetze, was passiert)

### 8.3 Handoff-File loeschen

```bash
rm buch/kapitel/{ID}-handoff.md
```

Das Handoff-File wird nicht mehr fuer `/lektorat-fix` ueberschrieben — es wird gelöscht. Bei Mikro-Edits braucht es kein Handoff (Skill liest nur das Kapitel + Positioning + status.json).

### 8.4 Commit + Deploy

```bash
git add buch/status.json buch/kapitel-summaries.md buch/kapitel/{ID}-{figur}.md
git rm buch/kapitel/{ID}-handoff.md
git commit -m "feat({ID}): Final — {Figur}, {Wörter}W, Council bestanden"
git push
ssh adrian@adrianphilipp.de "cd ~/apps/Alphina-Static && git pull && bash generate-lesen.sh"
```

Status: `final`. Autor liest online.

## Phase 9: Harter Stop

Zeige dem Autor:

> KAPITEL FINAL. Status: final. Wörter: {N}. Council bestanden.
>
> Diese Session ist abgeschlossen.
>
> Falls beim Online-Lesen Mikro-Fixes auffallen:
> 1. Neue Session: `claude --model sonnet` (oder haiku)
> 2. `/lektorat-fix {ID}` — laedt minimal Kontext, Edit-only, kein Council.
>
> Diese Session schreibt jetzt nichts mehr.

**WICHTIG:** Nach Phase 9 NICHT weiterarbeiten. Auf Folgefragen: "Diese Phase ist abgeschlossen. Bitte starte eine /lektorat-fix-Session sobald du Feedback hast."

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
