#!/usr/bin/env python3
"""
Minimal static blog generator. No deps beyond stdlib + markdown (pip install markdown).
Reads posts/*.md (with --- front matter ---), writes blog/<slug>.html and blog/index.html.
Everything here applies to every post — no per-post logic. Diagrams live in diagrams.py.
"""
import re, sys, html, pathlib, hashlib, math

from diagrams import expand as expand_diagrams

try:
    import markdown
except ImportError:
    sys.exit("Run: pip install markdown")

HERE = pathlib.Path(__file__).resolve().parent
POSTS = HERE / "posts"
RECENT = 3  # posts shown on the landing page
TEMPLATE = (HERE / "template.html").read_text()
# cache-bust: stylesheet/script links carry a hash of their contents, so browsers never mix a new page with an old CSS
ASSET_V = hashlib.sha1(b"".join(p.read_bytes() for p in (HERE / "style.css", HERE.parent / "theme.css", HERE.parent / "theme.js"))).hexdigest()[:8]
TEMPLATE = TEMPLATE.replace("{{ASSET_V}}", ASSET_V)

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

# one Markdown setup for every post: section links, footnotes, typographic quotes
MD = markdown.Markdown(
    extensions=["fenced_code", "tables", "footnotes", "smarty", "sane_lists", "toc"],
    extension_configs={"toc": {"permalink": "#", "permalink_title": "Link to this section", "toc_depth": "2-3"}},
)
WORDS_PER_MINUTE = 230

def post_nav(newer, older):
    # "older / newer" links at the end of each post
    def link(p, cls, label):
        if not p:
            return '<span></span>'
        return (f'<a class="pn-link {cls}" href="{p["slug"]}.html" title="{html.escape(p["title"])}">'
                f'<span class="pn-label">{label}</span><span class="pn-title">{html.escape(p["title"])}</span></a>')
    if not (newer or older):
        return ""
    return f'<nav class="post-nav">{link(older, "pn-older", "← older")}{link(newer, "pn-newer", "newer →")}</nav>'

def render():
    posts = []
    for f in sorted(POSTS.glob("*.md")):
        meta, body = parse(f.read_text())
        posts.append({
            "slug": f.stem, "body": body,
            "title": meta.get("title", f.stem), "date": meta.get("date", ""),
            "summary": meta.get("summary", ""), "image": meta.get("image", ""),
        })
    posts.sort(key=lambda p: p["date"], reverse=True)

    for i, p in enumerate(posts):
        MD.reset()
        body_html = MD.convert(expand_diagrams(p["body"]))
        words = len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", body_html)))
        meta_line = f'{html.escape(p["date"])} · {max(1, math.ceil(words / WORDS_PER_MINUTE))} min read'
        # standard pattern: every post leads with its image, then the content
        image_html = (
            f'<figure class="post-hero"><img src="../assets/blog/{html.escape(p["image"])}" '
            f'alt="{html.escape(p["title"])}" loading="eager" /></figure>'
            if p["image"] else ""
        )
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i + 1 < len(posts) else None
        page = (TEMPLATE
                .replace("{{TITLE}}", html.escape(p["title"]))
                .replace("{{DATE}}", meta_line)
                .replace("{{SUMMARY}}", html.escape(p["summary"]))
                .replace("{{IMAGE}}", image_html)
                .replace("{{BODY}}", body_html)
                .replace("{{POST_NAV}}", post_nav(newer, older)))
        (HERE / f'{p["slug"]}.html').write_text(page)
        print(f'  built {p["slug"]}.html')

    def row(p):
        # each post is a card; its image (when present) lives on the same card
        thumb = (
            f'<span class="pr-media"><img src="../assets/blog/{html.escape(p["image"])}" '
            f'alt="" loading="lazy" /></span>'
            if p["image"] else ""
        )
        cls = "post-row" if p["image"] else "post-row no-media"
        return (
            f'      <a class="{cls}" href="{p["slug"]}.html" title="{html.escape(p["title"])}">\n'
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
             .replace("    {{IMAGE}}\n", "")
             .replace("{{BODY}}", index_body)
             .replace("    {{POST_NAV}}\n", "")
             .replace('<article class="post">', '<article class="post post-index">'))
    (HERE / "index.html").write_text(index)
    print(f"  built index.html ({len(posts)} posts)")

    # the landing page shows the latest few posts between the recent-posts markers
    def recent(p):
        return (
            f'        <a class="recent-row" href="blog/{p["slug"]}.html" title="{html.escape(p["title"])}">\n'
            f'          <span class="rr-date">{html.escape(p["date"])}</span>\n'
            f'          <span class="rr-title">{html.escape(p["title"])}</span>\n'
            f'          <span class="rr-sum">{html.escape(p["summary"])}</span>\n'
            f'        </a>'
        )
    landing = HERE.parent / "index.html"
    page, n = re.subn(
        r"(<!-- recent-posts:start[^>]*-->\n).*?(<!-- recent-posts:end -->)",
        lambda m: m.group(1) + "".join(recent(p) + "\n" for p in posts[:RECENT]) + m.group(2),
        landing.read_text(), flags=re.DOTALL)
    if n != 1:
        sys.exit("index.html: recent-posts markers not found")
    landing.write_text(page)
    print(f"  updated ../index.html (latest {min(len(posts), RECENT)} posts)")

    # hand-authored root pages get the same cache-busting stamp on the shared theme files
    for name in ("index.html", "resume.html"):
        root_page = HERE.parent / name
        stamped, n = re.subn(r'((?:href="theme\.css)|(?:src="theme\.js))(?:\?v=[0-9a-f]+)?"', rf'\1?v={ASSET_V}"', root_page.read_text())
        if n != 2:
            sys.exit(f"{name}: expected theme.css + theme.js links, found {n}")
        root_page.write_text(stamped)
    print(f"  stamped theme assets on ../index.html, ../resume.html (v={ASSET_V})")

if __name__ == "__main__":
    print("Building blog…")
    render()
    print("Done.")
