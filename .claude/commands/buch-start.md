# /buch-start — Session starten

Starte eine neue Arbeitssession am Buchprojekt "Der Riss".

## Ablauf

### 1. Kontext laden

Lies folgende Dateien und fasse den aktuellen Stand zusammen:

- `state/current.md` — Letzter Stand
- `sessions/` — Letzte Session-Datei (neueste nach Datum)
- `buch/status.json` — Kapitel-Übersicht (wie viele pro Status, Gesamtwörter)

### 2. Offene Threads prüfen

Aus der letzten Session: Was ist offen? Was war der nächste Schritt?

### 3. Werkzeuge prüfen

Falls der Moragh-Karten-Editor benötigt wird:
```bash
python moragh-server.py
```
→ http://localhost:8090

### 4. Ausgabe

```markdown
### Der Riss — Session Start

**Letzter Stand:** {1-2 Sätze aus state/current.md}

**Kapitel-Status:**
| Status | Anzahl | Wörter |
|--------|--------|--------|
| final  | N      | N      |
| ...    | ...    | ...    |

**Offene Threads:**
- [ ] Thread 1
- [ ] Thread 2

**Vorgeschlagener Fokus:** {Was als nächstes sinnvoll wäre}
```

### 5. Auf Autor warten

NICHT sofort losarbeiten. Frage: "Womit sollen wir starten?"

$ARGUMENTS
