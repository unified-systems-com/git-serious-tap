# git-serious — Does this meet our bar

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*Which of my repositories are below the line, and on what?*

A scorecard: standards a repository is supposed to meet, scored across the estate so laggards sort to the top. Consistency decays silently and in one direction, and every check is something you already believe — the value is asking it of all nineteen at once, repeatedly. The honest limit: the checks are a fixed list in the vendor's little language, so they can only find problems somebody already anticipated.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **self** milestone (git-serious-tap epic #1).

## Prior Art

Overlay survey, feature **07 · Does this meet our bar** — [`doc-git-serious-overlay-consensus.md`](../docs/doc-git-serious-overlay-consensus.md) (§The nine; the coverage matrix places it by category). Built by five named incumbents, listed there. Axis: **operations** — this is a legibility feature first, not a security feature (register item 12, *more than security*).

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-meets-our-bar | [Does this meet our bar](#does-this-meet-our-bar) | Proposed | Table-stakes (built by 5 named incumbents; overlay survey #07) |
| req-git-serious-meets-our-bar-executable-principles | [Principles with executable expressions, evaluated against config and operation](#principles-with-executable-expressions-evaluated-against-config-and-operation) | Proposed | Improvement — the switching argument (tap#211 sketch); four fields, verification unfilled |

### Does this meet our bar
----
RID: `req-git-serious-meets-our-bar`

Status: `Proposed`
Feature: `table-stakes`
Milestone: `self`

The instance scores every repository of the observed account against a stated set of standards and sorts the estate by shortfall, with each score traceable to the collected facts that produced it.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-meets-our-bar-1 | Estate Sorted By Shortfall | Proposed | Across all repositories of the observed account, each standard's pass/fail is shown per repository with the fact behind it, and a standard that could not be evaluated for a repository renders as *not evaluable*, never as pass. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
### Principles with executable expressions, evaluated against config and operation
----
RID: `req-git-serious-meets-our-bar-executable-principles`

Status: `Proposed`
Feature: `improvement`
Milestone: `self`

The improvement to the table-stakes feature above — the switching argument. Four fields, all
required (tap#206); a claim that needs special-case work rather than falling out of the
architecture is a feature commitment wearing an improvement's clothes.

- **Capability:** The standards are the team's own operational principles, each with an executable expression (a Search on the grid), evaluated against the pipeline as *written* and as it *ran* — and the two can disagree, which is itself the finding.
- **Incumbent's specific limitation:** Scorecards are a fixed vendor list evaluated against declared metadata or a settings snapshot; they cannot hold a team's own intent, and they never check what actually ran against what was configured.
- **Mechanism (why ours differs):** `Search` already dispatches Gryphon, ORM and module runners behind one envelope, so a principle is a statement plus an edge to the thing that evaluates it; the observation dimension separates declaration from execution so one principle yields two evaluations. See `spec-git-serious-principles-as-predicate.md`.
- **Five-minute verification:** *(unfilled — the tap#211 improvements pass fills this; a claim a prospect cannot check in five minutes is not a selling point)*

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-meets-our-bar-executable-principles-1 | Verifiable In Five Minutes | Proposed | A user with a running instance can confirm the capability against their own organisation inside five minutes, following the verification above. | Unfillable until the field above is filled. |

---
