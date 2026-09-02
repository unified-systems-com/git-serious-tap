# git-serious — Pin drift

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*Has anything I execute moved out from under me?*

An action referenced by tag or branch can be retargeted by its publisher at any time with no diff on our side. Dependabot, Renovate and pinact own the *remediation* (bump PRs); the table-stakes observation is the drift itself — the resolved SHA behind each reference at each observation, and whether it moved.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **friends** milestone (git-serious-tap epic #2).

## Prior Art

CI/CD security prior art — [`doc-git-serious-cicd-security-prior-art.md`](../docs/doc-git-serious-cicd-security-prior-art.md), §6 *Implications for git-serious* item 9 (*where it is table stakes*), with the observable-conditions tables in §3.10 and the ranked v0 list in item 7. Axis: **security**. The incumbents named there do this better than we will; the requirement is that it exist on the graph, beside the operations features, not that it win.

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-pin-drift | [Pin drift](#pin-drift) | Proposed | Table-stakes, security axis (prior art §6 item 9: must exist, will not win) |

### Pin drift
----
RID: `req-git-serious-pin-drift`
Status: `Proposed`
Feature: `table-stakes`
Milestone: `friends`

For every action reference the account's workflows consume, the instance records the SHA it resolved to at observation time and reports references whose resolved SHA changed between observations without the reference text changing.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-pin-drift-1 | Moved Tag Reported | Proposed | When a consumed action's tag is retargeted between two collections, the instance names the action, the two SHAs, and every workflow that consumes it. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
