# Learnings

## A fine-grained token only reaches the repos you list
*28 October 2026 · GitHub tokens*

**How the portfolio build reads a private repo**

```mermaid
flowchart LR
  B[Portfolio build<br/>GitHub Actions] -->|LAB_TOKEN| Q[queue-system]
  B -->|LAB_TOKEN| C[carpool-app-2]
  B -.->|403, repo not on the list| X[Any other private repo]
  classDef server fill:#EEEDFE,stroke:#534AB7,color:#3C3489
  classDef external fill:#F1EFE8,stroke:#5F5E5A,color:#444441
  class B server
  class Q,C,X external
```
*Purple = runs in the build, grey = a repo outside the portfolio*

- **The trick**: `LAB_TOKEN` is a fine-grained token, so it comes with a list of repos. A new private repo gets a 403 until you add it to that list with Contents: Read.
- **Old habit → new**: one classic token opens everything you own → one fine-grained token opens only the repos on its list.
- **Gotcha**: git says "Write access to repository not granted" for this 403, even though the build only reads. The wording is misleading, so read it as "this token can't reach this repo".
- **Gotcha**: the token expires on the date you picked, and then every private repo fails at once.

```python
url = f"https://x-access-token:{token}@github.com/{repo}.git"
```
