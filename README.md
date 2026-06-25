# xnulinu.dev — Rajesh RC portfolio + blog

Static site. No framework, no tracking, no build dependencies beyond one Python script.

## Layout
```
site/
  index.html            # portfolio (hand-authored, single file)
  blog/
    index.html          # generated — list of posts
    posts/              # write posts here as Markdown
      *.md
    build.py            # md -> html generator
    template.html       # post page shell (header/footer match portfolio)
    style.css           # shared blog styles (pulled from index.html tokens)
```

## Writing a post
1. Drop a Markdown file in `blog/posts/`, e.g. `2026-07-control-planes.md`
2. Front matter at top:
   ```
   ---
   title: The control plane is the product
   date: 2026-07-01
   summary: Why trusted execution, not diagnosis, is the defensible problem.
   ---
   ```
3. Run `python3 blog/build.py`
4. Commit. Done.

## Deploy (pick one — do NOT use AstroPulse nginx)
The AstroPulse box is wildcard-configured for astropulse.io. Keep this separate.

### Option A — Cloudflare Pages (recommended)
- Push this repo to GitHub.
- Cloudflare dashboard -> Pages -> connect repo -> build command: `python3 blog/build.py` (or none if you pre-build), output dir: `site` (or repo root if you flatten).
- Add custom domain `xnulinu.dev` -> Cloudflare auto-creates the CNAME + SSL.

### Option B — GitHub Pages
- Repo -> Settings -> Pages -> deploy from branch (root or /docs).
- Add `xnulinu.dev` as custom domain; create a `CNAME` file containing `xnulinu.dev`.
- At your DNS provider: ALIAS/ANAME `@` -> `<user>.github.io`, or the 4 GitHub A records, plus `www` CNAME.

Both give free HTTPS. Neither touches AstroPulse.

## DNS quick ref (whoever hosts xnulinu.dev's zone)
- Cloudflare Pages: add domain in dashboard, it manages records for you.
- GitHub Pages apex: A records 185.199.108.153 / .109.153 / .110.153 / .111.153
