# git-serious — Branch-protection tiers

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*What actually protects the default branch of each repository?*

Which rulesets and branch-protection rules govern each default branch, what they require, and who may bypass them. Scorecard grades this; we must at least show it. Two traps the incumbents fall into: the classic branch-protection API does not know about rulesets and reports a ruleset-protected branch as unprotected, and `bypass_actors` needs write access to read — so a blank must render as *not observable*, never as *nobody*.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **self** milestone (git-serious-tap epic #1).

## Prior Art

CI/CD security prior art — [`doc-git-serious-cicd-security-prior-art.md`](../docs/doc-git-serious-cicd-security-prior-art.md), §6 *Implications for git-serious* item 9 (*where it is table stakes*), with the observable-conditions tables in §3.10 and the ranked v0 list in item 7. Axis: **security**. The incumbents named there do this better than we will; the requirement is that it exist on the graph, beside the operations features, not that it win.

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-branch-protection-tiers | [Branch-protection tiers](#branch-protection-tiers) | Proposed | Table-stakes, security axis (prior art §6 item 9: must exist, will not win) |
| req-git-serious-branch-protection-tiers-bypass-badge | [The bypass badge — four colours, one alarm](#the-bypass-badge-four-colours-one-alarm) | Proposed | Improvement — read-only progress without crying wolf (decided 2026-09-02; git-serious-tap issue filed, make-it-work) |

### Branch-protection tiers
----
RID: `req-git-serious-branch-protection-tiers`
Status: `Proposed`
Feature: `table-stakes`
Milestone: `self`

For every repository, the instance shows the rulesets governing its default branch, the rules each enforces, the required checks, and the bypass list in its observability states: observed (a list, possibly empty), counted (a number, identities redacted), or not observable with the credential held (github_core `req-github-core-rulesets-bypass-2`).

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-branch-protection-tiers-1 | Three States On Bypass | Proposed | A ruleset whose bypass list the credential could not read renders as *not observable*, distinguishably from an empty list, and a repository governed only by rulesets is never reported as unprotected. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---

### The bypass badge — four colours, one alarm
----
RID: `req-git-serious-branch-protection-tiers-bypass-badge`
Status: `Proposed`
Feature: `improvement`
Milestone: `self`

The improvement to the table-stakes feature above. A read-only credential learns *how many* actors may bypass a ruleset, never *who* (github_core: GraphQL's `bypassActors.totalCount` with redacted nodes → `bypass_observability = counted`). The instance must let an operator make progress on that credential, flag that exemptions exist, and never alarm on a configuration that is ordinarily legitimate — release bots and admins hold bypass on purpose.

- **Capability:** each ruleset on the graph carries one status badge whose colour is its bypass state — **grey** `unobservable` (nothing readable with this credential), **yellow** `counted` with the true count (identities not observable; the info window names the credential that would show them, from the collector's `absent_note`), **neutral** `observed` with the names in the info window (an empty list is a fact), and **red reserved for a bypass that happened** — a rule suite with `result: bypass` (github_core rule suites), never for "someone could".
- **Incumbent's specific limitation:** incumbents either need an admin credential to say anything about bypass, or say nothing and render the gate as intact; none distinguishes "we could not look" from "nobody", and none separates capability from event.
- **Mechanism (why ours differs):** the count and state are fields on the ruleset node (no count node — a number is not a type), the badge population is a search over those fields, and the event badge reads the rule-suite edges — all queries over data already on the grid, no special case.
- **Five-minute verification:** boot with the read-only App; open the projection; every ruleset shows grey or yellow, none green; click a yellow badge and read which credential would name the actors. *(observed against our own organisation once github_core #22 item 1 lands; until then every ruleset is grey and the verification is the grey state alone.)*

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-branch-protection-tiers-bypass-badge-1 | Counted Renders Yellow With The Count | Proposed | On an instance whose credential can only count, a ruleset with N ≥ 1 bypass actors renders a yellow badge showing N, and its info window names the credential that would show the identities. | Done-test; observed on a running instance. Depends on github_core `req-github-core-rulesets-bypass-2`. |
| req-git-serious-branch-protection-tiers-bypass-badge-2 | Never Green On Unobservable | Proposed | No ruleset with `bypass_observability = unobservable` renders in the neutral or empty style; it renders grey. | The failure guarded against: "we could not look" read as "nobody can bypass". |
| req-git-serious-branch-protection-tiers-bypass-badge-3 | Red Means It Happened | Proposed | A ruleset renders red only when a rule suite with `result: bypass` targets it in the collected window; a ruleset with bypass actors but no bypass event never renders red. | Capability is configuration; the event is the finding. |
