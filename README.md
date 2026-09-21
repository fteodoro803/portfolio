# Portfolio site

Static site on GitHub Pages. Text lives in `content/`, page shapes and styling in `site-src/`, and `build.py` combines them into `dist/`. The workflow in `.github/workflows/deploy.yml` builds and deploys on every push to `main`.

| I want to… | Read |
|---|---|
| Edit text, projects, resumes, or hide something | **[CONTENT.md](CONTENT.md)**. Editable in a browser with Pages CMS |
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
