---
title: The overlay consensus — the nine features every GitHub-overlay tool rebuilds, and the tenth none of them has
date: 2026-08-27
status: research
audience:
  - developer
  - llm
related_docs:
  - docs/doc-git-serious-shape-of-a-pipeline.md
  - docs/doc-git-serious-cicd-security-prior-art.md
---

> **Prior-art survey, 2026-08-27.** Seven categories of GitHub-overlay tooling (browser skins, run
> boards, CI observability, engineering intelligence, developer portals, config-as-code, merge queues)
> surveyed for the features they all rebuild. Written by an AI research agent from public sources.
> The coverage matrix is **estimated**, not measured — the cells are the agent's reading of each
> category's products, rendered in the visual grammar of a measurement (the day-one audit calls this
> out on itself). Nothing here is canon — requirements live in specs, the fence lives in the roadmap.
> Landed from the published artifact on 2026-09-02 (git-serious-tap#26, item 1); this file is the
> record the specs cite.

# The Overlay Consensus

Seven categories of tool exist to make GitHub bearable. Strip away the branding and they build the same nine things — plus one they all leave out.

Prior-art survey · 27 August 2026 · companion to *The Shape of a Pipeline*

Nobody has been suffering through the GitHub interface quietly. There are browser extensions with tens of thousands of installs, a half-dozen independently-written open-source dashboards that are almost the same program, four venture-funded developer-portal companies, and a whole product category devoted to the question of what order pull requests should merge in. The market is not empty. It is crowded and oddly shaped.

What follows is the consensus feature set — the things that keep getting rebuilt, stated as the question *you* are actually asking when you want one. If several unrelated teams independently build the same thing, that thing is a real need, and it is worth understanding the need on its own terms before deciding whether to serve it.

## The nine
### 01 · The status wall

*“Is anything broken right now?”*

One live table of every workflow run across every repository, newest first, red and green. This is the single most-rebuilt artifact in the entire space — at least five separate open-source projects are essentially this program, and every commercial observability product opens on a version of it.

**Why you want it:** GitHub scopes everything to one repository. Your Actions tab shows you one repo's runs, so with nineteen repositories the honest answer to “is anything broken” costs nineteen tab-opens, and nobody does that, which means the real answer is “I don't know, and I find out when someone complains.” The wall converts a survey into a glance.

**The honest limit:** it tells you a thing is red. It cannot tell you whether that matters, and after a week of looking at a wall with two permanent reds on it you stop looking at the wall.

**Built by** gha-dash · GH-Watch · github-action-dashboard · Snorlx · Datadog CI Visibility · every portal's Actions plugin

### 02 · Reliability history

*“Should I trust this red?”*

The last twenty runs of one job, as a strip. Pass rate, flake rate, which tests fail intermittently. Sold variously as flaky-test detection, test analytics, or a reliability score.

**Why you want it:** this is the most expensive question in daily CI use, and a single run cannot answer it. A red that has been red for three weeks means something completely different from a red that appeared with your commit — one is a broken pipeline you have learned to ignore, the other is your bug. Without history you re-run the job to find out, which costs ten minutes and often lies. The strip answers in a glance what a re-run answers slowly and unreliably.

**The honest limit:** it is per-job. It says *this test is flaky*, never *this test became flaky the day we changed the runner image*, because it holds no history of anything except results.

**Built by** Datadog CI Visibility · Trunk · BuildPulse · the late Foresight · Snorlx repository scoring · merge queues, as a selling point

### 03 · Time and money

*“Where are my ten minutes going, and why is the bill that?”*

Duration per job, trend over time, minutes consumed, cost attributed per workflow and per repository.

**Why you want it:** CI duration is a tax levied on every single change, paid by every person, forever — so a lane that quietly grew from two minutes to nine is one of the highest-leverage things you can find, and it is invisible without a trend line because each individual run felt fine. The money half becomes real the moment you use larger runners or a self-hosted fleet.

**The honest limit:** it optimises what exists. It never asks whether the slow lane needed to run at all, because it has no idea what any lane is for.

**Built by** Datadog · Trunk · Snorlx · CircleCI Insights · every engineering-intelligence platform

### 04 · What is waiting on me

*“What actually needs my attention today?”*

One queue of pull requests and issues that need *you* — assigned, review-requested, mentioned — across every repository, with the noise removed.

**Why you want it:** GitHub's notification system reports events, and you do not want events; you want obligations. The two look similar and behave nothing alike — a thread stays unread after you have dealt with it, and a review request you have already handled sits in the list exactly like one you have not. Most people's coping strategy is to declare notification bankruptcy and rely on someone tapping them on the shoulder, which works until the team has more than one timezone.

**The honest limit:** pure triage. It moves work in front of you and knows nothing about the work.

**Built by** gh-dash · Octobox · gh-dashboard · Graphite · Refined GitHub, in fragments

### 05 · Why isn't this merging

*“It's approved and green. What is it waiting for?”*

A per-pull-request account of what stands between here and merged: required checks outstanding, reviews missing, branch behind, conflict, queue position.

**Why you want it:** a stalled pull request is a genuinely confusing object. GitHub's merge box tells you *that* you cannot merge and is often vague about *why* — particularly the case where a required check will never report because nothing is configured to produce it, which presents as waiting rather than as broken. The gap between “blocked” and “blocked on a thing that will never happen” is where hours go.

**The honest limit:** the merge-queue products own this and answer it in terms of queue mechanics. They can tell you check `gate` is missing; they cannot tell you which workflow was supposed to produce it.

**Built by** Mergify · Graphite · Trunk · Aviator · GitHub's own merge queue

### 06 · Who owns this

*“Who do I ask about this repository?”*

A catalog of software components with an owner, a team, a description, and links to the things attached to it — docs, dashboards, on-call rota, dependencies.

**Why you want it:** past roughly five repositories, “who do I ask” starts costing real minutes, and past twenty it becomes a routine tax on every cross-team question. It also decays invisibly: ownership was accurate the day it was written and then two people left. This is the founding feature of the entire developer-portal category, which is the single best-funded corner of this market.

**The honest limit — and it is a big one:** in every portal, this catalog is *declared*. A human writes a `catalog-info.yaml` and asserts the facts. Declared metadata rots on contact with reality, and the portal has no way to know that it has.

**Built by** Backstage · Cortex · OpsLevel · Port · Roadie

### 07 · Does this meet our bar

*“Which of my repositories are below the line, and on what?”*

A scorecard: a list of standards a repository is supposed to meet — has an owner, has CI, has a required check, has a security policy, pins its actions — scored across the estate so the laggards sort to the top.

**Why you want it:** consistency across repositories decays silently and in one direction. Repo fourteen was created in a hurry and never got the gate; nothing was ever going to tell you, because nothing failed. Every check in a scorecard is something you already believe — the value is entirely in *asking it of all nineteen at once, repeatedly*, which is the part humans reliably do not do.

**The honest limit:** the checks are a fixed list written by the vendor, or by you in the vendor's little language. They encode known-good patterns, so they can only ever find the problems somebody already anticipated.

**Built by** Cortex scorecards · OpsLevel maturity · Allstar · OpenSSF Scorecard · Snorlx repository scoring

### 08 · Are they all configured the same

*“Set the rules once, everywhere, and tell me when one drifts.”*

Repository and organisation settings declared in a file, applied across the estate, with a report of the difference between what is declared and what is actually there.

**Why you want it:** GitHub settings live in per-repository web forms. Nineteen repositories is nineteen forms, no diff, no history, no review, and any administrator can change one at three in the morning with no record that anyone will ever read. Declaring them in a file makes settings behave like code — reviewed, versioned, and identical by construction rather than by everybody remembering.

**The honest limit:** these tools are *appliers*. They know the settings you declared and the settings that exist, and nothing else — not your workflows, not your runs. GitHub's own `safe-settings` has a dry-run mode that posts the delta on a pull request, which is the closest thing in this entire survey to drift detection, and it covers settings only.

**Built by** safe-settings · Allstar · Peribolos · the Terraform GitHub provider

### 09 · Tell me when it breaks

*“Don't make me watch a dashboard.”*

A message in chat when main goes red, when a nightly fails, when a deploy finishes, when a scorecard slips.

**Why you want it:** every dashboard above has the same defect, which is that you have to go and look at it. The alert inverts that. It is also the feature most likely to be quietly switched off, because the ratio of messages to actions you take is the whole ballgame, and most tools ship it tuned far too loud.

**The honest limit:** alerts fire on *results*, because results are the only thing these tools model. Nothing here can alert you that your gate configuration changed, only that a run went red afterwards.

**Built by** effectively everything, in some form

## Who covers what

Laid out as a matrix, the shape of the market is visible in about four seconds — and it is not the shape you would expect from a crowded space.

| Feature | Browser skins | Run boards | CI observ. | Eng. intel. | Dev portals | Config as code | Merge queues |
|---|---|---|---|---|---|---|---|
| **Is it healthy right now?** |  |  |  |  |  |  |  |
| 01 · The status wall | ○ | ● | ● | ○ | ○ | · | ○ |
| 02 · Reliability history | · | ○ | ● | ○ | · | · | ● |
| 03 · Time and money | · | ○ | ● | ● | · | · | ○ |
| 09 · Tell me when it breaks | · | ● | ● | ○ | ○ | ○ | ● |
| **What is mine to do?** |  |  |  |  |  |  |  |
| 04 · What is waiting on me | ● | · | · | ○ | ○ | · | ○ |
| 05 · Why isn't this merging | ○ | · | · | ○ | · | · | ● |
| **Is it built the way we said?** |  |  |  |  |  |  |  |
| 06 · Who owns this | · | · | · | ○ | ● | ○ | · |
| 07 · Does this meet our bar | · | ○ | · | ○ | ● | ● | · |
| 08 · Configured the same | · | · | · | · | ○ | ● | · |
| 10 · What changed *(the tenth feature)* | · | · | · | · | · | ○ | · |

Legend: **●** core to the category · **○** partial or peripheral · **·** absent

## What the shape means

Three things fall out of that grid, and the third is the one worth acting on.

### The nine cluster into three questions, and nothing crosses a cluster

Features one, two, three and nine answer *is it healthy right now*. Four and five answer *what is mine to do*. Six, seven and eight answer *is it built the way we said it would be*. Every category in the survey sits squarely inside one cluster and has, at best, a token presence in the others.

That is not a coincidence and it is not laziness. The market has segmented by **audience** — developers get skins and inboxes, platform teams get dashboards and portals, managers get metrics, security gets scanners — and each vendor built precisely the data model their one audience's questions required, then stopped. A run-history model cannot answer an ownership question no matter how much money you throw at it, so nobody tries.

### The consequence is that your system has no single representation

Each role in an organisation holds a different partial map, drawn in a different tool, and no two of them can be laid over one another. When the developer, the platform engineer and the security reviewer disagree about what the pipeline does, there is no shared artifact to settle it — which is precisely why those conversations take an afternoon and end in someone opening the YAML on a shared screen. The absence of a common picture is felt as a communication problem and is actually a modelling one.

### The tenth feature does not exist, and it is the interesting one
**The vacancy**

Every tool in this survey shows you the system as it is *now*, or a metric aggregated *over* time. Not one of them keeps the *shape itself* over time.

So no tool in the field can answer: *what changed since last week, and did anybody mean it?*

The closest thing that exists is `safe-settings`' dry-run report — a genuine drift detector, limited to repository settings, comparing against a file you wrote rather than against yesterday. Everything else is a snapshot. GitHub's own answer to “what changed” is the audit log, which is an Enterprise feature, is a flat event stream rather than a model, and expires.

That vacancy is not an oversight anybody has been lazy about. It is structural: these tools query an API when you open them, and the API only ever returns *now*. Keeping the shape over time requires holding a model of the system rather than a cache of an API response, and holding a model is a different kind of product from the ones in this survey.

### All ten are downstream of one representation

Here is the part that changes what we build rather than merely confirming it. Every feature in the grid is a question about the same three things — the configuration as written, the runs as they happened, and the relationships between them. Given a model that holds all three and keeps its history, none of the nine is a feature to be designed; each is a query to be written.

Which suggests a straightforward rule for our own build. **Do not build any of the nine as a feature.** Build the representation, then derive them — and treat any of the nine that turns out to be awkward to derive as evidence that the model is wrong, rather than as an argument for a special case. The status wall in particular is table stakes: it has been written five times in public, it earns us nothing, and its absence would be the first thing anyone noticed. It should cost us a page and a query.

The tenth is where a reason to switch actually lives.
