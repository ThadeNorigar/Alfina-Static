#!/bin/bash
# Generiert /lesen/N/index.html für jedes Kapitel das eine 'datei'-Property hat.
# Liest buch/status.json, erstellt Verzeichnisse, kopiert _reader.html.
# Aufruf: ./generate-lesen.sh (im Projekt-Root)

set -e
cd "$(dirname "$0")"

TEMPLATE="lesen/_reader.html"
STATUS="buch/status.json"

if [ ! -f "$TEMPLATE" ]; then
  echo "FEHLER: $TEMPLATE nicht gefunden"
  exit 1
fi

if [ ! -f "$STATUS" ]; then
  echo "FEHLER: $STATUS nicht gefunden"
  exit 1
fi

# Extract all chapter IDs that have a "datei" field from status.json
# Uses python for reliable JSON parsing
# Find Python
for p in python3 python /c/Users/micro/AppData/Local/Programs/Python/Python310/python; do
  if command -v "$p" &>/dev/null && "$p" -c "import json" 2>/dev/null; then
    PYTHON="$p"
    break
  fi
done
if [ -z "$PYTHON" ]; then
  echo "FEHLER: Python nicht gefunden"
  exit 1
fi

$PYTHON -c "
import json, sys, os

with open('$STATUS', encoding='utf-8') as f:
    data = json.load(f)

template = open('$TEMPLATE', encoding='utf-8').read()
count = 0

NEEDS_DATEI = {'entwurf', 'council', 'checked', 'lektorat', 'final'}
warnings = []

for buch_key in ['buch1', 'buch2', 'buch3']:
    buch = data.get(buch_key)
    if not buch:
        continue
    for kap_id, ch in buch.get('kapitel', {}).items():
        status = ch.get('status', '')
        has_datei = bool(ch.get('datei'))
        if status in NEEDS_DATEI and not has_datei:
            warnings.append(f'  WARNUNG: {buch_key}/{kap_id} hat status=\"{status}\" aber kein datei-Feld!')
        if not has_datei:
            continue
        # URL slug: '01' -> '1', 'I1' -> 'I1'
        if kap_id.startswith('I'):
            slug = kap_id
        else:
            slug = str(int(kap_id))

        dir_path = os.path.join('lesen', slug)
        os.makedirs(dir_path, exist_ok=True)

        out_path = os.path.join(dir_path, 'index.html')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(template)
        count += 1

if warnings:
    print('\\n'.join(warnings))
print(f'generate-lesen: {count} Kapitel-Seiten generiert')
" 2>&1
