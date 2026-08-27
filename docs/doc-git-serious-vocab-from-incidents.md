---
title: Vocabulary from the incident corpus — what 35 compromises require the graph to express
date: 2026-08-27
status: research
audience:
  - developer
  - llm
related_docs:
  - docs/doc-git-serious-cicd-shape-review.md
  - docs/doc-git-serious-cicd-security-prior-art.md
---

> **Research pass, 2026-08-27.** Every documented CI/CD compromise and observable condition mapped to the entities and relationships it requires, with each proposal tested and each gap named.
> One of four gathering passes behind the domain vocabulary corpus, which lives with the
> vocabulary's owner as `spec-github-core-vocabulary.md`. Written by an AI research agent;
> claims carry citations and the report flags what it could not verify. Not canon.

# Vocabulary completeness — derived from 35 incident rows (≈42 incidents) and 40 observable conditions

**Question answered:** for every attack, incident and observable condition the research documented, does
git-serious have a node type and an edge type that can *represent* it? A missing concept means the graph
physically cannot express the thing an operator needs to see.

**Not answered here:** whether the data is collectible with a given credential (§3.9 of the prior art
settles that, and it is carried in the tables as a caveat), and whether a finding should be *emitted*
(that is `compliance_core`, deliberately out of scope for the self milestone).

## 0. Headline

1. The single largest gap is **not** an exotic object — it is the **declared workflow job**. Today
   `github_actions_job` is an *executed* job on a run; there is no node for the job as *written*. Every
   privilege decision in CI (`permissions:`, `runs-on:`, `environment:`, `if:`, which steps see which
   secret) is made at the declared-job level, so hanging `USES_ACTION` / `REFERENCES_SECRET` /
   cache edges off the *workflow* forces every conjunction query into a string join on a `{job}` edge
   property. This is the difference between "shape exists" and "shape is exploitable" for ~20 of the 35
   incident rows.
