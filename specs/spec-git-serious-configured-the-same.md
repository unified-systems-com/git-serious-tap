# git-serious — Are they all configured the same

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*Set the rules once, everywhere, and tell me when one drifts.*

Repository and organisation settings declared in a file, applied across the estate, with a report of the difference between declared and actual. Settings live in per-repository web forms: no diff, no history, no review. The honest limit: these tools are *appliers* — they know the declared and the actual settings and nothing else, and `safe-settings`' dry-run is the closest thing in the field to drift detection, for settings only.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **friends** milestone (git-serious-tap epic #2).

## Prior Art

Overlay survey, feature **08 · Are they all configured the same** — [`doc-git-serious-overlay-consensus.md`](../docs/doc-git-serious-overlay-consensus.md) (§The nine; the coverage matrix places it by category). Built by four named incumbents, listed there. Axis: **operations** — this is a legibility feature first, not a security feature (register item 12, *more than security*).

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-configured-the-same | [Are they all configured the same](#are-they-all-configured-the-same) | Proposed | Table-stakes (built by 4 named incumbents; overlay survey #08) |

### Are they all configured the same
----
RID: `req-git-serious-configured-the-same`

Status: `Proposed`
Feature: `table-stakes`
Milestone: `friends`

The instance reports, per repository, where its rulesets, required checks, permissions defaults and security features differ from the account's declared or majority configuration.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-configured-the-same-1 | Outliers Named | Proposed | For an account where one repository lacks a required check the others share, the instance names that repository and the missing check, from collected ruleset rows. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
