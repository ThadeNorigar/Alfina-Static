import json
data = json.load(open('buch/zeitleiste.json', encoding='utf-8'))
for monat in data['monate']:
    thal_portals = [e for e in (monat['events'].get('thalassien') or []) if 'portal' in (e.get('typen') or [])]
    moragh_portals = [e for e in (monat['events'].get('moragh') or []) if 'portal' in (e.get('typen') or [])]
    if thal_portals and moragh_portals:
        print(f"=== DUPLIKAT-VERDACHT: {monat['label']} ===")
        for e in thal_portals:
            print(f"  THAL: {e.get('titel','?')}")
        for e in moragh_portals:
            print(f"  MORAGH: {e.get('titel','?')}")
        print()