2. **`actions_cache` is missing entirely** and is demanded by 5 incidents including the two most recent
   and most severe (TanStack 2026-05, Ultralytics, Kong, Angular, Khan's research). It is the textbook
   convergence node: one key written from a low-trust job and restored by a privileged one.
3. **Refs are missing, and `git_branch` is the wrong shape.** Merge branch and tag into one `git_ref`.
   Tag movement (`head_sha` with field history) is the detection for tj-actions, trivy-action and
   actions-cool — 3 incident rows, ecosystem-wide blast radius — and ruleset targeting already speaks
   `branch|tag|push`.
4. **`credential_grant`** (one node, `kind ∈ {fine_grained_pat, classic_pat, deploy_key, oauth_grant,
   registry_token, ssh_key, gpg_key}`) is demanded by 12 incident rows. Splitting it into `pat_grant`
   + `deploy_key` + `oauth_app` gives three thin types and forces a UNION in the one query that matters
   (OWASP SEC-2 verbatim: "map *all* identities ... all methods of programmatic access").
5. The edge **`actions_secret REPRESENTS_CREDENTIAL credential_grant`** turns incident #27's headline
   ("ruleset bypass actor is a bot account whose PAT is stored as a secret") from three disconnected
   facts into one traversal. Cheap, and nothing else in the estate provides it.
6. **`BYPASSES` must be an edge, not a JSON field.** `bypass_actors` as JSON on the ruleset cannot be
   traversed from the actor side, which is exactly what the "who can change `main` without the gate"
   panel (shape review 4.3.2) asks. Keep the raw JSON; derive the edge.
7. **Package / package_version is the highest-count gap (13 incident rows)** and the *absence* of
   `BUILDS_PACKAGE_VERSION` is the finding — "a registry version with no workflow run behind it" is
   how SolarWinds, xz, lottie-player, eslint-config-prettier and Axios all read on the graph.
8. **Nothing new is needed for change-over-time.** Grid entities already carry field-level history and
   provenance; `batch` / `collection_job` already carry the observation. The 2025–26 delta detections
   (tag burst, new runner, new collaborator, new workflow) all fall out of history *on the right node* —
   which is another argument for `git_ref` and `github_action` existing at all.
9. Three proposals should be **rejected or demoted**: `status_check` survives but only as a
   convergence node with an honest `confidence` on `PRODUCES_CHECK`; a `review` node is unnecessary (an
   edge answers SLSA L4); and a per-object "org policy" node is correctly a *property*, exactly because
   nothing points at it — the contrast with `github_ruleset` (which many repos point at) is the cleanest
   illustration of the node test in the whole corpus.
10. Forge-neutral core, confirmed by the kernel pressure test: `repository`, `git_ref`, `git_commit`,
    `pull_request`, `release`, `principal`, `pipeline`/`pipeline_run`/`job`, `package_version`,
    `credential_grant`. Everything else — rulesets, status checks, actions, apps, installations, secrets,
    environments, caches, runner groups — has **no kernel analogue at all**, which is the sharpest
    available evidence for where the `git_core` line should fall.

---

## 1. The test applied

A concept becomes a **node** only if:

| Test | Question |
| --- | --- |
| **T1 identity** | Is there a natural key that is stable across re-collection and survives a re-name of everything around it? |
| **T2 convergence** | Is it referenced from ≥2 independent directions, or by ≥2 different source types? |
| **T3 own history** | Does it change on its own timeline, independently of any parent? |
| **T4 traversal** | Does a question the corpus demands become a *traversal* instead of a string join or a JSON predicate? |
| **T5 cardinality** | Is the population bounded enough to collect, and is there query demand for every member? |

Rule used throughout: **node** requires T1 and (T2 or T3), and is only worth the cost if T4 holds.
Fails T2 and T3 → **property on an existing node**. The fact is about the *pair*, not about either end →
**property on an edge**. Unbounded population with no per-member demand (T5) → do not collect, even if
T1–T4 pass (this is why `step` and "all commits" are rejected).

Applied to the corpus, the rule kills five candidates and creates nine.

---

## 2. Incident × concept matrix

Rows follow §4 of the prior art (35 rows; rows 26, 27 and 31 each bundle 2–3 named incidents, which is
how "42 incidents" and "35 entries" reconcile). Legend:

- **✅** exists today (github_core / identity_core / platform types)
- **○** proposed in the shape review §2.2 (validated below in §4)
- **✗** **MISSING** — neither existing nor proposed
- *(prop)* the concept is correctly a property, not a node — named so the matrix is honest

| # | Incident | Entities the story requires | Relationships the story requires |
| --- | --- | --- | --- |
| 1 | SolarWinds SUNBURST (2019–20) | build host ✅ `github_runner` (+`ephemeral` prop) · release ○ `github_release` · **published artifact ✗ `package_version`** · source revision **✗ `git_commit`** · attestation ✅ reuse `sigstore_core.rekor_log_entry` | run→artifact **✗ `BUILDS_PACKAGE_VERSION`** (its *absence* is the finding) · artifact→attestation ✅ `ATTESTED_BY` |
| 2 | Codecov Bash Uploader (2021) | **declared job ✗ `workflow_job`** · secret ○ `actions_secret` · **remote host ✗ (reuse `computing_core.web_host`)** · step content *(prop on job)* | job→secret ○ `REFERENCES_SECRET` · **job→host ✗ `FETCHES_FROM`** |
| 3 | Travis CVE-2021-41077 (2021) | **third-party CI grant ✗ `credential_grant{oauth_grant}`** · secret ○ · **declared job ✗** · fork run ✅ (`head_repository` prop) | job→secret ○ `REFERENCES_SECRET{trigger_events, fork_reachable}` · account→grant **✗ `HOLDS_CREDENTIAL`** |
| 4 | Heroku/Travis OAuth → npm (2022) | **✗ `credential_grant{oauth_grant}`** · repo ✅ · **✗ `package`/`package_version`** | ○ `HAS_REPO_PERMISSION` · **✗ `GRANTS_ACCESS_TO`** · clone activity ❌ *not observable* (audit log, GHEC) |
| 5 | CircleCI breach (2022–23) | secret ○ `actions_secret` · **✗ `credential_grant`** · app ✅ `github_app` | **✗ `REPRESENTS_CREDENTIAL`** (the "same secret name lives in two systems" fact) · ○ `HOSTS_INSTALLATION` |
| 6 | Dependabot-impersonating commits (2023) | **✗ `git_commit`** (author vs verified signer) · ref ○→**`git_ref`** · ruleset ○ · workflow ✅ · **✗ `credential_grant{classic_pat}`** *(unobservable — name it)* | ○ `ENFORCED_ON` · **✗ `POINTS_AT`** · **✗ `REVIEWED`** (its absence) · ✅ `DEFINES_WORKFLOW` + history |
| 7 | Microsoft 38 TB SAS token (2023) | — *no vocabulary gap*: this is a secret-scanning **finding**, `compliance_core`, not a shape | — |
| 8 | Okta → Cloudflare (2023–24) | **✗ `credential_grant`** (`last_used_at`, `revoked_at`) · **✗ `identity_core.principal`** (service account outside GitHub) · account ✅ | **✗ `HOLDS_CREDENTIAL`** · ○ `HAS_REPO_PERMISSION` |
| 9 | Ledger connect-kit (2023) | **✗ `identity_core.principal`** (npm publisher) · **✗ `package_version`** · account ✅ · org ✅ | **✗ `LINKED_IDENTITY`** (npm identity ↔ GitHub account) · ○ `MEMBER_OF_ORG` (its *absence* is the finding) |
| 10 | PyTorch / TensorFlow / DeepSpeed self-hosted runners (2024) | runner ✅ (`ephemeral`) · **✗ `runner_group`** (`allows_public_repositories`) · **✗ `workflow_job`** (`runs-on`) · pull_request ○ · repo visibility ✅ *(prop)* · fork-PR approval policy *(prop on repo/org)* | ✅ `EXECUTED_ON` · **✗ `REGISTERED_ON`** · **✗ `MEMBER_OF_RUNNER_GROUP`** · ○ `OPENS_PULL_REQUEST` |
| 11 | xz-utils CVE-2024-3094 (2024) | **✗ `git_ref`** (signed tag) · **✗ `git_commit`** (tagged tree) · release ○ (+`assets`) · **✗ `identity_core.principal`** (maintainer key) | ○ `PUBLISHES_RELEASE` · ○ `BUILDS_RELEASE` (**absence** = manual upload = the finding) · ○ `HAS_REPO_PERMISSION` + history ("maintainer added within N months") |
| 12 | Actions cache poisoning research / Cacheract (2024) | **✗ `actions_cache`** · **✗ `workflow_job`** · ref ○→`git_ref` (cache scope) | **✗ `WRITES_CACHE`** · **✗ `RESTORES_CACHE`** |
| 13 | Polyfill.io (2024) | action ○ `github_action` · **✗ upstream `github_repository` as a collected node** (owner, archived, transfer) | **✗ `DEFINED_IN`** (action → its repo) · `owner_login` field history ✅ *once the upstream repo is a node* |
| 14 | ArtiPACKED (2024) | **✗ `actions_artifact`** · **✗ `workflow_job`** · action ○ (`with: persist-credentials`) | **✗ `UPLOADS_ARTIFACT`** · ○ `USES_ACTION{with_keys}` |
| 15 | lottie-player (2024) | **✗ `package_version`** · **✗ `identity_core.principal`** (npm account) · run ✅ | **✗ `BUILDS_PACKAGE_VERSION`** (absence = the finding) |
| 16 | Ultralytics (2024) | **✗ `workflow_job`** (trigger × interpolation × permissions) · **✗ `actions_cache`** · secret ○ (`PYPI_API_TOKEN`) · **✗ `credential_grant{registry_token}`** · **✗ `package_version`** | ○ `REFERENCES_SECRET{trigger_events, reaches_run_block, checks_out_pr_head}` · **✗ `WRITES_CACHE`/`RESTORES_CACHE`** · **✗ `REPRESENTS_CREDENTIAL`** |
| 17 | Rspack / Vant (2024) | as #16 + `issue_comment` trigger *(prop on workflow)* + `author_association` gate *(prop: job `if:`)* | as #16 |
| 18 | Kong Ingress Controller (2024–25) | **✗ per-ref workflow variant (`VARIES_ON`)** — the zombie-workflow class · **✗ `actions_cache`** · secret ○ (CI PAT) · **✗ `credential_grant`** · `default_workflow_permissions` *(prop)* | **✗ `VARIES_ON` (workflow → `git_ref`, `{content_sha, has_privileged_trigger}`)** · ○ `REFERENCES_SECRET` |
| 19 | Bybit / Safe{Wallet} (2025) | **✗ `deployment`** · cloud resource ✅ `aws_core` via `REFERENCES_RESOURCE` · **✗ `principal`** | ○ `DEPLOYS_TO_ENVIRONMENT` · **✗ run→deployment** (absence = "target changed with no run behind it") |
| 20 | SpotBugs → reviewdog → tj-actions → Coinbase (2025) | action ○ · **✗ `git_ref` on the upstream repo (`head_sha` history = the tag move)** · **✗ `git_commit`** (`reachable_from_any_branch=false` = impostor) · secret ○ (bot PAT) · **✗ `credential_grant`** · **✗ `workflow_job`** · pull_request ○ · account ✅ | ○ `USES_ACTION{ref, pin_kind}` · **✗ `DEFINED_IN`** · **✗ transitive `USES_ACTION` (action → action)** · ○ `HAS_REPO_PERMISSION` ("org auto-grants write") · **✗ `REPRESENTS_CREDENTIAL`** |
| 21 | Grafana pwn request (2025) | as #16 (declared job + trigger + interpolation) | as #16 |
| 22 | Salesloft / Drift (2025) | account ✅ · workflow ✅ (+first-seen) · **✗ `git_commit`** (first-time committer) · **✗ `credential_grant{oauth_grant}`** | ○ `HAS_REPO_PERMISSION` + history · ○ `MEMBER_OF_ORG` + history · ✅ `DEFINES_WORKFLOW` + history |
| 23 | eslint-config-prettier (2025) | **✗ `package_version`** · **✗ `principal`** | **✗ `BUILDS_PACKAGE_VERSION`** (absence) |
| 24 | Nx "s1ngularity" (2025) | **✗ `workflow_job`** (`workflow_dispatch`-able publish job) · secret ○ (`NPM_TOKEN`) · **✗ `package_version`** · repo visibility ✅ *(prop, flipped)* · `default_workflow_permissions` *(prop)* | ○ `REFERENCES_SECRET{trigger_events incl. workflow_dispatch, fork_reachable}` · **✗ `BUILDS_PACKAGE_VERSION`** |
| 25 | GhostAction (2025) | **✗ `git_commit`** (direct push) · ref ○→`git_ref` · ruleset ○ · CODEOWNERS ○ · secret ○ · **✗ `web_host`** | ○ `ENFORCED_ON` (absence) · ○ `REVIEWS_AS_CODEOWNER` (absence on `.github/workflows`) · ○ `REFERENCES_SECRET` · **✗ `FETCHES_FROM`** |
| 26 | chalk/debug; Shai-Hulud v1; Shai-Hulud 2.0 (2025) | **✗ `credential_grant`** (bot PAT, 3-year-old npm token) · **✗ `workflow_job`** · runner ✅ (the `SHA1HULUD` registration) · **✗ `git_commit`** · **✗ `package_version`** · **✗ `principal`** · bot account ✅ | **✗ `REGISTERED_ON`** ("a self-hosted runner appeared on a repo that never had one") · **✗ `REPRESENTS_CREDENTIAL`** · ○ `REFERENCES_SECRET` · **✗ `FETCHES_FROM`** |
| 27 | Zombie workflows; QuantCo "PRs go both ways"; Angular dev-infra (2025) | **✗ per-ref workflow variant** · environment ○ (+`deployment_branch_policy`) · ruleset ○ (**bypass actor = bot**) · secret ○ (App private key / bot PAT) · **✗ `credential_grant`** · **✗ `actions_cache`** | **✗ `VARIES_ON`** · **✗ `BYPASSES` (actor → ruleset)** · **✗ `GATED_BY` (environment → reviewer)** — its *absence* alongside a branch policy is the QuantCo finding · **✗ `REPRESENTS_CREDENTIAL`** · **✗ `RESTORES_CACHE`** |
| 28 | Coordinated GitHub API enumeration / ghost accounts (2025–26) | account ✅ (`created_at`; derived `last_activity_at` *(prop)*) · **✗ `credential_grant`** | ○ `MEMBER_OF_ORG` · audit-log activity ❌ *not observable (GHEC)* — say so on the page |
| 29 | hackerbot-claw (2026) | **✗ `workflow_job`** · pull_request ○ (+ author `created_at`) · fork ✅ *(prop `is_fork` + `FORKED_FROM` edge)* · **✗ `credential_grant`** · release ○ (178 deleted — history) | ○ `OPENS_PULL_REQUEST` · **✗ `FORKED_FROM`** · ○ `PUBLISHES_RELEASE` + history |
| 30 | Trivy / trivy-action / setup-trivy "TeamPCP" (2026) | **✗ `git_ref`** (76 of 77 tags force-pushed — mass `head_sha` change in one observation) · action ○ · **✗ upstream repo node** · secret ○ (`updated_at`) · **✗ `credential_grant`** (`last_used_at` overlapping a rotation) · **✗ `package_version`** (OCI + PyPI) | **✗ `HAS_REF`** · **✗ `DEFINED_IN`** · ○ `USES_ACTION{pin_kind=tag}` · **✗ `REPRESENTS_CREDENTIAL`** |
| 31 | LiteLLM; Checkmarx KICS/AST (2026) | **✗ `workflow_job`** (publish secret readable by a *scanning* job) · secret ○ · **✗ `package_version`** · **✗ `credential_grant`** (30-day residual access) · action ○ | ○ `REFERENCES_SECRET` — the finding is *which job* holds it, i.e. the job must be the edge source · ○ `USES_ACTION` |
| 32 | Axios 1.14.1 / 0.30.4 (2026) | **✗ `principal`** (maintainer npm account) · **✗ `package_version`** | **✗ `BUILDS_PACKAGE_VERSION`** (absence) · **✗ `LINKED_IDENTITY`** |
| 33 | prt-scan campaign (2026) | pull_request ○ (+ author account age) · **✗ `workflow_job`** (triggers) · fork *(prop)* | ○ `OPENS_PULL_REQUEST` · **✗ `FORKED_FROM`** |
| 34 | TanStack CVE-2026-45321 (2026) | **✗ `actions_cache`** · **✗ `workflow_job`** (one job fork-reachable, one holding `id-token: write`) · OIDC issuer ✅ · **✗ `package_version`** (84 versions / 42 packages) · environment ○ | **✗ `WRITES_CACHE{fork_reachable}`** + **`RESTORES_CACHE{privileged}`** — the three-condition conjunction is one traversal or it is nothing · ✅ `FEDERATES_VIA` |
| 35 | actions-cool imposter commits (2026) | **✗ `git_ref`** (every tag moved) · **✗ `git_commit`** (`reachable_from_any_branch=false`) · action ○ · **✗ upstream repo node** | **✗ `HAS_REF`** + **`POINTS_AT`** · ○ `USES_ACTION{pin_kind}` · **✗ `DEFINED_IN`** |

### 2.1 Missing-concept frequency (how many incident rows demand it)

| Missing concept | Incident rows | Count |
| --- | --- | --- |
| `package` / `package_version` + `BUILDS_PACKAGE_VERSION` | 1, 4, 9, 11, 15, 16, 17, 23, 24, 26, 30, 31, 32, 34 | **14** |
| `credential_grant` (+ `HOLDS_CREDENTIAL`, `GRANTS_ACCESS_TO`) | 3, 4, 5, 6, 8, 16, 18, 20, 22, 26, 27, 28, 29, 30, 31 | **15** |
| `workflow_job` (declared job) | 2, 3, 10, 12, 14, 16, 17, 18, 20, 21, 24, 26, 29, 31, 33, 34 | **16** |
| `git_ref` (branch **and** tag, with `head_sha` history) | 6, 11, 12, 18, 20, 25, 27, 30, 35 | 9 |
| `git_commit` (narrow slice) | 1, 6, 11, 20, 22, 25, 26, 35 | 8 |
| `identity_core.principal` + `LINKED_IDENTITY` | 8, 9, 11, 15, 19, 23, 26, 32 | 8 |
| `actions_cache` + `WRITES_CACHE` / `RESTORES_CACHE` | 12, 16, 18, 27, 34 | 5 |
| `REPRESENTS_CREDENTIAL` (secret ↔ credential) | 5, 16, 20, 26, 27, 30 | 6 |
| upstream repo as a collected node + `DEFINED_IN` | 13, 20, 30, 35 | 4 |
| `FETCHES_FROM` (job → `web_host`) | 2, 25, 26, 30 | 4 |
| `FORKED_FROM` / fork-run edge | 10, 20, 26, 29, 33, 34 | 6 |
| `VARIES_ON` (workflow content per ref — zombie workflows) | 18, 24, 27 | 3 |
| `BYPASSES` (actor → ruleset) | 27 (+ OWASP SEC-1 as a class) | 1 |
| `REGISTERED_ON` / `runner_group` / `MEMBER_OF_RUNNER_GROUP` | 10, 26 | 2 |
| `actions_artifact` + `UPLOADS_ARTIFACT` | 14 | 1 |
| `GATED_BY` (environment → reviewer/app) | 27 | 1 |
| `deployment` | 19 | 1 |
| `REVIEWED` (edge) | 6, 11, 22, 25 (+ SLSA Source L4) | 4 |

Two readings. First, the three highest-count gaps (`workflow_job`, `credential_grant`, `package_version`)
are the *three axes of the deadly conjunction* named in §6.1 of the prior art — where code runs, what
credential it can reach, and what it publishes. Second, the highest-count gap of all is the one nobody
proposed, because it looks like it is already there: `github_actions_job` exists, but it is the wrong
job.

---

## 3. Observable-conditions coverage (§3.10, all 40)

Status column: **✅** representable today · **○** representable with the shape review's proposals ·
**✗** **not representable** without a new concept · **n/a** not a graph shape (a finding, or not
observable at all).

| # | Condition (abbreviated) | Representable? | What it needs |
| --- | --- | --- | --- |
| 1 | Action `uses:` pinned by 40-hex SHA | ○ | `github_action` + `USES_ACTION{pin_kind}` — but the source must be **`workflow_job`**, not the workflow, or "which job runs the unpinned action" is unanswerable |
| 2 | Pinned SHA belongs to canonical repo; tag ≠ moved (impostor / ref confusion) | **✗** | **`git_ref`** on the upstream repo (`head_sha` + history) + **`git_commit`**`{reachable_from_any_ref}` + **`DEFINED_IN`** to a collected upstream repo |
| 3 | No `pull_request_target`/`workflow_run`/`issue_comment` checking out PR head with secrets in scope | **✗** | **`workflow_job`** (the conjunction is per-job) + `REFERENCES_SECRET{trigger_events, checks_out_pr_head, fork_reachable}` |
| 4 | No `${{ github.event.* }}` interpolation into `run:` / `GITHUB_ENV` | **✗** | **`workflow_job`** field `injection_sinks[]` (parser output); pure property once the job node exists |
| 5 | `permissions:` explicit and minimal | **✗** | **`workflow_job.permissions`** — the prior art explicitly notes job-level *effective* permissions are not returned by the runs API, so they must be parsed and stored per declared job |
| 6 | `id-token: write` only in publish jobs, bound to an environment | **✗** | **`workflow_job`** + ○ `DEPLOYS_TO_ENVIRONMENT` |
| 7 | `persist-credentials: false`; no artifact upload of checkout dir | **✗** | `USES_ACTION{with_keys}` (○, needs the property added) + **`actions_artifact`** + **`UPLOADS_ARTIFACT`** |
| 8 | No `secrets: inherit`; no `toJson(secrets)` | ○ | `REFERENCES_SECRET{reference_form}` — the property carries it; needs `secrets: inherit` as a first-class `reference_form` value including the *callee* side |
| 9 | Cache not shared across trust boundaries | **✗** | **`actions_cache`** + **`WRITES_CACHE`/`RESTORES_CACHE`** — nothing today can express it |
| 10 | `runs-on: self-hosted` only in private repos | **✗** | **`workflow_job.runs_on`** + repo `visibility` ✅ |
| 11 | Trusted publishing rather than `NPM_TOKEN`/`PYPI_API_TOKEN` | ○ | `actions_secret` name-class *(prop)* + ✅ `FEDERATES_VIA` — full answer needs **`package_version.provenance`** |
| 12 | Release/publish workflow emits provenance | ○ | `github_release` + reuse `sigstore_core.ATTESTED_BY`; **`BUILDS_PACKAGE_VERSION`** for the registry half |
| 13 | Bot-conditions not used as an authz gate | **✗** | **`workflow_job.if_condition`** *(prop on the new node)* |
| 14 | Known-vulnerable action versions | ○ | `github_action` + advisory data → `compliance_core` finding; needs `git_ref` to join a SHA pin to an advisory range |
| 15 | Runs triggered from forks on privileged workflows | ✅/○ | `github_actions_run.head_repository` *(prop, exists)* + **`FORKED_FROM`** for the repo-side answer |
| 16 | Default/release branches protected (PR, approvals, no force-push, required checks) | ○ | `github_ruleset` + `ENFORCED_ON` → **`git_ref`** |
| 17 | Ruleset bypass actors; `enforce_admins=false` | **✗** | **`BYPASSES`** edge (JSON field cannot answer "what can this bot bypass?") — with `observable:false` when the credential cannot see it |
| 18 | Ruleset `enforcement: evaluate`/`disabled` | ○ | `github_ruleset.enforcement` *(prop)* |
| 19 | CODEOWNERS covers `.github/workflows/` | ○ | `REVIEWS_AS_CODEOWNER{patterns, resolved}` |
| 20 | Tags protected / immutable releases | **✗** | **`git_ref{ref_kind=tag}`** — `git_branch` as proposed cannot represent a tag at all |
| 21 | Signed commits required; `web_commit_signoff_required` | ○ / **✗** | ruleset rule *(prop)* ✅; *observed* signature status needs **`git_commit.verified`** |
| 22 | Environments with reviewers, `prevent_self_review`, branch policy | ○ + **✗** | `github_environment` ○ + **`GATED_BY`** edge (reviewer identity must be traversable — the QuantCo finding is an *absent* reviewer beside a *present* branch policy) |
| 23 | Repo secrets duplicating cloud keys; secret age | ○ | `actions_secret{created_at, updated_at}` + name-class *(prop)*; the "is it really a live credential" half needs **`REPRESENTS_CREDENTIAL`** |
| 24 | Deploy keys with write, unused >90d | **✗** | **`credential_grant{kind=deploy_key}`** |
| 25 | Webhooks to unknown hosts / `insecure_ssl` / no secret | ○ | `repository.configuration.webhooks[]` for self; **`webhook`** node + `computing_core.web_host` when the "which third parties do we feed" question arrives |
| 26 | Runners non-ephemeral; groups allowing public repos; stale version | ✅ + **✗** | `github_runner` ✅ + **`runner_group`** + **`MEMBER_OF_RUNNER_GROUP`** + **`REGISTERED_ON`** |
| 27 | Fork-PR settings (`require_approval_for_fork_pr_workflows`, …) | ✅ | `repository.configuration.actions_policy` *(prop)* |
| 28 | `sha_pinning_required`; `allowed_actions` tight; blocked list | ✅ | `github_account.configuration.org_policy` *(prop)* — correctly a property; nothing points at it |
| 29 | `default_workflow_permissions=read`; `can_approve_pull_request_reviews=false` | ✅ | *(prop)* |
| 30 | 2FA required; members without 2FA | ✅/○ | org *(prop)* + `MEMBER_OF_ORG{two_factor_enabled}` |
| 31 | `default_repository_permission ≤ read`; member repo creation | ✅ | *(prop)* |
| 32 | App installations: permission map, `repository_selection=all`, suspended, events | ○ | `app_installation` + `INSTANCE_OF_APP` + `HOSTS_INSTALLATION` |
| 33 | Fine-grained PATs: expiry, last-used, breadth; classic PATs | **✗** | **`credential_grant`** (`pat_grant` is the right instinct but too narrow) |
| 34 | OAuth apps with org access | **✗**, and **unobservable** | slot in `credential_grant{kind=oauth_grant}`; must render as "not observable" per the security-posture doctrine |
| 35 | Outside collaborators with write/admin; teams with admin; bot accounts with write | ○ | `HAS_REPO_PERMISSION{permission, via}` + **`github_team`** |
| 36 | Org secrets with `visibility=all` | ○ | `actions_secret{scope_kind=organization, visibility}` |
| 37 | Artifact/log retention | ✅ | *(prop)* |
| 38 | Audit-log coverage / snapshot-diff cadence | ✅ | platform types (`batch`, `collection_job`) + entity history — **no domain vocabulary needed** |
| 39 | Cloud/registry-side OIDC trust policies | **✗**, second collector | `aws_core` + `identity_core`; slot exists via ✅ `FEDERATES_VIA` / `TRUSTS_ISSUER` |
| 40 | Package-registry-side state (publisher config, provenance) | **✗**, second collector | **`package` / `package_version`** + **`identity_core.principal`** |

**Tally:** of 40 conditions, 10 are representable today, 13 with the shape review's proposals as
written, and **17 need a concept nobody has proposed**. Of those 17, eleven are covered by just four
new concepts: `workflow_job` (7 conditions), `credential_grant` (3), `git_ref` (3), `actions_cache` (1).

---

## 4. Critique of the shape review's proposals

Each proposal, the test that decided it, and the verdict. Six survive unchanged, three survive with a
material correction, one is replaced.

### 4.1 `git_branch` → **replace with `git_ref`**

- **Test:** T2 convergence passes (rulesets, PRs, runs, releases all point at it). But T4 fails for
  *tags*: condition 20, incidents 11, 20, 30 and 35 are all about **tags**, and `git_branch` cannot
  hold one. GitHub's own ruleset `target` enum is `branch|tag|push`.
- **Verdict: replace.** One `git_ref` node, `ref_kind ∈ {branch, tag}`, natural key `owner/repo` +
  `ref_name` (full `refs/…` form). `is_default` becomes a branch-only field; `signature_verified`,
  `tagger_login`, `is_immutable` become tag-only fields. Tag protection, tag-move detection and
  branch protection then share one node and one `ENFORCED_ON` edge — **fewer types, more coverage**,
  which is the direction the discipline wants.
- The load-bearing field is **`head_sha`**: field-level history on it *is* the tag-burst detection
  for incidents 20, 30, 35. That fact must live in exactly one place — the ref node — and not be
  copied onto each consumer's `USES_ACTION` edge (derive-a-fact-once).

### 4.2 `github_ruleset` — **endorse**

- **Test:** T1 (`ruleset_id` global), T2 (org-sourced rulesets are pointed at by every repo they
  apply to — the same singleton pattern as `github_app`), T3 (rulesets change on their own timeline;
  GitHub even ships `/rulesets/{id}/history`), T4 (the gate view is a traversal). Passes all four.
- **Correction:** `bypass_actors` must **not** be only a JSON field. See §5.4.

### 4.3 `status_check` — **endorse, with an honesty property**

- **Test:** T2 is the whole case, and it holds — the same context string is pointed at by a ruleset
  (required), a workflow job (producer) and a check run (observation). Three directions, three source
  types. This is the strongest convergence argument in the proposal set.
- **Correction:** the producer is a **job**, not a workflow (a check context is a job name, or
  `"<caller job> / <callee job>"` for a reusable workflow). `PRODUCES_CHECK` must originate at
  `workflow_job`, and must carry `{match_kind: exact|rendered_reusable|inferred, confidence}` — the
  shape review itself admits the match is heuristic, and an unlabelled heuristic edge in a gate view
  is exactly the "confident nonsense" failure mode.

### 4.4 `pull_request` — **endorse**

- **Test:** T1/T2/T3 all pass. T5 is the risk (unbounded); the proposed `initial_run_limit` collection
  policy handles it.
- **Note:** the incidents (29, 33, 22) want the *author's account age* and *fork origin*, which are
  fields on `github_account` and an edge to the head repo — not more PR fields.

### 4.5 `app_installation` — **endorse**

- **Test:** T2 (pointed at by the app and by the org, and by every repo when `selection=selected`),
  T3 (the permission map changes on its own timeline — the 2022 GitHub bug that escalated App
  read→write for a week is exactly a field-history question). Passes.
- This is the one place where a "grant" deserves its own type rather than folding into
  `credential_grant`: it carries a granular permission map, an events list and a repo-selection
  fan-out that the generic grant cannot hold without becoming a bag.

### 4.6 `actions_secret` — **endorse**; `actions_variable` — **demote to a field**

- `actions_secret` passes T2 (pointed at by its declaring scope, by every workflow job that reads it,
  and — new — by the credential it represents) and T3 (`updated_at` is the rotation signal in
  incidents 30/31). Node.
- `actions_variable` fails T2: nothing points at a variable except the workflow that reads it, and
  the value is not sensitive. **Verdict: `repository.configuration.variables[]` as a field.** One
  fewer type. (Revisit only if a variable ever turns out to gate something, e.g. the release bot's
  App ID pairing with a secret key — and note that pairing is better expressed as
  `REPRESENTS_CREDENTIAL` on the *secret*.)

### 4.7 `github_environment` — **endorse, add one edge**

- **Test:** T2 passes (declared by a repo, deployed to by jobs, and — the missing direction —
  *gated by* reviewers). T3 passes.
- **Correction:** `protection_rules` as pure JSON cannot answer "who approves deployments here",
  which is incident 27's QuantCo half. Add **`GATED_BY`** (environment → `github_account` | `github_team`
  | `github_app`) with `{rule_kind: required_reviewer|deployment_protection_app, prevent_self_review,
  wait_timer}`. The *absence* of this edge beside a present `deployment_branch_policy` is the finding.

