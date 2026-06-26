# xnulinu.dev — RJ's site + blog

Static site. Hand-authored HTML, no framework, no tracking. The only build step is a tiny Python blog generator.

## Layout
```
index.html        # "who am i" landing (hand-authored)
resume.html       # detailed résumé (also prints / saves to PDF cleanly)
favicon.svg
Makefile          # `make blog` / `make serve`
CLAUDE.md         # notes for working in this repo (blog voice, conventions)
blog/
  index.html      # generated — list of posts
  posts/*.md      # write posts here as Markdown
  build.py        # md -> html generator
  template.html   # post shell (header/footer match the site)
  style.css       # shared blog styles
```

## Writing a post
1. Add `blog/posts/YYYY-MM-DD-slug.md` with front matter:
   ```
   ---
   title: The control plane is the product
   date: 2026-07-01
   summary: Why trusted execution, not diagnosis, is the defensible problem.
   ---
   ```
2. `make blog` — builds the HTML (first run creates a local `.venv` with the `markdown` dependency, since system Python is externally managed).
3. Commit the generated HTML. Done.

Preview the whole site locally with `make serve` → http://localhost:8000.

> GitHub Pages serves these files as-is (no build), so the blog HTML must be built locally and committed.

## Deploy
The domain **xnulinu.dev is registered with Squarespace**, so DNS lives in the Squarespace panel
(Settings → Domains → xnulinu.dev → DNS settings). Keep this separate from the AstroPulse nginx box
(it's wildcard-configured for astropulse.io — don't route this site through it).

### Recommended: GitHub Pages + Squarespace DNS
- Repo → Settings → Pages → deploy from branch (root). The `CNAME` (`xnulinu.dev`) and `.nojekyll` files are already in the repo.
- In Squarespace DNS, add **custom records**:
  - Apex `@` → four A records: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
  - `www` → CNAME → `xnulinu.github.io`
- GitHub Pages issues free HTTPS once DNS resolves.

### Alternative: Cloudflare Pages
Requires moving DNS to Cloudflare (repoint Squarespace's nameservers, or transfer the zone). More involved
while Squarespace holds the domain — only worth it for Cloudflare's edge features.
