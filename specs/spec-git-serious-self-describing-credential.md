# git-serious — A credential that shows its own permissions

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*What can this instance see, what can it not, and how would I know?*

A read-only GitHub App with the minimum permissions its collection manifest declares, rendered as the first row of the inventory it builds — and the two things read-only cannot see (ruleset bypass actors without write; OAuth apps at all) named on the page rather than implied complete. A missing fact and a negative fact must never render the same way: three states, none / some / not observable. The day-one audit counted eight instances of *an unknown rendered as a known* committed in one day by people hunting for it; the substrate has to refuse the conflation.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **friends** milestone (git-serious-tap epic #2).

## Prior Art

Prior art §6 items 3 and 8 (*granted vs used*, CICD-SEC-2/-8) ([`doc-git-serious-cicd-security-prior-art.md`](../docs/doc-git-serious-cicd-security-prior-art.md)); the day-one audit §VI ([`doc-git-serious-standing-at-day-one.md`](../docs/doc-git-serious-standing-at-day-one.md)); the README's fifth promise (*down-scoped, read-only access*). The credential the product ships on is undecided (git-serious-tap#24, register item 15) and gates the friends milestone.

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-self-describing-credential | [A credential that shows its own permissions](#a-credential-that-shows-its-own-permissions) | Proposed | Innovation (register disposition CANON unless noted); falsifier field is the MVP entry gate |

### A credential that shows its own permissions
----
RID: `req-git-serious-self-describing-credential`

Status: `Proposed`
Feature: `innovation`
Milestone: `friends`

The instance renders its own credential — kind, permissions granted, permissions used per source, and the surfaces it could not observe — as a first-class object in the inventory, and every view derives its *not observable* state from that record rather than from an empty response.

**Falsifier (MVP entry gate, tap#211):** *(unfilled — required before this innovation may enter the MVP, tap#211; a proposal that cannot say what would falsify it is a hunch)*

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-self-describing-credential-1 | Granted, Used, Not Observable | Proposed | The inventory's first row is the instance's own credential with granted versus used permissions per collection source, and a view over a surface the credential cannot read renders *not observable* with a link to the permission that would unlock it. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
