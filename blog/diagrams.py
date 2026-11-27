"""
Diagrams for blog posts, written as fenced blocks in markdown and expanded to HTML/SVG at build time.
No per-post logic: every post gets the same diagram types, styled by blog/style.css tokens (both themes).

Every diagram is a figure: a card on a tinted plate, exactly as wide as the text column, with an
optional caption ("title: ..." as the first line) numbered "Figure n" by CSS. Steps, tiles, gates and
the heads of a shift can start with "[icon]", one of ICONS below (e.g. "[lab] labs"); a leading "*"
(before the icon) marks the one item to emphasise.

    ```flow                          a left-to-right pipeline of stations (stacks vertically on phones)
    title: How a change ships        optional caption
    [laptop] laptop
    * [release] release
    ```

    ```sets                          a universal set: one big circle holding 1-4 disjoint groups
    title: ...                       optional caption
    Blueprint: the whole system      first line = the big circle (": subtitle" optional)
    * Your product: routing, caching then "Group: item, item, ..." (keep items short)
    ```

    ```trend                         a line over time on a relative log scale (no numeric y axis)
    title: Weekly merged changes     optional caption
    3.7 Jul                          one point per line: "<level 0-10> [x-axis label]"
    * 5.3 v1.0                       "*" annotates the point; the line after it is drawn in the accent
    ```

    ```bars                          horizontal bars: relative share, labels only (no numbers shown)
    title: Where the time goes
    * 28.5 labs one at a time        "<relative weight> <label>", scaled to the largest
    ```

    ```tiles                         a grid of labelled mechanisms: "[icon] Title: one short line"
    [lab] Real platform: drives the real CLI
    ```

    ```gates                         layered filters a change passes, each with what it catches
    [commit] commit: lint errors     "[icon] Layer: catch, catch"; layers narrow toward the last one
    * [person] a person merges: agents merging
    ```

    ```shift                         before -> after, row by row
    [laptop] Workshop -> [factory] Factory     first line = the two column heads
    labs one at a time -> labs in parallel
    ```
"""
import html
import re

FENCE = re.compile(r"^```(flow|sets|trend|bars|tiles|gates|shift)[ \t]*\n(.*?)\n```[ \t]*$", re.MULTILINE | re.DOTALL)

