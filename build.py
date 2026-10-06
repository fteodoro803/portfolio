#!/usr/bin/env python3
"""
Build script for the portfolio site.

Assembles site-src/ (page templates, CSS, JS) and content/ (everything you edit)
into dist/, the folder that gets published.

  - Shared pieces are pulled in with:
        <!--#include partial="nav.html"-->
    from site-src/partials/.

  - Text comes from content/ (see CONTENT.md). In a page, {{site.x}} is a value
    from content/site.yml and {{page.x}} is a value (or {{page.body}}, the
    rendered Markdown) from content/pages/<page>.md. Home uses home.md.

  - Marker comments are replaced with generated HTML:
        <!--FEATURED-CARDS-->    home-page cards: every project and Lab tool marked featured
        <!--CASE-STUDY-CARDS-->  Projects page: projects with format "page"
        <!--LAB-CARDS-->         Projects page: live-tool cards, from lab-tools.json
        <!--WRITEUP-CARDS-->     Projects page: projects with format "modal" (card + pop-up)
        <!--*-COUNT-->           how many cards are in each of those three sections
        <!--RESUME-CARDS-->      one card per resume variant

  - Projects and Lab tools all become cards of one shape (content.project_card).
    Each visible file in content/projects/ with `format: page` also becomes
    projects/<name>.html, using site-src/templates/case-study.html.

  - CSS and JS links get a version stamp (style.css?v=3f9a1c1b) that changes only
    when the file's contents change. GitHub Pages lets browsers reuse files for
    10 minutes; a new URL makes them fetch the new file straight away. See the
    "Caching" section of README.md.

  - {{ROOT}} becomes the relative path back to the site root ("" for top-level
    pages, "../" one folder down), so links work under any URL prefix.

  - The Lab (see lab.py and LAB.md): each tool in lab-tools.json is fetched,
    built with its own build command, and copied into dist/lab/<id>/.

Usage: python3 build.py     (needs: pip install -r requirements.txt)
Output: dist/

Environment:
  LAB_TOKEN  Optional GitHub token, only needed if a Lab tool repo is private.
"""

import hashlib
import re
import shutil
from pathlib import Path

import content
import lab

ROOT_DIR = Path(__file__).parent
SRC = ROOT_DIR / "site-src"
DIST = ROOT_DIR / "dist"
PARTIALS = SRC / "partials"
TEMPLATES = SRC / "templates"

INCLUDE_RE = re.compile(r'<!--#include partial="([^"]+)"-->')
NAV_RE = re.compile(r'<nav class="site-nav".*?</nav>', re.DOTALL)
ASSET_LINK_RE = re.compile(r"\{\{ROOT\}\}((?:css|js)/[^\"'?#]+\.(?:css|js))")


def render_includes(html):
    def _sub(match):
        return (PARTIALS / match.group(1)).read_text()

    prev = None
    while prev != html:  # partials may include other partials
        prev = html
        html = INCLUDE_RE.sub(_sub, html)
    return html


def mark_active_nav(html, rel):
    """Add aria-current="page" to the nav link that points at this page."""
    link = f'<a href="{{{{ROOT}}}}{rel}">'
    return NAV_RE.sub(
        lambda m: m.group(0).replace(link, link[:-1] + ' aria-current="page">', 1), html, count=1
    )


def fill(html, prefix, values, raw=()):
    """Replace {{prefix.key}} with values[key]; keys in `raw` are already HTML."""
    def _sub(match):
        key = match.group(1)
        value = values.get(key, "")
        value = "" if value is None else str(value)
        return value if key in raw else content.esc(value)

    return re.sub(r"\{\{" + prefix + r"\.(\w+)\}\}", _sub, html)


def asset_versions():
    """Short content hash for each CSS/JS file, e.g. {"css/style.css": "3f9a1c1b"}."""
    versions = {}
    for folder in ("css", "js"):
        for path in (SRC / folder).rglob("*"):
            if path.is_file():
                digest = hashlib.md5(path.read_bytes()).hexdigest()[:8]
                versions[path.relative_to(SRC).as_posix()] = digest
    return versions


class Site:
    """Everything the pages need, loaded once per build."""

    def __init__(self):
        self.asset_versions = asset_versions()
        self.site = content.load_site()
        self.pages = {}
        for path in (content.CONTENT / "pages").glob("*.md"):
            page = content.load_page(path.stem)
            page["photoBlock"] = content.photo_block(page)
            self.pages[path.stem] = page
        self.projects = content.load_projects()
        self.resumes = content.load_collection("resumes")
        self.lab_tools = lab.load_lab_tools()
        self.cards = content.sort_specs(
            [content.project_spec(e) for e in self.projects] + lab.lab_specs(self.lab_tools)
        )

    def render(self, html, rel, entry=None):
        html = render_includes(html)
        html = mark_active_nav(html, rel)

        featured = [c for c in self.cards if c["featured"]]
        html = html.replace("<!--FEATURED-CARDS-->", content.project_cards(featured))
        for marker, group in (("CASE-STUDY", "page"), ("LAB", "live"), ("WRITEUP", "modal")):
            cards = [c for c in self.cards if c["group"] == group]
            html = html.replace(f"<!--{marker}-CARDS-->", content.project_cards(cards))
            html = html.replace(f"<!--{marker}-COUNT-->", str(len(cards)))
        html = html.replace("<!--RESUME-CARDS-->", content.resume_cards(self.resumes, SRC))

        html = fill(html, "site", self.site)
        # Top-level pages read content/pages/<name>.md; the home page is "home".
        if "/" not in rel:
            name = "home" if rel == "index.html" else Path(rel).stem
            html = fill(html, "page", self.pages.get(name, {}), raw=("body", "photoBlock"))
        if entry is not None:
            html = fill(html, "entry", entry, raw=("body", "demoBlock"))

        # Version-stamp CSS/JS links so browsers refetch a file as soon as it changes.
        html = ASSET_LINK_RE.sub(
            lambda m: m.group(0) + "?v=" + self.asset_versions.get(m.group(1), ""), html
        )

        depth = rel.count("/")
        return html.replace("{{ROOT}}", "../" * depth)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def build():
    site = Site()
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    for path in SRC.rglob("*"):
        if path.is_dir() or PARTIALS in path.parents or TEMPLATES in path.parents:
            continue
        rel = path.relative_to(SRC)
        if path.suffix == ".html":
            write(DIST / rel, site.render(path.read_text(), rel.as_posix()))
        else:
            (DIST / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, DIST / rel)

    template = (TEMPLATES / "case-study.html").read_text()
    for entry in site.projects:
        if entry["meta"]["format"] != "page":
            continue
        rel = f"projects/{entry['slug']}.html"
        write(DIST / rel, site.render(template, rel, content.project_page_values(entry)))

    lab.build_lab(site.lab_tools)

    print(f"Built site to {DIST}")
    hidden = [e for e in (content.CONTENT / "projects").glob("*.md")
              if e.stem not in {p["slug"] for p in site.projects}]
    if hidden:
        print("Hidden by 'visible: false':")
        for path in hidden:
            print(f"  - projects/{path.name}")


if __name__ == "__main__":
    build()
