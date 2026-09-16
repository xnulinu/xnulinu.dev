"""
Diagrams for blog posts, written as fenced blocks in markdown and expanded to HTML/SVG at build time.
No per-post logic: every post gets the same diagram types, styled by blog/style.css tokens (both themes).

    ```flow                          a left-to-right sequence (stacks vertically on phones)
    Intent
    Blueprint
    * Production system              leading "*" marks the step to emphasise
    ```

    ```sets                          a universal set: one big circle holding 1-4 disjoint groups
    Blueprint: the whole production system        first line = the big circle (": subtitle" optional)
    Platform Bricks: GPUs, deployment, networking  then "Group: item, item, ..." (keep items short)
    * Your product: scheduler, routing, caching    leading "*" marks the group to emphasise
    ```
"""
import html
import re

FENCE = re.compile(r"^```(flow|sets)[ \t]*\n(.*?)\n```[ \t]*$", re.MULTILINE | re.DOTALL)


def expand(md_text):
    """Replace every ```flow / ```sets fence with its rendered HTML block."""
    def render(m):
        kind, body = m.group(1), m.group(2)
        lines = [l.strip() for l in body.splitlines() if l.strip()]
        out = RENDERERS[kind](lines)
        return "\n" + out + "\n"  # raw HTML must stand alone as a markdown block
    return FENCE.sub(render, md_text)


def _marked(line):
    return (True, line[1:].strip()) if line.startswith("*") else (False, line)


def _esc(s):
    return html.escape(s, quote=True)


def render_flow(lines):
    steps = [_marked(l) for l in lines]
    label = " → ".join(text for _, text in steps)
    items = "".join(
        ('<li class="is-marked">' if marked else "<li>") + _esc(text) + "</li>" for marked, text in steps
    )
    return f'<ol class="flow" aria-label="{_esc(label)}">{items}</ol>'


# sets geometry, in viewBox units. Groups sit inside the universe circle without overlapping.
W, H = 520, 540
CX, CY, R = 260, 280, 240
LAYOUTS = {  # group count -> [(dx, dy)], group radius
    1: ([(0, 30)], 150),
    2: ([(-92, 30), (92, 30)], 86),
    3: ([(0, -62), (-90, 96), (90, 96)], 86),
    4: ([(-72, -36), (72, -36), (-72, 108), (72, 108)], 68),
}


def render_sets(lines):
    if not lines:
        raise ValueError("sets diagram needs a first line naming the big circle")
    head, rest = lines[0], lines[1:]
    title, _, subtitle = head.partition(":")
    groups = []
    for line in rest:
        marked, text = _marked(line)
        name, _, items = text.partition(":")
        groups.append((marked, name.strip(), [i.strip() for i in items.split(",") if i.strip()]))
    if len(groups) not in LAYOUTS:
        raise ValueError(f"sets diagram supports 1-4 groups, got {len(groups)}")

    centers, r = LAYOUTS[len(groups)]
    parts = [
        f'<circle class="sets-universe" cx="{CX}" cy="{CY}" r="{R}"/>',
        f'<text class="sets-label" x="{CX}" y="{CY - R + 42}" text-anchor="middle">{_esc(title.strip())}</text>',
    ]
    if subtitle.strip():
        parts.append(f'<text class="sets-sub" x="{CX}" y="{CY - R + 62}" text-anchor="middle">{_esc(subtitle.strip())}</text>')

    # one text size for every group: shrink only when the longest line anywhere wouldn't fit a circle
    longest = max(len(t) for _, name, items in groups for t in [name, *items])
    size = min(15 * r / 86, (1.45 * r) / (0.56 * longest))
    for (marked, name, items), (dx, dy) in zip(groups, centers):
        gx, gy = CX + dx, CY + dy
        cls = "sets-group is-marked" if marked else "sets-group"
        parts.append(f'<circle class="{cls}" cx="{gx}" cy="{gy}" r="{r}"/>')
        line_h = size * 1.4
        total = line_h * len(items) + size * 1.15
        y = gy - total / 2 + size * 0.85
        parts.append(f'<text class="sets-title" x="{gx}" y="{y:.1f}" font-size="{size * 1.05:.1f}" text-anchor="middle">{_esc(name)}</text>')
        y += size * 0.35
        for item in items:
            y += line_h
            parts.append(f'<text class="sets-item" x="{gx}" y="{y:.1f}" font-size="{size * 0.92:.1f}" text-anchor="middle">{_esc(item)}</text>')

    summary = f"{title.strip()} contains " + "; ".join(
        f"{name} ({', '.join(items)})" if items else name for _, name, items in groups
    )
    # narrow screens get the same set as nested boxes (circle text would be too small to read)
    stack = "".join(
        f'<div class="sets-box{" is-marked" if marked else ""}">'
        f'<span class="sets-box-title">{_esc(name)}</span>'
        f'<span class="sets-box-items">{_esc(", ".join(items))}</span></div>'
        for marked, name, items in groups
    )
    sub_html = f'<span class="sets-stack-sub">{_esc(subtitle.strip())}</span>' if subtitle.strip() else ""
    return (
        f'<figure class="diagram diagram-sets">'
        f'<svg class="sets-svg" viewBox="0 0 {W} {H}" role="img" aria-label="{_esc(summary)}">{"".join(parts)}</svg>'
        f'<div class="sets-stack"><span class="sets-stack-label">{_esc(title.strip())}</span>{sub_html}{stack}</div>'
        f'</figure>'
    )


RENDERERS = {"flow": render_flow, "sets": render_sets}
