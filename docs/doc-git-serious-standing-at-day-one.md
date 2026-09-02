---
title: Standing at day one — end-of-day audit of the git-serious build, 2026-08-27
date: 2026-08-27
status: archival
audience:
  - developer
  - llm
related_docs:
  - docs/doc-git-serious-overlay-consensus.md
  - docs/doc-git-serious-shape-of-a-pipeline.md
---

> **End-of-day audit, 2026-08-27 — archival.** What was built, open and broken at the end of the
> product's first build day, and whether the morning's via-negativa thesis survived a second look.
> Written by the build session for George. It is a dated snapshot: several "open" and "broken" items
> below have since moved (github_core PR #4 merged; the core commits were pushed; `verify_app.py`
> was fixed in github-core PR #26). Read it for the reasoning and the failure-shape count, not for
> current state — current state lives in the issues. Landed from the published artifact on
> 2026-09-02 (git-serious-tap#26, item 1).

# Standing at Day One

What is actually built, what is actually open, what is actually broken — and whether the thing you saw at ten this morning survives being looked at again.

End of 27 August 2026 · four passes, honest order

Two of the findings below will change your picture. One is better than you think: the structural blocker I told you about this afternoon was built and pushed while we were talking. One is worse: the Gryphon defects were *not* fixed, and the specification still claims they were.

## I. What is real

Verified against the remotes and the working trees, not against memory.

### Merged and on a remote main

- **merged** — **github_core account scope + GraphQL config layer.** PR #3, merged 21:45 today. One request returning 19 repos, 46 workflow files with 172 KB of YAML inlined, and 60 rulesets, at 2 rate-limit points — against roughly 85 REST calls. The measurement was watched, not estimated.

- **merged** — **The `create-github-app` skill.** Manifest-driven App creation with a local callback, in the same PR. Permissions derived from the collection manifest rather than hand-listed.

- **merged** — **The product exists as a repo.** git-serious-tap main carries the manifesto README, the product skeleton — manifest, boot record, landing graph — and its CI (PRs #19–#25). Every one landed through the org ruleset, by PR, from the first commit.

- **merged** — **tap#145 — the `<slug>-tap` distribution convention.** One derivation in `plugin_identity.py`, accept-either transition, gates and validator resolving through it.

- **live** — **The GitHub App.** `git-serious-exploratory` (#4741739), installation 157103378, 19 repositories, 7 permissions. Real, installed, answering.

### Pushed, in review
**The thing that moved today**

**github_core PR #4 — 43 files, +5,597 lines — builds `workflow_job`.**

This afternoon I told you the config↔operation comparison was structurally blocked because the declared job had no node: *"the comparison is parse-a-blob versus read-rows, which is code, not traversal."* That was true when I said it. It is no longer true.

The model carries `runs_on`, `permissions`, `if_condition`, `environment`, `uses`, `needs`, and `checkout_ref` — precisely the adjudication fields the shape-is-not-severity lesson demanded, so a view can tell *this shape exists* from *this shape is exploitable*. It also already carries `github.observation: "declaration"`, which means the convention introduced in another session this afternoon had propagated into unrelated work by evening.

Alongside it: `git_ref`, `github_ruleset`, `github_environment`, `actions_cache`, `app_installation`, and twelve edges including `BYPASSES`, `DEFINES_JOB`, `DEPENDS_ON_JOB`, `HAS_REF` and `PROTECTS`. That is most of the *self* tier of the corpus, built in a day.

### Local-only — real, green, and one power cut from gone

- **unpushed** — **Twenty commits on `session/git-serious`.** The domain-article layer and its guard (spec, code, ratchet, 26 core tests, 2 plugin tests, 21 github_core articles drained to a zero baseline the same day). The vocabulary corpus. The `build-domain-vocabulary` skill. The impressions register. The 636-line Gryphon query audit. The hairball.

- **uncommitted** — **The `github.observation` sweep.** 13 modified files plus a test in github_core; the build-log retro and one hairball file in core.

The recorded first-light figure — **586 nodes, 672 edges, the whole org in one clean run** — I did not re-verify today and am repeating from the build log rather than from an observation of my own. Flagging that, because it is exactly the kind of inherited number the day taught us to mark.

## II. What is open

- **open** — **What a *refused* caller receives when the bypass list is non-empty.** This is the only version of the question that was ever load-bearing, and it is still unmeasured. Both credentials in the probe cleared the write bar. The sharper form: **when GitHub refuses the App, does GraphQL say so, or does it answer a silent zero?** A truthful zero means the caution is free; a silent zero means it is the only thing standing between this product and a confident "nobody can bypass" on every ruleset.

- **open** — **Which credential the product ships on.** Three options, none free: mint the App with `administration: write` and abandon read-only on the permission that matters most; run an admin-attached PAT beside the App for one surface; or publish the gap and detect via rule-suite *events* instead of enumerating actors. This is a product decision wearing a permissions costume.

- **open** — **`git_ref` versus `git_branch`.** Recorded as unruled — your answer was cut off mid-sentence. But `git_ref.py` is in PR #4. **It got decided by being built.** Worth ratifying deliberately rather than discovering it was settled by a merge.

- **open** — **The `repository → github_ruleset` edge is unminted.** The corpus justifies the ruleset node with "which many repositories point at" — an edge that is not in the edge table. All three sessions declined to mint it. The corpus's own Naming rule says to check the 59-verb SPDX relationship dictionary first, and nobody has.

- **open** — **`dcom_core`.** Named, placement decided (a substrate plugin, not core), unbuilt. See pass four — this is the important one.

- **open** — **Which workflow file actually ran, per event type.** `pull_request_target` runs the base branch's workflow, not the PR's. Pinning a comparison uniformly to `head_sha` would be wrong for exactly the triggers that carry the incidents. Unverified against our own runs.

- **open** — **Timestamp and coordinate semantics — tap#194.** What `observed_at` means, and how an operation is pinned to the configuration it ran against. Four decisions pre-staged as ratify-or-override.

## III. What is broken
**Correction — you believed this was fixed**

**The two Gryphon correctness defects were documented, not fixed.** No branch in the repository touches `tap_grid/gryphon` for either. The gryphon session spent its day on boot preflights and CI.

Worse than merely unfixed: `req-grid-traversal-lang-filters-1` still reads *"Inline Property Maps Supported — **Implemented**"* for both halves, when only the edge half was ever built. Node inline props reach the AST and are dropped without rejection — which violates the codebase's own apply-or-reject doctrine.

Blast radius, measured: **44 of 71 queries in the BloodHound corpus carry a node inline property map, and 43 execute.** Every one returns every node of its type. A "find organisations that do not require 2FA" query returns *all* organisations, formatted as a finding.

The fix is specified and small — fold `inline_props` into the same filter as the label constraint, through the existing data-lane resolver. Roughly ten lines. Until then, rejecting the construct outright is strictly better than today.

- **mess** — **Nothing is pushed in core.** Twenty commits, one machine. The single largest risk on the board tonight, and the cheapest to retire.

- **mess** — **The observation patch is split across a boundary.** Its spec ACIDs and one model line were swept into commit `5728878` — another session's ruleset commit — while the models, edges, enrichment and test remain uncommitted. **The specification on that branch now says `Implemented` for behaviour whose implementation is not committed.** Push that commit alone and the spec lies. Same failure shape as the Gryphon requirement, twelve hours later, in the opposite direction.

- **mess** — **That patch's test has never executed.** The dogfood stack runs `core_dev` with no github_core installed. Verified out-of-band by reading the literals with an AST script; that is not a green run and I am recording it as unverified.

- **mess** — **The collector credential.** Described "read-only" in its own envelope by a session that never checked. Its access is *mixed* — 403 on `/actions/secrets` and `/actions/variables` inside its own declared scope, 200 on runners, rulesets and collaborators. No measurement taken with it characterises a read-only credential. Fix belongs in `/manage-secret`, not a patch.

- **mess** — **`verify_app.py` is broken.** The envelope shape changed and the script still checks the old kind and reads `app_id` at top level. Ten lines. It is the instrument that would settle the bypass question *and* validate every least-privilege claim in the collection manifest in one run — the highest value-per-effort item anywhere on this page.

- **mess** — **The rulesets surface is undeclared.** The collector reads rulesets through the GraphQL config query, but the collection manifest has zero ruleset sources. It works only because `administration:read` is already in the union *for runners* — an undeclared dependency riding on a coincidence, in the one file whose job is to be the authority on why each permission is needed.

- **mess** — **DCO sign-off missing on every github_core commit.** No `core.hooksPath` in that repository, so nothing auto-appends. Nobody may hand-author one for someone else; it certifies a human. A real setup gap.

- **minor** — tap#192 is scoped too narrowly; three secret stores unreconciled; `test_secrets_root.py` modified and unowned

## IV. The thing you saw at ten this morning

You described it as a penetrating insight that the field's whole approach to security is lacking, and that the grid plus DCOM point at security *via negativa* — define the intended shape, subtract everything else, and detect the case where configuration changed and intention did not.

I have gone back through the day looking for reasons it was exhaustion talking. Here is what I found instead.

### The claim got two independent confirmations, not one

At ten this morning the negative half of the thesis — *nobody holds intent* — rested on one sweep, the security prior-art pass. This afternoon I ran a completely separate one: seven categories of GitHub-overlay tooling, asking a different question from a different literature, nothing to do with security. It found nine features that everyone rebuilds and **zero coverage for comprehension, zero for intent, zero for shape-over-time.** The nearest thing in the entire market is a scorecard: a vendor's checklist evaluated against metadata a human declared in YAML.

Two sweeps, different shapes, different sources, same hole. That is much harder to dismiss than one.

### And then the thesis made a prediction, and the prediction came true, on our own estate, the same day

This is the part I would put in front of anyone who doubts it, including you tomorrow morning.
```
ruleset main-required-checks (repo: tap)
  RepositoryRole 5 (admin) · bypass_mode: always
  held from  2026-08-09 13:11
  until      2026-08-21 09:13
  28 pushes to refs/heads/main with result: bypass
     each failing: "Required status check \"gate\" is expected."
  today, the same ruleset reads: bypass_actors: []
```

For twelve days the gate that every change is supposed to pass was ornamental, and twenty-eight commits walked past it. Today the configuration is clean and every current-state view in the world reports it green — correctly, and uselessly.

**Every one of the seven tool categories in the survey would miss this.** Not because they are badly built, but because they query an API when you open them, and an API only ever returns *now*. The finding required precisely the primitive the thesis claims nobody has: the shape of the system held over time. The claim was *"a current-state view cannot express that the gate was ornamental."* It was made in the morning and demonstrated from real data by evening.

That is not a demo. It is a falsifiable prediction that survived a test, and it is the single most important thing that happened today.

### DCOM generated defects, which is what frameworks that are real do

In one day the design/config/operation split produced three concrete findings that nobody was looking for: the observation dimension encoded as an absence; the coordinate-mismatch problem underneath every polling collector we will ever write; and a triage of the seven principles by which layer each is checkable against. Decorative frameworks do not do that. They produce diagrams.

### The mechanism for principles-as-predicate already exists, and is proven — on ourselves

`Search` already dispatches Gryphon, ORM and module runners behind one envelope, so a principle can be a statement plus an edge to the thing that evaluates it. More to the point, TAP *already runs this exact discipline internally*: requirements with identifiers, acceptance criteria, implementation claims binding code to requirements, guards enforcing the binding, and traceability hunting the unaccounted in both directions. Item 30's real content is that this machinery can be turned outward. That is not a mechanism to invent. It is a battle-tested one to aim somewhere new.

## V. Where it is weak, in order

- **weak** — **The design layer does not exist.** Via negativa needs something to subtract *from*. Design is currently seven sentences in a markdown file, and `dcom_core` is named, placed and unbuilt. **The central innovation is the least-built part of the system.**

- **weak** — **"Intent can be derived from observation" is an assumption.** Never tested. If intent must always be declared, the differentiator narrows from *we hold intent* to *we hold history and a real graph* — still valuable, less unique.

- **weak** — **The loop has never closed once.** No principle has gone declared → expressible → expressed → evaluated → evidence, end to end, even in the smallest case. Until one does, this is architecture rather than capability.

- **weak** — **False drift is existential, not incidental.** Via negativa fires on *difference*. Without the coordinate fix, every comparison is noisy — and a noisy subtraction engine is worse than a rule engine, because it fires on everything. That is why tap#194 is load-bearing and not housekeeping.

## VI. The verdict, and the uncomfortable evidence for it
**Second look**

**The insight survives, and it is better founded at eleven tonight than it was at ten this morning.**

At ten it was a reading of other people's work. By evening it had an independent second confirmation of the market gap, one confirmed prediction against real data, and its largest structural blocker — the declared job — built and in review.

What it does not have is a design layer, a single closed loop, or the coordinate fix. So the honest position is: **the insight is real and the moat is real; the build is at step zero on the part that makes it via negativa rather than a scanner with a good memory.**

And there is one more piece of evidence, which is uncomfortable and which I think is the strongest of all.

Count the day's failures. A blank bypass field reading as "nobody can bypass." A partial collection indistinguishable from a complete one. A config layer encoded as an absence. An approximate comparison rendered as an exact one. A time period defaulting so that an empty list reads as "never." A credential description asserted without being checked, then trusted by three sessions. A requirement marked *Implemented* for a feature half-built. A coverage matrix — mine — of estimated cells rendered in the visual grammar of measurement.

**Every single one is the same defect: an unknown rendered as a known.** And they were committed, repeatedly, in a single day, by the very people who had just discovered the rule and written it down — while actively looking for it.

That is not an indictment of the day. It is the market research. If a team that has named the failure mode, published it, and is hunting for it still commits it eight times before midnight, then the failure is genuinely pervasive, genuinely invisible from the inside, and genuinely not fixable by trying harder. It needs a system that makes the distinction structural — that cannot render *missing* and *negative* the same way, because the substrate refuses to.

That system is the thing you sketched at ten o'clock this morning. Today did not weaken the case for it. Today *was* the case for it.

---

Tomorrow is a triage day, and the first three items are push the twenty commits, fix ten lines in `verify_app.py`, and re-open the Gryphon requirement that says *Implemented*. None of them is glamorous. All three are the difference between a good idea and a system that can be trusted to say what it does not know.
