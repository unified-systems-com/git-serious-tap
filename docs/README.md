# git-serious docs

Product-specific documentation lives here, in the product repo — not in the TAP core repo.
The platform's docs describe the platform; these describe *this product*.

| Doc | What it is |
| --- | --- |
| [doc-git-serious-cicd-shape-review.md](doc-git-serious-cicd-shape-review.md) | What a real organization's CI/CD system actually contains, the gap against what we collect, and the models, edges, icons, and landing-page story that close it. |
| [doc-git-serious-cicd-security-prior-art.md](doc-git-serious-cicd-security-prior-art.md) | The space we operate in: products, open-source tools, best-practice sources distilled to observable conditions, and the incident history behind them. |
| [doc-git-serious-linux-kernel-pipeline.md](doc-git-serious-linux-kernel-pipeline.md) | How the Linux kernel ships software without pull requests or required checks — the pressure test for a forge-neutral vocabulary. |
| [doc-git-serious-vocab-from-incidents.md](doc-git-serious-vocab-from-incidents.md) | What 35 documented compromises require the graph to be able to express — the gap list that drove the vocabulary. |
| [doc-git-serious-vocab-security-standards.md](doc-git-serious-vocab-security-standards.md) | 29 security and supply-chain standards surveyed for the entities and relationships they name. |
| [doc-git-serious-vocab-platform-models.md](doc-git-serious-vocab-platform-models.md) | 16 platform, graph and tooling models, including a direct diff against the published GitHub graph schemas. |
| [doc-git-serious-field-players-academic.md](doc-git-serious-field-players-academic.md) | The academic signal network — research centres, professors, venues, and what to watch. |
| [doc-git-serious-field-players-practitioners.md](doc-git-serious-field-players-practitioners.md) | The practitioner signal network — attack researchers, tools, feeds, cadences. |
| [doc-git-serious-shape-of-a-pipeline.md](doc-git-serious-shape-of-a-pipeline.md) | A working model of git-based CI/CD — five nouns, the trust boundary, identity, the gate, supply chain — built from our own pipelines outward, with the seven organising principles and the walk-in order for an unfamiliar org. |
| [doc-git-serious-overlay-consensus.md](doc-git-serious-overlay-consensus.md) | The nine features every GitHub-overlay tool rebuilds (the **table-stakes** list), the seven-category coverage matrix, and the tenth feature none of them has: the shape of the system held over time. |
| [doc-git-serious-standing-at-day-one.md](doc-git-serious-standing-at-day-one.md) | Archival end-of-day audit of the first build day (2026-08-27): built / open / broken, and the second look at the via-negativa thesis. Dated snapshot; current state lives in the issues. |

**Status.** These are dated research passes, not canon. Requirements live in specs; what is
committed and moving lives in this repo's issues and milestones.

## The vocabulary corpus

The five vocabulary and field-player passes above feed one canonical artifact: the **domain vocabulary corpus**, which
lives with the vocabulary's owner rather than here — `specs/spec-github-core-vocabulary.md` in the
`github_core` plugin. That document is the decision record (what was accepted, rejected, and why);
these are the evidence behind it. The method is the `build-domain-vocabulary` skill.
