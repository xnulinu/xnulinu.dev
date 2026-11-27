# xnulinu.dev

Personal site + blog. Hand-authored static HTML — no framework, no tracking. The only build step is a small Python script that turns Markdown posts into HTML.

## Layout
```
index.html      who-am-i landing
resume.html     résumé (prints / saves to PDF cleanly)
favicon.svg
Makefile        make blog · make serve · make clean
blog/
  posts/*.md    write posts here
  build.py      Markdown → HTML generator
  diagrams.py   diagram blocks for posts
  template.html post shell
  style.css     shared blog styles
  index.html    generated — list of posts
```

## Develop
```
make serve      # preview the site at http://localhost:8000
make blog       # rebuild blog HTML after editing posts
```
First `make blog` creates a local `.venv` with the one dependency (`markdown`), since system Python is externally managed.

## Write a post
1. Add `blog/posts/YYYY-MM-DD-slug.md` with front matter:
   ```
   ---
   title: The control plane is the product
   date: 2026-07-01
   summary: Why trusted execution, not diagnosis, is the defensible problem.
   ---
   ```
   Diagrams are fenced blocks (see Diagrams below):
   ````text
   ```sets
   Blueprint: the whole production system
   Platform Bricks: GPUs, deployment, networking
   * Your product: scheduler, routing, caching
   ```
   ````
2. `make blog`
3. Commit the generated HTML and push.

## Diagrams
Diagrams and reading features are shared, never per post. Anything a post needs (a new diagram type, a new block style) goes into `blog/diagrams.py` / `blog/build.py` / `blog/style.css` so every post gets it. No hand-written HTML or post-specific CSS in `posts/*.md`.
- Every diagram is a numbered figure (a card on a tinted plate, exactly the width of the text column, so text, hero and figures share one edge). An optional first line `title: …` becomes its caption. `*` marks the one item to emphasise; `[icon]` (after any `*`) adds a glyph from `ICONS` in `diagrams.py` (laptop, cloud, lab, gate, merge, release, agent, person, console, terminal, package, branch, commit, push, check, checks, moon, issue, eye, layers, clock, lock, doc, factory, wrench, repeat, api). An unknown icon fails the build.
- ` ```flow ` — one station per line, left→right with arrows (stacks on phones): `[lab] every safe lab`.
- ` ```sets ` — the "universal set" diagram: first line is the big circle (`Name: optional subtitle`), then 1–4 lines of `Group: item, item`. Keep items short (a few words); phones get a nested-box version automatically.
- ` ```trend ` — a line on a relative log scale, one `<level 0-10> [label]` per line; `*` annotates a point and draws the line after it in the accent. Phones get their own taller drawing.
- ` ```bars ` — relative share, `<weight> <label>` per line; weights are never shown.
- ` ```tiles ` — a ruled grid of mechanisms: `[icon] Title: one short line`.
- ` ```gates ` — layered filters narrowing toward the last one: `[icon] Layer: what it catches, …`.
- ` ```shift ` — before → after: first line `[icon] From head -> [icon] To head`, then `before -> after` rows.
- Post hero images live in `assets/blog/` (1894×830 webp), set with `image:` in front matter. Keep the SVG source next to it when there is one.
- Built in for every post: reading time, section links on `##`/`###` headings, footnotes (`[^1]`), curly quotes, older/newer links at the end.