# one icon set for every diagram: 24px grid, drawn with a single stroke weight (set in style.css)
ICONS = {
    "laptop": '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>',
    "cloud": '<path d="M7.5 18.5h9.5a4 4 0 0 0 .4-7.98A5.8 5.8 0 0 0 6.3 9.4a4.6 4.6 0 0 0 1.2 9.1z"/>',
    "lab": '<path d="M9 3h6M10 3v6.2L4.6 18.4A1.7 1.7 0 0 0 6.1 21h11.8a1.7 1.7 0 0 0 1.5-2.6L14 9.2V3"/><path d="M7.2 15h9.6"/>',
    "gate": '<path d="M12 3l7.5 3v5.3c0 4.6-3.1 8.2-7.5 9.7-4.4-1.5-7.5-5.1-7.5-9.7V6z"/><path d="M8.8 12.2l2.2 2.2 4.2-4.4"/>',
    "merge": '<circle cx="6.5" cy="5" r="2"/><circle cx="6.5" cy="19" r="2"/><circle cx="17.5" cy="12" r="2"/><path d="M6.5 7v10M6.5 7.5c.6 3.2 3.4 4.5 9 4.5"/>',
    "release": '<path d="M12 2.8c3.2 2.3 4.9 5.7 4.9 9.6l-1.9 3.4H9l-1.9-3.4c0-3.9 1.7-7.3 4.9-9.6z"/><circle cx="12" cy="10" r="1.7"/><path d="M9.2 15.8l-2.4 3.6 3.2-.9M14.8 15.8l2.4 3.6-3.2-.9M12 18.5v2.7"/>',
    "agent": '<rect x="4.5" y="8" width="15" height="11.5" rx="2.5"/><path d="M12 4.5V8M2.5 12.5v3M21.5 12.5v3"/><circle cx="12" cy="3.6" r="1"/><circle cx="9.2" cy="13.2" r="1.1"/><circle cx="14.8" cy="13.2" r="1.1"/><path d="M9.5 16.6h5"/>',
    "person": '<circle cx="12" cy="8" r="3.6"/><path d="M4.8 20.5c.8-3.9 3.6-6.2 7.2-6.2s6.4 2.3 7.2 6.2"/>',
    "console": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M9 9v11"/><path d="M12.5 13h5M12.5 16h3"/>',
    "terminal": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9.5l3 2.5-3 2.5M12.5 15H17"/>',
    "package": '<path d="M12 2.8l8 4.4v9.6L12 21.2l-8-4.4V7.2z"/><path d="M4 7.2l8 4.5 8-4.5M12 11.7v9.5M8 5l8 4.5"/>',
    "branch": '<circle cx="6.5" cy="5" r="2"/><circle cx="6.5" cy="19" r="2"/><circle cx="17.5" cy="6.5" r="2"/><path d="M6.5 7v10M17.5 8.5c0 4.8-4.4 5.6-9.8 8.8"/>',
    "commit": '<circle cx="12" cy="12" r="3.6"/><path d="M2.5 12h5.9M15.6 12h5.9"/>',
    "push": '<path d="M12 20V7.5M6.8 12.5L12 7.3l5.2 5.2M5 3.5h14"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12.4l2.8 2.8L16.2 9.8"/>',
    "checks": '<path d="M3.5 6.2l1.6 1.6L8 4.9M3.5 12.2l1.6 1.6L8 10.9M3.5 18.2l1.6 1.6L8 16.9M11.5 6.5h9M11.5 12.5h9M11.5 18.5h9"/>',
    "moon": '<path d="M19.8 14.6A8.2 8.2 0 1 1 9.4 4.2a6.6 6.6 0 0 0 10.4 10.4z"/>',
    "issue": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="1.6"/>',
    "eye": '<path d="M2.5 12S6 5.8 12 5.8 21.5 12 21.5 12 18 18.2 12 18.2 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
    "layers": '<path d="M12 3.5l9 4.8-9 4.8-9-4.8z"/><path d="M3 12.3l9 4.8 9-4.8M3 16.2l9 4.8 9-4.8"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5.2l3.4 2"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8.2 10.5V7.6a3.8 3.8 0 0 1 7.6 0v2.9"/>',
    "doc": '<path d="M6 3h8.5L19 7.5V21H6z"/><path d="M14 3v5h5M9 12.5h7M9 16h7"/>',
    "factory": '<path d="M3 21V10.5l5 3v-3l5 3v-3l5 3V4h3v17z"/><path d="M7 17.5h2M11.5 17.5h2"/>',
    "wrench": '<path d="M14.6 3.4a5 5 0 0 0-4.9 6.5l-6.1 6.1a2.1 2.1 0 0 0 3 3l6.1-6.1a5 5 0 0 0 6.5-4.9l-3 1.4-2.6-2.6z"/>',
    "repeat": '<path d="M4 11V9.5A3.5 3.5 0 0 1 7.5 6H19M16 3l3 3-3 3M20 13v1.5a3.5 3.5 0 0 1-3.5 3.5H5M8 21l-3-3 3-3"/>',
    "api": '<path d="M8 4.5c-2 0-2.5 1-2.5 3v2c0 1.5-.8 2.5-2.5 2.5 1.7 0 2.5 1 2.5 2.5v2c0 2 .5 3 2.5 3M16 4.5c2 0 2.5 1 2.5 3v2c0 1.5.8 2.5 2.5 2.5-1.7 0-2.5 1-2.5 2.5v2c0 2-.5 3-2.5 3"/>',
}
ALIASES = {"flask": "lab", "shield": "gate", "rocket": "release", "robot": "agent", "review": "eye",
           "nightly": "moon", "batch": "layers", "worktree": "branch", "docs": "doc", "workshop": "wrench"}

