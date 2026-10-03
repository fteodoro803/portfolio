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

### Where it shows up

It's decided: this is a Lab tool, since it's its own tool. It appears in two places:

- **The Projects page:** the normal Lab card.
- **The Resume page:** a card beside the PDF cards, so visitors find it where they'd look for a resume.

The Resume page cards currently need a PDF (`file`) in `content/resumes/*.md`. The second card needs a small change in `resume_cards` in `content.py` so an entry can have a `link` (e.g. `/lab/resume/`) instead of a `file`, with a button like "Explore →" instead of "Download PDF →". Document the new field in [CONTENT.md](CONTENT.md) when it's added.

### Steps

1. Tag every bullet in the master resume (the main piece of work). Agree the tag list first, then tag against it.
2. Convert the master resume to `resume.json` in the data shape above.
3. Build the page: render, filter, URL state, print stylesheet.
4. Add the `lab-tools.json` entry ([how](LAB.md#add-a-new-tool)).
5. Add the `link` support and the Resume page card.

### Open questions

- Needs the master resume as input, and a tag set agreed before any building.