### 4.8 `github_action` — **endorse, with two corrections**

- **Test:** T1 passes (`owner/repo[/path]`, `./local`, `docker://…`). T2 passes strongly (many
  workflows point at one action). Keeping the *version* off the node is correct — but see below.
- **Correction A — the source of `USES_ACTION` is a job, not a workflow.** Otherwise "does the job
  that runs this unpinned action also hold a publish secret" is a string join.
- **Correction B — actions call actions.** Composite actions have their own `uses:` (incident 20 is
  a *transitive* chain: `tj-actions/eslint-changed-files` → `reviewdog/action-setup@v1`; §3.8 records
  18% of marketplace actions carrying vulnerable dependencies). `USES_ACTION` must therefore allow
  `github_action` as a **source** as well as a target, and the edge needs `transitive_depth`.
- **Correction C — the upstream repo must be a node.** Incident 13 (Polyfill: org sold) and the
  §3.8 "762 archived actions" statistic are facts about the action's *repository* — owner, transfer,
  archived, last push. Add `github_action DEFINED_IN github_repository` and collect consumed upstream
  repos as thin `github_repository` nodes under a dimension (`github.scope=upstream`). No new type;
  a collection-scope decision the shape review does not make.

### 4.9 `CALLS_WORKFLOW` / `TRIGGERS_WORKFLOW` — **endorse, with properties**

