# Editing the site's content

All the text on the site lives in the `content/` folder as small files. You can edit them in a browser with **Pages CMS** (forms, no code), directly on GitHub, or locally. Every save goes through the same pipeline: a commit to `main` → the deploy workflow rebuilds → the site updates in about a minute.

Sections marked **▸ Why?** expand to explain the reasoning.

- [Quick reference](#quick-reference)
- [Set up Pages CMS (one time)](#set-up-pages-cms-one-time)
- [How saving works](#how-saving-works)
- [What you can edit](#what-you-can-edit)
- [Recipes](#recipes)
- [Writing tips](#writing-tips)
- [Editing without the CMS](#editing-without-the-cms)
- [Troubleshooting](#troubleshooting)
- [Background](#background)

## Quick reference

| I want to… | Where |
|---|---|
| Change the intro line on the home page | CMS → **Home page** |
| Change my bio, or add a photo | CMS → **About page** |
| Edit a case study | CMS → **Case studies** → pick one |
| Add or edit a smaller project | CMS → **Other projects** |
| Add a new resume variant | CMS → **Resumes** → new |
| Change email, LinkedIn, GitHub, footer | CMS → **Site details** |
| Add or edit a Lab card | CMS → **Lab tools** (see [LAB.md](LAB.md) for the tool repo side) |
| Hide something | Turn **Published** off. It disappears from the site completely |
| Change colours or layout | Not the CMS. See [DESIGN.md](DESIGN.md) |

## Set up Pages CMS (one time)

[Pages CMS](https://pagescms.org) is a free, open-source editor. It runs on its own website and edits files in your GitHub repo, so nothing about your hosting changes.

1. Make sure `.pages.yml` (in this repo's root) is on `main`. It tells the CMS what's editable.
2. Go to Pages CMS and sign in with GitHub.
3. Give it access to this repo (`fteodoro803/portfolio`) when it asks. You can limit it to just this repo.
4. Open the repo in the CMS. You should see the sections listed in [What you can edit](#what-you-can-edit).

The CMS's own screens may change wording over time. The steps are always: sign in, allow the repo, open it. If something differs, see their [docs](https://pagescms.org/docs/).

<details>
<summary><strong>▸ Why?</strong> — how does an editor for my site work without any hosting?</summary>

The CMS never touches your live site. It's a separate app that reads and writes files in your GitHub repo, the same as you would by hand. When you press save, it makes a commit to `main`. That commit triggers your existing deploy workflow, which rebuilds the site.

```
Pages CMS ──commit──▶ GitHub repo (main) ──triggers──▶ deploy workflow ──▶ live site
```

The site stays a static site on GitHub Pages. The CMS is just a friendlier way to make commits. `.pages.yml` describes which files it can edit and what fields each has.

</details>

## How saving works

1. You edit in the CMS and press **Save**. That commits to `main`.
2. The **Build and deploy portfolio site** workflow starts by itself. Watch it under **Actions** on GitHub.
3. About a minute later the change is live.

If the run turns red, the previous version of the site stays live. Open the run to see why ([Troubleshooting](#troubleshooting)).

<details>
<summary><strong>▸ Why?</strong> — why does it commit straight to <code>main</code>?</summary>

The site only deploys from `main`, so that's where changes have to land. It also means there's no preview or review step: what you save goes live. That's normal for a personal site, and every change is a commit, so any edit can be undone by reverting it on GitHub.

If you'd rather preview first, Pages CMS can be pointed at a separate branch, but then you'd merge it yourself each time. It's usually more hassle than it's worth here.

</details>

## What you can edit

| CMS section | Files | Shows up on |
|---|---|---|
| Site details | `content/site.yml` | Header, footer, contact links, page titles |
| Home page | `content/pages/home.md` | Intro line under your name |
| About page | `content/pages/about.md` | About page (text + optional photo) |
| Resume page intro | `content/pages/resume.md` | Text above the resume cards |
| Case studies | `content/case-studies/*.md` | `/projects/<name>.html`, plus a card on the home page |
| Other projects | `content/other-projects/*.md` | Other Projects page (card + pop-up) |
| Resumes | `content/resumes/*.md` | One card per variant on the Resume page |
| Lab tools | `lab-tools.json` | Lab hub cards (and which tools get built) |

Not editable in the CMS: the look of the site (`site-src/css/style.css`), the page layouts (`site-src/*.html`), and the Lab tools themselves, which live in their own repos.

### Fields worth knowing

**Case studies**
- **Published:** off hides the case study everywhere (page and card). The Queue System write-up is currently off.
- **Show on the home page:** off keeps the page but removes its home card.
- **Order:** lowest number first, on the home page and elsewhere.
- **Card summary / Short tags:** what shows on the home card. The full **Tags line** shows on the page itself.
- **Live demo URL:** leave empty for no demo button.

**Other projects**
- **Card summary:** leave empty to use the first sentence of the write-up.
- **Note:** small italic line under the write-up in the pop-up. The hackathon entry uses it for a draft note, so clear it once you're happy with the wording.

**Resumes**
- **PDF:** upload or pick a file. It's stored in `site-src/assets/uploads/`.
- **Mark as "Start here":** adds a label to that card. Use it on one resume.

## Recipes

### Add a resume variant

1. CMS → **Resumes** → add a new entry.
2. Fill in the name (e.g. "Software"), a line about who it's for, and upload the PDF.
3. Set **Order**. Save.

It appears on the Resume page. Nothing else needs changing.

<details>
<summary><strong>▸ Why a separate Resume page?</strong></summary>

A single "Download resume" link only works with one resume. With variants for different kinds of roles, a visitor needs somewhere to choose. The nav link now goes to a Resume page with one card per variant, so adding a variant is just adding an entry.

</details>

### Add a case study

1. CMS → **Case studies** → add a new entry.
2. Fill in the title, tags, card summary and write-up. Set **Order** and leave **Published** on.
3. Save. The page appears at `/projects/<title-as-filename>.html` and a card appears on the home page.

### Add a smaller project

CMS → **Other projects** → new entry. Title, tags and a write-up are enough.

### Add a photo to About

CMS → **About page** → **Photo** → upload. It shows as a round photo next to the heading. Add a description for screen readers.

### Add an image inside a write-up

In the editor, use the image button and upload. The site rewrites the saved path so it works from any page.

### Add a Lab tool

Add the card in CMS → **Lab tools**, and follow [LAB.md](LAB.md) for the tool's own repo.

## Writing tips

- **Headings** create the sections of a case study. Use a second-level heading (`##`) for each.
- **Bulleted lists** get the site's list style automatically.
- **A quote block becomes a highlighted callout.** Use it for "a decision worth being upfront about" or a status note.
- **Bold and italics** work as usual.
- Don't put the page title at the top of the write-up. It's added from the **Title** field.

<details>
<summary><strong>▸ Why do quotes become callouts?</strong></summary>

The CMS's editor has a quote button but no "callout" button. Mapping one to the other means you can place a callout anywhere in a write-up, using a button that already exists, with no special syntax to remember.

</details>

## Editing without the CMS

The files are plain text, so you can edit them anywhere.

**On GitHub:** open the file under `content/`, click the pencil icon, edit, and commit. The rebuild follows.

**Locally:**

```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python build.py
cd dist && python3 -m http.server 8000
```

(You only need the first two lines once.) Then open http://localhost:8000.

**The file format** is Markdown with a small settings block at the top:

```markdown
---
title: Pa-Ride
tags: React Native · TypeScript
featured: true
order: 1
---
## The problem

Text of the write-up goes here.
```

Everything between the `---` lines is a setting (`key: value`). Everything after is the write-up. The list of valid keys for each content type is in `.pages.yml`.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Saved in the CMS but the site didn't change | Check **Actions**. The run may still be going, or failed |
| Run is red at "Deploy to GitHub Pages" with a timeout | GitHub hiccup. Start a **new** run (Actions → Run workflow). Don't use "Re-run jobs" |
| Run is red at "Build site" | Read the error. Usual causes below |
| `file '…' not found` for a resume | The PDF path in the entry is wrong or the file wasn't uploaded |
| `missing 'title'` | An entry has an empty title |
| A page or card vanished | Its **Published** switch is off (or **Show on the home page**, for the home card) |
| CMS doesn't list a section | `.pages.yml` isn't on `main` yet, or has a syntax error |
| CMS says it can't access the repo | Re-check the GitHub access you granted it |
| Image shows as broken | The upload failed, or the path in the entry doesn't match the file in `site-src/assets/uploads/` |

## Background

<details>
<summary><strong>▸ Why Markdown files with a settings block?</strong></summary>

It's the format Pages CMS reads and writes natively, and it's plain text, so it works with git, GitHub's web editor, and any text editor. Nothing is locked into the CMS. If you stopped using it tomorrow, the content would still be there in readable files.

</details>

<details>
<summary><strong>▸ Why did <code>config.json</code> go away?</strong></summary>

It had one job: hide the Queue System page. That's now the **Published** switch on the case study itself, so there's one obvious place to look. Hiding still removes the page completely, not just its card.

</details>

<details>
<summary><strong>▸ Why is the build now dependent on Python packages?</strong></summary>

Turning Markdown into HTML and reading the settings blocks needs two small, standard libraries (`markdown` and `pyyaml`, listed in `requirements.txt`). The deploy workflow installs them automatically. You only need to install them yourself to preview locally.

</details>

<details>
<summary><strong>▸ How do the pieces fit together?</strong></summary>

```
content/*.md, site.yml, lab-tools.json   ← the words (edited in the CMS)
site-src/*.html, templates/, partials/   ← the page shapes, with {{placeholders}}
site-src/css, js                         ← the look
build.py + content.py + lab.py           ← combine them into dist/
```

Page templates contain placeholders like `{{site.name}}` and `{{page.body}}`, and marker comments like `<!--OTHER-PROJECTS-->`. The build fills them from `content/`. The top of `build.py` lists every placeholder and marker.

</details>
