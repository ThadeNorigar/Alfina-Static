"""
Shift all MZ values in zeitleiste.json by +3635.
MZ 0 (old: Durchgang der Vier) becomes MZ 3635.
MZ 0 (new) = Besiedelung von Moragh.

Handles:
- Numeric mz fields (int/float)
- German thousand separators in strings (MZ -3.635 = minus dreitausendsechshundertfuenfunddreissig)
- ~ prefix (MZ ~-4)
- Ranges (MZ -4 bis -3)
"""
import json, re

SHIFT = 3635
path = 'buch/zeitleiste.json'

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

data['meta']['zeitrechnung']['mz_null'] = 'Besiedelung von Moragh'

num_count = 0

def shift_num(val):
    global num_count
    if isinstance(val, (int, float)):
        num_count += 1
        result = val + SHIFT
        if result == int(result):
            return int(result)
        return round(result, 4)
    return val

def parse_german_number(s):
    """Parse a German-formatted number: 3.635 = 3635, 0,25 = 0.25"""
    # Remove thousand separators (dots followed by 3 digits)
    cleaned = re.sub(r'\.(\d{3})', r'\1', s)
    # Replace comma decimal with dot
    cleaned = cleaned.replace(',', '.')
    return float(cleaned)

def format_mz_number(n):
    """Format MZ number in German style"""
    if n == int(n):
        n = int(n)
        # Add thousand separators for large numbers
        if abs(n) >= 1000:
            s = f'{abs(n):,}'.replace(',', '.')
            return f'-{s}' if n < 0 else s
        return str(n)
    else:
        # Decimal: use comma
        s = f'{n:.2f}'.rstrip('0').rstrip('.')
        s = s.replace('.', ',')
        return s

def shift_mz_string(s):
    """Shift MZ values in string fields"""
    if not isinstance(s, str) or 'MZ' not in s:
        return s

    # Match MZ followed by optional ~ and a number (with optional German thousand seps and decimal comma)
    # Pattern: MZ<space>~?<number>
    # Number can be: -3.635 (thousand sep) or -0,25 (decimal comma) or -4 (plain)
    def replace_match(m):
        prefix = m.group(1)  # "MZ " or "MZ ~"
        numstr = m.group(2)  # "-3.635" or "-0,25" or "-4"
        try:
            num = parse_german_number(numstr)
            new_num = num + SHIFT
            return prefix + format_mz_number(new_num)
        except ValueError:
            return m.group(0)

    # Match: MZ followed by optional space, optional ~, then a number
    return re.sub(r'(MZ\s*~?)([-]?\d[\d.,]*)', replace_match, s)

def process_event(ev):
    if 'mz' in ev and isinstance(ev['mz'], (int, float)):
        ev['mz'] = shift_num(ev['mz'])

for monat in data['monate']:
    if 'mz' in monat:
        monat['mz'] = shift_mz_string(monat['mz'])
    if 'label' in monat:
        monat['label'] = shift_mz_string(monat['label'])

    events = monat.get('events', {})

    if 'sync' in events:
        sync = events['sync']
        if 'mz' in sync:
            sync['mz'] = shift_mz_string(sync['mz'])
        if 'label' in sync:
            sync['label'] = shift_mz_string(sync['label'])

    for ev in events.get('thalassien', []) + events.get('moragh', []):
        process_event(ev)

# Schema examples
for typ_name, typ_def in data['meta'].get('schema', {}).items():
    if isinstance(typ_def, dict) and 'beispiel' in typ_def:
        bsp = typ_def['beispiel']
        if 'mz' in bsp and isinstance(bsp['mz'], (int, float)):
            bsp['mz'] = shift_num(bsp['mz'])

# Also shift in zeitrechnung strings
zr = data['meta']['zeitrechnung']
if 'monat' in zr:
    zr['monat'] = shift_mz_string(zr['monat'])

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Shifted {num_count} numeric MZ values by +{SHIFT}')

# Validate
json.load(open(path, encoding='utf-8'))
print('JSON valid!')

# Spot checks
data2 = json.load(open(path, encoding='utf-8'))
for m in data2['monate'][:3]:
    print(f"  {m['label']}  |  {m.get('mz','')}")
for m in data2['monate']:
    for ev in m['events'].get('thalassien', []) + m['events'].get('moragh', []):
        if 'Besiedelung' in (ev.get('titel') or ''):
            print(f"  Besiedelung: mz={ev['mz']}")
        if 'Vier' in (ev.get('titel') or '') and 'nach Moragh' in (ev.get('titel') or ''):
            print(f"  Durchgang: mz={ev['mz']}")
