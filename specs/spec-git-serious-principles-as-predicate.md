# git-serious — Principles as predicate — executable operational principles

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*Is our pipeline what we say it is, and can a machine keep checking?*

Teams should define the operational principles their CI/CD executes under, and those principles should be executable — each a statement plus an edge to the Search that evaluates it — so validations *emerge from* the principles, applicable to design, config and operation alike. TAP already runs this discipline on itself (requirements, acceptance criteria, implementation claims, guards, traceability); this turns it outward. Ours are drafted: seven principles, four of them observable from the graph today.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **self** milestone (git-serious-tap epic #1).

## Prior Art

Impressions register items 13, 24 and 30, the *Principles as predicate* section and *Operational principles — ours* (`tap/docs/misc/doc-products-git-serious-impressions-register.md`); the shape-of-a-pipeline Part seven ([`doc-git-serious-shape-of-a-pipeline.md`](../docs/doc-git-serious-shape-of-a-pipeline.md)). Placement decided 2026-08-27: the vocabulary lives in the `dcom_core` substrate plugin, not core; git-serious is its first consumer.

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-principles-as-predicate | [Principles as predicate — executable operational principles](#principles-as-predicate--executable-operational-principles) | Proposed | Innovation (register disposition CANON unless noted); falsifier field is the MVP entry gate |

### Principles as predicate — executable operational principles
----
RID: `req-git-serious-principles-as-predicate`
Status: `Proposed`
Feature: `innovation`
Milestone: `self`

A principle is a first-class object with a statement, an executable expression (a Search), an honest status (declared → expressible → expressed → evaluated), and evaluation records against configuration and operation; the product ships a default set and the operator authors their own, and neither may masquerade as the other.

**Falsifier (MVP entry gate, tap#211):** The loop has never closed once (day-one audit §V). Falsifier: if no drafted principle can be expressed as a Search without a bespoke module per principle, "principles emerge into validations" collapses into "we wrote seven checks".

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-principles-as-predicate-1 | One Loop Closed | Proposed | At least one of the seven drafted principles (e.g. *pin what executes*) goes end to end on a running instance: declared, expressed as a Search, evaluated against the observed account, with evidence recorded — and its status renders as *evaluated* only then. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
