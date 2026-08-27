#!/usr/bin/env python3
"""
Build script for the portfolio site.

Reads config.json (a simple {"flagName": true/false} map) and assembles
site-src/ into dist/, the folder that actually gets published:

  - A whole page can be gated with a marker as its very first line:
        <!--PAGE-IF:flagName-->
    If config[flagName] is false, that page is skipped entirely — it will
    not exist in dist/ and will not be reachable by URL once deployed.
    This is how the Queue System page gets hidden: flip the flag in
    config.json, and the page simply isn't published until you flip it
    back and push again.

  - A block within a page can be gated the same way:
        <!--IF:flagName--> ... <!--ENDIF-->
    Used for the Queue System's card on the home page.

  - Shared header/footer are pulled in with:
        <!--#include partial="nav.html"-->
    from site-src/partials/.

  - {{ROOT}} is replaced with the correct relative path prefix depending
    on how deep the file is (e.g. "" for top-level pages, "../" for
    pages under projects/), so links and the stylesheet work either way.

Usage: python3 build.py
Output: dist/
"""

import json
import re
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).parent
SRC = ROOT_DIR / "site-src"
DIST = ROOT_DIR / "dist"
PARTIALS = SRC / "partials"

INCLUDE_RE = re.compile(r'<!--#include partial="([^"]+)"-->')
IF_BLOCK_RE = re.compile(r'<!--IF:(\w+)-->(.*?)<!--ENDIF-->', re.DOTALL)
PAGE_IF_RE = re.compile(r'^\s*<!--PAGE-IF:(\w+)-->\s*\n')


def load_config():
    with open(ROOT_DIR / "config.json") as f:
        return json.load(f)


def render_includes(html):
    def _sub(match):
        partial_name = match.group(1)
        partial_path = PARTIALS / partial_name
        return partial_path.read_text()
    # allow includes inside includes (nav/footer are flat here, but safe to loop)
    prev = None
    while prev != html:
        prev = html
        html = INCLUDE_RE.sub(_sub, html)
    return html


def render_if_blocks(html, config):
    def _sub(match):
        flag, block = match.group(1), match.group(2)
        return block if config.get(flag, False) else ""
    return IF_BLOCK_RE.sub(_sub, html)


def build():
    config = load_config()
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    skipped = []

    for path in SRC.rglob("*"):
        if PARTIALS in path.parents or path == PARTIALS:
            continue
        rel = path.relative_to(SRC)
        out_path = DIST / rel

        if path.is_dir():
            out_path.mkdir(parents=True, exist_ok=True)
            continue

        if path.suffix != ".html":
            out_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, out_path)
            continue

        html = path.read_text()

        page_if_match = PAGE_IF_RE.match(html)
        if page_if_match:
            flag = page_if_match.group(1)
            if not config.get(flag, False):
                skipped.append(str(rel))
                continue
            html = PAGE_IF_RE.sub("", html, count=1)

        depth = len(rel.parts) - 1  # subfolders below site-src root
        root_prefix = "../" * depth

        html = render_includes(html)
        html = render_if_blocks(html, config)
        html = html.replace("{{ROOT}}", root_prefix)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html)

    print(f"Built site to {DIST}")
    if skipped:
        print("Skipped (hidden by config.json):")
        for s in skipped:
            print(f"  - {s}")


if __name__ == "__main__":
    build()
