#!/usr/bin/env python3
"""
zeitrechnung.py — Konverter zwischen UZ, TZ (Thalassien) und MZ (Moragh).

Canon (buch/zeitleiste.json.meta.zeitrechnung):

  TZ (Thalassien):
    24 h/Tag, 12 Monate/Jahr, 365 Tage/Jahr (Gregorianisch).
    Monate: Eismond=Januar, Sturmmond=Februar, Saatmond=März,
    Grünmond=April, Blütenmond=Mai, Lichtmond=Juni, Glutmond=Juli,
    Erntemond=August, Herbstmond=September, Nebelmond=Oktober,
    Frostmond=November, Dunkelmond=Dezember.
    TZ 0 = Erfindung des Uhrwerks = ~1269 UZ.

  MZ (Moragh):
    26 h/Tag (Eigenrotation).
    8 Tage/Woche (Gor-Umlauf, Roter Mond).
    36 Tage/Monat = 4,5 Wochen (Nyr-Umlauf, Bleicher Mond).
    8 Monate/Jahr = 288 Tage (Orbit um das "Auge").
    Doppelflut alle 72 Tage.
    Monate:
      1 Torash  (Bogenwende,   Licht)
      2 Ashral  (Glutzeit,     Licht)
      3 Keldath (Doppelflut,   Licht)
      4 Reshvan (Ernteschluss, Licht)
      5 Dravon  (Dämmerfall,   Dunkel)
      6 Gormath (Rotmond,      Dunkel)
      7 Nyrath  (Bleichmond,   Dunkel)
      8 Shelkam (Tiefnacht,    Dunkel)
    MZ 0 = Besiedelung Moragh = TZ-Jahr -1.453.449 (absoluter Nullpunkt).

  Kopplung:
    1 MZ-Jahr = 400 TZ-Jahre (erzählerische Zeitdilatation).
    Umrechnung erfolgt auf Jahresebene mit Bruchteilen.
    Innerhalb eines MZ-Jahres: 8 Monate à 36 Tage, eigenständige Tag/Stunde-Struktur.
    Astronomisch impliziert das eine 468-fache Dilatation auf Stunden-Ebene;
    das ist Canon-Feature (Moragh-Zeit fließt relativ zur TZ langsamer).

  Anker:
    21. Saatmond 551 TZ = 21. März 1820 UZ (B1-Start).
    TZ 551 = MZ 3635 (Jahresebene). Ganz Buch 1 spielt in MZ 3635, Monat 5 (Dravon).

Usage:
    python scripts/zeitrechnung.py uz 2026-04-22
    python scripts/zeitrechnung.py tz "22. Blütenmond 551"
    python scripts/zeitrechnung.py mz "14. Dravon 3635"
    python scripts/zeitrechnung.py tz 551-5-22
"""

from __future__ import annotations
import argparse
import datetime as _dt
import io
import re
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# --- TZ-Canon (Gregorianisch + thalassische Monatsnamen) -----------------

TZ_MONATE = [
    "Eismond", "Sturmmond", "Saatmond", "Grünmond",
    "Blütenmond", "Lichtmond", "Glutmond", "Erntemond",
    "Herbstmond", "Nebelmond", "Frostmond", "Dunkelmond",
]
TZ_MONATE_LOWER = {m.lower(): i + 1 for i, m in enumerate(TZ_MONATE)}
for _m, _i in list(TZ_MONATE_LOWER.items()):
    _alt = _m.replace("ü", "ue").replace("ö", "oe").replace("ä", "ae")
    if _alt != _m:
        TZ_MONATE_LOWER[_alt] = _i

# TZ-Jahr ↔ UZ-Jahr: Jahresoffset
TZ_UZ_OFFSET = 1269  # TZ 0 = UZ ~1269

# --- MZ-Canon ------------------------------------------------------------

MZ_MONATE = [
    ("Torash",  "Bogenwende",   "Licht"),
    ("Ashral",  "Glutzeit",     "Licht"),
    ("Keldath", "Doppelflut",   "Licht"),
    ("Reshvan", "Ernteschluss", "Licht"),
    ("Dravon",  "Dämmerfall",   "Dunkel"),
    ("Gormath", "Rotmond",      "Dunkel"),
    ("Nyrath",  "Bleichmond",   "Dunkel"),
    ("Shelkam", "Tiefnacht",    "Dunkel"),
]
MZ_MONATE_LOWER = {m[0].lower(): i + 1 for i, m in enumerate(MZ_MONATE)}
for _m, _i in list(MZ_MONATE_LOWER.items()):
    _alt = _m.replace("ä", "ae")
    if _alt != _m:
        MZ_MONATE_LOWER[_alt] = _i

