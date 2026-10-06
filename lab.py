"""
The Lab: self-contained tools that live in their own repos.

lab-tools.json lists the tools. For each enabled one, build_lab() fetches it
(git clone of `repo`, or a copy of a local `path`), runs its build command,
and copies the output folder into dist/lab/<id>/. lab_specs() describes the
Projects-page cards from the same list (content.py draws them). See LAB.md for the
full guide.
"""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import content

ROOT_DIR = Path(__file__).parent
DIST = ROOT_DIR / "dist"
LAB_CACHE = ROOT_DIR / ".lab-cache"
LAB_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


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


def lab_specs(tools):
    """Card specs (see content.project_spec) for the Lab tools, in list order."""
    specs = []
    for index, tool in enumerate(tools):
        # An explicit empty "sourceUrl" hides the Source link, for a tool whose
        # repo is private (the "or" form this replaced treated "" as unset).
        if "sourceUrl" in tool:
            source_url = tool["sourceUrl"]
        else:
            source_url = f"https://github.com/{tool['repo']}" if tool.get("repo") else ""
        specs.append({
            "group": "live",
            "order": index,
            "slug": tool["id"],
            "featured": content.is_true(tool.get("featured")),
            "title": tool["title"],
            "label": tool.get("type") or "Tool",
            "tags": tool.get("tags", ""),
            "hook": tool["description"],
            "note": tool.get("note", ""),
            "primary": ("Open", f"{{{{ROOT}}}}lab/{tool['id']}/"),
            "secondary": [("Source", source_url)] if source_url else [],
        })
    return specs


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

    output = (checkout / (tool.get("output") or ".")).resolve()
    if checkout.resolve() not in output.parents and output != checkout.resolve():
        sys.exit(f"Lab tool {tool['id']!r}: 'output' must stay inside the repo")
    if not (output / "index.html").is_file():
        sys.exit(f"Lab tool {tool['id']!r}: no index.html in output folder {tool.get('output') or '.'!r}")

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
