# git-serious — The repository page

> **First light, 2026-09-09** (double-tap-git-serious session; git-serious-tap#56). The generic
> page for ONE repository, built first for the TAP repository: the machinery on top, the open pull
> requests with the check verdict on each head, the status wall filtered to this repository. This
> spec owns the page's shape and reading order; the capabilities it surfaces own their claims
> ([status wall](spec-git-serious-status-wall.md), [why isn't this merging](spec-git-serious-why-not-merging.md),
> the machinery projection in github_core). `Feature:` / `Milestone:` marker lines follow the
> corpus convention.

## Philosophy

*What is the current state of this repository's build and its proposals?* — asked of ONE repository.

GitHub answers this across four tabs (Actions, Pull requests, Settings → Rules, the workflow
files) and none of them shows the machine. git-serious holds the machine as a graph, the proposals
as nodes joined to it, and the runs as rows, so one page can read top to bottom: who this
repository is, how its CI is wired, what is proposed against it and where each proposal stands,
and whether anything is broken right now. Current state only — the page is built towards an
overlay of failures on the machinery and a dig into *why*, and both are named non-goals until the
current-state picture is right.

Human-factors rules the layout follows: one vertical reading order and nothing side by side that
must be compared; the picture before the lists; every empty answer states what it means
(observed-empty versus could-not-read); GitHub's own words for GitHub's own states, never a
re-labelling; heights in `auto`, `vh` or `fr`, never pixels on the page grid.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature
target: **self** milestone (git-serious-tap epic #1). Pulled by git-serious-tap#56; demo-week
keystone target 3 ("map unified-systems").

## Prior Art

- The landing page (`grift/landing.grift.json`, git-serious-tap#35) — draws one repository's
  machinery already; this page reuses its projection, elevation and layout by entity id rather
  than re-minting them, and declares its own scene searches.
- [The workflow page](spec-git-serious-workflow-page.md) (2026-09-02) — the per-entity page
  pattern: a search with a URL-bound parameter, envelope-mode rows, table panels.
- github_core `spec-github-core-repo-landing-page-v0.md` — the plugin-level repository page
  (hero, activity, health, catalog); this product page is not that page: it is the operator's
  current-state view, and links out rather than repeating the catalogue.
- `github_core` pull requests (github-core#82, 2026-09-09) and custom properties (github-core#77,
  2026-09-08) — the two surfaces the page reads that did not exist a day earlier.

Provenance of every claim: **documented** unless marked *observed* or *inferred*.

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-repository-page | [The repository page](#the-repository-page) | Implemented | Four sections in reading order, parameterised by `?repo=owner/name`; no new code — searches, table panels, one graph panel |
| req-git-serious-repository-page-empties | [Empty answers say what they mean](#empty-answers-say-what-they-mean) | In Development | The three-state rule at page level: observed-empty, could-not-read, never-asked |

### The repository page
----
RID: `req-git-serious-repository-page`
Status: `Implemented`
Feature: `table-stakes`
Milestone: `self`

One page at `/git-serious/repository?repo=<owner/name>` shows one repository, top to bottom:

1. **This repository** — one row: the repository (a link to GitHub), its role, criticality,
   lifecycle and owner as the organization declares them (`github_repository.custom_properties`),
   the default branch, visibility, and the two "read?" states that qualify everything below.
2. **Machinery** — github_core's machinery projection over this repository: the landing page's
   projection, elevation and layout (visualization configuration, referenced by id) over this
   page's own scene searches, about sixty percent of the viewport, header hidden so the picture
   reads first. The owning account enters the scene through `OWNS_REPO`, never by an unfiltered
   account match — pull-request authors are accounts too since github-core#82 (git-serious-tap#57
   carries that fix to the landing and org pages).
3. **Open pull requests** — `pull_request` rows with `state = OPEN`, most recently updated first:
   number (to GitHub), title, author, head → base (the head linking to the branch on the
   repository it lives in, a fork's on the fork), the check verdict on the head as GitHub's
   combined rollup with the count it counted, review decision, mergeability, updated.
4. **Status wall, this repository** — the landing wall's columns minus the repository column,
   over runs filtered to this repository, newest first; then the repository's workflows with no
   run in the collected window.

Every panel derives from the grid through a search declaring `repo` as a REQUIRED string input with
no default, so the page names no repository of its own and is a query with a parameter, never a
special-cased view; `?repo=` reproduces the same page for any collected repository, and the page is
reached by link rather than from the top navigation, because without its parameter it has nothing
to show. *Observed 2026-09-09 on the 8010 dev stack for three repositories.*

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-repository-page-1 | Reading Order | Implemented | The page renders identity, machinery, open pull requests, status wall and not-observed in that order, one column, with the machinery slot sized in viewport units and every other row `auto`. | No pixels on the page grid. |
| req-git-serious-repository-page-2 | One Repository Throughout | Implemented | With `?repo=owner/name`, every section shows that repository alone: its row, its scene (exactly one account — the owner, reached through `OWNS_REPO`, never a pull-request author), its open pull requests, only its runs and only its workflows; another `?repo=` reproduces the page for that repository. | No default: without the parameter every panel states that `repo` is required. |
| req-git-serious-repository-page-3 | Machinery Reused, Not Re-minted | Implemented | The machinery panel references the landing page's projection, elevation and layout by entity id (configuration, not data); changing the landing's machinery module changes this page's. Its scene searches are its own, so no default repository rides in from another page. | Derive once; embed nothing from the data nodes. |
| req-git-serious-repository-page-4 | Build Status Per Proposal | Implemented | Each open pull request shows GitHub's combined check verdict on its head commit and how many checks it counted, App-produced ones included; a head with nothing run shows a dash, never green. | Reads `checks_rollup_state` / `checks` (github-core#82). |
| req-git-serious-repository-page-5 | Reachable | Proposed | The page is reachable from a repository on the org graph and from the double-tap cards without typing a URL. | Graph nav rules resolve to `html_url` only today; the same-origin page rule is tap#355. The double-tap cards can link today (`/git-serious/repository?repo=<full_name>`). |

### Empty answers say what they mean
----
RID: `req-git-serious-repository-page-empties`
Status: `In Development`
Feature: `improvement`
Milestone: `self`

The switching argument applied to a page: an empty list under a credential that could not look is
the most reassuring possible message, and this page must never produce it. The identity row
carries `pull_requests_observability` and `custom_properties_observability` as words; a dash in a
property column is a declared property this repository has not set; the not-observed table says
in its own description that absence of a run is not evidence the workflow never runs.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-repository-page-empties-1 | Three States On The Row | Implemented | The identity row shows `observed`, `unobservable` or blank (never asked) for pull requests and for custom properties, beside the values they qualify. | From the repository node's own fields. |
| req-git-serious-repository-page-empties-2 | Unset Is Not Missing | Implemented | A custom property the organization declares and this repository has not set renders as a dash in its own column, distinguishable from a repository whose properties could not be read. | null on the wire (github-core#77). |
| req-git-serious-repository-page-empties-3 | Zero Proposals Is A Fact Only When Observed | Proposed | An empty open-pull-requests table under `pull_requests_observability = observed` reads as "no open pull requests"; under `unobservable` the page says the list could not be read. | Needs a table-panel empty message keyed to a sibling field — tap#354. Until then the identity row's "PRs read?" column carries the state. |

## Non-goals (v0)

Failure overlays on the machinery; the "why is this red" dig into the machinery and the repository's
configuration; check-run nodes; a repository picker (the URL is the picker); the plugin-level
repository catalogue page that github_core already ships.
