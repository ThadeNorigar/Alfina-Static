#!/usr/bin/env python3
"""
kapitel-kontext.py — Extrahiert schlanken, kapitelspezifischen Kontext
aus zeitleiste.json, status.json und Aktplänen.

Usage:
    python scripts/kapitel-kontext.py B1-K15 [--phase entwurf|ausarbeitung|lektorat]
    python scripts/kapitel-kontext.py B1-I3 [--phase entwurf]
"""

import argparse
import io
import json
import os
import re
import sys

# Force UTF-8 output on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BUCH_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "buch")
LESEPROBEN_DIR = os.path.join(BUCH_DIR, "leseproben")
KAPITEL_DIR = os.path.join(BUCH_DIR, "kapitel")

# Whitelist kanonischer Figurennamen fuer Text-Extraktion.
# Genutzt fuer Figuren-Matching bei Leseproben und Vorgaenger-Kapiteln.
MAIN_FIGURES = {
    "Alphina", "Sorel", "Vesper", "Maren", "Runa", "Varen",
    "Jara", "Esther", "Halvard", "Henrik", "Edric", "Tohl",
    "Nyr", "Elke", "Lene", "Haron", "Talven", "Kesper", "Keldan",
}

AKTPLAN_MAP = {
    "02-akt1.md": lambda k: not k.startswith("I") and int(k) <= 12 or k in ("I1", "I2", "I3"),
    "03-akt2.md": lambda k: not k.startswith("I") and 13 <= int(k) <= 22 if not k.startswith("I") else False,
    "04-akt3.md": lambda k: not k.startswith("I") and 23 <= int(k) <= 33 if not k.startswith("I") else False,
    "05-akt4.md": lambda k: not k.startswith("I") and 34 <= int(k) <= 41 if not k.startswith("I") else False,
}


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"# WARNUNG: {path} nicht gefunden", file=sys.stderr)
        return None


def parse_kapitel_id(raw):
    """Parse 'B1-K15' -> ('1', '15'), 'B1-I3' -> ('1', 'I3')"""
    m = re.match(r"B(\d+)-K(\d+)", raw)
    if m:
        return m.group(1), m.group(2).lstrip("0") or "0"
    m = re.match(r"B(\d+)-(I\d+)", raw)
    if m:
        return m.group(1), m.group(2)
    return None, None


def get_kapitel_order(status):
    """Build ordered list of kapitel keys from akte structure."""
    order = []
    for akt in status.get("buch1", {}).get("akte", []):
        for k in akt.get("kapitel", []):
            order.append(k)
    return order


def status_key(kap_num):
    """Convert kapitel number to status.json key. '15' -> '15', 'I3' -> 'I3', '9' -> '09'"""
    if kap_num.startswith("I"):
        return kap_num
    try:
        n = int(kap_num)
        return f"{n:02d}" if n < 10 else str(n)
    except ValueError:
        return kap_num


def get_kap_info(status, key):
    """Get kapitel info from status.json."""
    return status.get("buch1", {}).get("kapitel", {}).get(key, None)


def collect_all_events(zeitleiste):
    """Collect all events from all monate, both thalassien and moragh."""
    events = []
    for monat in zeitleiste.get("monate", []):
        ev = monat.get("events", {})
        for e in ev.get("thalassien", []):
            events.append(e)
        for e in ev.get("moragh", []):
            events.append(e)
    return events


def event_has_kapitel(event):
    """Check if event has a kapitel field."""
    return "kapitel" in event and event["kapitel"] is not None


def kap_sort_key(kap_str, order):
    """Sort key for kapitel string based on akte order."""
    key = status_key(kap_str)
    try:
        return order.index(key)
    except ValueError:
        # Fallback: interludien after regular chapters
        if kap_str.startswith("I"):
            return 1000 + int(kap_str[1:])
        try:
            return int(kap_str)
        except ValueError:
            return 9999


def kap_is_before_or_equal(kap_str, target, order):
    """Check if kap_str comes before or at target in the order."""
    return kap_sort_key(kap_str, order) <= kap_sort_key(target, order)


def kap_is_before(kap_str, target, order):
    """Check if kap_str comes strictly before target in the order."""
    return kap_sort_key(kap_str, order) < kap_sort_key(target, order)


