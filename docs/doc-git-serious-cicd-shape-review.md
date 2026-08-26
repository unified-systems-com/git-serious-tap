---
title: CI/CD shape review — what our own pipeline is, and what git-serious must model
date: 2026-08-26
status: research
audience:
  - developer
  - llm
related_docs:
  - docs/doc-git-serious-cicd-security-prior-art.md
---

> **Research pass, 2026-08-26.** Inventory of one real GitHub organization's CI/CD system, the gap between it and what github_core collects today, the models/edges/icons that close the gap, and the landing-page story. Written by an AI research agent from public sources and
> read-only API calls; claims carry citations, and the report flags what it could not verify.
> Nothing here is canon — requirements live in specs, the fence lives in the roadmap.

# git-serious — CI/CD shape review (design-research pass, 2026-08-26)

Scope: our own org `unified-systems-com` as the first git-serious target. **Redactions:** secret
*names*, concrete App ID values, and maintainer handles are generalized in this published copy — they
are reconnaissance value we control, and the specific inventory is exactly what a running instance
is for. Structure (counts, permission shapes, policy flags, pin posture) is kept in full. Read-only `gh` inventory
(OAuth token: `repo`, `read:org`, `project`, `gist` — NOT org admin scopes), the `github_core` plugin
checkout at `_dev-plugins/github_core/`, the house skills (add-model / add-edge / add-page / add-panel),
the page-story doctrine, and `plan/product-map.md` from `origin/session/strategy` (Iron Man 1 rule).

Legend for tiers: **self** = needed for the Aug 30 "gate view" Done-Test; **friends** = Sep 6;
**later** = public alpha or beyond. Every `403/404` below is a real observation with this token.

---

## 1. Our CI/CD system as it actually is

### 1.1 Inventory

