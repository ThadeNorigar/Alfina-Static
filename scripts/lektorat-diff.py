#!/usr/bin/env python3
"""Generiert HTML-Diff-Seiten fuer Lektorats-Aenderungen.

Auto-Discovery: scannt buch/status.json, findet Kapitel mit status in
{'lektorat', 'final'}, ermittelt pro Kapitel den Basis-Commit (letzter
feat(...)-Commit auf der Datei) und generiert einen Diff gegen HEAD.

Rot durchgestrichen = entfernt, gruen = neu, grau = unveraenderte Absaetze.
Output: story-in-work/lektorat-diffs/{ID}.html

Aufruf: python scripts/lektorat-diff.py
"""
import subprocess
import difflib
import os
import re
import html
import json

STATUS_FILE = "buch/status.json"
KAPITEL_DIR = "buch/kapitel"
OUT_DIR = "story-in-work/lektorat-diffs"
HEAD_REF = "HEAD"
LEKTORAT_STATES = {"lektorat", "final"}

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
.commits { margin-top: 0.6rem; font-size: 0.8rem; color: #888; }
"""


def sh(args):
    return subprocess.check_output(args, text=True, encoding="utf-8").strip()


def get_file_at(ref, path):
    try:
        return subprocess.check_output(
            ["git", "show", f"{ref}:{path}"], text=True, encoding="utf-8",
        )
    except subprocess.CalledProcessError:
        return ""


def last_feat_commit(path):
    """Letzter Commit mit Message-Prefix 'feat' auf dieser Datei."""
    try:
        out = subprocess.check_output(
            ["git", "log", "--format=%H %s", HEAD_REF, "--", path],
            text=True, encoding="utf-8",
        )
    except subprocess.CalledProcessError:
        return None
    for line in out.splitlines():
        h, _, msg = line.partition(" ")
        if msg.startswith("feat"):
            return h
    return None


def discover_chapters():
    with open(STATUS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    result = []
    for bkey in ("buch1", "buch2", "buch3"):
        buch = data.get(bkey) or {}
        for kid, ch in (buch.get("kapitel") or {}).items():
            if ch.get("status") in LEKTORAT_STATES and ch.get("datei"):
                path = f"{KAPITEL_DIR}/{ch['datei']}"
                base = last_feat_commit(path)
                if not base:
                    continue
                book_num = bkey[-1]
                cid = f"B{book_num}-K{kid}"
                result.append((cid, path, base))
    return result


def word_level_diff(old_text, new_text):
    old_words = re.split(r"(\s+)", old_text)
    new_words = re.split(r"(\s+)", new_text)
    sm = difflib.SequenceMatcher(a=old_words, b=new_words)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            out.append(html.escape("".join(new_words[j1:j2])))
        elif tag == "replace":
            out.append(f"<del>{html.escape(''.join(old_words[i1:i2]))}</del>"
                       f"<ins>{html.escape(''.join(new_words[j1:j2]))}</ins>")
        elif tag == "delete":
            out.append(f"<del>{html.escape(''.join(old_words[i1:i2]))}</del>")
        elif tag == "insert":
            out.append(f"<ins>{html.escape(''.join(new_words[j1:j2]))}</ins>")
    return "".join(out)


def diff_inline(old_text, new_text):
    old_paras = re.split(r"\n\s*\n", old_text.strip())
    new_paras = re.split(r"\n\s*\n", new_text.strip())
    sm = difflib.SequenceMatcher(a=old_paras, b=new_paras)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for p in new_paras[j1:j2]:
                out.append(f'<p class="unchanged">{html.escape(p)}</p>')
        elif tag == "replace":
            old_block = "\n\n".join(old_paras[i1:i2])
            new_block = "\n\n".join(new_paras[j1:j2])
            out.append(f"<p>{word_level_diff(old_block, new_block)}</p>")
        elif tag == "delete":
            for p in old_paras[i1:i2]:
                out.append(f'<p><del>{html.escape(p)}</del></p>')
        elif tag == "insert":
            for p in new_paras[j1:j2]:
                out.append(f'<p><ins>{html.escape(p)}</ins></p>')
    return "\n".join(out)


def make_nav(chapters):
    parts = ['<a href="../index.html">&larr; story-in-work</a>',
             '<a href="index.html">&larr; Uebersicht</a>']
    for cid, _, _ in chapters:
        parts.append(f'<a href="{cid}.html">{cid}</a>')
    return f'<div class="nav">{" ".join(parts)}</div>'


def render(cid, path, base, all_chapters):
    old = get_file_at(base, path)
    new = get_file_at(HEAD_REF, path)
    body = diff_inline(old, new)
    try:
        log = sh(["git", "log", "--format=%h %s", f"{base}..{HEAD_REF}", "--", path])
    except subprocess.CalledProcessError:
        log = ""
    log_html = "<br>".join(html.escape(l) for l in log.splitlines()) or "(keine Aenderungen seit Basis)"
    nav = make_nav(all_chapters)
    return f"""<!DOCTYPE html>
<html lang="de"><head>
<meta charset="utf-8">
<title>Lektorat-Diff: {cid}</title>
<style>{CSS}</style>
</head><body>
{nav}
<h1>Lektorat-Diff: {cid}</h1>
<div class="meta">Basis: {base[:7]} &middot; Kopf: HEAD</div>
<div class="legend">
  <strong>Legende:</strong>
  <del>geloeschter Text</del> &nbsp; <ins>neuer Text</ins> &nbsp;
  <span class="unchanged">unveraenderte Absaetze</span>
  <div class="commits"><strong>Commits seit Basis:</strong><br>{log_html}</div>
</div>
{body}
</body></html>"""


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    chapters = discover_chapters()
    if not chapters:
        print("Keine Kapitel im Lektorat/Final gefunden.")
        return

    index_links = []
    for cid, path, base in chapters:
        out_path = os.path.join(OUT_DIR, f"{cid}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(render(cid, path, base, chapters))
        index_links.append(f'<li><a href="{cid}.html">{cid}</a></li>')
        print(f"  -> {out_path} (Basis {base[:7]})")

    index_html = f"""<!DOCTYPE html>
<html lang="de"><head>
<meta charset="utf-8">
<title>Lektorat-Diffs</title>
<style>{CSS}</style>
</head><body>
<div class="nav"><a href="../index.html">&larr; story-in-work</a></div>
<h1>Lektorat-Diffs</h1>
<div class="meta">Alle Kapitel im Lektorats- oder Final-Status. Diff gegen letzten feat-Commit.</div>
<ul>{"".join(index_links)}</ul>
</body></html>"""
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"  -> {OUT_DIR}/index.html")


if __name__ == "__main__":
    main()
