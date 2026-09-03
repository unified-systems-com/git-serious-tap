# git-serious — SHA-pinning status

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*Are the things we execute pinned to something immutable?*

Only a full commit hash is immutable; a tag looks permanent and is not. This is one org field now (`sha_pinning_required`) plus a per-reference fact derivable from YAML already parsed. Table stakes, and the single fastest read of an organisation's real supply-chain maturity.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **self** milestone (git-serious-tap epic #1).

## Prior Art

CI/CD security prior art — [`doc-git-serious-cicd-security-prior-art.md`](../docs/doc-git-serious-cicd-security-prior-art.md), §6 *Implications for git-serious* item 9 (*where it is table stakes*), with the observable-conditions tables in §3.10 and the ranked v0 list in item 7. Axis: **security**. The incumbents named there do this better than we will; the requirement is that it exist on the graph, beside the operations features, not that it win.

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-sha-pinning-status | [SHA-pinning status](#sha-pinning-status) | Proposed | Table-stakes, security axis (prior art §6 item 9: must exist, will not win) |

### SHA-pinning status
----
RID: `req-git-serious-sha-pinning-status`

Status: `Proposed`
Feature: `table-stakes`
Milestone: `self`

The instance shows, per repository and for the account, the share of action references pinned by full SHA versus tag or branch, and whether the organisation setting requiring SHA pins is enabled.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-sha-pinning-status-1 | Pin Posture Per Repository | Proposed | For the observed account, each repository shows its pinned/unpinned reference counts with the unpinned references listed, and the account shows the `sha_pinning_required` setting's observed value or *not observable*. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