MZ_STUNDEN_PRO_TAG = 26
MZ_TAGE_PRO_WOCHE = 8
MZ_TAGE_PRO_MONAT = 36
MZ_MONATE_PRO_JAHR = 8
MZ_TAGE_PRO_JAHR = MZ_TAGE_PRO_MONAT * MZ_MONATE_PRO_JAHR  # 288

# --- Kopplung TZ ↔ MZ ----------------------------------------------------

TZ_JAHRE_PRO_MZ_JAHR = 400
# MZ 0 in TZ-Jahren (absoluter Nullpunkt Besiedelung Moragh)
MZ_NULL_IN_TZ_JAHR = -1_453_449

# --- UZ ↔ TZ (Gregorianisch) ---------------------------------------------

def uz_zu_tz_datum(dt: _dt.datetime) -> tuple[int, int, int, int, int]:
    """UZ-datetime -> (TZ-Jahr, Monat 1-12, Tag, Stunde, Minute)."""
    return (dt.year - TZ_UZ_OFFSET, dt.month, dt.day, dt.hour, dt.minute)

def tz_zu_uz_datum(jahr: int, monat: int, tag: int, stunde: int = 0, minute: int = 0) -> _dt.datetime:
    """TZ-Datum -> UZ-datetime (Gregorianisch)."""
    return _dt.datetime(jahr + TZ_UZ_OFFSET, monat, tag, stunde, minute)

# --- TZ: Jahr + Tag-Index --------------------------------------------------

def tz_tag_des_jahres(jahr: int, monat: int, tag: int) -> int:
    """Liefert den 1-basierten Tag im Jahr (Gregorianisch)."""
    return (_dt.date(jahr + TZ_UZ_OFFSET, monat, tag) -
            _dt.date(jahr + TZ_UZ_OFFSET, 1, 1)).days + 1

def tz_jahr_ist_schaltjahr(jahr: int) -> bool:
    y = jahr + TZ_UZ_OFFSET
    return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

def tz_tage_pro_jahr(jahr: int) -> int:
    return 366 if tz_jahr_ist_schaltjahr(jahr) else 365

# --- TZ ↔ MZ (Jahresebene, 400:1) -----------------------------------------

def tz_zu_mz_jahresanteil(tz_jahr: int, monat: int, tag: int, stunde: int = 0) -> float:
    """TZ-Datum -> MZ-Jahr als float (Jahr + Bruchteil innerhalb MZ-Jahr)."""
    tz_jahr_float = tz_jahr + (tz_tag_des_jahres(tz_jahr, monat, tag) - 1) / tz_tage_pro_jahr(tz_jahr)
    tz_jahr_float += stunde / (tz_tage_pro_jahr(tz_jahr) * 24)
    tz_jahre_seit_mz0 = tz_jahr_float - MZ_NULL_IN_TZ_JAHR
    return tz_jahre_seit_mz0 / TZ_JAHRE_PRO_MZ_JAHR

def mz_jahresanteil_zu_datum(mz_jahr_float: float) -> tuple[int, int, int, int]:
    """MZ-Jahr-Float -> (MZ-Jahr, Monat 1-8, Tag 1-36, Stunde 0-25)."""
    jahr = int(mz_jahr_float) if mz_jahr_float >= 0 else int(mz_jahr_float) - (1 if mz_jahr_float != int(mz_jahr_float) else 0)
    rest = mz_jahr_float - jahr  # [0, 1)
    tag_des_jahres_float = rest * MZ_TAGE_PRO_JAHR  # 0-288
    tag_im_jahr = int(tag_des_jahres_float)  # 0-287
    monat_idx, tag_im_monat = divmod(tag_im_jahr, MZ_TAGE_PRO_MONAT)
    stunde_float = (tag_des_jahres_float - tag_im_jahr) * MZ_STUNDEN_PRO_TAG
    stunde = int(stunde_float)
    return jahr, monat_idx + 1, tag_im_monat + 1, stunde

def mz_zu_jahresanteil(jahr: int, monat: int, tag: int, stunde: int = 0) -> float:
    """MZ-Datum -> MZ-Jahr als float."""
    if not (1 <= monat <= MZ_MONATE_PRO_JAHR):
        raise ValueError(f"MZ-Monat muss 1-{MZ_MONATE_PRO_JAHR} sein, war {monat}")
    if not (1 <= tag <= MZ_TAGE_PRO_MONAT):
        raise ValueError(f"MZ-Tag muss 1-{MZ_TAGE_PRO_MONAT} sein, war {tag}")
    if not (0 <= stunde < MZ_STUNDEN_PRO_TAG):
        raise ValueError(f"MZ-Stunde muss 0-{MZ_STUNDEN_PRO_TAG - 1} sein, war {stunde}")
    tag_im_jahr = (monat - 1) * MZ_TAGE_PRO_MONAT + (tag - 1)
    tag_float = tag_im_jahr + stunde / MZ_STUNDEN_PRO_TAG
    rest = tag_float / MZ_TAGE_PRO_JAHR
    return jahr + rest

