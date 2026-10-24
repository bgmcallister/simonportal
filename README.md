# simonportal

A portal and file hub for a long-running story and AI collaboration project.

## What is here

- A directory and file tree, generated from the actual files in this repo,
  not hand-typed, so it cannot drift from what is really here.
- Every document in three versions: `.md`, `.txt`, and `.html`,
  listed side by side as `Download: [.md || .txt || .html]`.
- A full file explorer on the home page and on `tree.html`.
- A compact navigation block on every document page, with a link
  to the full explorer.
- `llms.txt`, a plain list of every document set, for AI readers
  that want a map without re-reading the whole tree on every page.

## How to read it

Start at `index.html`. Open a folder in the tree, pick a document,
and choose the format that fits: `.html` for browsing with navigation,
`.txt` for clean reading with no navigation noise, `.md` for the
plain-text source version.

## What is not here yet

- The bio section is held out until a redacted, anonymous version
  is written. Only identifying personal bio details are redacted;
  story and other project material is included in full.
- The four-part story folder is empty on purpose, awaiting a
  word-for-word rebuild from its original source.

The tree on every page is stamped in one build run from a single
master tree, so a change to the tree updates all pages together.
