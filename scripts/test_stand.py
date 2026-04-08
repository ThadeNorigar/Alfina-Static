"""
Tests fuer scripts/stand.py — Replay-Falter fuer Wohnorte / Begegnungen / Wissen.

Strategie: synthetische Fixtures (kleine Inline-Strukturen),
keine Abhaengigkeit zur echten zeitleiste.json oder status.json.
Damit bleiben die Tests deterministisch und schnell.
"""

import unittest
from stand import (
    extract_events,
    lesereihenfolge,
    kapitel_position,
    filter_until,
    build_snapshot,
    format_snapshot,
)


def fixture_status():
    """Minimal status.json mit Lesereihenfolge fuer 4 Kap + 2 Interludien."""
    return {
        "buch1": {
            "akte": [
                {"titel": "Anker", "kapitel": ["01", "02", "I1", "03", "04", "I2", "05"]},
                {"titel": "Zusammenfinden", "kapitel": ["06", "07"]},
            ],
        }
    }


def fixture_zeitleiste():
    """Minimal zeitleiste.json mit allen drei Event-Typen, ueber zwei Monate verteilt."""
    return {
        "meta": {},
        "typen": {},
        "monate": [
            {
                "label": "M1",
                "events": {
                    "sync": {"label": "x"},
                    "thalassien": [
                        {
                            "tz": 551, "mz": 0, "kapitel": "01",
                            "typen": ["wohnort"],
                            "figur": "Alphina", "ort": "Velde-Wohnung", "stadt": "Velde",
                            "titel": "Alphina in Velde",
                        },
                        {
                            "tz": 551, "mz": 0, "kapitel": "03",
                            "typen": ["wohnort"],
                            "figur": "Alphina", "ort": "Anker", "stadt": "Vael",
                            "titel": "Alphina bezieht den Anker",
                        },
                        {
                            "tz": 551, "mz": 0, "kapitel": "03",
                            "typen": ["begegnung"],
                            "figuren": ["Alphina", "Runa"],
                            "intensitaet": "fluechtig",
                            "ort": "Druckerei",
                            "titel": "Alphina trifft Runa",
                        },
                        {
                            "tz": 551, "mz": 0, "kapitel": "05",
                            "typen": ["begegnung"],
                            "figuren": ["Alphina", "Runa"],
                            "intensitaet": "bekannt",
                            "ort": "Garten",
                            "titel": "Alphina trifft Runa erneut",
                        },
                        {
                            "tz": 551, "mz": 0, "kapitel": "04",
                            "typen": ["wissen"],
                            "figur": "Maren", "fakt": "schemen-am-boot", "stufe": "ahnt",
                            "titel": "Maren ahnt etwas",
                        },
                        {
                            "tz": 551, "mz": 0, "kapitel": "05",
                            "typen": ["wissen"],
                            "figur": "Maren", "fakt": "schemen-am-boot", "stufe": "gesehen",
                            "titel": "Maren sieht die Schemen",
                        },
                        {
                            "tz": 551, "mz": 0, "kapitel": "07",
                            "typen": ["wissen"],
                            "figur": "Maren", "fakt": "schemen-am-boot", "stufe": "versteht",
                            "titel": "Maren versteht (zu spaet fuer cutoff=05)",
                        },
                    ],
                    "moragh": [],
                },
            }
        ],
    }


class TestLesereihenfolge(unittest.TestCase):
    def test_includes_interludes_in_order(self):
        order = lesereihenfolge(fixture_status(), "buch1")
        self.assertEqual(
            order, ["01", "02", "I1", "03", "04", "I2", "05", "06", "07"]
        )

    def test_kapitel_position_returns_index(self):
        order = lesereihenfolge(fixture_status(), "buch1")
        self.assertEqual(kapitel_position(order, "01"), 0)
        self.assertEqual(kapitel_position(order, "I1"), 2)
        self.assertEqual(kapitel_position(order, "07"), 8)

    def test_kapitel_position_unknown_raises(self):
        order = lesereihenfolge(fixture_status(), "buch1")
        with self.assertRaises(KeyError):
            kapitel_position(order, "99")


class TestExtractEvents(unittest.TestCase):
    def test_flattens_thalassien_and_moragh(self):
        z = fixture_zeitleiste()
        z["monate"][0]["events"]["moragh"] = [
            {"tz": 1, "mz": 0, "kapitel": "01", "typen": ["hintergrund"], "titel": "moragh-event"}
        ]
        events = extract_events(z)
        self.assertEqual(len(events), 8)  # 7 thal + 1 mor

    def test_skips_sync(self):
        events = extract_events(fixture_zeitleiste())
        # sync ist nur ein label, kein event mit kapitel
        for e in events:
            self.assertIn("kapitel", e)


