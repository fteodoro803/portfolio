"""
Content loading and rendering.

Everything editable lives in content/ as Markdown files with YAML front matter
(the format Pages CMS reads and writes) plus content/site.yml for site details.
This module reads those files and turns them into HTML fragments for build.py.
See CONTENT.md for the full guide.
"""

import html as html_lib
import re
from pathlib import Path

import markdown
import yaml

ROOT_DIR = Path(__file__).parent
CONTENT = ROOT_DIR / "content"

# The settings block can be empty (`---` then `---`), which is how Pages CMS saves a
# file with no settings, and may use Windows line endings.
FRONT_MATTER_RE = re.compile(r"\A---[ \t]*\r?\n(?:(.*?)\r?\n)?---[ \t]*(?:\r?\n(.*))?\Z", re.DOTALL)
FIRST_SENTENCE_RE = re.compile(r"^.*?[.!?](?=\s|$)", re.DOTALL)
# Uploaded media is stored as "assets/..." (or "/assets/..."). Rewrite it so it works
# from any page depth and under a sub-path like /portfolio/.
ASSET_URL_RE = re.compile(r'(src|href)="/?(assets/[^"]*)"')

esc = lambda text: html_lib.escape(str(text), quote=True)


def read_entry(path):
    """Return (meta, body) for a Markdown file with optional YAML front matter."""
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text.strip()
    meta = yaml.safe_load(match.group(1) or "") or {}
    if not isinstance(meta, dict):
        raise SystemExit(f"{path}: front matter must be key: value pairs")
    body = (match.group(2) or "").strip()
    # Pages CMS has, at least once, saved an empty front matter block as
    # `---\n---\n---\n\n---\n\n<body>` instead of `---\n---\n<body>`. Our regex is lenient
    # enough to parse that without error, silently treating the stray `---` lines as
    # body content (which then renders as a horizontal rule). Catch it here instead.
    if body == "---" or body.startswith("---\n"):
        raise SystemExit(f"{path}: body starts with a stray '---' — front matter is likely corrupted")
    return meta, body


def load_site():
    """Site-wide details from content/site.yml."""
    with open(CONTENT / "site.yml", encoding="utf-8") as f:
        site = yaml.safe_load(f) or {}
    site["githubHandle"] = re.sub(r"^https?://", "", site.get("github", ""))
    return site


def load_page(name):
    """Front matter and rendered body for content/pages/<name>.md, or empty if none."""
    path = CONTENT / "pages" / f"{name}.md"
    if not path.exists():
        return {}
    meta, body = read_entry(path)
    return {**meta, "body": render_markdown(body)}


def load_collection(folder):
    """Visible entries in content/<folder>/, sorted by `order` then filename.

    Each entry is {"slug", "meta", "body"} where body is the raw Markdown.
    """
    entries = []
    for path in sorted((CONTENT / folder).glob("*.md")):
        meta, body = read_entry(path)
        if str(meta.get("visible", True)).lower() == "false":
            continue
        if not meta.get("title"):
            raise SystemExit(f"{path}: missing 'title'")
        entries.append({"slug": path.stem, "meta": meta, "body": body})
    def sort_key(e):
        order = e["meta"].get("order")  # a CMS may leave this blank
        return (order if isinstance(order, (int, float)) else 9999, e["slug"])

    entries.sort(key=sort_key)
    return entries


def render_markdown(text):
    """Markdown to HTML using the site's component classes.

    Lists become .project-bullets, blockquotes become .callout, and uploaded
    media paths are made relative to the site root.
    """
    out = markdown.markdown(text, extensions=["sane_lists"])
    out = out.replace("<ul>", '<ul class="project-bullets">')
    out = out.replace("<blockquote>", '<div class="callout">').replace("</blockquote>", "</div>")
    return ASSET_URL_RE.sub(r'\1="{{ROOT}}\2"', out)


def first_sentence(text):
    """First sentence of Markdown text, as plain text, for card summaries."""
    plain = re.sub(r"[*_`]", "", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text))
    match = FIRST_SENTENCE_RE.match(plain.strip())
    return match.group(0) if match else plain.strip()


# ---------- Project cards ----------
#
# Every project (a content/projects/ file or a Lab tool) is turned into the same card
# "spec" and drawn by project_card(), so all cards share one layout. Only the type label
# and the primary action change. Sections of the Projects page are picked by `group`.

PROJECT_FORMATS = ("page", "modal")
# Order of groups when cards from different groups share a list (the home page).
GROUP_RANK = {"page": 0, "live": 1, "modal": 2}


def is_true(value, default=False):
    """Read a front-matter flag; a CMS may leave it blank or save it as text."""
    if value is None or value == "":
        return default
    return str(value).lower() == "true"


def load_projects():
    """Visible entries in content/projects/, each checked for a valid `format`."""
    entries = load_collection("projects")
    for e in entries:
        if e["meta"].get("format") not in PROJECT_FORMATS:
            raise SystemExit(
                f"content/projects/{e['slug']}.md: 'format' must be one of {', '.join(PROJECT_FORMATS)}"
            )
    return entries


