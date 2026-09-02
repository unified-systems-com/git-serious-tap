# git-serious — Branch-protection tiers

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*What actually protects the default branch of each repository?*

Which rulesets and branch-protection rules govern each default branch, what they require, and who may bypass them. Scorecard grades this; we must at least show it. Two traps the incumbents fall into: the classic branch-protection API does not know about rulesets and reports a ruleset-protected branch as unprotected, and `bypass_actors` needs write access to read — so a blank must render as *not observable*, never as *nobody*.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **self** milestone (git-serious-tap epic #1).

## Prior Art

CI/CD security prior art — [`doc-git-serious-cicd-security-prior-art.md`](../docs/doc-git-serious-cicd-security-prior-art.md), §6 *Recommendations* item 9 (*where it is table stakes*), with the observable-conditions tables in §3.10 and the ranked v0 list in item 7. Axis: **security**. The incumbents named there do this better than we will; the requirement is that it exist on the graph, beside the operations features, not that it win.

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-branch-protection-tiers | [Branch-protection tiers](#branch-protection-tiers) | Proposed | Table-stakes, security axis (prior art §6 item 9: must exist, will not win) |

### Branch-protection tiers
----
RID: `req-git-serious-branch-protection-tiers`
Status: `Proposed`
Feature: `table-stakes`
Milestone: `self`

For every repository, the instance shows the rulesets governing its default branch, the rules each enforces, the required checks, and the bypass list in three states: none, some, or not observable with the credential held.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-branch-protection-tiers-1 | Three States On Bypass | Proposed | A ruleset whose bypass list the credential could not read renders as *not observable*, distinguishably from an empty list, and a repository governed only by rulesets is never reported as unprotected. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
