#!/usr/bin/env python3
"""Generiert JSON-Dateien pro Lektorats-Kapitel mit allen Commit-Versionen.

Pro Kapitel: alle Commits seit letztem feat(...)-Commit. Pro Version wird der
Delta zum Vorgaenger als fertig gerendertes Prose-HTML gespeichert (mit
<ins>/<del>-Markierungen). Client zeigt das als Inline-Diff an.

Output: story-in-work/lektorat-versions/{ID}.json
Aufruf: python scripts/lektorat-versions.py
"""
import subprocess
import difflib
import html
import json
import os
import re

STATUS_FILE = "buch/status.json"
KAPITEL_DIR = "buch/kapitel"
OUT_DIR = "story-in-work/lektorat-versions"
HEAD_REF = "HEAD"
LEKTORAT_STATES = {"lektorat", "final"}


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


def commits_between(base, head, path):
    """Liste (hash, iso-date, subject) chronologisch aufsteigend."""
    try:
        out = subprocess.check_output(
            ["git", "log", "--reverse", "--format=%H%x09%aI%x09%s",
             f"{base}..{head}", "--", path],
            text=True, encoding="utf-8",
        )
    except subprocess.CalledProcessError:
        return []
    result = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) == 3:
            result.append(tuple(parts))
    return result


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
                result.append((cid, ch["datei"], path, base, kid))
    return result


# --- Markdown-Rendering (spiegelt renderProsa() aus lesen/_reader.html) ---

_EM_RE = re.compile(r"\*([^*]+)\*")


def _inline(line):
    esc = html.escape(line)
    # re-apply italics after escape
    return _EM_RE.sub(r"<em>\1</em>", esc)


def md_to_paragraphs(md_text):
    """Liefert Liste von (css_class, inner_html, raw_text) analog zum Reader.

    raw_text wird fuer den Diff-Vergleich benutzt (ohne HTML-Tags).
    """
    paras = []
    lines = md_text.split("\n")
    is_first = True
    skip_title = True
    for raw in lines:
        line = raw.strip()
        if skip_title and line.startswith("# "):
            skip_title = False
            continue
        if line == "":
            continue
        if line == "---":
            paras.append(("scene-break", "&middot; &middot; &middot;", "---"))
            is_first = True
            continue
        if line.startswith("#"):
            continue
        processed = _inline(line)
        is_dialog = line.startswith('"') or line.startswith("\u201e") or line.startswith("\u00ab")
        is_date_line = is_first and re.match(r"^\*[^*]+\*$", line)
        if is_date_line:
            cls = "date-line"
        elif is_first:
            cls = "opening"
            is_first = False
        elif is_dialog:
            cls = "dialog"
        else:
            cls = ""
        paras.append((cls, processed, line))
    return paras


# --- Diff-Rendering ---

def _word_tokens(text):
    return re.split(r"(\s+)", text)


def _word_diff_inline(old_text, new_text):
    """Word-level Diff innerhalb eines Absatzes; return HTML mit <del>/<ins>."""
    old_w = _word_tokens(old_text)
    new_w = _word_tokens(new_text)
    sm = difflib.SequenceMatcher(a=old_w, b=new_w)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            out.append(_inline("".join(new_w[j1:j2])).replace("&amp;middot;", "&middot;"))
        elif tag == "delete":
            out.append(f"<del>{_inline(''.join(old_w[i1:i2]))}</del>")
        elif tag == "insert":
            out.append(f"<ins>{_inline(''.join(new_w[j1:j2]))}</ins>")
        elif tag == "replace":
            out.append(f"<del>{_inline(''.join(old_w[i1:i2]))}</del>"
                       f"<ins>{_inline(''.join(new_w[j1:j2]))}</ins>")
    return "".join(out)


