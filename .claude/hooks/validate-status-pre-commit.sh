#!/usr/bin/env bash
# PreToolUse-Hook auf Bash. Filtert auf "git commit"-Commands.
# Ruft scripts/validate-status.py auf — bei Fehlern: blockt den Commit
# (exit 2 + JSON mit decision: deny).
#
# Input: JSON via stdin mit tool_input.command.

input=$(cat)
cmd=$(echo "$input" | jq -r '.tool_input.command // empty' 2>/dev/null)

# Nur bei git commit reagieren
case "$cmd" in
  *"git commit"*) ;;
  *) exit 0 ;;
esac

# Skip wenn nur status.json-loses commit (z.B. .gitignore-Aenderung)
# - hier nicht filtern, lieber zu oft pruefen als zu selten

# Projekt-Root
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

if [ ! -f "$ROOT/scripts/validate-status.py" ]; then
  echo "[validate-status-hook] Validator-Skript nicht gefunden — skip" >&2
  exit 0
fi

# Validator ausfuehren
output=$(cd "$ROOT" && python scripts/validate-status.py 2>&1)
status=$?

if [ $status -eq 0 ]; then
  # Sauber — silent durch
  exit 0
fi

# Fehler — blocken. Output an stderr fuer Claude/User.
echo "" >&2
echo "🛑 [validate-status] BLOCKING: buch/status.json hat Fehler." >&2
echo "" >&2
echo "$output" >&2
echo "" >&2
echo "→ Erst die Fehler beheben, dann erneut commiten." >&2
echo "→ Manuell pruefen: python scripts/validate-status.py" >&2
echo "→ Notfall-Bypass: HOOK_SKIP_VALIDATE_STATUS=1 git commit ..." >&2
echo "" >&2

# Notfall-Bypass via Env-Variable
if [ "$HOOK_SKIP_VALIDATE_STATUS" = "1" ]; then
  echo "[validate-status-hook] Bypass aktiv (HOOK_SKIP_VALIDATE_STATUS=1) — durchgewunken" >&2
  exit 0
fi

# exit 2 in PreToolUse blockt das Tool
exit 2
