# xnulinu.dev

Personal site + blog. Hand-authored static HTML — no framework, no tracking. The only build step is a small Python script that turns Markdown posts into HTML.

## Layout
```
index.html      who-am-i landing
resume.html     résumé (prints / saves to PDF cleanly)
favicon.svg
Makefile        make blog · make serve · make clean
CLAUDE.md       repo notes (blog voice, conventions)
blog/
  posts/*.md    write posts here
  build.py      Markdown → HTML generator
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
2. `make blog`
3. Commit the generated HTML and push.
