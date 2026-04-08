"""
stand.py — Replay-Falter fuer den Roman-Stand zu einem beliebigen Kapitel.

Liest buch/zeitleiste.json und buch/status.json, filtert State-Events bis
zum gewuenschten Kapitel-Cutoff (in Lesereihenfolge inkl. Interludien) und
faltet sie zu einem Snapshot:

  - WOHNORTE: wer wohnt jetzt wo  (letzter wohnort-Event pro Figur)
  - BEGEGNUNGEN: wer hat wen wie eng getroffen  (max intensitaet pro Paar)
  - WISSEN: was weiss wer  (max stufe pro figur+fakt)

Verwendung:
  python scripts/stand.py --bis 11 [--buch buch1]

Schema-Doku liegt in buch/zeitleiste.json unter meta.schema.
"""

import argparse
import json
from pathlib import Path

INTENSITAETEN = ["fluechtig", "bekannt", "vertraut", "intim"]
STUFEN = ["ahnt", "gesehen", "versteht", "erklaert"]


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_zeitleiste(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_status(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Lesereihenfolge (Kapitel + Interludien) aus status.json
# ---------------------------------------------------------------------------

def lesereihenfolge(status, buch_key):
    """Liefert die Kapitel-Lesereihenfolge des Buches als flache Liste."""
    buch = status[buch_key]
    order = []
    for akt in buch.get("akte", []):
        order.extend(akt.get("kapitel", []))
    return order


def kapitel_position(order, kapitel):
    """Index eines Kapitels in der Lesereihenfolge. KeyError bei unbekannt."""
    try:
        return order.index(kapitel)
    except ValueError:
        raise KeyError(f"Unbekanntes Kapitel: {kapitel!r}")


# ---------------------------------------------------------------------------
# Event-Extraktion + Filter
# ---------------------------------------------------------------------------

def extract_events(zeitleiste):
    """Flacht alle Events aus monate[*].events.thalassien|moragh in eine Liste."""
    out = []
    for monat in zeitleiste.get("monate", []):
        ev = monat.get("events", {})
        for bucket in ("thalassien", "moragh"):
            for e in ev.get(bucket, []) or []:
                if "kapitel" in e:
                    out.append(e)
    return out


def filter_until(events, cutoff_kapitel, order):
    """Behaelt nur Events deren Kapitel ≤ Cutoff in Lesereihenfolge liegt."""
    cutoff_pos = kapitel_position(order, cutoff_kapitel)
    out = []
    for e in events:
        kap = e.get("kapitel")
        try:
            pos = kapitel_position(order, kap)
        except KeyError:
            continue  # unbekannte Kapitel ueberspringen
        if pos <= cutoff_pos:
            out.append(e)
    return out


# ---------------------------------------------------------------------------
# Snapshot-Builder
# ---------------------------------------------------------------------------

def _has_typ(event, typ):
    return typ in (event.get("typen") or [])


def _intensitaet_rank(value):
    try:
        return INTENSITAETEN.index(value)
    except ValueError:
        return -1


def _stufe_rank(value):
    try:
        return STUFEN.index(value)
    except ValueError:
        return -1


def build_snapshot(events, cutoff_kapitel, order):
    """Faltet die Events zu einem Snapshot-Dict."""
    relevant = filter_until(events, cutoff_kapitel, order)

    # In Lesereihenfolge sortieren — wichtig fuer wohnort-Reihenfolge
    relevant.sort(key=lambda e: kapitel_position(order, e["kapitel"]))

    wohnorte = {}      # figur -> {ort, stadt, seit_kapitel, detail}
    begegnungen = {}   # (a,b) sortiert -> {intensitaet, ort, kapitel:[...]}
    wissen = {}        # (figur, fakt) -> {stufe, kapitel}

    for e in relevant:
        kap = e["kapitel"]

        if _has_typ(e, "wohnort"):
            figur = e.get("figur")
            if figur:
                wohnorte[figur] = {
                    "ort": e.get("ort", ""),
                    "stadt": e.get("stadt", ""),
                    "seit_kapitel": kap,
                    "detail": e.get("detail", ""),
                }

        if _has_typ(e, "begegnung"):
            figuren = e.get("figuren") or []
            if len(figuren) >= 2:
                # Alle Paare bilden (fuer Gruppen-Begegnungen)
                for i in range(len(figuren)):
                    for j in range(i + 1, len(figuren)):
                        key = tuple(sorted([figuren[i], figuren[j]]))
                        cur = begegnungen.get(key)
                        new_int = e.get("intensitaet", "fluechtig")
                        if cur is None:
                            begegnungen[key] = {
                                "intensitaet": new_int,
                                "ort": e.get("ort", ""),
                                "kapitel": [kap],
                            }
                        else:
                            cur["kapitel"].append(kap)
                            if _intensitaet_rank(new_int) > _intensitaet_rank(cur["intensitaet"]):
                                cur["intensitaet"] = new_int
                                cur["ort"] = e.get("ort", cur["ort"])

        if _has_typ(e, "wissen"):
            figur = e.get("figur")
            fakt = e.get("fakt")
            stufe = e.get("stufe")
            if figur and fakt and stufe:
                key = (figur, fakt)
                cur = wissen.get(key)
                if cur is None or _stufe_rank(stufe) > _stufe_rank(cur["stufe"]):
                    wissen[key] = {"stufe": stufe, "kapitel": kap}

    return {
        "cutoff": cutoff_kapitel,
        "wohnorte": wohnorte,
        "begegnungen": begegnungen,
        "wissen": wissen,
    }


# ---------------------------------------------------------------------------
# Formatter
# ---------------------------------------------------------------------------

def format_snapshot(snapshot, bis):
    """Druckbare ASCII-Darstellung des Snapshots."""
    lines = []
    lines.append(f"STAND nach Kapitel {bis}")
    lines.append("=" * 40)
    lines.append("")

    # WOHNORTE
    lines.append("WOHNORTE")
    if not snapshot["wohnorte"]:
        lines.append("  (keine wohnort-Events)")
    else:
        # nach Stadt + Ort gruppieren, damit Kollisionen sichtbar werden
        max_figur = max(len(f) for f in snapshot["wohnorte"]) if snapshot["wohnorte"] else 0
        for figur in sorted(snapshot["wohnorte"]):
            w = snapshot["wohnorte"][figur]
            ort = w["ort"]
            if w["stadt"]:
                ort_str = f"{ort} ({w['stadt']})"
            else:
                ort_str = ort
            lines.append(f"  {figur:<{max_figur}}  {ort_str:<40} seit Kap {w['seit_kapitel']}")

        # Kollisions-Check: mehrere Figuren am gleichen Ort
        ort_groups = {}
        for figur, w in snapshot["wohnorte"].items():
            key = w["ort"]
            ort_groups.setdefault(key, []).append(figur)
        kollisionen = {ort: figs for ort, figs in ort_groups.items() if len(figs) >= 2}
        if kollisionen:
            lines.append("")
            lines.append("  KOLLISIONEN (gleicher Wohnort):")
            for ort, figs in kollisionen.items():
                figs_str = ", ".join(sorted(figs))
                lines.append(f"    {ort}: {figs_str}")

    lines.append("")

    # BEGEGNUNGEN
    lines.append("BEGEGNUNGEN")
    if not snapshot["begegnungen"]:
        lines.append("  (keine begegnung-Events)")
    else:
        for key in sorted(snapshot["begegnungen"]):
            b = snapshot["begegnungen"][key]
            paar = " <-> ".join(key)
            kaps = ", ".join(b["kapitel"])
            lines.append(f"  {paar:<35} {b['intensitaet']:<10} (Kap {kaps})")

    lines.append("")

    # WISSEN
    lines.append("WISSEN")
    if not snapshot["wissen"]:
        lines.append("  (keine wissen-Events)")
    else:
        # nach Figur gruppieren
        by_figur = {}
        for (figur, fakt), w in snapshot["wissen"].items():
            by_figur.setdefault(figur, []).append((fakt, w))
        for figur in sorted(by_figur):
            lines.append(f"  {figur}:")
            for fakt, w in sorted(by_figur[figur]):
                lines.append(f"    {fakt:<30} {w['stufe']:<10} (seit Kap {w['kapitel']})")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(description="Stand des Romans zu Kapitel N.")
    parser.add_argument("--bis", required=True, help="Cutoff-Kapitel (z.B. 11 oder I2)")
    parser.add_argument("--buch", default="buch1", help="Buch-Schluessel in status.json")
    parser.add_argument(
        "--zeitleiste",
        default=None,
        help="Pfad zu zeitleiste.json (default: buch/zeitleiste.json relativ zum Repo-Root)",
    )
    parser.add_argument(
        "--status",
        default=None,
        help="Pfad zu status.json (default: buch/status.json relativ zum Repo-Root)",
    )
    args = parser.parse_args(argv)

    # Repo-Root finden — scripts/stand.py liegt in scripts/, also eine Ebene hoch
    repo_root = Path(__file__).resolve().parent.parent
    zeitleiste_path = Path(args.zeitleiste) if args.zeitleiste else repo_root / "buch" / "zeitleiste.json"
    status_path = Path(args.status) if args.status else repo_root / "buch" / "status.json"

    zeitleiste = load_zeitleiste(zeitleiste_path)
    status = load_status(status_path)

    order = lesereihenfolge(status, args.buch)
    events = extract_events(zeitleiste)
    snapshot = build_snapshot(events, args.bis, order)
    print(format_snapshot(snapshot, bis=args.bis))


if __name__ == "__main__":
    main()