- Both are correctly edges (the fact is about the pair). `TRIGGERS_WORKFLOW` must carry
  `{trigger_kind: workflow_run|workflow_call|repository_dispatch, branches, types, privilege_delta}` —
  the last one is the whole point: our own `ai-review-capture` (`permissions: {}`) triggering
  `ai-review` (`pull-requests: write` + provider keys) is a privilege step-up, and it is the shape
  Legit Security's `workflow_run` escalation research names.

### 4.10 `REFERENCES_SECRET` — **endorse the edge, expand the properties**

This is the edge where "shape is not severity" bites hardest. Properties required, each with the
question it settles:

| Property | Question it settles |
| --- | --- |
| `job` → **replaced by the edge source being `workflow_job`** | which privilege context reads it (incident 31: a *scanning* job could read the *publish* secret) |
| `reference_form` (`expression`\|`secrets_inherit`\|`env`\|`with`\|`toJson`) | condition 8; `secrets: inherit` and `toJson(secrets)` are categorically worse than a named reference |
| `trigger_events[]` | is it reachable from `pull_request_target` / `workflow_run` / `workflow_dispatch`? (incidents 3, 16, 24) |
| `fork_reachable` (bool, derived) | can an outsider cause this job to run at all? (incidents 3, 16, 21, 34) |
| `checks_out_pr_head` (bool) | the pwn-request signature (incidents 16, 20, 27, 34) |
| `reaches_run_block` (bool) | does the value reach a shell, or only an action input? |
| `job_permissions` (snapshot) | blast radius if it leaks (OpenSSF: permissions are a blast-radius control) |
| `gated_by_environment` / `gated_by_if_condition` | is there an approval or an author gate in front of it? (incidents 10, 17, 27) |
| `step_index`, `env_var_name` | locate it in the file for a human; distinguish two references in one job |

Without `fork_reachable` × `checks_out_pr_head` × `trigger_events`, a "secrets exposure map" panel
draws the same line for our benign release secret and for Ultralytics' `PYPI_API_TOKEN`.

### 4.11 `OPENS_PULL_REQUEST`, `REVIEWS_AS_CODEOWNER`, `MEMBER_OF_ORG`, `HAS_REPO_PERMISSION` — **endorse**

All four are facts about a pair, all four carry the property that decides severity
(`{role}`, `{permission, via}`, `{patterns, resolved}`). `HAS_REPO_PERMISSION` needs `via` precisely
because incident 20's "reviewdog auto-grants write to contributors" and our own outside-collaborator
row are the same edge with different provenance.

### 4.12 `pat_grant` — **replace with `credential_grant`** (see §5.4)

### 4.13 Posture as fields (§2.2.9) — **endorse, and it is the cleanest call in the review**

Org Actions policy, merge policy, security features, `oidc_sub_claim`: nothing points at them, they
are singletons per parent, and field-level history answers "when did `sha_pinning_required` flip".
**Property.** The instructive contrast is `github_ruleset`, which *is* a policy object and *is* a node
— because many repos point at one org ruleset. The test that separates them is T2, not intuition.

*(One defect worth flagging while the surface is open: `github_workflow.configuration` is declared as
a bare `{"type": "object"}` in both `FIELD_CRUD_SCHEMA` and `FIELD_VALIDATION_SCHEMA` — verified in
the plugin source. The parsed-YAML facts every condition above depends on are today not merely
un-traversable, they are undescribed. House rule: JSON structures require descriptions.)*

---

## 5. The gaps — proposed definitions

Nine new node types and one collection-scope change. Each carries the incidents that demand it, a
natural key, key fields and its edges. Ordered by incident-demand weight.

### 5.1 `github_core__workflow_job` — the declared job *(tier: self · neutral-capable)*

- **Demanded by:** incident rows 2, 3, 10, 12, 14, 16, 17, 18, 20, 21, 24, 26, 29, 31, 33, 34 (16) and
  conditions 3, 4, 5, 6, 7, 10, 13 (7). The most-demanded missing concept in the corpus.
- **Why it is not covered by `github_actions_job`:** verified in the plugin source —
  `GithubActionsJob` is keyed on `job_id` and carries `status` / `conclusion` / `started_at` /
  `completed_at`. It is an *execution*, one per run. The job as *written* has no node; its facts live
  inside `github_workflow.configuration` as an un-schema'd blob.
