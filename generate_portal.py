#!/usr/bin/env python3
"""Portal prototype builder, from the restored tree.
Master tree source: restored-tree-verified-2026-10-23.md counts + Drive restored listing.
Output: index.html (full explorer), tree.html (same explorer, standalone),
llms.txt (AI map), and one sample document set with .md/.txt/.html versions.
Nav rule (agreed in talk, 2026-10-23): one master tree, build script stamps it
into every HTML page at once; full explorer on the home/tree page; compact
collapsed nav on document pages; .txt versions are clean content with only
a one-line pointer to the full tree, so they never go stale.
"""
import os, html, re, json
OUT = os.path.expanduser("~/workspace/sites/portal-restored-build")
os.makedirs(OUT, exist_ok=True)

# Restored tree, verified 2026-10-23. Folders use underscore names in restored;
# portal display keeps the original triangle names where Jacob used them.
TREE = {
    "_ellellem": {
        "_handshake": ["1_handshake.txt", "2_context.txt", "3_mirrors.txt", "4_fieldnotes.txt", "NEW_HANDSHAKE.md"],
        "_llm_prompts": ["audio_overview_01.md", "big_handshake.md", "big_handshake1.md", "big_handshake2.md"],
        "_chatgpt": ["conversation files (GPT export, _gpt_data)"],
        "_notebooklm": ["bgmstory2.md", "bgmstory3.md", "bgmstory_part1.md", "master_doc.md", "cont_guide.md", "chain_of_title.md", "rules_production.md", "themes_legacy.md"],
        "_muse": [],
        "_gemini": ["googleai.md"],
        "_big-g-mack": {
            "_bgmstory": {
                "_3pt_story": ["bgmstory1.md", "bgm-bgmstory1.md", "bgmstory2.md", "bgm-bgmstory2.md", "bgmstory3.md", "bgm-bgmstory3.md", "ONE.md", "TWO.md", "THREE.md"],
                "_2pt_story": ["story1.md", "story2.md"],
                "_full_story": ["bgmstory.md", "bgmstory.html"],
                "_4pt_story": [],
                "_working_draft": ["_bgmstory_working_draft.md"],
            },
            "_persona_spec": ["miles.html"],
            "_persona_rico": ["rico.html"],
        },
    },
    "_user": {
        "_biography": [],
        "_life_other": [],
        # _relationship_logs deliberately out of the public tree for now,
        # pending Jacob's call, like the bio. Names only were in the
        # prototype; removed before the first push to simonportal.
    },
}

def esc(s):
    return html.escape(s)

def render_tree(node, path=""):
    lines = []
    for name, val in node.items():
        p = f"{path}/{name}" if path else name
        if isinstance(val, dict):
            inner = render_tree(val, p)
            lines.append(f'<details><summary>{esc(name)}</summary>\n{inner}</details>')
        else:
            lines.append(f'<details><summary>{esc(name)}</summary>')
            if not val:
                lines.append('<p class="empty">Empty for now.</p>')
            for f in val:
                base = re.sub(r"\.[^.]+$", "", f)
                lines.append(f'<p class="file">• {esc(f)} - Download: [<a href="#">{esc(base)}.md</a> || <a href="#">{esc(base)}.txt</a> || <a href="#">{esc(base)}.html</a>]</p>')
            lines.append('</details>')
    return "\n".join(lines)

FULL_TREE = render_tree(TREE)
COMPACT_NAV = f'''<nav aria-label="Portal navigation" id="site-nav">
<p><a href="index.html">Portal home</a> | <a href="tree.html">Full file explorer</a></p>
<details><summary>▷_ellellem</summary><p>See the full explorer for every folder and document.</p></details>
<details><summary>▶_user</summary><p>See the full explorer for every folder and document.</p></details>
</nav>'''

CSS = """body{font-family:Georgia,serif;max-width:900px;margin:0 auto;padding:20px;line-height:1.6;color:#222}
a{color:#004080} details{margin:8px 0} summary{font-size:1.2em;cursor:pointer;padding:8px;background:#eef2f7}
.file{margin:6px 0 6px 24px;font-size:1.1em} .empty{margin-left:24px;color:#666}
nav{border:2px solid #004080;padding:12px;margin:16px 0} main{margin-top:20px}
"""

def page(title, body, nav):
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><style>{CSS}</style></head>
<body>
{nav}
<main>
<h1>{esc(title)}</h1>
{body}
</main>
<footer>
{nav}
<p>Portal prototype, built from Drive muse/restored, 2026-10-23. Bio stays out until the anonymous version is written together.</p>
</footer>
</body></html>"""

index_body = f"""<p>Station image goes at the top here in the finished portal. Below it is the full file explorer for the whole portal, in your format: folder, then file, then Download: [.md || .txt || .html].</p>
{FULL_TREE}
<p>Note: _4pt_story is empty here on purpose. You are rebuilding it yourself from the Gemini Notebook, word for word, and it will be filled in from your rebuild, not from anywhere else.</p>"""

with open(os.path.join(OUT, "index.html"), "w") as f:
    f.write(page("Portal", index_body, COMPACT_NAV))
with open(os.path.join(OUT, "tree.html"), "w") as f:
    f.write(page("Full file explorer", FULL_TREE, COMPACT_NAV))

# llms.txt: AI map, one line per document set
llms = ["# Portal - llms.txt", "# One line per document set. .txt versions are clean content, no nav.", ""]
def walk(node, path=""):
    for name, val in node.items():
        p = f"{path}/{name}" if path else name
        if isinstance(val, dict):
            walk(val, p)
        else:
            for f in val:
                base = re.sub(r"\.[^.]+$", "", f)
                llms.append(f"{p}/{base}: {base}.md | {base}.txt | {base}.html")
walk(TREE)
with open(os.path.join(OUT, "llms.txt"), "w") as f:
    f.write("\n".join(llms) + "\n")

# Sample document set: bgmstory part 1, from the restored 3-part copy already on disk
src = os.path.expanduser("~/workspace/recovery/inspect-2026-10-23/root1.txt")
doc_dir = os.path.join(OUT, "docs", "_ellellem", "_big-g-mack", "_bgmstory", "_3pt_story")
os.makedirs(doc_dir, exist_ok=True)
if os.path.exists(src):
    text = open(src, encoding="utf-8", errors="ignore").read()
    md = text
    txt = re.sub(r"[#>*`_]", "", text)
    html_body = "<pre>" + esc(text[:4000]) + "</pre><p>Full text in the .md and .txt versions.</p>"
    open(os.path.join(doc_dir, "bgmstory1.md"), "w").write(md)
    open(os.path.join(doc_dir, "bgmstory1.txt"), "w").write(txt + "\n\nFull navigation: see tree.html in the portal root.\n")
    open(os.path.join(doc_dir, "bgmstory1.html"), "w").write(page("bgmstory1 - Story Part One", html_body, COMPACT_NAV))
    print("sample: bgmstory1 set written")
print("index.html, tree.html, llms.txt written to", OUT)