ARROW = ('<svg class="fig-arrow" viewBox="0 0 32 12" aria-hidden="true" focusable="false">'
         '<path d="M1 6h28M24 1.5L29.5 6 24 10.5"/></svg>')
CROSS = ('<svg class="glyph-x" viewBox="0 0 12 12" aria-hidden="true" focusable="false">'
         '<path d="M3 3l6 6M9 3l-6 6"/></svg>')


def expand(md_text):
    """Replace every diagram fence with its rendered HTML block."""
    def render(m):
        kind, body = m.group(1), m.group(2)
        lines = [l.strip() for l in body.splitlines() if l.strip()]
        out = RENDERERS[kind](lines)
        return "\n" + out + "\n"  # raw HTML must stand alone as a markdown block
    return FENCE.sub(render, md_text)


def _esc(s):
    return html.escape(s, quote=True)


def _marked(line):
    return (True, line[1:].strip()) if line.startswith("*") else (False, line)


def _iconed(text):
    """'[lab] labs' -> ('lab', 'labs'); unknown icon names fail the build instead of rendering nothing."""
    m = re.match(r"^\[([a-z-]+)\]\s*(.*)$", text)
    if not m:
        return None, text
    name = ALIASES.get(m.group(1), m.group(1))
    if name not in ICONS:
        raise ValueError(f"unknown diagram icon [{m.group(1)}]; known: {', '.join(sorted(ICONS))}")
    return name, m.group(2).strip()


def _item(line):
    marked, text = _marked(line)
    icon, text = _iconed(text)
    return marked, icon, text


def icon_svg(name, cls="glyph"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
            f'{ICONS[name]}</svg>')


def _title(lines):
    if lines and lines[0].lower().startswith("title:"):
        return lines[0][6:].strip(), lines[1:]
    return "", lines


def _figure(kind, inner, title, label, role_img=False, extra=""):
    """Shared figure frame: plate + card + numbered caption. role_img hides the inner markup from
    screen readers when the aria-label already says everything (charts); otherwise the text inside stays readable."""
    role = ' role="img"' if role_img else ""
    cap = f'<figcaption class="fig-cap"><span class="fig-cap-text">{_esc(title)}</span></figcaption>' if title else ""
    return (f'<figure class="diagram diagram-{kind}"{role} aria-label="{_esc(label)}"{extra}>'
            f'<div class="fig-plate"><div class="fig-card">{inner}</div></div>{cap}</figure>')


# ---------------------------------------------------------------- flow
def render_flow(lines):
    title, lines = _title(lines)
    steps = [_item(l) for l in lines]
    if len(steps) < 2:
        raise ValueError("flow diagram needs at least two steps")
    parts = []
    for i, (marked, icon, text) in enumerate(steps):
        if i:
            parts.append(f'<li class="flow-link" aria-hidden="true">{ARROW}</li>')
        node = icon_svg(icon) if icon else '<span class="flow-dot"></span>'
        parts.append(f'<li class="flow-step{" is-marked" if marked else ""}">'
                     f'<span class="flow-node">{node}</span><span class="flow-label">{_esc(text)}</span></li>')
    label = (title + ": " if title else "") + " → ".join(t for _, _, t in steps)
    inner = f'<ol class="flow" style="--n:{len(steps)}">{"".join(parts)}</ol>'
    return _figure("flow", inner, title, label)


# ---------------------------------------------------------------- sets
# geometry, in viewBox units. Groups sit inside the universe circle without overlapping.
W, H = 560, 560
CX, CY, R = 280, 285, 262
LAYOUTS = {  # group count -> [(dx, dy)], group radius
    1: ([(0, 30)], 160),
    2: ([(-102, 34), (102, 34)], 94),
    3: ([(0, -62), (-100, 108), (100, 108)], 92),
    4: ([(-80, -38), (80, -38), (-80, 122), (80, 122)], 76),
}
_ids = {"n": 0}


