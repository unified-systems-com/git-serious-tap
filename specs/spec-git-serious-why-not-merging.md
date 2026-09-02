# git-serious — Why isn't this merging

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*It's approved and green. What is it waiting for?*

A per-pull-request account of what stands between here and merged: required checks outstanding, reviews missing, branch behind, conflict, queue position. GitHub's merge box says *that* you cannot merge and is vague about *why* — especially when a required check will never report because nothing produces it, which presents as waiting rather than broken. The honest limit: merge-queue products answer in queue mechanics; they can say check `gate` is missing but not which workflow was supposed to produce it.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **self** milestone (git-serious-tap epic #1).

## Prior Art

Overlay survey, feature **05 · Why isn't this merging** — [`doc-git-serious-overlay-consensus.md`](../docs/doc-git-serious-overlay-consensus.md) (§The nine; the coverage matrix places it by category). Built by five named incumbents, listed there. Axis: **operations** — this is a legibility feature first, not a security feature (register item 12, *more than security*).

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-why-not-merging | [Why isn't this merging](#why-isnt-this-merging) | Proposed | Table-stakes (built by 5 named incumbents; overlay survey #05) |
| req-git-serious-why-not-merging-gate-chain | [The ruleset → check → workflow chain](#the-ruleset--check--workflow-chain) | Proposed | Improvement — the switching argument (tap#211 sketch); four fields, verification unfilled |

### Why isn't this merging
----
RID: `req-git-serious-why-not-merging`
Status: `Proposed`
Feature: `table-stakes`
Milestone: `self`

For a pull request, the instance lists every condition between it and merge — each required check with its state, reviews outstanding, branch currency — derived from the ruleset, status-check and run rows on the grid.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-why-not-merging-1 | Blocked Versus Never | Proposed | A pull request whose required check has no producing workflow is shown as *blocked on a check nothing produces*, distinguishably from one whose check is merely pending. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
### The ruleset → check → workflow chain
----
RID: `req-git-serious-why-not-merging-gate-chain`
Status: `Proposed`
Feature: `improvement`
Milestone: `self`

The improvement to the table-stakes feature above — the switching argument. Four fields, all
required (tap#206); a claim that needs special-case work rather than falling out of the
architecture is a feature commitment wearing an improvement's clothes.

- **Capability:** The answer names the chain: this ruleset requires check `gate`; that check is produced by this job in this workflow; that workflow last ran here, and this is what it trusts.
- **Incumbent's specific limitation:** Merge-queue products own this feature and answer in queue mechanics because their model stops at the check name; none holds the workflow that produces it, so "waiting" and "never" are indistinguishable.
- **Mechanism (why ours differs):** Ruleset, status check, workflow and job are typed nodes with edges between them (`github_core` self tier; the gate view on `feat/gate-view` is the first cut), so the chain is one traversal from the pull request.
- **Five-minute verification:** *(unfilled — the tap#211 improvements pass fills this; a claim a prospect cannot check in five minutes is not a selling point)*

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-why-not-merging-gate-chain-1 | Verifiable In Five Minutes | Proposed | A user with a running instance can confirm the capability against their own organisation inside five minutes, following the verification above. | Unfillable until the field above is filled. |

---
