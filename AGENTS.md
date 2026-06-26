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

**Writing a post:** add `blog/posts/YYYY-MM-DD-slug.md` with front matter (`title`, `date`, `summary`), then `make blog`.

## Conventions (don't regress)
- **Links are relative** and point at files, not dirs: use `blog/index.html`, not `blog/` (breaks over `file://`). Blog pages use `../` to reach root.
- **Every `<a>` has a `title`.**
- **Email is never in the source** — it's assembled at runtime from `data-u`/`data-d` on `.email-link` (anti-scrape). Don't add a plaintext `mailto:`.
- **Keep personal/contact details minimal** and footers lean.
- **Reveal animations must degrade:** `.reveal` is only hidden under `.js`, so no-JS / crawlers / link previews see full content. Keep this pattern on every page.
- `resume.html` has a print stylesheet (`@media print` overrides the color tokens to light) — keep it printable.
