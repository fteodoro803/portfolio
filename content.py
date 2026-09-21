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

FRONT_MATTER_RE = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n(.*))?\Z", re.DOTALL)
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
    meta = yaml.safe_load(match.group(1)) or {}
    if not isinstance(meta, dict):
        raise SystemExit(f"{path}: front matter must be key: value pairs")
    return meta, (match.group(2) or "").strip()


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


# ---------- HTML fragments ----------

def case_study_cards(entries):
    """Home-page cards for featured case studies."""
    cards = []
    for e in entries:
        m = e["meta"]
        if str(m.get("featured", True)).lower() == "false":
            continue
        cards.append(
            '<div class="card">'
            f'<h3>{esc(m["title"])}</h3>'
            f'<div class="card-tags">{esc(m.get("cardTags") or m.get("tags", ""))}</div>'
            f'<p class="card-hook">{esc(m.get("summary", ""))}</p>'
            f'<a class="card-link" href="{{{{ROOT}}}}projects/{e["slug"]}.html">Read case study →</a>'
            "</div>"
        )
    return "\n".join(cards)


def case_study_values(entry):
    """Placeholder values for the case-study page template."""
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


def other_project_cards(entries):
    """Other Projects: a card plus a dialog with the full write-up."""
    cards = []
    for e in entries:
        m, pid = e["meta"], f'proj-{e["slug"]}'
        summary = m.get("summary") or first_sentence(e["body"])
        extra = ""
        if m.get("note"):
            extra += f'\n          <p class="dialog-note">{esc(m["note"])}</p>'
        if m.get("link"):
            extra += f'\n          <a class="card-link" href="{esc(m["link"])}">View repo →</a>'
        cards.append(f'''    <article class="project-card">
      <h3>{esc(m["title"])}</h3>
      <div class="card-tags">{esc(m.get("tags", ""))}</div>
      <p>{esc(summary)}</p>
      <button class="more-link" type="button" data-open="{pid}">Read more →</button>
      <dialog class="project-dialog" id="{pid}" aria-labelledby="{pid}-title">
        <div class="dialog-body">
          <form method="dialog"><button class="dialog-close" aria-label="Close">✕</button></form>
          <h3 id="{pid}-title">{esc(m["title"])}</h3>
          <div class="card-tags">{esc(m.get("tags", ""))}</div>
          {render_markdown(e["body"]) or ""}{extra}
        </div>
      </dialog>
    </article>''')
    return "\n\n".join(cards)


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
    """Optional About-page photo (set `photo` in content/pages/about.md)."""
    photo = str(page.get("photo") or "").lstrip("/")
    if not photo:
        return ""
    return f'<img class="about-photo" src="{{{{ROOT}}}}{esc(photo)}" alt="{esc(page.get("photoAlt") or "")}" />'
