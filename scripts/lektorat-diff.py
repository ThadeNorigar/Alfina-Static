#!/usr/bin/env python3
"""Generiert HTML-Diff-Seiten fuer Lektorats-Aenderungen.

Zeigt geloeschte Stellen rot durchgestrichen, neue Stellen gruen markiert.
Output: story-in-work/lektorat-diffs/{ID}.html

Aufruf: python scripts/lektorat-diff.py
"""
import subprocess
import difflib
import os
import re
import html

# Mapping: Kapitel-ID -> (Datei, Basis-Commit)
# Basis = der erste Lektorats-Commit dieser Session. Kopf ist IMMER HEAD,
# damit spaetere Folge-Commits (auch manuelle) automatisch mit angezeigt werden.
CHAPTERS = [
    ("B1-K17", "buch/kapitel/B1-K17-maren.md", "f49dd66"),
    ("B1-K18", "buch/kapitel/B1-K18-vesper.md", "f46be4e"),
    ("B1-K19", "buch/kapitel/B1-K19-alle.md", "fa62366"),
    ("B1-K20", "buch/kapitel/B1-K20-maren.md", "a294a00"),
    ("B1-K21", "buch/kapitel/B1-K21-alphina.md", "40ab43b"),
    ("B1-K22", "buch/kapitel/B1-K22-maren.md", "b67cd9b"),
]
HEAD_REF = "HEAD"

OUT_DIR = "story-in-work/lektorat-diffs"

CSS = """
body { font-family: Georgia, serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; line-height: 1.7; color: #222; background: #fafaf7; }
h1 { font-size: 1.4rem; margin-bottom: 0.3rem; }
.meta { color: #888; font-size: 0.85rem; margin-bottom: 2rem; }
.legend { background: #fff; border: 1px solid #ddd; padding: 0.6rem 1rem; margin-bottom: 2rem; font-size: 0.9rem; border-radius: 4px; }
del { background: #fee; color: #b00; text-decoration: line-through; padding: 1px 2px; }
ins { background: #efe; color: #060; text-decoration: none; padding: 1px 2px; }
p { margin: 0.7em 0; }
hr { border: none; border-top: 1px solid #ccc; margin: 1.5rem 0; }
.unchanged { color: #666; }
.nav { margin-bottom: 1.5rem; }
.nav a { margin-right: 1rem; color: #06c; text-decoration: none; font-size: 0.9rem; }
"""

def get_file_at(commit, path):
    """Liest Dateiinhalt aus einem git commit."""
    try:
        return subprocess.check_output(
            ["git", "show", f"{commit}:{path}"],
            text=True,
            encoding="utf-8",
        )
    except subprocess.CalledProcessError:
        return ""

def diff_inline(old_text, new_text):
    """Erzeugt HTML mit <del>/<ins> fuer Wort-Diffs innerhalb von Absaetzen."""
    # Splitte beide Texte in Absaetze (Doppel-Newline)
    old_paras = re.split(r"\n\s*\n", old_text.strip())
    new_paras = re.split(r"\n\s*\n", new_text.strip())

    # SequenceMatcher auf Absatz-Ebene
    sm = difflib.SequenceMatcher(a=old_paras, b=new_paras)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for p in new_paras[j1:j2]:
                out.append(f'<p class="unchanged">{html.escape(p)}</p>')
        elif tag == "replace":
            # Bei Ersetzung: Wort-Diff innerhalb der Absaetze
            old_block = "\n\n".join(old_paras[i1:i2])
            new_block = "\n\n".join(new_paras[j1:j2])
            word_diff = word_level_diff(old_block, new_block)
            out.append(f"<p>{word_diff}</p>")
        elif tag == "delete":
            for p in old_paras[i1:i2]:
                out.append(f'<p><del>{html.escape(p)}</del></p>')
        elif tag == "insert":
            for p in new_paras[j1:j2]:
                out.append(f'<p><ins>{html.escape(p)}</ins></p>')
    return "\n".join(out)

def word_level_diff(old_text, new_text):
    """Diff auf Wort-Ebene mit <del>/<ins>."""
    old_words = re.split(r"(\s+)", old_text)
    new_words = re.split(r"(\s+)", new_text)
    sm = difflib.SequenceMatcher(a=old_words, b=new_words)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            out.append(html.escape("".join(new_words[j1:j2])))
        elif tag == "replace":
            old_chunk = html.escape("".join(old_words[i1:i2]))
            new_chunk = html.escape("".join(new_words[j1:j2]))
            out.append(f"<del>{old_chunk}</del><ins>{new_chunk}</ins>")
        elif tag == "delete":
            out.append(f"<del>{html.escape(''.join(old_words[i1:i2]))}</del>")
        elif tag == "insert":
            out.append(f"<ins>{html.escape(''.join(new_words[j1:j2]))}</ins>")
    return "".join(out)

def make_nav():
    parts = ['<a href="../index.html">&larr; story-in-work</a>']
    for kid, _, _ in CHAPTERS:
        parts.append(f'<a href="{kid}.html">{kid}</a>')
    return f'<div class="nav">{" ".join(parts)}</div>'

def render(kid, path, base):
    old = get_file_at(f"{base}^", path)
    new = get_file_at(HEAD_REF, path)
    body = diff_inline(old, new)

    # Liste aller Commits zwischen Basis^ und HEAD, die diese Datei veraendert haben
    log = subprocess.check_output(
        ["git", "log", "--format=%h %s", f"{base}^..{HEAD_REF}", "--", path],
        text=True, encoding="utf-8",
    ).strip()

    nav = make_nav()
    log_html = "<br>".join(html.escape(line) for line in log.splitlines()) or "(keine Aenderungen)"
    html_out = f"""<!DOCTYPE html>
<html lang="de"><head>
<meta charset="utf-8">
<title>Lektorat-Diff: {kid}</title>
<style>{CSS}</style>
</head><body>
{nav}
<h1>Lektorat-Diff: {kid}</h1>
<div class="meta">Basis: {base}^ &middot; Kopf: HEAD</div>
<div class="legend">
  <strong>Legende:</strong>
  <del>geloeschter Text</del> &nbsp; <ins>neuer Text</ins> &nbsp;
  <span class="unchanged">unveraenderte Absaetze</span>
  <div style="margin-top:0.6rem;font-size:0.8rem;color:#888;"><strong>Commits in diesem Bereich:</strong><br>{log_html}</div>
</div>
{body}
</body></html>"""
    return html_out

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # Index-Seite
    index_links = []
    for kid, path, base in CHAPTERS:
        out_path = os.path.join(OUT_DIR, f"{kid}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(render(kid, path, base))
        index_links.append(f'<li><a href="{kid}.html">{kid}</a></li>')
        print(f"  -> {out_path}")

    index_html = f"""<!DOCTYPE html>
<html lang="de"><head>
<meta charset="utf-8">
<title>Lektorat-Diffs</title>
<style>{CSS}</style>
</head><body>
<h1>Lektorat-Diffs</h1>
<div class="meta">Aenderungen aus dem aktuellen Lektorats-Durchgang</div>
<ul>{"".join(index_links)}</ul>
</body></html>"""
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"  -> {OUT_DIR}/index.html")

if __name__ == "__main__":
    main()