- **Tests:** T1 — natural key `owner/repo` + workflow `path` + job **key** (the YAML mapping key, which
  is stable across edits far better than a name). T2 — pointed at by actions used, secrets referenced,
  caches written/restored, environments deployed to, checks produced, `needs:` siblings, and every
  executed job. T3 — its `permissions` and `runs-on` change independently of the workflow's triggers.
  T4 — every conjunction in §6.1 of the prior art becomes one traversal instead of a join on a
  `{job}` string. All four.
- **Fields:** `job_key`, `name`, `permissions` (JSON, effective incl. workflow-level default),
  `runs_on` (JSON labels), `is_self_hosted` (derived), `environment_name`, `if_condition` (raw),
  `needs[]`, `strategy` (JSON), `container`, `uses` (when the job *is* a reusable-workflow call),
  `secrets_passing` (`none|named|inherit`), `injection_sinks[]` (parser: which `${{ }}` contexts reach
  `run:` / `GITHUB_ENV` / `GITHUB_PATH`), `checks_out_ref` (the ref expression given to checkout),
  `persist_credentials` (tri-state), `steps` (ordered JSON — steps are **not** nodes, see §6.1).
- **Edges:** `github_workflow DEFINES_JOB workflow_job`; `workflow_job USES_ACTION github_action`;
  `workflow_job REFERENCES_SECRET actions_secret`; `workflow_job WRITES_CACHE|RESTORES_CACHE
  actions_cache`; `workflow_job DEPLOYS_TO_ENVIRONMENT github_environment`; `workflow_job
  PRODUCES_CHECK status_check`; `workflow_job FETCHES_FROM web_host`; `github_actions_job
  INSTANCE_OF_JOB workflow_job` (execution → definition; the link that makes "this shape not only
  exists, it *ran* 40 times last week" answerable).
- **Cost honesty:** ~5 jobs × 14 workflows on `tap` ≈ 70 nodes; ~2 × 13 plugin repos ≈ 26. Under 150
  nodes for the whole org. This is not a cardinality problem.
- **Neutrality:** GitLab jobs map 1:1. The kernel has no analogue (§5 of the kernel doc: no
  repo-owned pipeline definition at all).

### 5.2 `credential_grant` — one node for every programmatic access path *(tier: friends · neutral)*

- **Demanded by:** rows 3, 4, 5, 6, 8, 16, 18, 20, 22, 26, 27, 28, 29, 30, 31 (15) and conditions 24,
  33, 34.
- **Why one node and not four (`pat_grant`, `deploy_key`, `oauth_grant`, `registry_token`):** each
  alone is 5–8 fields with one edge (fails the "is it worth a type" bar), and the question the corpus
  actually asks is OWASP SEC-2 verbatim — *"map all identities across all systems… Ensure all methods
  of programmatic access are covered."* Four types force a UNION into every instance of the one query
  that matters. `app_installation` stays separate because it carries a granular permission map and a
  repo fan-out (§4.5).
- **Natural key:** `(kind, issuer, external_id)`; where the platform gives no id (classic PATs), a
  synthetic key plus `observable: false` — the row exists to say *we know this class exists and cannot
  see it*, which is the security-posture doctrine's "name the risks left open" applied to vocabulary.
- **Fields:** `kind ∈ {fine_grained_pat, classic_pat, deploy_key, oauth_grant, registry_token, ssh_key,
  gpg_key, installation_token}`, `holder_login`, `holder_kind`, `scope_kind` (`org|repo|user`),
  `scope`, `capabilities` (JSON), `created_at`, `expires_at`, `last_used_at`, `revoked_at`,
  `observable` (bool), `source_endpoint`, `read_only` (deploy keys).
- **Edges:** `github_account|principal HOLDS_CREDENTIAL credential_grant`;
  `credential_grant GRANTS_ACCESS_TO github_repository {permission}`;
  **`actions_secret REPRESENTS_CREDENTIAL credential_grant {match_kind: name_heuristic|app_id_pairing|declared, confidence}`**.
- **The `REPRESENTS_CREDENTIAL` edge is the sleeper.** It is what turns incident 27's headline —
  *"ruleset bypass actor is a bot account whose PAT is stored as a secret in a repo with an injectable
  workflow"* — into a single path: `workflow_job -REFERENCES_SECRET-> actions_secret
  -REPRESENTS_CREDENTIAL-> credential_grant <-HOLDS_CREDENTIAL- github_account -BYPASSES-> github_ruleset`.
  Six incidents (5, 16, 20, 26, 27, 30) turn on that join and nothing in the estate provides it.
  The `match_kind`/`confidence` properties keep it honest: most of the time it will be a name heuristic.

### 5.3 `package` + `package_version` — what actually ships *(tier: friends · neutral)*

- **Demanded by:** rows 1, 4, 9, 11, 15, 16, 17, 23, 24, 26, 30, 31, 32, 34 (14) and conditions 11, 12, 40.
- **Two nodes, not one:** incident 34 is "84 versions across 42 packages in 6 minutes" — the burst is
  a fact about the *package* population; the payload is a fact about a *version*. `package_version`
  also carries T3 (its provenance and yank status change after publication).
- **Natural key:** purl (`pkg:npm/@scope/name` and `pkg:npm/@scope/name@1.2.3`; `pkg:oci/…`,
  `pkg:pypi/…`, `pkg:githubactions/…`). Registry-neutral by construction; GUAC uses the same key,
  which is the interoperability argument.
- **Fields (version):** `purl`, `version`, `published_at`, `yanked`, `digest`, `provenance_present`,
  `publisher_identity`, `registry`.
- **Edges:** `package HAS_VERSION package_version`; `github_actions_run BUILDS_PACKAGE_VERSION
  package_version {step, attested}`; `package_version ATTESTED_BY <sigstore_core.rekor_log_entry>`
  (reuse — the shape review §5 is right that attestations do **not** belong in `github_core`).
- **The finding is the missing edge.** SolarWinds, xz, lottie-player, eslint-config-prettier and
  Axios all read identically on the graph: *a `package_version` exists with no `BUILDS_PACKAGE_VERSION`
  edge and no attestation*. That is one query covering five incidents across seven years, and it is
  the single strongest argument for spending a second collector on registries.

### 5.4 `BYPASSES` — the edge the gate view cannot be drawn without *(tier: self · GitHub-specific)*

- **Demanded by:** incident 27 (Angular: ruleset bypass preserved for the bot whose PAT was stolen),
  OWASP SEC-1 verbatim ("avoid exclusion of user accounts… from branch protection rules"), and the
  shape review's own panel 4.3.2.
- **Why not the JSON field it is proposed as:** `bypass_actors` on the ruleset answers "who can bypass
  *this* rule" and nothing else. The panel asks the inverse — "what can this bot bypass, anywhere" —
  which a JSON array cannot serve. Keep the raw array for fidelity; **derive** the edge once, in one
  function.
- **`github_account|github_team|github_app BYPASSES github_ruleset`**, properties
  `{actor_type: Integration|OrganizationAdmin|RepositoryRole|Team|DeployKey, bypass_mode: always|pull_request,
  observable: bool, source: ruleset_field|rule_suite_inference}`.
- **Honesty requirement:** §3.9 and §5.1 of the prior art record that `bypass_actors` needs
  *Administration: write*, which contradicts the read-only posture. `observable: false` edges (or the
  absence of edges plus a page-level caveat) must be distinguishable from "no bypass actors exist" —
  our own org genuinely has zero on all four rulesets, and the view must not make that
  indistinguishable from blindness.

### 5.5 `git_ref` + `git_commit` — the ref layer *(tier: self / friends · neutral)*

- **`git_ref`** replaces the proposed `git_branch`; see §4.1. Natural key `owner/repo` + `ref_name`.
  Fields: `ref_kind`, `ref_name`, `short_name`, `is_default`, `head_sha`, `protected`,
  `protection_source` (`rulesets|classic|none`), `signature_verified`, `is_immutable`, `last_pushed_at`.
  Edges: `github_repository HAS_REF git_ref`; `github_ruleset ENFORCED_ON git_ref`;
  `pull_request TARGETS_REF git_ref`; `git_ref POINTS_AT git_commit` (friends).
- **`git_commit`** *(tier: friends, narrow slice only)* — natural key `owner/repo` + `sha` (keyed by
  repo *on purpose*: "does this SHA exist in the canonical repo and is it reachable from any ref" is
  the impostor-commit question, incidents 20 and 35). Fields: `sha`, `author_login`,
  `committer_login`, `verified`, `verification_reason`, `signer`, `reachable_from_any_ref`,
  `touches_workflow_paths` (bool), `authored_at`, `parents[]`.
  **T5 discipline — do not collect all commits.** Collect only distinguished commits: ref heads, tag
  targets, release targets, resolved action-pin SHAs, PR heads, and commits touching
  `.github/workflows/**`. Everything else is unbounded volume with no query demand.
- **Derive-once note:** `git_ref.head_sha` is the canonical store of "where does this ref point"; the
  `POINTS_AT` edge is a derived convenience that must be produced by the one function that reads that
  field, never collected independently. If it ever *is* collected twice, it needs a
  `TAP-KNOWN-DUPE` group.

### 5.6 `actions_cache` — the 2026 attack surface *(tier: self (declared) / friends (observed) · neutral-capable)*

- **Demanded by:** rows 12, 16, 18, 27, 34 (5) and condition 9. Includes the most recent and most
  sophisticated incident in the corpus (TanStack, 2026-05).
- **Tests:** T2 is textbook — the *entire* finding is that one key is pointed at by a low-trust writer
  and a privileged reader. T4 decisively: as a job property this is a self-join on string equality
  across jobs and workflows; as a node it is `job -WRITES_CACHE-> cache <-RESTORES_CACHE- job`.
- **Natural key:** `owner/repo` + normalized `key_expression` (as written, e.g.
  `${{ runner.os }}-pnpm-store-${{ hashFiles('**/pnpm-lock.yaml') }}`). The *expression* is the
  identity because the attack targets the key template, not one materialized entry.
- **Fields:** `key_expression`, `restore_keys[]`, `ref_scope` (cache is branch-scoped with
  default-branch fallback — this fallback *is* the vulnerability), `observed_keys[]`, `size_bytes`,
  `last_accessed_at`, `source` (`declared|observed`).
- **Edges:** `workflow_job WRITES_CACHE actions_cache` and `workflow_job RESTORES_CACHE actions_cache`,
  both with `{step_index, action_used, ref_scope, fork_reachable, privileged}` where `privileged` =
  the job holds `id-token: write` or references a publish-class secret. TanStack's three-condition
  conjunction ("each is necessary; none alone is sufficient") is then literally one query:
  *a cache with an incoming `WRITES_CACHE{fork_reachable:true}` and an incoming
  `RESTORES_CACHE{privileged:true}`.*
- The declared half costs **nothing new to collect** — it is already in the YAML the parser reads.

### 5.7 `identity_core__principal` — a machine identity that is not a GitHub account *(tier: later · neutral)*

- **Demanded by:** rows 8, 9, 11, 15, 19, 23, 26, 32 (8) and condition 40.
- Ledger (#9) is the clean statement: *"publish-capable registry identity not mapped to a current org
  member."* That sentence needs two identity spaces and a link between them; today there is one.
- **Home:** `identity_core`, not `github_core` — it is the neutral identity substrate, it already owns
  `oidc_issuer`, and the dependency direction is downward. Natural key `(provider, subject)` per the
  house rule that email is not identity.
- **Edges:** `github_account LINKED_IDENTITY principal {confidence, evidence}`;
  `principal HOLDS_CREDENTIAL credential_grant`; `principal PUBLISHED package_version`.
- Also the kernel's shape: a maintainer's PGP key is a principal, and the ≥2-signature web-of-trust
  rule is `principal -VOUCHED_FOR-> principal`. Cheap to leave the slot open; expensive to retrofit.

### 5.8 `runner_group` + `REGISTERED_ON` *(tier: friends · GitHub-specific)*

- **Demanded by:** rows 10, 26 and condition 26.
- `github_runner` exists, but there is no edge saying **where a runner is registered** — and incident
  26's Shai-Hulud 2.0 detection is exactly *"a self-hosted runner appeared on a repo that never had
  one."* `EXECUTED_ON` only appears after a job has already run on it. Add
  `github_runner REGISTERED_ON github_repository|github_account {registered_at_observed, first_seen}`.
- `runner_group` passes T2 (runners point at it, repos point at it, workflows point at it via
  `restricted_to_workflows`). Fields: `visibility`, `allows_public_repositories`,
  `restricted_to_workflows`, `selected_workflows[]`, `inherited`. Edges:
  `github_runner MEMBER_OF_RUNNER_GROUP runner_group`; `runner_group SCOPED_TO_REPO github_repository`.

### 5.9 `actions_artifact` *(tier: friends · neutral-capable)*

- **Demanded by:** row 14 (ArtiPACKED) and condition 7; also GitHub canon verbatim ("treat artifacts
  from other workflows as untrusted"), which is a *cross-run* trust edge, not a property.
- T2 holds: produced by one run, consumed by another — often across a trust boundary.
- Fields: `name`, `size_bytes`, `expired`, `digest`, `contains_git_config` (derived from a content
  scan — the ArtiPACKED finding itself), `created_at`.
- Edges: `workflow_job UPLOADS_ARTIFACT actions_artifact {paths}`;
  `workflow_job DOWNLOADS_ARTIFACT actions_artifact {from_workflow, cross_workflow: bool}`.
- Requires artifact **downloads** — §6.13 of the prior art: "do not treat read-only as metadata-only."

### 5.10 Collection-scope gap: **the upstream third party is not a node** *(tier: self · no new type)*

Not a missing *type* — a missing *scope decision*, and it blocks four incidents (13, 20, 30, 35).
Every consumed action lives in a repository we do not own, and the facts the corpus wants —
`owner_login` (Polyfill: org sold), `archived` (762 archived marketplace actions), `pushed_at`,
`is_fork`, tag population — are `github_repository` fields. Today `github_repository` is implicitly
"a repo in our org." Proposal: collect consumed upstream repos as thin `github_repository` nodes under
a dimension (`github.scope = owned|upstream`), with `github_action DEFINED_IN github_repository`.
Cost is one API call per distinct upstream owner/repo (16 for `tap`).

### 5.11 Smaller gaps, named for completeness

| Gap | Demanded by | Shape | Tier |
| --- | --- | --- | --- |
| **`VARIES_ON`** (workflow → `git_ref`, `{content_sha, has_privileged_trigger, differs_from_default}`) | rows 18, 24, 27 — the "zombie workflow" class | edge; `github_workflow` stays keyed on repo+path with default-branch content canonical | friends |
| **`FETCHES_FROM`** (`workflow_job` → `computing_core.web_host`, `{url_pattern, piped_to_shell, digest_pinned, step_index}`) | rows 2, 25, 26, 30 — `curl \| bash`, exfil destinations | edge, reuses an existing substrate type (downward dependency) | friends |
| **`FORKED_FROM`** (repo → repo) + `github_actions_run HEAD_FROM_REPOSITORY` | rows 10, 20, 26, 29, 33, 34; condition 15 | edge; `is_fork` is already a field | self (field) / friends (edge) |
| **`REVIEWED`** (`github_account` → `pull_request`, `{state, submitted_at, is_codeowner, dismissed, author_is_submitter}`) | rows 6, 11, 22, 25; SLSA Source L4 "uploader ≠ reviewer" | **edge, not a node** — see §6.4 | self-lite |
| **`GATED_BY`** (environment → account/team/app) | row 27 (QuantCo) ; condition 22 | edge | self-lite |
| **`github_team`** | conditions 17, 22, 35; CODEOWNERS, bypass actors and env reviewers all resolve to teams | node (T2: four directions point at it) | friends |
| **`deployment`** | row 19 (Bybit) | node; GitHub Deployments API + statuses | later |
| **`webhook`** | condition 25; our own Codacy finding | node at friends (field at self), converging on `computing_core.web_host` | friends |
| **`CAN_WRITE_REF`** (actor → `git_ref`, `{via[], gated_by_pr, requires_review, bypasses_gate}`) | panel 4.3.2; §6.4's BloodHound-style computed edge | **computed** edge, derived once from permissions ∪ membership ∪ installations ∪ grants ∪ bypasses | friends |

---

## 6. Rejected candidates

As valuable as the accepted list — this is the record that the question was asked.

### 6.1 `step` — **rejected (T1, T5)**
§6.4 of the prior art says "Workflow → Job → Step". A step has no stable identity (`id:` is optional,
the index shifts on any edit), nothing ever points at a step from a second direction, and the
population is ~10× the job population. Steps stay an ordered JSON array on `workflow_job`, with
`step_index` / `step_id` riding as **edge properties** on `USES_ACTION`, `REFERENCES_SECRET`,
`WRITES_CACHE` and `FETCHES_FROM` — which is where they belong, because "which step" is a fact about
the *pair*, not about the step.

### 6.2 `trigger` — **rejected (T1, T2)**
The most-cited precondition in the corpus (11 incident rows) is a *trigger* condition, which tempts a
node. But a trigger has no identity that persists and nothing points at it. It is a property of the
workflow, denormalized onto `REFERENCES_SECRET` / cache edges as `trigger_events[]` because the fact
the reader needs is "is *this* secret reachable from *that* trigger" — an edge fact. Recorded here so
the next person does not re-litigate.

### 6.3 `org_policy` / `actions_policy` / `security_posture` as nodes — **rejected (T2)**
Singletons per parent that nothing points at. Field-level history answers every "when did it change"
question the corpus asks (conditions 27–31, 37). The contrast with `github_ruleset` — which *is* a
policy object and *is* a node, because many repos point at one org ruleset — is the cleanest
illustration of T2 in this domain, and worth keeping in the corpus for teaching value.

### 6.4 `review` as a node — **rejected (T2 weak, T4 fails)**
A review has an id, but it is pointed at only by its PR and its author. SLSA Source L4
("changes MUST be agreed to by two or more trusted persons"; uploader ≠ reviewer) is answered by an
edge with `{state, is_codeowner, author_is_submitter}`. Prefer the edge; revisit only if review
*comments* ever become a consumer.

### 6.5 `fork` as a node — **rejected (T1 duplicate)**
A fork *is* a repository. `is_fork` + `parent_full_name` fields plus a `FORKED_FROM` edge. Inventing a
type would create two identities for one object.

### 6.6 `deploy_key`, `oauth_app`, `pat_grant` as separate nodes — **rejected (folded)**
Each is 5–8 fields and one edge; the query that matters is their union. Folded into
`credential_grant{kind}` — §5.2.

### 6.7 `actions_variable` as a node — **rejected (T2)**
Demoted to `repository.configuration.variables[]`. §4.6.

### 6.8 `change_event` / `snapshot` / `observation` — **rejected (substrate)**
The grid already gives field-level history and provenance on every entity and edge, and `batch` /
`collection_job` / `schedule` already carry the observation. Condition 38 and the entire
"change-over-time is the differentiator" thesis need **zero** new domain vocabulary. Modelling a
change type here would be re-inventing the substrate — the failure mode the skill names explicitly.

### 6.9 `finding` / `vulnerability` — **rejected (owned elsewhere)**
`compliance_core` owns `compliance_finding` / `HAS_COMPLIANCE_FINDING`. Incident 7 (the Microsoft SAS
token) is a *finding*, not a shape, and is the one incident row in the corpus with no vocabulary
implication at all. Self renders facts; verdicts wait for `compliance_core` at friends+.

### 6.10 `attestation` / `signature` — **rejected (owned elsewhere)**
`sigstore_core` already has `rekor_log_entry`, `sigstore_ca`, `ATTESTED_BY`, `SIGNED_BY_IDENTITY`.
Re-defining it in `github_core` would be derive-a-fact-twice wearing a graph costume. *(Residual:
the kernel's PGP-signed tags and tarballs are not sigstore-shaped; a neutral signer identity is the
`principal` slot in §5.7, flagged for later.)*

### 6.11 `third_party_service` — **rejected (composed)**
Incidents 3, 4, 5 (Travis, Heroku, CircleCI) want "a third-party system holding org-wide access."
That is already expressible as `github_app` + `app_installation` + `credential_grant{oauth_grant}` +
`webhook`→`web_host`. A wrapper type would add a join without adding a fact.

### 6.12 `egress` / network telemetry — **rejected (platform will eat it)**
§6.10 of the prior art: GitHub's 2026 roadmap ships a native L7 egress firewall for hosted runners in
6–9 months. Design collectors to *ingest* it; do not model it.

---

## 7. Forge-neutral vs GitHub-specific — and the kernel pressure test

The test applied is the skill's: *could a structurally different implementation of the same domain
populate this type?* The Linux kernel (§5 of the kernel doc) is that second implementation — email
threads, PGP keys, a text file for authority, and no gate at all.

| Neutral (`git_core` candidates) | Evidence from the kernel |
| --- | --- |
| `repository` | ~850 maintainer trees + linux-next + stable trees |
| **`git_ref`** | signed release tags **are** the kernel's release object; the branch/tag merge is *validated* by this case |
| **`git_commit`** | the primary object; `Fixes:` / `Link:` trailers are commit→commit edges |
| `pull_request` | maps *loosely* — a kernel pull request is an email referencing a signed tag; the kernel doc calls this "different" and proposes `patch_series` keyed by Message-ID. Neutral-with-a-caveat |
| `release` | `releases.json` + signed tarballs |
| **`principal`** | maintainer PGP keys, the ≥2-signature web of trust, FIDO2 keys |
| **`credential_grant`** | kernel.org SSH keys via gitolite — same shape, different issuer |
| `pipeline`/`pipeline_run`/`job` | KernelCI / KCIDB `checkout`/`build`/`test`, many origins |
| **`package_version`** | tarballs + per-distro packages; purl covers both |
| `environment`, `actions_cache`, `actions_artifact` | no kernel analogue, but GitLab CI has all three → neutral-capable, not neutral-proven |
| **GitHub-specific (stays in `github_core`)** | **Kernel verdict** |
| `github_platform`, `github_app`, `app_installation` | absent |
| `github_ruleset`, `status_check` | absent — "the protection rule is `S:`/`M:` plus Linus" |
| `github_action`, `USES_ACTION` pin posture | absent |
| `actions_secret`, OIDC sub customization | absent |
| `github_runner`, `runner_group` | absent (CI labs are independent systems, not registered runners) |
| `github_team`, `webhook` | absent / different |

**Reading:** the kernel populates 9 of the neutral candidates and **zero** of the GitHub-specific
ones. That is unusually clean evidence for the `git_core` boundary and it independently confirms the
shape review's §2.3 list, with two corrections: `git_ref` (not `git_branch`) and `credential_grant`
belong on the neutral side, and `secret` is *less* neutral than the shape review assumed (the kernel
has none, and GitLab's CI variables are the only second instance).

**Recommendation on timing:** unchanged from the shape review — build everything in `github_core` for
the self milestone with forge-neutral field names, and mark the neutral candidates. But note that
`git_ref`, `git_commit`, `credential_grant` and `principal` are the four types most likely to be
populated by a *second* collector (kernel, GitLab, a registry), so if `git_core` is ever extracted,
those four go first and `principal` should be born in `identity_core` rather than moved later.

---

## 8. Consolidated node inventory

Tier: **self** = the Aug-30 gate view · **friends** = Sep 6 · **later** = public alpha+.
Status: **exists** / **proposed** (shape review §2.2) / **new** (this pass).

| slug | forge-neutral? | tier | status | justification (incidents / conditions) |
| --- | --- | --- | --- | --- |
| `github_core__github_platform` | no | self | exists | root of the inventory |
| `github_core__github_account` | partial (user/org neutral) | self | exists | rows 6, 22, 26, 28, 29; conditions 30, 31, 35 |
| `github_core__github_repository` | **yes** | self | exists (+ **scope dimension**, §5.10) | every row; rows 13, 20, 30, 35 need the *upstream* scope |
| `github_core__github_workflow` | yes (`pipeline`) | self | exists | every trigger/injection row |
| `github_core__workflow_job` | yes (`job`) | **self** | **new** | **rows 2,3,10,12,14,16,17,18,20,21,24,26,29,31,33,34; conditions 3,4,5,6,7,10,13** |
| `github_core__github_actions_run` | yes (`pipeline_run`) | self | exists | rows 15, 20, 29; conditions 15, 38 |
| `github_core__github_actions_job` | yes | self | exists | execution evidence; runner-ephemerality heuristics (row 10) |
| `github_core__git_ref` | **yes** | **self** | **proposed → reshaped** (replaces `git_branch`) | rows 6,11,12,18,20,25,27,30,35; conditions 16, 20 |
| `github_core__github_ruleset` | no (neutral face: `protection_rule`) | self | proposed | rows 6, 25, 27; conditions 16, 17, 18, 21 |
| `github_core__status_check` | no | self | proposed | our own #3 finding (plugin repos have none); condition 16 |
| `github_core__github_action` | no | self | proposed (+ transitive + `DEFINED_IN`) | rows 13, 20, 30, 31, 35; conditions 1, 2, 14 |
| `github_core__actions_secret` | partial (GitLab CI variables) | self | proposed | rows 3,5,16,17,18,20,24,25,26,27,30,31; conditions 8, 11, 23, 36 |
| `github_core__actions_cache` | neutral-capable | **self** (declared) | **new** | **rows 12, 16, 18, 27, 34; condition 9** |
| `github_core__app_installation` | no | self | proposed | our own #1/#6 findings; condition 32 |
| `github_core__pull_request` | yes (merge request) | self | proposed | rows 22, 29, 33; conditions 15, 16 |
| `github_core__github_environment` | neutral-capable | self-lite | proposed (+ `GATED_BY`) | row 27; conditions 6, 22 |
| `github_core__github_release` | **yes** | self-lite | proposed | rows 11, 29; conditions 12, 20 |
| `github_core__github_runner` | no | self | exists (+ `REGISTERED_ON`) | rows 10, 26; conditions 10, 26 |
| `github_core__github_app` | no | self | exists | rows 5, 22; conditions 25, 32 |
| `identity_core__oidc_issuer` | yes | self | exists | row 34; conditions 6, 39 |
| `github_core__git_commit` | **yes** | friends | **new** (narrow slice — T5) | rows 1, 6, 11, 20, 22, 25, 26, 35; conditions 2, 21 |
| `credential_grant` (home TBD: `identity_core`) | **yes** | friends | **new** (replaces `pat_grant`) | rows 3,4,5,6,8,16,18,20,22,26,27,28,29,30,31; conditions 24, 33, 34 |
| `github_core__runner_group` | neutral-capable | friends | **new** | rows 10, 26; condition 26 |
| `github_core__actions_artifact` | neutral-capable | friends | **new** | row 14; condition 7 |
| `github_core__github_team` | no | friends | proposed (deferred) | conditions 17, 22, 35 |
| `github_core__webhook` | neutral-capable | friends | proposed (field at self) | our own #6 finding; condition 25 |
| `package` / `package_version` (home: new `supplychain_core` or `git_core`) | **yes** (purl) | friends | **new** | rows 1,4,9,11,15,16,17,23,24,26,30,31,32,34; conditions 11, 12, 40 |
| `identity_core__principal` | **yes** | later | **new** | rows 8, 9, 11, 15, 19, 23, 26, 32; condition 40 |
| `github_core__deployment` | neutral-capable | later | **new** | row 19 |
| `actions_variable` | — | — | **rejected → field** | §4.6 |

**Self-milestone node delta vs the shape review's build order:** `workflow_job` and `actions_cache`
are additions; `git_branch` becomes `git_ref`; `actions_variable` is dropped. Net +1 type, and the
two additions are what make the conjunction queries (§6.1 of the prior art — "the product's first
killer finding") expressible at all.

## 9. Consolidated edge inventory

| edge | source → target | neutral? | tier | status | properties (each answering a question) |
| --- | --- | --- | --- | --- | --- |
| `HOSTS_ACCOUNT` | platform → account | no | self | exists | — |
| `OWNS_REPO` | account → repo | yes | self | exists | — |
| `DEFINES_WORKFLOW` | repo → workflow | yes | self | exists | `{path}` — which file, for the CODEOWNERS join |
| `DEFINES_JOB` | workflow → workflow_job | yes | **self** | **new** | `{job_key, order}` — job identity within the file |
| `EXECUTES_WORKFLOW` | workflow → run | yes | self | exists | — |
| `HAS_ACTIONS_JOB` | run → actions_job | yes | self | exists | — |
| `INSTANCE_OF_JOB` | actions_job → workflow_job | yes | friends | **new** | `{run_attempt}` — "this shape actually ran", the static↔dynamic bridge |
| `EXECUTED_ON` | actions_job → runner | no | self | exists | `{runner_name_observed, ephemeral_inferred, evidence}` — row 10's non-ephemerality heuristic vs the API field |
| `HAS_REF` | repo → git_ref | yes | **self** | **new** | — (the drift lives on the ref's `head_sha` history) |
| `POINTS_AT` | git_ref → git_commit | yes | friends | **new** | `{observed_at}` — derived from `head_sha`, never collected twice |
| `ENFORCED_ON` | ruleset → git_ref | no | self | proposed | `{matched_condition}` — did `~DEFAULT_BRANCH` or an explicit pattern match? |
| `REQUIRES_CHECK` | ruleset → status_check | no | self | proposed | `{integration_id, strict}` — which app must produce it; is it stale-tolerant? |
| `PRODUCES_CHECK` | **workflow_job**\|app → status_check | no | self | proposed (**source corrected**) | `{match_kind, confidence}` — the match is heuristic and must say so |
| **`BYPASSES`** | account\|team\|app → ruleset | no | **self** | **new** | `{actor_type, bypass_mode, observable, source}` — "can this bot skip the gate?"; `observable:false` distinguishes *none* from *blind* |
| `USES_ACTION` | **workflow_job**\|action → action | no | self | proposed (**source + transitivity corrected**) | `{ref, pin_kind, version_comment, step_index, with_keys, transitive_depth}` — mutable vs pinned; `persist-credentials`; row 20's transitive chain |
| `DEFINED_IN` | action → repository | no | **self** | **new** | — enables owner-transfer (row 13) and archived-action checks |
| `CALLS_WORKFLOW` | workflow_job → workflow | yes | self | proposed | `{ref, pin_kind, secrets_passing}` — our plugin gates pin `tap@main` (mutable) |
| `TRIGGERS_WORKFLOW` | workflow → workflow | no | self | proposed | `{trigger_kind, branches, types, privilege_delta}` — is the callee more privileged than the caller? |
| `REFERENCES_SECRET` | **workflow_job** → actions_secret | partial | self | proposed (**expanded**) | see §4.10 — nine properties, each named with its question |
| `DECLARES_SECRET` | repo\|account\|environment → secret | partial | self | proposed | `{scope_kind, visibility}` — org secret with `visibility:all` (condition 36) |
| **`REPRESENTS_CREDENTIAL`** | actions_secret → credential_grant | yes | friends | **new** | `{match_kind, confidence}` — row 27's whole chain; honest about heuristics |
| **`WRITES_CACHE`** | workflow_job → actions_cache | neutral-capable | **self** | **new** | `{step_index, action_used, ref_scope, fork_reachable}` — is the writer reachable by an outsider? |
| **`RESTORES_CACHE`** | workflow_job → actions_cache | neutral-capable | **self** | **new** | `{step_index, ref_scope, privileged}` — does the reader hold `id-token: write` / a publish secret? |
| `DEPLOYS_TO_ENVIRONMENT` | workflow_job → environment | neutral-capable | self-lite | proposed | `{on_triggers}` |
| **`GATED_BY`** | environment → account\|team\|app | neutral-capable | self-lite | **new** | `{rule_kind, prevent_self_review, wait_timer}` — its *absence* beside a branch policy is row 27 |
| `DECLARES_ENVIRONMENT` | repo → environment | neutral-capable | self-lite | proposed | — |
| `OPENS_PULL_REQUEST` | account\|app → pull_request | yes | self | proposed | `{author_type, author_account_age_days}` — rows 29, 33 (throwaway accounts) |
| `TARGETS_REF` | pull_request → git_ref | yes | self | proposed (renamed) | — |
| `CHECKS_PULL_REQUEST` | run → pull_request | yes | self | proposed | `{match: head_sha}` |
| **`REVIEWED`** | account → pull_request | yes | self-lite | **new (edge, not node)** | `{state, submitted_at, is_codeowner, dismissed, author_is_submitter}` — SLSA Source L4 uploader≠reviewer |
| `REVIEWS_AS_CODEOWNER` | account\|team → repo | yes | self | proposed | `{patterns, resolved}` — `resolved:false` = GitHub silently ignores the owner |
| `MEMBER_OF_ORG` | account → account | yes | self | proposed | `{role, two_factor_enabled, first_seen}` — row 22's collaborator delta |
| `HAS_REPO_PERMISSION` | account → repo | yes | self | proposed | `{permission, via}` — `via` separates row 20's auto-granted write from a deliberate grant |
| `INSTANCE_OF_APP` / `HOSTS_INSTALLATION` / `SCOPED_TO_REPO` | installation ↔ app/org/repo | no | self | proposed | `{permissions, repository_selection, suspended, events}` on the node; edges thin |
| **`HOLDS_CREDENTIAL`** | account\|principal → credential_grant | yes | friends | **new** | — (severity fields live on the grant) |
| **`GRANTS_ACCESS_TO`** | credential_grant → repo | yes | friends | **new** | `{permission}` |
| **`REGISTERED_ON`** | runner → repo\|account | no | friends | **new** | `{first_seen, scope}` — "a runner appeared on a repo that never had one" (row 26) |
| **`MEMBER_OF_RUNNER_GROUP`** | runner → runner_group | no | friends | **new** | — |
| **`UPLOADS_ARTIFACT`** / **`DOWNLOADS_ARTIFACT`** | workflow_job → artifact | neutral-capable | friends | **new** | `{paths}` / `{from_workflow, cross_workflow}` — GitHub canon: other workflows' artifacts are untrusted |
| **`FETCHES_FROM`** | workflow_job → `computing_core.web_host` | yes | friends | **new** | `{url_pattern, piped_to_shell, digest_pinned, step_index}` — rows 2, 25, 26, 30 |
| **`VARIES_ON`** | workflow → git_ref | yes | friends | **new** | `{content_sha, differs_from_default, has_privileged_trigger}` — the zombie-workflow class |
| **`FORKED_FROM`** | repo → repo | yes | friends | **new** | — |
| `PUBLISHES_RELEASE` / `BUILDS_RELEASE` | repo → release / run → release | yes | self-lite | proposed | `{tag_match}`; **absence** of `BUILDS_RELEASE` = manual upload (row 11) |
| **`BUILDS_PACKAGE_VERSION`** | run → package_version | yes | friends | **new** | `{step, attested}` — **absence** is the finding for rows 1, 15, 23, 32 |
| **`HAS_VERSION`** | package → package_version | yes | friends | **new** | — |
| **`LINKED_IDENTITY`** | account → principal | yes | later | **new** | `{confidence, evidence}` — row 9 |
| **`CAN_WRITE_REF`** | actor → git_ref | yes | friends | **new (computed)** | `{via[], gated_by_pr, requires_review, bypasses_gate}` — panel 4.3.2 in one hop; derived once |
| `ATTESTED_BY` | release\|package_version → `sigstore_core.rekor_log_entry` | yes | friends | **reuse, do not redefine** | condition 12 |
| `FEDERATES_VIA` / `TRUSTS_ISSUER` / `ENABLED_ON` / `REFERENCES_RESOURCE` | — | mixed | self | exists | row 34; conditions 6, 39 |

---

## 10. Source register and the update seam

| Source | Version / date pinned | Machine-readable artifact | Verdict |
| --- | --- | --- | --- |
| GitHub "Secure use reference" | as of 2026-08-26 | none (HTML) | **adopt** — the base checklist |
| GitHub REST API surface (§3.9) | 2026-08-26 | OpenAPI (`github/rest-api-description`) | **adopt** — the observability ground truth; the OpenAPI repo is the diff feed |
| GitHub Actions 2026 security roadmap | 2026-03-26 | changelog feed | **align** — `dependencies:` lockfile and trigger rulesets become new vocabulary when they GA |
| OWASP Top 10 CI/CD Security Risks | 2022, still canonical | per-risk pages | **adopt** — SEC-1…SEC-10 as finding tags |
| SLSA v1.2 (Build + Source tracks) | 2025-11 | spec site, git repo | **adopt** — Source L2–L4 is a ruleset-continuity model; drives `git_ref` history |
| NIST SSDF SP 800-218 v1.1 | 2022 | PDF Table 1 | **reference** — compliance hook only |
| CISA/NSA Defending CI/CD | 2023-06-28 | PDF | **reference** |
| zizmor rule set | 1.24.1 (2026-05) | rules in-repo; `json-v1` output | **adopt as findings**, align on names (`unpinned-uses`, `template-injection`, `cache-poisoning`, `artipacked`, `secrets-inherit`, `bot-conditions`, `self-hosted-runner`) |
| OpenSSF Scorecard checks | current | JSON API / BigQuery | **align** |
| GUAC | current | purl / in-toto schemas | **adopt purl** as the `package_version` key |
| BloodHound GitHub OpenGraph schema | 2026 (gaps noted §5.8 of prior art) | schema page | **reference / diff** — an existing graph model of our exact domain; **run OpenHound on our org and diff node+edge kinds** (skill: "an existing graph model converts a survey into a diff") |
| Cartography GitHub module | current | schema docs | **reference** |
| Incident corpus (§4, 35 rows) | 2026-08-26 | this repo | **adopt** — the load-bearing direction |
| Linux kernel pipeline (neutrality test) | 2026-08-26 | this repo | **reference** — the second implementation |

**Update seam (record, do not build):** the two feeds that will move this vocabulary are the GitHub
OpenAPI description (new endpoints = new observability = candidate types; the `dependencies:`
lockfile and trigger rulesets are already announced) and the zizmor/Scorecard rule sets (new rule =
candidate edge property). Per the skill, the eventual shape is a **ledger that opens a proposal**,
never an auto-mutation — precedent: the AWS service-detection ledger and the aws_core coverage delta.

**Maintenance obligation.** This is a dated artefact (2026-08-27) built from a corpus that ends
2026-05. Five of the six most recent incidents were detectable only from a *change*, and the attack
technique is moving faster than any standard absorbs it. Re-run this pass when the incident corpus is
refreshed, when GitHub ships the 2026 roadmap items, or when a second collector (kernel, GitLab,
registry) lands — whichever comes first.

## 11. Decisions to put in front of a human

1. **Does `workflow_job` land in the self milestone?** It is +1 type and one migration, and without it
   the Aug-30 gate view can show shape but not exploitability. Recommendation: yes — it is cheaper now
   than after `USES_ACTION` / `REFERENCES_SECRET` have shipped pointing at the wrong source.
2. **`git_ref` instead of `git_branch`.** Free before the migration, a rename after.
3. **Where does `credential_grant` live** — `identity_core` (neutral, matches `principal`) or
   `github_core` (ships sooner)? Recommendation: `identity_core`, because the kernel and registry
   collectors both populate it.
4. **Is `package_version` a `git_core` concept or a new `supplychain_core`?** It is the highest-count
   gap but needs a registry collector; the type's home decides whether the second collector is cheap.
5. **`BYPASSES` when `bypass_actors` is unobservable.** Confirm the §5.1 empirical test (a read-only
   App on our org) before shipping a panel whose blank cells could mean either "none" or "blind."
