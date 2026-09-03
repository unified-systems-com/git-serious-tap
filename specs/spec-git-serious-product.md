# git-serious — Product Specification

> **Skeleton, 2026-09-02.** The product spec tap#206 says every product has, instantiated for
> git-serious in the convergence git-serious-tap#26 planned. Sections marked **unwritten** are the
> tap#211 spike's output (improvements → innovations → MVP) and the tap#210 gap pass; they are named
> here so their absence is visible rather than implied complete.

## Purpose

> **CI/CD configuration is impossible to see all at once — and getting it wrong is catastrophic.**
> **Visualize, track, and secure your CI/CD system — for humans and agents.**

The problem line and the promise line, settled 2026-08-26 (build log, *decision — the two lines*;
`tap/docs/misc/doc-products-git-serious-build-log.md`). Building, maintaining and securing a modern
CI/CD system is complicated, and the complexity is the bad kind: it is not in one place. Workflow
files, rulesets, environments, org settings, the apps and bots wired into the repos, the third-party
services they talk to, the tokens. No single screen shows all of it, so nobody actually knows what it
is — on the most critical of critical paths, the one that ships the software.

The README (repo root) is the manifesto; this spec is the engineering record behind it. The README's
five promises each map to a feature below: pull the system onto the grid (the collectors, owned by
`github_core`), present the pages (the table-stakes features), track change over time (*what
changed*), agent-driven review (*agent-operable review*), read-only access (*a credential that shows
its own permissions*).

**Positioning (register item 12, *more than security*).** The security framing is how the space is
legible today; the durable version is a shared picture that platform teams and security teams both
operate from. The operations features are first-class, not a means to a findings list. The product
is self-contained — no Rampart, product-line or initiative language (the Iron Man 1 rule,
`plan/product-map.md`).

## Goals

|   |   |   |
| :---: | --- | --- |
| 1. | One Representation | Every feature is a query over one model that holds configuration, operation and the relationships between them, with history. None of the nine table-stakes features is built as a feature; a feature that is awkward to derive is evidence the model is wrong. |
| 2. | Three States, Never Two | A missing fact and a negative fact never render the same way: none / some / *not observable with this credential*, in every view, dimension and report. |
| 3. | Legible To The Third Player | The graph, the findings and the collectors' permission needs are machine-legible from day one; an agent can review what a human can, read-only. |
| 4. | Honest About The Bar | Table-stakes features must exist and will not win; improvements state what a prospect can verify in five minutes; innovations state what would falsify them before they enter the MVP. |

## How to read the feature specs

One spec per capability, `specs/spec-git-serious-<slug>.md`. Each carries the existing spec/req
machinery — a `RID:` block, `Status:`, acceptance criteria — plus two marker lines read by the corpus
parser once tap#288 lands (inert prose until then):

```
Feature: `table-stakes` | `improvement` | `innovation`     — the tier
Milestone: `self` | `friends` | `everyone`                 — the product step targeted (epics #1, #2, #3)
```

