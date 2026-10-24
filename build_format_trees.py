#!/usr/bin/env python3
"""Build format-first portal trees: md/, txt/, html/ each mirroring the
restored tree, one format per directory.
Exclusions (Jacob's rules): bio (not drafted yet), relationship logs,
context scoop family logs, GPT export JSONs, empty files, and the
handshake file with a slur filename (held out, not renamed, pending his call).
"""
import os, re, html, pathlib
SRC = pathlib.Path.home() / "workspace/recovery/markor-drive-copy"
OUT = pathlib.Path.home() / "workspace/sites/portal-restored-build"
EXCLUDE_NAMES = {
    "context scoop.md", "context scoop 2.md",
    "big nigger.md",
    "bmm.md", "bgmsrc4.html", "geminirewrite.txt",
}
def is_excluded(p):
    if p.suffix.lower() == ".json":
        return True
    if p.name in EXCLUDE_NAMES:
        return True
    if p.stat().st_size == 0:
        return True
    if "_gpt_data" in p.parts:
        return True
    if "textlog" in p.name.lower():
        return True
    return False

def rel_restored(p):
    rel = p.relative_to(SRC)
    parts = []
    for part in rel.parts:
        part = part.replace("▶_", "_")
        parts.append(part)
    # loose files at safeguard root were ellellem loose files
    if len(parts) == 1:
        parts = ["_ellellem"] + parts
    return pathlib.Path(*parts)

def strip_html(t):
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", "", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", "", t)
    return html.unescape(t)

def strip_md(t):
    t = re.sub(r"^#{1,6}\s*", "", t, flags=re.M)
    t = re.sub(r"[*_`>]", "", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    return t

def to_txt(t, suffix):
    if suffix == ".html":
        return strip_html(t)
    if suffix == ".md":
        return strip_md(t)
    return t

def to_md(t, suffix):
    if suffix == ".html":
        return strip_html(t)
    return t

docs = []
for p in sorted(SRC.rglob("*")):
    if not p.is_file():
        continue
    if is_excluded(p):
        print("exclude:", p.relative_to(SRC))
        continue
    if p.suffix.lower() not in (".md", ".txt", ".html"):
        continue
    docs.append(p)

print(f"documents: {len(docs)}")
for p in docs:
    text = p.read_text(encoding="utf-8", errors="ignore")
    r = rel_restored(p)
    base = re.sub(r"\.[^.]+$", "", r.name)
    # md
    md_path = OUT / "md" / r.parent / f"{base}.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(to_md(text, p.suffix.lower()), encoding="utf-8")
    # txt
    txt_path = OUT / "txt" / r.parent / f"{base}.txt"
    txt_path.parent.mkdir(parents=True, exist_ok=True)
    txt_path.write_text(to_txt(text, p.suffix.lower()) + "\n\nFull navigation: see the portal home index.html and the format trees.\n", encoding="utf-8")
    # html
    html_path = OUT / "html" / r.parent / f"{base}.html"
    html_path.parent.mkdir(parents=True, exist_ok=True)
    body = html.escape(to_txt(text, p.suffix.lower())[:20000])
    html_path.write_text(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(base)}</title><style>body{{font-family:Georgia,serif;max-width:900px;margin:0 auto;padding:20px;line-height:1.6}} nav{{border:2px solid #004080;padding:12px;margin:16px 0}} pre{{white-space:pre-wrap}}</style></head>
<body>
<nav aria-label="Portal navigation"><p><a href="../../../../index.html">Portal home</a> | <a href="../../../../tree.html">Full file explorer</a></p><p>Format trees: <a href="../../../../md/">md</a> | <a href="../../../../txt/">txt</a> | <a href="../../../../html/">html</a></p></nav>
<main><h1>{html.escape(base)}</h1><pre>{body}</pre></main>
<nav aria-label="Portal navigation"><p><a href="../../../../index.html">Portal home</a> | <a href="../../../../tree.html">Full file explorer</a></p></nav>
</body></html>""", encoding="utf-8")

# per-format tree index pages (simple file lists, in that format)
for fmt, ext in [("md", ".md"), ("txt", ".txt"), ("html", ".html")]:
    root = OUT / fmt
    lines = []
    for p in sorted(root.rglob(f"*{ext}")):
        lines.append(str(p.relative_to(root)))
    if fmt == "html":
        items = "".join(f"<li><a href=\"{html.escape(x)}\">{html.escape(x)}</a></li>" for x in lines)
        (root / "index.html").write_text(f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>HTML tree</title></head><body><h1>HTML format tree</h1><ul>{items}</ul></body></html>", encoding="utf-8")
    elif fmt == "md":
        (root / "index.md").write_text("# MD format tree\n\n" + "\n".join(f"- {x}" for x in lines) + "\n", encoding="utf-8")
    else:
        (root / "index.txt").write_text("TXT format tree\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    print(fmt, len(lines), "files")
