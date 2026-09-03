# git-serious — Conjunction findings across object types

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*Where do a mutable reference, a privileged trigger and a long-lived secret meet in one job?*

Nearly every real compromise was a conjunction — a mutable reference, plus a privileged trigger, plus a long-lived secret. Each ingredient is individually tolerable and individually reported by some tool; almost nothing shows all three at once, in one place, for one job. The graph makes the conjunction a single traversal, and a Gryphon query that returns that path is the product's first killer finding; three separate lints are not.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **self** milestone (git-serious-tap epic #1).

## Prior Art

Prior art §6 items 1 and 8 ([`doc-git-serious-cicd-security-prior-art.md`](../docs/doc-git-serious-cicd-security-prior-art.md)); the shape-of-a-pipeline closing framing ([`doc-git-serious-shape-of-a-pipeline.md`](../docs/doc-git-serious-shape-of-a-pipeline.md), *nearly every real compromise was a conjunction*); the 35-incident corpus in `doc-git-serious-vocab-from-incidents.md`.

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-conjunction-findings | [Conjunction findings across object types](#conjunction-findings-across-object-types) | Proposed | Innovation (register disposition CANON unless noted); falsifier field is the MVP entry gate |

### Conjunction findings across object types
----
RID: `req-git-serious-conjunction-findings`

Status: `Proposed`
Feature: `innovation`
Milestone: `self`

The instance reports findings that are paths across object types — workflow (trigger, checkout ref, permissions) → action reference (mutability, drift) → reachable secret / cache / OIDC token — as one finding per path, never as three per-object lints.

**Falsifier (MVP entry gate, tap#211):** Falsifier: if, across the observed account and the incidents pack, the conjunction query returns nothing that the three per-object lints would not also have returned side by side, the path is a presentation choice rather than a finding class.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-conjunction-findings-1 | One Finding Per Path | Proposed | For a workflow with a `pull_request_target` trigger, a fork checkout, and a tag-referenced action that reaches a repository secret, the instance emits one finding carrying the whole path, and emits nothing when any leg is absent. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
