# git-serious — Secret-in-code detection

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*Did a credential land in a repository?*

GitHub secret scanning and kingfisher own this; the table-stakes move is to ingest the alerts the platform already raises onto the graph, attached to the repository, so they sit beside everything else rather than in one more tab.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **everyone** milestone (git-serious-tap epic #3).

## Prior Art

CI/CD security prior art — [`doc-git-serious-cicd-security-prior-art.md`](../docs/doc-git-serious-cicd-security-prior-art.md), §6 *Recommendations* item 9 (*where it is table stakes*), with the observable-conditions tables in §3.10 and the ranked v0 list in item 7. Axis: **security**. The incumbents named there do this better than we will; the requirement is that it exist on the graph, beside the operations features, not that it win.

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-secret-in-code-detection | [Secret-in-code detection](#secret-in-code-detection) | Proposed | Table-stakes, security axis (prior art §6 item 9: must exist, will not win) |

### Secret-in-code detection
----
RID: `req-git-serious-secret-in-code-detection`
Status: `Proposed`
Feature: `table-stakes`
Milestone: `everyone`

The instance ingests the forge's secret-scanning alerts for each repository as typed findings, with alert state and the repository they concern, and reports repositories where secret scanning is not enabled or not observable.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-secret-in-code-detection-1 | Alerts And Coverage | Proposed | A repository with an open secret-scanning alert carries a finding naming it; a repository where the feature is disabled, or where the credential cannot read alerts, is shown as such rather than as clean. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
