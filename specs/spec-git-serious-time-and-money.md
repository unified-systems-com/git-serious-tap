# git-serious — Time and money

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*Where are my ten minutes going, and why is the bill that?*

Duration per job, trend over time, minutes consumed, cost per workflow and repository. CI duration is a tax on every change, paid forever, and a lane that grew from two minutes to nine is invisible without a trend line. The honest limit: it optimises what exists and never asks whether the slow lane needed to run at all.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **friends** milestone (git-serious-tap epic #2).

## Prior Art

Overlay survey, feature **03 · Time and money** — [`doc-git-serious-overlay-consensus.md`](../docs/doc-git-serious-overlay-consensus.md) (§The nine; the coverage matrix places it by category). Built by five named incumbents, listed there. Axis: **operations** — this is a legibility feature first, not a security feature (register item 12, *more than security*).

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-time-and-money | [Time and money](#time-and-money) | Proposed | Table-stakes (built by 5 named incumbents; overlay survey #03) |

### Time and money
----
RID: `req-git-serious-time-and-money`

Status: `Proposed`
Feature: `table-stakes`
Milestone: `friends`

The instance reports duration per job and per workflow with a trend over the collected history, and minutes consumed per repository, from the timestamps already on collected runs and jobs.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-time-and-money-1 | Trend From Collected Runs | Proposed | For a workflow with collected history spanning at least two weeks, the instance shows its duration trend and the per-job breakdown of the latest run, with no additional API calls at view time. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
