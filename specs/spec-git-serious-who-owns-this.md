# git-serious — Who owns this

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*Who do I ask about this repository?*

A catalog of components with an owner, a team, a description and links. Past five repositories "who do I ask" costs real minutes; past twenty it is a tax on every cross-team question, and it decays invisibly. The founding feature of the developer-portal category, and its big honest limit: in every portal the catalog is *declared* — a human writes `catalog-info.yaml` — and declared metadata rots on contact with reality with no way to know it has.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **friends** milestone (git-serious-tap epic #2).

## Prior Art

Overlay survey, feature **06 · Who owns this** — [`doc-git-serious-overlay-consensus.md`](../docs/doc-git-serious-overlay-consensus.md) (§The nine; the coverage matrix places it by category). Built by five named incumbents, listed there. Axis: **operations** — this is a legibility feature first, not a security feature (register item 12, *more than security*).

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-who-owns-this | [Who owns this](#who-owns-this) | Proposed | Table-stakes (built by 5 named incumbents; overlay survey #06) |
| req-git-serious-who-owns-this-collected-ownership | [Collected, not declared, so it cannot rot](#collected-not-declared-so-it-cannot-rot) | Proposed | Improvement — the switching argument (tap#211 sketch); four fields, verification unfilled |

### Who owns this
----
RID: `req-git-serious-who-owns-this`
Status: `Proposed`
Feature: `table-stakes`
Milestone: `friends`

For any repository, the instance answers "who owns this" from what the forge itself records — CODEOWNERS, admin and maintain grants, recent authorship — and shows the evidence for each answer.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-who-owns-this-1 | Ownership With Evidence | Proposed | For a repository with a CODEOWNERS file and at least one admin grant, the instance names the owners and, for each, the collected fact that makes them an owner. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
### Collected, not declared, so it cannot rot
----
RID: `req-git-serious-who-owns-this-collected-ownership`
Status: `Proposed`
Feature: `improvement`
Milestone: `friends`

The improvement to the table-stakes feature above — the switching argument. Four fields, all
required (tap#206); a claim that needs special-case work rather than falling out of the
architecture is a feature commitment wearing an improvement's clothes.

- **Capability:** Ownership is derived from observed facts (CODEOWNERS, permission grants, commit authorship) rather than asserted in a YAML file, and a CODEOWNERS rule naming an account that has lost access is surfaced as a broken rule.
- **Incumbent's specific limitation:** Every portal's catalog is declared by a human and the portal has no way to know it has rotted; a CODEOWNERS rule that silently stopped matching turns nothing red.
- **Mechanism (why ours differs):** The grid holds the grants, the file and the people as nodes with edges; ownership is a query over them, and the *rule names a departed account* case is a dangling edge — observable without a rule author anticipating it.
- **Five-minute verification:** *(unfilled — the tap#211 improvements pass fills this; a claim a prospect cannot check in five minutes is not a selling point)*

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-who-owns-this-collected-ownership-1 | Verifiable In Five Minutes | Proposed | A user with a running instance can confirm the capability against their own organisation inside five minutes, following the verification above. | Unfillable until the field above is filled. |

---