| Surface | Count | Where configured | Who can change it | What it gates |
| --- | --- | --- | --- | --- |
| Repos | 19 public (1 core `tap`, 12 live `tap-plugin-*` + 1 archived `tap-plugin-aws-secrets-source`, `tap-build-dependencies`, `.github`, `unified-ai-review`, `unified-ai-review-prompts`, `git-serious-tap`) | org | org owner (`notgeorge`); `members_can_create_repositories=false` | everything |
| Org members / roles | 1 member (admin), 1 outside collaborator (write on `tap` — the same human's second account), 1 team (`maintainers`, `maintain` on `tap`) | org settings | org owner | who can approve / bypass / push |
| Org posture | 2FA required; `default_repository_permission=none`; Dependabot alerts + secret scanning on for new repos; GHAS not default for new repos; plan `team` | org settings | org owner | baseline for every repo |
| Workflows in `tap` | 14 files + 1 composite action (`.github/actions/ci-web-image`) | `tap/.github/workflows/` | anyone with a merged PR; `/.github/` is CODEOWNED (needs `a maintainer account` + `a maintainer account` approval) | PR gate, post-merge publish, release, nightly scans, dependency bots |
| Reusable workflows (`workflow_call`) in `tap` | 3: `plugin-ci.yml`, `plugin-release-sbom.yml`, `api-fuzz.yml` | `tap` | same | every plugin repo's CI and release |
| Plugin-repo workflows | 2 per repo (`ci.yml` → `plugin-ci.yml@main`; `release-sbom.yml` → `plugin-release-sbom.yml@main`); same in `tap-build-dependencies` | each plugin repo | plugin repo writers | plugin admission + release attestations |
| `unified-ai-review` workflows | 4 (`capture.yml`, `review.yml`, `self-capture.yml`, `self-review.yml`) | that repo; consumed from `tap` by full SHA | its writers | AI review of every `tap` PR |
| Rulesets on `tap` | 4, all `active`, all target `~DEFAULT_BRANCH`, **zero bypass actors on all four**: org-level `protect-default-branches` (no delete / no force-push), `org-require-pr` (PR required, code-owner review, extra approval for unattributed changes, 0 approvals otherwise), `copilot-review-floor` (`copilot_code_review` on push, not drafts); repo-level `main-required-checks` (required status check **`gate`**, integration 15368 = GitHub Actions, `strict=false`; PR rule duplicated) | org settings (3) + repo settings (1) | org owner / repo admin | landing on `main` |
| Rulesets on plugin repos | the 3 org rulesets only — **no required status check** on any plugin repo (`ci` is advisory) | org | org owner | PR required, but red CI can merge |
| Classic branch protection | none (`GET /branches/main/protection` → 404 "Branch not protected") | — | — | a naive tool reports `main` unprotected |
| Required check → producer | `gate` = the aggregator job in `product-lines.yml` (needs `setup`, `secret-scan`, `rids`, `line[test_all,samsite]`, `cold-boot`, `lean-boot`, `api-fuzz`; change-tier lets docs/specs skip lanes) | `product-lines.yml` | CODEOWNED | the whole promote |
| Other checks on a PR (NOT required) | CodeQL default setup (`Analyze (actions/js/python)`, `CodeQL`), `SonarCloud Code Analysis` (failing on #180), `Codacy Static Code Analysis` (`action_required` on #180), `copilot-pull-request-reviewer`, AI review `capture`/`review` jobs, `dco`, `secret-scan` | apps + workflows | app installers | nothing — advisory |
| GitHub Apps installed on the org | 4, **all `repository_selection: all`**: `tap-renovate` (contents:write, workflows:write, PRs:write, issues:write, checks:read, vuln_alerts:read), `tap-release-please` (contents:write, PRs:write), `sonarqubecloud` (checks/statuses/PRs:write, security_events:write, members:read), `codacy-production` (checks/statuses/PRs/issues:write, **repository_hooks:write, organization_hooks:write**, merge_queues:read, custom_properties:read) | org → Settings → Installations | org owner | bots that can push/PR/comment on every repo |
| First-party platform apps | Dependabot (security updates on), CodeQL default setup (5 languages, weekly, `threat_model: remote`), GitHub Advanced Security app, Copilot code review (via ruleset) | repo/org security settings | repo admin | advisory checks + alerts |
| Secrets (names) on `tap` | 5 (names generalized for publication — the live inventory belongs in the instance, not in a public file): two third-party AI-review provider keys, and the App ID + private key for each of the two org bots; Dependabot secrets: 0 | repo settings | repo admin | AI review seats; bot identities |
| Variables on `tap` | 1: the release bot's App ID (value withheld here; it is a variable, not a secret, precisely because it is not sensitive) | repo settings | repo admin | release-please identity |
| Org-level secrets/variables | **403** with this token (needs org admin or fine-grained org `Secrets: read`) | org | org owner | unknown to us right now |
| Plugin-repo secrets/vars | 0 / 0 in all three sampled repos (`grid-fixtures/ci.yml` still references `secrets.TAP_CORE_RO_PAT` — dead reference, silently empty) | — | — | — |
| Environments | `copilot` on `tap` and on `tap-build-dependencies` (created 2026-02-05, no protection rules, `can_admins_bypass=true`, referenced by NO workflow) | repo settings | repo admin | nothing — orphan |
| Webhooks | `tap`: 1 (Codacy, `push` + `pull_request`, JSON, last response 200). Org hooks: 404 (needs `admin:org_hook`) | repo settings | repo admin | outbound event feed to Codacy |
| Deploy keys | 0 on `tap` | — | — | — |
| CODEOWNERS | 20 rules; owners `the two maintainer accounts` on guard machinery, `pyproject.toml`, `/.github/`, `/ci/terraform/`, promote/gate scripts, Dockerfiles, `docker/`, compose, `.githooks/`, `**/guards/`; last rule un-owns `**/guards/baselines/` | `tap/.github/CODEOWNERS` (self-owning) | CODEOWNED | second-account approval on weakening moves |
| Actions policy on `tap` | `allowed_actions: selected` (GitHub-owned + verified creators + `astral-sh/*`); **`sha_pinning_required: false`**; default `GITHUB_TOKEN` = read; `can_approve_pull_request_reviews=false`. Org-level Actions policy: 403 | repo/org settings | admin | which third-party code may run |
| Third-party `uses:` in `tap` | 16 distinct actions, **all SHA-pinned with `# vX` comments** (checkout, cache, upload/download-artifact, setup-python, attest, attest-build-provenance, create-github-app-token, astral-sh/setup-uv, docker/{setup-buildx,build-push,login}, aquasecurity/trivy-action, github/codeql-action/upload-sarif, googleapis/release-please-action, renovatebot/github-action) + 2 cross-repo reusable workflows pinned by SHA (unified-ai-review) + local `./.github/...` | workflow files; Renovate `helpers:pinGitHubActionDigests` keeps them current | CODEOWNED | supply chain of the gate itself |
| Cross-repo pin posture (plugins → core) | every plugin `ci.yml`/`release-sbom.yml` calls `unified-systems-com/tap/.github/workflows/*.yml@main` — a **mutable branch pin**, documented as deliberate | plugin repos | plugin writers | one `tap` main change alters all 13 plugin gates |
| Dependency bots | Renovate self-hosted (`renovate.yml`, cron 05:45 UTC, app token, PR-only, `RENOVATE_REPOSITORIES=unified-systems-com/tap` only); no `dependabot.yml` (security updates only). Observed: PR #148 open (uv docker tag), #124/#125/#97/#98 merged | `renovate.json5`, `renovate.yml` | CODEOWNED (`/.github/`) | dependency freshness / pin refresh |
| Release machinery | `release-please.yml` (push main; rolling PR #139 "release 0.1.5"; app token) → tag `vX.Y.Z` + GitHub Release → `publish-release-tags.yml` retags the already-attested `:sha-<short>` manifest → `ghcr.io/unified-systems-com/tap-{web,db}:X.Y.Z`. Releases: v0.1.0 (human) … v0.1.4 (bot). Stray non-release tag `park/steampipe-tooling` | `release-please-config.json`, `.release-please-manifest.json` | CODEOWNED | what a version number means |
| Published artifacts | GHCR `tap-web`, `tap-db` (multi-arch, `:sha-*`, `:latest`, `:X.Y.Z`, `buildcache-*`), SLSA provenance + SBOM attestations; plugin wheels attested by `plugin-release-sbom.yml` (no GitHub Release assets — 0 assets on every release). **Package listing: 403** (needs `read:packages`; fine-grained PATs cannot list packages at all) | `publish-images.yml`, `plugin-release-sbom.yml` | — | what consumers pull |
| Scheduled scans | `trivy-nightly` (09:30 UTC, SARIF → code scanning), `api-fuzz-nightly` (09:47), `nightly-plugins` (09:17, discovers every `tap-plugin-*` repo via API and runs `plugin-ci.yml` against core `main`), Renovate (05:45) | `tap` workflows | CODEOWNED | drift detection off the PR path |
| Alerts | code scanning: **77 open** on `tap`; Dependabot: 0; secret scanning: 0; push protection on; `secret_scanning_validity_checks`/`non_provider_patterns`/`ai_detection` off | repo security | admin | advisory |
| Local git hooks | `.githooks/`: `pre-commit` (stdlib secret scan, fails loud w/o python3), `prepare-commit-msg` (DCO trailer), `post-checkout/merge/rewrite` (mypy cache clear) | `hooksPath` set at spawn | any dev (opt-out with `--no-verify`) | developer-side only, not a server control |
| Merge settings on `tap` | merge/squash/rebase all allowed, `allow_auto_merge=true`, `delete_branch_on_merge=false`, `web_commit_signoff_required=false` | repo settings | admin | how PRs land |
| OIDC | default `sub` claim (`repo:unified-systems-com@…/tap@…`), no custom claims; issuer `token.actions.githubusercontent.com` (already an `identity_core__oidc_issuer` node) | repo Actions settings | admin | attestations, future PyPI trusted publishing |
| Fine-grained PAT grants to the org | **404** (`/orgs/{org}/personal-access-tokens` — needs org-owner token with the org "Personal access tokens: read" permission; classic PATs are never enumerable) | org settings | org owner | who else can read/write via token |

### 1.2 How a commit on `tap` reaches `main` (diagram in prose)

```
developer worktree ──.githooks (secret scan, DCO trailer)──▶ push session branch
   └─ scripts/promote-to-main.sh: pre-push merge + local fast lane + opens PR (auto-merge armed)
PR opened ──▶ rulesets on ~DEFAULT_BRANCH (4 active, 0 bypass actors)
   ├─ org-require-pr / main-required-checks: PR required · code-owner review on CODEOWNED paths
   │     (a maintainer account cannot approve own PR ⇒ a maintainer account from a second device) · stale reviews
   │     dismissed · extra approval for unattributed commits
   ├─ copilot-review-floor: Copilot code review runs on push (advisory comments)
   └─ main-required-checks: required status check `gate` (GitHub Actions app 15368)
        └─ product-lines.yml (pull_request, merge_group, dispatch; concurrency per ref)
             setup (change-tier docs|specs|full) ─▶ secret-scan (gitleaks) · dco · rids
             ─▶ line[test_all, samsite] (compose stack, ci-web-image pull-or-build)
             ─▶ cold-boot · lean-boot · api-fuzz (calls ./api-fuzz.yml)
             ─▶ gate (fail-closed aggregator: skip allowed only where tier permits)
   in parallel, advisory: ai-review-capture (pull_request, permissions {}) ─workflow_run─▶
        ai-review (base-repo context, pull-requests:write, OPENAI/XAI keys) — both call
        unified-ai-review/.github/workflows/*.yml@<full SHA>; CodeQL default setup; SonarCloud;
        Codacy (via app + repo webhook); copilot-pull-request-reviewer
merge (auto-merge when gate green + reviews satisfied) ──▶ push to main
   ├─ publish-images.yml: build amd64+arm64 by digest ─▶ multi-arch :sha-<short> (+:latest)
   │     ─▶ attest (id-token, attestations:write) ─▶ trivy scan → SARIF
   └─ release-please.yml: app token (vars.TAP_RELEASE_PLEASE_APP_ID + secret key) maintains
         the rolling release PR; merging it ─▶ tag vX.Y.Z + Release ─▶ publish-release-tags.yml
         retags the attested :sha-<short> manifest as :X.Y.Z (packages:write)
nightly (off-path): renovate (app token, PR-only) · trivy-nightly · api-fuzz-nightly ·
   nightly-plugins (discovers tap-plugin-* via API, runs plugin-ci.yml against main)
```

### 1.3 How a plugin release happens

```
plugin repo PR ──▶ 3 org rulesets (PR required, code-owner review, Copilot) — NO required check
   └─ ci.yml (thin caller) ─▶ tap/.github/workflows/plugin-ci.yml@main
        conformance (validate_plugin --strict, Django-free) [+ boot-and-test if ci/nightly.boot.json]
merge ──▶ scripts/release-plugin.sh tags vX.Y.Z ──▶ release-sbom.yml (thin caller, id-token +
   attestations:write) ─▶ tap/plugin-release-sbom.yml@main: build wheel at tag, CycloneDX + SPDX,
   attest provenance + both SBOM predicates ──▶ verify: gh attestation verify <wheel> --owner …
consumers: boot profiles pin git source + tag (boot-record-as-BOM); PyPI trusted publishing = later
```

Things this inventory taught us that we did not already know (candidate "surprise" views, section 4):

1. `tap-release-please` is installed on **all** repos; the workflow comment says "installed on this repo only". `tap-renovate` (contents+workflows write) is also org-wide while Renovate only runs against `tap`.
2. `sha_pinning_required` is **off** — our SHA pins are Renovate discipline, not a platform control.
3. Plugin repos have **no required status check**; red `ci` can merge.
4. Every plugin gate is pinned to `tap@main` (mutable), while `tap` pins `unified-ai-review` by SHA.
5. `copilot` environments exist on two repos and nothing uses them.
6. Codacy holds `organization_hooks: write` + `repository_hooks: write` and already owns a repo webhook.
7. Classic branch-protection API says `main` is unprotected; only rulesets protect it.
8. `grid-fixtures/ci.yml` references a secret that does not exist.
9. 77 open code-scanning alerts on `tap`; SonarCloud/Codacy checks are red/blocked on the open PR and nobody is gated on them.

---

## 2. Model gap analysis

### 2.1 What github_core already covers

`github_platform`, `github_account`, `github_repository`, `github_workflow` (parsed YAML incl. triggers,
permissions, jobs[].uses/needs/runs_on, raw_yaml), `github_actions_run`, `github_actions_job`,
`github_runner`, `github_app` (slug singleton, synthetic-path detection only); `identity_core__oidc_issuer`.
Edges: `HOSTS_ACCOUNT`, `OWNS_REPO`, `DEFINES_WORKFLOW`, `EXECUTES_WORKFLOW`, `HAS_ACTIONS_JOB`,
`EXECUTED_ON`, `ENABLED_ON`, `REFERENCES_RESOURCE`, `FEDERATES_VIA` (+ `TRUSTS_ISSUER` emitted).
Dimensions: `github.platform`, `github.owner`, `github.repo`, `github.surface`, `github.observation`.
Assumed: org-scope refactor (enumerate the account's repos; `github.owner` becomes the org).

No new model is needed for: triggers, `permissions:` blocks, `concurrency`, job `needs`, runner labels,
run/job status — all already on `workflow.configuration` / `job.configuration`. The gaps are the
**governance layer** (refs, rules, checks, identities, credentials) and the **cross-repo edges**.

### 2.2 Proposed models and edges

Principle: fewer nodes, more derived edges. A node earns its place only when the same identity is
referenced from more than one direction (convergence) or needs history of its own.

| # | Thing | Covered today? | Proposal | Tier | Vocabulary home |
| --- | --- | --- | --- | --- | --- |
| 1 | Protected ref (`main`) | No — `head_branch` is a string on runs | **`git branch` node** | self | neutral (`git_core`) |
| 2 | Rulesets / branch protection | No | **`ruleset` node** + `ENFORCED_ON` | self | GitHub-specific now; neutral `protection_rule` later |
| 3 | Required status checks / check contexts | No | **`status_check` node** + `REQUIRES_CHECK`, `PRODUCES_CHECK` (derived) | self | GitHub-specific |
| 4 | Check runs (observed outputs) | Partly — an Actions job IS a check run | field `check_run_id` on `actions_job`; app-produced check runs as a node later | friends | GitHub-specific |
| 5 | Pull requests (incl. bot PRs) | No | **`pull_request` node** + `OPENS_PULL_REQUEST`, `TARGETS_BRANCH`, `CHECKS_PULL_REQUEST` (derived) | self | neutral (`git_core`, "merge request") |
| 6 | GitHub App installations w/ permissions | Partly — `github_app` describes the app, not the grant | **`app_installation` node** + `INSTANCE_OF_APP`, `HOSTS_INSTALLATION`, `SCOPED_TO_REPO` | self | GitHub-specific |
| 7 | Fine-grained PAT grants | No | **`pat_grant` node** + `HOLDS_TOKEN`, `SCOPED_TO_REPO` | friends (404 with our token) | GitHub-specific |
| 8 | Secrets / variables (names) | No (backlog `req-github-core-backlog-references`) | **`actions_secret` node** (scope enum), `actions_variable` node; `DECLARES_SECRET`, `REFERENCES_SECRET` (derived from YAML), `REFERENCES_VARIABLE` | self (secrets) / friends (variables) | GitHub-specific (GitLab has CI variables — could go neutral later) |
| 9 | Environments | No | **`environment` node** + `DECLARES_ENVIRONMENT`, `DEPLOYS_TO_ENVIRONMENT` (from `environment:` key) | self-lite | neutral-ish |
| 10 | Action references + pin posture | Partly — `jobs[].uses` strings in `workflow.configuration` | **`action` node** (identity = `owner/repo[/path]`) + `USES_ACTION` edge carrying `{ref, pin_kind, version_comment, job, step}` | self | GitHub-specific |
| 11 | Reusable-workflow calls / workflow_run chains | No | `CALLS_WORKFLOW` (workflow → workflow, in-scope) and `TRIGGERS_WORKFLOW` (from `on.workflow_run`) — edges only | self | GitHub-specific |
| 12 | CODEOWNERS | No | parse into `repository.configuration.codeowners` + `REVIEWS_AS_CODEOWNER` edge (account → repo, `{patterns}`) | self | neutral (GitLab has CODEOWNERS too) |
| 13 | Security-feature posture | No | fields on `repository.configuration.security` + `.actions_policy` + `.merge_policy` (JSON with schema); org posture on `github_account.configuration.org_policy` | self | GitHub-specific values, neutral shape |
| 14 | Org membership / collaborators / teams | Partly — `github_account` covers users and orgs | `MEMBER_OF_ORG` (account → org account, `{role}`), `HAS_REPO_PERMISSION` (account → repo, `{permission, via}`); **`team` node** later | self (members, collaborators) / friends (teams) | GitHub-specific |
| 15 | Releases / tags / packages | No | **`release` node** + `PUBLISHES_RELEASE`; `package`/`package_version` nodes later (API unobservable with fine-grained PATs; OCI registry is an alternative source) | self-lite (releases) / friends (packages) | release neutral; package GitHub-specific |
| 16 | Dependabot / Renovate PRs as activity | No | covered by #5 + `github_app OPENS_PULL_REQUEST` (this is the backlog `OPENS_PR` item) | self | — |
| 17 | Webhooks / deploy keys | No | `repository.configuration.webhooks[]` (host, events, active) and `.deploy_keys[]` for self; `webhook` node friends | self-lite | GitHub-specific |
| 18 | Commits | No | none for self — `head_sha` fields suffice; `commit` node only when a code-paths/traceability consumer appears | later | neutral |

#### 2.2.1 `branch` (self, neutral)

- Slug: `github_core__git_branch` for self (see 2.3 on where it ends up); class `GitBranch`.
- Natural key: `owner/repo` + `name`. Fields: `full_name`, `name`, `is_default` (bool), `head_sha`,
  `protected` (bool, from `GET /repos/{o}/{r}/branches/{b}` — reflects rulesets too), `html_url`, `configuration`.
- Dimensions: `github.platform`, `github.owner`, `github.repo`, `github.surface=refs`.
- Edges: `github_repository HAS_BRANCH git_branch` (1→N; self collects the default branch only, plus
  any branch a ruleset names explicitly).
- Why a node and not a field: it is the anchor of the gate view — rulesets, PRs, runs and releases all
  point at it. Icon: octicon `git-branch`.

#### 2.2.2 `ruleset` (self, GitHub-specific)

- Slug: `github_core__github_ruleset`. Natural key: `ruleset_id` (globally unique on GitHub; org-sourced
  rulesets are one node shared by every repo they apply to — same singleton pattern as `github_app`).
- Fields: `ruleset_id`, `name`, `source_type` (`Organization|Repository`), `source`, `enforcement`
  (`active|evaluate|disabled`), `target` (`branch|tag|push`), `conditions` (JSON), `rules` (JSON list of
  `{type, parameters}`), `bypass_actors` (JSON list), `created_at`, `updated_at`, `html_url`.
- Dimensions: `github.platform`, `github.owner`, `github.surface=governance` (no `github.repo` on
  org-sourced nodes — they are not repo-scoped).
- Edges: `github_ruleset ENFORCED_ON git_branch` (N↔N; resolved per repo from `conditions.ref_name`;
  `~DEFAULT_BRANCH` → that repo's default-branch node). Property schema: `{matched_condition}`.
  `github_ruleset REQUIRES_CHECK status_check` (from `rules[type=required_status_checks]`),
  property `{integration_id, strict}`.
- Observability: `GET /repos/{o}/{r}/rulesets` (returns org-level rulesets that apply — good: a
  repo-scoped read-only PAT sees org rules' effect) + `/rulesets/{id}`. `GET /orgs/{org}/rulesets` is
  404 without org admin — do not depend on it. Read requires repo `Administration: read` on a
  fine-grained PAT (rulesets are readable publicly for public repos, but do not rely on that).
- Classic branch protection: also probe `GET /branches/{b}/protection`; when 404 and rulesets exist,
  record `protection_source=rulesets` on the branch so the page can say "protected by rulesets, not
  classic protection". Icon: octicon `law` (or `shield-lock`).

#### 2.2.3 `status_check` (self, GitHub-specific)

- Slug: `github_core__status_check`. Natural key: `owner/repo` + `context` + `integration_id`
  (the required-check identity GitHub uses; e.g. `gate` / 15368).
- Fields: `full_name`, `context`, `integration_id`, `app_slug` (resolved: 15368→`github-actions`,
  57789→`github-advanced-security`, 12526→`sonarqubecloud`, 56611→`codacy-production`), `required`
  (bool, derived), `last_conclusion`, `last_observed_at`, `configuration`.
- Dimensions: `github.platform`, `github.owner`, `github.repo`, `github.surface=checks`.
- Edges: `github_ruleset REQUIRES_CHECK status_check`; `github_workflow PRODUCES_CHECK status_check`
  (derived, enrichment phase, exact match: a job `name:`/id in the parsed YAML equals the context, OR a
  reusable-workflow caller renders as `"<caller job> / <callee job>"`); `github_app PRODUCES_CHECK
  status_check` for app-owned contexts (integration_id ≠ 15368). One edge type, two source types —
  acceptable because it is one relationship ("this producer emits this check context").
- Why a node: the same context name is referenced by rulesets (required), by workflows (producer), and
  by check runs on every commit (observation) — a convergence node, same reasoning as `oidc_issuer`.
- Observability: rulesets give the required set; `GET /commits/{sha}/check-runs` on the default-branch
  head gives the observed set (`name`, `app.id`, `conclusion`) — cheap, one call per repo.
  Icon: octicon `checklist` (required) / `check-circle` family for status.

#### 2.2.4 `pull_request` (self, neutral)

- Slug: `github_core__pull_request`. Natural key: `owner/repo` + `number`.
- Fields: `full_name`, `number`, `title`, `state` (`open|closed`), `merged` (bool), `draft`,
  `author_login`, `author_type` (`User|Bot`), `base_ref`, `head_ref`, `head_sha`, `created_at`,
  `updated_at`, `merged_at`, `merged_by_login`, `merge_commit_sha`, `labels` (JSON), `review_decision`
  (from `GET /pulls/{n}/reviews` summarized: `{approvals:[…], changes_requested:[…], commented:[…]}`),
  `html_url`, `configuration`.
- Dimensions: `github.platform`, `github.owner`, `github.repo`, `github.surface=pulls`,
  `github.observation=activity`.
- Edges: `pull_request TARGETS_BRANCH git_branch`; `github_account OPENS_PULL_REQUEST pull_request`
  and `github_app OPENS_PULL_REQUEST pull_request` (bot authors like `app/tap-renovate` resolve to the
  app node by slug — this closes `req-github-core-backlog-app-relationships`'s `OPENS_PR`);
  `github_actions_run CHECKS_PULL_REQUEST pull_request` (derived: `run.head_sha == pr.head_sha`, exact).
- Collection policy: open PRs + last N merged/closed (N = `initial_run_limit`, reuse the knob).
  Reviews stay JSON in v0; a `review` node is friends/later.
- Observability: public data; `Pull requests: read`. Icon: octicon `git-pull-request` /
  `git-merge` (merged).

#### 2.2.5 `app_installation` (self, GitHub-specific)

- Slug: `github_core__app_installation`. Natural key: `installation_id`.
- Fields: `installation_id`, `app_id`, `app_slug`, `target_type`, `target_login`,
  `repository_selection` (`all|selected`), `permissions` (JSON map perm→`read|write`), `events`
  (JSON), `created_at`, `updated_at`, `suspended_at`, `html_url`.
- Dimensions: `github.platform`, `github.owner`, `github.surface=apps`.
- Edges: `app_installation INSTANCE_OF_APP github_app` (N→1; also upserts the `github_app` node with a
  real `app_id` — today Dependabot's is null); `github_account HOSTS_INSTALLATION app_installation`
  (org → installation); `app_installation SCOPED_TO_REPO github_repository` only when
  `repository_selection=selected` (from `GET /orgs/{org}/installations` you cannot list the selected
  repos without an installation token — record `selected` and leave the fan-out for a later
  `GET /user/installations/{id}/repositories` path; all four of ours are `all`, so no edge and the
  page reads the field).
- Observability: `GET /orgs/{org}/installations` worked with our org-owner OAuth token; a fine-grained
  PAT needs org `Administration: read`. Non-owners: 403 — collector must degrade with a warning (same
  pattern as runners). Icon: octicon `plug` (installation) vs existing `github-app`.

#### 2.2.6 `actions_secret`, `actions_variable`, `environment` (self / friends / self-lite)

- `github_core__actions_secret` — natural key `scope_kind` + `scope` + `name` where `scope_kind ∈
  {repository, organization, environment}` and `scope` is `owner/repo`, `org`, or `owner/repo#env`.
  Fields: `name`, `scope_kind`, `scope`, `visibility` (org: `all|private|selected`), `created_at`,
  `updated_at`. **Never a value.** Dimensions: platform/owner/(repo)/`github.surface=secrets`.
- `github_core__actions_variable` — same key shape, plus `value` (variables are not secret).
- `github_core__github_environment` — natural key `owner/repo` + `name`; fields `protection_rules`
  (JSON), `deployment_branch_policy` (JSON), `can_admins_bypass`, `created_at`, `html_url`.
- Edges: `github_repository DECLARES_SECRET actions_secret`; `github_account DECLARES_SECRET
  actions_secret` (org scope); `github_environment DECLARES_SECRET actions_secret`;
  `github_repository DECLARES_ENVIRONMENT github_environment`; `github_workflow REFERENCES_SECRET
  actions_secret` (derived from `${{ secrets.X }}` / `secrets: {X: ...}` / `secrets: inherit` in the
  raw YAML, property `{job, trigger_events}` — the trigger list is what makes the exposure map
  answerable: is this secret reachable from `pull_request`? from `workflow_run`?);
  `github_actions_job DEPLOYS_TO_ENVIRONMENT github_environment` (from `environment:`; none in our
  org today — that itself is a finding). `GITHUB_TOKEN` is not a secret node; its per-workflow
  `permissions` block is already on the workflow.
- Observability: repo secrets/variables names need fine-grained `Secrets: read` / `Variables: read`;
  org-level needs org `Secrets: read` (we got 403 — name it as a possibly-unobservable surface and
  degrade). Icons: octicon `lock` (secret), `hash` (variable), `server` (environment).

#### 2.2.7 `action` + `USES_ACTION` / `CALLS_WORKFLOW` / `TRIGGERS_WORKFLOW` (self)

- `github_core__github_action` — natural key `owner/repo[/path]` for remote, `./path` for local
  composites (scoped to repo), `docker://image` for container actions. Fields: `identity`, `kind`
  (`action|reusable_workflow|local|docker`), `owner`, `repo`, `path`, `html_url`, `verified_creator`
  (bool, from `GET /repos/{o}/{r}` owner type + marketplace flag — optional), `configuration`.
  One node per action identity; the *version* lives on the edge so "actions/checkout used by 12
  workflows at 1 SHA" is one node with 12 edges. Dimensions: platform + `github.surface=actions`.
- `github_workflow USES_ACTION github_action` — property schema (required, `additionalProperties:
  false`): `{ref, pin_kind: sha|tag|branch|none|local|digest, version_comment, job, step_index}`.
  `pin_kind` is derived once by the parser (40-hex → `sha`; `v\d…` → `tag`; else `branch`).
- `github_workflow CALLS_WORKFLOW github_workflow` — derived in enrichment when the `uses:` target is a
  workflow file in a collected repo (plugins → `tap/plugin-ci.yml@main`; `tap` →
  `unified-ai-review/capture.yml@sha`). Same property schema as `USES_ACTION`. When the target repo is
  out of scope, only the `github_action` node (kind `reusable_workflow`) + `USES_ACTION` edge exist.
- `github_workflow TRIGGERS_WORKFLOW github_workflow` — derived from `on.workflow_run.workflows: [name]`
  matched by workflow `name` within the repo (our `ai-review-capture` → `ai-review` privilege step-up).
- Also record the repo's Actions policy (`allowed_actions`, `patterns_allowed`, `sha_pinning_required`,
  `default_workflow_permissions`) on `repository.configuration.actions_policy` — the pin-hygiene view
  compares observed pins to the policy. Icons: octicon `package` (action), `pin` / `pin-slash`
  for pin posture badges.

#### 2.2.8 CODEOWNERS, membership, permissions (self)

- Parse `.github/CODEOWNERS` (also `/CODEOWNERS`, `docs/CODEOWNERS`) into
  `repository.configuration.codeowners = [{pattern, owners:[…]}]`; probe
  `GET /repos/{o}/{r}/codeowners/errors` and store `codeowners_errors`.
- Edge `github_account REVIEWS_AS_CODEOWNER github_repository` with `{patterns:[…]}`; team owners
  become `github_team` edges in friends. Unresolvable owners (GitHub silently ignores them — the
  CODEOWNERS header itself warns of this) become a warning flag on the edge property `resolved: false`.
- `github_account MEMBER_OF_ORG github_account` `{role: admin|member}` from `GET /orgs/{org}/members`
  (+ `?role=admin`); `github_account HAS_REPO_PERMISSION github_repository` `{permission, via:
  direct|outside_collaborator|team}` from `GET /repos/{o}/{r}/collaborators` (needs repo
  `Administration: read`; degrade on 403). `github_team` node + `HAS_TEAM` / `MEMBER_OF_TEAM` in
  friends. Icons: octicon `code-review` (codeowner), `organization`, `people` (team), `person`.

#### 2.2.9 Posture fields (self, no nodes)

On `github_repository.configuration`: `security` (the `security_and_analysis` block verbatim +
`code_scanning_default_setup` `{state, languages, schedule}` + alert counts `{code_scanning_open,
dependabot_open, secret_scanning_open}`), `merge_policy` (`allow_*_merge`, `allow_auto_merge`,
`delete_branch_on_merge`, `web_commit_signoff_required`), `actions_policy` (2.2.7), `webhooks[]`
(`{id, host, events, active, last_response_code}` — URL host only, never the full URL with its
token), `deploy_keys[]`, `oidc_sub_claim`. Give each a JSON Schema with descriptions (house rule:
JSON structures require descriptions). On the org `github_account.configuration.org_policy`:
`two_factor_requirement_enabled`, `default_repository_permission`, `members_can_create_repositories`,
`*_enabled_for_new_repositories`, `plan`. Alert counts feed a future `compliance_core` finding
(later); do not model findings in self.

#### 2.2.10 `release` (self-lite) and packages (friends)

- `github_core__github_release` — natural key `owner/repo` + `tag_name`; fields `tag_name`, `name`,
  `draft`, `prerelease`, `published_at`, `author_login`, `author_type`, `target_sha`, `assets` (JSON
  names+sizes), `html_url`. Edge `github_repository PUBLISHES_RELEASE github_release`;
  `github_actions_run` → release link only via `event=push` on `refs/tags/…` (`head_branch` holds the
  tag) — derive `github_actions_run BUILDS_RELEASE github_release` (exact tag match). Icon `tag`.
- Packages: `GET /orgs/{org}/packages` needs classic `read:packages`; fine-grained PATs do not
  support the Packages API at all. Alternative source for self/friends: the anonymous OCI registry
  (`GET https://ghcr.io/v2/<owner>/<image>/tags/list` with the anonymous token flow) — a second
  collector source, not GitHub REST. Defer to friends; for self, the release-chain view reads
  `publish-release-tags.yml` + release nodes and states "image `:X.Y.Z` expected at ghcr…" without
  proving it. Say so on the page rather than implying completeness.

### 2.3 Neutral `git_core` vs GitHub-specific — recommendation

Neutral candidates (tap#144): `repository`, `branch`, `pull_request`, `release`, `environment`,
`protection_rule` (the neutral face of `ruleset`), `pipeline` / `pipeline_run` / `job` (the neutral
faces of workflow/run/job), `secret`. GitHub-only: `platform`, `app`, `app_installation`, `ruleset`
details (`bypass_actors`, rule types), `status_check` (GitHub check contexts), `action`, `pat_grant`,
`team`, `runner`, webhooks.

Recommendation for the self milestone: **build every new model inside `github_core`**, name the neutral
candidates with forge-neutral field names (`git_branch`, `pull_request`, no GitHub-only required
fields), and mark them `git_core-earmarked` in the spec. Reasons: (1) one repo, one migration wave, no
new-repo CI/release ceremony before Aug 28; (2) tap#145 (dist-name derivation) still fails closed for a
`git-core-tap` distribution, so a new plugin would ship under the old prefix and be renamed anyway;
(3) entity ids are UUIDv5 over `(entity_type, natural_key)`, so the later slug change is a re-collect
not a data migration **as long as no field instance persists data** — that window closes at the
friends milestone (Sep 6). Decision to put in front of George: extract `git_core` between self and
friends, or accept that post-friends extraction is a migration. Do not extract during self.

### 2.4 Unobservable or degraded with a read-only fine-grained PAT (say it on the page)

- Org secrets/variables names (org `Secrets: read` needed), org Actions policy, org rulesets list, org
  webhooks — 403/404 for us today.
- Fine-grained PAT grants (org-owner token with "Personal access tokens: read"); classic PATs never.
- GHCR packages (Packages API needs classic scope) — OCI registry is the workaround.
- App-installation selected-repo lists (needs an installation token).
- Copilot code review results are comments/reviews on the PR (observable via reviews), not a check.
- Runner config on repos still needs `Administration: read` (already degrades).

---

## 3. Icons

Existing convention: `static/github_core/icons/<key>.svg`, Octicon glyphs wrapped in a padded viewBox with
explicit GitHub-ink fill (`#1f2328`), NOTICE file listing which keys derive from Octicons, the
`mark-github` glyph used nominatively for the platform node. Octicons (`primer/octicons`) are MIT
(confirmed via API: `license.spdx_id = MIT`). GitHub's logo rules (github.com/logos): the Invertocat /
wordmark may be used to refer to GitHub or link to it, must not be modified, recolored beyond their
guidance, or combined into our own mark — nominative use as "the GitHub platform node" is fine and
already documented in NOTICE. Third-party app marks (Renovate, SonarCloud, Codacy, release-please) are
their owners' trademarks — do not ship them; render a generic glyph, and treat `avatar_url` hotlinking
as an opt-in (it is a remote fetch from the viewer's browser — an egress the page should not do by
default). `aws_core` has no icons NOTICE (only `LICENSE`); the github_core NOTICE is the better precedent
and should be the pattern for git-serious.

| Type | Icon key | Source | Octicon name (24px set) | Notes |
| --- | --- | --- | --- | --- |
| `git_branch` | `git-branch` | Octicon | `git-branch` (`git-branch-check` variant for "protected") | pull |
| `github_ruleset` | `github-ruleset` | Octicon | `law` (alt: `shield-lock`) | pull; `shield-x` badge when `enforcement != active` |
| `status_check` | `status-check` | Octicon | `checklist`; badges `check-circle-fill` / `x-circle-fill` / `skip-fill` (12px set) | pull |
| `pull_request` | `pull-request` | Octicon | `git-pull-request`, `git-pull-request-draft`, `git-merge` (merged), `git-pull-request-closed` | pull |
| `app_installation` | `github-app-installation` | Octicon | `plug` | pull; existing `github-app` stays for the app node |
| `pat_grant` | `github-pat` | Octicon | `key` (`key-asterisk` for expired?) | pull |
| `actions_secret` | `actions-secret` | Octicon | `lock` | pull |
| `actions_variable` | `actions-variable` | Octicon | `hash` | pull |
| `github_environment` | `github-environment` | Octicon | `server` (alt `rocket`) | pull |
| `github_action` | `github-action` | Octicon | `package`; `package-dependencies` for reusable workflows | pull |
| pin posture badge | `pin-sha`, `pin-tag`, `pin-branch` | Octicon | `pin` (sha), `pin-slash` (branch/none), `tag` (tag) | pull; badge-only, no node |
| `github_release` | `github-release` | Octicon | `tag` (alt `milestone`) | pull |
| `github_team` | `github-team` | Octicon | `people` | pull |
| org membership badge | `org-admin` | Octicon | `organization` / `person` | pull |
| codeowner badge | `codeowner` | Octicon | `code-review` | pull |
| webhook | `webhook` | Octicon | `webhook` (**16px only** — upscale, or draw a 24px version ourselves) | draw/scale |
| bot actors | `dependabot`, `copilot`, `hubot` | Octicon | `dependabot`, `copilot`, `hubot` | pull (GitHub's own product glyphs; nominative) |
| Renovate / SonarCloud / Codacy / release-please | — | draw ourselves / generic | use `plug` or `apps` | never ship their logos |
| GitHub platform | `github-platform` (exists) | Octicon `mark-github` | — | nominative; unchanged |

Practical: extend the existing NOTICE list with every new key; keep the same padded-viewBox + `#1f2328`
fill pipeline (a tiny script that wraps `octicons/icons/<name>-24.svg` would be the git-serious
equivalent of `get-aws-icons`, and is worth a `get-octicon` skill in github_core — S task).

---

## 4. Landing page story + sub-visualizations

Story sentence (page-story doctrine): *"Here is your organization's path to `main` — what guards it,
who and what can act on it, what has been running through it, and where the posture is thin."*
Reads top-down: **org at a glance → the gate → who/what can act → activity → posture**. The
grid-centric thread (history, cross-repo edges, derived links) is woven into each paragraph, not a
separate "look at TAP" section. Iron Man 1: no Rampart vocabulary anywhere on the page.

### 4.1 Panel catalog available (from `tap_web` / `tap_viz`)

Standard: `text`, `table` (Tabulator; bound to a Search via `USES_SEARCH`; explicit `columns[]` with
named formatters incl. `tickDash`; declarative `group_by` sections; `quick_filter`; pagination),
`chart` (ECharts — **v0 is bare**: no chart definition language yet, so no heatmap/timeline from config
today), `viewer`, `editor`, `flip`, `history`, `batch-*`, `sequence-nav`; `tap_viz` `graph`
(Cytoscape; projection + seed Search; status badges). KPI tiles: the gryphon-driven `finding_strip`
lives in `fedramp_20x_ksi` — git-serious must not depend on a compliance plugin, so the org hero needs
its own small strip type (in `github_core`, mirroring `finding_strip`'s config shape) or `finding_strip`
moves down into `tap_web` (larger; later).

### 4.2 Page layout (`/git-serious` org landing; page + instances live in `git-serious-tap`, panel types in `github_core`)

| Row | Slot | Panel type | Story paragraph |
| --- | --- | --- | --- |
| 1 | `hero` | custom `github-org-hero` (KPI strip) | The org at a glance: repos, workflows, apps installed (write-capable count), open PRs (bot vs human), required checks per repo, secrets declared, `% uses: SHA-pinned`, open alerts, last collected age |
| 2 | `intro` | `text` | One paragraph: what this org's gate is, in words, derived from the data ("main on 19 repos is protected by 3 org rulesets; only `tap` requires a check; 0 bypass actors; 4 apps can write everywhere") |
| 3 | `gate` | `graph` (projection) | **The Gate** — see 4.3.1 |
| 4 (2 cols) | `actors` / `apps` | `table` × 2 | Who can act on main (people, roles, codeowners) / What can act (installations with permissions) |
| 5 | `activity` | `table` (org-wide recent runs + PRs, grouped by outcome) | What has been running through the gate; failures first |
| 6 (2 cols) | `pins` / `secrets` | `table` × 2 | Pin hygiene / Secrets exposure |
| 7 | `posture` | `table` (repo × feature, `tickDash`) | Security-feature posture across every repo |
| 8 | `release` | `graph` (small projection) | The release chain for `tap` |
| 9 | `history` | `history` strip | What changed since last collection (rulesets, apps, pins, secrets) — the grid thread |

Per-repo drill-down = the existing `/samsite/repo`-style page re-homed as `/git-serious/repo?repository_entity_id=…`
with the new panels added (ruleset card, required checks, pins for that repo).

### 4.3 Sub-visualizations worth building

| # | View | Question it answers | Data needed | Panel type | Surprise likelihood |
| --- | --- | --- | --- | --- | --- |
| 4.3.1 | **The Gate graph** | "What must be true for a commit to land on `main`?" | `git_branch` ← `ENFORCED_ON` ← rulesets → `REQUIRES_CHECK` → `status_check` ← `PRODUCES_CHECK` ← workflow → `CALLS_WORKFLOW`/`USES_ACTION`; codeowner edges; app installations with `contents: write` | `graph` projection, nested compounds (platform → org → repo) | **High** — the graph shows `tap` with a required check and 12 plugin repos with none; shows apps that bypass PR entirely |
| 4.3.2 | **Who-can-bypass / write matrix** | "Who or what can change `main` without the gate?" | org members `{role}`, collaborators `{permission}`, ruleset `bypass_actors`, installations with `contents|workflows: write`, PAT grants (friends), deploy keys | `table` with `group_by` (humans / apps / tokens) and `tickDash` columns per capability | **High** — release-please + Renovate org-wide write is the first row |
| 4.3.3 | **Pin-hygiene heatmap** | "Where does mutable code enter the gate?" | `USES_ACTION` + `CALLS_WORKFLOW` edges with `pin_kind`, `actions_policy.sha_pinning_required` | `table` rows = workflows (all repos), columns = actions, cell formatter = pin kind (chart panel is bare, so table-as-heatmap for self; ECharts heatmap later) | **High** — 13 plugin repos → `tap@main`; `sha_pinning_required=false` |
| 4.3.4 | **Secrets exposure map** | "Which secret can which workflow read, and from which trigger?" | `REFERENCES_SECRET` `{job, trigger_events}`, `DECLARES_SECRET`, `TRIGGERS_WORKFLOW` | `graph` (secret ← workflow ← trigger) or `table` grouped by secret | Medium — `OPENAI_API_KEY` reachable via `workflow_run` from a PR-triggered capture; dead `TAP_CORE_RO_PAT` reference |
| 4.3.5 | **Bot activity timeline** | "What are the machines doing to our repos, and is anyone merging it?" | `pull_request` + `OPENS_PULL_REQUEST` from `github_app`, `CHECKS_PULL_REQUEST`, labels | `table` grouped by author app, sorted by age (timeline chart later) | Medium — open Renovate/release PRs age; 0 Dependabot PRs because there is no `dependabot.yml` |
| 4.3.6 | **Release chain** | "How does a version number become bytes someone can pull, and is each hop proven?" | releases, runs on `refs/tags/*`, `publish-release-tags` / `publish-images` workflows, attestation presence (friends via OCI) | small `graph` projection: release-please PR → tag → Release → run → image tag | Medium — surfaces the v0.1.2/v0.1.3 race class and the "0 assets" releases |
| 4.3.7 | **Posture grid** | "Which repo is the weakest link?" | `repository.configuration.security`, `actions_policy`, `merge_policy`, rulesets applied, required-check presence, CODEOWNERS presence, environments/webhooks | `table` repo × feature with `tickDash` | Medium — orphan `copilot` environments, Codacy hook, 77 alerts on `tap` |

The "teaches us something we did not already know" test: 4.3.1–4.3.3 already did during this pass
(items 1–4 in section 1.3). Build those three first; 4.3.7 is nearly free once posture fields land.

---

## 5. Delta from the plugin estate

- `identity_core` — already used (`oidc_issuer`, `TRUSTS_ISSUER`, `ENABLED_ON` source). git-serious reuses
  it for the Actions OIDC issuer and, at friends, for PyPI trusted publishing / attestation identities.
- `sigstore_core` — `rekor_log_entry`, `sigstore_ca`, edges `ATTESTED_BY`, `SIGNED_BY_IDENTITY`,
  `CERT_ISSUED_BY`, `IDENTITY_VOUCHED_BY`, `REQUESTS_SIGSTORE_SIGNATURE`: the release chain's
  "is this hop proven" question is exactly `github_release`/image `ATTESTED_BY` a Rekor entry whose cert
  was issued to the `token.actions.githubusercontent.com` identity. Friends/public-alpha ("sigstore-signed
  images" issue #10). Do not model attestations in github_core.
- `compliance_core` — `compliance_finding` / `HAS_COMPLIANCE_FINDING` is the right home for
  "unpinned action", "app with org-wide write", "no required check" once git-serious emits findings
  (the README's "agent-driven security review"). Later; self renders the facts, not verdicts.
- `computing_core` — `program`, `file`, `public_key`, `user`, `web_host`: not needed for self. A
  workflow's `raw_yaml` could become a `file` node later for code-paths; skip.
- `aws_core` — `FEDERATES_VIA` / `REFERENCES_RESOURCE` remain the samsite bridge; git-serious standalone
  must work with zero AWS nodes (already true: enrichment warns on zero candidates).
- `administrivia` — pages/panels infrastructure only; no vocabulary.
- `samsite`, `fedramp_20x_ksi`, `grid_fixtures`, `gryphon_playground`, `roscale` — no vocabulary to reuse;
  `finding_strip` (KPI tiles) is the one thing git-serious would *want* from `fedramp_20x_ksi` and must not
  take (dependency direction).
- `git_core` extraction (tap#144) would pull from github_core: `github_repository` → `repository`,
  `git_branch`, `pull_request`, `github_release` → `release`, `github_environment`, the neutral halves of
  `workflow`/`run`/`job` (`pipeline`/`pipeline_run`/`job`), and `ruleset` → `protection_rule` with a
  `github_ruleset` detail node kept GitHub-side. `identity_core` is the proof this pattern works.

---

## 6. Recommended build order (self milestone; first-light Aug 28, done-test Aug 30)

All in `github_core` (+ page/instances in `git-serious-tap`). S ≈ ½ day, M ≈ 1 day.

| Order | Task | Size | Lands by | Notes |
| --- | --- | --- | --- | --- |
| 1 | Finish org-scope collection: enumerate `orgs/{org}/repos`, run existing per-repo walk over all 19 repos, org node as `github_account` | S (in progress) | Aug 27 | first-light prerequisite |
| 2 | Posture fields on `repository.configuration` (`security`, `merge_policy`, `actions_policy`, `webhooks[]`, `codeowners`) + org `org_policy`; JSON schemas with descriptions | S | Aug 27 | no migrations; feeds hero + posture grid |
| 3 | `github-org-hero` KPI strip panel type + `/git-serious` page GRIFT in `git-serious-tap` with hero, intro text, org-wide activity table (Search + standard `table`), posture table | M | **Aug 28 first-light** | proves composition-only product plugin boots (product-map open question) |
| 4 | `git_branch` + `github_ruleset` + `status_check` models, `HAS_BRANCH`, `ENFORCED_ON`, `REQUIRES_CHECK`, `PRODUCES_CHECK` (derived, link-manifest rule) | M | Aug 29 | the gate; one migration |
| 5 | `app_installation` model + `INSTANCE_OF_APP`, `HOSTS_INSTALLATION`; `MEMBER_OF_ORG`, `HAS_REPO_PERMISSION`, `REVIEWS_AS_CODEOWNER` edges | S | Aug 29 | who/what can act |
| 6 | Gate graph projection (4.3.1) + actors/apps tables (4.3.2) on the landing page | M | **Aug 30 done-test** | the view that surprises |
| 7 | `github_action` node + `USES_ACTION` / `CALLS_WORKFLOW` / `TRIGGERS_WORKFLOW` (parser already has `uses` per job; add pin-kind derivation + step-level scan) + pin table (4.3.3) | M | Aug 31 | slips past Aug 30 if 4–6 run long; still self |
| 8 | `pull_request` + `OPENS_PULL_REQUEST` (account/app) + `CHECKS_PULL_REQUEST` + bot activity table (4.3.5) | M | Sep 1 | closes backlog `OPENS_PR` |
| 9 | `actions_secret` / `github_environment` + `DECLARES_*`, `REFERENCES_SECRET` (trigger-aware) + secrets map (4.3.4) | S–M | Sep 2 | closes backlog `references` (secrets half) |
| 10 | Icons: `get-octicon` mini-skill, 12 new keys, NOTICE update; `DEFAULT_DISPLAY` palette for governance nodes (distinct from the Actions blue — e.g. a neutral slate for rules/checks, amber for credentials) | S | alongside 4–9 | |
| 11 | `github_release` + `PUBLISHES_RELEASE` + release-chain mini graph (4.3.6) | S | friends | packages via OCI at friends |
| 12 | Spec: `spec-github-core-org-v0.md` (new models, edges, dims, unobservable surfaces, `git_core`-earmarks) + `spec-git-serious-org-landing-page-v0.md` (story sentence, panels, layout) — written first for each task per house rule | S each | with each task | |

Decision points to raise with George, not decide here: (a) extract `git_core` between self and friends
or accept a post-friends migration (2.3); (b) whether avatar/logo hotlinking is ever on by default
(3); (c) whether git-serious should *emit* findings in self (recommend no — facts only until
`compliance_core` is wired at friends+); (d) whether the collector's own PAT should be visible to
itself via `pat_grant` (a nice honesty signal, but needs an org-owner-issued token with the PAT-read
permission).
