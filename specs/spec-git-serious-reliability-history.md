# git-serious — Reliability history

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*Should I trust this red?*

The last N runs of one job as a strip: pass rate, flake rate, which tests fail intermittently. The most expensive question in daily CI use, unanswerable from one run; without history people re-run the job, which costs ten minutes and often lies. The honest limit: per-job, results-only — it says *this test is flaky*, never *this test became flaky the day the runner image changed*.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **friends** milestone (git-serious-tap epic #2).

## Prior Art

Overlay survey, feature **02 · Reliability history** — [`doc-git-serious-overlay-consensus.md`](../docs/doc-git-serious-overlay-consensus.md) (§The nine; the coverage matrix places it by category). Built by six named incumbents, listed there. Axis: **operations** — this is a legibility feature first, not a security feature (register item 12, *more than security*).

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-reliability-history | [Reliability history](#reliability-history) | Proposed | Table-stakes (built by 6 named incumbents; overlay survey #02) |
| req-git-serious-reliability-history-became-flaky | [When it became flaky, not that it is](#when-it-became-flaky-not-that-it-is) | Proposed | Improvement — the switching argument (tap#211 sketch); four fields, verification unfilled |

### Reliability history
----
RID: `req-git-serious-reliability-history`
Status: `Proposed`
Feature: `table-stakes`
Milestone: `friends`

For any job, the instance shows the outcome strip of its recent runs and a pass/flake rate, derived from collected `workflow_run` / `workflow_job` history rather than re-fetched on view.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-reliability-history-1 | Strip From History | Proposed | For a job with at least ten collected runs, the strip renders every run's conclusion in order with a pass rate, and a run the collector did not observe is shown as a gap, not as a pass. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
### When it became flaky, not that it is
----
RID: `req-git-serious-reliability-history-became-flaky`
Status: `Proposed`
Feature: `improvement`
Milestone: `friends`

The improvement to the table-stakes feature above — the switching argument. Four fields, all
required (tap#206); a claim that needs special-case work rather than falling out of the
architecture is a feature commitment wearing an improvement's clothes.

- **Capability:** The strip is aligned against the configuration history of the same job — runner image, action pins, workflow edits — so the answer is *this became flaky on the commit that changed X*.
- **Incumbent's specific limitation:** Incumbents hold no history of anything except results, so the question "what changed when this started failing" is unaskable.
- **Mechanism (why ours differs):** The grid keeps the job as *written* (declaration) and as *run* (execution) under one observation dimension, with history on both; the alignment is a traversal across the two layers, which is the DCOM seam.
- **Five-minute verification:** *(unfilled — the tap#211 improvements pass fills this; a claim a prospect cannot check in five minutes is not a selling point)*

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-reliability-history-became-flaky-1 | Verifiable In Five Minutes | Proposed | A user with a running instance can confirm the capability against their own organisation inside five minutes, following the verification above. | Unfillable until the field above is filled. |

---
