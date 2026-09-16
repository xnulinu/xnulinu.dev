# Repo notes

A hand-authored static personal site + blog. No framework, no tracking; the only build step is the blog generator.

## Structure
- `index.html` — landing / "who am i"
- `resume.html` — résumé (work, credentials, expertise)
- `blog/` — writing. `posts/*.md` → `build.py` → `*.html` + `index.html`
- `favicon.svg`, `CNAME`, `.nojekyll`

## Blog

**Voice: short, to the point, and personal.** The author's own words, first person. No corporate filler, no LLM throat-clearing ("In this post we will…"), no padding to hit a length. If a sentence isn't earning its place, cut it. One clear idea per post, said plainly.

**Analyze drafts, don't ghost-write.** When a post is drafted (a new/edited file in `blog/posts/`), review it and give honest feedback:
- Is it short and tight? Flag fluff, repetition, hedging, and any paragraph that could be one sentence.
- Does it sound like the author — personal and direct — or generic?
- Is the core point clear and up front?
- Call out anything unclear, unsupported, or that buries the lede.

Suggest specific cuts/edits; don't rewrite it into a different voice. The point is to make the author's writing sharper, not replace it.

**Writing a post:** add `blog/posts/YYYY-MM-DD-slug.md` with front matter (`title`, `date`, `summary`), then `make blog`. The build also refreshes the "recent writing" list on `index.html` (between the `recent-posts` markers — don't hand-edit inside them). It also stamps `?v=<hash>` on the CSS/JS links of every page so browsers never mix a new page with a stale stylesheet — run it after touching `theme.css`, `theme.js` or `blog/style.css`.

**Diagrams and reading features are shared, never per post.** Anything a post needs (a new diagram type, a new block style) goes into `blog/diagrams.py` / `blog/build.py` / `blog/style.css` so every post gets it. No hand-written HTML or post-specific CSS in `posts/*.md`.
- ` ```flow ` — one step per line, left→right (stacks on phones). Prefix a step with `*` to highlight it.
- ` ```sets ` — the "universal set" diagram: first line is the big circle (`Name: optional subtitle`), then 1–4 lines of `Group: item, item`. Prefix a group with `*` to highlight it. Keep items short (a few words); phones get a nested-box version automatically.
- Built in for every post: reading time, section links on `##`/`###` headings, footnotes (`[^1]`), curly quotes, older/newer links at the end.

## Conventions (don't regress)
- **Links are relative** and point at files, not dirs: use `blog/index.html`, not `blog/` (breaks over `file://`). Blog pages use `../` to reach root.
- **Every `<a>` has a `title`.**
- **No email on the site**, in any form (not even runtime-assembled). Contact goes through LinkedIn.
- **Keep personal/contact details minimal** and footers lean.
- **Reveal animations must degrade:** `.reveal` is only hidden under `.js`, so no-JS / crawlers / link previews see full content. Keep this pattern on every page.
- **Two themes:** dark is the default (tokens in each page's `:root`); `theme.css` overrides the tokens for light and styles the header toggle, `theme.js` switches and remembers it. Use color tokens, not hardcoded colors, so both themes keep working.
- `resume.html` has a print stylesheet (`@media print` overrides the color tokens to light) — keep it printable.
