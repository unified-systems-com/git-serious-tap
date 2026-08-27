---
title: The field's practitioner signal network — researchers, tools, feeds
date: 2026-08-27
status: research
audience:
  - developer
  - llm
related_docs:
  - docs/doc-git-serious-cicd-shape-review.md
  - docs/doc-git-serious-cicd-security-prior-art.md
---

> **Research pass, 2026-08-27.** The people and projects producing attack research, tooling and incident disclosure, each with a verified feed URL, cadence and follow tier.
> One of four gathering passes behind the domain vocabulary corpus, which lives with the
> vocabulary's owner as `spec-github-core-vocabulary.md`. Written by an AI research agent;
> claims carry citations and the report flags what it could not verify. Not canon.

# The CI/CD Security Field: People, Institutions, and Signal Sources

**A standing signal network for git-serious**
Compiled 2026-08-27. All verification timestamps in this document are that date unless stated otherwise.

---

## How to read this, and how much to trust it

This is a map of the *field* git-serious operates in — who produces new knowledge about CI/CD and software-supply-chain security, and where that knowledge appears before it becomes common knowledge. It deliberately does **not** review vendor products; a sibling pass covered ~23 commercial tools. Where a company appears here it is because of the people and research it emits.

**Verification method.** The session's WebSearch budget was exhausted early, which turned out to be a blessing: essentially everything below was verified by **direct primary-source fetch** rather than by search-result summary —
- project `MAINTAINERS` / `OWNERS` / `GOVERNANCE` / `tags.yaml` files read through the authenticated GitHub API;
- the GitHub Users API `company` and `bio` fields, which the person sets themselves;
- the person's own website;
- **live feed retrievals with the HTTP status and entry count actually checked.**

Every feed marked ✅ was fetched and returned real content. Feeds marked ⚠️ returned 200 but were empty, or were blocked. Anything we could not confirm is marked **UNVERIFIED** and left in place rather than dropped — a named gap is more useful than a confident guess.

**Three findings that shape everything else:**

1. **Governance files systematically lie about affiliation.** Sigstore's TSC roster, in-toto's `MAINTAINERS.txt`, TUF's `MAINTAINERS.md` and SLSA's retired-maintainer table all disagree with the individuals' own profiles. Where they conflict, trust the person's self-set `company` field — it is the more recently updated of the two. (§2.0)

2. **Two "obvious" feeds are silently broken or wrong.** `securitylab.github.com/feed.xml` returns valid Atom with **zero entries** — anyone subscribed has been receiving nothing. `slsa-framework/slsa` has **zero GitHub Releases**, so its `releases.atom` will never fire; use `tags.atom`. Both are the kind of failure a naive poller reports as "healthy."

3. **The canonical taxonomy is stale and the living one is a linter.** The OWASP Top 10 CI/CD Security Risks is still v1.0, **October 2022**, with no update in progress. Meanwhile `zizmor` ships **41 audit rules** covering the 2023-2026 attack wave. Buyers speak OWASP; the field speaks zizmor. git-serious should be fluent in both. (§4.7, §1)

---
## 1. Individual security researchers — the CI/CD attack canon

These are the people who found *classes* of bug, not instances.

> ### The best single artifact in this entire map
> **`zizmor`'s audit documentation is the field's de facto annotated bibliography.** Every audit rule cites the primary research that defined its vulnerability class, with a working URL, maintained by an active project so it stays current.
> ```
> https://raw.githubusercontent.com/zizmorcore/zizmor/main/docs/audits.md
> ```
> ✅ Verified: 87 link-reference definitions; grepping out the internal test-data links leaves ~30 canonical external citations. Extract with `grep -oE '^\[[^]]+\]: https?://[^ ]+'`. It yields, among others: Lobačevski's pwn-request series (Parts 1, 2, 4), Adnan Khan's two cache-poisoning posts, Unit 42's ArtiPACKED and tj-actions analyses, Legit Security's environment-injection pair, Chainguard's impostor-commits, Synacktiv's exploitation series (environment manipulation, Dependabot), elttam's "Hacking with Environment Variables", Trail of Bits' Trusted Publishing benchmark, the Nix ecosystem disclosure, and the Trusted Publishing docs for **every major registry** (PyPI, RubyGems, crates.io, npm, NuGet, pub.dev).
>
> Companion: **`woodruffw/gha-hazmat`** — a deliberately-vulnerable workflow menagerie that serves as the field's ground-truth corpus. **This is the obvious test fixture for git-serious's own detection.**

### 1.1 Adnan Khan — the most prolific individual in GitHub Actions attack research

- **Affiliation: deliberately undisclosed, and we are honouring that.** His About page says he works as a Security Engineer for a large company and **explicitly asks not to be associated with his employer when citing his blog.** He was at **Praetorian** for the founding work. Do not assert a current employer.
- **Why he matters — this is most of the modern canon:**
  - **Self-hosted runner takeover.** Original author of **`gato`** (Praetorian, ShmooCon 2023, with **Mason Davis** and **Matt Jackoski**), and co-author of the origin document *"From Self-Hosted GitHub Runner to Self-Hosted Backdoor"* (2022-10-26): non-ephemeral self-hosted runners are persistently compromisable by untrusted workflow code, and the logging needed to see it sits behind GitHub's most expensive Enterprise tier.
  - **Cache poisoning — he named and then weaponised the class.** *"The Monsters in Your Build Cache — GitHub Actions Cache Poisoning"* (2024-05-06) named it; **Cacheract** (2024-12-21) shipped the weaponised implementation; *"Turning Almost Nothing into a Supply Chain Compromise of Angular…"* (2026-03-03) proved it end-to-end against a tier-1 OSS project. This is now `zizmor`'s `cache-poisoning` audit.
  - **Runner-image poisoning.** *"One Supply Chain Attack to Rule Them All — Poisoning GitHub's Runner Images"* (Dec 2023).
  - **Real-world compromises:** TensorFlow via self-hosted runner (with Stawinski, Jan 2024); RoguePuppet (Puppet Forge, 2024-07); Release-Drafter → `google/accompanist` (2024-11); Safe{Wallet} frontend (2025-02); CVE-2023-49291.
  - **Cross-platform:** *"Who's SHA is it Anyway: Bypassing Google Cloud Build Comment Control for $30,000"* (2025-07-21) — the class is not GitHub-specific.
  - **Race conditions in CI plumbing:** *"Watch your Dispatch: Race Condition in Dependabot Core CI"* (2025-05-02).
  - **The AI-agents-in-CI frontier — he got there first.** *"Copilot or Coconspirator: Tricking GitHub Copilot and Stealing all Your Secrets"* (2026-01-07) and *"Clinejection — Compromising Cline's Production Releases just by Prompting an Issue Triager"* (2026-02-09).
- **Tooling:** **`gato-x`** (`github.com/AdnaneKhan/gato-x`, 581★, v1.4.0 Apr 2026, last push 2026-07-20) — an independently maintained successor to `gato`. If we run one offensive tool against our own Actions estate, it is this one.
- **Follow:** ✅ **RSS `https://adnanthekhan.com/rss.xml`** (verified 200, `application/xml`) · GitHub `@AdnaneKhan` · X `@adnanthekhan` · releases `https://github.com/AdnaneKhan/gato-x/releases.atom`
- **Cadence:** ~4-6 deep posts/year, each typically naming a class. Tooling commits continuous.
- **Tier:** `core` — **rank 1.**

### 1.2 John Stawinski IV — affiliation **UNVERIFIED** (was Praetorian; none stated on his site)

- **Why he matters:** With Adnan Khan, executed the **PyTorch supply-chain compromise** (*"Playing with Fire"*, Jan 2024) and the TensorFlow one — the demonstrations that turned self-hosted-runner takeover from theory into headline. Solo-authored **CodeQLEAKED** (2025-03-26): a secret valid for **1.022 seconds** that could have backdoored GitHub CodeQL itself. Also ByteDance Rspack pwn requests (with **Adam Crosser**), a Node.js Jenkins agent hijack (*"Agent of Chaos"*), and a Microsoft perimeter breach that started from a typo fix.
- **He has pivoted hard into AI-agent CI/CD**, which is where the next wave is: RCE in Anthropic's Claude Code Action via PR-title prompt injection (Feb 2026); repo-jacking Claude Community Plugins (Jun 2026); TOCTOU→prompt-injection in OpenAI Codex Cloud Code Review (Jul 2026).
- **Talks:** Black Hat USA 2024 *"Self-Hosted GitHub Runners: Continuous Integration, Continuous Destruction"*; DEF CON 32 *"Grand Theft Actions: Abusing Self-Hosted GitHub Runners at Scale"* — `https://johnstawinski.com/talks/`
- **Follow:** ✅ **RSS `https://johnstawinski.com/feed/`** (verified 200, `application/rss+xml`). ⚠️ Note the site root returned **403** to one of our fetchers while the feed served fine — **poll the feed, not the page.**
- **Cadence:** ~3-5 posts/year, high depth.
- **Tier:** `core` — **rank 2.**

### 1.3 William Woodruff — `zizmor`, and the packaging-standards bridge

- **Affiliation: OpenAI, on the Astral team, working on `uv`'s security features.** ✅ Verified from his own words (Python Packaging Council candidacy statement, 2026-08-13); GitHub `company` reads `@astral-sh @openai`. **Previously Trail of Bits.** He is also standing for the inaugural **Python Packaging Council**.
- **Why he matters — `zizmor` is the living taxonomy of this field.** Moved from `woodruffw/zizmor` to its own org **`zizmorcore/zizmor`** (6,399★, pushed 2026-08-27), now covering **GitHub Actions, Dependabot, and pre-commit**. It implements **41 audit rules**, and the rule names are a better map of the 2023-2026 attack surface than any published taxonomy:

  `artipacked` · `cache-poisoning` · `template-injection` · `dangerous-triggers` · `impostor-commit` · `ref-confusion` · `ref-version-mismatch` · `typosquat-uses` · `unpinned-uses` · `stale-action-refs` · `known-vulnerable-actions` · `archived-uses` · `forbidden-uses` · `excessive-permissions` · `undocumented-permissions` · `overprovisioned-secrets` · `secrets-inherit` · `secrets-outside-env` · `unredacted-secrets` · `github-env` · `github-app` · `bot-conditions` · `self-hosted-runner` · `self-repository` · `insecure-commands` · `insecure-url-scheme` · `hardcoded-container-credentials` · `unpinned-images` · `unpinned-tools` · `adhoc-packages` · `superfluous-actions` · `obfuscation` · `misfeature` · `anonymous-definition` · `concurrency-limits` · `dependabot-cooldown` · `dependabot-execution` · `use-trusted-publishing` · `unsound-condition` · `unsound-contains` · `unsound-ternary`

  **For git-serious this rule list is the single most useful coverage checklist in the field, and it is four years fresher than OWASP's.** Note `artipacked` is named directly after Yaron Avital's research and `github-env` after Legit Security's and Synacktiv's — the tool is where research becomes enforcement.
- **He also built:** `pip-audit`, **PyPI Trusted Publishing**, **PEP 740** (attestations), and `gha-hazmat`.
- **Recent writing, directly on-topic:** ***"GitHub Actions needs OIDC audience constraints"* (2026-08-10)** · ***"You shouldn't trust Trusted Publishing"* (2026-07-07)** — the argument that Trusted Publishing is an *authentication* mechanism, not a trust signal. That distinction is one git-serious will need to make to customers, and it pairs directly with Boost's Red Hat npm finding (§1.4).
- **Follow:** ✅ **Atom `https://blog.yossarian.net/feed.xml`** · Mastodon **`@yossarian@yossarian.net`** (no X, deliberately) · GitHub `@woodruffw` · docs `https://docs.zizmor.sh/` (rules at `/audits/`) · ✅ **releases `https://github.com/zizmorcore/zizmor/releases.atom`** — every 1-2 weeks (v1.29.0 2026-08-01, v1.30.0-rc1 2026-08-13). **New rules ship in those releases; this feed is effectively a live changelog of the CI/CD attack surface.**
- **Tier:** `core` — **rank 3.**

### 1.4 Boost Security Labs — François Proulx and Sébastien Graveline

A research team producing genuinely novel CI/CD attack classes that was not in the original brief.

- **François Proulx — VP of Security Research, Boost Security** (✅ GitHub `company: Boost Security`). **Sébastien Graveline — Security Researcher**, offensive CI/CD, red-team background.
- **Why they matter:**
  - ***"Deployment Poisoning"* (2026-04-07, Graveline)** — a new class abusing the **Deployments API**. A fork PR references a **non-existent environment**; GitHub *auto-creates* it; privileged e2e-test workflows (Playwright/Cypress/Lighthouse) then consume the attacker-controlled deployment target URL, yielding command injection and secret exfiltration. Disclosed to 15+ vendors from Nov 2025; demonstrated against Argos CI, Checkly and others. **No published taxonomy covers this.**
  - ***"Sleeper Squats: How a Hyphen (Almost) Unravelled GitHub's Immutable OIDC Subject Claim"* (2026-06-11, Proulx)** — OIDC **subject-claim confusion**, found in GitHub's own claim construction rather than in a user's trust policy.
  - ***"Trusted Publishing, Untrusted Branch: Inside the Red Hat npm Compromise"* (2026-06-01)** — how Trusted Publishing fails when branch scoping is wrong.
  - *"TeamPCP Compromises LiteLLM"* (2026-03-24) and a recurring *"Supply Chain Hunting Season"* series.
  - **`poutine`** (510★, v1.1.6 2026-05-22) — a **multi-platform** build-pipeline scanner, complementing zizmor's Actions focus.
  - **Living Off The Pipeline (LOTP)** — `boostsecurityio/lotp` (161★, pushed 2026-07-31), site `https://boostsecurityio.github.io/lotp/`. Explicitly modelled on **GTFOBins and LOLBAS**: an inventory of **RCE-by-design "foot guns" in ordinary developer CLIs**, tagged by injection vector (`eval-sh`, `eval-js`, `env-var`, `config-file`, `input-file`). It is why "this innocuous linter is an RCE primitive when fed untrusted PR content" is now a *checkable claim* rather than folklore.
    > ✅ **Machine-readable: `https://boostsecurityio.github.io/lotp/api.json`** — a JSON array of `name`, `url`, `tags`, `refs`, `html`, `meta{files, sinks, purl}`, ~50+ entries. **The single most directly ingestible dataset found in this entire pass**: it maps "tool present in a pipeline" → "known code-execution sink," a join git-serious can perform directly.
- **Follow:** ✅ **RSS `https://labs.boostsecurity.io/rss.xml`** (verified — RSS 2.0, per-author bylines). ⚠️ **The old `boostsecurity.io/blog/rss.xml` 404s** and old blog URLs 301 to `labs.boostsecurity.io`; use the new host.
- **Cadence:** ~1-2 research articles/month.
- **Tier:** `core` — **rank 4.**

### 1.5 Varun Sharma and StepSecurity — the fastest incident channel

- **Varun Sharma — CEO and co-founder, StepSecurity** (✅ verified via GitHub bio + blog).
- **Why they matter:** **Harden-Runner** (1,257★) is EDR-for-Actions-runners — egress, file integrity, process monitoring — which means **they see attacks in flight rather than after the fact.** They **first detected the tj-actions/changed-files compromise** on 2025-03-14 via network anomaly detection; Varun wrote that post personally, and every subsequent analysis (Wiz, Unit 42, Aqua) cites StepSecurity as the origin report. They shipped a drop-in replacement action within hours, and later found the **reviewdog** org compromise.
  - **The tj-actions incident itself is the canonical modern CI/CD supply-chain compromise:** `tj-actions/changed-files`, **CVE-2025-30066**, ~23,000 dependent repos, began ~09:00 PT 2025-03-14. A compromised **PAT on a maintainer's bot account** was used to **retroactively repoint multiple version tags at one malicious commit**, which dumped CI/CD secrets from the Runner Worker process into build logs. **Tag mutability is the root cause** — which is why hash-pinning (`unpinned-uses`) is the highest-value single control git-serious can check, subject to Kästner's caveat in §3.4 and Lynch's in §1.9.
