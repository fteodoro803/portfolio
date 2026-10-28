# The Lab — how it works and how to add tools

The Lab is the "Try it live" section of the Projects page (`/projects.html`; `/lab/` redirects there). It holds small side projects that visitors can open and use. Each tool lives in **its own GitHub repo**. This repo only holds the Projects page and `lab-tools.json`, the list of tools.

Sections marked **▸ Why?** expand to explain the reasoning.

- [Quick reference](#quick-reference)
- [Add a new tool](#add-a-new-tool)
- [Putting a project on the portfolio](#putting-a-project-on-the-portfolio)
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
| Put an app that runs on a server (Cloud Run etc.) on the portfolio | [Putting a project on the portfolio](#putting-a-project-on-the-portfolio) |
| Hide a tool temporarily | Set `"enabled": false` in `lab-tools.json`, push |
| Stop a broken tool blocking deploys | Same as above |
| Use a private tool repo | Make sure `LAB_TOKEN` can read it: add the repo to the token's list ([details](#private-tool-repos)) |
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
  lab/index.html                       ← redirect to the Projects page
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
     "screenshotKind": "web",
     "cardImages": [
       { "image": "assets/uploads/telemetry-1.webp", "alt": "What the picture shows" }
     ],
     "enabled": true
   }
   ```

   The fields you must fill in are `id`, `title`, `description`, `screenshotKind`, at least one entry in `cardImages`, and one of `repo` or `path`. The build fails without the pictures. How to capture and save them is in [Add card pictures](CONTENT.md#add-card-pictures). The [field reference](#lab-toolsjson-field-reference) covers the rest.
3. **Preview it locally** (optional but recommended):

   ```
   python3 build.py
   cd dist && python3 -m http.server 8000
   ```

   Open http://localhost:8000/projects.html. This needs `git` and network access for `repo` tools, and the local setup from the [README](README.md#local-preview).
4. **Commit and push to `main`.** The push triggers a rebuild, which publishes the tool.

Your tool is now at `/lab/<id>/` and has a card on the Projects page.

## Putting a project on the portfolio

For an app that runs on a server and sleeps when idle (Cloud Run scaled to zero, for example). It can't live on GitHub Pages, and linking straight to it leaves the visitor on a blank tab for several seconds while it cold-starts. So the portfolio hosts a small **demo entry page** instead. It opens instantly, explains the demo, and pings the app so it wakes up while the visitor reads.

```
case study ──"Try the live demo"──▶ /lab/<id>/ (static, instant) ──▶ the app (already awake)
                                         │ on load: ping the app, show "Ready" when it answers
```

It's an ordinary Lab entry (the page lives in the app's repo, see [Add a new tool](#add-a-new-tool)) with `"card": false`, so it publishes a page but adds no card to the Projects page. The project's own case study keeps its card and gets the demo button.

### Steps

1. **Design the entry page** with the person ([below](#designing-the-entry-page)), then copy the [`demo-entry/`](demo-entry/index.html) template into the app's repo as `lab-web/index.html` and fill it in. The finished page is the first thing a visitor sees, so it should read like the app, not the portfolio.
2. **Get it onto the branch the portfolio builds from** (`ref`, below). In the queue system that's `release`.
3. **Add the Lab entry** to `lab-tools.json`:

   ```json
   {
     "id": "queue-demo",
     "title": "Queue System: live demo",
     "card": false,
     "repo": "fteodoro803/queue-system",
     "ref": "release",
     "output": "lab-web",
     "enabled": true
   }
   ```

   **A private repo needs `LAB_TOKEN` to be able to read it, and a fine-grained token only reaches the repos on its list.** Add the repo to the token before you rebuild, or the build fails with a 403 ([details](#private-tool-repos)).
4. **Point the case study at it.** In `content/projects/<project>.md` set `demoUrl: lab/<id>/` (a path without `https://` is resolved from the site root, so it works on every page).
5. **[Rebuild the site](#rebuild-the-site).** The portfolio only picks up the page when it rebuilds.
6. **Check it.** Open the case study, press the demo button, and watch the chip go from "Demo is getting ready" to "Demo is ready". Check it on a phone width too.
7. **Remind the owner of the follow-up:** once the page is live, the app's own entry route (`/`) can redirect straight into the app, so there is one copy of the text, not two.

### Designing the entry page

Ask these, then draft the page and preview it (open the HTML in a browser) before it goes anywhere.

| Ask | Why |
|---|---|
| Who is the visitor, and what should they do first? | Sets the intro line and the order of the cards |
| What are the doors into the app? (roles, screens, personas) | One card each. Link them to the app's real routes |
| Does the demo auto-sign-in or seed data? Is it shared, and when does it reset? | Goes in the note. Visitors need to know they may see each other's changes |
| What shouldn't they enter? | A one-line warning, such as no real names or contact details |
| What does the app look like? | Take the colours and fonts from the app's design system (`DESIGN_SYSTEM.md` or similar) and put them in the template's `:root` tokens |
| Does one door make sense, or several? | One card is fine. The queue demo has three because the point is watching one view react to another |

Rules the page follows, so keep them when you edit it:

- **Plain static HTML, CSS and JS.** It's a Lab tool, so [the rules for a tool repo](#rules-for-a-tool-repo) apply. The back link `../` is already in the template.
- **Links to the app are full URLs in the HTML,** so they work without JavaScript. The ping and the chip are only a bonus.
- **The links are never disabled.** If the ping fails or takes more than 20 seconds, the chip says so and the links still work.
- **Ping the app's root address.** Cloud Run holds the request until an instance is up, so the answer arriving means "ready". The request is `no-cors`, which can't read the answer, and that's all it needs.

<details>
<summary><strong>▸ Why?</strong> — why not just link straight to the app?</summary>

Cloud Run scales to zero when idle. The first request after a quiet spell starts a new instance, which takes a few seconds, and the browser shows a blank tab the whole time. A visitor can't tell that from a broken link.

A static page on the portfolio has no cold start. Landing there first gives the visitor something to read, and the ping on load means the app is usually awake by the time they click through. Keeping the app running all the time (`min-instances=1`) would remove the wait too, but costs money every month.

</details>

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
4. **Link back to the Projects page** with `<a href="../">← Back to Projects</a>`. `../` is the old `/lab/` page, which forwards to the address set by `projectsPage` in `content/site.yml`, so a changed address is a one-line edit.
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
| `type` | no | Short label shown above the card title, e.g. `"Tool"` or `"Log"`. Defaults to `"Tool"`. |
| `featured` | no | `true` also shows the card on the home page. Defaults to off. |
| `tags` | no | Small line of tech under the title, e.g. `"JavaScript · WebSockets"`. |
| `note` | no | Extra short line, e.g. "Needs a local bridge for live data; demo mode works standalone." |
| `repo` | one of `repo`/`path` | GitHub `owner/name`. Cloned fresh on every build. |
| `path` | one of `repo`/`path` | Local folder in this repo to copy instead. Used by the demo, and handy for testing offline. |
| `ref` | no | Branch or tag. Defaults to the repo's default branch. |
| `build` | no | Shell command run in a fresh checkout (e.g. `"npm ci && npm run build"`). Leave out for plain HTML. |
| `output` | no | Folder inside the repo to publish. Defaults to `"."` (everything), so set it, e.g. `"web"`. It must contain `index.html`. |
| `sourceUrl` | no | Link for the card's "Source" link. Defaults to the GitHub repo when `repo` is set. Set to `""` to hide the link, for a private repo. (Pages CMS can't save an empty value; edit `lab-tools.json` directly.) |
| `screenshotKind` | yes | `"web"` or `"phone"`. How the card shows the pictures: a framed page, or a whole phone screen. Same for every picture. |
| `cardImages` | yes | List of `{ "image", "alt" }`, one to five. The first is the cover; more get arrows and dots. See [Add card pictures](CONTENT.md#add-card-pictures). |
| `card` | no | `false` publishes the page but adds no card to the Projects page, and `description` and the card pictures aren't needed. For a [demo entry page](#putting-a-project-on-the-portfolio). Defaults to `true`. |
| `enabled` | no | `false` skips the tool entirely. Defaults to `true`. |

### Private tool repos

Public repos need nothing. A private repo needs a GitHub token that can read it, saved in the portfolio repo under Settings → Secrets and variables → Actions as **`LAB_TOKEN`**. For local builds, set the `LAB_TOKEN` environment variable.

`LAB_TOKEN` is a fine-grained personal access token, and **a fine-grained token only works for the repos listed on it**. So each time a new private repo joins the Lab:

1. GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens → open the token behind `LAB_TOKEN`.
2. Under **Repository access**, add the new repo. It needs **Contents: Read** and nothing more.
3. Re-run the portfolio's deploy workflow.

If you skip step 2, the build fails with a 403 on that repo (git words it as "Write access to repository not granted", even though it only reads). A token also expires on the date you chose when you made it, and then every private repo fails at once. When that happens, make a new token with read access to all the private repos and save it as `LAB_TOKEN` again.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Tool changes aren't on the live site | You haven't [rebuilt](#rebuild-the-site). |
| Run is red: "could not clone" (often a 403) | Typo in `repo`, or the repo is private and `LAB_TOKEN` isn't set, has expired, or doesn't list this repo. See [Private tool repos](#private-tool-repos). |
| Run is red: "build command failed" | The tool's own build broke. Run its build locally to see why. |
| Run is red: "no index.html in output folder" | `output` points at the wrong folder, or the build didn't produce one. |
| Tool page loads but is unstyled or blank | It's using absolute paths (`/app.js`). Switch to relative paths. |
| Run is red: "add at least one card image" (or "alt text", or "screenshotKind") | The tool's entry is missing its pictures. See [Add card pictures](CONTENT.md#add-card-pictures). |
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