def mz_zu_tz(mz_jahr_float: float) -> float:
    """MZ-Jahr-Float -> TZ-Jahr-Float (als Jahresbruchteil)."""
    tz_jahre_seit_mz0 = mz_jahr_float * TZ_JAHRE_PRO_MZ_JAHR
    return MZ_NULL_IN_TZ_JAHR + tz_jahre_seit_mz0

def tz_jahr_float_zu_datum(tz_jahr_float: float) -> tuple[int, int, int, int]:
    """TZ-Jahr-Float -> (Jahr, Monat 1-12, Tag, Stunde)."""
    jahr = int(tz_jahr_float) if tz_jahr_float >= 0 else int(tz_jahr_float) - (1 if tz_jahr_float != int(tz_jahr_float) else 0)
    rest = tz_jahr_float - jahr
    tage_im_jahr = tz_tage_pro_jahr(jahr)
    tag_des_jahres_float = rest * tage_im_jahr
    tag_des_jahres = int(tag_des_jahres_float) + 1  # 1-basiert
    stunde = int((tag_des_jahres_float - int(tag_des_jahres_float)) * 24)
    # Konvertiere tag_des_jahres in Monat/Tag via Gregorianisch
    basis = _dt.date(jahr + TZ_UZ_OFFSET, 1, 1)
    datum = basis + _dt.timedelta(days=tag_des_jahres - 1)
    return jahr, datum.month, datum.day, stunde

# --- Parser / Formatter ---------------------------------------------------

def parse_uz(s: str) -> _dt.datetime:
    s = s.strip()
    m = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})(?:\s+(\d{1,2}):(\d{2}))?$", s)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        hh = int(m.group(4)) if m.group(4) else 0
        mm = int(m.group(5)) if m.group(5) else 0
        return _dt.datetime(y, mo, d, hh, mm)
    m = re.match(r"^(\d{1,2})[./](\d{1,2})[./](\d{4})(?:\s+(\d{1,2}):(\d{2}))?$", s)
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        hh = int(m.group(4)) if m.group(4) else 0
        mm = int(m.group(5)) if m.group(5) else 0
        return _dt.datetime(y, mo, d, hh, mm)
    raise ValueError(f"UZ-Datum nicht erkannt: '{s}'. Nutze YYYY-MM-DD oder DD.MM.YYYY")

def parse_tz(s: str) -> tuple[int, int, int, int]:
    s = s.strip()
    m = re.match(r"^(\d+)\.\s*([A-Za-zÄÖÜäöüß]+)\s+(-?\d+)(?:(?:,\s*|\s+)(\d{1,2})(?::(\d{2}))?)?$", s)
    if m:
        tag = int(m.group(1))
        monat_name = m.group(2).lower()
        jahr = int(m.group(3))
        stunde = int(m.group(4)) if m.group(4) else 0
        monat = TZ_MONATE_LOWER.get(monat_name)
        if monat is None:
            raise ValueError(f"TZ-Monatsname unbekannt: '{m.group(2)}'. Muss einer von {TZ_MONATE} sein.")
        return jahr, monat, tag, stunde
    m = re.match(r"^(-?\d+)-(\d+)-(\d+)(?:\s+(\d{1,2}))?$", s)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)) if m.group(4) else 0
    raise ValueError(f"TZ-Datum nicht erkannt: '{s}'. Nutze '22. Blütenmond 551' oder '551-5-22'.")

def parse_mz(s: str) -> tuple[int, int, int, int]:
    s = s.strip()
    m = re.match(r"^(\d+)\.\s*([A-Za-zÄÖÜäöüß]+)\s+(-?\d+)(?:(?:,\s*|\s+)(\d{1,2}))?$", s)
    if m:
        tag = int(m.group(1))
        monat_name = m.group(2).lower()
        jahr = int(m.group(3))
        stunde = int(m.group(4)) if m.group(4) else 0
        monat = MZ_MONATE_LOWER.get(monat_name)
        if monat is None:
            raise ValueError(f"MZ-Monatsname unbekannt: '{m.group(2)}'. Muss einer von {[n for n,_,_ in MZ_MONATE]} sein.")
        return jahr, monat, tag, stunde
    m = re.match(r"^(-?\d+)-(\d+)-(\d+)(?:\s+(\d{1,2}))?$", s)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)) if m.group(4) else 0
    raise ValueError(f"MZ-Datum nicht erkannt: '{s}'. Nutze '14. Dravon 3635' oder '3635-5-14'.")

_UZ_WOCHENTAGE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
_UZ_MONATE_NAME = ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"]

