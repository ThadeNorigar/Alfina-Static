"""Move TZ/MZ prefix to suffix in monat-level string fields."""
import json, re

path = 'buch/zeitleiste.json'
data = json.load(open(path, encoding='utf-8'))

def prefix_to_suffix(s):
    if not isinstance(s, str):
        return s
    # "TZ -79.449" -> "-79.449 TZ"
    # "MZ ~3.633" -> "~3.633 MZ"
    # "TZ ~-1.149" -> "~-1.149 TZ"
    # "MZ 3.435 bis 3.633" -> "3.435 bis 3.633 MZ"
    # "Buch 1 — MZ Monat -1 bis 0" -> leave as-is (label text)
    s = re.sub(r'^TZ\s+(.+)$', r'\1 TZ', s)
    s = re.sub(r'^MZ\s+(.+)$', r'\1 MZ', s)
    return s

count = 0
for monat in data['monate']:
    for key in ['tz', 'mz']:
        if key in monat and isinstance(monat[key], str):
            old = monat[key]
            new = prefix_to_suffix(old)
            if old != new:
                monat[key] = new
                count += 1

    # Also sync bridges
    sync = monat.get('events', {}).get('sync', {})
    for key in ['tz', 'mz']:
        if key in sync and isinstance(sync[key], str):
            old = sync[key]
            new = prefix_to_suffix(old)
            if old != new:
                sync[key] = new
                count += 1

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

json.load(open(path, encoding='utf-8'))
print(f'Fixed {count} fields. JSON valid!')

# Spot check
for m in data['monate'][:5]:
    print(f"  tz: {m.get('tz','')}  |  mz: {m.get('mz','')}")