def render_diff_html(old_paras, new_paras):
    """Liefert HTML-String mit <p>-Absaetzen und <div class='diff-deleted'>-Bloecken.

    Kommentar-kompatibel: nur <p>-Elemente werden vom Reader-Kommentar-System
    gezaehlt. Geloeschte Bloecke sind <div> und werden ignoriert.
    """
    a_texts = [p[2] for p in old_paras]
    b_texts = [p[2] for p in new_paras]
    sm = difflib.SequenceMatcher(a=a_texts, b=b_texts)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(j1, j2):
                cls, inner, _ = new_paras[k]
                cls_attr = f' class="{cls}"' if cls else ""
                out.append(f"<p{cls_attr}>{inner}</p>")
        elif tag == "delete":
            for k in range(i1, i2):
                cls, _, raw = old_paras[k]
                cls_attr = f' class="diff-deleted-block {cls}"' if cls else ' class="diff-deleted-block"'
                out.append(f'<div{cls_attr}><del>{_inline(raw)}</del></div>')
        elif tag == "insert":
            for k in range(j1, j2):
                cls, inner, _ = new_paras[k]
                extra = " diff-inserted" if cls else "diff-inserted"
                cls_attr = f' class="{cls} diff-inserted"' if cls else ' class="diff-inserted"'
                out.append(f'<p{cls_attr}><ins>{inner}</ins></p>')
        elif tag == "replace":
            # Paarweise mappen: erste new_paras mit old_paras als word-diff,
            # ueberschuessige old als delete-block, ueberschuessige new als insert.
            old_block = old_paras[i1:i2]
            new_block = new_paras[j1:j2]
            pair_n = min(len(old_block), len(new_block))
            for k in range(pair_n):
                cls, _, new_raw = new_block[k]
                old_raw = old_block[k][2]
                inner = _word_diff_inline(old_raw, new_raw)
                cls_attr = f' class="{cls}"' if cls else ""
                out.append(f"<p{cls_attr}>{inner}</p>")
            # Rest old als gelöscht
            for k in range(pair_n, len(old_block)):
                cls, _, raw = old_block[k]
                cls_attr = f' class="diff-deleted-block {cls}"' if cls else ' class="diff-deleted-block"'
                out.append(f'<div{cls_attr}><del>{_inline(raw)}</del></div>')
            # Rest new als eingefügt
            for k in range(pair_n, len(new_block)):
                cls, inner, _ = new_block[k]
                cls_attr = f' class="{cls} diff-inserted"' if cls else ' class="diff-inserted"'
                out.append(f'<p{cls_attr}><ins>{inner}</ins></p>')
    return "\n".join(out)


def build_versions(path, base):
    commits = commits_between(base, HEAD_REF, path)
    if not commits:
        return []
    # Basis-Paragraphen
    prev_md = get_file_at(base, path)
    prev_paras = md_to_paragraphs(prev_md)

    versions = []
    for h, iso, subject in commits:
        curr_md = get_file_at(h, path)
        curr_paras = md_to_paragraphs(curr_md)
        diff_html = render_diff_html(prev_paras, curr_paras)
        versions.append({
            "hash": h,
            "short": h[:7],
            "date": iso,
            "message": subject,
            "diffHtml": diff_html,
        })
        prev_paras = curr_paras
    return versions


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    chapters = discover_chapters()
    if not chapters:
        print("Keine Kapitel im Lektorat/Final gefunden.")
        return

    index = []
    for cid, datei, path, base, kid in chapters:
        versions = build_versions(path, base)
        data = {
            "kapitel_id": cid,
            "slug": kid,
            "datei": datei,
            "base": base[:7],
            "versions": versions,
        }
        out_path = os.path.join(OUT_DIR, f"{cid}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        index.append({"id": cid, "slug": kid, "versions": len(versions)})
        print(f"  -> {out_path} ({len(versions)} Versionen)")

    with open(os.path.join(OUT_DIR, "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=1)
    print(f"  -> {OUT_DIR}/index.json")


if __name__ == "__main__":
    main()