def project_spec(entry):
    """Card spec for a content/projects/ entry."""
    m, fmt = entry["meta"], entry["meta"]["format"]
    secondary = []
    if m.get("demoUrl"):
        secondary.append(("Demo", m["demoUrl"]))
    if m.get("link"):
        secondary.append(("Repo", m["link"]))
    spec = {
        "group": fmt,
        "order": m.get("order"),
        "slug": entry["slug"],
        "featured": is_true(m.get("featured")),
        "title": m["title"],
        "label": "Case study" if fmt == "page" else "Write-up",
        "neutral": fmt == "modal",
        "tags": m.get("cardTags") or m.get("tags", ""),
        "hook": m.get("summary") or first_sentence(entry["body"]),
        "secondary": secondary,
    }
    if fmt == "page":
        spec["primary"] = ("Read more", f'{{{{ROOT}}}}projects/{entry["slug"]}.html')
    else:
        # The pop-up shows the role and the stack on separate lines, and repeats
        # the links as buttons so they sit next to the full write-up.
        links = []
        if m.get("demoUrl"):
            links.append(("Try the demo", m["demoUrl"]))
        if m.get("link"):
            links.append(("View repo", m["link"]))
        spec["dialog"] = {
            "role": m.get("role", ""),
            "tags": m.get("tags", ""),
            "body": render_markdown(entry["body"]),
            "note": m.get("note", ""),
            "links": links,
        }
        spec["quiet"] = True
    return spec


def sort_specs(specs):
    """Group first (case studies, live tools, write-ups), then `order`, then name."""
    def key(s):
        order = s["order"] if isinstance(s["order"], (int, float)) else 9999
        return (GROUP_RANK[s["group"]], order, s["slug"])

    return sorted(specs, key=key)


def project_card(spec):
    """One project card. `spec` keys are described in project_spec()."""
    title = esc(spec["title"])
    hidden = lambda text: f'<span class="visually-hidden">{text}</span>'
    dialog = spec.get("dialog")
    pid = f'proj-{spec["slug"]}'

    # The main button's ::after stretches over the whole card (see style.css), so the
    # card has one real link and the small links sit above it in the top row.
    if dialog:
        primary = (
            f'<button class="pill primary" type="button" data-open="{pid}" aria-haspopup="dialog">'
            f'Read more{hidden(": " + title)} →</button>'
        )
    else:
        label, href = spec["primary"]
        primary = f'<a class="pill primary" href="{esc(href)}">{esc(label)}{hidden(" " + title)} →</a>'

    secondary = "".join(
        f'<a class="card-link" href="{esc(href)}">{esc(label)}{hidden(" for " + title)}</a>'
        for label, href in spec["secondary"]
    )
    links = f'<div class="card-links">{secondary}</div>' if secondary else ""
    pill = f'<span class="card-type{" neutral" if spec.get("neutral") else ""}">{esc(spec["label"])}</span>'
    tags = f'<div class="card-tags">{esc(spec["tags"])}</div>' if spec.get("tags") else ""
    note = f'<p class="card-note">{esc(spec["note"])}</p>' if spec.get("note") else ""

    html = (
        f'<article class="card project-card{" is-quiet" if spec.get("quiet") else ""}">'
        f'<div class="card-head">{pill}{links}</div>'
        f'<h3>{title}</h3>{tags}'
        f'<p class="card-hook">{esc(spec["hook"])}</p>{note}'
        f'<div class="card-actions">{primary}</div>'
    )
    if dialog:
        role = f'<p class="dialog-role">{esc(dialog["role"])}</p>' if dialog["role"] else ""
        dtags = f'<div class="card-tags">{esc(dialog["tags"])}</div>' if dialog["tags"] else ""
        extra = f'<p class="dialog-note">{esc(dialog["note"])}</p>' if dialog["note"] else ""
        buttons = "".join(
            f'<a class="pill outline" href="{esc(href)}">{esc(label)} →</a>' for label, href in dialog["links"]
        )
        html += (
            f'<dialog class="project-dialog" id="{pid}" aria-labelledby="{pid}-title">'
            '<div class="dialog-head"><div class="dialog-titles">'
            # Focus lands on the title when the dialog opens, so no ring shows until Tab.
            f'<h2 id="{pid}-title" tabindex="-1" autofocus>{title}</h2>{role}{dtags}</div>'
            '<form method="dialog"><button class="dialog-close" aria-label="Close">✕</button></form>'
            "</div>"
            f'<div class="dialog-body">{dialog["body"]}{extra}{buttons}</div>'
            "</dialog>"
        )
    return html + "</article>"


def project_cards(specs):
    return "\n".join(project_card(s) for s in specs)


def project_page_values(entry):
    """Placeholder values for the project page template (format: page)."""
    m = entry["meta"]
    demo = ""
    if m.get("demoUrl"):
        label = m.get("demoLabel") or "Try the live demo →"
        note = f' <span class="tags">{esc(m["demoNote"])}</span>' if m.get("demoNote") else ""
        demo = f'<p><a class="button" href="{esc(m["demoUrl"])}">{esc(label)}</a>{note}</p>'
    return {
        "title": m["title"],
        "tags": m.get("tags", ""),
        "demoBlock": demo,
        "body": render_markdown(entry["body"]),
    }


def resume_cards(entries, src_dir):
    """Resume page: one card per resume variant with a download link."""
    cards = []
    for e in entries:
        m = e["meta"]
        file = str(m.get("file", "")).lstrip("/")
        if not file or not (src_dir / file).is_file():
            raise SystemExit(f"content/resumes/{e['slug']}.md: file {file!r} not found in site-src/")
        label = '<span class="card-type">Start here</span>' if m.get("recommended") else ""
        desc = f'<p class="card-hook">{esc(m["description"])}</p>' if m.get("description") else ""
        cards.append(
            '<div class="card">'
            f'{label}<h3>{esc(m["title"])}</h3>{desc}'
            f'<a class="card-link" href="{{{{ROOT}}}}{esc(file)}">Download PDF →</a>'
            "</div>"
        )
    return "\n".join(cards)


def photo_block(page):
    """Optional home-page photo (set `photo` in content/pages/home.md)."""
    photo = str(page.get("photo") or "").lstrip("/")
    if not photo:
        return ""
    return f'<img class="about-photo" src="{{{{ROOT}}}}{esc(photo)}" alt="{esc(page.get("photoAlt") or "")}" />'
