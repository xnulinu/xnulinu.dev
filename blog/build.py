#!/usr/bin/env python3
"""
Minimal static blog generator. No deps beyond stdlib + markdown (pip install markdown).
Reads posts/*.md (with --- front matter ---), writes blog/<slug>.html and blog/index.html.
"""
import os, re, sys, html, datetime, pathlib

try:
    import markdown
except ImportError:
    sys.exit("Run: pip install markdown")

HERE = pathlib.Path(__file__).resolve().parent
POSTS = HERE / "posts"
TEMPLATE = (HERE / "template.html").read_text()

def parse(md_text):
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', md_text, re.DOTALL)
    meta, body = {}, md_text
    if m:
        for line in m.group(1).splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                meta[k.strip()] = v.strip()
        body = m.group(2)
    return meta, body

def render():
    posts = []
    for f in sorted(POSTS.glob("*.md")):
        meta, body = parse(f.read_text())
        slug = f.stem
        title = meta.get("title", slug)
        date = meta.get("date", "")
        summary = meta.get("summary", "")
        body_html = markdown.markdown(body, extensions=["fenced_code", "tables"])
        page = (TEMPLATE
                .replace("{{TITLE}}", html.escape(title))
                .replace("{{DATE}}", html.escape(date))
                .replace("{{SUMMARY}}", html.escape(summary))
                .replace("{{BODY}}", body_html))
        (HERE / f"{slug}.html").write_text(page)
        posts.append({"slug": slug, "title": title, "date": date, "summary": summary})
        print(f"  built {slug}.html")

    posts.sort(key=lambda p: p["date"], reverse=True)
    items = "\n".join(
        f'''      <a class="post-row" href="{p["slug"]}.html" title="{html.escape(p["title"])}">
        <span class="pr-date">{html.escape(p["date"])}</span>
        <span class="pr-mid">
          <span class="pr-title">{html.escape(p["title"])}</span>
          <span class="pr-sum">{html.escape(p["summary"])}</span>
        </span>
        <span class="pr-arr">→</span>
      </a>''' for p in posts)

    index = (TEMPLATE
             .replace("{{TITLE}}", "Writing")
             .replace("{{DATE}}", "")
             .replace("{{SUMMARY}}", "Notes on distributed systems, control planes, and safe autonomous execution.")
             .replace("{{BODY}}", f'<div class="post-list">\n{items}\n    </div>')
             .replace('<article class="post">', '<article class="post post-index">'))
    (HERE / "index.html").write_text(index)
    print(f"  built index.html ({len(posts)} posts)")

if __name__ == "__main__":
    print("Building blog…")
    render()
    print("Done.")
