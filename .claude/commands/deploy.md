# /deploy — Quick Deploy

Kapitel zusammenbauen, committen, deployen.

## Ablauf

1. Szenen zusammenbauen:
```bash
# Alle Szenen-Dateien des aktuellen Kapitels zusammenführen
echo "# Kapitel X — Figur" > buch/kapitel/XX-figur.md
cat buch/kapitel/XX-szene*.md >> buch/kapitel/XX-figur.md
wc -w buch/kapitel/XX-figur.md
```

2. Commit + Push + Server Pull:
```bash
git add -A
git commit -m "feat: Kapitel XX — [Figur], [Wörter]W"
git push
ssh adrian@adrianphilipp.de "cd ~/apps/Alphina-Static && git pull"
```

3. Verify:
```bash
curl -sI https://alphina.net/lesen/ | head -3
```

$ARGUMENTS
