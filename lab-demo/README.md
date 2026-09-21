# lab-demo

Stand-in for a Lab tool that lives in its own repo. Each folder here behaves like a separate tool repo: `lab-tools.json` points at it with `"path"` instead of `"repo"`, and the build copies it into `dist/lab/<id>/` exactly as it would for a cloned repo.

It exists so the Lab works end to end before any real tool repo does, and to test the build without network access. Once you have a real tool repo, replace the entry in `lab-tools.json` (or set `"enabled": false`) and delete this folder.
