# Portfolio site

Static site, built from `site-src/` into `dist/` by `build.py`, deployed automatically to GitHub Pages by the workflow in `.github/workflows/deploy.yml` on every push to `main`.

## To hide/show the Queue System page

Edit `config.json`:

```json
{
  "queueSystemVisible": false
}
```

Set it to `true` when you're ready to reveal it, commit, and push (or just edit the file directly on github.com — click it, click the pencil icon, change `false` to `true`, commit). GitHub Actions rebuilds and redeploys automatically within about a minute. When `false`, the Queue System page and its home-page card don't exist in the published output at all — it's not just hidden, the URL won't resolve.

## Before this is live

1. **Add your resume**: drop a PDF at `site-src/assets/resume.pdf` (a general, non-tailored version).
2. **Fill in the two demo links**: search for `PASTE_..._LIVE_URL_HERE` in `site-src/projects/pa-ride.html` and `site-src/projects/queue-system.html` and swap in the real URLs.
3. **Confirm the hackathon write-up**: `site-src/other-projects.html` has a draft note on `The Professionals' Portfolio` marked for your review — see the chat for the full findings.
4. **Custom domain** (optional): once you've bought a domain, add a `CNAME` file at the repo root containing just the domain (e.g. `fteodoro.dev`), and point your DNS at GitHub's servers per [GitHub's custom domain docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).

## The Lab

The Lab (`/lab/`) is a hub of small side projects. Each tool lives in its own repo; this repo holds the hub page and `lab-tools.json` (the tool list), and the build assembles everything into one site.

> **⚠️ Reminder: the site does not rebuild when a tool repo changes.** After you push to a tool's repo, rebuild the portfolio to publish it.

**To rebuild:** GitHub → **Actions** → **Build and deploy portfolio site** → **Run workflow**. Or from a terminal:

```
gh workflow run deploy.yml
```

**Full guide** — adding and editing tools, the rules a tool repo must follow, the `lab-tools.json` fields, troubleshooting, and expandable "why" explanations: see **[LAB.md](LAB.md)**.

## Local preview

```
python3 build.py
cd dist && python3 -m http.server 8000
```

`build.py` needs `git` (and network access) to fetch Lab tools that use `repo`. Tools that use `path` build offline.

Then open http://localhost:8000

## One-time repo setup

In the repo's Settings → Pages, set **Source** to **GitHub Actions** (not "Deploy from a branch") — the workflow handles the rest.
