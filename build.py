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

  - The Lab (see lab-tools.json): each entry is a self-contained tool that
    lives in its own repo (or, for the demo, a local folder). After the main
    site is built, every enabled tool is fetched, built with its own build
    command, and copied into dist/lab/<id>/. The Lab hub page
    (site-src/lab/index.html) gets its cards generated from the same list.

Usage: python3 build.py
Output: dist/

Environment:
  LAB_TOKEN  Optional GitHub token, only needed if a Lab tool repo is private.
"""

import html as html_lib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent
SRC = ROOT_DIR / "site-src"
DIST = ROOT_DIR / "dist"
PARTIALS = SRC / "partials"
LAB_CACHE = ROOT_DIR / ".lab-cache"
LAB_MARKER = "<!--LAB-CARDS-->"
LAB_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")

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


def load_lab_tools():
    """Read lab-tools.json and return the enabled entries, validated."""
    with open(ROOT_DIR / "lab-tools.json") as f:
        tools = json.load(f)

    enabled, seen = [], set()
    for tool in tools:
        tool_id = tool.get("id", "")
        if not LAB_ID_RE.match(tool_id):
            sys.exit(f"lab-tools.json: invalid id {tool_id!r} (use lowercase letters, digits, hyphens)")
        if tool_id in seen:
            sys.exit(f"lab-tools.json: duplicate id {tool_id!r}")
        seen.add(tool_id)
        if not tool.get("enabled", True):
            continue
        if bool(tool.get("repo")) == bool(tool.get("path")):
            sys.exit(f"lab-tools.json: {tool_id!r} needs exactly one of 'repo' or 'path'")
        for field in ("title", "description"):
            if not tool.get(field):
                sys.exit(f"lab-tools.json: {tool_id!r} is missing '{field}'")
        enabled.append(tool)
    return enabled


def render_lab_cards(tools):
    if not tools:
        return "<p>Nothing here yet — check back soon.</p>"

    esc = html_lib.escape
    cards = []
    for tool in tools:
        source_url = tool.get("sourceUrl") or (
            f"https://github.com/{tool['repo']}" if tool.get("repo") else ""
        )
        note = f'<p class="card-note">{esc(tool["note"])}</p>' if tool.get("note") else ""
        source = f' · <a class="card-link" href="{esc(source_url)}">Source</a>' if source_url else ""
        tags = f'<div class="card-tags">{esc(tool["tags"])}</div>' if tool.get("tags") else ""
        cards.append(
            '<div class="card">'
            f'<h3>{esc(tool["title"])}</h3>{tags}'
            f'<p class="card-hook">{esc(tool["description"])}</p>{note}'
            f'<a class="card-link" href="{{{{ROOT}}}}lab/{tool["id"]}/">Open →</a>{source}'
            "</div>"
        )
    return "\n".join(cards)


def redact(text, secret):
    return text.replace(secret, "***") if secret else text


def fetch_lab_tool(tool):
    """Put a fresh copy of the tool's source in .lab-cache/<id> and return that path."""
    checkout = LAB_CACHE / tool["id"]
    ignore = shutil.ignore_patterns(".git", "node_modules")

    if tool.get("path"):
        source = ROOT_DIR / tool["path"]
        if not source.is_dir():
            sys.exit(f"Lab tool {tool['id']!r}: local path {tool['path']!r} not found")
        shutil.copytree(source, checkout, ignore=ignore)
        return checkout

    token = os.environ.get("LAB_TOKEN", "")
    auth = f"x-access-token:{token}@" if token else ""
    url = f"https://{auth}github.com/{tool['repo']}.git"
    cmd = ["git", "clone", "--depth", "1"]
    if tool.get("ref"):
        cmd += ["--branch", tool["ref"]]
    result = subprocess.run(cmd + [url, str(checkout)], capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(
            f"Lab tool {tool['id']!r}: could not clone {tool['repo']} "
            f"(private repo? set LAB_TOKEN)\n{redact(result.stderr, token)}"
        )
    sha = subprocess.run(
        ["git", "-C", str(checkout), "rev-parse", "--short", "HEAD"],
        capture_output=True, text=True,
    ).stdout.strip()
    print(f"  {tool['id']}: {tool['repo']} @ {sha}")
    return checkout


def build_lab_tool(tool):
    """Fetch, build, and copy one tool into dist/lab/<id>/."""
    target = DIST / "lab" / tool["id"]
    if target.exists():
        sys.exit(f"Lab tool {tool['id']!r}: dist/lab/{tool['id']}/ already exists (clashes with site-src/lab/)")

    checkout = fetch_lab_tool(tool)

    if tool.get("build"):
        result = subprocess.run(tool["build"], shell=True, cwd=checkout)
        if result.returncode != 0:
            sys.exit(f"Lab tool {tool['id']!r}: build command failed: {tool['build']}")

    output = (checkout / tool.get("output", ".")).resolve()
    if checkout.resolve() not in output.parents and output != checkout.resolve():
        sys.exit(f"Lab tool {tool['id']!r}: 'output' must stay inside the repo")
    if not (output / "index.html").is_file():
        sys.exit(f"Lab tool {tool['id']!r}: no index.html in output folder {tool.get('output', '.')!r}")

    shutil.copytree(output, target, ignore=shutil.ignore_patterns(".git", "node_modules"))


def build_lab(tools):
    if LAB_CACHE.exists():
        shutil.rmtree(LAB_CACHE)
    if tools:
        print("Building Lab tools:")
    for tool in tools:
        build_lab_tool(tool)
    if LAB_CACHE.exists():
        shutil.rmtree(LAB_CACHE)


def build():
    config = load_config()
    lab_tools = load_lab_tools()
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
        html = html.replace(LAB_MARKER, render_lab_cards(lab_tools))
        html = html.replace("{{ROOT}}", root_prefix)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html)

    build_lab(lab_tools)

    print(f"Built site to {DIST}")
    if skipped:
        print("Skipped (hidden by config.json):")
        for s in skipped:
            print(f"  - {s}")


if __name__ == "__main__":
    build()