class TestFilterUntil(unittest.TestCase):
    def test_excludes_later_chapters(self):
        z = fixture_zeitleiste()
        order = lesereihenfolge(fixture_status(), "buch1")
        events = filter_until(extract_events(z), "05", order)
        # alle ausser dem 07er-event sollten drin sein
        kaps = [e["kapitel"] for e in events]
        self.assertNotIn("07", kaps)
        self.assertIn("05", kaps)
        self.assertIn("04", kaps)

    def test_includes_interlude_when_cutoff_after(self):
        z = fixture_zeitleiste()
        z["monate"][0]["events"]["thalassien"].append(
            {"tz": 551, "mz": 0, "kapitel": "I1", "typen": ["hintergrund"], "titel": "I1-event"}
        )
        order = lesereihenfolge(fixture_status(), "buch1")
        # Cutoff 03: I1 (pos 2) liegt vor 03 (pos 3), muss enthalten sein
        events = filter_until(extract_events(z), "03", order)
        kaps = [e["kapitel"] for e in events]
        self.assertIn("I1", kaps)


class TestBuildSnapshot(unittest.TestCase):
    def test_wohnort_takes_latest(self):
        z = fixture_zeitleiste()
        order = lesereihenfolge(fixture_status(), "buch1")
        snap = build_snapshot(extract_events(z), "05", order)
        # Alphina hatte zwei Wohnorte: Velde (01) und Anker (03). Cutoff 05 → Anker.
        self.assertEqual(snap["wohnorte"]["Alphina"]["ort"], "Anker")
        self.assertEqual(snap["wohnorte"]["Alphina"]["seit_kapitel"], "03")

    def test_wohnort_first_only(self):
        z = fixture_zeitleiste()
        order = lesereihenfolge(fixture_status(), "buch1")
        snap = build_snapshot(extract_events(z), "01", order)
        # Cutoff 01: nur Velde, nicht Anker
        self.assertEqual(snap["wohnorte"]["Alphina"]["ort"], "Velde-Wohnung")

    def test_begegnung_max_intensitaet(self):
        z = fixture_zeitleiste()
        order = lesereihenfolge(fixture_status(), "buch1")
        snap = build_snapshot(extract_events(z), "05", order)
        # Alphina-Runa: fluechtig (03) und bekannt (05) → max ist bekannt
        key = tuple(sorted(["Alphina", "Runa"]))
        self.assertEqual(snap["begegnungen"][key]["intensitaet"], "bekannt")
        self.assertEqual(snap["begegnungen"][key]["kapitel"], ["03", "05"])

    def test_begegnung_below_cutoff_only(self):
        z = fixture_zeitleiste()
        order = lesereihenfolge(fixture_status(), "buch1")
        snap = build_snapshot(extract_events(z), "03", order)
        key = tuple(sorted(["Alphina", "Runa"]))
        self.assertEqual(snap["begegnungen"][key]["intensitaet"], "fluechtig")

    def test_wissen_max_stufe(self):
        z = fixture_zeitleiste()
        order = lesereihenfolge(fixture_status(), "buch1")
        # Cutoff 05: ahnt (04) + gesehen (05) → max gesehen, NICHT versteht (07)
        snap = build_snapshot(extract_events(z), "05", order)
        key = ("Maren", "schemen-am-boot")
        self.assertEqual(snap["wissen"][key]["stufe"], "gesehen")

    def test_wissen_full_eskalation(self):
        z = fixture_zeitleiste()
        order = lesereihenfolge(fixture_status(), "buch1")
        snap = build_snapshot(extract_events(z), "07", order)
        key = ("Maren", "schemen-am-boot")
        self.assertEqual(snap["wissen"][key]["stufe"], "versteht")


class TestFormatSnapshot(unittest.TestCase):
    def test_format_includes_sections(self):
        z = fixture_zeitleiste()
        order = lesereihenfolge(fixture_status(), "buch1")
        snap = build_snapshot(extract_events(z), "05", order)
        out = format_snapshot(snap, bis="05")
        self.assertIn("WOHNORTE", out)
        self.assertIn("BEGEGNUNGEN", out)
        self.assertIn("WISSEN", out)
        self.assertIn("Alphina", out)
        self.assertIn("Anker", out)


if __name__ == "__main__":
    unittest.main()
