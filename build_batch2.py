#!/usr/bin/env python3
import os, re, html, pathlib
SRC = pathlib.Path.home() / "workspace/portal-batch2"
OUT = pathlib.Path.home() / "workspace/sites/portal-restored-build"
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
    return strip_html(t) if suffix == ".html" else (strip_md(t) if suffix == ".md" else t)
def to_md(t, suffix):
    return strip_html(t) if suffix == ".html" else t

count=0
for p in sorted(SRC.rglob("*")):
    if not p.is_file(): continue
    rel = p.relative_to(SRC)
    parts = list(rel.parts)
    if parts[0] == "_big-g-mack":
        parts = ["_ellellem"] + parts
    r = pathlib.Path(*parts)
    base = re.sub(r"\.[^.]+$", "", r.name)
    text = p.read_text(encoding="utf-8", errors="ignore")
    for fmt, content in [
        ("md", to_md(text, p.suffix.lower())),
        ("txt", to_txt(text, p.suffix.lower()) + "\n\nFull navigation: see the portal home index.html and the format trees.\n"),
    ]:
        out = OUT / fmt / r.parent / f"{base}.{fmt}"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    body = html.escape(to_txt(text, p.suffix.lower())[:20000])
    out = OUT / "html" / r.parent / f"{base}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(base)}</title><style>body{{font-family:Georgia,serif;max-width:900px;margin:0 auto;padding:20px;line-height:1.6}} nav{{border:2px solid #004080;padding:12px;margin:16px 0}} pre{{white-space:pre-wrap}}</style></head>
<body>
<nav aria-label="Portal navigation"><p><a href="../../../../index.html">Portal home</a> | <a href="../../../../tree.html">Full file explorer</a></p><p>Format trees: <a href="../../../../md/">md</a> | <a href="../../../../txt/">txt</a> | <a href="../../../../html/">html</a></p></nav>
<main><h1>{html.escape(base)}</h1><pre>{body}</pre></main>
<nav aria-label="Portal navigation"><p><a href="../../../../index.html">Portal home</a> | <a href="../../../../tree.html">Full file explorer</a></p></nav>
</body></html>""", encoding="utf-8")
    count+=1
print(f"batch2 documents: {count}")
# regenerate per-format index lists
for fmt, ext in [("md", ".md"), ("txt", ".txt"), ("html", ".html")]:
    root = OUT / fmt
    lines = [str(p.relative_to(root)) for p in sorted(root.rglob(f"*{ext}")) if p.name != f"index{ext}"]
    if fmt == "html":
        items = "".join(f"<li><a href=\"{html.escape(x)}\">{html.escape(x)}</a></li>" for x in lines)
        (root / "index.html").write_text(f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>HTML tree</title></head><body><h1>HTML format tree</h1><ul>{items}</ul></body></html>", encoding="utf-8")
    elif fmt == "md":
        (root / "index.md").write_text("# MD format tree\n\n" + "\n".join(f"- {x}" for x in lines) + "\n", encoding="utf-8")
    else:
        (root / "index.txt").write_text("TXT format tree\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    print(fmt, len(lines))
