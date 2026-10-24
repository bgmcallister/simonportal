#!/usr/bin/env python3
import pathlib, re, html, os
BASE = pathlib.Path.home() / "workspace/sites/portal-restored-build"
# --- Miles restore: original files intact under _ellellem/_persona_miles ---
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
miles_html = (pathlib.Path.home() / "workspace/portal-batch2/_persona_miles/miles.html").read_text(encoding="utf-8", errors="ignore")
miles_md = (pathlib.Path.home() / "workspace/portal-batch2/_persona_miles/miles.md").read_text(encoding="utf-8", errors="ignore")
miles_txt = strip_html(miles_html)
miles_md_txt = strip_md(miles_md)
dest = BASE / "html" / "_ellellem" / "_persona_miles"
dest.mkdir(parents=True, exist_ok=True)
# html version: ORIGINAL miles.html intact, no stripping, no nav injection (it is the persona page itself)
(dest / "miles.html").write_text(miles_html, encoding="utf-8")
# md version of miles.html, plus original miles.md as its own document
(BASE / "md" / "_ellellem" / "_persona_miles").mkdir(parents=True, exist_ok=True)
(BASE / "md" / "_ellellem" / "_persona_miles" / "miles.md").write_text(miles_txt, encoding="utf-8")
(BASE / "md" / "_ellellem" / "_persona_miles" / "miles-note.md").write_text(miles_md, encoding="utf-8")
(BASE / "txt" / "_ellellem" / "_persona_miles").mkdir(parents=True, exist_ok=True)
(BASE / "txt" / "_ellellem" / "_persona_miles" / "miles.txt").write_text(miles_txt, encoding="utf-8")
(BASE / "txt" / "_ellellem" / "_persona_miles" / "miles-note.txt").write_text(miles_md_txt, encoding="utf-8")
# html version of miles.md note
(BASE / "html" / "_ellellem" / "_persona_miles" / "miles-note.html").write_text(f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>miles-note</title></head><body><pre>{html.escape(miles_md)}</pre></body></html>", encoding="utf-8")
print("miles restored to _ellellem/_persona_miles, original html intact")

# --- nav.html: single source frame file, absolute Pages paths ---
# collect html documents, excluding old miles locations
docs = []
for p in sorted((BASE / "html").rglob("*.html")):
    rel = str(p.relative_to(BASE / "html"))
    if rel == "index.html": continue
    if "_persona_spec/miles.html" in rel or "_user/miles.html" in rel: continue
    docs.append(rel)
# add miles-note already in docs via rglob
lines = ["<!DOCTYPE html><html><head><meta charset='utf-8'><title>Portal navigation</title><style>body{font-family:Georgia,serif;padding:12px;line-height:1.5} a{color:#004080} details{margin:6px 0} summary{cursor:pointer;padding:6px;background:#eef2f7}</style></head><body><h1>Portal</h1><p><a href='/simonportal/index.html' target='_parent'>Portal home</a></p>"]
from collections import defaultdict
by_folder = defaultdict(list)
for rel in docs:
    folder = os.path.dirname(rel) or "(root)"
    base = re.sub(r"\.html$", "", os.path.basename(rel))
    by_folder[folder].append((base, rel))
for folder in sorted(by_folder):
    lines.append(f"<details><summary>{html.escape(folder)}</summary>")
    for base, rel in sorted(by_folder[folder]):
        md_rel = rel[:-5] + ".md"
        txt_rel = rel[:-5] + ".txt"
        lines.append(f"<p>• {html.escape(base)} - Download: [<a href='/simonportal/md/{md_rel}' target='_parent'>.md</a> || <a href='/simonportal/txt/{txt_rel}' target='_parent'>.txt</a> || <a href='/simonportal/html/{rel}' target='_parent'>.html</a>]</p>")
    lines.append("</details>")
lines.append("</body></html>")
(BASE / "nav.html").write_text("\n".join(lines), encoding="utf-8")
print(f"nav.html written, {len(docs)} documents")

# --- inject frame into every html page (root + format html + tree) ---
FRAME = '<iframe src="/simonportal/nav.html" title="Portal navigation" style="width:100%;height:360px;border:2px solid #004080"></iframe>\n'
count = 0
for p in list(BASE.rglob("*.html")):
    if p.name == "nav.html": continue
    t = p.read_text(encoding="utf-8", errors="ignore")
    if 'src="/simonportal/nav.html"' in t: continue
    if "<body>" in t:
        t = t.replace("<body>", "<body>\n" + FRAME, 1)
        p.write_text(t, encoding="utf-8")
        count += 1
print(f"frame injected into {count} html pages")
