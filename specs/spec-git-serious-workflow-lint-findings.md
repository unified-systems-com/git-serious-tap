# git-serious — Per-workflow lint findings

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*Which of my workflows has a known-bad pattern in it?*

Static findings on workflow files: injection sinks, unpinned actions, over-broad permissions, dangerous triggers. zizmor and CodeQL's Actions pack do this better than we will, so the rule is consume, don't rebuild (prior art §6 item 5): run them with our read-only credential and land their finding IDs as typed findings attached to workflow and step nodes, with origin, collector and justification recorded so scanner disagreement is data.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **self** milestone (git-serious-tap epic #1).

## Prior Art

CI/CD security prior art — [`doc-git-serious-cicd-security-prior-art.md`](../docs/doc-git-serious-cicd-security-prior-art.md), §6 *Implications for git-serious* item 9 (*where it is table stakes*), with the observable-conditions tables in §3.10 and the ranked v0 list in item 7. Axis: **security**. The incumbents named there do this better than we will; the requirement is that it exist on the graph, beside the operations features, not that it win.

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-workflow-lint-findings | [Per-workflow lint findings](#per-workflow-lint-findings) | Proposed | Table-stakes, security axis (prior art §6 item 9: must exist, will not win) |

### Per-workflow lint findings
----
RID: `req-git-serious-workflow-lint-findings`

Status: `Proposed`
Feature: `table-stakes`
Milestone: `self`

The instance carries per-workflow lint findings from at least one established scanner as typed `finding` nodes attached to the workflow (and step, where the scanner locates it) they concern, with the scanner and rule ID recorded on each.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-workflow-lint-findings-1 | Scanner Findings On The Graph | Proposed | After a collection run, a workflow that a scanner flags carries a finding node naming the scanner and rule, reachable from the workflow node; a workflow the scanner did not evaluate carries no finding and renders as *not observed* by that scanner — never as clean. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
