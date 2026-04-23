# /figuren-check — Logik/Plausibilität-Check pro Figur mit Subagenten

Parallele Explore-Agenten prüfen jede Haupt-/Nebenfigur auf Wissens-Lücken, Premature Doubt, zeitliche/räumliche Logik, Charakterkonsistenz, Plot-Lücken und "Hä?"-Momente über alle Kapitel, in denen die Figur auftaucht.

## Input

`$ARGUMENTS`:
- Leer oder `alle` — alle 8 Standard-Agenten parallel (Alphina, Sorel, Vesper, Maren, Runa, Elke+Vorgänger, Varen, Zeitgenossen-Nebenfiguren)
- Figurname (z.B. `alphina`, `varen`, `nebenfiguren`) — nur diese Figur
- Mehrere Namen komma-getrennt (z.B. `sorel,vesper`)

## Phase 0: Vorbereitung

1. Canon-Grundlage laden:
   - `buch/00-welt.md`, `buch/00-storyline.md`, `buch/00-positioning.md`
   - `buch/00-zeitrechnung.md` (TZ/MZ-Kalender, Anker)
   - `buch/10-magie-system.md` (Resonanz, Schemen, Varen)
   - `buch/02-stilregeln-v2.md` (Premature Doubt, Cross-POV-Regel)
   - `buch/kapitel-ton-referenzen.md`
   - Memory-Canons (`CLAUDE.md`-Top + MEMORY.md-Links)
2. Status-Stand holen: `python scripts/kapitel-kontext.py B1-K{NN} --phase lektorat` (pro Hotspot-Kapitel)
3. Entscheiden welche Figuren gescannt werden (laut Argument).

## Phase 1: Parallele Agenten starten

Pro Figur genau **ein** Explore-Agent (thoroughness "very thorough"), alle in einem Message-Block parallel. Prompt pro Figur folgt dem Template unten.

**Standard-Figuren-Set:**

| Key | Rolle | POV-Kapitel (final) | Auftritte in Fremd-POV |
|---|---|---|---|
| alphina | Haupt | K1, K5, K9, K12, K15, K19, K21, K23, K24 | K11, K13, K17-K22, K25 |
| sorel | Haupt | K2, K6, K10, K12, K13, K16, K18 | K19, K21, K23, K24 |
| vesper | Haupt | K3, K7, K11, K18 | K14, K17, K19, K20, K24 |
| maren | Haupt | K4, K8, K14, K17, K20, K22 | K19, K24 |
| runa | Nebenfigur + K25-POV | K25 (entwurf-ok) | K5, K9, K11, K15, K22-K24 |
| elke+vorgänger | Manuskript-POV + Canon | I1, I2, I3 | K9, K20, K24 (Manuskript) |
| varen | Antagonist | — | I3-Ende, K21 (Schem-Agent), K24, K35+ |
| nebenfiguren | Zeitgenossen in Vael | — | Jara, Esther, Edric, Tohl, Halvard, Henrik, Anker-Wirt, Magd |

## Phase 2: Prompt-Template pro Figur

Jeder Agent bekommt ein Prompt mit diesen Blöcken:

### 1. Auftrag (identisch)

```
Du bist Logik-Prüfer für Buch 1 "Der Riss" (Dark Romantasy, 3. Person nah/Präteritum).
Fokus: {FIGUR}.

Ziel: Jede Ungenauigkeit, jede Unlogik finden. Alles wo eine Leserin denkt:
"Hä? Woher weiß sie das? Kann nicht sein. Wurde nie erwähnt. Warum reagiert sie so?"

Nur Research — KEINE Edits.
```

### 2. Kernkapitel + Auftritte (figur-spezifisch)

Explizite Dateiliste, damit Agent nichts rät. Beide: POV-Kapitel + Fremd-POV-Auftritte.

### 3. Figuren-Dossier

- `buch/pov/{figur}.md` (falls vorhanden)
- `buch/00-welt.md` (Figur-Abschnitt)
- `buch/nebenfiguren/{figur}.md` (wenn Nebenfigur)

### 4. Welt/Canon-Pflicht

- `buch/00-welt.md`, `buch/00-positioning.md`, `buch/00-zeitrechnung.md`
- `buch/10-magie-system.md`, `buch/19-varen.md`
- `buch/20-moragh-talente.md`, `buch/21-moragh-gesellschaft.md`, `buch/22-moragh-figuren.md`
- `buch/02-stilregeln-v2.md`, `buch/kapitel-ton-referenzen.md`

### 5. Kontext-Extraktor

`python scripts/kapitel-kontext.py B1-K{NN} --phase lektorat` für jedes Kapitel mit Figur-Auftritt.

### 6. Figur-spezifische Kanon-Regeln

Kuratierte Memory-Auszüge (POV-Linse, Vokabular, Leitmotive, BDSM-Register, Canon-Fakten). Vollständige Liste siehe `figuren-check-memories.md` (separat, wenn länger).

### 7. Prüf-Kategorien (identisch)

1. **Wissen** (wichtigste): Woher weiß die Figur etwas? Sorel-Prinzip. Premature Doubt.
2. **Zeit/räumlich:** Plausible Standorte, Reisedauern, frühes 19. Jhd. Technik.
3. **Charakterkonsistenz:** POV-Linse, Leitmotive, Register (Sie/Du).
4. **Plot-Lücken:** Unvermittelte Gegenstände/Fakten; Tschechow-Waffen ohne Setup.
5. **Magie-Canon:** Keine Kosten. Schemen nie namentlich. "Resonanz" nie in Prosa. "Moragh" nie in Thalassien.
6. **Beziehungen:** Escalation-Kurven, Cross-POV-Konsistenz.

### 8. Output-Format (identisch)

```
Liste von Findings, pro Finding:
- Kapitel:Zeile oder Zitat
- Problem: 1-2 Sätze
- Kategorie: Wissen / Zeit / Charakter / Lücke / Magie / Beziehung
- Schwere: kritisch / mittel / klein
- Möglicher Fix: 1 Satz (optional)

Keine Einleitung. Am Ende: Summary-Counts nach Schwere.
Falls alles OK: "Keine Findings."
```

## Phase 3: Konsolidierung

Nach Rückkehr aller Agenten:

1. **Deduplizieren** — gleicher Befund in mehreren Reports zusammenführen
2. **Priorisieren** — nach Schwere (kritisch > mittel > klein) + gemeinsamer Häufigkeit
3. **Gruppieren** — nach Kategorie (Canon-Infrastruktur | Plot-Entscheidung | Text-Fix)
4. **Ablegen** als `buch/review/figuren-check-{JJJJ-MM-TT}.md` (Dateiname mit aktuellem Datum, Vorlage siehe bestehende Reports)

## Phase 4: Gate

Dem Autor zeigen:
1. Anzahl Findings nach Schwere
2. Root-Cause-Cluster (z.B. "3 Findings hängen an einer Canon-Entscheidung")
3. Empfehlung: "Welche 1-3 Canon-Klärungen lösen die meisten Findings?"
4. Frage: "Mit welchem Befund anfangen?"

**GATE: Keine Fixes ohne Autor-Freigabe pro Befund.**

## Hinweise zur Ausführung

- Agenten parallel im selben Message-Block (Performance + Kohärenz)
- `subagent_type: "Explore"` (Read-only, sicher)
- Thoroughness "very thorough"
- Output pro Agent sollte strukturiert sein (siehe Format oben) — ansonsten nachfragen
- Bei Konflikten zwischen Agenten: beide Befunde beibehalten, mit Quelle markieren

$ARGUMENTS
