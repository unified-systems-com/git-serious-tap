# git-serious — Tell me when it breaks

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*Don't make me watch a dashboard.*

A message when main goes red, a nightly fails, a deploy finishes, a scorecard slips. Every dashboard has the same defect — you have to go and look at it — and the alert inverts that. It is also the feature most likely to be switched off, because the message-to-action ratio is the whole ballgame. The honest limit: alerts fire on *results*, because results are the only thing these tools model; nothing can alert that the gate configuration changed, only that a run went red afterwards.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **friends** milestone (git-serious-tap epic #2).

## Prior Art

Overlay survey, feature **09 · Tell me when it breaks** — [`doc-git-serious-overlay-consensus.md`](../docs/doc-git-serious-overlay-consensus.md) (§The nine; the coverage matrix places it by category). Built by effectively every tool in the survey, in some form. Axis: **operations** — this is a legibility feature first, not a security feature (register item 12, *more than security*).

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-tell-me-when-it-breaks | [Tell me when it breaks](#tell-me-when-it-breaks) | Proposed | Table-stakes (built by effectively everything; overlay survey #09) |

### Tell me when it breaks
----
RID: `req-git-serious-tell-me-when-it-breaks`
Status: `Proposed`
Feature: `table-stakes`
Milestone: `friends`

The instance can notify a configured channel when a collected observation crosses a stated condition, and the condition may be over configuration as well as results.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-tell-me-when-it-breaks-1 | Configuration Alert | Proposed | An alert fires when a ruleset's bypass list or required-check set changes between two observations, and a separate alert fires on a red gate lane; both name the object that changed. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
