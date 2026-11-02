# Portal clean rebuild — build report (LOCAL ONLY, 2026-11-01)

No push to GitHub. No deletions from any repo, Drive, or local source tree.
No edits to the live site. Source trees `portal-dironly`, `portal-restored-build`,
`portal-renamed`, and `portal-co-sovereign-push` were read only, never overwritten.

## Source

- Base: `~/workspace/sites/portal-dironly/` (md 114 / txt 114 / html 115)
- Plus: `~/workspace/sites/portal-co-sovereign-push/` — the 3 Triad files only
  (`handshake/co-sovereign-triad-of-constitution` in md, txt, html)
- Plus: root assets copied from the local design source
  `~/workspace/sites/jacobzimmerly-github-io/assets/` — `avatar-jacob.webp`
  (85,496 B), `avatar-muse.webp` (74,702 B), `station-v16.webp` (352,502 B).
  The station hash matches the copy already in `portal-restored-build` and the
  loose `assets-station-copy.webp` in dironly, so no live fetch was needed.
- Output: `~/workspace/sites/portal-clean-2026-11-01/` — 357 files, 9.8 MB.

## File counts in the clean tree

| Format tree | Files |
|---|---|
| md | 116 (114 content + index.md + index.html) |
| txt | 116 (114 content + index.txt + index.html) |
| html | 116 (115 content + index.html) |
| Root | index.html, nav.html, tree.html, .nojekyll |
| assets/ | avatar-jacob.webp, avatar-muse.webp, station-v16.webp |
| personamiles/ | miles.html, miles.md (root-level copies, carried over unchanged) |

Content bases: 115 (114 with md/txt/html + 1 html-only, see below).

## What was fixed

1. **Internal header nav (the main breakage).** Every html file's fixed
   `../../../../` prefix was replaced with site-absolute `/simonportal/` links,
   so Portal home, Full file explorer (tree.html), and the md / txt / html
   format trees all resolve to the correct live targets regardless of file depth.
   No `../../../../` occurrences remain anywhere in the clean tree.
2. **Truncated html mirrors.** Every html mirror was regenerated in full from
   its md source, preserving the existing template, `<title>`, and `<h1>`.
   Verified: the html `<pre>` text is now byte-identical to the md source for
   all 114 md-backed bases, including all 38 truncated bases from the audit —
   notably `ellellem/gemini/googleai` (277k md, was 20k html),
   `ellellem/big-g-mack/bgmstory/fullstory/bgmstory`,
   `ellellem/big-g-mack/bgmstory/workingdraft/_bgmstory_working_draft`, and
   the 3ptstory / NotebookLM story files. md and txt files are byte-identical
   to their dironly sources (plus the Triad files).
3. **nav.html regenerated from the actual files** in the new tree — no drift.
   115 content rows in 22 directory groups, 344 hrefs. It now includes the
   Triad (3 formats) and the previously unlinked `miles-note` files
   (md/txt/html under `ellellem/personamiles`), with space and non-ASCII
   filenames percent-encoded in links (`gemini instr`, `context urls nc`,
   `español`, `日本語`).
4. **Format-tree and explorer pages that the header nav points at.**
   `md/index.html` and `txt/index.html` were added alongside the existing
   `index.md` / `index.txt` lists, so `/simonportal/md/` and `/simonportal/txt/`
   actually resolve on GitHub Pages (static hosting serves index.html, not
   index.md). `html/index.html` was regenerated from the actual files
   (the old one listed stale underscore paths). Root `tree.html` was generated
   (it existed live but was not in dironly).

## Link-crawl verification (new tree, `/simonportal/` simulated as root)

- Before (audit, live site): 462 of 550 internal header-nav link instances
  resolved to 404.
- After (clean tree, all internal href/src links in all html files, directories
  resolved to their index.html): **1,720 internal links checked, 1,720 OK,
  0 404.** The only 404s found in a first crawl were the two new
  `md/index.html` / `txt/index.html` targets (113 links each); those files
  were then added, and a full re-crawl came back clean.

## What was NOT changed

- No document content changed except html regeneration (full md text) and the
  header-nav links. No deletions, no merges, no renames.
- `handshake/digital-handshake` stays html-only (byte-identical to dironly);
  no md/txt version was invented for it.
- The empty 4-part story was not filled, and no 4-part files were created.
- No old underscore trees (`_handshake`, `_ellellem`, etc.) were copied into
  the clean tree; they remain live in the repo until Jacob approves otherwise.

## Left for Jacob's per-item decision (NOT done here)

1. Duplicate / near-duplicate bgmstory versions: `bgmstory1` (35,352 B) vs
   `bgm-bgmstory1` (78,178 B); `bgmstory3` vs `bgm-bgmstory3` (49 B apart);
   3ptstory `bgmstory2`/`bgmstory3` vs their NotebookLM copies (one identical,
   one the bgm- variant); fullstory (99,582 B) vs the sum of the 3 parts
   (99,045 B); working draft (110,690 B, largest) vs fullstory; ONE/TWO/THREE
   beat-map outlines sitting in the story folder.
2. Old underscore trees and renamed variants still live in the repo but
   unlinked (`_handshake`, `_ellellem`, `aialign`, etc.) — keep live or remove,
   per item.
3. `handshake/digital-handshake` — html-only, live 404, unlinked in the old
   nav (now linked in the clean nav). Decide: publish as-is, add md/txt, or
   leave out.
4. Station-room labels on the home page: Library and Muse's notes both lead
   to nav.html; Jacob's notes leads to the anonymous biography, not the
   user1–user5 notes. (Home page itself was carried over unchanged.)
5. Whether to push this clean tree to the simonportal repo, and whether the
   push should replace or sit alongside the existing live trees.
