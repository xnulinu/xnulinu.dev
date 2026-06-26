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
        image = meta.get("image", "")
        body_html = markdown.markdown(body, extensions=["fenced_code", "tables"])
        # standard pattern: every post leads with its image, then the content
        image_html = (
            f'<figure class="post-hero"><img src="../assets/blog/{image}" '
            f'alt="{html.escape(title)}" loading="eager" /></figure>'
            if image else ""
        )
        page = (TEMPLATE
                .replace("{{TITLE}}", html.escape(title))
                .replace("{{DATE}}", html.escape(date))
                .replace("{{SUMMARY}}", html.escape(summary))
                .replace("{{IMAGE}}", image_html)
                .replace("{{BODY}}", body_html))
        (HERE / f"{slug}.html").write_text(page)
        posts.append({"slug": slug, "title": title, "date": date, "summary": summary, "image": image})
        print(f"  built {slug}.html")

    posts.sort(key=lambda p: p["date"], reverse=True)

    def row(p):
        # each post is a card; its image lives on the same card
        thumb = (
            f'<span class="pr-media"><img src="../assets/blog/{p["image"]}" '
            f'alt="" loading="lazy" /></span>'
            if p["image"] else ""
        )
        return (
            f'      <a class="post-row" href="{p["slug"]}.html" title="{html.escape(p["title"])}">\n'
            f'        <span class="pr-text">\n'
            f'          <span class="pr-date">{html.escape(p["date"])}</span>\n'
            f'          <span class="pr-title">{html.escape(p["title"])}</span>\n'
            f'          <span class="pr-sum">{html.escape(p["summary"])}</span>\n'
            f'        </span>\n'
            f'        {thumb}\n'
            f'      </a>'
        )

    items = "\n".join(row(p) for p in posts)
    index_body = f'<div class="post-list">\n{items}\n    </div>'

    index = (TEMPLATE
             .replace("{{TITLE}}", "Writing")
             .replace("{{DATE}}", "")
             .replace("{{SUMMARY}}", "Notes on distributed systems, control planes, and safe autonomous execution.")
             .replace("{{IMAGE}}", "")
             .replace("{{BODY}}", index_body)
             .replace('<article class="post">', '<article class="post post-index">'))
    (HERE / "index.html").write_text(index)
    print(f"  built index.html ({len(posts)} posts)")

if __name__ == "__main__":
    print("Building blog…")
    render()
    print("Done.")
