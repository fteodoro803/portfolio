# Portfolio site

**To change something on the site, use [Pages CMS →](https://pagescms.org)** (sign in with GitHub, open this repo). No code needed. See [CONTENT.md](CONTENT.md) for how.

Static site on GitHub Pages. Text lives in `content/`, page shapes and styling in `site-src/`, and `build.py` combines them into `dist/`. The workflow in `.github/workflows/deploy.yml` builds and deploys on every push to `main`.

| I want to… | Read |
|---|---|
| Edit text, projects, resumes, or hide something | **[Pages CMS](https://pagescms.org)** in a browser. Guide: **[CONTENT.md](CONTENT.md)** |
| Add or update a Lab tool | **[LAB.md](LAB.md)** |
| Change colours, fonts or components | **[DESIGN.md](DESIGN.md)** |

## Editing content

Use [Pages CMS](https://pagescms.org) (forms, no code), or edit the files in `content/` directly on GitHub. Saving commits to `main` and the site rebuilds in about a minute. Setup, recipes and troubleshooting are in **[CONTENT.md](CONTENT.md)**.

## The Lab

The Lab (`/lab/`) is a hub of small side projects. Each tool lives in its own repo; this repo holds the hub page and `lab-tools.json` (the tool list), and the build assembles everything into one site.

> **⚠️ Reminder: the site does not rebuild when a tool repo changes.** After you push to a tool's repo, rebuild the portfolio to publish it.

**To rebuild:** GitHub → **Actions** → **Build and deploy portfolio site** → **Run workflow**. Or from a terminal:

```
gh workflow run deploy.yml
```

If a run fails at "Deploy to GitHub Pages" with a timeout, start a **new** run this way instead of using "Re-run jobs" (re-running inside the same run uploads a second artifact, which the deploy step rejects).

Full guide: **[LAB.md](LAB.md)**.

## Caching (why changes can take a few minutes to show)

GitHub Pages tells browsers they may reuse any file for **10 minutes** (`cache-control: max-age=600`), and there's no setting to change that. Two things follow:

- **Styling and scripts show up straight away.** The build adds a version stamp to the CSS and JS links (for example `style.css?v=b2d32183`). The stamp is a short fingerprint of the file's contents, so it changes only when the file does. A changed file gets a new address, and browsers fetch it immediately instead of using their saved copy.
- **Page text can lag by up to 10 minutes** for someone who visited recently, because the HTML page itself can't be stamped: its address has to stay the same. A hard refresh (`Cmd+Shift+R` / `Ctrl+Shift+R`) or an incognito window shows the latest straight away.

<details>
<summary><strong>▸ Why?</strong> — why stamp the CSS and JS but not the pages?</summary>

Browsers decide whether to reuse a saved file by its address. If a file's address never changes, the browser can't tell it has been updated, so it may keep showing the old copy until the 10 minutes are up.

For CSS and JS we control the address, so the build appends `?v=<fingerprint>`. Because the fingerprint comes from the file's contents, an unchanged file keeps the same address (so it stays cached and loads fast), and a changed file gets a new one.

Pages can't work the same way. Visitors and links use addresses like `/about.html`, and adding a changing suffix would break those links and bookmarks. So pages stay subject to the 10-minute window. Uploaded images and PDFs aren't stamped either, but if you replace one, upload it under a new file name and it will show immediately.

</details>

## Local preview

One-time setup (the build needs two small Python packages):

```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Then, whenever you want to preview:

```
.venv/bin/python build.py
cd dist && python3 -m http.server 8000
```

Open http://localhost:8000. `build.py` also needs `git` and network access to fetch Lab tools that use `repo`; tools that use `path` build offline.

## One-time repo setup

In the repo's Settings → Pages, set **Source** to **GitHub Actions** (not "Deploy from a branch"). The workflow handles the rest.

## Still to do

- **Confirm the hackathon write-up:** `content/other-projects/professionals-portfolio.md` has a draft note (the **Note** field) that shows publicly. Clear it once you're happy with the wording.
- **Custom domain** (optional): once you've bought a domain, add a `CNAME` file at the repo root containing just the domain (e.g. `fteodoro.dev`), and point your DNS at GitHub's servers per [GitHub's custom domain docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).
