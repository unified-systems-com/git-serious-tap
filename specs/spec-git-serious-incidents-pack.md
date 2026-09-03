# git-serious — git-serious-incidents — historical compromises as grid representations

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*What would this tool have shown the day before the incident?*

A batch pack of modelled historical incidents someone can investigate and view: the 35-incident corpus and the observable-conditions tables are most of the raw material. It is the demo, the teaching artifact, and the regression suite for the vocabulary at once — and the instance of a TAP-wide method, *model the world, then learn from the model*.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **everyone** milestone (git-serious-tap epic #3).

## Prior Art

Impressions register items 17 and 25 (`tap/docs/misc/doc-products-git-serious-impressions-register.md`); `doc-git-serious-vocab-from-incidents.md` and the incident table in prior art §4 ([`doc-git-serious-cicd-security-prior-art.md`](../docs/doc-git-serious-cicd-security-prior-art.md)).

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-incidents-pack | [git-serious-incidents — historical compromises as grid representations](#git-serious-incidents--historical-compromises-as-grid-representations) | Proposed | Innovation (register disposition CANON unless noted); falsifier field is the MVP entry gate |

### git-serious-incidents — historical compromises as grid representations
----
RID: `req-git-serious-incidents-pack`

Status: `Proposed`
Feature: `innovation`
Milestone: `everyone`

A GRIFT pack reconstructs a set of documented CI/CD compromises as graph representations in the product vocabulary, each annotated with the precondition the incident required, so that the product's own findings can be run against them.

**Falsifier (MVP entry gate, tap#211):** *(unfilled — required before this innovation may enter the MVP, tap#211; a proposal that cannot say what would falsify it is a hunch)*

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-incidents-pack-1 | Precondition Found In The Pack | Proposed | For at least five packed incidents, running the conjunction and drift findings against the pack surfaces the documented precondition of each, and the pack is installable on any instance as seed data. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
