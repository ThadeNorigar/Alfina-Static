# /buch-end — Session beenden

Beende die aktuelle Arbeitssession am Buchprojekt "Der Riss" mit Summary und Persistierung.

## Ablauf

### 1. Session reviewen

Gehe den Konversationsverlauf durch und extrahiere:

- **Bearbeitet:** Welche Kapitel/Szenen/Bibel-Teile wurden bearbeitet?
- **Entscheidungen:** Welche Welt-/Plot-/Stil-Entscheidungen wurden getroffen?
- **Offene Threads:** Was ist noch offen?
- **Nächste Schritte:** Was steht als nächstes an?
- **Geänderte Dateien:** Aus `git status -s`

### 2. Session-Log schreiben

Datei: `sessions/{YYYY-MM-DD}.md`

Falls nicht existiert, neu anlegen. Sonst appendieren.

```markdown
## Session End {HH:MM}

### Bearbeitet
- Was wurde gemacht

### Entscheidungen
- Welt/Plot/Stil-Festlegungen

### Kapitel-Bewegungen
- 02 entwurf → council
- I1 szenenplan → entwurf
- (nur falls Status-Änderungen in dieser Session)

### Offene Threads
- Was noch zu tun ist

### Nächste Schritte
- [ ] Konkrete Action Items

### Dateien geändert
- `buch/00-welt.md` — Was geändert wurde
- `buch/kapitel/02-*.md` — Was geändert wurde
```

### 3. State aktualisieren

Datei: `state/current.md`

- **Recent Context:** 1-2 Sätze zur aktuellen Session
- Alte Einträge älter als 4 Wochen entfernen
- Aktueller Fokus (z.B. "Buch 1 Akt II — Kapitel 15-18 im Entwurf")

### 4. Kapitel-Status prüfen

```bash
cat buch/status.json | python -c "import json, sys; d = json.load(sys.stdin); ..."
```

Zeige Übersicht: Wie viele Kapitel sind in welchem Status?

### 5. Kaskaden-Check

Falls in dieser Session die **Weltbibel** (`00-welt.md`), **Storyline** (`00-storyline.md`), **Magie-System** (`10-magie-system.md`) oder **Charakter-Dossiers** geändert wurden:

> ⚠ **Kaskaden-Pflicht:** Prüfe ob betroffene Aktpläne, Szenen und Kapitel noch konsistent sind.

Liste die betroffenen Ebenen auf (Aktpläne → Status → Szenen → Kapitel).

### 6. Git Commit

NUR wenn der Autor explizit zustimmt:

```bash
git add sessions/ state/ buch/
git commit -m "chore(session): end $(date +%Y-%m-%d) — {Kurzbeschreibung}"
```

NICHT automatisch pushen.

### 7. Prompt für nächste Session

Generiere einen kompakten Prompt den der Autor in eine neue Session kopieren kann:

```markdown
## {Thema für nächste Session}

### Kontext
{Was ist passiert, wo stehen wir}

### Was zu tun ist
1. {Nächster Schritt}
2. {...}

### Wichtige Regeln (Erinnerung)
- Umlaute verwenden
- Deutsch
- Stilverbote aus CLAUDE.md beachten
- Bibel-Check vor Kapitel-Arbeit
```

### 8. Output

```markdown
### Der Riss — Session End

**Bearbeitet:** {Kurzfassung}

**Kapitel-Status:**
| Status | Anzahl | Wörter |
|--------|--------|--------|
| ...    | ...    | ...    |

**Offene Threads:**
- ...

**Kaskaden-Check:** {OK / betroffene Ebenen}

**Log:** `sessions/{YYYY-MM-DD}.md`

---

### Prompt für nächste Session
{Der generierte Prompt}
```

## Regeln

- **Kompakt.** Tabellen und Listen.
- **Buch-zentriert.** Kein Code-Sync, kein K2Memory, kein Beads — das ist ein Autorenprojekt, keine Software.
- **Kaskaden-Warnung prominent.** Wenn Bibel geändert → User MUSS sehen was das invalidiert.
- **Prompt fuer naechste Session ist Pflicht** — damit der Autor ohne Reibung weitermachen kann.
- **Nie eigenmaechtig Kapitel-Status auf "lektorat" setzen** — das ist Autor-Gate.

$ARGUMENTS
