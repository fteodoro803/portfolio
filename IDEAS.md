# Ideas

Things worth doing later. Nothing here is built yet. When one gets started, move its notes into the relevant doc and delete it from this list.

- [Resume explorer](#resume-explorer)

## Resume explorer

**What:** an interactive page that holds the exhaustive master resume and lets a visitor filter it by interest (backend, frontend, data, and so on). It sits beside the PDFs on the Resume page, not in place of them. Recruiters and ATS systems still want a file.

### How it would work

Built as a [Lab tool](LAB.md): its own repo, published under `/lab/<id>/`, with a card on the Projects page and a link from the Resume page. That keeps the portfolio repo untouched and follows the existing [rules for a tool repo](LAB.md#rules-for-a-tool-repo).

```
resume-explorer/
  web/                  ← published (output: "web")
    index.html
    app.js
    style.css
    resume.json         ← the master resume as data
  README.md             ← NOT published
```

The page reads `resume.json` and renders it. A tool can't use the portfolio's CSS, so it needs its own light styling (match the colours and fonts in [DESIGN.md](DESIGN.md)). Remember the "← Back to Lab" link.

Because it's a Lab tool, it has the usual Lab catch: the portfolio doesn't rebuild when the tool repo changes, so [rebuild the site](LAB.md#rebuild-the-site) after pushing.

### Data shape

Tags go on each bullet. A project or job gets its tags from the union of its bullets, so there's only one place to maintain them.

```json
{
  "tags": [
    { "id": "backend", "label": "Backend" },
    { "id": "frontend", "label": "Frontend" }
  ],
  "default": ["general"],
  "entries": [
    {
      "title": "Project or job name",
      "role": "Role",
      "dates": "2024",
      "bullets": [
        { "text": "One line, as on the resume.", "tags": ["backend", "data"] }
      ]
    }
  ]
}
```

- **Keep the tag list short**, about 6 to 10. A long list gets messy fast.
- An entry with no visible bullets hides itself.

### Behaviour

- **Start curated.** Don't open on the full wall of text. Pre-select the tags that match the General resume, and let people widen the selection or switch to one interest.
- **Shareable filters.** Keep the selected tags in the URL (`?tags=backend,data`), so a link like `/lab/resume/?tags=backend` opens that view.
- **Print / Save as PDF.** Add a print stylesheet so printing gives a clean one-page-ish resume of whatever view is on screen. Hide the filter controls when printing.

### Privacy

The page is public, so keep phone, address and email out of `resume.json`.

### Open questions

- Needs the master resume as input, and a tag set agreed before any building.
- Lab tool (own repo, as above) or a normal page here? A page here would be editable in the CMS and wouldn't need a rebuild step, but it would need new build code in `build.py`. The Lab route is the lighter change.