def get_aktplan_file(kap_num):
    """Determine which aktplan file to use."""
    if kap_num.startswith("I"):
        return "02-akt1.md"
    try:
        n = int(kap_num)
    except ValueError:
        return None
    if n <= 12:
        return "02-akt1.md"
    elif n <= 22:
        return "03-akt2.md"
    elif n <= 33:
        return "04-akt3.md"
    elif n <= 41:
        return "05-akt4.md"
    return None


def extract_aktplan_snippet(kap_num):
    """Extract the section for a specific chapter from the aktplan."""
    aktplan_file = get_aktplan_file(kap_num)
    if not aktplan_file:
        return "*Kein Aktplan zugeordnet.*"

    path = os.path.join(BUCH_DIR, aktplan_file)
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return f"*{aktplan_file} nicht gefunden.*"

    # Build search pattern for the chapter heading
    if kap_num.startswith("I"):
        num = int(kap_num[1:])
        # Interludia use Roman numerals in aktplan headings
        roman = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI"}
        roman_num = roman.get(num, str(num))
        pattern = rf"^### Interludium {re.escape(roman_num)}\b"
    else:
        n = int(kap_num)
        pattern = rf"^### Kap\. {n}\b"

    lines = content.split("\n")
    start = None
    end = None
    for i, line in enumerate(lines):
        if start is None:
            if re.match(pattern, line):
                start = i
        elif re.match(r"^### ", line):
            end = i
            break

    if start is None:
        return f"*Kap. {kap_num} nicht in {aktplan_file} gefunden.*"

    snippet_lines = lines[start:end] if end else lines[start:]
    # Trim trailing empty lines
    while snippet_lines and not snippet_lines[-1].strip():
        snippet_lines.pop()
    return "\n".join(snippet_lines)


def extract_figures_from_text(text):
    """Finde bekannte Figurennamen aus MAIN_FIGURES in einem Text.
    Robust gegen beliebige Trennzeichen (Komma, Plus, Klammern, Text)."""
    if not text:
        return set()
    found = set()
    for name in MAIN_FIGURES:
        if re.search(rf"\b{re.escape(name)}\b", text):
            found.add(name)
    return found


def get_kapitel_figures(kap_info, events_current):
    """Vereinigung der Figuren aus POV-Feld, Kurztext und Event-Feldern."""
    figures = set()
    pov = kap_info.get("pov", "") or ""
    text = kap_info.get("text", "") or ""
    figures |= extract_figures_from_text(pov)
    figures |= extract_figures_from_text(text)
    # "Alle vier" / "alle Vier" in POV oder Kurztext → die vier Hauptfiguren
    for src in (pov, text):
        if re.search(r"\balle\s+vier\b", src, re.IGNORECASE):
            figures |= {"Alphina", "Sorel", "Vesper", "Maren"}
            break
    for e in events_current:
        pov_e = e.get("pov", "") or ""
        figures |= extract_figures_from_text(str(pov_e))
        figuren_e = e.get("figuren", []) or []
        if isinstance(figuren_e, list):
            for f in figuren_e:
                figures |= extract_figures_from_text(str(f))
        elif isinstance(figuren_e, str):
            figures |= extract_figures_from_text(figuren_e)
        figur_e = e.get("figur", "") or ""
        figures |= extract_figures_from_text(str(figur_e))
    return figures


