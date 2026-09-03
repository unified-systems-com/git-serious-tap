# git-serious — What changed — the shape of the system over time

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*What changed since last week, and did anybody mean it?*

Every tool in the field shows the system as it is *now* or a metric aggregated over time; none keeps the *shape itself* over time, because they query an API when opened and the API only returns now. The tenth feature. Keeping the shape requires holding a model rather than a cache, which is what the grid is. Evidence already in hand (*observed*, 2026-08-27): the `main-required-checks` ruleset on `tap` carried an admin bypass for twelve days and twenty-eight commits walked past the gate; every current-state view reports that ruleset green today, correctly and uselessly.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **self** milestone (git-serious-tap epic #1).

## Prior Art

Overlay survey — the tenth feature ([`doc-git-serious-overlay-consensus.md`](../docs/doc-git-serious-overlay-consensus.md), §The tenth feature does not exist); prior art §6 items 2 and 8 (change-over-time is the differentiator, snapshot-derived); impressions register items 5 and 16 (`tap/docs/misc/doc-products-git-serious-impressions-register.md`); the day-one audit's confirmed prediction ([`doc-git-serious-standing-at-day-one.md`](../docs/doc-git-serious-standing-at-day-one.md), §IV).

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-what-changed | [What changed — the shape of the system over time](#what-changed--the-shape-of-the-system-over-time) | Proposed | Innovation (register disposition CANON unless noted); falsifier field is the MVP entry gate |

### What changed — the shape of the system over time
----
RID: `req-git-serious-what-changed`

Status: `Proposed`
Feature: `innovation`
Milestone: `self`

The instance answers, for any object on the graph and for the account as a whole, what changed between two observations — configuration and relationships, not only results — as the default view rather than an add-on.

**Falsifier (MVP entry gate, tap#211):** Partly tested already: the thesis predicted that a current-state view cannot express an ornamental gate, and the 2026-08-27 ruleset history demonstrated the case from real data (*observed*). Remaining falsifier: if, on a friends' organisation, a month of observations yields no change a user acts on, the differentiator is a demo rather than a product — that is the test the friends milestone runs.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-what-changed-1 | Ornamental Gate Found | Proposed | Given collected observations spanning a period in which a ruleset's bypass list was non-empty and is now empty, the instance shows the change, its duration, and the pushes that bypassed during it. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