def _uid(prefix):
    _ids["n"] += 1
    return f"{prefix}{_ids['n']}"


def render_sets(lines):
    title, lines = _title(lines)
    if not lines:
        raise ValueError("sets diagram needs a first line naming the big circle")
    head, rest = lines[0], lines[1:]
    name0, _, subtitle = head.partition(":")
    name0, subtitle = name0.strip(), subtitle.strip()
    groups = []
    for line in rest:
        marked, text = _marked(line)
        name, _, items = text.partition(":")
        groups.append((marked, name.strip(), [i.strip() for i in items.split(",") if i.strip()]))
    if len(groups) not in LAYOUTS:
        raise ValueError(f"sets diagram supports 1-4 groups, got {len(groups)}")

    centers, r = LAYOUTS[len(groups)]
    dots, arc = _uid("sets-dots-"), _uid("sets-arc-")
    ra = R - 26  # the universe name runs along this arc, just inside the rim
    parts = [
        f'<defs><pattern id="{dots}" width="14" height="14" patternUnits="userSpaceOnUse">'
        f'<circle class="sets-dot" cx="7" cy="7" r="1.1"/></pattern>'
        f'<path id="{arc}" d="M{CX - ra} {CY} A{ra} {ra} 0 0 1 {CX + ra} {CY}"/></defs>',
        f'<circle class="sets-universe" cx="{CX}" cy="{CY}" r="{R}"/>',
        f'<circle class="sets-texture" cx="{CX}" cy="{CY}" r="{R}" fill="url(#{dots})"/>',
        f'<text class="sets-label" text-anchor="middle"><textPath href="#{arc}" startOffset="50%">{_esc(name0)}</textPath></text>',
    ]
    if subtitle:
        parts.append(f'<text class="sets-sub" x="{CX}" y="{CY - R + 66}" text-anchor="middle">{_esc(subtitle)}</text>')

    # one text size for every group: shrink only when the longest line anywhere wouldn't fit a circle
    longest = max(len(t) for _, name, items in groups for t in [name, *items])
    size = min(18 * r / 92, (1.55 * r) / (0.6 * longest))
    for (marked, name, items), (dx, dy) in zip(groups, centers):
        gx, gy = CX + dx, CY + dy
        cls = "sets-group is-marked" if marked else "sets-group"
        parts.append(f'<circle class="{cls}" cx="{gx}" cy="{gy}" r="{r}"/>')
        line_h = size * 1.38
        total = line_h * len(items) + size * 1.5
        y = gy - total / 2 + size * 0.9
        tcls = "sets-title is-marked" if marked else "sets-title"
        parts.append(f'<text class="{tcls}" x="{gx}" y="{y:.1f}" font-size="{size * 1.08:.1f}" text-anchor="middle">{_esc(name)}</text>')
        parts.append(f'<line class="sets-rule{" is-marked" if marked else ""}" x1="{gx - 14}" y1="{y + size * 0.6:.1f}" x2="{gx + 14}" y2="{y + size * 0.6:.1f}"/>')
        y += size * 0.55
        for item in items:
            y += line_h
            parts.append(f'<text class="sets-item" x="{gx}" y="{y:.1f}" font-size="{size * 0.92:.1f}" text-anchor="middle">{_esc(item)}</text>')

    summary = f"{name0} contains " + "; ".join(
        f"{name} ({', '.join(items)})" if items else name for _, name, items in groups
    )
    # narrow screens get the same set as nested boxes (circle text would be too small to read)
    stack = "".join(
        f'<div class="sets-box{" is-marked" if marked else ""}">'
        f'<span class="sets-box-title">{_esc(name)}</span>'
        f'<span class="sets-box-items">{_esc(", ".join(items))}</span></div>'
        for marked, name, items in groups
    )
    sub_html = f'<span class="sets-stack-sub">{_esc(subtitle)}</span>' if subtitle else ""
    inner = (f'<svg class="sets-svg" viewBox="0 0 {W} {H}" aria-hidden="true">{"".join(parts)}</svg>'
             f'<div class="sets-stack" aria-hidden="true"><span class="sets-stack-label">{_esc(name0)}</span>{sub_html}{stack}</div>')
    return _figure("sets", inner, title, (title + ". " if title else "") + summary, role_img=True)