def parse_leseprobe_frontmatter(path):
    """Parse YAML-aehnliches Frontmatter einer Leseproben-Datei.
    Erwartet Schema: --- key: value ... ---."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return None
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not m:
        return None
    front = m.group(1)
    data = {}
    for line in front.split("\n"):
        m2 = re.match(r"^([a-zA-Z_][a-zA-Z_0-9]*):\s*(.*)$", line)
        if m2:
            key = m2.group(1)
            val = m2.group(2).strip()
            data[key] = val
    return data


def load_all_leseproben():
    """Laedt alle Frontmatter-Bloecke aus buch/leseproben/*.md."""
    if not os.path.isdir(LESEPROBEN_DIR):
        return []
    result = []
    for fn in sorted(os.listdir(LESEPROBEN_DIR)):
        if fn.startswith("README") or not fn.endswith(".md"):
            continue
        path = os.path.join(LESEPROBEN_DIR, fn)
        data = parse_leseprobe_frontmatter(path)
        if data:
            data["_file"] = fn
            result.append(data)
    return result


def score_leseprobe(probe, kap_pov, kap_figures):
    """Bewertet eine Leseprobe gegen ein Kapitel.
    POV-Match = 10, Figuren-Ueberlappung je Figur = 3.
    Rueckgabe: (score, ueberlappte_figuren_set)."""
    score = 0
    probe_pov = (probe.get("pov", "") or "").strip()
    probe_figures_raw = probe.get("figuren", "") or ""
    probe_figures = (
        extract_figures_from_text(probe_figures_raw)
        | extract_figures_from_text(probe_pov)
    )
    # POV-Match: Probe-POV-Figur in Kapitel-POV-String
    kap_pov_figs = extract_figures_from_text(kap_pov)
    probe_pov_figs = extract_figures_from_text(probe_pov)
    if probe_pov_figs & kap_pov_figs:
        score += 10
    # Figuren-Ueberlappung
    overlap = probe_figures & kap_figures
    score += len(overlap) * 3
    return score, overlap


def format_event_compact(event):
    """Format event as one compact line."""
    kap = event.get("kapitel", "?")
    titel = event.get("titel", "?")
    pov = event.get("pov", "")
    datum = event.get("datum_text", "")
    typen = ", ".join(event.get("typen", []))
    parts = [f"K{kap}"]
    if pov:
        parts.append(pov.split(" - ")[-1] if " - " in pov else pov)
    if datum:
        parts.append(datum)
    parts.append(titel)
    if typen:
        parts.append(f"[{typen}]")
    return " | ".join(parts)


def format_event_full(event):
    """Format event with all fields."""
    lines = []
    kap = event.get("kapitel", "?")
    titel = event.get("titel", "?")
    pov = event.get("pov", "")
    datum = event.get("datum_text", "")
    typen = ", ".join(event.get("typen", []))
    detail = event.get("detail", "")

    header = f"- **K{kap}** {titel}"
    if pov:
        header += f" ({pov})"
    if datum:
        header += f" — {datum}"
    if typen:
        header += f" [{typen}]"
    lines.append(header)
    if detail:
        lines.append(f"  {detail}")

    # Extra fields for structured events
    for field in ("figur", "figuren", "intensitaet", "ort", "fakt", "stufe"):
        val = event.get(field)
        if val:
            if isinstance(val, list):
                val = ", ".join(val)
            lines.append(f"  {field}: {val}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Kapitel-Kontext extrahieren")
    parser.add_argument("kapitel", help="z.B. B1-K15, B1-I3")
    parser.add_argument("--phase", choices=["entwurf", "ausarbeitung", "lektorat"],
                        default="entwurf")
    args = parser.parse_args()

    buch_num, kap_num = parse_kapitel_id(args.kapitel)
    if not buch_num or not kap_num:
        print(f"Fehler: '{args.kapitel}' nicht erkannt. Format: B1-K15 oder B1-I3", file=sys.stderr)
        sys.exit(1)

    kap_key = status_key(kap_num)

    # Load files
    status = load_json(os.path.join(BUCH_DIR, "status.json"))
    zeitleiste = load_json(os.path.join(BUCH_DIR, "zeitleiste.json"))

    if not status:
        print("Fehler: status.json konnte nicht geladen werden.", file=sys.stderr)
        sys.exit(1)

    order = get_kapitel_order(status)
    kap_info = get_kap_info(status, kap_key)

    if not kap_info:
        print(f"Fehler: Kapitel '{kap_key}' nicht in status.json gefunden.", file=sys.stderr)
        sys.exit(1)

    # Collect events
    all_events = collect_all_events(zeitleiste) if zeitleiste else []
    kap_events = [e for e in all_events if event_has_kapitel(e)]

    # Sort events by kapitel order
    kap_events.sort(key=lambda e: kap_sort_key(e["kapitel"], order))

    # Events up to and including this chapter
    events_until = [e for e in kap_events if kap_is_before_or_equal(e["kapitel"], kap_num, order)]
    events_current = [e for e in kap_events if status_key(e["kapitel"]) == kap_key]
    events_before = [e for e in kap_events if kap_is_before(e["kapitel"], kap_num, order)]

    # POV figure
    pov = kap_info.get("pov", "?")

    # === OUTPUT ===
    phase_label = {"entwurf": "Entwurf", "ausarbeitung": "Ausarbeitung", "lektorat": "Lektorat"}
    print(f"# Kontext für {args.kapitel} ({phase_label[args.phase]})\n")

    # --- Kapitel-Info ---
    print("## Kapitel-Info")
    datum = ""
    for e in events_current:
        if e.get("datum_text"):
            datum = e["datum_text"]
            break
    info_parts = [f"POV: {pov}", f"Status: {kap_info.get('status', '?')}"]
    if datum:
        info_parts.append(f"Datum: {datum}")
    if kap_info.get("woerter"):
        info_parts.append(f"Wörter: {kap_info['woerter']}")
    print(" | ".join(info_parts))
    if kap_info.get("text"):
        print(f"\n{kap_info['text']}\n")
    else:
        print()

    # --- Nachbar-Kapitel ---
    try:
        idx = order.index(kap_key)
    except ValueError:
        idx = -1

    if args.phase == "lektorat":
        neighbor_range = range(max(0, idx - 1), min(len(order), idx + 2))
    else:
        neighbor_range = range(max(0, idx - 2), min(len(order), idx + 3))

    print("## Nachbar-Kapitel")
    for i in neighbor_range:
        nk = order[i]
        ni = get_kap_info(status, nk)
        if not ni:
            continue
        marker = " ← DIESES KAPITEL" if nk == kap_key else ""
        npov = ni.get("pov", "?")
        nstatus = ni.get("status", "?")
        ntext = ni.get("text", "")
        if ntext and len(ntext) > 200:
            ntext = ntext[:200] + "…"
        prefix = f"I{nk[1:]}" if nk.startswith("I") else f"K{nk}"
        print(f"- **{prefix}** ({npov}, {nstatus}): {ntext}{marker}")
    print()

    if args.phase == "lektorat":
        # Lektorat: minimal output, done here
        return

    # --- Zeitleisten-Events bis hierher (nur entwurf) ---
    if args.phase == "entwurf":
        print("## Zeitleisten-Events bis hierher")
        # Only events with kapitel field, compact
        for e in events_until:
            if e.get("kapitel") and status_key(e["kapitel"]) != kap_key:
                print(f"- {format_event_compact(e)}")
        print()

    # --- Zeitleisten-Events aktuelles Kapitel ---
    print(f"## Zeitleisten-Events {args.kapitel}")
    if events_current:
        for e in events_current:
            print(format_event_full(e))
    else:
        print("*Keine Events für dieses Kapitel in der Zeitleiste.*")
    print()

    # --- Offene Tschechow-Waffen ---
    print("## Offene Tschechow-Waffen")
    tschechow_events = [e for e in events_before
                        if "tschechow" in e.get("typen", [])]
    if tschechow_events:
        # Check which ones fire later
        future_events = [e for e in kap_events
                         if not kap_is_before_or_equal(e["kapitel"], kap_num, order)]
        for te in tschechow_events:
            titel = te.get("titel", "?")
            kap = te.get("kapitel", "?")
            # Check if it fires later
            fires_in = []
            for fe in future_events:
                if "tschechow" in fe.get("typen", []):
                    # Same title or related
                    if te.get("titel") and te["titel"].lower() in fe.get("detail", "").lower():
                        fires_in.append(f"K{fe['kapitel']}")
            fire_note = f" → feuert in {', '.join(fires_in)}" if fires_in else " → offen"
            print(f"- K{kap}: {titel}{fire_note}")
    else:
        print("*Keine Tschechow-Waffen vor diesem Kapitel.*")
    print()

    # --- Aktplan-Snippet ---
    print("## Aktplan-Snippet")
    snippet = extract_aktplan_snippet(kap_num)
    print(snippet)
    print()

    # --- Empfohlene Leseproben ---
    # Nur fuer entwurf/ausarbeitung. Matching gegen POV + Figuren des Kapitels.
    kap_figures = get_kapitel_figures(kap_info, events_current)
    # Auch fruehere Events beruecksichtigen, damit "alle vier"-Kapitel gut matchen.
    for e in events_current:
        for field in ("figuren", "figur"):
            val = e.get(field)
            if isinstance(val, list):
                for x in val:
                    kap_figures |= extract_figures_from_text(str(x))
            elif isinstance(val, str):
                kap_figures |= extract_figures_from_text(val)

    probes = load_all_leseproben()
    print("## Empfohlene Leseproben")
    if probes:
        scored = []
        for p in probes:
            s, ov = score_leseprobe(p, pov, kap_figures)
            if s > 0:
                scored.append((s, ov, p))
        scored.sort(key=lambda x: (-x[0], x[2].get("_file", "")))
        if scored:
            fig_str = ", ".join(sorted(kap_figures)) if kap_figures else "(keine erkannt)"
            print(f"*Kapitel-Figuren (erkannt): {fig_str}*\n")
            for s, ov, p in scored[:6]:
                tier = "Primaer" if s >= 10 else ("Stark" if s >= 6 else "Ergaenzend")
                ov_str = ", ".join(sorted(ov)) if ov else "—"
                kat = p.get("kategorie", "?")
                probe_pov = p.get("pov", "?")
                probe_heat = p.get("heat_level", "?")
                zweck = p.get("zweck", "")
                if len(zweck) > 220:
                    zweck = zweck[:220] + "…"
                print(f"- **[{tier}, Score {s}]** `buch/leseproben/{p['_file']}`")
                print(f"  - Kategorie: {kat} | POV: {probe_pov} | Heat: {probe_heat}")
                print(f"  - Ueberlappung: {ov_str}")
                if zweck:
                    print(f"  - Zweck: {zweck}")
        else:
            print("*Keine Leseproben matchen POV/Figuren dieses Kapitels.*")
    else:
        print("*Keine Leseproben gefunden.*")
    print()

    # --- Vorgaenger-Kapitel mit Figuren-Ueberlappung ---
    # Gehe rueckwaerts durch die Kapitel-Reihenfolge, suche die letzten 2
    # Kapitel, bei denen mindestens eine Figur mit dem aktuellen Kapitel ueberlappt.
    print("## Vorgaenger-Kapitel mit Figuren-Ueberlappung")
    if kap_figures and idx > 0:
        predecessors = []
        for i in range(idx - 1, -1, -1):
            prev_key = order[i]
            prev_info = get_kap_info(status, prev_key)
            if not prev_info:
                continue
            prev_num = prev_key  # z.B. "24" oder "I3"
            prev_events = [e for e in kap_events if status_key(e.get("kapitel", "")) == prev_key]
            prev_figures = get_kapitel_figures(prev_info, prev_events)
            overlap = prev_figures & kap_figures
            if overlap:
                prev_prefix = f"I{prev_key[1:]}" if prev_key.startswith("I") else f"K{prev_key}"
                b1_id = f"B1-{prev_prefix}"
                predecessors.append({
                    "id": b1_id,
                    "key": prev_key,
                    "pov": prev_info.get("pov", "?"),
                    "status": prev_info.get("status", "?"),
                    "overlap": overlap,
                    "text": prev_info.get("text", ""),
                })
                if len(predecessors) >= 2:
                    break
        if predecessors:
            print(f"*Letzte {len(predecessors)} Kapitel mit mindestens einer gemeinsamen Figur.*\n")
            for p in predecessors:
                ov_str = ", ".join(sorted(p["overlap"]))
                # Passende Datei bestimmen: finale Prosa-Datei bevorzugt, sonst Entwurf
                candidate_files = []
                # Finale Kapitel-Dateien (ohne -entwurf, ohne -handoff)
                if os.path.isdir(KAPITEL_DIR):
                    for fn in os.listdir(KAPITEL_DIR):
                        if not fn.endswith(".md"):
                            continue
                        if fn.startswith(f"{p['id']}-") or fn.startswith(f"{p['id']}."):
                            if any(suffix in fn for suffix in ("-handoff", "-prework", ".backup", "-handoff-lektorat")):
                                continue
                            candidate_files.append(fn)
                # Sortierpraeferenz: final (ohne -entwurf) > -entwurf
                candidate_files.sort(key=lambda f: (0 if "-entwurf" not in f else 1, f))
                file_hint = candidate_files[0] if candidate_files else "(keine Datei gefunden)"
                text = p["text"]
                if text and len(text) > 160:
                    text = text[:160] + "…"
                print(f"- **{p['id']}** ({p['pov']}, {p['status']}) — Ueberlappung: {ov_str}")
                print(f"  - Datei: `buch/kapitel/{file_hint}`")
                if text:
                    print(f"  - {text}")
        else:
            print("*Keine Vorgaenger-Kapitel mit Figuren-Ueberlappung gefunden.*")
    else:
        print("*Kein Vorgaenger oder keine Figuren erkannt.*")
    print()

    # --- Wissensstand der POV-Figur ---
    print("## Wissensstand der POV-Figur")
    # Extract base figure name from POV (e.g. "Alphina + Sorel" -> check both)
    pov_figures = [f.strip() for f in pov.split("+")]
    wissen_events = [e for e in events_until
                     if "wissen" in e.get("typen", [])
                     and e.get("figur", "") in pov_figures]
    if wissen_events:
        # Group by (figur, fakt), keep highest stufe
        stufen_order = ["ahnt", "gesehen", "versteht", "erklaert"]
        best = {}
        for e in wissen_events:
            key = (e.get("figur", ""), e.get("fakt", ""))
            stufe = e.get("stufe", "")
            old_stufe = best.get(key, {}).get("stufe", "")
            old_idx = stufen_order.index(old_stufe) if old_stufe in stufen_order else -1
            new_idx = stufen_order.index(stufe) if stufe in stufen_order else -1
            if new_idx > old_idx:
                best[key] = e
        for (figur, fakt), e in sorted(best.items()):
            detail = e.get("detail", "")
            detail_str = f" — {detail}" if detail else ""
            print(f"- {figur}: **{fakt}** ({e.get('stufe', '?')}, K{e.get('kapitel', '?')}){detail_str}")
    else:
        print("*Keine Wissens-Events für die POV-Figur.*")
    print()

    # --- Begegnungen bis hierher ---
    print("## Begegnungen bis hierher")
    begegnung_events = [e for e in events_until
                        if "begegnung" in e.get("typen", [])]
    if begegnung_events:
        # Group by figurenpaar, keep highest intensitaet
        intensitaet_order = ["fluechtig", "bekannt", "vertraut", "intim"]
        best_beg = {}
        for e in begegnung_events:
            figuren = tuple(sorted(e.get("figuren", [])))
            if not figuren:
                continue
            intensitaet = e.get("intensitaet", "")
            old_int = best_beg.get(figuren, {}).get("intensitaet", "")
            old_idx = intensitaet_order.index(old_int) if old_int in intensitaet_order else -1
            new_idx = intensitaet_order.index(intensitaet) if intensitaet in intensitaet_order else -1
            if new_idx > old_idx:
                best_beg[figuren] = e
        for figuren, e in sorted(best_beg.items()):
            fig_str = " + ".join(figuren)
            print(f"- {fig_str}: **{e.get('intensitaet', '?')}** (K{e.get('kapitel', '?')})")
    else:
        print("*Keine Begegnungen bis hierher.*")
    print()

    # --- Wohnorte aktuell ---
    print("## Wohnorte aktuell")
    wohnort_events = [e for e in events_until
                      if "wohnort" in e.get("typen", [])]
    if wohnort_events:
        # Last per figur
        latest = {}
        for e in wohnort_events:
            figur = e.get("figur", "?")
            latest[figur] = e  # events are sorted, so last wins
        for figur in sorted(latest):
            e = latest[figur]
            ort = e.get("ort", "?")
            stadt = e.get("stadt", "")
            stadt_str = f", {stadt}" if stadt else ""
            print(f"- {figur}: {ort}{stadt_str} (seit K{e.get('kapitel', '?')})")
    else:
        print("*Keine Wohnort-Events.*")
    print()

    # --- Phase-specific extras ---
    if args.phase == "ausarbeitung":
        print("## Beziehungsstatus")
        # All begegnung events until now, highest intensity per pair
        if begegnung_events:
            intensitaet_order = ["fluechtig", "bekannt", "vertraut", "intim"]
            best_beg = {}
            for e in begegnung_events:
                figuren = tuple(sorted(e.get("figuren", [])))
                if not figuren:
                    continue
                intensitaet = e.get("intensitaet", "")
                old_int = best_beg.get(figuren, {}).get("intensitaet", "")
                old_idx = intensitaet_order.index(old_int) if old_int in intensitaet_order else -1
                new_idx = intensitaet_order.index(intensitaet) if intensitaet in intensitaet_order else -1
                if new_idx > old_idx:
                    best_beg[figuren] = e
            for figuren, e in sorted(best_beg.items()):
                fig_str = " + ".join(figuren)
                detail = e.get("detail", "")
                detail_str = f" — {detail[:120]}…" if detail and len(detail) > 120 else (f" — {detail}" if detail else "")
                print(f"- {fig_str}: **{e.get('intensitaet', '?')}** (K{e.get('kapitel', '?')}){detail_str}")
        else:
            print("*Keine Begegnungs-Events.*")
        print()


if __name__ == "__main__":
    main()
