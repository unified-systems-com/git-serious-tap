# git-serious — Past the event horizon — collectors on the third parties themselves

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*What does the bot, the app, the cloud account actually have — not what the forge says it granted?*

Every commercial tool stops at the boundary of the forge because its model of the world stops there. We can write a collector against the third party itself — the OIDC trust policy in the cloud account, the package registry's publisher config — and pull its configuration onto the same graph. Their perimeter is our ingest. Second collectors, in incident order: cloud-side OIDC trust (AWS first, reusing `aws_core`), then registries, then a second forge.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **everyone** milestone (git-serious-tap epic #3).

## Prior Art

Impressions register item 7.2 and the *Past the event horizon* section (`tap/docs/misc/doc-products-git-serious-impressions-register.md`); prior art §6 item 14 ([`doc-git-serious-cicd-security-prior-art.md`](../docs/doc-git-serious-cicd-security-prior-art.md)). The AWS side already federates this way (shape-of-a-pipeline, Part three).

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-past-the-event-horizon | [Past the event horizon — collectors on the third parties themselves](#past-the-event-horizon-collectors-on-the-third-parties-themselves) | Proposed | Innovation (register disposition CANON unless noted); falsifier field is the MVP entry gate |

### Past the event horizon — collectors on the third parties themselves
----
RID: `req-git-serious-past-the-event-horizon`
Status: `Proposed`
Feature: `innovation`
Milestone: `everyone`

At least one third-party system a pipeline publishes to or authenticates against is collected by its own collector and joined to the forge graph — so a workflow's OIDC claim and the cloud trust policy that accepts it are one path.

**Falsifier (MVP entry gate, tap#211):** *(unfilled — required before this innovation may enter the MVP, tap#211; a proposal that cannot say what would falsify it is a hunch)*

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-past-the-event-horizon-1 | Cross-System Path | Proposed | For a workflow that assumes an AWS role via OIDC, the instance shows the workflow, its `id-token` grant, the role's trust policy conditions, and whether the policy's subject pattern is narrower or broader than the workflow's actual claims. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