def fmt_uz(dt: _dt.datetime) -> str:
    return f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d} {dt.hour:02d}:{dt.minute:02d} ({_UZ_WOCHENTAGE[dt.weekday()]}, {dt.day}. {_UZ_MONATE_NAME[dt.month - 1]} {dt.year})"

def fmt_tz(jahr: int, monat: int, tag: int, stunde: int) -> str:
    mname = TZ_MONATE[monat - 1] if 1 <= monat <= 12 else f"Monat?{monat}"
    return f"{tag}. {mname} {jahr} TZ, {stunde:02d}:00"

def fmt_mz(jahr: int, monat: int, tag: int, stunde: int) -> str:
    if 1 <= monat <= MZ_MONATE_PRO_JAHR:
        mname, bedeutung, halb = MZ_MONATE[monat - 1]
        return f"{tag}. {mname} {jahr} MZ, {stunde:02d}h/26 · Monat {monat}/8 ({bedeutung}, {halb}-Halbjahr)"
    return f"MZ {jahr}-{monat}-{tag}"

# --- Hauptausgabe ---------------------------------------------------------

def konvertiere_und_drucke(tz_jahr_float: float,
                           quelle_label: str,
                           quelle_tz: tuple[int, int, int, int] | None = None) -> None:
    # Falls eine originale TZ-Eingabe verfuegbar ist (uz/tz), die exakt zurueck verwenden
    # um Floating-Point-Rundung zu vermeiden.
    if quelle_tz is not None:
        tz_y, tz_m, tz_d, tz_h = quelle_tz
    else:
        tz_y, tz_m, tz_d, tz_h = tz_jahr_float_zu_datum(tz_jahr_float)
    uz = tz_zu_uz_datum(tz_y, tz_m, tz_d, tz_h)
    mz_float = tz_zu_mz_jahresanteil(tz_y, tz_m, tz_d, tz_h)
    mz_y, mz_m, mz_d, mz_h = mz_jahresanteil_zu_datum(mz_float)

    print(f"Quelle:  {quelle_label}")
    print()
    print(f"  UZ:  {fmt_uz(uz)}")
    print(f"  TZ:  {fmt_tz(tz_y, tz_m, tz_d, tz_h)}")
    print(f"  MZ:  {fmt_mz(mz_y, mz_m, mz_d, mz_h)}")
    print()
    print(f"  Intern:  TZ-Jahr-Float = {tz_jahr_float:.6f}  |  MZ-Jahr-Float = {mz_float:.6f}")

    # Delta zum B1-Anker (21. Saatmond 551 TZ)
    anker_float = 551 + (tz_tag_des_jahres(551, 3, 21) - 1) / tz_tage_pro_jahr(551)
    delta_tz = tz_jahr_float - anker_float
    delta_tz_tage = delta_tz * tz_tage_pro_jahr(551)
    print(f"  Zum B1-Anker (21. Saatmond 551 TZ):  {delta_tz:+.4f} TZ-Jahre  ({delta_tz_tage:+.1f} TZ-Tage)")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("system", choices=["uz", "tz", "mz"],
                    help="Quell-Zeitsystem des Eingabedatums.")
    ap.add_argument("datum", help="Datum, z.B. '2026-04-22' oder '22. Blütenmond 551' oder '14. Dravon 3635'.")
    args = ap.parse_args()

    quelle_tz = None
    try:
        if args.system == "uz":
            dt = parse_uz(args.datum)
            tz_y, tz_m, tz_d, tz_h, _ = uz_zu_tz_datum(dt)
            quelle_tz = (tz_y, tz_m, tz_d, tz_h)
            tz_float = tz_y + (tz_tag_des_jahres(tz_y, tz_m, tz_d) - 1) / tz_tage_pro_jahr(tz_y)
            tz_float += tz_h / (tz_tage_pro_jahr(tz_y) * 24)
            label = f"UZ {args.datum}"
        elif args.system == "tz":
            y, m, d, h = parse_tz(args.datum)
            quelle_tz = (y, m, d, h)
            tz_float = y + (tz_tag_des_jahres(y, m, d) - 1) / tz_tage_pro_jahr(y)
            tz_float += h / (tz_tage_pro_jahr(y) * 24)
            label = f"TZ {args.datum}"
        else:  # mz
            y, m, d, h = parse_mz(args.datum)
            mz_float = mz_zu_jahresanteil(y, m, d, h)
            tz_float = mz_zu_tz(mz_float)
            # Float-Rundung robust machen: +0.5h Offset
            tz_float += 0.5 / (365 * 24)
            label = f"MZ {args.datum}"
    except ValueError as e:
        print(f"FEHLER: {e}", file=sys.stderr)
        return 1

    konvertiere_und_drucke(tz_float, label, quelle_tz=quelle_tz)
    return 0


if __name__ == "__main__":
    sys.exit(main())
