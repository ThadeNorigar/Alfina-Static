#!/usr/bin/env bash
# Läuft als PostToolUse auf Write|Edit.
# Prüft Kapitel-Dateien auf "Resonanz" und erinnert an Deploy.
# Input: JSON auf stdin mit tool_input.file_path.
# Output: Warnungen/Reminder auf stderr. Nie blockieren (exit 0).

f=$(jq -r '.tool_input.file_path // .tool_response.filePath // empty' 2>/dev/null)

# Pfad-Separatoren normalisieren (Git Bash auf Windows kann beide)
f_norm="${f//\\//}"

# Nur bei Kapitel-Dateien unter buch/kapitel/*.md weiterarbeiten
case "$f_norm" in
  */buch/kapitel/*.md) ;;
  *) exit 0 ;;
esac

if [ -f "$f_norm" ]; then
  hits=$(grep -Ein 'Resonanz|resonant' "$f_norm" 2>/dev/null)
  if [ -n "$hits" ]; then
    echo "" >&2
    echo "⚠️  Canon-Verstoß: 'Resonanz' in ${f_norm##*/}" >&2
    echo "   Regel: Figuren benennen Fähigkeiten konkret (Wachstum, Licht, Zeit, Wasser)." >&2
    echo "   Fundstellen:" >&2
    echo "$hits" | sed 's/^/     /' >&2
    echo "" >&2
  fi
fi

echo "📦 Kapitel geändert: commit + git push für Deploy nicht vergessen." >&2
exit 0
