"""
Fix all monat-level tz/mz strings:
- Remove ~
- Convert decimal MZ to "Monat. Jahr MZ" format
- Fix broken ranges (unshifted values after "bis")
- Clean up TZ values
"""
import json, re, math

SHIFT = 3635
path = 'buch/zeitleiste.json'
data = json.load(open(path, encoding='utf-8'))

def mz_decimal_to_text(val):
    """Convert MZ decimal to 'Monat. Jahr' or 'Jahr' format"""
    if isinstance(val, str):
        # Parse German number
        val = val.replace('.', '').replace(',', '.')
        val = val.replace('~', '').strip()
        try:
            val = float(val)
        except:
            return val

    year = int(val)
    frac = abs(val - year)
    month = round(frac * 12)

    # Format year with thousand separator
    def fmt_year(y):
        if abs(y) >= 1000:
            return f'{abs(y):,}'.replace(',', '.')
            if y < 0:
                return '-' + fmt_year(abs(y))
        return str(y)

    ys = f'{abs(year):,}'.replace(',', '.') if abs(year) >= 1000 else str(abs(year))
    if year < 0:
        ys = '-' + ys

    if month > 0 and month < 12:
        return f'{month}. {ys}'
    return ys

# Manual corrections for each monat
fixes = {
    # (old_tz, old_mz) -> (new_tz, new_mz)
}

for m in data['monate']:
    tz = m.get('tz', '')
    mz = m.get('mz', '')
    label = m.get('label', '')

    # Remove ~ from tz
    if isinstance(tz, str):
        m['tz'] = tz.replace('~', '')

    # Remove ~ from mz
    if isinstance(mz, str):
        m['mz'] = mz.replace('~', '')

# Now fix specific values manually based on what we know
corrections = [
    # (label_contains, new_tz, new_mz)
    ('MZ 0', '-1.453.449 TZ', '0 MZ'),
    ('MZ 3.435', '-79.449 TZ', '3.435 MZ'),  # first one only
    ('3.435 bis 3.633', '-79.449 bis -249 TZ', '3.435 bis 3.633 MZ'),
    ('-249 TZ', '-249 TZ', '3.633 MZ'),
    ('0 TZ', '0 TZ', '3.634 MZ'),
    ('3630,75', '-1.149 TZ', '9. 3630 MZ'),
    ('3.631 MZ', '-1.049 TZ', '3.631 MZ'),
    ('3.631 bis', '-1.049 bis -649 TZ', '3.631 bis 3.632 MZ'),
    ('3.632 MZ', '-649 TZ', '3.632 MZ'),
    ('3.632 bis 3.634', '-649 bis 154 TZ', '3.632 bis 3.634 MZ'),
    ('MZ Monat -12', '154 TZ', '3.634 MZ'),
    ('MZ Monat -11', '154 bis 354 TZ', '3.634 MZ'),
    ('MZ Monat -6', '354 TZ', '6. 3634 MZ'),
    ('MZ Monat -5', '354 bis 485 TZ', '7. 3634 bis 10. 3634 MZ'),
    ('MZ Monat -2', '485 TZ', '10. 3634 MZ'),
    ('Buch 1', '551 TZ', '11. 3634 bis 3.635 MZ'),
    ('MZ Monat 1', '551 bis 583 TZ', '3.635 bis 1. 3635 MZ'),
    ('MZ Monat 2', '583 bis 651 TZ', '1. 3635 bis 2. 3635 MZ'),
    ('MZ Monat 3', '651 TZ', '2. 3635 bis 3. 3635 MZ'),
    ('MZ Monat 4', '651 bis 2.751 TZ', '3. 3635 bis 6. 3640 MZ'),
    ('Buch 3', '2.751 TZ', '6. 3640 MZ'),
]

for m in data['monate']:
    label = m.get('label', '')
    for (match, new_tz, new_mz) in corrections:
        if match in label:
            m['tz'] = new_tz
            m['mz'] = new_mz
            break

# Also fix sync bridges
for m in data['monate']:
    sync = m.get('events', {}).get('sync')
    if sync:
        if 'tz' in sync:
            sync['tz'] = sync['tz'].replace('~', '')
        if 'mz' in sync:
            sync['mz'] = sync['mz'].replace('~', '')

# Fix "~2 MZ-Jahre" leftover
for m in data['monate']:
    if m.get('mz') == '2 MZ-Jahre':
        m['mz'] = '3.632 bis 3.634 MZ'

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

json.load(open(path, encoding='utf-8'))
print('JSON valid! Fixed values:')
for m in data['monate']:
    print(f"  {m.get('label','')[:35]:35s} | {m.get('tz',''):25s} | {m.get('mz','')}")
