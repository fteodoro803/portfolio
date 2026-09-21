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
        <!--CASE-STUDY-CARDS-->  featured case-study cards (home)
        <!--OTHER-PROJECTS-->    Other Projects cards and dialogs
        <!--RESUME-CARDS-->      one card per resume variant
        <!--LAB-CARDS-->         Lab hub cards, from lab-tools.json

  - Each visible file in content/case-studies/ becomes projects/<name>.html,
    using site-src/templates/case-study.html.

  - {{ROOT}} becomes the relative path back to the site root ("" for top-level
    pages, "../" one folder down), so links work under any URL prefix.

  - The Lab (see lab.py and LAB.md): each tool in lab-tools.json is fetched,
    built with its own build command, and copied into dist/lab/<id>/.

Usage: python3 build.py     (needs: pip install -r requirements.txt)
Output: dist/

Environment:
  LAB_TOKEN  Optional GitHub token, only needed if a Lab tool repo is private.
"""

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


class Site:
    """Everything the pages need, loaded once per build."""

    def __init__(self):
        self.site = content.load_site()
        self.pages = {}
        for path in (content.CONTENT / "pages").glob("*.md"):
            page = content.load_page(path.stem)
            page["photoBlock"] = content.photo_block(page)
            self.pages[path.stem] = page
        self.case_studies = content.load_collection("case-studies")
        self.other_projects = content.load_collection("other-projects")
        self.resumes = content.load_collection("resumes")
        self.lab_tools = lab.load_lab_tools()

    def render(self, html, rel, entry=None):
        html = render_includes(html)
        html = mark_active_nav(html, rel)

        html = html.replace("<!--CASE-STUDY-CARDS-->", content.case_study_cards(self.case_studies))
        html = html.replace("<!--OTHER-PROJECTS-->", content.other_project_cards(self.other_projects))
        html = html.replace("<!--RESUME-CARDS-->", content.resume_cards(self.resumes, SRC))
        html = html.replace("<!--LAB-CARDS-->", lab.render_lab_cards(self.lab_tools))

        html = fill(html, "site", self.site)
        # Top-level pages read content/pages/<name>.md; the home page is "home".
        if "/" not in rel:
            name = "home" if rel == "index.html" else Path(rel).stem
            html = fill(html, "page", self.pages.get(name, {}), raw=("body", "photoBlock"))
        if entry is not None:
            html = fill(html, "entry", entry, raw=("body", "demoBlock"))

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
    for entry in site.case_studies:
        rel = f"projects/{entry['slug']}.html"
        write(DIST / rel, site.render(template, rel, content.case_study_values(entry)))

    lab.build_lab(site.lab_tools)

    print(f"Built site to {DIST}")
    hidden = [e for e in (content.CONTENT / "case-studies").glob("*.md")
              if e.stem not in {c["slug"] for c in site.case_studies}]
    if hidden:
        print("Hidden by 'visible: false':")
        for path in hidden:
            print(f"  - case-studies/{path.name}")


if __name__ == "__main__":
    build()
