# The Lab — how it works and how to add tools

The Lab (`/lab/`) is a hub of small side projects that visitors can open and use. Each tool lives in **its own GitHub repo**. This repo only holds the hub page and `lab-tools.json`, the list of tools.

Sections marked **▸ Why?** expand to explain the reasoning.

- [Quick reference](#quick-reference)
- [Add a new tool](#add-a-new-tool)
- [Update an existing tool](#update-an-existing-tool)
- [Rebuild the site](#rebuild-the-site)
- [Edit, hide, pin or remove a tool](#edit-hide-pin-or-remove-a-tool)
- [Rules for a tool repo](#rules-for-a-tool-repo)
- [`lab-tools.json` field reference](#lab-toolsjson-field-reference)
- [Troubleshooting](#troubleshooting)
- [Background](#background)

## Quick reference

| I want to… | Do this |
|---|---|
| Publish a change I made to a tool | Push to the tool's repo, then [rebuild the site](#rebuild-the-site) |
| Add a new tool | [Add a new tool](#add-a-new-tool) |
| Hide a tool temporarily | Set `"enabled": false` in `lab-tools.json`, push |
| Stop a broken tool blocking deploys | Same as above |
| Use a private tool repo | Add the `LAB_TOKEN` secret ([details](#private-tool-repos)) |
| Edit Lab cards in a browser | Pages CMS → **Lab tools** (see [CONTENT.md](CONTENT.md)); it edits `lab-tools.json` |

> **⚠️ The portfolio site does not rebuild when a tool repo changes.** Pushing to a tool repo does nothing to the live site until you [rebuild](#rebuild-the-site).

<details>
<summary><strong>▸ Why?</strong> — how tools get from separate repos onto one site</summary>

GitHub Pages publishes whatever folder the deploy workflow uploads (`dist/`). Right now that folder is assembled from several sources at build time:

```
portfolio repo ──────────────┐
telemetry-viz repo ──build──▶├──▶ dist/ ──▶ GitHub Pages ──▶ yoursite.dev
another-tool repo ───build──▶┘
```

So `dist/` ends up like this:

```
dist/
  index.html, about.html, ...          ← from the portfolio repo (build.py)
  lab/index.html                       ← hub page, from the portfolio repo
  lab/telemetry/index.html, app.js     ← from the telemetry-viz repo
  lab/another-tool/index.html, ...     ← from another-tool repo
```

Visitors just see one site. The separate repos only exist on your side.

Each tool repo stays a normal, standalone project with its own README, history and issues. It only has to follow the [rules](#rules-for-a-tool-repo) so the build knows what to publish.

</details>

## Add a new tool

1. **Create the tool's repo** and follow the [rules for a tool repo](#rules-for-a-tool-repo). For a plain HTML/JS tool, put the page in a `web/` folder.
2. **Add an entry to `lab-tools.json`** (a list; add a comma between entries):

   ```json
   {
     "id": "telemetry",
     "title": "Telemetry Visualiser",
     "type": "Tool",
     "tags": "JavaScript · WebSockets · UDP",
     "description": "One or two sentences for the hub card.",
     "note": "Optional short line under the description.",
     "repo": "fteodoro803/telemetry-viz",
     "output": "web",
     "enabled": true
   }
   ```

   The only fields you must fill in are `id`, `title`, `description`, and one of `repo` or `path`. The [field reference](#lab-toolsjson-field-reference) covers the rest.
3. **Preview it locally** (optional but recommended):

   ```
   python3 build.py
   cd dist && python3 -m http.server 8000
   ```

   Open http://localhost:8000/lab/. This needs `git` and network access for `repo` tools, and the local setup from the [README](README.md#local-preview).
4. **Commit and push to `main`.** The push triggers a rebuild, which publishes the tool.

Your tool is now at `/lab/<id>/` and has a card on the hub page.

## Update an existing tool

1. Make and push your change in the **tool's** repo.
2. [Rebuild the site](#rebuild-the-site) so the portfolio picks up the new version.

You don't need to edit anything in this repo unless you're changing the tool's card text, its `output` folder, or its build command.

## Rebuild the site

Do this after updating a tool repo:

1. Open the portfolio repo on GitHub → **Actions** → **Build and deploy portfolio site**.
2. Click **Run workflow** → choose branch `main` → **Run workflow**.
3. Wait about a minute. A green run means it's live. A red run means a tool failed to clone or build. The previous version of the site stays live in that case; open the run and read the log.

Or from a terminal:

```
gh workflow run deploy.yml
```

Every rebuild fetches the latest version of every enabled tool. Pushing to this repo's `main` also triggers one.

<details>
<summary><strong>▸ Why?</strong> — why isn't this automatic?</summary>

The deploy workflow only runs when the **portfolio** repo gets a push, because that's the only repo GitHub knows it belongs to. Nothing tells it a tool repo changed.

Ways to make it automatic, if the manual step ever gets annoying:

1. **Manual** (what we do now): press the Run workflow button. Simple, no setup.
2. **Scheduled:** add a nightly `schedule:` (cron) trigger to `.github/workflows/deploy.yml`. Updates show up within a day.
3. **Instant:** each tool repo gets a small workflow that notifies the portfolio on every push (`repository_dispatch`). This needs a personal access token stored as a secret in each tool repo, so it's the most setup.

</details>

## Edit, hide, pin or remove a tool

- **Change card text:** edit `title`, `tags`, `description` or `note` in `lab-tools.json`, push.
- **Hide a tool** without touching its repo: set `"enabled": false`, push. It's not fetched and not published, and its URL stops working.
- **Pin a tool** to a known-good version: set `ref` to a tag or branch, e.g. `"ref": "v1.0"` (commit hashes aren't supported).
- **Remove a tool:** delete its entry from `lab-tools.json`, push. The tool's repo is unaffected.
- **Change the order of cards:** reorder the entries in `lab-tools.json`.

<details>
<summary><strong>▸ Why?</strong> — why does one broken tool fail the whole deploy?</summary>

The alternative is to skip a broken tool and publish the rest. That would work, but the tool would vanish from the live site without anyone noticing, and you'd only find out when someone tells you.

A failing run is visible (red in Actions), and the **previous good site stays live** because the deploy step never runs. To unblock the portfolio, set the broken tool to `"enabled": false` and push.

</details>

## Rules for a tool repo

A tool repo can be written in any language or framework, as long as building it produces a folder of static files (HTML, JS, CSS, data) containing an `index.html`.

1. **Publish a subfolder, not the whole repo.** Put the page in `web/` for plain HTML tools, and set `"output": "web"`. For tools with a build step (React, Vite, etc.), use the build output folder (`dist`) and set `"build"` to the command that produces it.
2. **Keep everything else out of that folder:** companion programs (like a UDP bridge), tests, notes, `.env` files, config with IP addresses, and raw data.
3. **Use relative paths** for the tool's own files (`app.js`, not `/app.js`). The tool is served from `/lab/<id>/`, not from the site root.
4. **Link back to the hub** with `<a href="../">← Back to Lab</a>`.
5. **Don't depend on the portfolio's CSS or JS.** The tool must work on its own. It can look however it likes.
6. **Make it useful without extra setup** where you can, for example with demo data, so visitors can try it without installing anything.

Recommended layout for a tool with a companion program:

```
telemetry-viz/
  web/                   ← published (output: "web")
    index.html
    app.js
    demo-laps.json
  bridge/                ← NOT published
    bridge.py
    requirements.txt
  README.md              ← NOT published
```

Link to the companion from the page, for example "Download the bridge" pointing at the GitHub repo. Visitors get it from GitHub, not from your website.

<details>
<summary><strong>▸ Why?</strong> — why keep companion code out of the published folder?</summary>

The build copies everything in `output` onto the public website. Anything in that folder is downloadable by anyone at a URL.

If `output` were `"."` (the whole repo), the site would serve `/lab/telemetry/bridge/bridge.py`, the README, and everything else in the repo. That causes two problems:

- **Accidental leaks:** any file in the output folder is published. That includes a `.env` file, a config with your console's IP address, test captures, or notes.
- **Clutter:** the site fills up with files nobody visits, like `package.json`, tests and READMEs.

Publishing only `web/` avoids both. For tools with a build step this is automatic, since `dist` holds only compiled output.

</details>

<details>
<summary><strong>▸ Why?</strong> — why relative paths and a back link?</summary>

A tool lives at `/lab/telemetry/`, not at the site root. A path like `/app.js` looks for `yoursite.dev/app.js` and won't find it, while `app.js` resolves to `/lab/telemetry/app.js`.

The same goes for the back link: from `/lab/telemetry/`, `../` is `/lab/`. The tool can't use the portfolio's `{{ROOT}}` placeholder, because that's replaced only for pages built by this repo.

</details>

## `lab-tools.json` field reference

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Lowercase letters, digits, hyphens. Becomes the URL: `/lab/<id>/`. Must be unique. |
| `title` | yes | Card heading. |
| `description` | yes | Card text, one or two sentences. |
| `type` | no | Short label shown above the card title, e.g. `"Tool"` or `"Log"`. |
| `tags` | no | Small line of tech under the title, e.g. `"JavaScript · WebSockets"`. |
| `note` | no | Extra short line, e.g. "Needs a local bridge for live data; demo mode works standalone." |
| `repo` | one of `repo`/`path` | GitHub `owner/name`. Cloned fresh on every build. |
| `path` | one of `repo`/`path` | Local folder in this repo to copy instead. Used by the demo, and handy for testing offline. |
| `ref` | no | Branch or tag. Defaults to the repo's default branch. |
| `build` | no | Shell command run in a fresh checkout (e.g. `"npm ci && npm run build"`). Leave out for plain HTML. |
| `output` | no | Folder inside the repo to publish. Defaults to `"."` (everything), so set it, e.g. `"web"`. It must contain `index.html`. |
| `sourceUrl` | no | Link for the card's "Source" link. Defaults to the GitHub repo when `repo` is set. |
| `enabled` | no | `false` skips the tool entirely. Defaults to `true`. |

### Private tool repos

Public repos need nothing. For a private repo, create a GitHub token that can read that repo, and save it in the portfolio repo under Settings → Secrets and variables → Actions as **`LAB_TOKEN`**. For local builds, set the `LAB_TOKEN` environment variable.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Tool changes aren't on the live site | You haven't [rebuilt](#rebuild-the-site). |
| Run is red: "could not clone" | Typo in `repo`, or the repo is private and `LAB_TOKEN` isn't set (or lacks access). |
| Run is red: "build command failed" | The tool's own build broke. Run its build locally to see why. |
| Run is red: "no index.html in output folder" | `output` points at the wrong folder, or the build didn't produce one. |
| Tool page loads but is unstyled or blank | It's using absolute paths (`/app.js`). Switch to relative paths. |
| Tool isn't on the hub | Check `"enabled"` and that the JSON is valid (commas between entries). |
| Site is fine locally but red on GitHub | Build commands run on a clean Ubuntu machine; check for missing dependencies or things that only exist on your laptop. |

## Background

<details>
<summary><strong>▸ Why is the site still on GitHub Pages?</strong></summary>

Everything the Lab publishes is static files, which is exactly what GitHub Pages serves. Client-side tools (including the telemetry visualiser) run in the visitor's browser and need no server.

If a future tool needs a real backend (accounts, a database, secrets), keep the site on Pages and run only that backend elsewhere (Cloudflare Workers, Vercel, Supabase, etc., all with free tiers). The tool's page calls it over HTTP. That's usually simpler than moving the whole site.

</details>

<details>
<summary><strong>▸ Do all tools have to use the same language?</strong></summary>

No. The site itself is plain HTML/CSS/JS assembled by a Python script (`build.py`), but each tool picks its own stack. What matters is that building it produces static files. Tools with a build step declare it in `lab-tools.json`, and the build runs that command on GitHub's servers.

The Python in `build.py` is the only Python the site needs, and companion programs (like the telemetry bridge) can be in any language, since they run on the user's machine rather than on the site.

</details>

<details>
<summary><strong>▸ Why does the telemetry tool need a local bridge?</strong></summary>

Browsers can't receive UDP packets. That's a security limit of web pages, not something a different host would fix. Racing games send telemetry as UDP, so a small program on the same network (the "bridge") receives it, decodes it, and forwards it over a WebSocket. The page connects to the bridge at `ws://localhost:<port>`.

```
Console/PC ──UDP──▶ bridge (your laptop) ──WebSocket──▶ page (GitHub Pages)
```

A cloud relay doesn't help, because the game sends to your local network. Since most visitors won't run a bridge, the page should also have a demo/replay mode with recorded data.

</details>

<details>
<summary><strong>▸ What's in <code>lab-demo/</code>?</strong></summary>

A stand-in for a tool repo, so the Lab works end to end before any real tool repo exists. `lab-tools.json` points at it with `path` instead of `repo`. It's built the same way as a cloned repo. Once you have real tools, replace or remove the `lap-sim` entry and delete `lab-demo/`.

</details>
