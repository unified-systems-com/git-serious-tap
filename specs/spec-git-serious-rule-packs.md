# git-serious — Rule packs — shareable, publishable checks

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*Can a team publish the checks it wrote, and can I run someone else's?*

YARA turned private detection knowledge into a commons; nothing equivalent exists for CI/CD configuration. Packs carry transferable knowledge; intent carries local truth; a system with only packs is exactly what the intent critique targets, so keep both. The door already exists: the module search is a named, versioned, reviewable artifact on the grid that can hold arbitrary logic — a better substrate than a rule DSL, obtained without designing one.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **everyone** milestone (git-serious-tap epic #3).

## Prior Art

Impressions register items 4 and 29 with the *Rule packs* and *The module search* sections (`tap/docs/misc/doc-products-git-serious-impressions-register.md`); prior art §6 item 6 (rule sets to port). Constraint already written down: module registration is break-glass (`req-grid-search-canonical-read`), and third-party modules make its logged opt-in mandatory.

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-rule-packs | [Rule packs — shareable, publishable checks](#rule-packs--shareable-publishable-checks) | Proposed | Innovation (register disposition CANON unless noted); falsifier field is the MVP entry gate |

### Rule packs — shareable, publishable checks
----
RID: `req-git-serious-rule-packs`
Status: `Proposed`
Feature: `innovation`
Milestone: `everyone`

A pack of checks — expressed as Searches and modules — can be authored, published as a plugin, installed on another instance, and evaluated there against that instance's graph, with each finding recording the pack and check it came from.

**Falsifier (MVP entry gate, tap#211):** *(unfilled — required before this innovation may enter the MVP, tap#211; a proposal that cannot say what would falsify it is a hunch)*

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-rule-packs-1 | Foreign Pack Evaluated | Proposed | A pack authored on one instance and installed on another evaluates against the second instance's account and attributes each finding to the pack; module-backed checks pass through the break-glass logging `req-grid-search-canonical-read-5` asks for. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
