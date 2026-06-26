# xnulinu.dev

Rajesh's personal site. Hand-authored static HTML, no framework, no build step (except the blog generator). Deployed at `xnulinu.dev`.

## Structure
- `index.html` — the landing / "who am i" (personal, first-person)
- `resume.html` — the detailed résumé (work, patents, expertise)
- `blog/` — writing. `posts/*.md` → `build.py` → `*.html` + `index.html`
- `favicon.svg`, `CNAME`, `.nojekyll`

## Blog

**Voice: short, to the point, and personal.** Rajesh's own words, first person. No corporate filler, no LLM throat-clearing ("In this post we will…"), no padding to hit a length. If a sentence isn't earning its place, cut it. One clear idea per post, said plainly.

**My job is to analyze, not ghost-write.** When Rajesh drafts a post (a new/edited file in `blog/posts/`), review it and give honest feedback:
- Is it short and tight? Flag fluff, repetition, hedging, and any paragraph that could be one sentence.
- Does it sound like *him* — personal and direct — or generic?
- Is the core point clear and up front?
- Call out anything unclear, unsupported, or that buries the lede.

Suggest specific cuts/edits; don't rewrite it into my own voice. The point is to make *his* writing sharper, not replace it.

**Writing a post:** add `blog/posts/YYYY-MM-DD-slug.md` with front matter (`title`, `date`, `summary`), then run the generator. `build.py` needs the `markdown` package (use a venv — system Python is externally managed).

## Conventions (don't regress)
- **Links are relative** and point at files, not dirs: use `blog/index.html`, not `blog/` (breaks over `file://`). Blog pages use `../` to reach root.
- **Every `<a>` has a `title`.**
- **Email is never in the source** — it's assembled at runtime from `data-u`/`data-d` on `.email-link` (anti-scrape). Don't add a plaintext `mailto:`.
- **Don't leak personal info:** location is "San Francisco, CA" (hero only), no name/address in footers. Publications (Google Scholar) live on `resume.html` only, not the landing.
- **Reveal animations must degrade:** `.reveal` is only hidden under `.js`, so no-JS / crawlers / link-previews see full content. Keep this pattern on every page.
- `resume.html` has a print stylesheet (`@media print` overrides the color tokens to light) — keep it printable.