- **Current output** (verified Aug 2026): *"ChainDrop npm Worm: Bun-loaded CI/CD credential harvester with Ethereum dead-drop C2"* (08-16), *"Rust Supply-Chain Attack: arrayref, internment, append-only-vec Poisoned by the proc-macro1 Build-Time Dropper"* (08-22), *"The State of Open Source Supply Chain Attacks"* (08-23).
- **Follow:** ✅ **RSS `https://www.stepsecurity.io/blog/rss.xml`** · GitHub `@varunsh-coder`, org `@step-security` · X `@varunsh_coder`
- **Cadence:** **multiple posts/week** — the highest-frequency source in this map (3 posts in 4 days at time of writing).
- **Tier:** `core` — **rank 5.** Read for incidents; discount the product framing.

### 1.6 The Palo Alto Networks Unit 42 CI/CD cluster (largely ex-Cider Security)

This is where the Cider Security lineage ended up, and it is more active than the OWASP project it spawned.

- **Yaron Avital — Principal Researcher, Unit 42** (✅ verified, at PAN since 2022; still publishing 2026-08-21). Author of **ArtiPACKED** (2024-08-13), the canonical **artifact token leakage** work: `actions/checkout` persists a GitHub token to disk *by default*, `actions/upload-artifact` then publishes it when a workflow uploads a whole directory, and artifacts v4 made them downloadable mid-run — a race window in which the token is still valid. The archetype of "the default is the vulnerability." `core`
  - ⚠️ **Correction to a common belief: ArtiPACKED is Unit 42, not Aqua.** Confirmed twice (the post byline and zizmor's citation).
- **Omer Gil — Unit 42** (ex-Director of Research, Cider Security; ✅ verified via 2025 byline). Co-author of the **OWASP Top 10 CI/CD Security Risks** — he named **Poisoned Pipeline Execution (PPE)** as CICD-SEC-4. Lead byline on Unit 42's definitive **tj-actions root-cause investigation** (2025-03-20, updated 2025-04-02), which traced the chain backwards through **SpotBugs → reviewdog → tj-actions**, starting **November 2024** — months earlier than anyone had reported. `core`
- **Asi Greenholts — PAN** (Prisma Cloud / Unit 42; ex-Cider). ***"The GitHub Actions Worm: Compromising GitHub Repositories Through the Actions Dependency Tree"* (2023-09-14)** — the first systematic treatment of **transitive action-dependency compromise**, i.e. the actions dependency tree as a worm propagation medium. **This is the theoretical model that tj-actions/reviewdog later demonstrated in the wild.** `core`
- **Aviad Hahami — Unit 42.** Co-author on the tj-actions root-cause chain. `periodic`
- **Justin Moore — Unit 42.** Authored Unit 42's **Shai-Hulud** tracking (2025-11-25/26) covering **Shai-Hulud 2.0 / "The Second Coming"**: escalation from `postinstall` to **`preinstall`** execution (removing the need for human interaction and bypassing later-stage static scanners), a destructive fallback that can wipe `$HOME`, payloads `setup_bun.js` / `bun_environment.js`, and exfiltration into **~25,000 public GitHub repos across ~350 accounts**. `periodic`
- **Follow:** ✅ **RSS `https://unit42.paloaltonetworks.com/feed/`** (bylined). Per-author pages exist (`/author/yaron-avital/`, `/author/omer-gil/`, …) but **no per-author feeds** — filter the main feed on names. The feed is mostly malware/threat-intel; CI/CD is a small slice.
- **Tier:** `core` (the people), `periodic` (the feed).

### 1.7 Christophe Tafani-Dereeper — Datadog — the OIDC misconfiguration canon

- **Affiliation:** Datadog, Cloud Security Researcher and Advocate (✅ GitHub `company: @DataDog`).
- **Why he matters:** ***"No keys attached: Exploring GitHub-to-AWS keyless authentication flaws"*** (2023-07-27, last updated 2025-06-18) is **the** canonical research on **OIDC / `id-token: write` trust-policy misconfiguration.** He scanned for real IAM roles whose trust policies accepted `token.actions.githubusercontent.com` **without properly constraining the `sub` claim** — meaning *any* GitHub Actions workflow on the internet could assume them — and found live ones, including at a UK government entity. **This is the paper that made "pin your `sub` condition" standard practice.** Also drove Datadog's **GuardDog** and **Supply-Chain Firewall**.
- **Follow:** ✅ **RSS `https://securitylabs.datadoghq.com/rss/feed.xml`** · personal `https://christophetd.fr` · GitHub `@christophetd` · X `@christophetd`
- **Tier:** `core` — **rank 6.** If git-serious checks one cloud-trust thing, it is the `sub` constraint, and this is the citation.
- **Also at Datadog: Kennedy Toomey** (Application Security Researcher and Advocate) — *"The case for GitHub Actions security after recent supply chain attacks"* (2026-06-02) reports the number worth quoting: **38% of organizations have a GitHub Actions workflow vulnerable to script injection or dangerous-trigger issues**, from Datadog's 2026 State of DevSecOps telemetry. She also gives a clean three-class taxonomy of the recent wave: s1ngularity (pwn request), hackerbot-claw (untrusted input, AI-driven, RCE in >50% of targeted repos), TeamPCP (credential compromise → Trivy/KICS/LiteLLM). `periodic`

### 1.8 Jaroslav Lobačevski — GitHub Security Lab — the `pull_request_target` canon

- **Affiliation: ✅ GitHub Security Lab** — his GitHub bio reads "Security Researcher @ghsecuritylab."
  > ⚠️ **Reconciling a conflict in our own research:** a parallel pass found **no posts by him in any GitHub feed going back to December 2025** and concluded he had likely moved on. Both are true and the honest reading is: **still affiliated, not currently publishing.** Follow the work, not the byline.
- **Why he matters: he systematized the `pull_request_target` injection class.** *"Keeping your GitHub Actions and workflows secure Part 1: Preventing pwn requests"* (2021-08-03) coined and popularised **"pwn request"** and gave the CORS-analogy framing everyone still uses. Part 2 covers **untrusted input** (template/script injection); Part 3 secure building blocks. **Every later tool — zizmor, octoscan, poutine, gato-x, CodeQL's Actions queries — implements his taxonomy.** Part 1's example was still being updated as recently as 2026-06-17.
- **Follow:** the series at `https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/` · GitHub `@JarLob` · blog `https://jarlob.github.io` · X `@yarlob`
- ⚠️ **Feed trap:** `https://securitylab.github.com/feed.xml` returns **HTTP 200 and valid Atom with zero entries.** Use `https://securitylab.github.com/advisories/feed.xml` and `https://github.blog/tag/github-security-lab/feed/` instead.
- **Tier:** `core` (the work).
- **Alvaro Muñoz (`pwntester`) — current affiliation UNVERIFIED.** Authored **Part 4** of the series and led **CodeQL support for GitHub Actions workflows**, then ran those queries at scale across open source to discover new vulnerability classes **empirically rather than by hand** — the shift from anecdote to population-level CI/CD vulnerability research. GitHub `@pwntester`, X `@pwntester`. ⚠️ His personal blog `pwntester.com` is **stale since 2015**; his GitHub company field is empty. Foundational work, not a live signal. `core` (work) / `periodic` (person).

### 1.9 The rest of the canon — one finding each

| Researcher | Affiliation | The class they named | Follow |
|---|---|---|---|
| **Rami McCarthy** | **Wiz** ✅ (bylines through Aug 2026) | Runs *High Signal Security*. Unusually publishes **live incident microsites** rather than one-shot posts (a TeamPCP campaign tracker; an Axios npm compromise retro), and ships small tools against the canon: **`/imposter`**, a fork-commit detector that operationalises Billy Lynch's impostor-commit class, and `/commit-autopsy`. Latest: Rust `arrayref` attack with reported DPRK overlap (2026-08-20). | ✅ **`https://ramimac.me/feed.xml`** (note `/rss.xml` and `/index.xml` both 404) · `@ramimacisabird` · **`core`** |
| **Billy Lynch** | Chainguard, Principal SWE ✅ | ***Impostor commits*** (2023-03-08). Because GitHub shares a commit object store across a fork network, **a commit SHA that appears to belong to a trusted repo may originate from an untrusted fork** — meaning SHA-pinning, the standard mitigation, can itself be spoofed. One of very few findings that broke an assumed-safe control. **Read this before telling anyone that hash-pinning is sufficient.** | `chainguard.dev/unchained/...` · GitHub `@wlynch` · `periodic` |
| **Hugo Vincent** | **Synacktiv** ✅ | Multi-part *"GitHub Actions exploitation"* series — repo jacking, **`GITHUB_ENV` environment manipulation**, Dependabot-context abuse — demonstrated against Microsoft, FreeRDP, AutoGPT, Excalidraw, Angular, Apache, Cypress, Azure, Swagger, Firebase. Released **`octoscan`** (272★). zizmor cites him for `github-env`. | ✅ **`https://www.synacktiv.com/en/feed/lastblog.xml`** (note `/en/feed` and `/feed` both 403) · `core` |
| **Noam Dotan** | **Legit Security** ✅ | ***Artifact poisoning → `$GITHUB_ENV` injection*** (Sept 2022): a `workflow_run` workflow downloads artifacts uploaded by an untrusted `pull_request` workflow and writes their content into `GITHUB_ENV`, setting arbitrary env vars in a privileged context. With Legit's Part 1 on `workflow_run` privilege escalation (Apr 2022), this is the **origin of the artifact-poisoning class**. Found in Google and Apache. | ✅ **`https://www.legitsecurity.com/blog/rss.xml`** (heavily diluted by marketing) · `periodic` |
| **Charlie Eriksen** | **Aikido Security** ✅ | Lead analyst on the **s1ngularity / Nx** attack (Aug 2025) — a `pull_request_target` pwn request against the Nx build toolchain, notable because **the payload weaponised locally-installed AI CLI agents (Claude/Gemini) to hunt for secrets.** | ✅ `https://www.aikido.dev/blog/rss.xml` · high volume, mixed · `periodic` |
| **Praetorian offensive CI/CD team** | Praetorian | **`gato` is dead** (archived 2026-04-24) — **superseded by `Trajan`** (2026-03-06): unifies gato + glato across **GitHub Actions, GitLab CI, Azure DevOps and Jenkins**; 32 detection plugins, 24 attack plugins, compiles to WASM. Authors: AJ Hammond, Carter Ross, Evan Leleux, Mario Bartolome, Michael Weber, Nathan Sportsman, Rahul Saranjame, Ranganatha Rao Sridhar, Tanishq Rupaal. | `https://github.com/praetorian-inc/trajan` · ✅ `https://www.praetorian.com/feed/` · `core` (the tool), `periodic` (the blog — its recent content is BLE and kernel fuzzing; the Actions lineage left with the researchers) |
| **Wiz Threat Research** | Wiz | tj-actions reference explainer (**Merav Bar, Shay Berkovich, Gal Nagli**, 2025-03-15), and they **independently identified `reviewdog/action-setup` as the likely upstream compromise** — a genuinely new finding. 2026 supply-chain work by **Rami McCarthy, Benjamin Read**. | ✅ `https://www.wiz.io/blog/rss.xml` (per-item `<author>` tags) · also `https://www.wiz.io/feed/rss.xml` verified · `core` |
| **"ptrpaws" + "lexi"** (pseudonymous) | Independent | ***"Pwning the Entire Nix Ecosystem"*** (2025-09-11) — a `pull_request_target` bug in **nixpkgs** that would have allowed arbitrary code injection into effectively the whole Nix ecosystem, found and reported in about a day. Cited by zizmor. Proof the pwn-request class is **still live in 2025-26 against tier-1 ecosystems.** | `https://ptrpa.ws/nixpkgs-actions-abuse` · **no feed** · `context` |
| **RyotaK** | **GMO Flatt Security** ✅ | Registry/CI RCE across cdnjs, Homebrew, Cloudflare Pages. **His current output moved to Flatt Security Research — his personal blog is not where the work lands.** | `https://flatt.tech/research` (**no confirmed feed**) · personal `https://blog.ryotak.net/index.xml` ✅ but dormant since 2025-04 · Bluesky `@ryotak.net` · `context` |
| **Nikita Stupin** | Independent (employer UNVERIFIED) | **`pwnhub`** — *"How GitHub Actions workflows can be hacked"* (185★), a compact attack-pattern reference. ⚠️ **Last push 2024-08-23** — a static reference, not a live signal; his current output is smart-contract audits. | `github.com/nikitastupin/pwnhub` · **no feed** · `context` |
| **Trail of Bits** | Trail of Bits | Origin of the **Trusted Publishing** model (2023-05-23) — the OIDC-based, credential-free publishing pattern since adopted by PyPI, npm, crates.io, RubyGems, NuGet and pub.dev. **This is the structural fix for the long-lived-registry-token-in-CI problem that most CI/CD attacks ultimately monetise.** | ✅ `https://blog.trailofbits.com/feed/` · `core` |

### 1.10 The OWASP taxonomy authors — canon, but no longer a live signal

- **Daniel Krivelevich** — Palo Alto Networks, "CTO Application Security, Prisma Cloud". ⚠️ **Role page is live but his most recent post there is 2023-06-06; treat the 2026 role as UNVERIFIED.** **Omer Gil** is the co-author who *is* still active (§1.6). **Ory Segal** is the third project leader (verified on the OWASP page) and was not in our brief.
- **The taxonomy is the field's shared vocabulary** — CICD-SEC-1..10 (full list in §4.7), and every vendor scanner maps findings to those IDs. Speak it fluently.
- ⚠️ **But the project is effectively unmaintained.** Stable release still **v1.0, October 2022**. The **content repo `cider-security-research/top-10-cicd-security-risks` last received a commit on 2023-01-18** (428★, 3 open issues); the OWASP site-page repo has seen only cosmetic pushes since. It predates self-hosted-runner takeover at scale, cache poisoning, artifact token leakage, OIDC claim confusion, deployment poisoning, impostor commits, and the tag-mutability class tj-actions demonstrated.
- **Use it as vocabulary, not as a coverage model.** `core` as canon; `context` as signal.
- **Related:** **CI/CD Goat** (`cider-security-research/cicd-goat`, 2,296★) — the deliberately-vulnerable CI/CD range built for the Top 10. **Last pushed 2024-07-14; unmaintained.** Still a usable test corpus alongside `gha-hazmat`.

### 1.11 Vendor research arms where individual attribution failed — stated honestly

We could **not** verify individual researcher names from primary sources for these, and you should not cite the names we heard associated with them:

- **Checkmarx** — main feed (`https://checkmarx.com/feed/`, GET works, HEAD 403s) is almost entirely marketing/AppSec-strategy content with no supply-chain research in the current window; the "Checkmarx Zero" research arm sits behind URLs that 403 to automated fetches. Names heard associated (Yehuda Gelb, Tal Folkman, Jossef Harush Kadouri) are **UNVERIFIED.** `context`
- **Cycode** — most posts now bylined "Cycode Team". Individual bylines do appear (e.g. **Yuval Elbar**, GHSA-p9r8-2q67-fp86, Aug 2026), and they published a keyv/cacheable npm worm analysis (Aug 2026) that weaponised AI coding agents. **Alex Ilgayev, whom one might associate with Cycode's Actions research, could not be verified — UNVERIFIED.** `context`
- **Sysdig TRT** — no current CI/CD-specific research found; the last month of their feed is Kubernetes release notes and AI product marketing, with no author bylines. Lowest priority of the vendor research arms for our slice. `context`
- **Socket** — collective "Socket Research Team" byline; individual attribution weak. Among the first on the **`@ctrl/tinycolor` compromise (Sept 2025)** that became the Shai-Hulud worm's propagation base (40+ packages). ⚠️ **No working feed found** (`/blog/rss.xml` 404, `/blog/feed` 404, `/rss.xml` 403 Cloudflare) **and the site is behind Cloudflare bot protection** — awkward to monitor automatically. `periodic`
- **Aqua Nautilus** — a real, active group (**Assaf Morag**, Director of Threat Intelligence, ✅ verified; also Yakir Kadkoda, Ilay Goldman). But **we found no Aqua-originated named CI/CD attack class**; their tj-actions post largely summarises and credits StepSecurity, and their strength is container/cloud runtime and npm/PyPI malware. ✅ Feed `https://blog.aquasec.com/rss.xml` (note `https://www.aquasec.com/feed/` 403s). ⚠️ **Aqua prunes older research: several author pages and older URLs now 404 with no Wayback snapshot. Expect link rot.** `periodic`
- **Alex Birsan** (dependency confusion, 2021) — foundational, **no evidence of ongoing publication.** `context`
## 2. Key technologists — the people who own the load-bearing pieces

Everything in this section was verified by direct primary-source fetch: project `MAINTAINERS`/`OWNERS`/`GOVERNANCE` files via the authenticated GitHub API, the GitHub Users API `company` field (which the person sets themselves), the person's own site, and live feed retrievals with HTTP status confirmed.

### 2.0 Read this first: governance files lie about affiliation

The single most useful methodological finding of this whole exercise. **Across Sigstore, in-toto, TUF and SLSA, the projects' own governance files systematically disagree with the individuals' own profiles**, because affiliations move faster than roster files get edited:

| Common assumption | Verified reality | Evidence |
|---|---|---|
| Luke Hinds → Stacklok | **CEO, nolabs, inc** (nolabs.ai). Sigstore `OWNERS.md` still says Stacklok — its last edit was literally a commit titled *"Update OWNERS.md to correct Luke's affliation"* (2025-02-17), and it is stale **again**. | github.com/lukehinds |
| Naveen Srinivasan / Laurent Simon → Scorecard maintainers | **Both EMERITUS.** Neither is a current maintainer. | ossf/scorecard MAINTAINERS.md |
| Marina Moore → NYU | **Edera** (edera.dev — *not* edera.com, an unrelated healthcare company) | GitHub API, `@mnm678` |
| Joshua Lock → Verizon/VMware | **University of Lincoln / King's College London** — he left industry for academia. Corroborated by a SLSA commit *"nonspec: remove Verizon's logo"* (2026-08-06). | `@joshuagl` |
| Lukas Pühringer → NYU | **Eclipse Foundation** | `@lukpueh` |
| Aditya Sirish A Yelgundhalli → NYU | **Bloomberg** | in-toto/attestation MAINTAINERS.md |
| Trishank Karthik Kuppusamy → Datadog | Emeritus everywhere; **his own bio reads "Should be inactive after Sep 19th 2025."** Zero publications 2024-2026; zero public GitHub orgs. | `@trishankatdatadog` |
| Dan Lorenc → Sigstore steering | **Replaced on the TSC by Priya Wadhwa in Dec 2022.** Still Chainguard's founder and a loud voice; not in Sigstore governance. | `sigstore/community` commit log |
| William Woodruff → Trail of Bits | Profile now lists **`@astral-sh` `@openai`** | `@woodruffw` |
| Mike Fiedler still at PyPI? | **YES, confirmed active** (Apr 2026 post), role funded by Alpha-Omega | blog.pypi.org |

**Rule to carry forward: where a roster file and a person's self-set `company` field disagree, trust the person.** And prefer rosters that are *freshly committed* — in-toto's `STEERING-COMMITTEE.md` (last touched 2026-07-06) is the single most current governance snapshot in this ecosystem, and it tracked three personnel moves that faculty pages and TUF's own maintainer file (untouched since 2024-03-27) missed entirely.

### 2.1 Sigstore — OpenSSF Graduated

Org `github.com/sigstore` · community repo `sigstore/community` · TSC roster in `OWNERS.md`.
**Caveat:** TSC membership has not changed since Aug/Dec 2022. Treat `OWNERS.md` as a historical artifact, not a live org chart.

**TSC:** Luke Hinds (nolabs — originator, now largely rotated into AI-agent security; `context`) · **Bob Callaway** (Google, Rekor/Fulcio architecture, top rekor committer; `core`) · **Santiago Torres-Arias** (Purdue; `core`) · Trevor Rosen (GitHub; `periodic`) · Priya Wadhwa (Chainguard; `periodic`).

**The people actually shipping today** (from blog bylines and contributor graphs, not the roster):
- **Hayden Blauzvern — Google.** GitHub handle is `@Hayden-IO` (note: `haydentherapper` 404s). Wrote *"Rekor v2 GA — Cheaper to run, simpler to maintain"* (2025-10-10). `core`
- **Zach Steindler — GitHub** (`@steiza`). **The most load-bearing single person for git-serious's purposes.** He authors Sigstore releases (Cosign v3, sigstore-c) *and* co-authored GitHub's *"Disrupting supply chain attacks on npm and GitHub Actions"* (2026-07-28). He is also co-chair of the OpenSSF Securing Software Repositories WG. He is the bridge between Sigstore, npm, and Actions policy. `core`
- **Jussi Kukkonen — Google.** Also a python-tuf maintainer. Wrote *"sigstore.dev and Rekor evolution"* (2026-06-28) — the decision to keep sigstore.dev on Rekor v1 by default. `core`
- **Zack Newman — Chainguard.** Research voice (`speranza`, privacy-preserving signing). `periodic`

**Follow:** blog `https://blog.sigstore.dev/` — **RSS `https://blog.sigstore.dev/index.xml`** ✅ (note `/feed.xml` and `/rss.xml` both 404). List `sigstore-dev@googlegroups.com`. Slack `sigstore.slack.com`. Machine-readable calendar (.ics): `https://calendar.google.com/calendar/ical/fq4kgom2ce43hncnbcfja2ck20%40group.calendar.google.com/public/basic.ics`. Community meeting 1st + 3rd Thursday monthly.
**Release feeds (all ✅):** `https://github.com/sigstore/cosign/releases.atom` (v3.1.3, 2026-08-06 — note **parallel v2 and v3 lines**, v2.6.5 shipped the same day) · `.../rekor/releases.atom` (v1.5.4, 2026-08-20, every 4-8wk) · `.../sigstore-go/releases.atom` (v1.3.0, 2026-07-30, ~monthly).
**Blog cadence is low (~quarterly)** — use the release feeds for change detection.

### 2.2 in-toto — CNCF Graduated

**The repo that matters for CI/CD is `in-toto/attestation`, not the Python implementation** — it defines the predicate format SLSA provenance rides on. If the predicate schema changes, provenance verification breaks.

**Steering Committee** (`in-toto/community/STEERING-COMMITTEE.md`, last commit **2026-07-06** — the freshest governance file found anywhere in this research): Santiago Torres-Arias (Purdue, academia) · Justin Cappos (NYU, academia) · **Aditya Sirish A Yelgundhalli (Bloomberg, industry)** · Jack Kelly (ControlPlane, industry) · John Kjell (ControlPlane, industry).
> **ControlPlane holds two of five seats.** A UK consultancy that is quietly influential in this space and was not on our radar.

**Attestation-spec maintainers** (a different, more current roster): Aditya Sirish A Yelgundhalli (Bloomberg) · **Adolfo García Veytia / `@puerco`** (Carabiner Systems) · **Marcela Melara** (Intel) · **Parth Patel** (Kusari). Emeritus: joshuagl, trishankatdatadog, mikhailswift, TomHennen.

**Follow:** GitHub only — **no project blog, no machine-readable feed of its own**; announcements ride CNCF/OpenSSF channels.
**Releases:** `https://github.com/in-toto/attestation/releases.atom` ✅ — **good signal** (v1.2.0 2026-03-18, v1.1.2 2025-06-14; ~1-2/yr, each meaningful). `https://github.com/in-toto/in-toto/releases.atom` ✅ but near-dormant (v3.1.0 2026-05-04 after a two-year gap).
**Tier:** `core` for the attestation repo; `context` for the implementation.

### 2.3 TUF — CNCF Graduated

Governance is unusual and worth understanding: a **"Consensus Builder" model**, not a committee.
- **Justin Cappos (NYU)** is the Consensus Builder — *"ultimate authority for changes to the TUF specification."* `core`
- **TAP Editors** (review/approve all spec changes): Cappos, Trishank Kuppusamy (inactive), John Kjell, Joshua Lock, Marina Moore, Lukas Pühringer.
- **The TAP process** (TUF Augmentation Proposal, `theupdateframework/taps`, defined in tap1.md) is the RFC mechanism. Rules: minor changes need 2 TAP-editor approvals; major changes need 2 **and must stay open ≥1 week** so security properties can be contemplated. **No feed — watch the repo.**
- **python-tuf** (reference impl) maintainers: Cappos (consensus builder), Marina Moore (Edera), Lukas Pühringer (Eclipse), Jussi Kukkonen (Google), Kairo de Araujo.
- ⚠️ **`theupdateframework/community/MAINTAINERS.md` was last touched 2024-03-27 and is stale** — it still lists people the per-person evidence shows have moved on.

**Releases:** `https://github.com/theupdateframework/specification/releases.atom` ✅ — **unusually good early-warning signal**: dormant 2023-2025 (v1.0.33 was Aug 2023), then **three releases in 2026** (v1.0.34 Jan, v1.0.35 Jul, v1.0.36 2026-08-10). The spec has re-activated. `.../python-tuf/releases.atom` ✅ — roughly annual majors (v7.0.0 2026-05-18), and they do not fear breaking changes, so each release deserves a read.

### 2.4 SLSA — OpenSSF Graduated

**SLSA has TWO separate bodies**, which the usual write-ups miss:
- **Steering Committee** (runs the spec): Adrian Diglio (Microsoft) · Andrew McNamara (Red Hat) · Mike Lieberman (Kusari) · **Michael Winser (Eclipse Foundation)** · Tom Hennen (Google).
- **Maintainers:** Aditya Sirish A Yelgundhalli (Bloomberg) · Andrew McNamara (Red Hat) · Arnaud Le Hors (IBM) · **Marcela Melara (Intel)** · **Mark Lodato (Google)** · Michael Lieberman (Kusari) · Pavel Iakovenko (GitHub) · Tom Bedford (Bloomberg) · Tom Hennen (Google). **Retired:** Kris K (`@kpk47`), Joshua Lock, Trishank Kuppusamy, Zachariah Cox.

- **Mark Lodato (Google)** — original SLSA author, 714 commits to the spec repo. `core`
- **Marcela Melara — Research Scientist, Intel Labs** (Software and Systems Architecture Team), also on the **OpenSSF Technical Advisory Council**. Works on attested CI/CD and confidential computing; bridges SLSA + in-toto + academia (SCORED '23 chair; author of *Auditing the CI/CD Platform: Reproducible Builds vs. Hardware-Attested Build Environments*, SCORED 2024). **She is the single best-fit person in this whole map for what git-serious does.** `core`. Site `https://masomel.github.io/` (no RSS), GitHub `@marcelamelara`.
- **Michael Lieberman (Kusari, co-founder)** — leads GUAC; highly visible conference speaker. `core`
- **Tom Hennen (Google)** — on both bodies; strongest continuity signal. `core`

**Follow:** `https://slsa.dev` — **Atom `https://slsa.dev/feed.xml`** ✅. List `slsa-discussion@groups.google.com`. Slack `#slsa` on slack.openssf.org. **Weekly specification meeting** is the live one — slsa.dev/community notes the general Community meeting and Tooling SIG are **no longer held regularly**. The issue tracker is the real workspace.
- ⚠️ **`slsa-framework/slsa` has ZERO GitHub Releases** — `releases.atom` returns 200 but is permanently empty and will never fire. **Use `https://github.com/slsa-framework/slsa/tags.atom`** ✅ instead.
- **SLSA v1.2 is current** (tags: v1.2, v1.2-rc1, v1.1, v1.0.0, …). Anything citing v1.0/v1.1 as current is out of date.

### 2.5 OpenSSF Scorecard — OpenSSF Incubation (not Graduated)

**Steering Committee:** **Stephen Augustus** (Bloomberg, `@justaugustus` — also a Kubernetes-governance heavyweight) · **Raghav Kaul** (Google) · **Spencer Schrock** (Google) · Jeff Mendoza (Microsoft).
**Maintainers** also include **Adam Korczynski** (ADA Logics — the OSS-Fuzz/fuzzing specialist) and, for the Azure DevOps client, **Jamie Magee** (Microsoft). The `scorecard-doc-maintainers` group is **empty**.
**Emeritus:** Azeem Shaikh, Laurent Simon, Naveen Srinivasan.

**Why it matters concretely:** Scorecard's `Branch-Protection`, `Token-Permissions`, `Pinned-Dependencies` and `Dangerous-Workflow` checks are the de facto machine-readable audit of a repo's Actions configuration. **New check versions change an org's score without the org changing anything** — so release-watching here is operational, not merely informational. It is also the most direct public analogue to part of what git-serious computes.
**Follow:** checks doc `https://github.com/ossf/scorecard/blob/main/docs/checks.md`; releases `https://github.com/ossf/scorecard/releases.atom` ✅ — **2-4 minor releases/yr and slowing** (v5.5.0 2026-04-23, v5.4.0 2025-11-14; ~4 months quiet as of Aug 2026). No project blog; announcements ride `https://openssf.org/feed/`.

### 2.6 `b4` / `patatt` — Konstantin Ryabitsev, Linux Foundation

**Verified**: GitHub `company` = `@linuxfoundation`, `@mricon`. Director of IT Infrastructure Security / kernel.org sysadmin.

**Why he matters concretely:** he owns the *actual trust plumbing* of the largest email-based development workflow in existence. `patatt` is essentially DKIM-for-patches; `b4` is the tool that consumes it. **This is the non-forge model of CI/CD provenance** — valuable to us precisely because it does not assume GitHub. If git-serious ever needs a story for "how do you attest a change that never touched a forge," this is the prior art.
- `b4` — PyPI **v0.16.0, 2026-08-05**; docs `https://b4.docs.kernel.org/`; repo `https://git.kernel.org/pub/scm/utils/b4/b4.git` (⚠️ git.kernel.org returns 403 to bots).
- `patatt` — PyPI **v0.8.0, 2026-07-22**.
- `korgalore` — his newest work (blog post 2026-01-20).

**Follow:** blog `https://people.kernel.org/monsieuricon` — **RSS `https://people.kernel.org/monsieuricon/feed/`** ✅ (writefreely; `feed.atom` and `.rss` both 404). **Cadence ~1-2 posts/year — low volume, high value.** Tooling list `tools@kernel.org` → `https://lore.kernel.org/tools/new.atom` ✅. PyPI release feeds are a clean proxy: `https://pypi.org/rss/project/b4/releases.xml`, `.../patatt/releases.xml`.
**Tier:** `core` if non-forge provenance matters to us; `periodic` otherwise.

### 2.7 The Linux kernel release and CVE process — what each person actually emits

**Linus Torvalds (Linux Foundation)** emits the mainline git tree and merge-window/`-rc`/final release announcements to LKML. **He does not blog, does not tweet, has no feed.**
- ✅ **Use `https://www.kernel.org/feeds/kdist.xml`** (RSS 2.0) instead of the mailing list — the canonical machine-readable release feed, updated within the hour. Live state at time of writing: mainline **7.2**; stable 7.2.1, 7.1.11; longterm 6.18.47 / 6.12.106 / 6.6.154 / 6.1.185 / 5.15.218 / 5.10.267; linux-next `next-20260826`.
- LKML archive `https://lore.kernel.org/lkml/new.atom` ✅ is an unfiltered **firehose**; Linus's release mails are a few needles a year in it. `context`.

**Greg Kroah-Hartman (Linux Foundation)** — **he personally IS the kernel CVE pipeline.** All 25 most recent messages in the CVE announce archive were authored by `Greg Kroah-Hartman <gregkh@linuxfoundation.org>`. Volume is extreme: 12 CVEs published within ~30 seconds on 2026-08-26.
- Kernel-as-CNA, verified from MITRE's own `CNAsList.json`: shortName `Linux`, cnaID **`CNA-2024-0016`** (confirms the 2024 registration), org `kernel.org`, scope *"Any vulnerabilities in the Linux kernel as listed on kernel.org, excluding EOL versions"*, contact `cve@kernel.org`, advisories at `https://lore.kernel.org/linux-cve-announce/`, top-level root MITRE. Process: **CVEs are auto-assigned only after a fix lands in a stable tree**, tracked by git commit ID.
- ✅ **`https://lore.kernel.org/linux-cve-announce/new.atom`** — the single best kernel-security feed in existence. `core` (as data).

> **⚠️ Operational gotcha for whoever builds the poller.** lore.kernel.org is behind "Anubis" anti-bot protection, **selectively**. Plain `/<list>/new.atom` feeds serve fine (verified 200 on linux-cve-announce, stable, lkml, tools, git). But **HTML archive pages and all search/query endpoints return an Anubis JS challenge instead of content**. The otherwise-ideal trick of filtering a firehose down to one sender via public-inbox query-scoped Atom (`?q=f:gregkh...&x=A`) returns **HTTP 200 with a challenge page and zero entries, silently**. Budget for full-feed ingestion plus local filtering, and alarm on "feed parsed but zero entries."

### 2.8 Package-registry security programs

**PyPI / PSF — the best-documented program of the lot.**
⚠️ The obvious blog feed URLs 404. **Working feeds (Material-for-MkDocs convention):** ✅ **`https://blog.pypi.org/feed_rss_created.xml`** (use this) and `.../feed_rss_updated.xml`. ~1-3 posts/month, with proper `dc:creator` bylines so per-author filtering works.
- **Mike Fiedler — PSF, PyPI Safety & Security Engineer, Alpha-Omega funded. ✅ still current.** Also co-chairs the OpenSSF Securing Software Repositories WG. Recent: *"PyPI has completed its second audit"* (2026-04-16 — Sovereign Tech Agency funded, Trail of Bits run: 14 findings, 2 High / 1 Medium / 7 Low / 4 Info; 12 remediated, 2 accepted), *"PyPI and Shai-Hulud"* (2025-11-26), ***"Token Exfiltration Campaign via GitHub Actions Workflows"* (2025-09-16)**, *"Preventing Domain Resurrection Attacks"* (2025-08-18). `core`
- **Seth Larson — PSF Security Developer-in-Residence, Alpha-Omega funded.** Not in our original brief and **arguably the highest-output PyPI security voice.** Former urllib3 lead. Recent: *"Releases now reject new files after 14 days"* (2026-07-22), *"Incident Report: LiteLLM/Telnyx supply-chain attacks"* (2026-04-02), *"Phishing attacks with new domains likely to continue"* (2025-09-23), *"Preventing ZIP parser confusion attacks"* (2025-08-07). **Follow: `https://sethmlarson.dev/` — Atom `https://sethmlarson.dev/feed`** ✅. `core`
- **Dustin Ingram — Google OSS security team**, PSF/PyPI/PyPA. `periodic`. `https://di.dev`
- **William Woodruff — `@astral-sh` / `@openai`** (previously Trail of Bits). Author of PyPI's **Trusted Publishing** and much of the attestation work; also the author of `zizmor` (see §1). `core`
- **Donald Stufft — affiliation UNVERIFIED** (no company on profile) **but NOT gone**: the GitHub Events API shows him opening PRs and reviewing on `pypi/warehouse` on 2026-08-10. Status: technically active, organizationally unverifiable. `context`

**npm / GitHub.** There is **no npm-specific blog feed**; npm security messaging lands in the GitHub Blog security category.
- **Zach Steindler** (see §2.1) co-authored ***"Disrupting supply chain attacks on npm and GitHub Actions"* (2026-07-28)** with **Greg Ose**. `core`
- **Xavier René-Corail — GitHub**, authored ***"Our plan for a more secure npm supply chain"* (2025-09-22)**, explicitly responding to *"a surge in package registry attacks."* This is npm's strategy document. `core`
- Also publishing: Greg Ose, Ankit Kumar Honey (*"GitHub malware advisories no longer stop at npm"*, 2026-08-06), Madison Ficorilli (Advisory Database + malware campaigns). `periodic`
- Feed: ✅ `https://github.blog/security/feed/`

**crates.io / Rust.** Roster verified from the canonical machine-readable source `rust-lang/team/teams/crates-io.toml` (the rust-lang.org page just redirects): leads `jtgeibel`, `Turbo87`; members `carols10cents`, `LawnGnome`, `mdtro`, `eth3lbert`. Lists `crates-io@rust-lang.org`, `help@crates.io`; Zulip stream `t-crates-io` (+ `#incident-response`, `#operations`, `#moderation`).
- **Tobias Bieniek — Rust Foundation**, crates.io team **co-lead**. `core`
- **Adam Harvey — Rust Foundation** security SWE **and** simultaneously a crates.io team member (`LawnGnome`). **That dual seat is the real security↔registry link.** `core`
- **Walter Pearce — Security Engineer, Rust Foundation** (previously Epic Games, Blizzard). `core`
- Justin Geibel (co-lead), Joel Marcey (Director of Technology, oversees the Security Initiative), Carol Nichols.
- Security Initiative outputs: **Painter** (call-graph mapping) and **Typomania** (typosquatting detection), plus annual/semi-annual reports.
- Feeds: ✅ `https://blog.rust-lang.org/feed.xml` (project) · ✅ `https://rustfoundation.org/feed/` (foundation — note `feed.xml` 404s and the domain moved from `foundation.rust-lang.org` via 301).

**RubyGems.** ✅ **Atom `https://blog.rubygems.org/atom.xml`** (declared in the page's own `<link rel="alternate">`; `feed.xml`/`index.xml` 404). ⚠️ **Posts are not bylined** — no named-person signal. Cadence high (~weekly) because every gem release is announced, with security content interleaved: *"Security advisory: possible leak of legacy API keys via improper cache configuration"* (2026-07-22), *"Protecting rubygems.org from the outside in"* (2026-04), *"RubyGems.org Completes First Security Audit With Trail of Bits"* (2024-12), *"Announcing Trusted Publishing on RubyGems.org"* (2023-12). `periodic`

**Packagist / Composer (PHP).** Nils Adermann (`@naderman`) and Jordi Boggiano (`@Seldaek`) — Composer's creators and operators of Private Packagist. Security contact `security@packagist.org`. ✅ **RSS `https://blog.packagist.com/rss/`**. ~2-4 posts/month and unusually CI/CD-relevant right now: ***"Securing our GitHub Actions workflows with zizmor"* (2026-07-07)**, *"Immutable Versions on Packagist"* (2026-06-12), *"Restricting Composer plugins across your organization"* (2026-06-04), *"Blocking malware downloads for every Composer version"* (2026-06-01). `periodic`

### 2.9 GitHub's own security and Actions engineering voices

> **⚠️ The most important feed finding in this report: `https://securitylab.github.com/feed.xml` is a DEAD STUB.** It returns HTTP 200 and valid Atom, but it is **534 bytes with zero `<entry>` elements** — just the Jekyll header. Anyone subscribed to it has been silently receiving nothing. `securitylab.github.com/research/` now 301-redirects to the GitHub Blog.

**Use these instead (all verified 200 with real content):**

| Feed | Status | Content |
|---|---|---|
| ✅ `https://securitylab.github.com/advisories/feed.xml` | 10 entries, 372 KB | GHSL advisories — the real Security Lab output |
| ✅ `https://github.blog/tag/github-security-lab/feed/` | 10 items, bylined | Security Lab research posts with `dc:creator` |
| ✅ `https://github.blog/security/feed/` | 200 | GitHub Blog security category |
| ✅ `https://github.blog/changelog/feed/` | 200, **rolling 10-item window** | Actions/platform changes — **poll at least daily or you will miss entries** |
| ✅ `https://github.blog/changelog/label/actions/feed/` | 200 | Actions-scoped changelog — **much higher signal-to-noise than the unfiltered changelog** |
| ⚠️ `https://securitylab.github.com/feed.xml` | 200 but **EMPTY** | — |

**Individuals verified as currently publishing** (from live `dc:creator` fields):
- **Man Yue Mo — GitHub Security Lab, ✅ still current.** `core`
- **Kevin Backhouse — GitHub Security Lab, ✅ still current** (*"AI-supported vulnerability triage with the GitHub Security Lab Taskflow"*, 2026-01-14). `core`
- **Joseph Katsioloudes — GitHub.** Most frequent current publisher (*"Inside the Advisory Database and what happens when vulnerability volume…"*, 2026-04-14). `core`
- **Antonio Morales** (fuzzing), **Jonathan Evans** (*"Securing the open source supply chain across GitHub"*, 2026-03-26), **Kevin Crosby** (*"A year of open source vulnerability trends"*, 2026-03-17), **Natalie Guevara**. `periodic`/`context`
- ⚠️ **Jaroslav Lobačevski and Alvaro Muñoz — NOT FOUND** in any current feed going back to Dec 2025. **Mark UNVERIFIED / likely moved on.** Do not cite them as current GitHub Security Lab.

GHSL advisory cadence: **batched** — bursts of ~5 on a single day, then weeks quiet.

### 2.10 The seven people who cover most of the stack

A small set are load-bearing across multiple projects. Following these seven covers most of the standards surface:

**Santiago Torres-Arias** (Sigstore TSC + in-toto SC + TUF emeritus + Purdue faculty) · **Zach Steindler** (Sigstore + npm + GitHub Actions policy + OpenSSF repos WG) · **Aditya Sirish A Yelgundhalli** (in-toto SC + SLSA maintainer + gittuf lead) · **Jussi Kukkonen** (Sigstore + python-tuf) · **Justin Cappos** (TUF Consensus Builder + in-toto originator + CNCF TAG tech lead + NYU lab director) · **Marcela Melara** (SLSA + in-toto attestation + OpenSSF TAC + SCORED + attested-CI/CD research) · **Adam Harvey** (Rust Foundation security + crates.io team).
## 3. Academic research groups and professors

Academia matters here for a specific reason: it is the only part of the field that publishes **negative and contrarian results**. Vendors publish what worked; academics publish that pinning does not help as much as you think, and that trust signals are collapsing. For a product whose job is to tell people what to do about their pipelines, that is the more valuable literature.

### 3.1 NYU Secure Systems Lab — the TUF / in-toto lineage

- **Justin Cappos** — Professor, Computer Science and Engineering, NYU Tandon; **Lab Director** of the Secure Systems Laboratory; also NYU Center for Cybersecurity. Simultaneously **TUF Consensus Builder**, in-toto originator, CNCF TAG Security and Compliance **tech lead**, and co-lead of its Security Assessments subproject. ✅ Verified across four independent sources.
- **The lab is genuinely active** (roster verified 2026-08-27): postdocs **Vidya Lakshmi Rajagopalan** (kernel security, binary analysis) and **Marco De Vincenzi** (automotive/CPS); PhD students **Yaxuan (Alice) Wen**, **Patrick Zielinski** (distributed systems and *version control*), **Ann Malavet**, **Qianxi Chen**, and — note this one — **Sanchit Sahay, working on *build observability***.
- **Recent work, and it has moved toward exactly our problem:**
  - *SourceFabric: Consistent and Scalable Security Policies for Git Repositories* — **IEEE EuroS&P 2026**. Modularises security policy across many repositories in an organisation. This is, essentially, the academic statement of the problem git-serious solves.
  - *Rethinking Trust in Forge-Based Git Security* — **NDSS 2025, Distinguished Paper Award**. Presents **gittuf**: decentralising Git repository integrity so it does not depend on trusting the forge (GitHub/GitLab). Directly relevant to any product whose evidence currently comes *from* the forge.
  - *Enhancing Legal Document Security and Accessibility with TAF* — NDSS 2026.
  - *Securing Automotive Software Supply Chains* (2024, workshop) — Uptane + in-toto for OTA updates.
  - *Towards verifiable web-based code review systems* — Journal of Computer Security 31(2), 2023 (Cappos + Torres-Arias + Curtmola).
- **Follow:** lab `https://ssl.engineering.nyu.edu/` (people, publications) — **no RSS**. Cappos personal page `https://ssl.engineering.nyu.edu/personalpages/jcappos/`. **DBLP `https://dblp.org/pid/27/5136`** (see §3.7 on why DBLP, not Scholar).
- **Cadence:** several papers/year at top venues.
- **Tier:** `core`

### 3.2 Purdue — Santiago Torres-Arias

- **Assistant Professor of Electrical and Computer Engineering, Purdue University.** ✅ Verified three ways (his site, GitHub API `company` updated 2026-07-22, DBLP affiliation).
- ⚠️ **No named lab exists.** Guessed lab domains all fail to resolve; his site says he is "currently looking for motivated students," implying an active but informally-named group. **Do not invent a lab name.**
- **Why he matters:** he is arguably the highest-connectivity node in the entire map — **Sigstore TSC + in-toto Steering Committee + TUF emeritus + CNCF Catalog of Supply Chain Compromises lead + Purdue faculty**, simultaneously. He is the person through whom academic supply-chain work becomes deployed infrastructure.
- **Follow:** personal site **`https://badhomb.re`**; GitHub `@SantiagoTorres`; **DBLP `https://dblp.org/pid/185/1711`**. **No RSS on the personal site.**
- **Tier:** `core`

### 3.3 NC State — Laurie Williams

- **Goodnight Distinguished University Professor in Security Sciences**, Computer Science, NC State. **Co-director, NC State Secure Computing Institute**; co-director, Science of Security Lablet. ✅ Verified from the NC State faculty page.
- **Why she matters — she runs the largest funded programme in this area.** She leads the NSF grant **"Collaborative: SaTC: Frontiers: Enabling a Secure and Trustworthy Software Supply Chain" (2022-2027, $7.1M)**. If you want to know what the academic field will be saying in three years, it is largely what this grant funds.
- **Recent work:**
  - *Research Directions in Software Supply Chain Security* — **ACM TOSEM, 2025**. The field-defining survey; the right single citation for "what is the research agenda."
  - *The Software Supply Chain as a Market for Lemons: A Multivocal Review of Trust Signal Collapse* — **arXiv, 2026-08-21** (Paramitha, Kästner, Williams).
  - *The Rising Cost of Trust: Practitioners' Trust Signals, Controls, and Responses in the Software Supply Chain* — **arXiv, 2026-08-21** (Paramitha, Paidipalli, Williams, Kästner).
  > Those last two, published six days ago, are an *empirical study of whether supply-chain trust signals actually work in practice* — i.e. whether attestations, provenance, scores, and badges change behaviour. **This is the most directly load-bearing recent academic work for git-serious's positioning**, and it is available free on arXiv.
- **Follow:** NC State faculty page; **arXiv is the fastest route** (§3.7). **No personal RSS found.**
- **Tier:** `core`

### 3.4 CMU — Christian Kästner (and Bogdan Vasilescu)

- **Christian Kästner** — **Associate Professor, School of Computer Science, CMU**; Director of the CMU Software Engineering PhD Program. Research themes: AI engineering, **software supply chain security**, software variability. ✅ Verified from his CMU page.
- **Why he matters — he publishes the contrarian empirical results:**
  - ***"Pinning Is Futile"* — FSE 2025.** Demonstrates the limits of dependency version pinning as a supply-chain defence. **Read this before building any product feature that recommends pinning**, which git-serious plausibly will. It does not say pinning is worthless; it bounds what pinning buys you, and that boundary is a thing we should be able to state honestly to a customer.
  - *"Six Million (Suspected) Fake Stars on GitHub"* — **ICSE 2026**. Popularity signals on GitHub are manipulable at scale — relevant to any heuristic that weights an action or dependency by its stars.
  - *"Understanding the Response to Open-Source Dependency Abandonment in the npm Ecosystem"* — **ICSE 2025, Distinguished Paper Award**.
  - Plus the two Aug-2026 trust-signal papers with Laurie Williams above.
- **Bogdan Vasilescu** — CMU, software ecosystems / MSR-style empirical work. ⚠️ **Current title UNVERIFIED in this pass.**
- **Follow:** `https://www.cs.cmu.edu/~ckaestne/` — **no RSS found**; use arXiv and DBLP.
- **Tier:** `core` (Kästner), `periodic` (Vasilescu).

### 3.5 European groups

- **Martin Monperrus — Professor of Software Technology, KTH Royal Institute of Technology, Stockholm.** ✅ Verified from `https://www.monperrus.net/martin/`. Publishes heavily and fast on build reproducibility, dependency bots, and supply-chain tooling. **No RSS found on his site**; he is however unusually arXiv-forward, so the arXiv author feed works well. `core`.
- **Benoit Baudry** — ⚠️ **UNVERIFIED.** Formerly KTH; reported to have moved to **Université de Montréal**. His personal site (`baudry.dev`) returned a **502 and a TLS name mismatch** during this research, so we could not confirm anything. He co-authors extensively with Monperrus on reproducibility. **Check by hand before citing.**
- **TU Delft — Georgios Gousios** ⚠️ **UNVERIFIED / likely moved to industry.** **Sebastian Proksch** and **Diomidis Spinellis** (part-time) also associated. Not confirmed in this pass.
- **Chalmers / University of Gothenburg** — relevant enough that the **Reproducible Builds Summit 2026 is being held in Gothenburg**. Specific faculty **not verified**.
- **Yasemin Acar** (Paderborn / George Washington) — usable security of supply-chain tooling, i.e. *why developers do not use the secure path*. ⚠️ **Current institution UNVERIFIED.** Relevant because git-serious's adoption problem is a usability problem as much as a detection problem.

### 3.6 The industry-adjacent researchers who publish academically

- **Marcela Melara — Research Scientist, Intel Labs** (Software and Systems Architecture Team); also OpenSSF **Technical Advisory Council**, SLSA maintainer, in-toto attestation maintainer, and **SCORED '23 chair**. Her paper ***"Auditing the CI/CD Platform: Reproducible Builds vs. Hardware-Attested Build Environments"* (SCORED 2024)** is, of everything found in this research, **the closest published academic statement of git-serious's own problem**: how do you actually get trustworthy evidence about what a build platform did? She is also a co-author on SourceFabric (EuroS&P 2026). Site `https://masomel.github.io/` (**no RSS**), GitHub `@marcelamelara`. `core`.
- **Aditya Sirish A Yelgundhalli — Bloomberg** (industry, NYU alumnus). First author on **SourceFabric (EuroS&P 2026)** and **gittuf (NDSS 2025, Distinguished Paper)**; in-toto Steering Committee; SLSA maintainer. The research judgment stands even though he is now an industry node. `core`.

### 3.7 How to actually follow academic output — a practical note

⚠️ **Google Scholar profile URLs could not be verified in this research at all.** Scholar's endpoints redirect automated fetches to a login wall. Any Scholar `user=` ID not taken directly from the researcher's own website should be treated as unverified and looked up by hand.

**Use these instead — both verified working:**

1. ✅ **DBLP** is the durable, machine-readable spine. Every author page has stable XML/JSON at `https://dblp.org/pid/<PID>.xml`. Verified PIDs: Cappos `27/5136` · Torres-Arias `185/1711` · Marina Moore `236/5493` · Kuppusamy `44/8573`.
2. ✅ **arXiv is the fastest route and it works.** Verified live:
   - **API query** (returns Atom): `http://export.arxiv.org/api/query?search_query=all:%22software+supply+chain%22&sortBy=submittedDate&sortOrder=descending&max_results=20` — this is how we surfaced the two 2026-08-21 Williams/Kästner trust-signal papers.
   - **Category feed:** `https://rss.arxiv.org/rss/cs.CR` — valid RSS 2.0, **50 items, rebuilt daily at 04:00 UTC**. High volume and heavily AI-weighted right now; filter locally.
3. ✅ **The Reproducible Builds monthly report** (§4.8) includes a "scholarly papers" section — **a free, human-curated academic filter for this exact sub-field, delivered monthly.** For the cost of one RSS subscription this is better than most literature alerts.
## 4. Institutions, foundations, and working groups

These set the direction the tooling follows. Verified against primary sources (GitHub API, project repos, official sites) on 2026-08-27.

### 4.1 OpenSSF (Open Source Security Foundation) — Linux Foundation

- **What it is:** The umbrella foundation for Scorecard, the Best Practices Badge, SLSA stewardship, Alpha-Omega, and the repository-security guidance corpus.
- **Signal:** Standards and guidance documents, WG meeting notes, funded-engineer output, the SOSS podcast.
- **Why it matters to us:** Scorecard's `Token-Permissions`, `Dangerous-Workflow`, and `Pinned-Dependencies` checks are the closest thing the industry has to a *machine-checkable* CI/CD hygiene baseline — they are effectively a competing/complementary signal to anything git-serious computes. The Securing Software Repositories WG is where "Trusted Publishers" (OIDC-based registry publishing) was standardised, which is the mechanism that replaces long-lived registry tokens in CI.
- **Follow:** https://openssf.org/feed/ — **verified valid RSS 2.0** (checked 2026-08-27; most recent item 2026-08-26).
- **Cadence:** 2-6 posts/week. Currently heavily weighted to EU CRA readiness.
- **Tier:** `core`

**Working groups that actually matter (verified activity via GitHub API, 2026-08-27):**

| WG | Repo | Last push | Assessment |
|---|---|---|---|
| Securing Software Repositories | `ossf/wg-securing-software-repos` | 2026-04-06 | **Most relevant to us.** Co-chairs **Mike Fiedler** (PyPI/PSF) and **Zach Steindler**. Publishes at https://repos.openssf.org/ — "Principles for Package Repository Security" (Feb 2024), "Trusted Publishers for All Package Repositories" (Jul 2024), "Build Provenance for All Package Registries" (Jul 2023), "Crafting a Package Deletion Policy" (Apr 2025). Meets alternate Wednesdays, alternating EMEA (13:00 UTC) / APAC (22:00 UTC). |
| Best Practices for OSS Developers | `ossf/wg-best-practices-os-developers` | 2026-08-26 | Very active. Owns the Best Practices Badge criteria and the Concise Guides. |
| Supply Chain Integrity | `ossf/wg-supply-chain-integrity` | 2026-01-15 | Slowing. Home of S2C2F; SLSA lives in its own org. |
| Security Tooling | `ossf/wg-security-tooling` | 2025-07-06 | **Effectively dormant** — 13 months without a push. Do not treat as a live signal. |

- **Best Practices Badge:** https://www.bestpractices.dev/ — **has a JSON API**: `https://www.bestpractices.dev/projects.json?pq=<query>` returns valid JSON (verified — returns `[]` on no match, so it is a live endpoint, not a 404). Source at `github.com/ossf/best-practices-badge`. Tier: `periodic`.

### 4.2 Alpha-Omega

- **What it is:** OpenSSF-hosted funding vehicle (>$7M/yr per its own site) that pays for security engineers *embedded in* critical OSS projects — most relevantly the PyPI safety-and-security engineer role.
- **Leadership (from https://alpha-omega.dev/, verified 2026-08-27):** Bob Callaway (Google), Michael Scovetta (Microsoft), Tom "spot" Callaway (AWS), Michael Winser (co-founder), Kevin King, Mirko Swillus, Paul Brown, Yesenia Yser (Microsoft), Miaolai Zhou (AWS).
- **Why it matters:** Alpha-Omega funding is a *leading indicator* of where registry-side security capability will appear next. If they fund a registry, expect Trusted Publishing / provenance / 2FA enforcement there within ~18 months.
- **Follow:** https://alpha-omega.dev/resources/blog/ and `github.com/ossf/alpha-omega` (last push 2026-08-25). Annual reports are published in the repo. **No RSS feed found on the blog — unverified whether one exists.**
- **Cadence:** Monthly-ish blog, annual report.
- **Tier:** `periodic`

### 4.3 CNCF TAG Security → **now TAG Security and Compliance** (IMPORTANT CHANGE)

- **What changed:** `cncf/tag-security` was **archived read-only on 2025-12-18** as part of a CNCF-wide TAG restructure (verified: every `cncf/tag-*` repo is now `archived=true`). The successor is **TAG Security and Compliance**, and it does **not** have its own repo — it lives inside the TOC repo at `github.com/cncf/toc/tree/main/tags/tag-security-and-compliance`. The five current TAGs are Developer Experience, Infrastructure, Operational Resilience, **Security and Compliance**, and Workloads Foundation (source: `cncf/toc/tags.yaml`).
- **Leadership (verified from `cncf/toc/tags.yaml`, 2026-08-27):** Chairs — Evan Anderson (Custcodian), John Kjell (Control-Plane.io), **Marina Moore (Edera)**. Tech leads — Andrew McNamara (Red Hat), **Justin Cappos (NYU)**, Maxime Coquerel, Sherine Khoury, Shuting Zhao (Nirmata), Yoshiyuki Tabata (Hitachi).
- **Signal:** Whitepapers ("Software Supply Chain Best Practices", Mar 2025), the Security Assessment process (TSSA), meeting recordings.
- **Follow:** repo above; mailing list https://lists.cncf.io/g/cncf-tag-security-and-compliance ; Slack `#tag-security-and-compliance` in cloud-native.slack.com (channel C08JZ9YLAA3); recordings https://www.youtube.com/@CNCFTAGSecurityandCompliance
- **Cadence:** Weekly/biweekly meetings; whitepapers roughly annually.
- **Tier:** `periodic`
- **⚠️ Gap created by the reorg:** the **Catalog of Supply Chain Compromises** — the field's best-known curated incident list, previously led by Santiago Torres-Arias — is stranded in the archived read-only repo (`cncf/tag-security/community/catalog`). Only `security-assessments` carried over as a subproject. **There is no announced new home.** See the gap statement (§9.1).

### 4.4 Linux Foundation / kernel.org infrastructure

- **Linux kernel CNA:** the kernel became its own CVE Numbering Authority in Feb 2024, and now issues a very high volume of CVEs from the stable process. The machine-readable channel is the **`linux-cve-announce` mailing list**, archived at https://lore.kernel.org/linux-cve-announce/ with a per-list Atom feed at `https://lore.kernel.org/linux-cve-announce/new.atom`. **⚠️ Verification note:** lore.kernel.org now sits behind Anubis bot-protection and returned "Access Denied" to our fetcher — the archive is real and widely used, but *an automated poller will need a browser-like User-Agent and may be challenged*. Treat the feed URL as **structurally correct but not end-to-end verified from here.**
- **Why it matters:** if git-serious ever correlates runner-host kernel versions to known-exploited bugs, this is the firehose — and it is a firehose (hundreds of CVEs/month), so it is a *data source*, not a reading list.
- **Tier:** `context` (as reading) / `core` (as data, if consumed)

### 4.5 CISA

- **KEV (Known Exploited Vulnerabilities) catalog — the single most useful CISA artifact for us.**
  - JSON: `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` — **verified live**: `catalogVersion 2026.08.26`, `dateReleased 2026-08-26T17:00:09Z`, `count: 1682`.
  - CSV equivalent: `https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv` (**unverified** — same directory pattern, not fetched).
  - Cadence: updated most weekdays. Tier: `core` (as data).
- **Secure by Design:** **UNVERIFIED.** `https://www.cisa.gov/resources-tools/resources/secure-by-design` returned HTTP 403 to our fetcher. There were widely-reported changes to CISA's programme footprint during 2025 and we could **not** confirm from a primary source whether Secure by Design and the Secure Software Development Attestation Form are still in force. **Do not assert either way — check before citing.**
- **Tier:** `periodic` for policy, `core` for KEV data.

### 4.6 NIST

- **SSDF is moving.** Verified from https://csrc.nist.gov/ :
  - SP 800-218 v1.1 (final, 2022-02-03) — the current binding reference.
  - SP 800-218A (final, 2024-07-26) — generative-AI addendum.
  - **SP 800-218 Rev. 1 — "SSDF Version 1.2", Initial Public Draft, released 2025-12-17.**
  - **"Secure Software Development, Security, and Operations (DevSecOps) Practices" — Initial Preliminary Draft, 2026-03-24.**
- **Why it matters:** SSDF is the control language US federal procurement speaks. A v1.2 draft plus a *DevSecOps-specific* draft means the vocabulary git-serious should map its findings to is being rewritten right now. Reading the drafts is a cheap way to be aligned with the control names customers will be asked about in 2027.
- **Follow:** https://csrc.nist.gov/publications/search — CSRC advertises an RSS link in its footer but the **exact feed URL was not resolvable from the page content; treat as unverified.** The reliable low-tech route is the CSRC "Drafts open for comment" page plus the NIST mailing list.
- **Cadence:** Bursty; drafts + 60-day comment windows.
- **Tier:** `core` while the v1.2 / DevSecOps drafts are open.

### 4.7 OWASP

- **Top 10 CI/CD Security Risks** — project leaders **Daniel Krivelevich, Omer Gil, Ory Segal**. **Current version is still v1.0, October 2022**, and the project page shows **no update in progress** (verified 2026-08-27). Repo `OWASP/www-project-top-10-ci-cd-security-risks` last pushed 2025-12-22.
  - The ten IDs: CICD-SEC-1 Insufficient Flow Control · 2 Inadequate IAM · 3 Dependency Chain Abuse · 4 Poisoned Pipeline Execution (PPE) · 5 Insufficient PBAC · 6 Insufficient Credential Hygiene · 7 Insecure System Configuration · 8 Ungoverned 3rd Party Services · 9 Improper Artifact Integrity Validation · 10 Insufficient Logging and Visibility.
  - **Why it matters, and the honest read:** this is *the* shared taxonomy — it is what a buyer means when they say "we need CI/CD security coverage." It is also **four years stale** and predates the entire 2023-2026 wave (self-hosted runner takeover at scale, cache poisoning, artifact token leakage, OIDC trust-policy abuse, the tj-actions class of composite-action compromise). Adopting CICD-SEC-N as git-serious's outward-facing vocabulary is a cheap credibility win; relying on it as a *coverage model* would leave real gaps.
  - Follow: https://owasp.org/www-project-top-10-ci-cd-security-risks/ — **no machine-readable feed**; watch the GitHub repo instead.
  - Tier: `core` (as vocabulary), `context` (as live signal).
- **CI/CD Goat** (`cider-security-research/cicd-goat`) — the deliberately-vulnerable CI/CD range that accompanies the Top 10. **Last pushed 2024-07-14 — unmaintained.** Still useful as a test corpus; do not expect new scenarios.
- **CycloneDX** (`CycloneDX/specification`, last push 2026-08-27, very active) — SBOM/BOM format, now also an Ecma standard (ECMA-424; **the Ecma standardisation is widely reported but we did not verify it from an Ecma primary source**). Tier: `periodic`.
- **Dependency-Track** (`DependencyTrack/dependency-track`, last push 2026-08-27, 4.1k stars) — the reference open-source SBOM consumption/monitoring platform. Worth knowing as the shape of "what an org already has" when git-serious arrives. Tier: `context`.
- **Feeds:** GitHub `releases.atom` per repo is the right change signal for both — e.g. `https://github.com/CycloneDX/specification/releases.atom`.

### 4.8 Reproducible Builds

- **What it is:** The long-running cross-distribution project to make builds bit-for-bit reproducible — the only serious answer to "did this artifact really come from that source?"
- **Signal:** A **genuinely monthly** report (verified: "Reproducible Builds in July 2026" published 2026-08-09; June report 2026-07-11; May report 2026-06-04) covering tooling changes, distro progress, upstream patches, and *academic papers in the area*. That last part makes the monthly report an excellent low-cost academic-literature filter.
- **Why it matters:** reproducibility is the verification half of the story git-serious tells about builds. The monthly report is also where new build-nondeterminism classes surface first.
- **Follow:** https://reproducible-builds.org/news/ — **RSS verified**: `https://reproducible-builds.org/blog/index.rss` (valid RSS 2.0, Jekyll-generated).
- **Also:** Summit 2026 will be in **Gothenburg** (announced 2026-08-12) — this is the single best in-person room for this sub-field, and it is small and approachable.
- **Cadence:** Monthly, reliably.
- **Tier:** `core`

### 4.9 IETF SCITT (Supply Chain Integrity, Transparency and Trust)

- **Status: chartered and active** (verified at https://datatracker.ietf.org/wg/scitt/about/). Chairs **Jon Geater** and **Nicole Bates**.
- **Output:** **RFC 9943** (Architecture and Terminology) is published; `draft-ietf-scitt-software-use-cases` complete; REST API, countersigning, and information-model drafts in progress.
- **Why it matters:** SCITT is the standards-track attempt to make "append-only transparency log of supply chain statements" an interoperable primitive rather than a Sigstore-specific one. If a customer asks git-serious for "transparency-log-compatible evidence," this is the vocabulary.
- **Follow:** mailing list `scitt@ietf.org`, archive https://mailarchive.ietf.org/arch/browse/scitt/ (the IETF mail archive exposes per-list Atom).
- **Cadence:** Steady drafts; IETF meeting rhythm (3×/yr).
- **Tier:** `periodic`

### 4.10 EU Cyber Resilience Act — the regulatory clock

- **Verified dates** (https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act):
  - Entered into force **2024-12-10**.
  - **Vulnerability/incident reporting obligations begin 2026-09-11** — i.e. **two weeks from now.**
  - Main obligations apply **2027-12-11**.
  - The European Commission published practical implementation guidance on **2026-07-27**.
- **Why it matters to us specifically:** the CRA is why OpenSSF's own feed is currently ~half CRA content. It creates a near-term, dated, non-optional demand for *evidence about how software was built and how vulnerabilities are handled* — which is exactly the evidence a CI/CD-observing product holds. This is the strongest external forcing function in the field right now, and it has a date on it.
- **Follow:** the Commission page above (no feed); OpenSSF's feed is the better practical proxy because it translates CRA into engineering terms.
- **Tier:** `core` (context/timing), even though it is not security research.
## 5. Where the research actually lands

### 5.1 The one venue built for exactly this: SCORED

**SCORED — Software Supply Chain Offensive Research and Ecosystem Defenses.**
- ✅ **Verified: SCORED '26 runs 2026-10-06 in Prague, co-located with OpenSSF Community Day Europe**, carrying "ACM In-Cooperation" status. CFP posted 2026-05-13, submissions opened 2026-05-20, deadline extended to **2026-07-19**.
- **Note the migration:** SCORED began (2022-2024) as an **ACM CCS workshop**. It is now co-located with **OpenSSF Community Day Europe** rather than CCS — i.e. it has moved from the academic security calendar toward the practitioner/foundation calendar. That is a meaningful signal about where this sub-field's centre of gravity sits.
- **Why it matters to us more than any other venue:** it is the only recurring event whose entire remit is software-supply-chain offense *and* ecosystem defence, and it is the venue where **Marcela Melara's *"Auditing the CI/CD Platform: Reproducible Builds vs. Hardware-Attested Build Environments"* (SCORED 2024)** appeared — the closest published academic statement of git-serious's own problem. Melara chaired SCORED '23.
- **Follow:** `https://scored.dev/` (**no feed found**) · chairs `scored26-chairs@googlegroups.com` (individual chair names are **not published on the site** — a small gap).
- ⚠️ **It is roughly six weeks away at time of writing.** If we want one room this year, this is the strongest candidate: right topic, right size, co-located with the OpenSSF crowd we would otherwise have to chase separately.
- **Tier:** `core`

### 5.2 Everything else, ranked by whether it actually carries this work

| Venue | Does it carry CI/CD / supply-chain work? | Watch |
|---|---|---|
| **arXiv cs.CR** | **Yes, and it lands here first.** Preprints precede the conference by 6-18 months. | ✅ API: `http://export.arxiv.org/api/query?search_query=all:%22software+supply+chain%22&sortBy=submittedDate&sortOrder=descending&max_results=20` (Atom) · ✅ `https://rss.arxiv.org/rss/cs.CR` (RSS 2.0, 50 items, rebuilt daily 04:00 UTC — high volume, heavily AI-weighted right now, filter locally) |
| **ICSE / FSE / MSR / ASE** (software-engineering side) | **Yes — this is where the *empirical* supply-chain work lands**, and it is more useful to us than the security venues because it studies what developers actually do. Kästner's *"Pinning Is Futile"* (FSE 2025), *"Six Million (Suspected) Fake Stars on GitHub"* (ICSE 2026), *"Understanding the Response to Open-Source Dependency Abandonment in npm"* (ICSE 2025, Distinguished Paper). | Proceedings via DBLP; authors via arXiv |
| **NDSS** | **Yes.** *Rethinking Trust in Forge-Based Git Security* (gittuf) — **NDSS 2025, Distinguished Paper Award**; *TAF* — NDSS 2026. | dblp / ndss-symposium.org |
| **IEEE EuroS&P** | **Yes.** *SourceFabric: Consistent and Scalable Security Policies for Git Repositories* — EuroS&P 2026. | dblp |
| **USENIX Security · IEEE S&P · ACM CCS** | **Yes, but sparsely** — a handful of supply-chain papers per year each, and the CI/CD-specific slice is thinner than SCORED's. Worth scanning proceedings once a year rather than following. | USENIX publishes open-access proceedings; **tier: `periodic`** |
| **Black Hat USA / DEF CON** | **Yes, and this is where the offensive CI/CD work gets its audience.** Verified examples: John Stawinski, *"Self-Hosted GitHub Runners: Continuous Integration, Continuous Destruction"* (Black Hat USA 2024) and *"Grand Theft Actions: Abusing Self-Hosted GitHub Runners at Scale"* (DEF CON 32). Adnan Khan's `gato` debuted at **ShmooCon 2023**. | Briefings archives; **the researchers' own sites publish slides faster than the conferences do** — another reason to follow people over venues |
| **OpenSSF Community Days / SOSS** | Practitioner and standards-direction talks, not novel attack research. Now the host for SCORED. | `https://openssf.org/feed/` |
| **Reproducible Builds Summit** | Small, technical, unusually approachable. **2026: Gothenburg** (announced 2026-08-12). | `https://reproducible-builds.org/blog/index.rss` |
| **SupplyChainSecurityCon** (LF Open Source Summit track) | Industry/standards talks. ⚠️ **Not independently verified in this pass.** | — |

**The practical conclusion on venues:** for this field specifically, **conference proceedings are a lagging indicator and personal blogs are the leading one.** Every major CI/CD attack class in §1 was published on a personal or vendor blog *first*, sometimes years before any peer-reviewed treatment. Weight the follow list accordingly.
### 5.3 Practitioner channels — where things surface fastest

Ranked by how often they are *first*.

| Channel | Owner | What it produces | Feed | Cadence | Tier |
|---|---|---|---|---|---|
| **StepSecurity blog** | StepSecurity | **The single fastest public source for CI/CD-specific supply chain incidents.** Verified sample from 2026-08: "ChainDrop npm Worm: Bun-loaded CI/CD credential harvester with Ethereum dead-drop C2" (08-16), "Rust Supply-Chain Attack: arrayref, internment, and append-only-vec Poisoned by the proc-macro1 Build-Time Dropper" (08-22), "The State of Open Source Supply Chain Attacks" (08-23). They run runner-level egress telemetry, so they see attacks in-flight. | **verified RSS**: `https://www.stepsecurity.io/blog/rss.xml` | Multiple per week | `core` |
| **GitHub Actions changelog** | GitHub | Product-side ground truth: what the platform now does. Verified entries include **"GitHub Actions holds potentially malicious workflows for approval" (2026-07-28)** and "Reference same-repository actions with self-repository syntax" (2026-07-30) — both directly change the attack surface git-serious models. | **verified RSS 2.0**: `https://github.blog/changelog/label/actions/feed/` (label-scoped — much higher signal than the unfiltered `https://github.blog/changelog/feed/`) | ~2-6/month for the Actions label | `core` |
| **GitHub Security Lab advisories** | GitHub | GHSL-numbered advisories from GitHub's own offensive research team. | **verified Atom**: `https://securitylab.github.com/advisories/feed.xml` | Batched, ~monthly | `core` |
| **oss-security (openwall)** | Openwall | The disclosure list of record for open-source vulnerabilities and, increasingly, ecosystem/process arguments. Verified live: 34,048 messages, most recent 2026-08-27 including *"Reporter attribution is absent from GitHub's machine-readable vulnerability records, and from the NVD entirely"* — the kind of meta-discussion that tells you where the data you depend on is weak. | Archive https://www.openwall.com/lists/oss-security/ — **no RSS found on the archive page.** Subscribe by email via the Openwall list instructions (`oss-security-subscribe@lists.openwall.com`, **address pattern unverified — confirm on the page before use**). | Daily | `core` |
| **tl;dr sec** | **Clint Gibler** — note: issue #332 states he **joined OpenAI to lead Cyber efforts** (previously Semgrep). **Flagged: affiliation change reported in-newsletter, not independently verified.** | Weekly curated AppSec/cloud/supply-chain digest, ~90k subscribers. The highest-leverage single subscription for keeping peripheral vision. | **verified RSS**: `https://rss.beehiiv.com/feeds/xgTKUmMmUm.xml` (most recent issue #342, 2026-08-20) | Weekly | `core` |
| **Trail of Bits blog** | Trail of Bits | Deep engineering security research; historically the home of a lot of packaging/PyPI/Actions work. | **verified RSS 2.0**: `https://blog.trailofbits.com/feed/` | ~4-8/month | `core` |
| **Datadog Security Labs** | Datadog | See §6.1. | **verified RSS 2.0**: `https://securitylabs.datadoghq.com/rss/feed.xml` | ~4-6/month | `core` |
| **Wiz blog** | Wiz | See §6.1. High marketing-to-research ratio — filter. | **verified RSS 2.0**: `https://www.wiz.io/feed/rss.xml` | Near-daily | `periodic` |
| **CloudSecList** | Marco Lancini | Weekly (Sundays) hand-curated cloud security newsletter, 300+ issues over 7 years, ~12k subscribers. Consistently surfaces CI/CD and cloud-identity items. | https://www.cloudseclist.com/ — **no RSS feed found on the site; email only.** | Weekly | `periodic` |
| **Open Source Security Podcast** | **Josh Bressers** (Kurt Seifried not currently listed as co-host — **flagged as changed**) | Weekly-ish conversation on OSS security process, CVE/advisory politics, and ecosystem governance. Recent: "CVEs vs Advisories with Paul Asadoorian" (2026-08-24). Strong on the *meta* layer — how vulnerability data itself is produced. | **verified feed list** at https://opensourcesecurity.io/feeds/ → RSS: `https://opensourcesecuritypodcast.libsyn.com/rss` | Weekly | `periodic` |
| **LWN.net** | LWN | Kernel + distro engineering journalism, with reliable weekly security coverage and unusually good reporting on build/packaging politics. Subscription-supported; worth paying for. | **verified RSS 2.0**: `https://lwn.net/headlines/newrss` | Daily | `periodic` |
| **Sigstore blog** | Sigstore project | Project-direction announcements. Verified cadence is **low** — most recent posts 2026-06-28 ("sigstore.dev and Rekor evolution"), 2026-04-01, 2025-10-08. Use the GitHub release feeds instead for change detection. | feed: `https://blog.sigstore.dev/index.xml` (**verified as the declared feed URL**; note `/feed.xml` and `/rss.xml` both 404) | ~quarterly | `periodic` |
| **Praetorian blog** | Praetorian | Offensive research. **Honest note:** the verified recent feed content (Jul 2026) is BLE tooling and kernel fuzzing — **the GitHub Actions research lineage that made Praetorian famous here has moved with the researchers.** Follow the people, not this blog, for CI/CD. | `https://www.praetorian.com/blog/feed/` (**verified RSS 2.0**) | ~2-4/month | `context` |
| **Chainguard blog** | Chainguard | Moved: `blog.chainguard.dev/rss/` now 301-redirects to `https://www.chainguard.dev/unchained`. **Feed URL for the new location is unverified.** | see above | ~weekly | `periodic` |
| **Aqua "Nautilus"** | Aqua Security | Container/cloud-native threat research; historically published notable Actions/artifact research. **Honest note:** we could not confirm from https://www.aquasec.com/blog/ that the Nautilus brand is still in use, and no RSS URL was visible on the index. **Unverified.** | — | Unknown | `context` |
## 6. Adjacent-but-critical voices

These are not "CI/CD security" people by title, but they are the ones who are holding the pager when a CI/CD incident actually happens — because CI/CD compromises almost always *manifest* as a poisoned package, a leaked credential, or an unreproducible artifact.

### 6.1 Package-registry and dependency-attack research

| Who | Affiliation (verified 2026-08-27) | Signal | Follow | Cadence | Tier |
|---|---|---|---|---|---|
| **Feross Aboukhadijeh** + Socket research team | Founder/CEO, **Socket** (GitHub profile: `@SocketDev`) | Highest-volume malicious-package disclosure in npm/PyPI/VS Code-extension ecosystems. Recent posts cover Open VSX malware campaigns and cross-registry extension malware. | https://socket.dev/blog — **no RSS link found on the blog index; treat as no machine-readable feed until confirmed.** | Several posts/week | `core` |
| **Datadog Security Labs** | Datadog | Deep, technical, vendor-neutral-feeling writeups. Published **"Worm compromises hundreds of popular npm packages" (2026-08-04)** — i.e. they are on the current npm-worm class. | **RSS verified:** `https://securitylabs.datadoghq.com/rss/feed.xml` (valid RSS 2.0) | ~4-6/month | `core` |
| **Wiz Research** | Wiz | Fast incident analysis with cloud-blast-radius framing. Published **"Rust Supply Chain Attack on arrayref: Significant Overlap with DPRK Campaigns" (2026-08-20)** and **"Version Control DFIR: a Cheatsheet to GitHub, GitLab, Bitbucket, and Azure DevOps" (2026-08-27)** — the latter is directly, unusually on-topic for git-serious. | **RSS verified:** `https://www.wiz.io/feed/rss.xml` (valid RSS 2.0) | Near-daily (mixed product + research) | `core` (filter aggressively — much of the feed is product marketing) |
| **StepSecurity** | StepSecurity | See §5. The fastest public disclosure channel for *CI-specific* supply chain attacks. | **RSS verified:** `https://www.stepsecurity.io/blog/rss.xml` | Multiple/week | `core` |
| **Phylum** | **DEAD / MOVED — flagged.** `blog.phylum.io` now fails TLS (certificate resolves to a Fastly fallback), i.e. the host is no longer served. Phylum was reported acquired by Veracode; **we could not verify where, or whether, that research team now publishes.** Do not carry Phylum forward as a live source without re-checking. | — | — | — | `context` |
| **ReversingLabs / Sonatype / Endor Labs / JFrog / Snyk Labs / Checkmarx** | Various vendors | Annual "state of the software supply chain" style reports plus episodic malicious-package findings. **Not individually verified in this pass** — a sibling vendor review covered these companies commercially. | Vendor blogs; annual reports | Annual + episodic | `periodic` |
| **Alex Birsan** (dependency confusion, 2021) | **UNVERIFIED — current activity unknown.** His 2021 Medium writeup defined the dependency-confusion class; we found no evidence in this pass of ongoing publication. | Historic, foundational | — | Dormant | `context` |
| **OSV / OSV-Scanner (Google OSS Security Team)** | Google | The machine-readable vulnerability layer the whole ecosystem now reads: OSV schema `ossf/osv-schema` (v1.9.0, 2026-08-06), `google/osv.dev` (last push 2026-08-27), `google/osv-scanner` (v2.5.1, 2026-08-17, 10.9k stars). | API at https://api.osv.dev/ ; releases atom `https://github.com/google/osv-scanner/releases.atom` | Continuous | `core` (as data + as a tool git-serious will sit next to) |

### 6.2 Reproducible-builds and build-integrity practitioners

- **Reproducible Builds core team** — Chris Lamb, Holger Levsen, Vagrant Cascadian are the long-standing names; **we verified the project's output cadence but not each individual's current role.** The monthly report (§4.8) is the aggregate signal and is better than following individuals.
- **`diffoscope`** — the in-depth artifact-diffing tool; its release stream is a good proxy for "new classes of build nondeterminism found." Watch `https://salsa.debian.org/reproducible-builds/diffoscope` (GitLab; **Atom availability unverified**).
- **Kees Cook** — kernel self-protection / build hardening. GitHub profile lists no employer (Aug 2026); Mastodon `https://hachyderm.io/@kees`. He was a "Supporter spotlight" subject on the Reproducible Builds blog (2024-09-29). Tier: `context`.

### 6.3 Non-human identity, secrets, and credential research

This is the category that most reliably intersects CI/CD incidents: nearly every public CI/CD compromise ends with "…and then it exfiltrated the credentials in the runner environment."

| Who | Affiliation | Signal | Follow | Cadence | Tier |
|---|---|---|---|---|---|
| **Truffle Security** — Dylan Ayrey, Joe Leon, Luke Marshall, Zach Rice, Ian Sharpe, Haoxi Tan, Miccah Castorina (author list verified from the blog, 2026-08-27) | Truffle Security | Secret-exposure research at scale. Recent: **"768 Leaked Corporate AWS Keys Held Full Admin Rights" (2026-08-19)**, "API Keys Leaking in PNG Metadata of AI Images" (2026-08-13), "Scanning 7.6 Petabytes of HuggingFace Training Data for Secrets" (2026-06-01, Dylan Ayrey). | https://trufflesecurity.com/blog — **no RSS URL found on the page; unverified whether one exists.** TruffleHog repo: `github.com/trufflesecurity/trufflehog` (releases.atom is a good change signal) | 2-4/month | `core` |
| **GitGuardian** — "State of Secrets Sprawl" annual report | GitGuardian | The canonical dataset on how many secrets are committed to public/private repos per year, with CI-specific breakdowns. **⚠️ The 2026 report URL we tried returned HTTP 403 — the report's existence and URL for 2026 are UNVERIFIED.** The series itself is well established (2022-2025). | https://www.gitguardian.com/state-of-secrets-sprawl (verify path before citing) | Annual (usually Q1) + a regular blog | `periodic` |
| **Astrix / Entro / Aembit / Clutch (NHI vendors)** | Various | "Non-human identity" as a category label. **Not verified in this pass**; a sibling vendor review covers them commercially. The category matters to us because a CI runner *is* a non-human identity with a short-lived OIDC token, and that framing is how buyers will describe the problem. | — | — | `context` |
| **Cloud Security Alliance NHI working group** | **UNVERIFIED — we did not confirm this group exists.** Do not cite without checking. | — | — | — | `context` |

### 6.4 Incident cataloguing — a field with no maintained source

Two candidate catalogs, both dead or frozen:

- **IQT Labs `software-supply-chain-compromises`** — `github.com/IQTLabs/software-supply-chain-compromises`. **Archived read-only since 2022-09-20.** A CSV of publicly reported compromises. Historically useful, no longer maintained.
- **CNCF Catalog of Supply Chain Compromises** — frozen inside the archived `cncf/tag-security` repo since 2025-12-18 (§4.3). No announced successor.

**This is a real hole in the field** — see §9.1.
---

# SYNTHESIS

## 7. The ranked follow list — 20 sources

If we read nothing else, this keeps us within reach of the field. The ranking logic, stated plainly:

- **Ranks 1-6 are the incident and attack-class layer.** These tell us what is *newly possible*. They are ranked highest because git-serious's core claim is that it sees things in CI/CD that other tools miss — and that claim decays fastest if the attack surface moves without us.
- **Ranks 7-12 are the platform and enforcement layer.** These tell us what *changed underneath us* — GitHub's behaviour, the linters' rules, the registries' controls.
- **Ranks 13-17 are the standards and regulatory layer.** These tell us what customers will be *asked for*.
- **Ranks 18-20 are the corrective layer** — the sources most likely to tell us we are wrong.

| # | Source | Why this rank | Feed | Cadence |
|---|---|---|---|---|
| **1** | **StepSecurity blog** | The fastest public CI/CD incident channel that exists, because they run runner-level telemetry and see attacks in flight. They found tj-actions. If something is happening right now, it is here first. | ✅ `https://www.stepsecurity.io/blog/rss.xml` | multiple/week |
| **2** | **Adnan Khan** | More of the modern attack canon traces to him than to anyone else — cache poisoning, self-hosted runner takeover, and now AI-agents-in-CI. Low volume, and every post is a class. | ✅ `https://adnanthekhan.com/rss.xml` | 4-6/yr |
| **3** | **`zizmor` releases** | The living taxonomy. New audit rules ship in releases; each new rule is the field deciding a technique is real and checkable. Effectively a machine-readable changelog of the CI/CD attack surface. | ✅ `https://github.com/zizmorcore/zizmor/releases.atom` | every 1-2 weeks |
| **4** | **Boost Security Labs** | The most novel *new-class* research of the last 12 months — deployment poisoning, OIDC subject-claim confusion, Trusted-Publishing branch scoping. Plus LOTP and poutine. | ✅ `https://labs.boostsecurity.io/rss.xml` | 1-2/month |
| **5** | **GitHub Actions changelog (label-scoped)** | The platform changes under our pipelines. Verified examples: workflow-approval holds for suspicious runs, self-repository `uses:` syntax. Every entry can invalidate a detection. | ✅ `https://github.blog/changelog/label/actions/feed/` | 2-6/month |
| **6** | **John Stawinski IV** | The PyTorch/TensorFlow demonstrations, CodeQLEAKED, and now the sharpest work on AI coding agents wired into CI — the direction the next wave is coming from. | ✅ `https://johnstawinski.com/feed/` (poll the feed; the site root 403s) | 3-5/yr |
| **7** | **Datadog Security Labs** | Home of the canonical OIDC trust-policy research (Tafani-Dereeper) and of population-level measurement (38% of orgs have a vulnerable workflow). Deep and vendor-neutral in tone. | ✅ `https://securitylabs.datadoghq.com/rss/feed.xml` | 4-6/month |
| **8** | **William Woodruff's blog** | Where the argument about *what the controls actually mean* happens — "You shouldn't trust Trusted Publishing", "Actions needs OIDC audience constraints". Shapes how we should talk to customers. | ✅ `https://blog.yossarian.net/feed.xml` | ~monthly |
| **9** | **tl;dr sec** | The single highest-leverage subscription for peripheral vision — one weekly digest that catches most of what the specific feeds miss. | ✅ `https://rss.beehiiv.com/feeds/xgTKUmMmUm.xml` | weekly |
| **10** | **Wiz blog** | Fast incident analysis with blast-radius framing, plus Rami McCarthy. High marketing ratio — filter hard. | ✅ `https://www.wiz.io/feed/rss.xml` | near-daily |
| **11** | **Rami McCarthy / High Signal Security** | Live incident microsites and small purpose-built tools rather than one-shot posts. Consistently useful. | ✅ `https://ramimac.me/feed.xml` | weekly-biweekly |
| **12** | **GitHub Security Lab advisories** | GHSL-numbered advisories from GitHub's own offensive team. **Use the advisories feed — the top-level `feed.xml` is an empty stub.** | ✅ `https://securitylab.github.com/advisories/feed.xml` | batched, ~monthly |
| **13** | **OpenSSF blog** | Standards direction, and currently the best practical translator of the EU CRA into engineering terms. | ✅ `https://openssf.org/feed/` | 2-6/week |
| **14** | **Unit 42** | The Cider Security lineage — Avital, Gil, Greenholts, Hahami, Moore. Filter on those names; the feed is mostly threat intel. | ✅ `https://unit42.paloaltonetworks.com/feed/` | daily (filter) |
| **15** | **Reproducible Builds monthly report** | One subscription, monthly, and its "scholarly papers" section is a free human-curated academic filter for this exact sub-field. Punches far above its cost. | ✅ `https://reproducible-builds.org/blog/index.rss` | monthly |
| **16** | **oss-security (Openwall)** | The disclosure list of record, and where meta-arguments about the *vulnerability data we depend on* happen. | archive `https://www.openwall.com/lists/oss-security/` — **no RSS**; email subscription | daily |
| **17** | **PyPI blog + Seth Larson** | The best-documented registry security programme, and the fastest registry-side incident reporting. Two feeds, both bylined. | ✅ `https://blog.pypi.org/feed_rss_created.xml` · ✅ `https://sethmlarson.dev/feed` | 1-3/month each |
| **18** | **arXiv supply-chain query** | Where the corrective literature lands first — Kästner's *"Pinning Is Futile"*, the Williams/Kästner trust-signal-collapse papers. The papers most likely to tell us a control we recommend does not work. | ✅ `export.arxiv.org/api/query?...` (see §5.2) | continuous |
| **19** | **Synacktiv publications** | Hugo Vincent's exploitation series and `octoscan` — a second, independent offensive lens on the same surface. | ✅ `https://www.synacktiv.com/en/feed/lastblog.xml` | episodic |
| **20** | **Trail of Bits blog** | Where the structural fixes get designed (Trusted Publishing) rather than the attacks found. | ✅ `https://blog.trailofbits.com/feed/` | 4-8/month |

**Honourable mentions, deliberately not in the top 20:** Sigstore blog (only ~quarterly — the release feeds carry the signal instead) · SLSA `tags.atom` (a few releases a year, but each one matters) · Scorecard releases (2-4/yr and slowing) · `linux-cve-announce` (indispensable *as data*, unreadable *as a feed*) · CloudSecList and the Open Source Security Podcast (both good, both weekly, both largely subsumed by tl;dr sec).

---

## 8. The machine-pollable subset

Exact URLs, formats, and the traps. **Everything marked ✅ was fetched during this research and returned real content.** This section is written for a scheduled job, so the failure modes matter as much as the URLs.

### 8.1 RSS / Atom feeds — verified live

**Attack research and incidents**
```
https://www.stepsecurity.io/blog/rss.xml              RSS 2.0   multiple/week
https://adnanthekhan.com/rss.xml                      RSS 2.0   4-6/yr
https://johnstawinski.com/feed/                       RSS 2.0   3-5/yr   (site root 403s; feed is fine)
https://labs.boostsecurity.io/rss.xml                 RSS 2.0   1-2/month  (per-author bylines)
https://securitylabs.datadoghq.com/rss/feed.xml       RSS 2.0   4-6/month
https://www.wiz.io/feed/rss.xml                       RSS 2.0   near-daily
https://www.wiz.io/blog/rss.xml                       RSS 2.0   (per-item <author> tags)
https://ramimac.me/feed.xml                           Atom      weekly-ish  (/rss.xml and /index.xml 404)
https://unit42.paloaltonetworks.com/feed/             RSS 2.0   daily, bylined — filter on names
https://www.synacktiv.com/en/feed/lastblog.xml        XML       episodic  (/en/feed and /feed both 403)
https://www.legitsecurity.com/blog/rss.xml            XML       marketing-diluted
https://www.aikido.dev/blog/rss.xml                   RSS 2.0   daily-weekly, mixed
https://blog.aquasec.com/rss.xml                      RSS       weekly  (www.aquasec.com/feed/ 403s)
https://www.praetorian.com/blog/feed/                 RSS 2.0   2-4/month
https://blog.trailofbits.com/feed/                    RSS 2.0   4-8/month
```

**Platform, standards, and registries**
```
https://github.blog/changelog/label/actions/feed/     RSS 2.0   ← Actions-scoped; far better S/N than the unfiltered changelog
https://github.blog/changelog/feed/                   RSS 2.0   ROLLING 10-ITEM WINDOW — poll ≥daily or you lose entries
https://github.blog/security/feed/                    RSS 2.0
https://github.blog/tag/github-security-lab/feed/     RSS 2.0   bylined via dc:creator
https://securitylab.github.com/advisories/feed.xml    Atom      batched bursts
https://openssf.org/feed/                             RSS 2.0   2-6/week
https://slsa.dev/feed.xml                             Atom
https://blog.sigstore.dev/index.xml                   XML       ~quarterly  (/feed.xml and /rss.xml 404)
https://blog.pypi.org/feed_rss_created.xml            RSS 2.0   bylined  (/feed.xml and /index.xml 404)
https://sethmlarson.dev/feed                          Atom
https://blog.rubygems.org/atom.xml                    Atom      ~weekly, UNBYLINED
https://blog.packagist.com/rss/                       RSS       2-4/month
https://blog.rust-lang.org/feed.xml                   Atom
https://rustfoundation.org/feed/                      RSS       (feed.xml 404s; domain moved from foundation.rust-lang.org)
https://reproducible-builds.org/blog/index.rss        RSS 2.0   monthly, reliably
https://people.kernel.org/monsieuricon/feed/          RSS       1-2/YEAR  (feed.atom and .rss 404)
https://www.kernel.org/feeds/kdist.xml                RSS 2.0   canonical kernel release feed, sub-hour latency
https://lore.kernel.org/linux-cve-announce/new.atom   Atom      DOZENS/DAY — see trap 8.4
https://lwn.net/headlines/newrss                      RSS 2.0   daily
https://rss.beehiiv.com/feeds/xgTKUmMmUm.xml          RSS       weekly (tl;dr sec)
https://opensourcesecuritypodcast.libsyn.com/rss      RSS       weekly
https://rss.arxiv.org/rss/cs.CR                       RSS 2.0   50 items, rebuilt daily 04:00 UTC
```

### 8.2 GitHub release/tag feeds — change signals for the load-bearing projects

```
https://github.com/zizmorcore/zizmor/releases.atom                    every 1-2 weeks  ← highest value
https://github.com/AdnaneKhan/gato-x/releases.atom
https://github.com/boostsecurityio/poutine/releases.atom              every 1-2 months
https://github.com/step-security/harden-runner/releases.atom
https://github.com/ossf/scorecard/releases.atom                       2-4/yr, slowing
https://github.com/slsa-framework/slsa/tags.atom                      ⚠️ USE TAGS — releases.atom is permanently empty
https://github.com/theupdateframework/specification/releases.atom     re-activated: 3 releases in 2026
https://github.com/theupdateframework/python-tuf/releases.atom        ~annual majors, breaking
https://github.com/in-toto/attestation/releases.atom                  1-2/yr, each meaningful
https://github.com/in-toto/in-toto/releases.atom                      near-dormant
https://github.com/sigstore/cosign/releases.atom                      parallel v2 + v3 lines
https://github.com/sigstore/rekor/releases.atom                       every 4-8 weeks
https://github.com/sigstore/sigstore-go/releases.atom                 ~monthly
https://github.com/google/osv-scanner/releases.atom
https://github.com/CycloneDX/specification/releases.atom
https://pypi.org/rss/project/b4/releases.xml
https://pypi.org/rss/project/patatt/releases.xml
```

### 8.3 Structured data — APIs and datasets, not feeds

These are the ones a research job can *join against*, not just read.

| Source | Endpoint | Format | Why it is worth ingesting |
|---|---|---|---|
| **Living Off The Pipeline** | `https://boostsecurityio.github.io/lotp/api.json` | JSON array | ⭐ **The most directly ingestible dataset found.** `name`, `url`, `tags` (`cli`/`config-file`/`eval-sh`/`eval-js`/`env-var`/`input-file`), `refs`, `html`, `meta{files, sinks, purl}`. Maps *"tool present in a pipeline"* → *"known code-execution sink."* ~50+ entries. |
| **zizmor's bibliography** | `https://raw.githubusercontent.com/zizmorcore/zizmor/main/docs/audits.md` | Markdown, 87 link-refs | ⭐ The field's annotated bibliography, maintained. `grep -oE '^\[[^]]+\]: https?://[^ ]+'`. **Use this to seed and re-seed the source list itself.** |
| **CISA KEV** | `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` | JSON | ✅ Live: `catalogVersion 2026.08.26`, `count: 1682`. Updated most weekdays. CSV sibling at `/csv/known_exploited_vulnerabilities.csv` (**pattern unverified**). |
| **OSV** | `https://api.osv.dev/` · schema `ossf/osv-schema` (v1.9.0) | JSON API | The machine-readable vulnerability layer the whole ecosystem reads. |
| **DBLP** | `https://dblp.org/pid/<PID>.xml` | XML/JSON | Durable author-publication spine. Verified PIDs: Cappos `27/5136`, Torres-Arias `185/1711`, Moore `236/5493`, Kuppusamy `44/8573`. |
| **arXiv API** | `http://export.arxiv.org/api/query?search_query=all:%22software+supply+chain%22&sortBy=submittedDate&sortOrder=descending&max_results=20` | Atom | ✅ Verified — this is how we surfaced the 2026-08-21 Williams/Kästner trust-signal papers. |
| **OpenSSF Best Practices Badge** | `https://www.bestpractices.dev/projects.json?pq=<query>` | JSON | ✅ Live endpoint (returns `[]` on no match). |
| **CNCF TAG roster** | `https://github.com/cncf/toc/blob/main/tags.yaml` | YAML | ✅ **The freshest people-map in the ecosystem** — chairs and tech leads with term dates. Watch this file to track personnel movement. |
| **in-toto steering** | `https://github.com/in-toto/community/blob/main/STEERING-COMMITTEE.md` | Markdown | ✅ Last commit 2026-07-06 — the most current governance file found anywhere. Tracked three affiliation moves that faculty pages and TUF's own maintainer file missed. |
| **Sigstore calendar** | `https://calendar.google.com/calendar/ical/fq4kgom2ce43hncnbcfja2ck20%40group.calendar.google.com/public/basic.ics` | iCal | Machine-readable meeting schedule. |
| **MITRE CNA list** | `CNAsList.json` (CVE Project) | JSON | ✅ Used here to verify the kernel CNA (`CNA-2024-0016`). Useful for "who assigns CVEs for X." |

### 8.4 Traps a naive poller will fall into — **read this before writing the job**

1. ⚠️ **`https://securitylab.github.com/feed.xml` returns HTTP 200 and valid Atom with ZERO entries.** A health check based on status code and parseability will report it green forever. Use `/advisories/feed.xml`.
2. ⚠️ **`https://github.com/slsa-framework/slsa/releases.atom` returns 200 and will never fire** — the repo has no GitHub Releases. Use `tags.atom`.
3. ⚠️ **lore.kernel.org is selectively behind Anubis anti-bot.** Plain `/<list>/new.atom` serves fine; **HTML archive pages and all query endpoints return a JS challenge with HTTP 200 and zero entries.** The obvious optimisation — public-inbox query-scoped Atom (`?q=f:gregkh...&x=A`) to filter a firehose down to one sender — **silently returns nothing.** Ingest the full feed and filter locally.
4. ⚠️ **`https://github.blog/changelog/feed/` is a rolling 10-item window.** Poll at least daily or entries are lost permanently.
5. ⚠️ **Cloudflare / 403 walls:** Socket (`/rss.xml` 403), `www.aquasec.com/feed/` (403 — use `blog.aquasec.com/rss.xml`), `synacktiv.com/feed` and `/en/feed` (403 — use `/en/feed/lastblog.xml`), `johnstawinski.com` root (403 — the feed is fine), `checkmarx.com/feed/` (403 on HEAD, 200 on GET), CISA HTML pages (403 — the JSON feed works). **Send a browser-like User-Agent, and prefer GET over HEAD for liveness checks.**
6. ⚠️ **Feed URLs that look canonical but 404:** `blog.sigstore.dev/feed.xml` and `/rss.xml` · `blog.pypi.org/feed.xml` and `/index.xml` · `blog.rubygems.org/feed.xml` and `/index.xml` · `rustfoundation.org/feed.xml` · `ramimac.me/rss.xml` and `/index.xml` · `people.kernel.org/monsieuricon/feed.atom` and `/feed.rss` · `boostsecurity.io/blog/rss.xml` (moved to `labs.boostsecurity.io`) · `flatt.tech/research/feed.xml`. **Do not guess feed URLs by convention — read the page's `<link rel="alternate">`.**
7. ⚠️ **Redirects that change host:** `blog.chainguard.dev/rss/` → `chainguard.dev/unchained` (new feed URL **unverified**); `boostsecurity.io/blog/*` → `labs.boostsecurity.io/*`; `foundation.rust-lang.org` → `rustfoundation.org`.
8. ⚠️ **Link rot is real in this field.** Aqua has pruned older Nautilus research URLs *with no Wayback snapshot*. **Archive the content, not just the URL** — for anything we cite, keep a local copy.
9. ⚠️ **Google Scholar is not fetchable at all** — every automated request redirects to a login wall. Use DBLP and arXiv.
---

## 9. Gap statement — where the field has no good public signal

These are not gaps in our research. They are gaps in the field, and several of them are opportunities.

### 9.1 ⭐ There is no maintained public catalogue of supply-chain compromises

**This is the largest and most surprising hole.** Both candidate catalogues are dead:

- **CNCF Catalog of Supply Chain Compromises** — the best-known curated list, led by Santiago Torres-Arias. **Stranded read-only** in `cncf/tag-security` since the repo was archived **2025-12-18** in the CNCF TAG restructure. Only the `security-assessments` subproject carried over into TAG Security and Compliance. **No successor has been announced.**
- **IQT Labs `software-supply-chain-compromises`** — a CSV dataset of publicly reported compromises. **Archived read-only since 2022-09-20.**

So at the exact moment the incident rate is highest — tj-actions, Shai-Hulud 1.0 and 2.0, s1ngularity/Nx, TeamPCP, ChainDrop, the Rust `arrayref` dropper, all within ~18 months — **the field has no shared, machine-readable, maintained incident record.** Everyone reconstructs the timeline from vendor blogs.

**What we would have to do to close it:** either maintain one ourselves (a real contribution, and a natural fit for a product that already models CI/CD entities and relationships — this is arguably a *dataset* git-serious is uniquely positioned to build), or ask TAG Security and Compliance directly whether the catalogue has a planned home. The second is a cheap email; the first is a genuine standing asset and a legitimate reason for the field's core people to talk to us.

### 9.2 The canonical taxonomy has no maintainer

The OWASP Top 10 CI/CD Security Risks is frozen at **v1.0, October 2022**; its content repo has had **no commit since 2023-01-18**. It is nonetheless the vocabulary buyers use. There is no public signal for "the taxonomy is being updated" because nobody is updating it.

The de facto replacement — `zizmor`'s 41 audit rules — is *a linter's rule list*, not a taxonomy: it has no severity model, no threat model, no numbering customers can cite in a compliance document, and it is Actions-centric. **The gap between "what buyers can name" and "what attackers actually do" is currently about four years wide, and nobody owns closing it.** To hear about a v2 we would have to ask Omer Gil or Ory Segal directly.

### 9.3 Non-GitHub CI/CD is nearly invisible

Essentially the entire public research corpus is GitHub Actions. Verified exceptions are thin: Adnan Khan on **Google Cloud Build**, Stawinski on **Jenkins agents**, Praetorian's **Trajan** covering GitLab CI / Azure DevOps / Jenkins, and Boost's `poutine` being multi-platform by design. There is **no equivalent of Lobačevski's pwn-request series for GitLab, Azure DevOps, Jenkins, Buildkite, CircleCI, or Tekton.** If a customer runs GitLab, we cannot point them at a public canon, because there isn't one. **To hear from this space we would have to generate the research ourselves or commission it** — and it is a genuine differentiation opportunity.

### 9.4 Self-hosted runner incidents are structurally unreportable

Self-hosted-runner takeover is the highest-severity class in the canon, and it happens **inside private infrastructure** — so there is no public disclosure channel at all. The public record consists of a handful of researcher-run demonstrations against open-source projects (PyTorch, TensorFlow). **We have no way to know the real base rate.** Only a vendor with runner-level telemetry can see it, which currently means StepSecurity's aggregate posts and nothing else. **The honest position is that our own deployments would be the primary evidence source, and that is worth saying out loud rather than implying we know the prevalence.**

### 9.5 Individual attribution is dissolving at vendor research arms

Checkmarx, Cycode, Socket and increasingly Sysdig have moved to collective "Research Team" bylines. We could not verify individual researchers at any of them from primary sources. This matters because **you cannot follow a team when it changes employer, and in this field people move constantly** (see §2.0). The mitigation is to track *techniques* and their citations — which is exactly what zizmor's bibliography gives us — rather than tracking company blogs.

### 9.6 Several specific unknowns we did not close

Stated plainly so they are not mistaken for verified facts:

| Unknown | Why it matters | What it would take |
|---|---|---|
| **CISA Secure by Design status** — `cisa.gov` 403s to our fetcher, and there were widely-reported programme changes in 2025 | It is cited in procurement conversations | A manual browser visit, or ask someone in the OpenSSF policy orbit |
| **Whether the Secure Software Development Attestation Form is still in force** | Directly affects US federal-adjacent customers | Same |
| **NIST CSRC's exact publications RSS URL** — advertised in the footer but not resolvable from page content | SSDF v1.2 and the DevSecOps draft are both open right now | Manual check; fall back to the "Drafts open for comment" page |
| **Daniel Krivelevich's and Ory Segal's current roles** | They own the taxonomy in 9.2 | Direct contact |
| **Alvaro Muñoz's current affiliation** | He built CodeQL's Actions analysis | Direct contact |
| **Benoit Baudry's institution** — his site returned 502 + a TLS name mismatch | Build-reproducibility research | Manual check |
| **SCORED '26 chair names** — not published on the site | Deciding whether to attend / submit | Email `scored26-chairs@googlegroups.com` |
| **Where Phylum's research team landed post-Veracode** — `blog.phylum.io` no longer resolves to a valid cert | Was a real malicious-package research source | Ask, or write it off |
| **Chainguard's post-migration feed URL** | Billy Lynch's impostor-commit work lives there | Read `chainguard.dev/unchained` page source |

### 9.7 What has *no* feed at all, and must be watched by repo or by hand

- **in-toto** (project-level), **TUF and the TAP process**, **Scorecard** (project-level) — all ride other channels. Watch the repos.
- **OWASP CI/CD Top 10** — no feed; watch the repo (which is not moving anyway).
- **Marcela Melara's site**, **Mike Fiedler's personal site**, **Justin Cappos / NYU SSL**, **Santiago Torres-Arias**, **Laurie Williams**, **Christian Kästner**, **Martin Monperrus** — **no academic in this map publishes an RSS feed.** Use DBLP + arXiv + the Reproducible Builds monthly report's scholarly-papers section.
- **SCORED**, **CloudSecList**, **Socket**, **Flatt Security Research**, **git.kernel.org** — no usable feed.
- **oss-security** — no RSS; email subscription only.
## 10. Etiquette and approach notes

For the people and projects we may eventually want to *engage with*, not just read. This community is small, mostly public, and has strong and fairly consistent norms.

### 10.1 The general shape of it

- **Contribution is the currency; introductions are not.** Nobody in this field responds well to "I'd love to pick your brain." They respond to a good bug report, a correct patch, a useful dataset, or a well-posed question that shows you did the reading. The fastest legitimate path into any of these projects is to file one genuinely useful issue.
- **Public by default.** Ask in the project's issue tracker, mailing list, or Slack channel rather than by DM. A private DM to a maintainer asking a question that belongs in public reads as an attempt to extract free consulting. The exception is a security report (below).
- **Meetings are open and attending is normal.** OpenSSF WGs, the SLSA spec meeting, CNCF TAG Security and Compliance, and Sigstore community calls are all public, on published calendars, with public notes. Turning up, listening for a few sessions, and *then* speaking is the standard and well-received path. Do not turn up and pitch.
- **Never pitch a product on a project channel.** This is the fastest way to be permanently discounted. If git-serious has something to say, say it as research or as a contribution. The vendors who are respected here (StepSecurity, Boost, Chainguard, Trail of Bits, Datadog) earned it by publishing findings that were useful *whether or not* you bought anything.

### 10.2 Security reporting specifically

If our own work ever finds a vulnerability in someone's pipeline or project, the norms are strict and worth following exactly:

- Use the project's declared channel. The ones verified in this research: `cve@kernel.org` (kernel), `security@packagist.org` (Composer), GitHub Private Vulnerability Reporting where enabled, `security@` addresses in `SECURITY.md`. For PyPI/crates.io/RubyGems, use the registry's published security policy page, not a public issue.
- **Coordinated disclosure with a real embargo is the expectation**, and 90 days is the common default. Boost Security's deployment-poisoning work is a good model: disclosed to 15+ vendors starting Nov 2025, published Apr 2026.
- **`oss-security` (Openwall) is where multi-project issues get announced**, and posting there has its own etiquette — read a month of the archive before posting. Announcements are plain text, technically dense, no marketing, no logos, no "read more on our blog."
- Do not publish a finding about a specific organisation's pipeline without their consent, ever.

### 10.3 Per-community specifics

- **Linux kernel / kernel.org (Ryabitsev, Greg KH).** Email-only, plain text, no HTML mail, no attachments, reply inline and bottom-post. `b4` exists precisely to make this bearable — use it. Do not subscribe a Gmail address to a high-volume vger list; kernel.org explicitly warns Gmail's rate limits will break it. This community's tolerance for process errors is low but its tolerance for *good-faith technical questions asked correctly* is high.
- **OpenSSF.** Join the Slack (`slack.openssf.org`), lurk in the relevant WG channel, attend the call. The Securing Software Repositories WG (Mike Fiedler, Zach Steindler) is unusually welcoming and is the most relevant room for us. WG output is consensus-driven documents — offering to review a draft is a real and appreciated contribution.
- **CNCF TAG Security and Compliance.** Meetings on the LFX calendar, mailing list `cncf-tag-security-and-compliance@lists.cncf.io`, Slack in cloud-native.slack.com. The Security Assessment subproject (Cappos, Eddie Knight) is a genuine, structured way to contribute substantive work.
- **Academics (Cappos/NYU, Torres-Arias/Purdue, Williams/NC State, Kästner/CMU, Monperrus/KTH).** Email is fine and they generally answer, but the message has to contain something. What academics actually want from industry is **data and access to real practice** — anonymised telemetry, a case study, an interview pool, a validated dataset. If git-serious accumulates real observations about how pipelines are actually configured in the wild, that is a genuinely scarce research asset and a legitimate basis for collaboration. Offering it is far stronger than asking for their time. Note that several of them explicitly recruit industry collaborators for empirical studies.
- **Individual attack researchers (Adnan Khan, the Boost Labs team, Woodruff).** These are practitioners with public writing and public tools. The right approach is to *use the tool, find its rough edge, and file the issue* — a good `zizmor` or `gato-x` or `poutine` issue is worth more than any email. Woodruff in particular is highly active on his own repos and responds to well-formed issues.
- **Reproducible Builds.** IRC/Matrix-centric, long-tenured, quietly welcoming. The annual summit (2026: **Gothenburg**) is small and unusually approachable — if we want one in-person room in this field, that is a strong candidate.

### 10.4 One thing to be careful about

Much of this field is people who are *sceptical of security vendors on principle*, often for good reason. The credibility test is whether you publish things that are true and useful even when they do not help you sell. Our standing filter of naming the risks deliberately left open, rather than implying completeness, happens to be exactly the posture that earns standing here.

---

*Compiled 2026-08-27. Every ✅ feed in this document was fetched and its content confirmed on that date. Every **UNVERIFIED** marker is deliberate: affiliations in this field move faster than the rosters that record them, and a named gap is more useful than a confident guess.*