# ---------------------------------------------------------------- trend
# Two drawings of the same line: a wide one for desktop and a taller one for phones (CSS shows one),
# so the chart keeps readable text and height at any width. Geometry is in viewBox units.
TREND_SIZES = {
    #        width height left right top  axis  row  gap  font pill(char_w, h)
    "wide":  (860, 300, 20, 20, 48, 248, 30, 2, 13.5, (9.6, 28)),
    "narrow": (420, 280, 14, 14, 52, 236, 28, 2, 15, (10.4, 30)),
}


def _pill(x, y, text, char_w, h, side):
    """An annotation pill anchored at (x, y) on the given side (left / right of x)."""
    w = len(text) * char_w + h * 0.9
    x0 = x - w if side == "left" else x
    return (f'<rect class="trend-pill" x="{x0:.1f}" y="{y - h / 2:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}"/>'
            f'<text class="trend-pill-text" x="{x0 + w / 2:.1f}" y="{y + h * 0.17:.1f}" font-size="{h * 0.5:.1f}" text-anchor="middle">{_esc(text)}</text>')


def _trend_svg(points, size):
    tw, th, left, right, top, axis, row_h, min_gap, font, (cw, ph) = TREND_SIZES[size]
    step = (tw - left - right) / (len(points) - 1)
    xy = [(left + i * step, axis - v / 10 * (axis - top)) for i, (_, v, _) in enumerate(points)]
    mark = next((i for i, (m, _, _) in enumerate(points) if m), None)
    split = mark if mark is not None else len(points) - 1

    def poly(seg):
        return " ".join(f"{x:.1f},{y:.1f}" for x, y in seg)

    def area(seg):
        return poly([(seg[0][0], axis), *seg, (seg[-1][0], axis)])

    parts = [f'<line class="trend-grid" x1="{left}" y1="{axis - k / 10 * (axis - top):.1f}" '
             f'x2="{tw - right}" y2="{axis - k / 10 * (axis - top):.1f}"/>' for k in (2.5, 5, 7.5, 10)]
    parts.append(f'<text class="trend-note" x="{left}" y="{top - 26}" font-size="{font * 0.9:.1f}">log scale</text>')
    before, after = xy[: split + 1], xy[split:]
    parts.append(f'<polygon class="trend-area" points="{area(before)}"/>')
    if len(after) > 1:
        parts.append(f'<polygon class="trend-area is-marked" points="{area(after)}"/>')
    parts.append(f'<line class="trend-axis" x1="{left}" y1="{axis}" x2="{tw - right}" y2="{axis}"/>')
    last_on_row = {}
    for i, ((marked, _, label), (x, _)) in enumerate(zip(points, xy)):
        if label and not marked:
            row = 0
            while i - last_on_row.get(row, -min_gap) < min_gap:
                row += 1
            last_on_row[row] = i
            parts.append(f'<line class="trend-tick" x1="{x:.1f}" y1="{axis}" x2="{x:.1f}" y2="{axis + 7 + row * row_h}"/>')
            parts.append(f'<text class="trend-label" x="{x:.1f}" y="{axis + font + 12 + row * row_h:.1f}" font-size="{font}" text-anchor="middle">{_esc(label)}</text>')
    if mark is not None:
        mx, _ = xy[mark]
        parts.append(f'<line class="trend-mark-line" x1="{mx:.1f}" y1="{top - 20}" x2="{mx:.1f}" y2="{axis}"/>')
    parts.append(f'<polyline class="trend-line" points="{poly(before)}"/>')
    if len(after) > 1:
        parts.append(f'<polyline class="trend-line is-marked" points="{poly(after)}"/>')
    for i, (x, y) in enumerate(xy):
        if i != mark:
            parts.append(f'<circle class="trend-dot{" is-after" if i > split else ""}" cx="{x:.1f}" cy="{y:.1f}" r="3.5"/>')
    if mark is not None:
        mx, my = xy[mark]
        parts.append(f'<circle class="trend-halo" cx="{mx:.1f}" cy="{my:.1f}" r="13"/>')
        parts.append(f'<circle class="trend-dot is-marked" cx="{mx:.1f}" cy="{my:.1f}" r="6"/>')
        text = points[mark][2]
        if text:
            # the pill sits at the top of the dashed marker line, on whichever side has more room
            side = "left" if mx > tw / 2 else "right"
            parts.append(_pill(mx + (-8 if side == "left" else 8), top - 20, text, cw, ph, side))
    return f'<svg class="trend-svg is-{size}" viewBox="0 0 {tw} {th}" aria-hidden="true">{"".join(parts)}</svg>'


