# git-serious — Intent and via negativa — drift against the intended shape

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*Did the configuration change while the intention did not?*

Every scanner applies static rules to find bad configuration; none establishes what the system is *for* first. The inversion: derive the intended shape of a pipeline, express it as the set of things that must be able to happen, and treat everything else as removable. The detection that falls out needs no rule author to have anticipated the attack: if the configuration changed and the intention did not, something is wrong. DCOM — design, config, operation — is the mechanism; design is the layer that gives via negativa something to subtract from, and it is the least-built part of the system (day-one audit, §V).

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **friends** milestone (git-serious-tap epic #2).

## Prior Art

Impressions register items 10, 11 and 26, with the *DCOM* and *four that are strategy* sections (`tap/docs/misc/doc-products-git-serious-impressions-register.md`); the day-one audit §IV–V ([`doc-git-serious-standing-at-day-one.md`](../docs/doc-git-serious-standing-at-day-one.md)). Depends on `dcom_core` (named, placed, unbuilt) and the coordinate semantics in tap#194 — false drift is existential, not incidental.

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-intent-via-negativa | [Intent and via negativa — drift against the intended shape](#intent-and-via-negativa--drift-against-the-intended-shape) | Proposed | Innovation (register disposition CANON unless noted); falsifier field is the MVP entry gate |

### Intent and via negativa — drift against the intended shape
----
RID: `req-git-serious-intent-via-negativa`
Status: `Proposed`
Feature: `innovation`
Milestone: `friends`

The instance holds a design layer — the intended shape of the account's pipelines — alongside the configuration and operation layers, and reports where configuration departs from design and where operation departs from configuration.

**Falsifier (MVP entry gate, tap#211):** "Intent can be derived from observation" is an untested assumption (day-one audit §V). Falsifier: if intent must always be hand-declared for the drift signal to be usable, the differentiator narrows from *we hold intent* to *we hold history and a real graph*; and if the first closed loop (declared → expressed → evaluated → evidence) fires on every comparison because of coordinate noise, the subtraction engine is worse than a rule engine.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-intent-via-negativa-1 | Drift Without A Rule | Proposed | After a design is declared for a repository, a change to that repository's workflow permissions that no rule anticipates is reported as drift against the design, naming the layer pair that disagrees. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
