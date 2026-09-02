# git-serious — The status wall

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*Is anything broken right now?*

One live table of every workflow run across every repository, newest first, red and green — the single most-rebuilt artifact in the space. GitHub scopes everything to one repository, so "is anything broken" costs one tab per repo and nobody pays it. The honest limit of every incumbent: it says a thing is red, never whether that matters, and a wall with two permanent reds stops being looked at.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **self** milestone (git-serious-tap epic #1).

## Prior Art

Overlay survey, feature **01 · The status wall** — [`doc-git-serious-overlay-consensus.md`](../docs/doc-git-serious-overlay-consensus.md) (§The nine; the coverage matrix places it by category). Built by six named incumbents, listed there. Axis: **operations** — this is a legibility feature first, not a security feature (register item 12, *more than security*).

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-status-wall | [The status wall](#the-status-wall) | Proposed | Table-stakes (built by 6 named incumbents; overlay survey #01) |
| req-git-serious-status-wall-criticality | [Criticality sort and the not-observed state](#criticality-sort-and-the-not-observed-state) | Proposed | Improvement — the switching argument (tap#211 sketch); four fields, verification unfilled |

### The status wall
----
RID: `req-git-serious-status-wall`
Status: `Proposed`
Feature: `table-stakes`
Milestone: `self`

One page lists the latest run of every workflow across every repository of the observed account, newest first, with its conclusion, and derives entirely from the grid (`workflow_run` rows already collected by `github_core`) — a page and a query, never a special-cased feature (the overlay survey's build rule).

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-status-wall-1 | Every Repository, One Glance | Proposed | On an instance observing an account with N repositories, the wall shows the latest run of every workflow in all N without a per-repository action, and a repository with no runs collected renders as *not observed*, never as absent or green. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
### Criticality sort and the not-observed state
----
RID: `req-git-serious-status-wall-criticality`
Status: `Proposed`
Feature: `improvement`
Milestone: `self`

The improvement to the table-stakes feature above — the switching argument. Four fields, all
required (tap#206); a claim that needs special-case work rather than falling out of the
architecture is a feature commitment wearing an improvement's clothes.

- **Capability:** The wall sorts by the criticality of what is red — the gate lane of the repository that ships the product outranks a nightly on a nostalgia repo — and renders three states per cell: green, red, and *not observed with this credential*.
- **Incumbent's specific limitation:** Incumbents hold a run-history model only; they cannot rank because they do not know what any lane is for, and a cell they could not fetch renders identically to a cell that is fine.
- **Mechanism (why ours differs):** Criticality is derived from the graph (which ruleset requires which check, which workflow publishes) and the observation dimension carries what the credential could not see; both are already on the grid, so the sort and the third state are a query, not a feature.
- **Five-minute verification:** *(unfilled — the tap#211 improvements pass fills this; a claim a prospect cannot check in five minutes is not a selling point)*

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-status-wall-criticality-1 | Verifiable In Five Minutes | Proposed | A user with a running instance can confirm the capability against their own organisation inside five minutes, following the verification above. | Unfillable until the field above is filled. |

---