def render_trend(lines):
    title, lines = _title(lines)
    points = []
    for line in lines:
        marked, text = _marked(line)
        level, _, label = text.partition(" ")
        try:
            value = min(10.0, max(0.0, float(level)))
        except ValueError:
            raise ValueError(f"trend point needs a numeric level 0-10, got {line!r}")
        points.append((marked, value, label.strip()))
    if len(points) < 2:
        raise ValueError("trend diagram needs at least two points")

    def name(i):
        return points[i][2] or f"point {i + 1}"
    values = [v for _, v, _ in points]
    hi, lo = values.index(max(values)), values.index(min(values))
    labelled = [l for _, _, l in points if l]
    span = f" from {labelled[0]} to {labelled[-1]}" if len(labelled) > 1 else ""
    summary = f"{title + '. ' if title else ''}Line chart on a relative log scale{span}. "
    trend = "rising" if values[-1] > values[0] else "falling" if values[-1] < values[0] else "flat"
    summary += f"Highest near {name(hi)}, lowest near {name(lo)}, {trend} overall."
    mark = next((i for i, (m, _, _) in enumerate(points) if m), None)
    if mark is not None:
        summary += f" Marked: {name(mark)}."
    inner = _trend_svg(points, "wide") + _trend_svg(points, "narrow")
    return _figure("trend", inner, title, summary, role_img=True)


# ---------------------------------------------------------------- bars
def render_bars(lines):
    title, lines = _title(lines)
    bars = []
    for line in lines:
        marked, text = _marked(line)
        weight, _, label = text.partition(" ")
        try:
            value = float(weight)
        except ValueError:
            raise ValueError(f"bars line needs '<weight> <label>', got {line!r}")
        if value < 0 or not label.strip():
            raise ValueError(f"bars line needs a non-negative weight and a label, got {line!r}")
        bars.append((marked, value, label.strip()))
    if not bars:
        raise ValueError("bars diagram needs at least one bar")
    top = max(v for _, v, _ in bars) or 1.0

    # a plain-words summary: largest first, no numbers (the weights are relative, not measurements to quote)
    ranked = [label for _, _, label in sorted(bars, key=lambda b: -b[1])]
    summary = f"{title + '. ' if title else ''}Bar chart of relative share, largest first: {'; '.join(ranked)}."
    rows = "".join(
        f'<div class="bars-row{" is-marked" if marked else ""}">'
        f'<span class="bars-label">{_esc(label)}</span>'
        # a floor keeps a tiny share visible as a sliver instead of vanishing
        f'<span class="bars-track"><span class="bars-fill" style="width:{max(v / top * 100, 0.8):.1f}%"></span></span>'
        f'</div>'
        for marked, v, label in bars
    )
    return _figure("bars", f'<div class="bars" aria-hidden="true">{rows}</div>', title, summary, role_img=True)


