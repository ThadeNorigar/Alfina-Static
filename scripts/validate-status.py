#!/usr/bin/env python3
"""
Validator fuer buch/status.json — Pflicht-Felder, Stati, Synchronitaet.

Prueft:
  1. stati-Liste enthaelt nur die 6 erlaubten Werte
  2. Pro Buch: kapitel-Map und akte[*].kapitel-Liste sind synchron
  3. Pro Kapitel: Pflicht-Felder je nach Status
     - entwurf/entwurf-checked/entwurf-ok: entwurfs_datei muss existieren (Datei auch im FS)
     - ausarbeitung: entwurfs_datei muss existieren
     - final: datei muss existieren (im FS) UND text-Snippet darf nicht leer sein
  4. Felder zeigen auf existierende Files in buch/kapitel/

Aufruf:
  python scripts/validate-status.py             # exit 0 = OK, exit 1 = Fehler
  python scripts/validate-status.py --quiet     # nur Fehler ausgeben
  python scripts/validate-status.py --json      # JSON-Output (fuer Hooks)
  python scripts/validate-status.py --all-strict # buch2/buch3 auch strict (Default: nur Warnungen)

Default-Modus: NUR buch1 ist strict (errors blocken). buch2/buch3 sind im Konzept,
daher werden ihre Befunde als Warnungen gemeldet, nicht als Errors.
"""

import json
import sys
from pathlib import Path

ALLOWED_STATI = {
    'idee',
    'entwurf',
    'entwurf-checked',
    'entwurf-ok',
    'ausarbeitung',
    'final',
}

ENTWURFS_STATI = {'entwurf', 'entwurf-checked', 'entwurf-ok', 'ausarbeitung'}

STRICT_BUECHER = {'buch1'}  # Default: nur buch1 ist strict


def main():
    here = Path(__file__).resolve().parent.parent
    status_path = here / 'buch' / 'status.json'
    kapitel_dir = here / 'buch' / 'kapitel'

    quiet = '--quiet' in sys.argv
    json_out = '--json' in sys.argv
    all_strict = '--all-strict' in sys.argv

    errors = []
    warnings = []

    strict_buecher = {'buch1', 'buch2', 'buch3'} if all_strict else STRICT_BUECHER

    if not status_path.exists():
        errors.append(f'buch/status.json nicht gefunden ({status_path})')
        return _output(errors, warnings, quiet, json_out)

    try:
        with open(status_path, encoding='utf-8') as f:
            d = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f'buch/status.json ist kein gueltiges JSON: {e}')
        return _output(errors, warnings, quiet, json_out)

    # 1. stati-Liste
    stati = set(d.get('stati', []))
    unexpected = stati - ALLOWED_STATI
    missing = ALLOWED_STATI - stati
    if unexpected:
        errors.append(f'stati-Liste enthaelt ungueltige Werte: {sorted(unexpected)}')
    if missing:
        errors.append(f'stati-Liste fehlen Pflicht-Werte: {sorted(missing)}')

    # 2 + 3. Pro Buch
    for bk in ['buch1', 'buch2', 'buch3']:
        b = d.get(bk)
        if not b:
            continue

        is_strict = bk in strict_buecher
        bucket = errors if is_strict else warnings
        prefix = '' if is_strict else '[konzept] '

        # Synchronitaet akte vs. kapitel-map
        akte_ids = []
        for akt in b.get('akte', []):
            akte_ids.extend(akt.get('kapitel', []))
        akte_set = set(akte_ids)
        map_set = set(b.get('kapitel', {}).keys())

        only_in_akte = akte_set - map_set
        only_in_map = map_set - akte_set
        if only_in_akte:
            bucket.append(
                f'{prefix}{bk}: in akte-Liste aber nicht in kapitel-Map: {sorted(only_in_akte)}'
            )
        if only_in_map:
            bucket.append(
                f'{prefix}{bk}: in kapitel-Map aber nicht in akte-Liste: {sorted(only_in_map)}'
            )

        # Duplikate in akte-Liste (immer error, das ist Bug)
        if len(akte_ids) != len(akte_set):
            from collections import Counter
            dups = [k for k, c in Counter(akte_ids).items() if c > 1]
            errors.append(f'{bk}: Duplikate in akte-Liste: {dups}')

        # Pflicht-Felder pro Kapitel
        for kid, ch in b.get('kapitel', {}).items():
            status = (ch.get('status') or '').strip()
            ref = f'{prefix}{bk}/{kid} (status={status or "?"})'

            if not status:
                warnings.append(f'{ref}: kein status-Feld')
                continue

            if status not in ALLOWED_STATI:
                bucket.append(f'{ref}: ungueltiger Status "{status}"')
                continue

            # POV-Feld sollte da sein (außer idee)
            if status != 'idee' and not ch.get('pov'):
                warnings.append(f'{ref}: pov-Feld fehlt')

            # entwurf-Stati: entwurfs_datei muss da sein
            if status in ENTWURFS_STATI:
                ed = ch.get('entwurfs_datei')
                if not ed:
                    bucket.append(f'{ref}: entwurfs_datei fehlt')
                else:
                    fp = kapitel_dir / ed
                    if not fp.exists():
                        bucket.append(
                            f'{ref}: entwurfs_datei "{ed}" existiert nicht im Filesystem'
                        )

            # ausarbeitung + final: datei muss existieren
            if status in {'ausarbeitung', 'final'}:
                df = ch.get('datei')
                if not df and status == 'final':
                    bucket.append(f'{ref}: datei-Feld fehlt (Pflicht ab final)')
                elif df:
                    fp = kapitel_dir / df
                    if not fp.exists():
                        bucket.append(
                            f'{ref}: datei "{df}" existiert nicht im Filesystem'
                        )

            # final: text-Snippet + woerter
            if status == 'final':
                text = (ch.get('text') or '').strip()
                if not text:
                    bucket.append(f'{ref}: text-Plot-Snippet fehlt oder leer')
                elif len(text) < 30:
                    warnings.append(
                        f'{ref}: text-Snippet sehr kurz ({len(text)} Zeichen) — Sinnvoll?'
                    )

                woerter = ch.get('woerter', 0) or 0
                if woerter == 0:
                    warnings.append(f'{ref}: woerter-Feld ist 0 (Soll: gemessene Wortzahl)')
                elif woerter < 1400 or woerter > 9000:
                    warnings.append(
                        f'{ref}: woerter={woerter} liegt außerhalb 1400-9000 — Plausibilitaet pruefen'
                    )

    return _output(errors, warnings, quiet, json_out)


def _output(errors, warnings, quiet, json_out):
    if json_out:
        print(json.dumps({
            'ok': not errors,
            'errors': errors,
            'warnings': warnings,
        }, ensure_ascii=False, indent=2))
        return 0 if not errors else 1

    if errors:
        print(f'\n[validate-status] {len(errors)} FEHLER:', file=sys.stderr)
        for e in errors:
            print(f'  X {e}', file=sys.stderr)

    if warnings and not quiet:
        print(f'\n[validate-status] {len(warnings)} Warnungen:', file=sys.stderr)
        for w in warnings:
            print(f'  ! {w}', file=sys.stderr)

    if not errors:
        if not quiet:
            print('[validate-status] OK — buch/status.json sauber.')
        return 0
    return 1


if __name__ == '__main__':
    sys.exit(main())