- **Table-stakes** features are what every incumbent builds; each cites its source and the count of
  incumbents that build it. Two axes: **operations** (the overlay survey's nine) and **security**
  (the prior-art survey's five). A product that only has the second axis is a scanner.
- **Improvements** are child requirements *inside* their table-stakes spec: the switching argument,
  with four required fields — capability, the incumbent's specific limitation, the mechanism, and a
  five-minute verification. Five are sketched (tap#211); the verification field is unfilled on all
  five, and an unfilled field is shown as unfilled.
- **Innovations** are their own specs. Each carries a **falsifier**; a proposal that cannot say what
  would falsify it is a hunch, and hunches do not enter the MVP.
- **Built-ness is the requirement's status**, not a new field: `Proposed`/`Backlog` = not built,
  `In Development` = partial, `Implemented`/`Verified` = built, riding the core evidence gate. A
  status flips only when the done-test ACID is *observed* on a running instance.
- **Milestone targets are a draft mapping** written 2026-09-02 for review; the MVP trim rules on them.
- **Provenance markers** (tap#206): every claim is *documented* (from a cited source), *observed*
  (measured on a running system), or *inferred*. Skeleton claims are documented unless marked.

The README's feature table is **derived** from these specs by the generator tap#288 specifies, never
hand-maintained (presence is not correctness). Until the generator runs in this repo (blocked on
tap#286), the table below is the hand-written stand-in and says so.

## Prior art

Prior art is a *folder*: [`docs/`](../docs/README.md) — eight dated research passes plus the three
landed 2026-09-02. The key findings this spec stands on:

- **The overlay consensus** (`doc-git-serious-overlay-consensus.md`): seven tool categories rebuild
  the same nine features; they cluster into three questions and nothing crosses a cluster; all ten
  are downstream of one representation; the tenth — the shape of the system over time — exists
  nowhere in the market. *The coverage matrix is estimated, not measured.*
- **The security prior art** (`doc-git-serious-cicd-security-prior-art.md`, §6): model the
  conjunction, not the setting; change-over-time is the differentiator and must be snapshot-derived;
  a read-only App that shows its own permissions; consume zizmor/poutine/Scorecard rather than
  rebuild them; five table-stakes observables; the lanes GitHub will eat within twelve months.
- **The shape of a pipeline** (`doc-git-serious-shape-of-a-pipeline.md`): the five nouns, the trust
  boundary, the gate chain, and seven operational principles — four observable from the graph today.
- **The impressions register** (`tap/docs/misc/doc-products-git-serious-impressions-register.md`):
  thirty observations with dispositions; the four that are strategy (intent, via negativa, rule
  packs, past the event horizon); DCOM; principles as predicate; the module search.
- **The day-one audit** (`doc-git-serious-standing-at-day-one.md`): the thesis's confirmed prediction
  (a twelve-day ornamental gate) and the count of *unknown rendered as known* failures committed in
  one day by people hunting for them — the market research in one number.

## Features

Hand-written stand-in for the generated table (see *How to read* above). Status is the requirement's
declared status; none is built yet. Sources: **O** = overlay survey feature number; **S** = security
prior art §6 item; **R** = impressions register item; **A** = day-one audit section.

### Table-stakes — operations axis

| Feature | Spec | Milestone | Status | Source | Incumbents |
| --- | --- | :---: | :---: | --- | ---: |
| The status wall | [spec-git-serious-status-wall.md](spec-git-serious-status-wall.md) | self | Proposed | O-01 | 6 |
| Reliability history | [spec-git-serious-reliability-history.md](spec-git-serious-reliability-history.md) | friends | Proposed | O-02 | 6 |
| Time and money | [spec-git-serious-time-and-money.md](spec-git-serious-time-and-money.md) | friends | Proposed | O-03 | 5 |
| What is waiting on me | [spec-git-serious-waiting-on-me.md](spec-git-serious-waiting-on-me.md) | everyone | Proposed | O-04 | 5 |
| Why isn't this merging | [spec-git-serious-why-not-merging.md](spec-git-serious-why-not-merging.md) | self | Proposed | O-05 | 5 |
| Who owns this | [spec-git-serious-who-owns-this.md](spec-git-serious-who-owns-this.md) | friends | Proposed | O-06 | 5 |
| Does this meet our bar | [spec-git-serious-meets-our-bar.md](spec-git-serious-meets-our-bar.md) | self | Proposed | O-07 | 5 |
| Are they all configured the same | [spec-git-serious-configured-the-same.md](spec-git-serious-configured-the-same.md) | friends | Proposed | O-08 | 4 |
| Tell me when it breaks | [spec-git-serious-tell-me-when-it-breaks.md](spec-git-serious-tell-me-when-it-breaks.md) | friends | Proposed | O-09 | all |

### Table-stakes — security axis

| Feature | Spec | Milestone | Status | Source |
| --- | --- | :---: | :---: | --- |
| Per-workflow lint findings | [spec-git-serious-workflow-lint-findings.md](spec-git-serious-workflow-lint-findings.md) | self | Proposed | S-9, S-5 |
| Pin drift | [spec-git-serious-pin-drift.md](spec-git-serious-pin-drift.md) | friends | Proposed | S-9 |
| SHA-pinning status | [spec-git-serious-sha-pinning-status.md](spec-git-serious-sha-pinning-status.md) | self | Proposed | S-9, S-7 |
| Branch-protection tiers | [spec-git-serious-branch-protection-tiers.md](spec-git-serious-branch-protection-tiers.md) | self | Proposed | S-9, S-7 |
| Secret-in-code detection | [spec-git-serious-secret-in-code-detection.md](spec-git-serious-secret-in-code-detection.md) | everyone | Proposed | S-9 |

### Improvements (child requirements of the table-stakes spec named)

| Improvement | In spec | Milestone | Status | Verification |
| --- | --- | :---: | :---: | --- |
| Criticality sort and the not-observable state | status-wall | self | Proposed | unfilled |
| When it became flaky, not that it is | reliability-history | friends | Proposed | unfilled |
| The ruleset → check → workflow chain | why-not-merging | self | Proposed | unfilled |
| Collected, not declared, so it cannot rot | who-owns-this | friends | Proposed | unfilled |
| Principles with executable expressions, evaluated against config and operation | meets-our-bar | self | Proposed | unfilled |

The other four table-stakes operations features (time and money, waiting on me, configured the same,
tell me when it breaks) and the five security features have **no improvement sketched**. That is a
recorded absence, not an oversight: the tap#211 improvements pass asks of each "does the grid,
history or DCOM change it?", and *no* is an acceptable answer.

### Innovations register

| Innovation | Spec | Milestone | Status | Source | Falsifier |
| --- | --- | :---: | :---: | --- | --- |
| What changed — the shape of the system over time | [spec-git-serious-what-changed.md](spec-git-serious-what-changed.md) | self | Proposed | O-10, S-2, S-8, R-5, R-16, A-IV | stated (partly tested) |
| Conjunction findings across object types | [spec-git-serious-conjunction-findings.md](spec-git-serious-conjunction-findings.md) | self | Proposed | S-1, S-8 | stated |
| Intent and via negativa — drift against the intended shape | [spec-git-serious-intent-via-negativa.md](spec-git-serious-intent-via-negativa.md) | friends | Proposed | R-10, R-11, R-26, A-V | stated |
| Principles as predicate | [spec-git-serious-principles-as-predicate.md](spec-git-serious-principles-as-predicate.md) | self | Proposed | R-13, R-24, R-30 | stated |
| Rule packs | [spec-git-serious-rule-packs.md](spec-git-serious-rule-packs.md) | everyone | Proposed | R-4, R-29, S-6 | unfilled |
| Past the event horizon — collectors on the third parties | [spec-git-serious-past-the-event-horizon.md](spec-git-serious-past-the-event-horizon.md) | everyone | Proposed | R-7.2, S-14 | unfilled |
| A credential that shows its own permissions | [spec-git-serious-self-describing-credential.md](spec-git-serious-self-describing-credential.md) | friends | Proposed | S-3, S-8, A-VI | unfilled |
| Agent-operable review | [spec-git-serious-agent-operable-review.md](spec-git-serious-agent-operable-review.md) | everyone | Proposed | S-11 | unfilled |
| git-serious-incidents | [spec-git-serious-incidents-pack.md](spec-git-serious-incidents-pack.md) | everyone | Proposed | R-17, R-25 | unfilled |

Register items deliberately **not** carried as git-serious features, with where they live instead:
supply chain and SBOM (R-8, R-22 — product-map entries, `supply_chain_core`); defined dimensions
(R-27 — a `build-domain-vocabulary` skill change); GraphQL transport (R-28 — landed in github_core);
OCSF proposal (R-21 — after a second forge); the plugin hitlist (R-19 — ecosystem, not product);
"model the world, then learn from the model" (R-25's general form — a TAP-wide method).

## Gaps

**Unwritten — tap#210.** The gap list must be re-derived against current reality, not carried from
2026-08-27: github_core PR #4 built most of the *self* tier, `feat/gate-view` holds the first gate
view, and github-core PRs #19 and #27 are open. Split core versus plugins; every gap cites the
requirement IDs it serves and is filed as a sub-issue of the feature issue.

Known before the pass runs: the shipped boot record could not boot against the shared host store —
github_core v0.4.0 and kind `github_pat` versus the combined `github` App envelope (*observed*
2026-09-02, git-serious-tap#33; closed 2026-09-03 by pinning github_core v0.5.0 and declaring kind
`github`); and product-repo specs are outside the core traceability ratchet (tap#286).

## MVP

**Unwritten — tap#211.** The aggressive trim against why we are doing this, who the initial users
are, and what they care about most; arrives at something we are the right amount of embarrassed by.
Names what is in, what is explicitly deferred, the follow-on targets, and the **first target date**,
and moves the *self* milestone's date deliberately (it passed 2026-08-30). An innovation enters only
with its falsifier stated.