# ---------------------------------------------------------------- tiles
def render_tiles(lines):
    title, lines = _title(lines)
    tiles = []
    for line in lines:
        marked, icon, text = _item(line)
        name, _, desc = text.partition(":")
        tiles.append((marked, icon, name.strip(), desc.strip()))
    if not tiles:
        raise ValueError("tiles diagram needs at least one tile")
    cells = "".join(
        f'<li class="tile{" is-marked" if marked else ""}">'
        + (f'<span class="tile-icon">{icon_svg(icon)}</span>' if icon else "")
        + f'<span class="tile-name">{_esc(name)}</span>'
        + (f'<span class="tile-desc">{_esc(desc)}</span>' if desc else "")
        + "</li>"
        for marked, icon, name, desc in tiles
    )
    label = (title + ": " if title else "") + "; ".join(f"{n} — {d}" if d else n for _, _, n, d in tiles)
    cols = 3 if len(tiles) % 3 == 0 or len(tiles) > 4 else 2
    return _figure("tiles", f'<ul class="tiles" style="--cols:{cols}">{cells}</ul>', title, label)


# ---------------------------------------------------------------- gates
def render_gates(lines):
    title, lines = _title(lines)
    layers = []
    for line in lines:
        marked, icon, text = _item(line)
        name, _, catches = text.partition(":")
        layers.append((marked, icon, name.strip(), [c.strip() for c in catches.split(",") if c.strip()]))
    if not layers:
        raise ValueError("gates diagram needs at least one layer")
    n = len(layers)
    rows = []
    for i, (marked, icon, name, catches) in enumerate(layers):
        if i:
            rows.append(f'<li class="gate-link" aria-hidden="true">{ARROW}</li>')
        chips = "".join(f'<li class="gate-catch">{CROSS}{_esc(c)}</li>' for c in catches)
        rows.append(
            f'<li class="gate{" is-marked" if marked else ""}" style="--i:{i};--n:{n}">'
            f'<span class="gate-head">{icon_svg(icon) if icon else ""}<span class="gate-name">{_esc(name)}</span></span>'
            + (f'<ul class="gate-catches" aria-label="caught here">{chips}</ul>' if catches else "")
            + "</li>"
        )
    label = (title + ": " if title else "") + "; ".join(
        f"{name} catches {', '.join(c)}" if c else name for _, _, name, c in layers)
    return _figure("gates", f'<ol class="gates">{"".join(rows)}</ol>', title, label)


# ---------------------------------------------------------------- shift
def _split_arrow(line):
    if "->" not in line:
        raise ValueError(f"shift line needs 'before -> after', got {line!r}")
    a, _, b = line.partition("->")
    return a.strip(), b.strip()


def render_shift(lines):
    title, lines = _title(lines)
    if len(lines) < 2:
        raise ValueError("shift diagram needs a head line and at least one row")
    (ha, hb) = _split_arrow(lines[0])
    ia, ha = _iconed(ha)
    ib, hb = _iconed(hb)
    rows = []
    for line in lines[1:]:
        marked, text = _marked(line)
        rows.append((marked, *_split_arrow(text)))

    def head(icon, text, cls):
        return f'<span class="shift-head {cls}">{icon_svg(icon) if icon else ""}{_esc(text)}</span>'
    body = "".join(
        f'<li class="shift-row{" is-marked" if marked else ""}">'
        f'<span class="shift-from">{_esc(a)}</span>{ARROW}<span class="shift-to">{_esc(b)}</span></li>'
        for marked, a, b in rows
    )
    inner = (f'<div class="shift-heads" aria-hidden="true">{head(ia, ha, "is-from")}<span></span>{head(ib, hb, "is-to")}</div>'
             f'<ol class="shift">{body}</ol>')
    label = (title + ": " if title else "") + f"from {ha} to {hb}: " + "; ".join(f"{a} becomes {b}" for _, a, b in rows)
    return _figure("shift", inner, title, label)


RENDERERS = {"flow": render_flow, "sets": render_sets, "trend": render_trend, "bars": render_bars,
             "tiles": render_tiles, "gates": render_gates, "shift": render_shift}
