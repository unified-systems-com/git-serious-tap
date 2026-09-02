# git-serious — What is waiting on me

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*What actually needs my attention today?*

One queue of pull requests and issues that need *you* — assigned, review-requested, mentioned — across every repository, noise removed. GitHub's notifications report events; people want obligations. The honest limit: pure triage — it moves work in front of you and knows nothing about the work.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **everyone** milestone (git-serious-tap epic #3).

## Prior Art

Overlay survey, feature **04 · What is waiting on me** — [`doc-git-serious-overlay-consensus.md`](../docs/doc-git-serious-overlay-consensus.md) (§The nine; the coverage matrix places it by category). Built by five named incumbents, listed there. Axis: **operations** — this is a legibility feature first, not a security feature (register item 12, *more than security*).

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-waiting-on-me | [What is waiting on me](#what-is-waiting-on-me) | Proposed | Table-stakes (built by 5 named incumbents; overlay survey #04) |

### What is waiting on me
----
RID: `req-git-serious-waiting-on-me`

Status: `Proposed`
Feature: `table-stakes`
Milestone: `everyone`

The instance shows one cross-repository queue of pull requests awaiting the viewer's review or action, derived from collected pull-request state.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-waiting-on-me-1 | One Queue Across Repositories | Proposed | A viewer with review requests in three repositories sees all three in one list, and a request already acted on drops out without manual dismissal. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
