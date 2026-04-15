#!/usr/bin/env python3
"""Pruefe Konsistenz der Datums-Header in allen Buch-1-Kapiteln.

Header-Format (neue Kapitel ab K12):
  *{Tag}. {Mond} 551 · {N} Wochen {M} Tage in Vael*
  *{Tag}. {Mond} 551 · {N} Wochen in Vael*    (wenn M=0)
  *{Tag}. {Mond} 551 · Tag {N} in Vael*

Mond -> Monat (vermutet aus tz_tag-Belegen in Aktplaenen):
  Eismond=1, Schneemond=2, Lenzmond=3, Saatmond=4, Bluetenmond=5,
  Sonnmond=6, Glutmond=7, Erntemond=8, Weinmond=9, Reifmond=10,
  Nebelmond=11, Dunkelmond=12

Tag 1 in Vael (figuren-spezifisch, aus alten K05-K07-Headern):
  Alphina = 24. Maerz / Lenzmond
  Sorel   = 27. Maerz / Lenzmond
  Vesper  = 28. Maerz / Lenzmond
  Maren   = 24. Maerz / Lenzmond  (vermutet, da K08 mit Annahme passt)

Wochen-Berechnung: N Tage in Vael -> floor(N/7) Wochen, N%7 Tage.
"""
import os
import re
import sys
from pathlib import Path

KAPITEL_DIR = Path("buch/kapitel")

MOND_TO_MONAT = {
    "Eismond": 1, "Schneemond": 2, "Lenzmond": 3, "Saatmond": 4,
    "Blütenmond": 5, "Bluetenmond": 5, "Sonnmond": 6, "Glutmond": 7,
    "Erntemond": 8, "Weinmond": 9, "Reifmond": 10, "Nebelmond": 11,
    "Dunkelmond": 12,
    # Irdische Aliase (aelteste Kapitel)
    "Januar": 1, "Februar": 2, "März": 3, "Maerz": 3, "April": 4,
    "Mai": 5, "Juni": 6, "Juli": 7, "August": 8, "September": 9,
    "Oktober": 10, "November": 11, "Dezember": 12,
}

# Kumulative Tage bis Monatsende (nicht-Schaltjahr)
DAYS_BEFORE_MONTH = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]

ANKUNFT = {
    "alphina": (3, 24),
    "sorel":   (3, 27),
    "vesper":  (3, 28),
    "maren":   (3, 24),
}

# Header-Patterns
HEADER_RE = re.compile(
    r"\*\s*(\d+)\s*\.\s*(\w+)\s+551\s*[·•]\s*(.+?)\s*\*"
)
WT_RE = re.compile(r"^(\d+)\s+Wochen?\s+(\d+)\s+Tage?\s+in\s+Vael\s*$")
W_RE  = re.compile(r"^(\d+)\s+Wochen?\s+in\s+Vael\s*$")
TAG_RE = re.compile(r"^Tag\s+(\d+)\s+in\s+Vael\s*$")


def day_of_year(month, day):
    return DAYS_BEFORE_MONTH[month - 1] + day


def figur_from_filename(fn):
    name = fn.lower()
    for f in ("alphina-sorel", "alphina", "sorel", "vesper", "maren"):
        if f in name:
            # bei alphina-sorel nehmen wir den ersten POV
            if f == "alphina-sorel":
                return "alphina"
            return f
    if "alle" in name:
        return None  # Multi-POV, Ankunft unklar
    return None


def parse_header(line):
    m = HEADER_RE.search(line)
    if not m:
        return None
    tag = int(m.group(1))
    mond = m.group(2)
    rest = m.group(3).strip()
    return tag, mond, rest


def parse_zeitangabe(rest):
    """Liefert (mode, wochen, tage_oder_tag_n) oder ('text', None, rest)."""
    m = WT_RE.match(rest)
    if m:
        return "wt", int(m.group(1)), int(m.group(2))
    m = W_RE.match(rest)
    if m:
        return "w", int(m.group(1)), 0
    m = TAG_RE.match(rest)
    if m:
        return "tag", None, int(m.group(1))
    return "text", None, rest


def main():
    files = sorted(KAPITEL_DIR.glob("*.md"))
    rows = []
    for fp in files:
        name = fp.name
        if name.endswith("-handoff.md") or name.endswith("-entwurf.md") or name.endswith("-prework.md"):
            continue
        # Skip alte Szenen-Files (01-szene1.md etc.)
        if re.match(r"^\d+-(szene|alphina-v2)", name):
            continue
        try:
            head = fp.read_text(encoding="utf-8").splitlines()[:6]
        except Exception:
            continue
        date_line = None
        for line in head:
            if HEADER_RE.search(line):
                date_line = line.strip()
                break
        if not date_line:
            continue
        parsed = parse_header(date_line)
        if not parsed:
            continue
        tag, mond, rest = parsed
        if mond not in MOND_TO_MONAT:
            rows.append((name, date_line, "?", "Mond unbekannt"))
            continue
        monat = MOND_TO_MONAT[mond]
        doy = day_of_year(monat, tag)
        figur = figur_from_filename(name)
        mode, w, t = parse_zeitangabe(rest)
        if mode == "text":
            rows.append((name, date_line, "n/a", f"Zeitangabe nicht parsbar: {t!r}"))
            continue
        # Soll-Tag-in-Vael berechnen
        if not figur:
            rows.append((name, date_line, "?", "POV unklar (Multi/Alle) — manuell pruefen"))
            continue
        ankunft_m, ankunft_d = ANKUNFT[figur]
        ankunft_doy = day_of_year(ankunft_m, ankunft_d)
        tag_in_vael = doy - ankunft_doy + 1
        soll_w = tag_in_vael // 7
        soll_t = tag_in_vael % 7
        # Zur Anzeige: figur + ankunft
        if mode == "wt":
            ist_str = f"{w}W{t}T"
            ist_total = w * 7 + t
        elif mode == "w":
            ist_str = f"{w}W"
            ist_total = w * 7
        else:  # tag
            ist_str = f"Tag {t}"
            ist_total = t - 1  # "Tag 1" = 0 Tage seit Ankunft
        # Vergleich
        if mode == "tag":
            soll_str = f"Tag {tag_in_vael}"
            ok = (t == tag_in_vael)
        else:
            soll_str = f"{soll_w}W{soll_t}T" if soll_t else f"{soll_w}W"
            ok = (ist_total == tag_in_vael - 1) if False else (
                # neue Konvention: N Tage in Vael = Tag-Index ab Ankunft (1-basiert),
                # Wochen = floor(N/7), Tage = N%7
                w == soll_w and t == soll_t if mode == "wt" else (w == soll_w and soll_t == 0)
            )
        marker = "OK " if ok else "*** FEHLER ***"
        rows.append((name, date_line, f"{figur} (Tag1={ankunft_d}.{ankunft_m}.) -> Tag {tag_in_vael} = {soll_str}", marker if ok else f"{marker} ist={ist_str}"))

    # Ausgabe
    print(f"{'Datei':<35} {'Header':<55} {'Berechnung':<55} Status")
    print("-" * 180)
    for name, dl, calc, status in rows:
        print(f"{name:<35} {dl:<55} {calc:<55} {status}")


if __name__ == "__main__":
    main()
