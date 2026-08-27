---
title: Concept dictionaries — 16 platform, graph and tooling models
date: 2026-08-27
status: research
audience:
  - developer
  - llm
related_docs:
  - docs/doc-git-serious-cicd-shape-review.md
  - docs/doc-git-serious-cicd-security-prior-art.md
---

> **Research pass, 2026-08-27.** API taxonomies, published graph schemas, event vocabularies and infrastructure-as-code resource lists, including a direct diff against the two published GitHub graph models.
> One of four gathering passes behind the domain vocabulary corpus, which lives with the
> vocabulary's owner as `spec-github-core-vocabulary.md`. Written by an AI research agent;
> claims carry citations and the report flags what it could not verify. Not canon.

# Existing concept dictionaries for git-serious — platform APIs, graph models, and tooling schemas

**Research pass:** 2026-08-27 · **Scope:** the *platform and tooling models* direction of
`build-domain-vocabulary` Step 2. A sibling pass covers security/compliance standards
(OCSF, STIX, ATT&CK, SLSA, in-toto, CycloneDX, SPDX, NIST, CIS, OpenSSF) and is not duplicated here.

**What this is for.** git-serious projects a software project's CI/CD system onto an
entity/relationship graph. Before inventing vocabulary we want the lists other people already
argued about — the same reasoning that made us adopt Octicons rather than draw icons.
This report is raw research; it feeds a corpus document, it is not one.

**Honesty notes, up front.**

- The WebSearch budget for this session was exhausted early. Everything below was gathered by
  fetching primary artifacts directly (GitHub API, raw schema files, tarballs, docs pages).
  That is a *better* method for schema lists, but it means discovery of sources I did not already
  know to look for was limited. Gaps are flagged inline rather than papered over.
- Where a count or a date is uncertain I say so. Several of these projects rewrite git history
  (squash-published repos), so "first commit" is not a reliable origin date.

---

## Part A — Graph models of a GitHub organization (primary prior art)

### A1. SpecterOps BloodHound "OpenGraph" GitHub extension

This is the single most directly comparable vocabulary in existence: a published, versioned,
machine-readable list of node kinds and edge kinds for exactly our domain. It converts our survey
into a diff. **Read this section as the core of the report.**

#### A1.1 There are two repos, and they are not the same model

The task brief described "~27 node kinds and ~152 edge kinds". Both numbers are close to something
real, but they belong to different artifacts. What actually exists today:

| Repo | What it is | Schema version | Node kinds | Edge kinds | Licence | Last pushed |
|---|---|---|---|---|---|---|
| [`SpecterOps/GitHound`](https://github.com/SpecterOps/GitHound) | The original PowerShell collector (`Invoke-GitHound`). Fullest **workflow** model. | `GitHound` **v1.0.0** (`Documentation/Schema.md`) | **34** | **122** documented | Apache-2.0 | 2026-08-10 |
| [`SpecterOps/openhound-github`](https://github.com/SpecterOps/openhound-github) | The Python/DLT rewrite on the OpenHound framework. Fullest **enterprise + identity** model. | `SOGitHub` **v1.3.1** (`extension/schema.json`) | **40** | **148** registered | Apache-2.0 | 2026-08-25 |

The `152` in the brief matches the count of string constants in
[`src/openhound_github/kinds/edges.py`](https://github.com/SpecterOps/openhound-github/blob/main/src/openhound_github/kinds/edges.py)
(152 quoted literals, including the `SAML_*` and `SCIM_*` cross-extension kinds that are registered
by *sibling* extensions rather than by this one). The `27` does not match anything I found; the
node count has been 34 or 40 in every artifact I could read. **Flagging this as unresolved** — the
brief's numbers may come from the ~2025-07 launch announcement, which I could not retrieve
(no WebSearch budget, and the repos' git history is squashed).

Supporting repos: [`SpecterOps/OpenHound`](https://github.com/SpecterOps/OpenHound) (the collector
framework, v0.3.1, 2026-08-21), [`SpecterOps/og-docs-automation`](https://github.com/SpecterOps/og-docs-automation)
(generates `Schema.md` from `schema.json`).

#### A1.2 The machine-readable contract is itself worth stealing

`extension/schema.json` is a small, clean, *published* dictionary format. Its shape:

```json
{ "schema":  { "name": "SOGitHub", "display_name": "…", "version": "v1.3.1", "namespace": "GH" },
  "node_kinds": [ { "name": "GH_Repository", "display_name": "GitHub Repository",
                    "description": "…", "is_display_kind": true, "icon": "book", "color": "#9EECFF" } ],
  "relationship_kinds": [ { "name": "GH_HasSecret", "description": "…", "is_traversable": true } ],
  "environments": [ { "environment_kind": "GH_Organization", "source_kind": "GitHub",
                      "principal_kinds": ["GH_User"] } ],
  "relationship_findings": [] }
```

Three ideas in there are directly relevant to our AI-integration posture (declarative, described,
queryable metadata over human-only prose):

1. **Every kind carries a human description in the schema**, not only in docs. An agent reading the
   schema alone can explain the graph.
2. **`is_traversable` is a first-class per-edge property.** BloodHound distinguishes *this
   relationship exists* from *an attacker can walk this*. Only **28 of 148** edges are traversable.
   This is the same discipline as our skill's "shape is not severity" rule, expressed as a schema
   field rather than as edge properties. We have no equivalent flag.
3. **`environments` declares the tenancy root and the principal kinds** — the analogue of our
   dimensions, declared rather than inferred.

Also published alongside: 56 **saved searches** (named Cypher queries, `extension/saved_searches/`)
and 11 **privilege-zone rules** (`extension/privilege_zone_rules/`, "what counts as Tier Zero").
A saved-query library is a vocabulary artifact in its own right — it shows which paths the authors
consider worth naming.

#### A1.3 What the model is *about* (and why it differs from ours)

BloodHound's GitHub model is an **attack-path model of a GitHub organisation's configuration**.
Its centre of gravity is *role → capability → resource*: roughly 100 of its 148 edges are
"[Repository]/[Organization]/[Enterprise] role can do X" permission edges emitted from
`GH_RepoRole` / `GH_OrgRole` / `GH_EnterpriseRole` nodes.

The consequence that matters most for us:

> **BloodHound models workflow *definitions*, never workflow *executions*.**
> `GH_Workflow`, `GH_WorkflowJob`, `GH_WorkflowStep` are all parsed out of the workflow YAML.
> There is no node for a run, an attempt, a conclusion, a duration, or a deployment event.
> Their `GH_WorkflowJob` is a job *declaration*; our `github_actions_job` is a job *execution*.

The two models are therefore **complementary, not competing**. They share a spine
(platform → org → repo → workflow) and diverge immediately after it: BloodHound goes down into
*who can reach what*, we go down into *what actually ran and how it went*.

#### A1.4 Node kinds — the union of both repos (41 distinct)

Grouped by layer. `†` = present in `openhound-github` v1.3.1 only; `‡` = `GitHound` v1.0.0 only;
unmarked = both.

| Layer | Node kinds |
|---|---|
| **Platform / tenancy** | `GH_Enterprise`, `GH_Organization` |
| **Repository** | `GH_Repository`, `GH_Branch`, `GH_BranchProtectionRule` |
| **Actions — definition side** | `GH_Workflow`, `GH_WorkflowJob`, `GH_WorkflowStep` |
| **Actions — environments** | `GH_Environment`, `GH_EnvironmentBranchPolicy` † |
| **Actions — secrets/variables** | `GH_OrgSecret`, `GH_RepoSecret`, `GH_EnvironmentSecret`, `GH_OrgVariable`, `GH_RepoVariable`, `GH_EnvironmentVariable`, plus the generic labels `GH_Secret` †, `GH_Variable` † |
| **Actions — compute** | `GH_Runner` †, `GH_RunnerGroup`, `GH_EnterpriseRunner` †, `GH_EnterpriseRunnerGroup` †, `GH_OrgRunner`, `GH_OrgRunnerGroup` †, `GH_RepoRunner` |
| **Principals** | `GH_User`, `GH_Team`, `GH_EnterpriseTeam`, `GH_EnterpriseManagedUser` |
| **Roles (reified!)** | `GH_OrgRole`, `GH_TeamRole`, `GH_RepoRole`, `GH_EnterpriseRole` |
| **Applications / credentials** | `GH_App`, `GH_AppInstallation`, `GH_PersonalAccessToken`, `GH_PersonalAccessTokenRequest` |
| **Federated identity** | `GH_SamlIdentityProvider`, `GH_ExternalIdentity` |
| **Security findings** | `GH_SecretScanningAlert` |

Plus kinds this extension *references* but a sibling extension owns:
`SAML_FederationProvider`, `SAML_ServiceProvider`, `SAML_Issuer`, `SAML_AssertionConsumerService`,
`SAML_ClaimMapping`; `SCIM_Organization`, `SCIM_User`, `SCIM_Group`, `SCIM_Role`; `Okta_User`;
and the cloud-side targets `AZFederatedIdentityCredential` and `AWSRole`.

Four observations worth carrying forward:

- **Roles are reified as nodes, not as edge properties.** `GH_User -HasRole-> GH_RepoRole -AdminTo-> GH_Repository`.
  This is the single biggest structural difference from anything else in this report. It is what
  lets one permission edge be authored once per *role* instead of once per (user, repo) pair, and it
  makes role inheritance (`GH_HasBaseRole`) expressible. It costs a hop in every query.
- **Secrets are split by scope into distinct kinds** (`Org`/`Repo`/`Environment`), with a generic
  `GH_Secret` label applied *in addition* for cross-scope queries. That is a deliberate
  "specific kind + generic supertype label" pattern, available because Neo4j nodes take multiple labels.
  Our grid has one type per node, so we would express this as one `actions_secret` type with a
  `scope` enum — the shape review already proposes exactly that.
- **Runners are split by scope too** (`Enterprise`/`Org`/`Repo`) with a generic `GH_Runner` label.
  Ours is a single `github_runner`.
- **No `GH_PullRequest`, no `GH_Commit`, no `GH_Release`, no `GH_Tag`, no `GH_Issue`, no `GH_Package`,
  no `GH_Ruleset`, no `GH_CheckRun`, no `GH_Deployment`, no `GH_Webhook`, no `GH_DeployKey`.**
  Several exist only as *verbs* (`GH_CreateTag`, `GH_ClosePullRequest`) — a permission to act on a
  thing that is never itself modelled. `GH_BranchProtectionRule` is modelled but **rulesets are not**
  (there is a `tests/test_repository_rulesets.py`, so collection may exist without a node kind —
  uncertain, flagging).

#### A1.5 Edge kinds

The full 148-row table with descriptions and traversability is at
`scratchpad/bloodhound-github-schema.json`; the source→target pairs for 118 edges are at
`scratchpad/bloodhound-github-edge-endpoints.txt`. Summarised by family:

| Family | Count | Examples |
|---|---:|---|
| Repo-role capability ("repo role can X") | ~55 | `GH_ReadRepoContents`, `GH_WriteRepoContents`, `GH_WriteRepoPullRequests`, `GH_AdminTo`, `GH_CreateTag`, `GH_ManageWebhooks`, `GH_ManageDeployKeys`, `GH_EditRepoProtections`, `GH_JumpMergeQueue`, the 13 discussion verbs |
| Org-role capability | ~20 | `GH_CreateRepository`, `GH_InviteMember`, `GH_AddCollaborator`, `GH_TransferRepository`, `GH_WriteOrganizationActionsSecrets`, `GH_ManageOrganizationWebhooks` |
| Enterprise-role capability | 22 | `GH_ManageEnterpriseAdmins`, `GH_WriteEnterpriseSso`, `GH_ReadEnterpriseAuditLog`, `GH_ViewEnterpriseBilling` |
| **Structural containment** | 8 | `GH_Contains`, `GH_Owns`, `GH_HasBranch`‡, `GH_HasWorkflow`‡, `GH_HasJob`‡, `GH_HasStep`‡, `GH_HasEnvironment`‡, `GH_HasRunner`† |
| **Principal / role wiring** | 6 | `GH_HasRole`, `GH_HasBaseRole`, `GH_MemberOf`, `GH_HasMember`, `GH_AddMember`, `GH_AssignedTo` |
| **Actions dataflow** | 7 | `GH_UsesSecret`, `GH_UsesVariable`, `GH_HasSecret`, `GH_HasVariable`, `GH_CallsWorkflow`, `GH_DependsOn`, `GH_DeploysTo` |
| **Compute reachability** | 4 | `GH_CanUseRunner`, `GH_CanDispatchTo`‡, `GH_IsEligibleFor`†, `GH_InheritedFrom`† |
| **Identity / federation** | 7 | `GH_CanAssumeIdentity`, `GH_SyncedTo`, `GH_MapsToUser`, `GH_HasExternalIdentity`, `GH_HasSamlIdentityProvider`, `GH_InstalledAs`, `GH_CanAccess` |
| **Credentials** | 3 | `GH_HasPersonalAccessToken`, `GH_HasPersonalAccessTokenRequest`, `GH_ValidToken` |
| **Protection** | 4 | `GH_ProtectedBy`, `GH_RestrictionsCanPush`, `GH_BypassPullRequestAllowances`, `GH_BypassBranchProtection` |
| **Computed attack-path edges** | 9 | see below |

**The computed edges are the interesting ones** — these are *derived*, not observed, and each one is
a small policy engine. This is the technique worth learning from, independent of the vocabulary:

| Edge | Source → Target | What it computes |
|---|---|---|
| `GH_CanWriteBranch` | `GH_RepoRole`/`GH_User`/`GH_Team` → `GH_Branch` | push permission **after** evaluating branch protection, push restrictions and bypass allowances |
| `GH_CanCreateBranch` | same → `GH_Repository` | can create an *unprotected* branch that bypasses the merge gate |
| `GH_CanEditProtection` | `GH_RepoRole` → `GH_Repository`/`GH_Branch` | can modify or remove protection rules |
| `GH_CanPwnRequest` | `GH_RepoRole` → `GH_Repository`/`GH_Branch` | `pull_request_target` + attacker-controlled `actions/checkout` ref + forkability + read access |
| `GH_CanAssumeIdentity` | `GH_Repository`/`GH_Branch`/`GH_Environment` → `AZFederatedIdentityCredential`/`AWSRole` | OIDC `sub` claim matched against cloud workload-identity federation config |
| `GH_CanDeployToEnvironment` | repo/branch/role/reviewer → `GH_Environment` | after evaluating deployment branch policies and required reviewers |
| `GH_CanCreateEnvironment` | `GH_RepoRole` → repo | can create an environment by editing a workflow that names a nonexistent one |
| `GH_CanReadSecret` | `GH_OrgRole` → org secret | can read an org secret **by creating a repository in its scope** |
| `GH_CanCreateRepositoryWithRunnerAccess` | `GH_OrgRole` → runner group | same trick, aimed at compute |

`GH_CanPwnRequest`'s published derivation is unusually explicit — trigger is `pull_request_target`,
a step uses `actions/checkout` with `ref` in
`${{ github.event.pull_request.head.sha | .head.ref | github.head_ref }}`, the repo is forkable by
the role holder (public, or `members_can_fork_private_repositories` **and** `allow_forking`), and
the role has read. Branch targeting honours the trigger's `branches:` filter. That is a spec we
could implement against directly.

Note also the honesty in their traversability calls: `GH_CanUseRunner` and `GH_CanDispatchTo` are
documented as *deliberately non-traversable* — "scheduler eligibility and configuration evidence,
but not by itself a proven control path". (In v1.3.1 `GH_CanUseRunner` has since been flipped to
traversable, and the `GH_CanUseRunner.md` description file still contains **both** the old and new
justification paragraphs, contradicting itself. A real drift artifact, not a criticism worth much —
but a reminder that a published dictionary still needs a drift guard.)

#### A1.6 Verdict

| | |
|---|---|
| **Artifact kind** | Graph model (node/edge kind registry) + collector + query library |
| **Licence** | **Apache-2.0** on all of `GitHound`, `openhound-github`, `OpenHound`. Names and descriptions are reusable with attribution. |
| **Verdict** | **ALIGN** (strongly), and **ADOPT** selectively |

**ALIGN, not ADOPT wholesale**, because the model answers a different question. Their `GH_`-prefixed
names are BloodHound namespace convention (BloodHound requires a namespace per extension) and we
should not import the prefix. But where we model the same thing we should use their *word*:
`Environment`, `Runner`, `RunnerGroup`, `Workflow`, `WorkflowJob`, `WorkflowStep`,
`BranchProtectionRule`, `AppInstallation`, `ExternalIdentity`, `SecretScanningAlert`.

**ADOPT specifically:**
- the `is_traversable`-style per-edge flag, generalised: an edge property that says whether this
  edge asserts *capability* or merely *configuration adjacency*;
- the schema-carries-descriptions discipline (we already do this via edge JSON files — worth
  checking parity);
- the published saved-query library as a product artifact;
- the derivation of `GH_CanPwnRequest` and `GH_CanAssumeIdentity` as concrete algorithms.

**Do not adopt:** the reified `*Role` node layer (four extra node types and a mandatory extra hop,
justified by attack-path analysis and not by our use case), and the ~100 fine-grained permission
edges (`GH_ToggleDiscussionCommentMinimize` and friends) — that is the "adopting a dictionary
wholesale" failure mode in its purest form.

### A2. Cartography (CNCF Sandbox) — **ADOPT the ontology, ALIGN the structure**

| | |
|---|---|
| Version | release **0.140.0**, 2026-08-11 (releases roughly fortnightly; last push 2026-08-27) |
| URL | **https://github.com/cartography-cncf/cartography** — ⚠️ **`lyft/cartography` is dead**; the repo moved to the CNCF org and the old path 404s |
| Artifact kind | Executable graph model — typed Python dataclasses → Neo4j |
| Licence | **Apache-2.0** |

⚠️ **A second correction to the brief:** `docs/root/modules/github/schema.md` no longer exists. Schema
docs are now **generated from the Python models at docs-build time**
(https://cartography-cncf.github.io/cartography/modules/github/schema.html). The authoritative
machine-readable source is `cartography/models/github/*.py`. That is itself a good precedent —
the model is *data*, and the docs are derived from it.

**Node labels — 25 distinct across 26 schemas:** `GitHubOrganization`, `GitHubUser`, `GitHubTeam`,
`GitHubRepository`, `GitHubBranch`, `ProgrammingLanguage`, `PythonLibrary`, `GitHubDependency`,
`GitHubDependencyGraphManifest`, `GitHubCodeOwnerRule`, `GitHubBranchProtectionRule`,
**`GitHubRuleset`**, **`GitHubRulesetRule`**, `GitHubWorkflow`, **`GitHubAction`**,
`GitHubActionsSecret`, `GitHubActionsVariable`, `GitHubEnvironment`, `GitHubPersonalAccessToken`,
`GitHubPackage`, `GitHubContainerImage`, `GitHubContainerImageLayer`, `GitHubContainerImageTag`,
`GitHubContainerImageAttestation`, `GitHubDependabotAlert`.

**Relationship types:** `RESOURCE` (tenancy spine, on nearly every node), `OWNER`, `MEMBER_OF`,
`ADMIN_OF`, `UNAFFILIATED`, `MEMBER`, `MAINTAINER`, `MEMBER_OF_TEAM`, `BRANCH`, `LANGUAGE`,
`HAS_RULE`, `HAS_RULESET`, `CONTAINS_RULE`, `HAS_CODEOWNER_RULE`, `HAS_ENVIRONMENT`, `HAS_PACKAGE`,
`REQUIRES`, `HAS_MANIFEST`, `HAS_DEP`, `MATCHES_CODEOWNER_RULE`, **`HAS_WORKFLOW`**,
**`USES_ACTION`**, **`REFERENCES_SECRET`**, `HAS_SECRET`, `HAS_VARIABLE`, `COMMITTED_TO`,
`OWNS`/`OWNED_BY`, `CAN_ACCESS`, `CODEOWNER`, `FOUND_IN`, `DISMISSED_BY`, `ASSIGNED_TO`,
plus the container-provenance chain `HAS_IMAGE`, `REPO_IMAGE`, `IMAGE`, `HAS_LAYER`/`HEAD`/`TAIL`,
`NEXT`, `CONTAINS_IMAGE`, **`BUILT_FROM`**, `ATTESTS`, **`PACKAGED_FROM`**, **`PACKAGED_BY`**.

Permission edges are a **generated cross-product**: `(GitHubTeam)-[ADMIN|MAINTAIN|READ|TRIAGE|WRITE]->(GitHubRepository)`
and `DIRECT_COLLAB_{ADMIN,MAINTAIN,READ,TRIAGE,WRITE}` / `OUTSIDE_COLLAB_{…}` from
`(GitHubUser)->(GitHubRepository)` — 15 edge labels from two constants.
**This is a design choice we should decline**: it puts the permission level in the *edge name*
rather than in an edge *property*, which multiplies the type registry and defeats
"give me all access edges" queries. Our `HAS_REPO_PERMISSION {permission, via}` proposal is better.

#### A2.1 The Ontology layer — the most reusable artifact in this whole report

This was not in the brief and is the find of the survey. Cartography maintains a **cross-provider
semantic label vocabulary** (`cartography/models/ontology/labels.py`) and — critically — a
**guard-enforced canonical edge-naming table** (`ontology/constraints.py`).

**43 ontology labels**, each "a cross-provider X resource": `AIModel`, `APIKey`, `BlockStorage`,
**`CICDPipeline`**, `CVE`, `Certificate`, **`CodeRepository`**, `ComputeCluster`, `ComputeInstance`,
`ComputeNamespace`, `ComputePod`, `ComputeService`, `Container`, `ContainerRegistry`, `DNSRecord`,
`DNSZone`, `Database`, `EncryptionKey`, `FileStorage`, `FilesystemSnapshot`, `Function`,
`IdentityProvider`, `Image`, `ImageAttestation`, `ImageLayer`, `ImageManifestList`, `ImageTag`,
`LoadBalancer`, `NetworkAccessControl`, `ObjectStorage`, `Ontology`, `PermissionRole`, **`Secret`**,
`SecurityIssue`, `ServiceAccount`, `Snapshot`, `Subnet`, `Tag`, `Tenant`, `ThirdPartyApp`,
`UserAccount`, `UserGroup`, `VirtualNetwork`.

`ONTOLOGY_REL_CONSTRAINTS` states: *if a node carrying ontology label `src` has an outward edge to
`dst`, that edge **must** be named `label`.* The CI/CD-relevant entries:

```
(Image)              -[PACKAGED_FROM]->  (CodeRepository)   # built from a source repo (CI provenance)
(PackageVersion)     -[DEPLOYED]->       (Image | FilesystemSnapshot)
(Package)            -[HAS_VERSION]->    (PackageVersion)
(CVE | SecurityIssue)-[AFFECTS]->        (PackageVersion | FilesystemSnapshot)
(Container|Function) -[RESOLVED_IMAGE]-> (Image)
(UserAccount|ServiceAccount|UserGroup) -[MEMBER_OF]-> (UserGroup)
(UserAccount|ServiceAccount|UserGroup) -[HAS_ROLE]->  (PermissionRole)
(PermissionRole)     -[INCLUDES]->       (PermissionRole)
(APIKey)             -[OWNED_BY]->       (UserAccount | ServiceAccount)
(User)               -[HAS_ACCOUNT]->    (UserAccount)
(ComputePod|Function|ComputeInstance) -[USES_SECRET]-> (Secret)
```

And an honestly-documented open problem worth quoting in our corpus verbatim:

> `// NOTE: no UserAccount->CodeRepository constraint. Several distinct edges legitimately span that
> pair (COMMITTED_TO commit authorship, OWNER ownership, DIRECT_COLLAB_*/OUTSIDE_COLLAB_* access
> grants), so a single canonical label cannot be enforced here yet.`

**`CICDPipeline` normalisation** (`ontology/mapping/data/cicdpipelines.py`): every provider maps to
`_ont_name`, `_ont_type ∈ {build, deploy, iac}`, `_ont_status ∈ {active, disabled, unknown}`.
Mapped today: `AWSCodeBuildProject`(build), **`GitHubWorkflow`(build)**, `GitLabCIConfig`(build),
`SpaceliftStack`(**iac**), `CircleCIPipeline`(build). Azure Data Factory is **deliberately excluded**
with a written rationale ("ETL, not CI/CD — mapping them would pollute supply-chain inventory
queries"). **A rejected-candidate register with reasons — exactly what our corpus Step 7.3 requires.**

**Three things to adopt:**
1. The **edge-name constraint table** as a validation surface. It is a guard we could implement
   directly, and it is the antidote to "every plugin invents its own word for containment".
2. **`_ont_type ∈ {build, deploy, iac}`** for pipelines — we will hit this exact problem.
3. The **semantic label over concrete label** pattern: `GitHubWorkflow` *is a* `CICDPipeline`.
   This maps 1:1 onto our Entity-spine + typed-BaseModel split and is how cross-forge queries stay
   possible without a lossy normalisation pass.

**Two things to decline:** the bidirectional duplication (`OWNS`/`OWNED_BY`, `MEMBER`/`MEMBER_OF`,
`HAS_RULE` vs `CONTAINS_RULE`) — query convenience that violates derive-a-fact-once; and the
permission-in-the-edge-name cross-product.

⚠️ **Same blind spot as BloodHound:** Cartography has `GitHubWorkflow` (the `.yml`) but **no
`WorkflowRun`, `Job`, or `Step`**. Across its whole estate only the **Spacelift** module models an
execution (`SpaceliftRun`, with `GENERATED`, `TRIGGERED`, `COMMITTED`, `PUSHED`, `CONFIRMED` edges).

**Adjacent modules with reusable vocabulary:** CircleCI (`CircleCIPipeline`(CICDPipeline),
`CircleCIContext`, `CircleCIOidcConfig`, **`BUILDS`** edge to a repo), GitLab
(`GitLabCIConfig`(CICDPipeline), `GitLabRunner`, `GitLabCIVariable`, `GitLabEnvironment`),
Spacelift (the only run model), **zizmor** (`ZizmorFinding` → `AFFECTS` → `GitHubWorkflow`/`GitHubAction`
— a GitHub Actions static analyser already wired into a graph).

### A3. GUAC (OpenSSF) — **ALIGN, with one ADOPT**

| | |
|---|---|
| Version | **v1.1.0**, 2026-03-13 (v1.0.0 2025-06-12; last push 2026-08-26) |
| URL | https://github.com/guacsec/guac · schema in `pkg/assembler/graphql/schema/*.graphql` (28 files) |
| Artifact kind | GraphQL schema doubling as the ontology definition |
| Licence | Apache-2.0 |

⚠️ The published ontology page (`docs.guac.sh/guac/guac-ontology-definition/`) is **stale relative to
the schema** — it still lists `IsVulnerability` (now `VulnEqual`) and separate `OSV`/`GHSA`/`CVE`
nodes (replaced by the generic `Vulnerability` trie). Read the `.graphql` files, not the docs.

**Nouns (6) + tries.** Packages, sources and vulnerabilities are **prefix tries**, so an attestation
can attach at any level of specificity:

- Package trie: `Package` (= the pURL *type* level) → `PackageNamespace` → `PackageName` → `PackageVersion`
  (+ `PackageQualifier`). `PackageName` is "the first node that can be referred to by other parts of GUAC."
- Source trie: `Source` (VCS type) → `SourceNamespace` (host) → `SourceName` (repo URL, with `tag` **xor** `commit`).
- Vulnerability trie: `Vulnerability` (type: `cve`/`ghsa`/`osv`/`snyk`/`novuln`) → `VulnerabilityID`.
- Flat: **`Artifact`** (`algorithm` + `digest` — the actual bytes), **`Builder`** (a bare `uri`), `License`.

**Verb / evidence nodes (17):** `IsDependency` (`dependencyType ∈ DIRECT|INDIRECT|UNKNOWN`),
**`IsOccurrence`** (`PackageOrSource → Artifact` — the abstract↔concrete bridge), `HasSBOM`,
`HasSLSA` (+ embedded `SLSA{builtFrom: [Artifact], builtBy: Builder, buildType, startedOn, finishedOn}`),
`HasSourceAt`, `CertifyVuln`, `CertifyVEXStatement`, `VulnEqual`, `VulnerabilityMetadata`,
`CertifyBad`, `CertifyGood`, `CertifyScorecard`, `CertifyLegal`, `HashEqual`, `PkgEqual`,
`PointOfContact`, `HasMetadata` (the generic escape hatch).

**How it models artifacts vs sources vs builders — the part worth internalising:**

| | Meaning | Concreteness |
|---|---|---|
| **Source** | *where code lives* (VCS type / host / repo / tag-or-commit) | abstract |
| **Package** | *how software is named for distribution* (pURL) | abstract — a `PackageVersion` is still a **name**, not bytes |
| **Artifact** | *the actual bytes* (`algorithm` + `digest`) | concrete |
| **`IsOccurrence`** | the bridge `PackageOrSource → Artifact` | it is an **evidence node**, so it carries who said so |
| **Builder** | a bare URI identity for whatever ran the build | participates in exactly one relationship |

**GUAC has no pipeline, job, step, or run entity at all.** A "build" exists only as an SLSA
attestation hanging off an artifact, and the `Builder` is a URI with no structure.

**ADOPT: the evidence-node pattern.** Every assertion is a first-class node carrying
`origin` / `collector` / `documentRef` / `justification` / `knownSince` — provenance *of the
provenance*. It solves "two scanners disagree" without a merge step. Our grid already puts provenance
on the spine, so this is convergent design rather than something to import — but it is strong
independent validation, and the `justification` field is one we do not have.

**ALIGN: the trie.** Modelling identity as a *path* rather than an opaque string is what lets a claim
attach at the right specificity ("all versions of `pkg:pypi/requests`" vs one version).

**Do not adopt: the `Edge` enum.** 86 members for 23 node types, mechanically named `SRC_DST` in both
directions. It carries no semantics and grows combinatorially — the opposite of Cartography's
approach and a clear warning for a graph that must stay human- and AI-legible.

### A4. Other SDLC / supply-chain graph models

**Eiffel (Ericsson / Eiffel Community)** — https://github.com/eiffel-community/eiffel, Apache-2.0,
latest edition `edition-orizaba` **2023-06-30** (branch still moves; likely maintenance mode).
24 event types, and **the richest named *link* vocabulary I found anywhere**: `ACTIVITY_EXECUTION`,
`ARTIFACT`, **`CAUSE`**, `CHANGE`, `COMPOSITION`, **`CONFIDENCE_BASIS`**, `CONFIGURATION`,
**`CONTEXT`**, `ELEMENT`, `ENVIRONMENT`, `FAILED_ISSUE`, **`FLOW_CONTEXT`**, `INCONCLUSIVE_ISSUE`,
`IUT` (Item Under Test), **`ORIGINAL_TRIGGER`**, **`PRECURSOR`**, `PREDECESSOR`, `PREVIOUS_VERSION`,
`RUNTIME_ENVIRONMENT`, `SUBJECT`, `SUB_CONFIDENCE_LEVEL`, `SUCCESSFUL_ISSUE`, `TEST_CASE_EXECUTION`,
`VERIFICATION_BASIS`.
**REFERENCE — steal the distinctions, not the protocol.** `CAUSE` vs `CONTEXT` vs `FLOW_CONTEXT` vs
`PRECURSOR` vs `ORIGINAL_TRIGGER` are five genuinely different "why did this happen" edges that every
other model collapses into one. Ten years of industrial CI/CD graph modelling; CDEvents is the
successor most tooling now targets.

**Protobom (OpenSSF)** — https://github.com/protobom/protobom, Apache-2.0, **v0.6.0, 2026-08-26**
(very active). A genuinely node+edge protobuf model (`api/sbom.proto`), unlike SPDX/CycloneDX themselves.
Its **44-member `Edge.Type` enum is the tool-neutral union of SPDX + CycloneDX relationship types** —
adopting it means not picking a side. The CI/CD-relevant distinctions it makes that others flatten:
**`buildDependency`, `buildTool`, `devDependency`, `devTool`, `testDependency`, `testTool`,
`runtimeDependency`** — *seven* senses of "depends on", where Cartography has one `REQUIRES` and GUAC
has `IsDependency{DIRECT|INDIRECT}`. Also `generates`/`generatedFrom` (the build-output edge pair) and
`SBOMType ∈ {DESIGN, SOURCE, BUILD, ANALYZED, DEPLOYED, RUNTIME, DISCOVERY, DECOMISSION}` (sic — the
typo is baked into the wire format). **ALIGN — take the edge vocabulary, not the node model**
(its `NodeType` is only `{PACKAGE, FILE}`; everything else is a property, which is right for SBOM
interop and wrong for a semantically queryable graph).

**OpenSSF Security Insights** — https://github.com/ossf/security-insights (⚠️ the
`security-insights-spec` path redirects here), **v2.2.0, 2026-01-31**. CUE schema →
`.github/security-insights.yml`. Entities: `Project`, `Repository`, `Contact`, **`SecurityTool`**,
`Attestation`, `Assessment`, `License`, `ReleaseDetails`, `VulnerabilityReporting`.
The find is `SecurityTool{type ∈ {fuzzing, container, secret, SCA, SAST, other},
integration{adhoc, ci, release}, results{adhoc, ci, release}}` — it cleanly separates *what tool*,
*when in the lifecycle it runs*, and *where the evidence lands*, all hangable off a repo node.
Plus `ReleaseDetails.automated-pipeline: bool`.
**ADOPT for the self-declared layer** — these are facts a scraper cannot observe (who the security
champion is, whether the release pipeline is automated). ⚠️ GitHub reports the licence as
**`NOASSERTION`** — verify the LICENSE text before vendoring schema content.

**Kusari** — builds *on* GUAC; publishes no separate ontology. `kusaridev/sscp` (Apache-2.0, last push
2025-04-22, 2 stars — experimental/abandoned) is interesting only as an existence proof that
"**CDEvents for the verb + SLSA for the evidence**" is a real composition. **REFERENCE (weak).**

**Endor Labs** — `https://docs.endorlabs.com/api-reference/topapi.v3.json` (608 KB, 416 schemas,
no dated version stamp, **proprietary docs**). 18 resource objects: `v1Project`, `v1PackageVersion`,
`v1DependencyMetadata`, `v1Finding`, `v1ScanResult`, `v1Policy`, `v1Vuln`, `v1Malware`, … Entity-modelled,
not graph-modelled — relationships are `project_uuid`/`target_uuid`/`parent_uuid` foreign keys plus a
generic `references` list. **Notably has no `Pipeline`, `Run`, or `Workflow` entity** — Endor models
the code and its dependencies, not the CI system. **REFERENCE** as a market cross-check only.

**Legit Security (`legitify`)** — its `internal/common/namespace/namespace.go` is the whole public
model: `enterprise`, `organization`, `repository`, `member`, **`actions`**, **`runner_group`**.
Six nouns, but empirically the minimum set to express SCM/CI security posture across GitHub *and*
GitLab — and note that the CI *system config* (`actions`) and the CI *compute* (`runner_group`) are
both first-class. **REFERENCE.**

**Chainguard** — `chainguard-dev/sdk` is a registry/IAM/advisory control-plane API
(`Repo`, `Tag`, `SyncConfig`, …). No SDLC entity-relationship model. **IGNORE.**

**Jit, Cycode, Arnica, OX Security** — no public entity/graph model found within a bounded search.
OX's public GraphQL docs reveal a useful *partition* (`application` / `artifact` / `pipeline` /
`issue` / **`cicd-issue`** as a distinct finding class) but the API is dashboard-shaped — there is no
`Pipeline` type, only pipeline *summaries*. They market an "attack path graph" and publish no schema.
**Flag as "not found in a bounded search", not "does not exist".**

**Pipeline-as-DAG models (Tekton, Argo Workflows, Jenkins).** None gives a *project-level* vocabulary
— they give the *inside* of one pipeline. But three independent systems converge on the same
decomposition, which is worth encoding:

- **Tekton** (`pkg/apis/pipeline/v1/pipeline_types.go`, Apache-2.0): `Pipeline` → `PipelineTask`
  with **`runAfter []string`** (explicit ordering), result-references (implicit data dependency),
  workspace-binding (shared state), and **`finally[]`** (always-run). Runtime counterparts
  `PipelineRun` / `TaskRun`; `Task` → `Step`s.
- **Argo Workflows** (`workflow_types.go`, Apache-2.0): `DAGTask{**dependencies []string**}` for
  control flow, `Artifact{**from**}` for data flow.
- **Jenkins `pipeline-graph-analysis-plugin`** (MIT): a *post-hoc execution* graph of `FlowNode`s
  (stage / parallel-branch / atom) grouped into `FlowChunk`s.

> **The transferable finding: a CI/CD graph needs at least two distinct edge kinds between steps —
> control-flow ordering and data/artifact flow — and they are not the same edge.**
> Our `HAS_ACTIONS_JOB` covers neither; GitHub's `needs:` is control-flow and `outputs`/`artifacts`
> is data-flow, and we currently flatten both into `workflow.configuration` JSON.

**Academic "pipeline-graph" literature: not covered.** The WebSearch budget was exhausted, and I will
not invent citations. This is a real gap in the survey — flagging it rather than papering over it.
## Part B — Vendor-neutral event and telemetry vocabularies

Event taxonomies are entity dictionaries in disguise: a list of *things that can happen* names the
things they happen to. These four barely overlap, which is what makes them useful together.

### B1. CDEvents (CD Foundation) — **ADOPT**

| | |
|---|---|
| Version | **v0.5.1**, 2026-04-15 (`version.txt`) |
| URL | https://github.com/cdevents/spec |
| Artifact kind | Prose spec + **45 per-event JSON Schemas** + 45 conformance payloads + SDKs |
| Licence | **Apache-2.0**; CDF **incubated**, governance in `cdevents/community` |
| Cadence | **~annual and irregular** — a 19-month gap between v0.4.1 (2024-05) and v0.5.0 (2025-12). A low-churn vocabulary, which is a *feature* for something you want to align to. |

**The complete subject set: 14 subjects across 6 stages, 45 event types.**
Event-type grammar is `dev.cdevents.<subject>.<predicate>.<major>.<minor>.<patch>` — **the schema
version is per-event, not per-spec-release**, so subjects mature independently.

| Stage | Subjects → predicates |
|---|---|
| **Core** | `pipelineRun` → queued, started, finished · `taskRun` → started, finished |
| **Source Code Version Control** | `repository` → created, modified, deleted · `branch` → created, deleted · `change` → created, reviewed, merged, abandoned, updated |
| **Continuous Integration** | `build` → queued, started, finished · `artifact` → packaged, signed, published, downloaded, deleted |
| **Testing** *(a separate top-level stage since v0.4)* | `testCaseRun` → queued, started, finished, skipped · `testSuiteRun` → queued, started, finished · `testOutput` → published |
| **Continuous Deployment** | `environment` → created, modified, deleted · `service` → deployed, upgraded, rolledback, removed, published |
| **Continuous Operations** | `incident` → detected, reported, resolved · `ticket` → created, updated, closed |

Two corrections to the brief's sketch, both verified against the schemas: the test subjects are
**`testCaseRun`/`testSuiteRun`** (the `Run` suffix is load-bearing — `testCase`/`testSuite` exist
only as *embedded reference objects*), and Testing is its own stage, not part of CI.

**Breaking changes in v0.5.0 that make most online material wrong:** `subject.type` was **removed**;
`context.version` → `context.specversion`; snake_case → **camelCase everywhere** (so it is
**`chainId`**, not `chain_id`); `outcome` standardised to `success | failure | cancel | error`.

**The links model is the edge concept, and it is deliberately half-built.**
`context.chainId` is a UUID bucket "for all CDEvents with some path to each other" — explicitly a
*secondary index* so you need not chase parents recursively. `context.links` carries embedded links
with four `linkType` values: **`START`**, **`END`**, **`PATH`** (from→to, causal), **`RELATION`**
(source→target with a `linkKind`). **`linkKind` is an open string, not an enum** — CDEvents ships no
controlled vocabulary of relation kinds. That is a real gap and an opportunity: it is exactly the
place where our edge-type registry would be the contribution.

**Patterns worth stealing verbatim:**
- Cross-subject references are uniformly **`{ id*, source }`** — a foreign key plus the originating
  system's scope. Identity is `(source, id)`, **never `id` alone**.
- Reusable embedded value objects: `sbom = {uri*}`, `trigger = {type*, uri}` with
  `type ∈ manual|pipeline|event|schedule|other`, `testCase`, `testSuite`.
- The **enum-or-string** (`anyOf: [enum, string]`) pattern on `ticketType`/`priority`/`resolution`:
  standardise the common values *without fail-closing on vendor-specific ones*. Directly applicable
  to our JSON-blob schema work.
- Artifacts are keyed by **purl**.

**Caveats:** the Python SDK is stale (last pushed 2024-01-19, pre-v0.5) — consume the JSON Schemas
directly. One upstream defect noted: `schemas/ticketclosed.json` still declares the removed
`subject.type`; every sibling schema omits it.

**Poll:** `https://raw.githubusercontent.com/cdevents/spec/main/version.txt` (one line — the cheapest
detector anywhere in this report); schemas at
`https://raw.githubusercontent.com/cdevents/spec/v0.5.1/schemas/<event>.json`; canonical hosted
schemas serve live at their `$id` (`https://cdevents.dev/0.5.1/schema/taskrun-finished-event`,
verified 200). **The 45 conformance payloads are a ready-made ingest test corpus.**

### B2. OpenTelemetry semantic conventions — **ALIGN**

| | |
|---|---|
| Version | **v1.44.0**, 2026-08-04 |
| URL | https://github.com/open-telemetry/semantic-conventions |
| Artifact kind | **YAML model** (`model/**/*.yaml` is the system of record) → generated Markdown |
| Licence | Apache-2.0 |
| Cadence | **Monthly** — ~40× faster than CDEvents. Budget a quarterly re-sync. |

**Stability:** OTel renamed `experimental` → `development`. **Every `cicd.*` and `vcs.*` attribute in
v1.44.0 is `release_candidate` — none is `stable`.** Names can and do still change (five
`vcs.repository.*` attributes were renamed to `vcs.ref.*`/`vcs.change.*` and are now deprecated).

**`cicd.*` registry — 16 attributes:** `cicd.pipeline.name`; `cicd.pipeline.run.{id, url.full, state}`;
`cicd.pipeline.result`; `cicd.pipeline.action.name`; `cicd.pipeline.task.{name, type}`;
`cicd.pipeline.task.run.{id, url.full, result}`; `cicd.worker.{id, name, url.full, state}`;
`cicd.system.component`.
Enums: `run.state ∈ pending|executing|finalizing`; `result ∈ success|failure|error|timeout|cancellation|skip`;
`action.name ∈ BUILD|RUN|SYNC`; `task.type ∈ build|test|deploy`; `worker.state ∈ available|busy|offline`.

**`vcs.*` registry — 16 attributes:** `vcs.repository.{url.full, name}`;
`vcs.ref.head.{name, type, revision}`; `vcs.ref.base.{name, type, revision}`; `vcs.ref.type`;
`vcs.change.{id, title, state}`; `vcs.revision_delta.direction`; `vcs.line_change.type`;
`vcs.owner.name`; `vcs.provider.name`.
Enums: `ref.*.type ∈ branch|tag`; `change.state ∈ open|wip|closed|merged`;
`revision_delta.direction ∈ ahead|behind`; `line_change.type ∈ added|removed`;
`provider.name ∈ github|gitlab|gitea|bitbucket`.

**Metrics** — `cicd.pipeline.run.{duration, active, errors}`, `cicd.worker.count`, `cicd.system.errors`;
`vcs.change.{count, duration, time_to_approval, time_to_merge}`, `vcs.repository.count`,
`vcs.ref.{count, lines_delta, revisions_delta, time}`, `vcs.contributor.count`.

**The `entities.yaml` files are the find.** OTel now has a first-class **entity** group type with
explicit **`identifying` vs `descriptive`** attribute roles, and metrics carry `entity_associations`:

| Entity | Identifying (the key) | Descriptive |
|---|---|---|
| `cicd.pipeline` | `cicd.pipeline.name` | — |
| `cicd.pipeline.run` | `cicd.pipeline.run.id` | `cicd.pipeline.run.url.full` |
| `cicd.worker` | `cicd.worker.id` | `cicd.worker.name`, `.url.full` |
| `vcs.repository` | **`vcs.repository.url.full`** | `vcs.repository.name` |
| `vcs.ref` *(development)* | **`vcs.ref.head.revision`** | `vcs.ref.head.name`, `vcs.ref.type` |

**Three identity choices worth adopting outright:**
1. **Repository identity is the canonical URL**, not a name or numeric id.
2. **A ref's identity is its revision**, not its name.
3. **`state` is orthogonal to `result`.** Measuring duration *per state* is how you separate
   queue-time from execute-time — something our `github_actions_run` cannot currently express
   (we have `run_started_at`/`completed_at` but no queued-vs-executing split).

**Adjacent namespaces that fill real gaps:** `model/artifact/registry.yaml` has `artifact.purl`,
`artifact.hash`, and **`artifact.attestation.{id, filename, hash}`**; `model/deployment/` has
**`deployment.environment.name` — the only `stable` attribute in this whole neighbourhood**
(well-known values `production`, `staging`, `test`, `development`).

**Known conflict to record:** OTel `test.case.result.status ∈ pass|fail` and
`test.suite.run.status ∈ success|failure|skipped|aborted|timed_out|in_progress` **disagree with**
CDEvents' `outcome ∈ success|failure|cancel|error` + `severity`. Any ingest of both needs a mapping table.

**Poll:** `model/cicd/{registry,entities,spans,metrics}.yaml` and `model/vcs/{registry,entities,metrics}.yaml`
at a pinned tag; diff `CHANGELOG.md`'s "🛑 Breaking changes 🛑" section. ⚠️ Releases carry **no assets**
and `model/version.properties` is the *file-format* version, not the semconv version — use the git tag.

### B3. Backstage Software Catalog — **ADOPT (relations + kinds)**

| | |
|---|---|
| Version | app **v1.54.5** (2026-08-25); **`@backstage/catalog-model` 1.10.0** (2026-08-18); entity `apiVersion` still **`backstage.io/v1alpha1`** since 2020 |
| URL | https://github.com/backstage/backstage |
| Artifact kind | draft-07 JSON Schema per kind + TS relation constants |
| Licence | Apache-2.0 (CNCF incubating) |
| Cadence | App churns weekly; **the model is near-frozen.** Poll the npm package version, not the repo releases. |

**Kinds (10):** `Component` (spec: `type`, `lifecycle`, `owner`, `system`, `subcomponentOf`,
`providesApis[]`, `consumesApis[]`, `dependsOn[]`), `API` (+ required `definition`), `Resource`,
`System`, `Domain`, `Group`, `User`, `Location`, `Template` (`scaffolder.backstage.io/v1beta3`),
and — newly — **`AiResource`**.

**Relations — 14 constants = 7 bidirectional pairs:**
`ownedBy`/`ownerOf` · `providesApi`/`apiProvidedBy` · `consumesApi`/`apiConsumedBy` ·
`dependsOn`/`dependencyOf` · `parentOf`/`childOf` · `memberOf`/`hasMember` · `partOf`/`hasPart`.
The docs label this list **non-exhaustive** — plugins add more.

**Two design rules that map straight onto our architecture and are worth quoting in the corpus:**

1. **"Entity descriptor YAML files are not supposed to contain [`relations`]."** Relations are
   *derived* by catalog processors from spec fields and surrounding artifacts, then attached
   read-only. That is derive-a-fact-once, applied to edges.
2. **"Where relations are produced, they are to be considered the authoritative source for that
   piece of data."** A consumer reads `relations[].ownedBy`, **not** `spec.owner` — because the owner
   may have come from CODEOWNERS rather than the YAML. **The edge is canonical; the declaring field
   is merely one possible input.** This is exactly the argument for making `REVIEWS_AS_CODEOWNER` an
   edge rather than a repository field.

Also worth adopting: the Kubernetes-derived **`labels` (identifying) vs `annotations`
(non-identifying)** split on metadata.

⚠️ **Relevant to our AI-integration posture:** the kinds directory now ships
`AiResource.v1alpha1.schema.json` ("contextual information consumed by AI coding tools, such as
skills and rules") with `skill`/`rule`/`plugin`/`marketplace` variants, plus
`API.v1alpha1.mcp-server.schema.json`. **Someone else has begun naming the agent-facing nouns.**
Worth tracking directly for spec-ai-integration.

**Reference-only for the rest:** `spec.type` and `spec.lifecycle` are deliberately *unconstrained
strings* — no enforceable controlled vocabulary. And Backstage has **no event model at all**:
entities are current-state documents with an `etag`, not a history. Backstage answers *what exists
and who owns it*; CDEvents answers *what happened*; our grid answers both because history is on the spine.

**Poll:** `https://registry.npmjs.org/@backstage/catalog-model` → `dist-tags.latest`.

### B4. Sigstore / Fulcio — **REFERENCE, with one carve-out to ADOPT**

Do not import Rekor's 11 entry kinds or the TUF/trust-root model — that is a cryptographic
verification domain we do not own.

**But carve out the Fulcio OID directory and adopt it as the CI identity attribute set.**
`sigstore/fulcio/docs/oid-info.md`, OID root `1.3.6.1.4.1.57264`, extensions `.1.8`–`.1.24`
(the GitHub-specific `.1.1`–`.1.6` are deprecated in favour of provider-generic). It is the only
vendor-neutral, cross-provider normalisation of *"which workflow, running where, on whose behalf,
from what source"* — and it ships a claim-mapping table across
**GitHub / GitLab / Buildkite / Codefresh / CircleCI / Buddy**.

Five things it names that **nothing else in this entire report does**:

| OID | Name | Why it matters to us |
|---|---|---|
| `.1.9` / `.1.18` | **Build Signer URI** vs **Build Config URI** | the workflow that *signed* is not the workflow that *initiated*. Two different edges. |
| `.1.11` | **Runner Environment** (`[platform]-hosted` \| `self-hosted`) | a trust-boundary attribute; we have `github_runner` but no hosted/self-hosted posture |
| `.1.15` / `.1.17` | **Source Repository / Owner Identifier** (immutable) | fixes the rename-and-transfer problem that OTel's URL-as-identity has. **We key on `full_name`, which is mutable — this is a real latent defect in our model.** |
| `.1.22` | **Source Repository Visibility At Signing** | a point-in-time fact; our grid's field history gives us this for free, which is a genuine advantage |
| `.1.24` | **Token Subject** — the raw OIDC `sub`, e.g. `repo:org/repo:ref:refs/heads/main` | the actual workload identity string our `FEDERATES_VIA` should carry as an edge property |

These are cheap to record now and expensive to backfill — the security-posture "lay the cheap
foundational edge while the surface is open" case, exactly.

**Poll:** `https://raw.githubusercontent.com/sigstore/fulcio/main/docs/oid-info.md` (changes rarely).
## Part C — IaC and query tools whose resource/table lists *are* dictionaries

These are curated observability lists: someone already decided which GitHub objects are worth
declaring or querying. They are the cheapest way to find out what we have not thought of.

### C1. Terraform GitHub provider — **ADOPT**

| | |
|---|---|
| Version | **v6.13.0**, 2026-07-08 (repo active daily; ~monthly–quarterly minors) |
| URL | https://github.com/integrations/terraform-provider-github |
| Artifact kind | IaC resource/data-source schema |
| Licence | **MIT** — the most permissive source in this report |
| Scale | **88 resources, 75 data sources** (79 on `main`) |

Docs now live at `docs/`, not `website/docs/` (that path is retired).

**The classification is the value, not the raw list.** Of the 88 resources:

- **44 entity-shaped** — `github_repository`, `github_branch`, `github_branch_protection`(GraphQL) and
  `github_branch_protection_v3`(REST), `github_repository_ruleset`, `github_organization_ruleset`,
  `github_repository_environment`, `github_actions_secret`, `github_actions_variable`,
  `github_actions_organization_secret/_variable`, `github_actions_environment_secret/_variable`,
  `github_actions_runner_group`, `github_actions_hosted_runner`,
  `github_enterprise_actions_runner_group`, `github_repository_webhook`,
  `github_organization_webhook`, `github_repository_deploy_key`, `github_release`, `github_issue`,
  `github_issue_label`, `github_repository_milestone`, `github_repository_pull_request`,
  `github_repository_autolink_reference`, `github_repository_file`, `github_team`,
  `github_organization_role`, `github_organization_repository_role`,
  `github_dependabot_secret`, `github_codespaces_secret`, `github_user_gpg_key`, `github_user_ssh_key`, …
- **22 relationship-shaped** — `github_membership` (user→org), `github_team_membership`,
  `github_team_repository` (team→repo w/ permission), `github_repository_collaborator`,
  **`github_app_installation_repository`** (installation→repo),
  `github_actions_organization_secret_repository` (secret→repo visibility grant),
  `github_organization_role_team`, `github_organization_role_user`, `github_emu_group_mapping`,
  `github_organization_block` (a *negative* edge), …
- **3 pointer-edges** — `github_branch_default` (repo →default→ branch),
  `github_repository_environment_deployment_policy` (environment →deployable-from→ branch pattern)
- **16 setting-shaped singletons** — `github_actions_repository_permissions`,
  `github_actions_organization_oidc_subject_claim_customization_template` (⇐ directly relevant to
  our OIDC work), `github_organization_settings`, `github_repository_vulnerability_alerts`, …
- **2 schema/meta** — `github_organization_custom_properties` *defines* a property schema;
  `github_repository_custom_property` *assigns* a value. A metaschema/instance pair, not two entities.

**Two ideas worth carrying into our corpus:**

1. **The singular/plural duality.** The provider ships `github_team_repository` (one edge,
   non-authoritative) *and* `github_repository_collaborators` (the complete set — Terraform deletes
   edges you did not declare). That is the difference between *assert this edge exists* and *assert
   these are all the edges*. Most graph models silently drop it. If we ever ingest desired-state,
   we will need it.
2. **Entity/edge is not a clean binary.** We will need at least two more shapes: **setting**
   (a singleton config block on an existing node — belongs in `configuration`, per our discipline)
   and **set-assertion**. Naming them now prevents mis-modelling settings as nodes.

**Poll target:** `https://registry.terraform.io/v1/providers/integrations/github` returns
`{version, published_at, tag}` — the cheapest change detector anywhere in this report.
For property-level detail, `terraform providers schema -json` against a pinned provider yields every
attribute with type, required/optional/computed, and **sensitivity flag**.

### C2. Steampipe GitHub plugin + Powerpipe mods — **ADOPT (read side)**

| | |
|---|---|
| Version | **v1.10.0**, 2026-08-07 (~every 1–3 months) |
| URL | https://github.com/turbot/steampipe-plugin-github |
| Licence | **Apache-2.0** |
| Scale | **71 tables** (cross-verified three ways at tag v1.10.0) |

Its taxonomy is *richer than Terraform's precisely because it is read-only* — it can name things
GitHub will not let you declare. The categories Terraform structurally cannot have:

- **Event-shaped (3):** `github_audit_log` ← the one true event stream;
  `github_actions_repository_workflow_run`, `github_actions_repository_workflow_job`
  (**note: the only two sources in this whole report besides ours that model workflow runs at all**)
- **Finding-shaped (3):** `github_repository_dependabot_alert`,
  `github_organization_dependabot_alert`, `github_repository_vulnerability_alert`
- **Time-series (4):** `github_traffic_{clone,view}_{daily,weekly}`
- **Reference-data catalogues (3):** `github_gitignore`, `github_license` (SPDX-ish, with
  `permissions`/`conditions`/`limitations` arrays), `github_community_profile`
- **Content-tree (2):** `github_blob`, `github_tree` — the git object graph
- **BOM (1):** `github_repository_sbom`
- **Viewer-scoped projections (6):** `github_my_repository`, `github_my_team`, … — *not new types;
  a scoping dimension*. Our dimensions handle this; worth noting nobody else has that mechanism.
- **Query-shaped (8):** `github_search_*` — explicitly *not* entities.
- **Edge-shaped (8):** including **`github_code_owner`** (path glob →owned-by→ user/team, parsed
  from CODEOWNERS — an edge derived from file content, exactly our proposed `REVIEWS_AS_CODEOWNER`).

**Compliance mods exist and are a reusable assertion vocabulary** (all Apache-2.0):

- `turbot/steampipe-mod-github-compliance` — **37 controls, 15 benchmarks, 33 named queries**,
  mapped to CIS Software Supply Chain Security Guide v1.0.0. The 33 named queries are effectively a
  property dictionary: `default_branch_requires_signed_commits`,
  `default_branch_protections_apply_to_admins`, `default_branch_blocks_force_push`,
  `default_branch_requires_status_checks`, `repo_linear_history_enabled`,
  `org_two_factor_required`, … Last *released* v1.1.1 (2025-07-04) — **near-dormant**; treat as a
  stable reference corpus, not a live feed.
- `turbot/steampipe-mod-github-sherlock` — 34 controls (v1.0.0, 2024-10-22). Note its
  `public_repo_*` / `private_repo_*` near-duplicate control pairs — **an antipattern not to copy**;
  visibility should be a dimension, not a name prefix.
- `turbot/steampipe-mod-github-insights` — 16 dashboards over branch/issue/organization/pull_request/repository.

### C3. CloudQuery GitHub source — **REFERENCE only (licence)**

**The brief's premise needs correcting: this is no longer open source.** The plugin was deleted from
`cloudquery/cloudquery` on **2024-04-24** ("chore: Remove paid plugins", #17779). The hub API reports
`"tier":"paid"`, `"free_rows_per_month":0`, latest **v16.0.0 (2026-08-27)**, 61 tables, every one
`is_paid: true`. The last open-source version was **v9.3.0 (2024-04-16), MPL-2.0, 31 tables** — that
snapshot is safely reusable; the current one is not.

Two of its ideas are worth **independently reinventing** from GitHub's own API rather than copying:

- **An explicit parent→child `relations` graph shipped in the schema** —
  `https://api.cloudquery.io/plugins/cloudquery/source/github/versions/v16.0.0/tables` returns it,
  and it is the best machine-readable relationship artifact in this report.
- **An `is_incremental` flag** marking high-churn entities (issues, PRs, commits, repositories,
  alerts, workflow runs). That is a collection-strategy hint expressed as schema metadata.

One edge is unique to CloudQuery and genuinely valuable:
**`github_pull_request_closing_issues_references`** — PR →closes→ issue. Nobody else models it.

### C4. Others, briefly

- **Pulumi GitHub provider** (v6.15.0, Apache-2.0) — **IGNORE.** Verified byte-identical: its
  `upstream` submodule pins the exact `v6.13.0` commit of the Terraform provider. Same 88 resources,
  camel-cased. No new concepts.
- **`github/rest-api-description`** (MIT, updated continuously) — **ALIGN.** OpenAPI 3.x for the
  entire REST API, with separate bundles for `api.github.com`, `ghec`, and each `ghes-*` version.
  This is first-party ground truth for entities *and properties*, but it is **unclassified** — the
  curation into "which of these deserve to be nodes" is exactly what C1–C3 provide.
- **`Legit-Labs/legitify`** (Apache-2.0, active 2026-08-25) — **REFERENCE.** 53 Rego policies in
  6 namespaces (`actions`, `enterprise`, `member`, `organization`, `repository`, `runner_group`),
  each with `severity`, `threat`, `remediationSteps` and **`requiredScopes`** metadata. The only
  source treating **`runner_group`** and **`enterprise`** as first-class policy namespaces.
  Its `requiredScopes` field is a nice precedent for our "unobservable with a read-only PAT" problem.
- **`ossf/allstar`** (Apache-2.0) — **REFERENCE, thin.** 9 policies; notable only for being
  *enforcement-capable* rather than read-only.
- **Ansible `community.general`** — **IGNORE.** 9 modules, no relationship-shaped ones.

---

## Part D — GitHub's own taxonomy, the other forges, and the GitOps nouns

### D1. GitHub REST API resource categories — **ADOPT**

| | |
|---|---|
| Artifact | `github/rest-api-description` — OpenAPI 3.0.3, `api.github.com.json`, **12.9 MB** |
| Scale | **810 paths / 1,222 operations / 973 schemas**; head commit 2026-08-27 |
| Licence | **MIT** |
| Cadence | ~3 commits/day (21 in the last 7 days) |

The real taxonomy is `x-github.category` / `subcategory` on every operation — **51 categories** for
github.com, **54** for GHEC. ⚠️ The OpenAPI `tags` array (49) does *not* match: `branches`,
`collaborators`, `metrics`, `pages`, `releases` and `deploy-keys` are categories but not tags.

The CI/CD-relevant categories and their subcategories:

| Category (ops) | Subcategories |
|---|---|
| **actions** (195) | artifacts, cache, **concurrency-groups**, **hosted-runners**, oidc, permissions, secrets, self-hosted-runner-groups, self-hosted-runners, variables, workflow-jobs, workflow-runs, workflows |
| **orgs** (123) | api-insights, artifact-metadata, attestations, blocking, custom-properties, issue-fields, issue-types, members, network-configurations, organization-roles, orgs, outside-collaborators, personal-access-tokens, **rule-suites**, **rules**, security-managers, webhooks |
| **repos** (73) | attestations, autolinks, contents, custom-properties, forks, issue-types, repos, **rule-suites**, **rules**, webhooks |
| **branches** (38) | branch-protection, branches |
| **deployments** (21) | branch-policies, deployments, environments, protection-rules, statuses |
| **checks** (12) | runs, suites |
| **dependabot** (25) | alerts, **repository-access**, secrets |
| **dependency-graph** (5) | dependency-review, dependency-submission, sboms |
| **apps** (37) | apps, installations, marketplace, oauth-applications, webhooks |
| **git** (13) | blobs, commits, refs, tags, trees |
| **secret-scanning** (17) | custom-patterns, **push-protection**, secret-scanning |
| **code-security** (20) | configurations |

**Corrections to the brief's sketch:** `branches` is its own category, not a `repos` subcategory;
`tags` is not a subcategory at all; `dependabot` has gained `repository-access`. Genuinely new
categories worth knowing exist: **`agents`** (30 ops), **`agent-tasks`**, **`campaigns`**,
**`code-quality`**, **`code-security`**, **`copilot-spaces`**, **`credentials`**,
**`enterprise-teams`**, **`private-registries`**.

⚠️ `info.version` is a stale `1.1.4` — ignore it. The real signal is the dated API-version files
(`api.github.com.2022-11-28.json` and, newly, **`api.github.com.2026-03-10.json`**), with breaking
changes enumerated in `descriptions/api.github.com/CHANGELOG.md`.
### D2. GitHub GraphQL schema — **the most authoritative "what is an entity in GitHub" statement that exists**

I downloaded and counted the public schema directly (`https://docs.github.com/public/fpt/schema.docs.graphql`,
fetched 2026-08-27):

| Kind | Count |
|---|---:|
| `type` (objects) | **1025** — of which **439** after excluding `*Connection`, `*Edge`, `*Payload` |
| `interface` | **50** |
| `enum` | **255** |
| `union` | **50** |
| `input` | **417** |
| `scalar` | **13** |

**The 50 interfaces are the closest GitHub gets to declaring abstract entity classes**, and are worth
reading in full: `Actor`, `Agentic`, `Assignable`, `AuditEntry`, `Closable`, `Comment`,
`Contribution`, `Deletable`, `EnterpriseAuditEntryData`, `GitObject`, `GitSignature`,
`HovercardContext`, `IssueFieldCommon`, `IssueFieldValueCommon`, `Labelable`, `Lockable`,
`MemberStatusable`, `Migration`, `Minimizable`, `Node`, `OauthApplicationAuditEntryData`,
`OrganizationAuditEntryData`, `PackageOwner`, `Pinnable`, `ProfileOwner`, `ProjectOwner`,
`ProjectV2Event`, `ProjectV2FieldCommon`, `ProjectV2ItemFieldValueCommon`, `ProjectV2Owner`,
`ProjectV2Recent`, `Reactable`, `RepositoryAuditEntryData`, `RepositoryDiscussionAuthor`,
`RepositoryDiscussionCommentAuthor`, `RepositoryInfo`, `RepositoryNode`, `RepositoryOwner`,
`RequirableByPullRequest`, `Sponsorable`, `Starrable`, `Subscribable`, `SubscribableThread`,
`TeamAuditEntryData`, `TeamReviewRequestable`, `TopicAuditEntryData`, `UniformResourceLocatable`,
`Updatable`, `UpdatableComment`, `Votable`.

`Node` (globally-addressable id), `Actor` (anything that can act), `RepositoryOwner`,
`RepositoryNode` (anything that belongs to a repo) and `UniformResourceLocatable` are the
structurally interesting ones — they are GitHub's own answer to "what are the cross-cutting
supertypes", which is the same job our Entity spine does.

**The CI/CD- and governance-relevant object types** (verified present):

> `App` · `Blob` · `Bot` · `BranchProtectionRule` · `BypassForcePushAllowance` ·
> `BypassPullRequestAllowance` · `CheckAnnotation` · `CheckRun` · `CheckSuite` · `Commit` ·
> `DeployKey` · `Deployment` · `DeploymentProtectionRule` · `DeploymentRequest` · `DeploymentStatus` ·
> `Enterprise` · `EnterpriseUserAccount` · `Environment` · `ExternalIdentity` · `GitActor` ·
> `IpAllowListEntry` · `Issue` · `Label` · `Language` · `Mannequin` · `MergeQueue` ·
> `MergeQueueEntry` · `Milestone` · **`OIDCProvider`** · `Organization` ·
> `OrganizationIdentityProvider` · `Package` · `PackageVersion` · `ProjectV2` · `PullRequest` ·
> `PushAllowance` · `Ref` · `Release` · `ReleaseAsset` · `Repository` · **`RepositoryRule`** ·
> `RepositoryRuleConditions` · **`RepositoryRuleset`** · `RepositoryRulesetBypassActor` ·
> `RepositoryTopic` · `RepositoryVulnerabilityAlert` · `ReviewDismissalAllowance` ·
> `SecurityAdvisory` · `Status` · `StatusCheckRollup` · `StatusContext` · `Tag` · `Team` · `Topic` ·
> `Tree` · `User` · `VerifiableDomain` · **`Workflow`** · **`WorkflowRun`**

Three of these settle open questions for us: **`RepositoryRuleset`/`RepositoryRule` exist**
(so our proposed `github_ruleset` has first-party backing), **`Workflow` and `WorkflowRun` both
exist** (confirming that GitHub itself separates definition from execution — as we do and BloodHound
does not), and **`OIDCProvider` exists** as a first-class object.

**The enums are a controlled-vocabulary goldmine.** The ones that directly name role/permission/state
semantics we would otherwise invent:

| Enum | Members |
|---|---|
| `RepositoryPermission` | `ADMIN`, `MAINTAIN`, `WRITE`, `TRIAGE`, `READ` |
| `OrganizationMemberRole` | `ADMIN`, `MEMBER` |
| `TeamRole` | `ADMIN`, `MEMBER` |
| `RepositoryVisibility` | `PUBLIC`, `PRIVATE`, `INTERNAL` |
| `RepositoryRulesetTarget` | `BRANCH`, `TAG`, `PUSH`, `REPOSITORY` |
| `RuleEnforcement` | `ACTIVE`, `EVALUATE`, `DISABLED` |
| `RepositoryRulesetBypassActorBypassMode` | `ALWAYS`, `EXEMPT`, `PULL_REQUEST` |
| `CheckStatusState` | `QUEUED`, `WAITING`, `REQUESTED`, `PENDING`, `IN_PROGRESS`, `COMPLETED` |
| `CheckConclusionState` | `SUCCESS`, `FAILURE`, `NEUTRAL`, `CANCELLED`, `SKIPPED`, `STALE`, `TIMED_OUT`, `ACTION_REQUIRED`, `STARTUP_FAILURE` |
| `DeploymentState` | `PENDING`, `QUEUED`, `WAITING`, `IN_PROGRESS`, `ACTIVE`, `INACTIVE`, `FAILURE`, `ERROR`, `ABANDONED`, `DESTROYED` |
| `DeploymentProtectionRuleType` | `BRANCH_POLICY`, `REQUIRED_REVIEWERS`, `WAIT_TIMER` |
| `MergeStateStatus` | `CLEAN`, `DIRTY`, `BLOCKED`, `BEHIND`, `DRAFT`, `UNSTABLE`, `HAS_HOOKS`, `UNKNOWN` |
| `WorkflowState` | `ACTIVE`, `DELETED`, `DISABLED_FORK`, `DISABLED_INACTIVITY`, `DISABLED_MANUALLY` |

**`RepositoryRuleType` — 32 members — is the ruleset rule dictionary**, and it is exactly the list our
proposed `github_ruleset.rules[].type` should validate against:

> `AUTHORIZATION` · `BRANCH_NAME_PATTERN` · `CODE_SCANNING` · `COMMITTER_EMAIL_PATTERN` ·
> `COMMIT_AUTHOR_EMAIL_PATTERN` · `COMMIT_MESSAGE_PATTERN` · `COPILOT_CODE_REVIEW` · `CREATION` ·
> `DELETION` · `FILE_EXTENSION_RESTRICTION` · `FILE_PATH_RESTRICTION` ·
> `LICENSE_COMPLIANCE_SCANNING` · `LOCK_BRANCH` · `MAX_FILE_PATH_LENGTH` · `MAX_FILE_SIZE` ·
> `MAX_REF_UPDATES` · `MERGE_QUEUE` · `MERGE_QUEUE_LOCKED_REF` · `NON_FAST_FORWARD` ·
> `PULL_REQUEST` · `REQUIRED_DEPLOYMENTS` · `REQUIRED_LINEAR_HISTORY` ·
> `REQUIRED_REVIEW_THREAD_RESOLUTION` · `REQUIRED_SIGNATURES` · `REQUIRED_STATUS_CHECKS` ·
> `REQUIRED_WORKFLOW_STATUS_CHECKS` · `SECRET_SCANNING` · `TAG` · `TAG_NAME_PATTERN` · `UPDATE` ·
> `WORKFLOWS` · `WORKFLOW_UPDATES`

Note `WorkflowState`'s `DISABLED_FORK` / `DISABLED_INACTIVITY` / `DISABLED_MANUALLY` — GitHub
distinguishes *why* a workflow is disabled. Our `github_workflow.state` should carry the same values
rather than a boolean.

**Verdict: ALIGN (strongly).** This is first-party, complete, and free. It is also far too large to
adopt wholesale — 1025 object types is the "adopt a dictionary wholesale" trap in its purest form.
Take the **enums as controlled vocabularies** (near-zero cost, immediate correctness benefit) and use
the **object list as a checklist** for "did we forget a concept", not as a list to implement.

**Poll:** the `.graphql` file itself; `octokit/graphql-schema` publishes a **diff per change**, which
is the right signal to watch rather than re-diffing 1.5 MB ourselves.

#### D2.1 Two structural findings from the GraphQL schema

**(a) The sharper entity count.** Of the 1025 object types, **282 implement `Node`** (globally
addressable), and **60 of those are `*AuditEntry`** — leaving **222 real domain entities**. That is
the number to think with, not 1025. GitHub also tags objects with a `@docsCategory`, giving its own
domain partition: issues 71 · pulls 46 · projects 31 · repos 30 · users 26 · enterprise-admin 21 ·
orgs 18 · git 15 · commits 12 · deployments 10 · branches 10 · checks 7 · packages 6 · **actions 5** ·
dependabot 3 · teams 2 · releases 2 · dependency-graph 2 · deploy-keys 1.
**GitHub's own docs consider Actions a 5-type domain.** Ours is a 9-type domain. We are already
modelling Actions more finely than GitHub documents it.

**(b) GitHub's CI/CD entities carry no shared abstraction.**
`Deployment`, `Environment`, `Workflow`, `WorkflowRun`, `CheckSuite`, `BranchProtectionRule`,
`RepositoryRuleset`, `App`, `Package`, `Label`, `DeployKey` **implement nothing but `Node`.**
The interface layer is almost entirely issue/comment-shaped (`Comment`, `Reactable`, `Labelable`,
`Lockable`, `Assignable`, `Closable` — all with 2–11 implementors). Several "abstract classes" have
exactly **one** implementor (`RepositoryInfo`, `Pinnable`, `Agentic`, `SubscribableThread`) — they are
documentation devices, not polymorphism. **This is a gap in GitHub's model, not a model to copy.**
It is also an argument *for* Cartography's semantic-label approach: somebody has to say
"a Workflow is a CICDPipeline", and GitHub does not.

**(c) The unions are where the real polymorphism lives** — and several are directly useful to us:

```
StatusCheckRollupContext      = CheckRun | StatusContext
BypassActor                   = App | EnterpriseTeam | Team | User
PushAllowanceActor            = App | Team | User
BranchActorAllowanceActor     = App | Team | User
ReviewDismissalAllowanceActor = App | Team | User
DeploymentReviewer            = Team | User
RequestedReviewer             = Bot | EnterpriseTeam | Mannequin | Team | User
RuleSource                    = Enterprise | Organization | Repository
PermissionGranter             = EnterpriseTeam | Organization | Repository | Team
Closer                        = Commit | ProjectV2 | PullRequest
RuleParameters                = 17 *Parameters types, one per rule kind
```

`BypassActor = App | EnterpriseTeam | Team | User` and `RuleSource = Enterprise | Organization |
Repository` between them define the shape of our proposed `github_ruleset`: bypass actors are a
heterogeneous edge target set, and a ruleset's *source* is a different node than the repo it applies
to. Our shape review already spotted the org-sourced-ruleset singleton problem; `RuleSource` confirms it.
### D3. GitHub webhook events — the state changes worth modelling

Cross-checked against **three** sources. The authoritative machine-readable one is the `x-webhooks`
block **inside the REST OpenAPI**: **270 entries → 75 distinct events → 257 event+action
combinations**, matching docs.github.com exactly.

⚠️ **`@octokit/webhooks-schemas` is stale.** I independently downloaded and parsed it and counted
**66** events (its top-level `oneOf` has exactly 66 entries) — it is missing nine:
`issue_dependencies`, `personal_access_token_request`, `projects_v2`, `projects_v2_status_update`,
`repository_advisory`, **`repository_ruleset`**, `secret_scanning_scan`, `security_and_analysis`,
`sub_issues`. **`repository_ruleset` matters directly to our `github_ruleset` proposal.**
Use octokit for *payload shape*; use the REST OpenAPI's `x-webhooks` for the *event list*.

The 75 events:

> `branch_protection_configuration` · `branch_protection_rule` · `check_run` · `check_suite` ·
> `code_scanning_alert` · `commit_comment` · `create` · `custom_property` · `custom_property_values` ·
> `delete` · `dependabot_alert` · `deploy_key` · `deployment` · `deployment_protection_rule` ·
> `deployment_review` · `deployment_status` · `discussion` · `discussion_comment` · `fork` ·
> `github_app_authorization` · `gollum` · `installation` · `installation_repositories` ·
> `installation_target` · **`issue_dependencies`** · `issue_comment` · `issues` · `label` ·
> `marketplace_purchase` · `member` · `membership` · `merge_group` · `meta` · `milestone` ·
> `org_block` · `organization` · `package` · `page_build` ·
> **`personal_access_token_request`** · `ping` · `project` · `project_card` · `project_column` ·
> **`projects_v2`** · `projects_v2_item` · **`projects_v2_status_update`** · `public` ·
> `pull_request` · `pull_request_review` · `pull_request_review_comment` ·
> `pull_request_review_thread` · `push` · `registry_package` · `release` · `repository` ·
> **`repository_advisory`** · `repository_dispatch` · `repository_import` ·
> **`repository_ruleset`** · `repository_vulnerability_alert` · `secret_scanning_alert` ·
> `secret_scanning_alert_location` · **`secret_scanning_scan`** · `security_advisory` ·
> **`security_and_analysis`** · `sponsorship` · `star` · `status` · **`sub_issues`** · `team` ·
> `team_add` · `watch` · `workflow_dispatch` · `workflow_job` · `workflow_run`

⚠️ Trap: the OpenAPI keys hyphenate action names (`requested-action`) while the payload `action`
field uses underscores. Two vocabularies, one concept.

**Action vocabularies for the events that matter to us:**

| Event | Actions |
|---|---|
| `workflow_run` | `requested`, `in_progress`, `completed` |
| `workflow_job` | **`queued`, `waiting`, `in_progress`, `completed`** |
| `check_run` | `created`, `rerequested`, `requested_action`, `completed` |
| `check_suite` | `requested`, `rerequested`, `completed` |
| `deployment_review` | `requested`, `approved`, `rejected` |
| `deployment_protection_rule` | `requested` |
| `branch_protection_rule` | `created`, `edited`, `deleted` |
| `branch_protection_configuration` | `enabled`, `disabled` |
| `installation` | `created`, `deleted`, `suspend`, `unsuspend`, `new_permissions_accepted` |
| `installation_repositories` | `added`, `removed` |
| `merge_group` | `checks_requested`, `destroyed` |
| `pull_request` | 22 actions incl. `opened`, `synchronize`, `closed`, `ready_for_review`, `converted_to_draft`, `enqueued`, `dequeued`, `review_requested`, `auto_merge_enabled/disabled` |
| `repository` | `created`, `deleted`, `archived`, `unarchived`, `edited`, `renamed`, `transferred`, `privatized`, `publicized` |
| `secret_scanning_alert` | `created`, `reopened`, `resolved`, `revoked` |
| `member` / `membership` | `added`, `removed`, `edited` / `added`, `removed` |

**`workflow_job`'s `queued` → `waiting` → `in_progress` → `completed` is the single most useful find
here.** It confirms OTel's insistence that **run *state* is orthogonal to *result*** and gives us the
GitHub-native state names. Our `github_actions_job` has `status` + `conclusion` fields already, but
we do not model the queue-wait interval — which is exactly the number a CI/CD product is asked about
("why is CI slow?" is usually a runner-queue answer, not a test-duration answer).

**Verdict: ALIGN.** Events name the state changes worth modelling; the action vocabularies are free
controlled vocabularies. We should not build an event *node* type — our grid's field-level history
already answers "what changed and when" — but the action lists tell us **which fields must be
observable** for that history to be meaningful.

**Poll:** `.x-webhooks` inside
`https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json`
(MIT, current). Payload shapes from `@octokit/webhooks-schemas` / `@octokit/webhooks-types` — but do
not trust those for the event list.

### D4. GitHub audit-log actions — **ADOPT**

The machine-readable source the brief hoped existed **does exist**: `github/docs` ships one JSON file
per plan and scope.

```
https://raw.githubusercontent.com/github/docs/main/src/audit-logs/data/fpt/organization.json   812 actions
https://raw.githubusercontent.com/github/docs/main/src/audit-logs/data/ghec/enterprise.json    984
https://raw.githubusercontent.com/github/docs/main/src/audit-logs/data/fpt/user.json           448
                                    (+ ghec/organization.json, ghec/user.json, ghes-3.17…3.22/*, shared/)
```
⚠️ `fpt/enterprise.json` 404s — only `organization` and `user` exist for the free tier.

Each record is `{action, description, docs_reference_links, fields[]}`. Union across scopes:
**1,159 distinct actions across 185 category prefixes, with 504 distinct field names.**
768 of the 812 org actions carry real prose descriptions. **Licence CC-BY-4.0** — attribution, no
share-alike, so the descriptions are directly reusable with credit.

**The 185 category prefixes are an entity dictionary in verb form.** The largest are `org` (165),
`business` (109), `repo` (82), `user` (51), `copilot` (26), `protected_branch` (24), `sponsors` (24),
`personal_access_token` (18), `team` (17), **`workflows` (15)**, `billing` (14), `codespaces` (14),
`enterprise` (14), `project` (13), **`environment` (11)**, `pull_request` (11), `integration` (11),
`ip_allow_list` (11).

The CI/CD- and governance-relevant categories, with their actual verbs:

| Category | Actions |
|---|---|
| **`workflows`** | `actions_policy_violation`, **`approve_workflow_job`**, **`bypass_protection_rules`**, `cancel_workflow_run`, `comment_workflow_job`, `completed_workflow_run`, `created_workflow_run`, `delete_workflow_run`, `disable_workflow`, `enable_workflow`, `pin_workflow`, `prepared_workflow_job` (+3) |
| **`environment`** | `create`, `delete`, `add_protection_rule`, `remove_protection_rule`, `update_protection_rule`, `create_actions_secret`, `update_actions_secret`, `remove_actions_secret`, `create_actions_variable`, `update_actions_variable`, `remove_actions_variable` |
| **`repository_ruleset`** | `create`, `destroy`, `update` |
| **`protected_branch`** | `create`, `destroy`, **`policy_override`**, **`rejected_ref_update`**, `authorized_users_teams`, `branch_allowances`, `dismiss_stale_reviews`, `update_admin_enforced`, `update_allow_force_pushes_enforcement_level`, … (24 total) |
| **`merge_queue`** | `pull_request_dequeued`, **`pull_request_queue_jump`**, `queue_cleared`, `update_settings` |
| `git` | `clone`, `fetch`, `push` |
| `checks` | `auto_trigger_disabled`, `auto_trigger_enabled`, `delete_logs` |
| `artifact` / `actions_cache` | `destroy` / `delete` |
| `custom_hosted_runner`, `github_hosted_runner`, `premium_runner` | `create`, `destroy`, `update` |
| `integration_installation` | `create`, `destroy`, `repositories_added`, `repositories_removed`, `suspend`, `unsuspend`, `version_updated` |
| `personal_access_token` | `access_granted`, `access_revoked`, `create`, `destroy`, `credential_regenerated`, `credential_revoked`, `access_restriction_disabled/enabled/reset`, … (18) |
| `secret_scanning_alert` | `assign`, `create`, `delete`, `public_leak`, `reopen`, `report`, `resolve`, `revoke`, `unassign`, `validate` |
| **`mcp_registry`** | `allowlist_add_server`, `allowlist_assign`, `allowlist_create`, `allowlist_delete`, `allowlist_set_server_entries`, … (9) |

`operation_type ∈ {ACCESS, AUTHENTICATION, CREATE, MODIFY, REMOVE, RESTORE, TRANSFER}` (from the
GraphQL `OperationType` enum — the JSON dictionary names the field but never populates a value).

Three things here bear directly on our model:

1. **`workflows.approve_workflow_job` and `workflows.bypass_protection_rules`** are the audit
   record of an *approval* and a *bypass* — the two facts a CI/CD governance product is most often
   asked to evidence, and neither is observable from the Actions API alone.
2. **`protected_branch.policy_override` and `.rejected_ref_update`** are the "the gate was
   overridden / the gate held" pair. Same argument.
3. **`environment.create_actions_secret` / `update_actions_secret`** give secret *lifecycle* without
   ever exposing a value — a way to answer "when did this secret last rotate?" from metadata only.

⚠️ **Access caveat:** the audit-log REST endpoints exist **only in the GHEC OpenAPI description**,
not the github.com one (`/orgs/{org}/audit-log`, `/enterprises/{enterprise}/audit-log`, and the
`stream-key`/`streams` endpoints). `include ∈ {web, git, all}`. For a free-tier org, the audit log
is **not observable** — which belongs in our "unobservable with a read-only PAT" list.

### D5. GitLab — **ADOPT (for the neutrality test)**

**Headline: GitLab now ships a complete auto-generated OpenAPI 3.0 document for the whole REST API**
— 3.6 MB, **1,258 paths / 1,725 operations / 867 schemas / 179 tags**, `info.version: 19.3`,
commit 2026-08-26, at `https://docs.gitlab.com/api/openapi/openapi_v3.yaml`. This did not previously
exist and is the most complete forge REST contract available anywhere.

**GraphQL** (live introspection at `https://gitlab.com/api/graphql`, unauthenticated, works):
**2,605 objects** (1,081 excluding Connection/Edge/Payload), 847 inputs, **453 enums**,
**50 interfaces**, 23 unions — **~2.5× GitHub's object count and 10× its useful interface count.**
⚠️ There is **no committed SDL file**; `lib/tasks/gitlab/graphql.rake` dumps to gitignored
`tmp/tests/graphql/`. Live introspection is the only machine-readable poll for outsiders.

Nouns: Project, Group, **Namespace**, Epic, MergeRequest, Issue, **Pipeline**, PipelineSchedule,
**Job**, **Runner**, Environment, Deployment, ProtectedBranch, ProtectedTag, DeployKey, DeployToken,
Package, Release, Milestone, Label, Board, Snippet, Wiki, FeatureFlag, Vulnerability, Dependency,
Cluster/Agent, Webhook, SystemHook, AuditEvent, Member, ApprovalRule, **MergeTrain**, CI Variable,
FreezePeriod.

**The single most valuable thing GitLab contributes to a neutral model:**

```
ProjectMemberRelation  DIRECT INHERITED DESCENDANTS INVITED_GROUPS SHARED_INTO_ANCESTORS
GroupMemberRelation    DIRECT INHERITED DESCENDANTS SHARED_FROM_GROUPS
```

**Membership provenance.** GitHub and Gitea have no equivalent. A neutral `MEMBER_OF` edge without a
provenance property **silently loses information on GitLab ingest** — and the same argument applies
to GitHub, where a repo permission can come from a base role, a team, a direct grant, or an org role.
This is strong external support for our proposed `HAS_REPO_PERMISSION {permission, via}`.

Other enums worth having: `AccessLevelEnum ∈ NO_ACCESS, MINIMAL_ACCESS, GUEST, **PLANNER**, REPORTER,
**SECURITY_MANAGER**, DEVELOPER, MAINTAINER, OWNER, ADMIN` (the classic 5-rung ladder is stale);
`PipelineStatusEnum ∈ CREATED, WAITING_FOR_RESOURCE, PREPARING, WAITING_FOR_CALLBACK, PENDING,
RUNNING, FAILED, SUCCESS, CANCELING, CANCELED, SKIPPED, MANUAL, SCHEDULED` (13 values — **far richer
than GitHub's `status`/`conclusion` pair**, and it names the queue/resource-wait states explicitly);
`DeploymentTier ∈ PRODUCTION, STAGING, TESTING, DEVELOPMENT, OTHER`;
`CiRunnerType ∈ INSTANCE_TYPE, GROUP_TYPE, PROJECT_TYPE` (matching BloodHound's runner-scope split).

**Audit events: 633 documented types across 63 categories**, generated from 634 YAML files, each
carrying `{name, description, introduced_by_issue, feature_category, milestone, saved_to_database,
streamed, scope: [Project|Group|User|Instance]}`. **This is the best-structured audit catalogue of
any vendor** — note especially the pre-computed **`scope`**, which is exactly the partitioning
dimension a neutral model needs and which GitHub encodes only structurally (separate JSON files).

⚠️ **Licence split:** `doc/` (the OpenAPI YAML, GraphQL reference) is **CC BY-SA 4.0** — share-alike
attaches to verbatim descriptions. `config/audit_events/types/` (71 files) is **MIT**;
`ee/config/audit_events/types/` (563 files) is **EE-proprietary**. Names are facts and reusable;
verbatim descriptions are not.

⚠️ Trap: **GitLab's Job webhook has `object_kind: "build"`, not `"job"`.**

### D6. Gitea / Forgejo — **ALIGN (Gitea entity names), ADOPT (Gitea's webhook enum)**

⚠️ **The brief's Gitea URL is dead** — `templates/swagger/v1_json.tmpl` no longer exists in
`go-gitea/gitea`. Gitea now ships generated specs including a **new OpenAPI 3.0.3 artifact**:
`https://raw.githubusercontent.com/go-gitea/gitea/main/templates/swagger/v1-openapi3.generated.json`.
Also ⚠️ **`try.gitea.io` no longer resolves** — use `gitea.com`.

**Gitea** (live `1.27.0+dev`, release v1.27.2 2026-08-13, **MIT**): **225 definitions, 342 paths,
9 tags**. Of the 225: **119 entity-shaped**, 87 request-body options, 19 response wrappers.
The Actions entities: **`ActionWorkflow`, `ActionWorkflowRun`, `ActionWorkflowJob`,
`ActionWorkflowStep`, `ActionRunner`, `ActionRunnerLabel`, `ActionTask`, `ActionArtifact`,
`ActionVariable`, `Secret`, `RunDetails`**.

**That list is the most important neutrality datapoint in this report.** A structurally independent
forge, reimplementing CI from scratch, arrived at **Workflow → WorkflowRun → WorkflowJob →
WorkflowStep + Runner + Artifact + Variable + Secret**. That is almost exactly our spine *plus* the
step level — and it validates the run/definition split that BloodHound and Cartography both omit.

Naming corrections vs the brief: it is `ActionRunner` (not `ActionsRunner`), `ActionVariable`
(not `ActionsVariable`), bare **`Secret`**, **`Hook`** (not `Webhook`), `TopicName` (not `Topic`).
There is no `Collaborator` type (only `RepoCollaboratorPermission`) and no `Wiki` type.

**Forgejo** (v16.0.3, 2026-08-20; repo **GPL-3.0** with an explicit MIT carve-out on the spec file):
246–248 definitions. ⚠️ Its spec declares `+gitea-1.22.0` — **pinned to a Gitea 1.22 baseline while
Gitea is at 1.27**. Divergence: **183 shared definitions, 65 Forgejo-only, 42 Gitea-only.**
Forgejo added quota (21 types) and federation/ActivityPub (10), and uses a *different* Actions shape
(`ActionRun` / `ActionRunJob` / `ActionRunJobStep`). ⚠️ Forgejo's GPLv3+ relicence took effect at
**v9.0**, not v1.21.

**Webhook events** (from `modules/webhook/type.go`, MIT in both): 28 constants each; Gitea's
`AllEvents()` returns 26, including `workflow_run` and `workflow_job`. Forgejo drops those and adds
**`action_run_failure`, `action_run_recover`, `action_run_success`** — a *better CD-outcome*
vocabulary (it names recovery, which nobody else does), but Forgejo-only.

⚠️ Modelling trap worth recording: **Gitea's declared `HookEventType` differs from its delivered wire
event name** (four `issue*` constants collapse to `issues`; six PR variants collapse to
`pull_request`). The declared enum and the delivered event name are two distinct vocabularies and
need two fields — a mistake easy to make when ingesting.

### D7. GitOps (Argo CD, Flux) — the nouns, for when we extend there

**Argo CD v3.5.2** (2026-08-27, Apache-2.0) ships exactly **three** CRDs, all `argoproj.io/v1alpha1`,
all namespaced: **`Application`**, **`ApplicationSet`**, **`AppProject`**. Siblings add kinds to the
same group: **Argo Workflows v4.1.2** adds `Workflow`, `WorkflowTemplate`, `ClusterWorkflowTemplate`,
`CronWorkflow`, `WorkflowEventBinding`, `WorkflowTaskSet`, `WorkflowTaskResult`,
`WorkflowArtifactGCTask`; **Argo Rollouts v1.9.1** adds `Rollout`, `AnalysisTemplate`,
`ClusterAnalysisTemplate`, **`AnalysisRun`**, **`Experiment`**; **Argo Events v1.9.11** adds
`EventSource`, `Sensor`, `EventBus`. ⚠️ **Every kind is still `v1alpha1` after ~8 years** — the
version string is stable but carries no maturity signal. **REFERENCE** — the CRDs are
Kubernetes-shaped and carry no relationship vocabulary beyond `ownerReferences` and the
`AppProject`→`Application` scoping edge.

**Flux v2.9.4** (2026-08-07, ~1–2 week patch cadence, Apache-2.0) ships **15 CRDs across 5 API
groups**, each with exactly one served version that is also storage:
`source.toolkit.fluxcd.io/v1` → `GitRepository`, `OCIRepository`, `HelmRepository`, `HelmChart`,
`Bucket`, **`ExternalArtifact`**; `kustomize.toolkit.fluxcd.io/v1` → `Kustomization`;
**`helm.toolkit.fluxcd.io/v2`** → `HelmRelease` (**`v2`, not `v2beta2`, not `v1`**);
`image.toolkit.fluxcd.io/v1` → `ImageRepository`, `ImagePolicy`, `ImageUpdateAutomation`;
`notification.toolkit.fluxcd.io/v1beta3` → `Alert`, `Provider`, but
**`notification.toolkit.fluxcd.io/v1` → `Receiver`** (⚠️ the notification group is split across two
versions — a trap); and `source.extensions.fluxcd.io/v1beta1` → `ArtifactGenerator`.
⚠️ `ResourceSet` and `FluxInstance` are **not** upstream Flux — they belong to ControlPlane's
third-party `flux-operator` under `fluxcd.controlplane.io/v1`.

**ALIGN.** Flux is the best-factored CD entity model in this report, and unlike Argo it is
version-graduated. Its structure is worth internalising even though deployment is a non-goal today:
**sources** (`GitRepository`/`OCIRepository`/`Bucket`) are separate from **appliers**
(`Kustomization`/`HelmRelease`), with a **feedback loop** (`ImagePolicy` → `ImageUpdateAutomation`
writes back to the git source) and a **notification triad** (`Alert`/`Provider`/`Receiver`).
The cross-CRD edges are explicitly named in the specs — `spec.sourceRef`, `spec.chartRef`,
`spec.imageRepositoryRef`, `spec.eventSources` — and *that relationship vocabulary is the most
directly borrowable thing in this section*.

---

# Synthesis

The 16 independent sources counted below. Each is counted once even where it has several artifacts.

| # | Source | Kind |
|---|---|---|
| 1 | **BloodHound** GitHub extension (`openhound-github` / `GitHound`) | graph model |
| 2 | **Cartography** GitHub module + Ontology | graph model |
| 3 | **GUAC** | graph model |
| 4 | **Protobom** | graph model |
| 5 | **Eiffel** | event taxonomy w/ typed links |
| 6 | **CDEvents** | event taxonomy |
| 7 | **OpenTelemetry** semconv (`cicd.*`, `vcs.*`) | attribute + entity registry |
| 8 | **Backstage** Software Catalog | entity + relation model |
| 9 | **Sigstore/Fulcio** OID directory | identity attribute set |
| 10 | **OpenSSF Security Insights** | self-declared schema |
| 11 | **Terraform** GitHub provider | resource list |
| 12 | **Steampipe** GitHub plugin (+ compliance mods) | table list |
| 13 | **CloudQuery** GitHub source | table list *(proprietary)* |
| 14 | **GitHub** first-party (REST + GraphQL + webhooks + audit) | API taxonomy |
| 15 | **GitLab** (REST + GraphQL + audit YAML) | API taxonomy |
| 16 | **Gitea / Forgejo** | API taxonomy |

Plus, consulted but not counted as independent CI/CD dictionaries: legitify, Allstar, Endor, OX,
Argo, Flux, Tekton, Argo Workflows, Jenkins, Kusari, Chainguard.

## S1. Union of entity concepts, by number of independent sources

**Tier 1 — named by 8 or more sources. Not modelling these is a defect.**

| Concept | Count | Named by |
|---|---:|---|
| **Repository / project / code repo** | 15 | BloodHound, Cartography, GUAC(`SourceName`), CDEvents, OTel(`vcs.repository`), Backstage(`Component`), Fulcio(`.1.12`/`.1.15`), SecInsights, Terraform, Steampipe, CloudQuery, GitHub, GitLab, Gitea, Eiffel |
| **User / account / actor** | 14 | BloodHound, Cartography, Backstage(`User`), SecInsights(`Contact`), Terraform, Steampipe, CloudQuery, GitHub, GitLab, Gitea, GUAC(`PointOfContact`), Protobom(`Person`), legitify, Endor |
| **Organization / group / tenant** | 13 | BloodHound, Cartography(`Tenant`), Backstage(`Group`/`Domain`), Terraform, Steampipe, CloudQuery, GitHub, GitLab(`Group`/`Namespace`), Gitea, legitify, OTel(`vcs.owner.name`), Fulcio(`.1.16`/`.1.17`), Endor |
| **Branch / ref** | 12 | BloodHound, Cartography, CDEvents, OTel(`vcs.ref`), Eiffel, Terraform, Steampipe, CloudQuery, GitHub(`Ref`), GitLab, Gitea, Fulcio(`.1.14`) |
| **Pipeline / workflow (definition)** | 12 | BloodHound(`GH_Workflow`), Cartography(`CICDPipeline`), CDEvents(`pipelineRun`'s `pipelineName`), OTel(`cicd.pipeline`), Eiffel(activity), Steampipe, CloudQuery, GitHub(`Workflow`), GitLab, Gitea(`ActionWorkflow`), Fulcio(`.1.9`/`.1.18`), SecInsights(`automated-pipeline`) |
| **Secret / credential** | 11 | BloodHound (6 kinds), Cartography(`Secret`), Terraform (8 resources), Steampipe, CloudQuery, GitHub, GitLab, Gitea, legitify, OTel(—), Fulcio(cert) |
| **Artifact / package / build output** | 11 | GUAC(`Artifact`+`Package`), Protobom, CDEvents(`artifact`), Eiffel, OTel(`artifact.*`), Cartography(`GitHubPackage`), Steampipe, CloudQuery, GitHub(`Package`), GitLab, Gitea |
| **Environment / deployment target** | 10 | BloodHound, Cartography, CDEvents(top-level subject), OTel(`deployment.environment.name` — **stable**), Eiffel, Terraform, Steampipe, CloudQuery, GitHub, GitLab, Gitea |
| **Team / user group** | 10 | BloodHound, Cartography(`UserGroup`), Backstage(`Group`), Terraform, Steampipe, CloudQuery, GitHub, GitLab, Gitea, legitify |
| **Pull request / change / merge request** | 10 | CDEvents(`change`), OTel(`vcs.change`), Eiffel(`SourceChange*`), Cartography(—), Terraform, Steampipe, CloudQuery, GitHub, GitLab, Gitea |
| **Runner / worker / agent** | 9 | BloodHound (7 kinds), OTel(`cicd.worker`), Cartography(`GitLabRunner`), Terraform, Steampipe, CloudQuery(—), GitHub, GitLab, Gitea, legitify(`runner_group`), Fulcio(`.1.11`) |
| **Pipeline run / workflow run (execution)** | 8 | CDEvents(`pipelineRun`), OTel(`cicd.pipeline.run`), Eiffel, Steampipe, CloudQuery, GitHub(`WorkflowRun`), GitLab, Gitea(`ActionWorkflowRun`), Cartography(Spacelift only) |
| **Job / task run** | 8 | CDEvents(`taskRun`), OTel(`cicd.pipeline.task.run`), BloodHound(decl. only), Eiffel, Steampipe, CloudQuery, GitHub, GitLab, Gitea(`ActionWorkflowJob`) |

**Tier 2 — 4 to 7 sources. Strong candidates; each needs a demand justification.**

| Concept | Count | Notes |
|---|---:|---|
| **Protection rule / ruleset** | 7 | BloodHound(`GH_BranchProtectionRule`), Cartography(**both** `GitHubRuleset` and `GitHubBranchProtectionRule`), Terraform, Steampipe, GitHub(`RepositoryRuleset` + 32 rule types), GitLab(`ProtectedBranch`+push rules), Gitea(`BranchProtection`) |
| **App / installation / integration** | 7 | BloodHound (2 kinds), Terraform, Steampipe(—), CloudQuery(`github_installations`), GitHub(`App`), GitLab, Gitea(`OAuth2Application`) |
| **Variable** (non-secret config) | 6 | BloodHound (3 kinds), Cartography, Terraform, Steampipe, GitHub, GitLab, Gitea |
| **Release** | 6 | CDEvents(—), Terraform, Steampipe, CloudQuery, GitHub, GitLab, Gitea, SecInsights(`ReleaseDetails`) |
| **Check / status check** | 6 | GitHub(`CheckRun`/`CheckSuite`/`StatusContext`), GitLab(`DetailedMergeStatus`), Gitea(`CommitStatus`), Steampipe(—), CDEvents(`testCaseRun`), Steampipe-mods |
| **Commit / revision** | 6 | Cartography(`COMMITTED_TO`), OTel(`vcs.ref.head.revision`), Eiffel, Steampipe, CloudQuery, GitHub, GitLab, Gitea, Fulcio(`.1.13`) |
| **Finding / alert / vulnerability** | 6 | GUAC, Cartography(`SecurityIssue`), Steampipe, CloudQuery, GitHub, GitLab, Endor, OX |
| **Dependency** | 6 | GUAC(`IsDependency`), Protobom (7 kinds!), Cartography, Steampipe(—), CloudQuery(—), GitHub(dependency-graph), GitLab, Endor |
| **Role / permission grant** | 6 | BloodHound (4 reified role kinds), Cartography(`PermissionRole`), Terraform, GitHub, GitLab(`MemberRolePermission`, 45 values), CloudQuery |
| **Action / reusable step** | 4 | **Cartography(`GitHubAction`, with `is_pinned`)**, BloodHound(inside `GH_WorkflowStep`), GitHub(`uses:`), Protobom(`buildTool`) |
| **Step** | 4 | BloodHound(`GH_WorkflowStep`), Gitea(`ActionWorkflowStep`), Tekton(`Step`), Jenkins(atom node) |
| **Attestation / provenance** | 5 | GUAC(`HasSLSA`), Cartography(`GitHubContainerImageAttestation`), OTel(`artifact.attestation.*`), SecInsights(`Attestation`), Fulcio |
| **Identity provider / federated identity** | 5 | BloodHound(`GH_SamlIdentityProvider`/`GH_ExternalIdentity`), Cartography(`IdentityProvider`), GitHub(`OIDCProvider`), Fulcio(`.1.8`), CloudQuery |
| **Token / API key** | 4 | BloodHound (2 PAT kinds), Cartography(`APIKey`), GitHub, GitLab(`ProjectAccessToken`) |

**Tier 3 — 1 to 3 sources. Interrogate before building.**

`Enterprise` (BloodHound, GitHub, GitLab, legitify) · `RunnerGroup` (BloodHound, Terraform, legitify) ·
`CodeOwner rule` (**Cartography only, as a node**; Steampipe as a table) · `MergeQueue` (GitHub, GitLab
`MergeTrain`) · `Deployment` as distinct from environment (GitHub, GitLab, Eiffel) · `Incident` /
`Ticket` (CDEvents only) · `Approval` (CDEvents 0.5.x, GitHub audit-log only) · `Container image` /
`layer` / `tag` (Cartography, GitLab-via-Cartography) · `Domain` / `System` (Backstage only) ·
`API` as an entity (Backstage only) · `AiResource` (Backstage only) · `Builder` (GUAC only) ·
`Test case` / `test suite` (CDEvents, OTel `test.*`, Eiffel) · `SecurityTool` (SecInsights only) ·
`Traffic` / usage metrics (Steampipe, CloudQuery) · `Audit event` (GitHub, GitLab, Steampipe).

## S2. Union of relationship concepts, by number of independent sources

**Tier 1 — 5 or more sources:**

| Edge concept | Count | Names used |
|---|---:|---|
| **Containment / part-of** | 12 | `GH_Contains`, Cartography `RESOURCE`, Backstage `partOf`/`hasPart`, Protobom `contains`/`contained_by`, GUAC trie edges, CDEvents `{id, source}` refs, Flux `ownerReferences` |
| **Ownership** | 10 | `GH_Owns`, Cartography `OWNER`, Backstage `ownedBy`/`ownerOf`, GUAC `PointOfContact`, Terraform (implicit), Steampipe, our `OWNS_REPO` |
| **Membership** | 10 | `GH_MemberOf`/`GH_HasMember`, Cartography `MEMBER_OF` (an ontology constraint), Backstage `memberOf`/`hasMember`, Terraform `github_membership`, Steampipe `github_organization_member`, CloudQuery, GitLab `ProjectMemberRelation` |
| **Depends-on** | 9 | GUAC `IsDependency`, **Protobom (7 distinct senses)**, Cartography `REQUIRES`, Backstage `dependsOn`/`dependencyOf`, Tekton `runAfter`, Argo `dependencies`, BloodHound `GH_DependsOn`, GitHub `needs:` |
| **Defines / has-workflow** | 7 | `GH_HasWorkflow`, Cartography `HAS_WORKFLOW`, our `DEFINES_WORKFLOW`, Steampipe, CloudQuery, GitHub, Gitea |
| **Uses / references a secret** | 6 | `GH_UsesSecret` + `GH_HasSecret`, Cartography `REFERENCES_SECRET` + `HAS_SECRET`, Cartography ontology `USES_SECRET`, Terraform `..._secret_repository`, GitLab `REFERENCES_VARIABLE` |
| **Built-from / packaged-from (provenance)** | 6 | **Cartography ontology `PACKAGED_FROM`** + `PACKAGED_BY` + `BUILT_FROM`, GUAC `HasSLSA.builtFrom` + `HasSourceAt`, Protobom `generatedFrom`/`generates`, CDEvents `artifact.change`, Fulcio `.1.9`/`.1.12`, Eiffel `COMPOSITION` |
| **Runs-on / dispatched-to compute** | 5 | `GH_CanUseRunner` + `GH_CanDispatchTo`, our `EXECUTED_ON`, OTel `cicd.worker` association, GitLab runner assignment, Gitea `ActionTask` |
| **Deploys-to environment** | 5 | `GH_DeploysTo` + `GH_CanDeployToEnvironment`, CDEvents `service.environment`, Eiffel `ENVIRONMENT`, GitHub `Deployment`→`Environment`, Flux `Kustomization`→cluster |
| **Protected-by / enforced-on** | 5 | `GH_ProtectedBy`, Cartography `HAS_RULE`/`HAS_RULESET`, GitHub `RepositoryRuleset`→`RuleSource`, GitLab `ProtectedBranch`, Gitea `BranchProtection` |
| **Has-role / granted-permission** | 5 | `GH_HasRole`/`GH_HasBaseRole`, Cartography ontology `HAS_ROLE` + `INCLUDES`, Terraform `github_team_repository`, GitLab `MemberRolePermission`, GitHub `RepositoryPermission` |

**Tier 2 — 2 to 4 sources:**

`CALLS_WORKFLOW` (BloodHound, GitHub `workflow_call`, Gitea) · `USES_ACTION` (**Cartography only as a
typed edge**, GitHub as a string) · `TRIGGERED_BY` / `CAUSE` (Eiffel has **five** distinct kinds,
CDEvents `PATH`/`RELATION`, Cartography-Spacelift `TRIGGERED`) · `CAN_ASSUME_IDENTITY` /
federation (BloodHound, Fulcio, our `FEDERATES_VIA`) · `IS_OCCURRENCE` abstract↔concrete
(GUAC only) · `AFFECTS` finding→thing (Cartography ontology, GUAC, Steampipe) ·
`CODEOWNER` (Cartography, Steampipe, Backstage-via-CODEOWNERS) · `PROVIDES_API`/`CONSUMES_API`
(Backstage only) · `CLOSES` PR→issue (**CloudQuery only**) · `SYNCED_TO` / SSO identity
(BloodHound, Cartography, CloudQuery) · `NEXT` ordered chain (Cartography layers, Eiffel `PRECURSOR`).

## S3. The must-have set — concepts in three or more independent sources

Everything in **S1 Tier 1 and Tier 2** and **S2 Tier 1** clears the bar. Restated as a build list,
with what we have today:

| Concept | Sources | Our status |
|---|---:|---|
| Repository | 15 | ✅ `github_repository` |
| User / account | 14 | ✅ `github_account` |
| Organization | 13 | ✅ (merged into `github_account`) |
| **Branch / ref** | 12 | ❌ **a string field on runs** |
| Workflow (definition) | 12 | ✅ `github_workflow` |
| **Secret** | 11 | ❌ deferred backlog |
| **Artifact / package** | 11 | ❌ not modelled |
| **Environment** | 10 | ❌ not modelled |
| **Team** | 10 | ❌ not modelled |
| **Pull request / change** | 10 | ❌ not modelled |
| Runner | 9 | ✅ `github_runner` (no group, no scope) |
| Workflow run | 8 | ✅ `github_actions_run` — **and we are one of only 8** |
| Job / task run | 8 | ✅ `github_actions_job` |
| **Ruleset / protection rule** | 7 | ❌ proposed |
| **App installation** | 7 | ⚠️ `github_app` conflates app and installation |
| **Variable** | 6 | ❌ not modelled |
| **Release** | 6 | ❌ not modelled |
| **Status check** | 6 | ❌ proposed |
| **Commit / revision** | 6 | ⚠️ `head_sha` field only |
| **Role / permission grant** | 6 | ❌ not modelled |
| **Action (reusable step)** | 4 | ❌ proposed |
| **Step** | 4 | ❌ inside `configuration` JSON |
| — edges — | | |
| Containment | 12 | ✅ `HOSTS_ACCOUNT`, `OWNS_REPO`, `DEFINES_WORKFLOW`, `HAS_ACTIONS_JOB` |
| Ownership | 10 | ✅ `OWNS_REPO` |
| **Membership** | 10 | ❌ not modelled |
| **Depends-on** | 9 | ❌ `needs:` lives in JSON |
| **Uses-secret** | 6 | ❌ deferred |
| **Built-from / packaged-from** | 6 | ❌ not modelled |
| Runs-on compute | 5 | ✅ `EXECUTED_ON` |
| **Deploys-to environment** | 5 | ❌ not modelled |
| **Protected-by** | 5 | ❌ proposed |
| **Has-role** | 5 | ❌ not modelled |

**Nine must-have concepts we neither have nor have proposed:** *team*, *variable*, *release*,
*artifact/package*, *commit as a node*, *role/permission grant*, *membership edge*,
*depends-on edge (job `needs:`)*, *built-from/packaged-from edge*.
Of these, **membership + role/permission** and **job `needs:`** are the two that would most change
what the product can answer, and both are already half-present in data we collect.

## S4. What the corpus says that no single source does

**(a) The three-plane gap — and it is the product opportunity.**

- **Cartography + BloodHound + Terraform** = the *static configuration* of the SDLC. Rich nouns, **no runs**.
- **CDEvents + Eiffel + OTel** = the *executions and their outcomes*. Rich verbs, **thin nouns**.
- **GUAC + Protobom + Sigstore** = the *artifacts and the evidence about them*. Rich provenance, **no machinery**.

No source joins all three. Our model already spans plane 1 and plane 2 — which is unusual — and
touches plane 3 only via `FEDERATES_VIA`. **That span is the differentiator, and it should be stated
as such rather than discovered later.**

**(b) Definition vs. execution is the single sharpest dividing line in the field.**
BloodHound, Cartography, GUAC, Terraform, Backstage, Endor: **no run entity.**
CDEvents, OTel, Eiffel, Gitea, GitLab, GitHub, Steampipe, CloudQuery, Spacelift: **run entities.**
The split correlates exactly with the question being asked — *who can reach what* (configuration)
versus *what happened* (execution). A product that claims to model "your CI/CD system" needs both,
and must **not reuse one name for both** (BloodHound's `GH_WorkflowJob` is a declaration; ours is an
execution).

**(c) Everyone eventually reifies "how did this permission arrive".**
GitLab ships `ProjectMemberRelation ∈ {DIRECT, INHERITED, DESCENDANTS, INVITED_GROUPS,
SHARED_INTO_ANCESTORS}`; Steampipe ships `affiliation ∈ {ALL, OUTSIDE, DIRECT}`; GitHub ships
`CollaboratorAffiliation` and `RoleInOrganization`; Cartography encodes it in **15 generated edge
names**; BloodHound reifies **four `*Role` node types**. Four different mechanisms, one requirement.
**Model provenance-of-permission as an edge property from the start.** It is the cheapest possible
version of a fact that every mature model has been forced to add.

**(d) Two kinds of edge between steps, not one.**
Tekton (`runAfter` vs result-references), Argo Workflows (`dependencies` vs `artifact.from`) and
GitHub itself (`needs:` vs `outputs`/artifacts) independently separate **control-flow ordering** from
**data/artifact flow**. Neither Cartography nor GUAC nor BloodHound has either. We have neither.

**(e) Nobody models a GitHub Action as a node except Cartography** — and Cartography's
`GitHubAction` carries **`is_pinned`**, which is precisely the property the `tj-actions/changed-files`
class of supply-chain incident is about. Our proposed `github_action` + `USES_ACTION {pin_kind}` is
therefore **not** single-source speculation: it has one strong precedent, and that precedent
independently chose the same load-bearing property.

**(f) Three sources publish a *rejected-candidates* register, and it is the most reusable practice
in the corpus.** Cartography excludes Azure Data Factory from `CICDPipeline` with a written rationale;
BloodHound marks 120 of 148 edges non-traversable and says why; GUAC marks every schema experimental.
Our corpus's Step 7.3 "rejected candidates, with reasons" has good company.
## Part E — BloodHound's GitHub model vs. the vocabulary we have today

Ground truth for our side: I queried the running instance as the skill directs
(`list_entity_types`) — **`github_core` is not installed in this session's boot profile**, so the
registry shows only platform types and `grid_fixtures__*`. I therefore verified against the plugin's
own spec and source, which agree exactly with the brief:
`_dev-plugins/github_core/specs/spec-github-core-v0.md` (edge table), `.../models/*.py` (9 models),
`.../edges/*.edge.json` (9 edge files).

### E1. Node-for-node

| Our node | BloodHound equivalent | Verdict |
|---|---|---|
| `github_platform` | *(none — `environments` declares `GH_Organization` as the tenancy root)* | **We are ahead.** A platform node is what makes GHES / GitLab / Gitea coexist on one grid. BloodHound assumes github.com. Keep it. |
| `github_account` | `GH_User` **+** `GH_Organization` **+** `GH_EnterpriseManagedUser` (3 kinds) | **They split, we merge.** Ours is one type with an `account_type` field. Theirs must split because `GH_Organization` is the tenancy root. Our merge is defensible; the risk is queries that mean "orgs only" needing a field filter. |
| `github_repository` | `GH_Repository` | Same concept, same name. ✅ |
| `github_workflow` | `GH_Workflow` | Same — **but** theirs stores parsed YAML *as a subtree of nodes*, ours stores it in `configuration` JSON. See E3. |
| `github_actions_run` | **none** | **We are ahead, decisively.** No execution instance anywhere in their model. |
| `github_actions_job` | `GH_WorkflowJob` — *but a different thing* | **Name collision, semantic mismatch.** Theirs = job *declaration* from YAML. Ours = job *execution* with `status`/`conclusion`/`started_at`. Both are legitimate; they must not share a name. |
| `github_runner` | `GH_Runner` + `GH_EnterpriseRunner` + `GH_OrgRunner` + `GH_RepoRunner` (+ 3 `*RunnerGroup`) | **They are ahead on scope.** We have no runner-group concept and no scope discriminator. Runner *groups* are the actual access-control object. |
| `github_app` | `GH_App` | Same name. But theirs separates `GH_App` (the registered application) from `GH_AppInstallation` (the grant), which we do not. |
| `identity_core__oidc_issuer` | *(no OIDC issuer node; `SAML_Issuer` exists for SAML)* | **We are ahead on OIDC.** They jump straight from repo/branch/env to the cloud identity via `GH_CanAssumeIdentity` without reifying the issuer. Ours is more composable; theirs is more directly queryable. |

### E2. Edge-for-edge

| Our edge | BloodHound equivalent | Notes |
|---|---|---|
| `HOSTS_ACCOUNT` | *(none)* | Follows from having no platform node. |
| `OWNS_REPO` | **`GH_Owns`** (`GH_Organization → GH_Repository`) | Exact match. **Their name is better** — shorter, and it does not bake the target into the verb. |
| `DEFINES_WORKFLOW` | **`GH_HasWorkflow`** (`GH_Repository → GH_Workflow`) | Same edge. Ours is the more precise word (a repo *defines* a workflow; "has" is vague), theirs is the conventional one. |
| `EXECUTES_WORKFLOW` | *(none)* | No run nodes ⇒ no execution edge. |
| `HAS_ACTIONS_JOB` | **`GH_HasJob`** (`GH_Workflow → GH_WorkflowJob`) | **Different direction and different meaning.** Theirs: workflow *declares* job. Ours: run *contains* job execution. |
| `EXECUTED_ON` | **`GH_CanDispatchTo`** (`GH_WorkflowJob → GH_OrgRunner`/`GH_RepoRunner`) | Theirs is *eligibility* (label matching, non-traversable); ours is *observed fact*. Genuinely different edges — both are worth having. |
| `ENABLED_ON` | **`GH_InstalledAs`** + **`GH_CanAccess`** | Theirs splits app→installation→repo into two edges. Ours collapses it, and also overloads `ENABLED_ON` to carry the OIDC issuer. |
| `REFERENCES_RESOURCE` | *(none — they draw only typed cross-cloud edges)* | Our generic conservative link edge has no counterpart. |
| `FEDERATES_VIA` + `TRUSTS_ISSUER` | **`GH_CanAssumeIdentity`** (repo/branch/env → `AZFederatedIdentityCredential`/`AWSRole`) | **The most instructive comparison in the report.** Ours is a 2-hop composable chain through a reified issuer; theirs is one direct computed edge that already answers "can this repo assume that role?". Theirs is a *conclusion*; ours is *evidence*. We should keep the chain **and** derive their conclusion edge on top of it. Note their source is repo **or branch or environment** — ours is repo only, which over-grants: OIDC `sub` claims are usually branch- or environment-scoped. |

### E3. What they model that we do not — ranked by how much it would hurt to miss

1. **The workflow YAML as graph structure, not as a JSON blob.**
   `GH_Workflow -HasJob-> GH_WorkflowJob -HasStep-> GH_WorkflowStep`, and then
   `GH_WorkflowStep -UsesSecret-> GH_RepoSecret` / `-UsesVariable->` and
   `GH_WorkflowJob -CallsWorkflow-> GH_Workflow` / `-DependsOn-> GH_WorkflowJob` / `-DeploysTo-> GH_Environment`.
   We hold all of this in `github_workflow.configuration` where **nothing can point at it**. The
   skill's strongest test — *does anything need to point at it?* — says step and job-declaration are
   nodes: `USES_ACTION`, `REFERENCES_SECRET` and `CALLS_WORKFLOW` all want a step or job-decl endpoint.
   This is our single largest structural gap.
2. **Secrets and variables as first-class nodes, scoped.** Six kinds plus two generic labels, with
   `HasSecret` (availability) separate from `UsesSecret` (reference). Ours: deferred backlog item.
   Without it "which workflows can read this org secret" is unanswerable.
3. **Environments with protection semantics.** `GH_Environment` + `GH_EnvironmentBranchPolicy` +
   `GH_ApprovesDeploymentTo` (required reviewers) + `GH_MatchesEnvironmentPolicy` +
   `GH_CanDeployToEnvironment`. We have no environment node at all — yet an environment is exactly
   the object our OIDC federation should be keyed to.
4. **Runner *groups* and runner scope.** `GH_RunnerGroup`, `GH_HasRunner`, `GH_IsEligibleFor`,
   `GH_InheritedFrom` (org group inherits from enterprise group). The group is the access-control
   object; a bare `github_runner` cannot express who may use it.
5. **Branch as a node, and branch protection as a node.** `GH_Branch`, `GH_BranchProtectionRule`,
   `GH_ProtectedBy`, `GH_RestrictionsCanPush`, `GH_BypassPullRequestAllowances`. Our `head_branch`
   is a string on a run. Already proposed in our shape review as `git_branch` + `github_ruleset`.
6. **App installation as distinct from app.** `GH_App -InstalledAs-> GH_AppInstallation -CanAccess-> GH_Repository`.
   The *grant* is where the permissions live; our single `github_app` node cannot hold them.
7. **Credentials as nodes.** `GH_PersonalAccessToken`, `GH_PersonalAccessTokenRequest`,
   `GH_ValidToken` (a live leaked token linked back to its owner). We model no credential at all.
8. **Federated identity plumbing.** `GH_ExternalIdentity`, `GH_SamlIdentityProvider`, `GH_MapsToUser`,
   `GH_SyncedTo` — the SSO/SCIM join between a GitHub user and a corporate identity.
9. **Enterprise tier.** `GH_Enterprise`, `GH_EnterpriseTeam`, `GH_EnterpriseRole`, `GH_EnterpriseManagedUser`.
   Out of scope for us today; worth knowing the nouns exist above the org.
10. **Teams.** `GH_Team`, `GH_MemberOf`, `GH_HasRole`. Our shape review has this at the "friends" tier.
11. **Secret-scanning alerts.** `GH_SecretScanningAlert` + `GH_ValidToken`.
12. **Computed capability edges as a category.** Covered in A1.5 — the technique, not just the list.

### E4. What we model that they do not

- **Execution history**: runs, attempts, conclusions, durations, `run_number`, `event`, `head_sha`.
  This is not a small gap in their model; it is the entire other half of CI/CD.
- **A platform node**, enabling multi-forge and GHES on one grid.
- **A reified OIDC issuer** (`identity_core__oidc_issuer`) shared across clouds.
- **A generic conservative cross-domain link** (`REFERENCES_RESOURCE`).
- **Field-level history and provenance on every node**, from the grid spine — they re-collect and
  overwrite. "What did this look like before" is a query for us and a re-run for them.

### E5. Read on the eight proposed-but-not-built concepts

| Proposed | Independent support | Call |
|---|---|---|
| `git_branch` | **12 sources** — BloodHound `GH_Branch`, Cartography `GitHubBranch`, OTel `vcs.ref` (identity = **revision**, not name), CDEvents `branch`, Eiffel, Terraform `github_branch`, Steampipe, CloudQuery, GraphQL `Ref`, GitLab, Gitea `Branch`, Fulcio `.1.14` | **Overwhelming. Build it.** Name it `branch`, not `ref` — every source says "branch" (GraphQL's `Ref` is technically correct and universally unhelpful). |
| `github_ruleset` | **7 sources.** **Cartography models `GitHubRuleset` + `GitHubRulesetRule` as nodes**, Terraform `github_repository_ruleset`/`github_organization_ruleset`, GraphQL `RepositoryRuleset`/`RepositoryRule` + the **32-member `RepositoryRuleType`** enum, Steampipe `github_repository_ruleset`, webhook `repository_ruleset`, audit `repository_ruleset.*`. **BloodHound models only the legacy `GH_BranchProtectionRule`.** | **Build it.** We would be *ahead* of BloodHound. Validate `rules[].type` against GraphQL's `RepositoryRuleType`; model bypass actors as a heterogeneous target set (GraphQL `BypassActor = App \| EnterpriseTeam \| Team \| User`) and the ruleset's *source* as a separate node (`RuleSource = Enterprise \| Organization \| Repository`). |
| `status_check` | **6 sources.** GraphQL `CheckRun`/`CheckSuite`/`StatusContext`/`StatusCheckRollup` (+ the union `StatusCheckRollupContext = CheckRun \| StatusContext`), webhook `check_run`/`check_suite`/`status`, Gitea `CommitStatus`, GitLab `DetailedMergeStatus` (24 values), the Steampipe compliance mod's `default_branch_requires_status_checks` | **Build it** — it is the merge gate. Model the *requirement* (`status_check`) separately from the *result* (`check_run`): GitHub has both, and they are different objects. |
| `pull_request` | **10 sources** (GraphQL, webhooks — 22 actions, Steampipe, CloudQuery, Terraform, OTel `vcs.change.*`, CDEvents `change`, Eiffel `SourceChange*`, GitLab, Gitea) — **except BloodHound**, which has ~8 verbs about PRs and no PR node, and **Cartography**, which has none either. | **Build it.** Prefer the neutral name **`change`** (CDEvents' deliberate choice, and OTel's) or `pull_request` with `merge_request` as the GitLab alias. CloudQuery uniquely models a PR →closes→ issue edge. |
| `app_installation` | **7 sources.** BloodHound `GH_AppInstallation` (+ `GH_InstalledAs`, `GH_CanAccess`), Terraform `github_app_installation_repository`/`_repositories`, CloudQuery `github_installations`, GraphQL `App`, webhook `installation`/`installation_repositories`, audit-log `integration_installation.*` (7 verbs) | **Build it.** The *grant* is where permissions live; a single `github_app` node cannot hold them. |
| `github_action` | **One strong precedent: Cartography's `GitHubAction` node — and it carries `is_pinned`.** BloodHound keeps `uses:` inside `GH_WorkflowStep`; GitHub treats it as a string; Protobom has `buildTool` as an edge type. | **Build it.** Not single-source speculation after all: the one prior art independently chose the same load-bearing property (pin posture). Cartography's fields are `owner`, `name`, `version`, `is_pinned`, `is_local`, `full_name` — a good starting shape for `USES_ACTION {ref, pin_kind}`. |
| `actions_secret` | **11 sources.** BloodHound (6 kinds + generic `GH_Secret` label), Cartography `GitHubActionsSecret` (3 schemas, `level` field — the same scope-enum answer we want), Terraform (8 secret resources), Steampipe, CloudQuery, GitHub, GitLab, Gitea (bare `Secret`), legitify | **Build it.** One type with a `scope` enum, following Cartography's `level` field rather than BloodHound's six kinds. Add `actions_variable` alongside — 6 sources name it separately. |
| `github_environment` | **10 sources.** BloodHound `GH_Environment` + `GH_EnvironmentBranchPolicy` + 4 environment edges, Cartography `GitHubEnvironment`, Terraform `github_repository_environment`, Steampipe, CloudQuery, GraphQL `Environment` + `DeploymentProtectionRule`, CDEvents `environment` (a top-level subject), GitLab, Gitea, **OTel `deployment.environment.name` — the only `stable` attribute in the whole neighbourhood** | **Build it**, and re-key OIDC federation to it. Fulcio OID `.1.23` is literally "Deployment Environment", confirming the environment is the right federation subject. |
## Part F — Naming guidance

The rule: **where an industry-standard term exists, use it.** Where several exist, prefer the one
from the *vendor-neutral committee* for neutral concepts and the *platform* for platform concepts —
because that is where each is authoritative.

### F1. Rename or reconsider

| Ours today | Recommended | Why |
|---|---|---|
| `github_actions_run` | **`workflow_run`** (GitHub-facing) / **`pipeline_run`** (neutral) | GitHub's own API, GraphQL and webhook all say `workflow_run`; `actions_run` is a word nobody else uses. `pipeline_run` is CDEvents' and OTel's neutral term (`cicd.pipeline.run.*`) and GitLab's. |
| `github_actions_job` | **`workflow_job`** (GitHub) / **`task_run`** (neutral) | `workflow_job` is GitHub's webhook event name. CDEvents calls the neutral unit-inside-a-pipeline-run a **`taskRun`**; OTel calls it `cicd.pipeline.task.*`. **Also: rename to avoid the collision with BloodHound's declaration-side `GH_WorkflowJob`.** |
| `HAS_ACTIONS_JOB` | **`HAS_TASK_RUN`** / `HAS_WORKFLOW_JOB` | Follows the node rename; `ACTIONS_JOB` is not a term of art. |
| `DEFINES_WORKFLOW` | keep, or **`HAS_WORKFLOW`** | BloodHound says `GH_HasWorkflow`. Ours is more precise. Low stakes — keep, and note the synonym. |
| `github_account` | keep, but see below | No source merges user and org into one type. If we keep the merge, document `account_type` as the discriminator prominently, because every other dictionary will lead people to expect two types. |
| `EXECUTED_ON` | keep | Reads correctly and does not collide. BloodHound's `GH_CanDispatchTo` is a *different* (eligibility) edge — model both, do not rename one into the other. |

### F2. Use the standard word for the not-yet-built concepts

| Concept | Use | Not |
|---|---|---|
| A named line of development | **`branch`** | `ref` (GraphQL's `Ref` is technically correct and universally unhelpful) |
| A proposed change | **`change`** neutral / **`pull_request`** GitHub | `merge_request` is GitLab's word; CDEvents deliberately chose **`change`** to cover both, and OTel uses `vcs.change.*`. If we want one neutral noun, `change` is the committee-chosen one. |
| A merge gate result | **`status_check`** or **`check_run`** | GitHub has *both* the legacy `Status`/`StatusContext` and the modern `CheckRun`/`CheckSuite`. `check_run` is the modern one; `status_check` is the word the branch-protection UI uses for the requirement. Use `status_check` for the *requirement* and `check_run` for the *result* — they are different objects. |
| A deployment target | **`environment`** | Universal: BloodHound, GitHub, CDEvents (a top-level subject), Terraform, GitLab. No ambiguity. |
| A reusable step bundle | **`action`** | GitHub-specific and correctly so. |
| A protection policy | **`ruleset`** (GitHub) / **`protection_rule`** (neutral) | GitHub renamed branch protection to *rulesets*; the API is `repository_ruleset`. Model the modern name; keep `branch_protection_rule` as the legacy/neutral face. |
| An Actions credential | **`actions_secret`** with a `scope` enum | Terraform, Steampipe and BloodHound all say `actions_secret`/`GH_*Secret`. Do not invent `ci_credential`. |
| An app grant | **`app_installation`** | BloodHound `GH_AppInstallation`, GitHub webhook `installation`. |
| A runner pool | **`runner_group`** | GitHub's own term; BloodHound `GH_RunnerGroup`. |

### F3. Prefix and namespace discipline

- **Do not adopt BloodHound's `GH_` prefix.** It exists because BloodHound requires one namespace
  per extension in a single shared graph. Our plugin slug already namespaces us
  (`github_core__github_repository`), so a `GH_` prefix would be a second namespace on top of one.
- **Do keep the `github_` prefix on genuinely GitHub-shaped types** (`github_app`,
  `github_ruleset`, `github_runner`) and **drop it from forge-neutral ones** (`branch`,
  `pull_request`/`change`, `environment`, `release`) — this is the `git_core` extraction question
  the shape review already raised. Deciding the *name* now is free; renaming after data lands is not.
- **Verbs in edge names should be present-tense and not encode the target type.** `OWNS_REPO` bakes
  the target in; `OWNS` (BloodHound) does not. Ours is fine as long as we are consistent, but if a
  neutral `git_core` ever owns the edge, `OWNS_REPO` reads wrong when the target is a project or a
  namespace.
## Part G — Update cadence and the poll seam

Per `build-domain-vocabulary` Step 9: **record, do not build.** The shape when it is built is a
*ledger* — a scheduled job re-reads pinned sources, diffs against recorded versions, and **opens a
proposal** for a human or agent to judge. It must never mutate the vocabulary automatically.

Sorted by how much attention each deserves.

| Source | Pinned at | Cadence | Machine-readable poll target | Cheapest change detector |
|---|---|---|---|---|
| **OTel semconv** | v1.44.0 · 2026-08-04 | **monthly** ⚠️ everything still `release_candidate`, names still move | `model/cicd/{registry,entities,spans,metrics}.yaml`, `model/vcs/{registry,entities,metrics}.yaml` at a tag | diff `CHANGELOG.md` → "🛑 Breaking changes 🛑". ⚠️ releases carry **no assets**; `version.properties` is the file-format version, not semconv's — use the git tag |
| **Terraform GitHub provider** | v6.13.0 · 2026-07-08 | monthly–quarterly minors, daily commits | `registry.terraform.io/v2/provider-docs?filter[provider-version]=<id>&filter[category]=resources&page[size]=200`; property-level via `terraform providers schema -json` | `https://registry.terraform.io/v1/providers/integrations/github` → `{version, published_at, tag}` |
| **Backstage catalog-model** | `@backstage/catalog-model` 1.10.0 · 2026-08-18 | app weekly; **model near-frozen since 2020** | `packages/catalog-model/src/schema/kinds/*.json`, `packages/catalog-model/src/kinds/index.ts` | `https://registry.npmjs.org/@backstage/catalog-model` → `dist-tags.latest` (**not** repo releases — far too noisy) |
| **Steampipe GitHub plugin** | v1.10.0 · 2026-08-07 | every 1–3 months | `github/plugin.go` (the authoritative table-registration map — grep `"github_[a-z0-9_]+"`) | `repos/turbot/steampipe-plugin-github/releases/latest` |
| **BloodHound GitHub extension** | `SOGitHub` v1.3.1 (`openhound-github`) · pushed 2026-08-25 · GitHound v1.0.0 | bursty — 11 commits in 2026-06, 11 in 2026-08, nothing between | `https://raw.githubusercontent.com/SpecterOps/openhound-github/main/extension/schema.json` (**verified 200**) — a single file with every node kind, edge kind, description and traversability | `releases.atom` (**verified 200**); or the blob SHA of `extension/schema.json` |
| **CDEvents** | v0.5.1 · 2026-04-15 | **~annual, irregular** (19-month gap 2024→2025) | `schemas/*.json` at a tag; canonical `$id`-hosted schemas serve live (`https://cdevents.dev/0.5.1/schema/<event>`) | `https://raw.githubusercontent.com/cdevents/spec/main/version.txt` — **one line, the cheapest detector in this report** |
| **GitHub REST OpenAPI** | rolling · pushed 2026-08-27 | **continuous** — tracks the live API | `descriptions/api.github.com/api.github.com.json` (+ `ghec`, `ghes-*` bundles) | contents-API commit SHA for the `descriptions/` path (the bundle itself is ~13 MB — never poll the body) |
| **GitHub GraphQL schema** | fetched 2026-08-27: **1025 objects, 50 interfaces, 255 enums, 50 unions, 417 inputs, 13 scalars** | continuous, with a published deprecation calendar | `https://docs.github.com/public/fpt/schema.docs.graphql` (also mirrored in `octokit/graphql-schema`) | `octokit/graphql-schema` releases — it publishes a diff per change, which is exactly the signal we want |
| **Fulcio OID directory** | `.1.1`–`.1.24` | **slow** — `.1.23`/`.1.24` are recent additions | `https://raw.githubusercontent.com/sigstore/fulcio/main/docs/oid-info.md` | file blob SHA |
| **Steampipe compliance mods** | compliance v1.1.1 · 2025-07-04; sherlock v1.0.0 · 2024-10-22 | **near-dormant** (touched 2026-03-25, no feature work) | `contents/cis_supply_chain_v100`, `contents/query` | ⚠️ compliance mod has **no GitHub Releases objects** — version lives only in `CHANGELOG.md`. Treat as a frozen reference corpus. |
| **legitify** | pushed 2026-08-25 | active | `policies/github/*.rego` (6 files) | contents SHA |
| **Cartography** | 0.140.0 · 2026-08-11 | **fortnightly releases, daily commits** | `cartography/models/github/*.py` (26 files) and — more valuable — `cartography/models/ontology/{labels,constraints}.py` | `repos/cartography-cncf/cartography/releases/latest`. ⚠️ **Repo moved from `lyft/` to `cartography-cncf/`; the old path 404s.** Docs are generated from the models, so never poll the docs |
| **GitHub REST OpenAPI** | rolling · 2026-08-27 | **~3 commits/day** | `descriptions/api.github.com/api.github.com.json` — one 12.9 MB file carrying entities, the 51 REST categories **and all 75 webhook events** (`.x-webhooks`) | commit SHA for the `descriptions/` path; breaking changes in `descriptions/api.github.com/CHANGELOG.md`. ⚠️ `info.version` is a stale `1.1.4` — use the dated API-version filenames |
| **GitHub GraphQL** | Last-Modified 2026-08-25 | **changes on ~half of all business days** | `https://docs.github.com/public/fpt/schema.docs.graphql` | **`https://raw.githubusercontent.com/github/docs/main/src/graphql/data/fpt/changelog.json`** — 616 dated entries, plus `upcoming-changes.json` for deprecations. This is a structured change feed; use it rather than diffing 1.5 MB |
| **GitHub audit-log dictionary** | fetched 2026-08-27 | tracks docs merges (continuous) | `src/audit-logs/data/{fpt,ghec,ghes-*}/{organization,user,enterprise}.json` — 1,159 actions with descriptions and field lists | contents SHA. **CC-BY-4.0** — reusable with attribution. ⚠️ `fpt/enterprise.json` 404s |
| **GUAC** | v1.1.0 · 2026-03-13 | ~quarterly minors, active `main` | `pkg/assembler/graphql/schema/*.graphql` (28 files) | `releases/latest`. ⚠️ **`docs.guac.sh` ontology page is stale relative to the schema** — never poll the docs |
| **Protobom** | **v0.6.0 · 2026-08-26** | very active | `api/sbom.proto` — the 44-member `Edge.Type` enum in one file | `releases/latest` |
| **GitLab** | OpenAPI `info.version: 19.3` · 2026-08-26 | major yearly (May), minor **monthly** (3rd Thu), patch 2×/month | `https://docs.gitlab.com/api/openapi/openapi_v3.yaml` (3.6 MB); `config/audit_events/types/*.yml` (71 MIT) + `ee/…` (563, proprietary) | ⚠️ **No committed GraphQL SDL** — `lib/tasks/gitlab/graphql.rake` dumps to gitignored `tmp/`. Live introspection at `gitlab.com/api/graphql` is the only machine-readable poll |
| **Gitea** | v1.27.2 · 2026-08-13 | ~quarterly minors | `templates/swagger/v1-openapi3.generated.json` **(new OpenAPI 3.0.3)**; `modules/webhook/type.go` for the event enum | `releases/latest`. ⚠️ The brief's `v1_json.tmpl` path is dead; `try.gitea.io` no longer resolves |
| **Forgejo** | v16.0.3 · 2026-08-20 | ~monthly | `templates/swagger/v1_json.tmpl` (Swagger 2.0) | ⚠️ Spec pinned at `+gitea-1.22.0` while Gitea is at 1.27. Repo GPL-3.0 with an MIT carve-out on the spec file |
| **Flux v2** | v2.9.4 · 2026-08-07 | **~1–2 week patches** | `https://github.com/fluxcd/flux2/releases/latest/download/install.yaml` — 341 KB, one grep-able file with every CRD | `releases/latest`. ⚠️ Notification group is split: `Alert`/`Provider` at `v1beta3`, `Receiver` at `v1` |
| **Argo CD** | v3.5.2 · 2026-08-27 | frequent | `manifests/crds/{application,applicationset,appproject}-crd.yaml` | `releases/latest`. ⚠️ Everything is still `v1alpha1` after ~8 years — the version carries no maturity signal |
| **OpenSSF Security Insights** | v2.2.0 · 2026-01-31 | slow | `spec/schema.cue` | `VERSION` file. ⚠️ GitHub reports licence **`NOASSERTION`** — verify before vendoring text |
| **Eiffel** | `edition-orizaba` · **2023-06-30** | releases stale (branch still moves) | `eiffel-vocabulary/*.json` | `releases/latest`. Treat as a **frozen reference corpus** |
| **CloudQuery GitHub** | v16.0.0 · 2026-08-27 | very active | `https://api.cloudquery.io/plugins/cloudquery/source/github/versions/v16.0.0/tables` (returns the parent→child `relations` graph) | same endpoint's `latest_version`. **Licence blocks adoption — poll for awareness only.** |

**Two practical notes for whoever builds the ledger:**

- **Three artifacts are single files that fully describe a vocabulary** and are therefore ideal
  first targets: BloodHound's `extension/schema.json`, CDEvents' `version.txt` + `schemas/`, and
  OTel's `model/{cicd,vcs}/*.yaml`. Start there; the rest need scraping.
- **The strongest form** (per Step 9) is landing a catalogue on the grid as nodes so "what changed in
  the standard" is a graph query with history. BloodHound's `schema.json` is the best candidate in
  this report: 40 nodes + 148 edges + descriptions + traversability, one Apache-2.0 file, stable URL.

---

## Closing notes

**This is a dated artefact with a maintenance obligation.** Everything above was read on
**2026-08-27** from primary artifacts. Six of the sources moved in the last three weeks
(Cartography 08-11, Steampipe 08-07, Flux 08-07, Backstage 08-18, Protobom 08-26, BloodHound 08-25),
and two — OTel semconv and the GitHub schemas — change monthly or faster. Part G is the seam that
keeps this honest.

**Corrections this pass made to the brief's assumptions**, recorded so they are not re-litigated:

1. BloodHound's GitHub extension is **two repos**, not one: `GitHound` (v1.0.0, 34 nodes / 122 edges,
   fullest workflow model) and `openhound-github` (`SOGitHub` v1.3.1, 40 nodes / 148 edges, fullest
   enterprise + identity model). The "~27 node kinds" figure matches neither; "~152 edge kinds"
   matches a constant count in `kinds/edges.py`, not the registered schema.
2. `lyft/cartography` is dead — the repo is **`cartography-cncf/cartography`**, and its
   `docs/root/modules/github/schema.md` no longer exists (docs are generated from the models).
3. **CloudQuery's GitHub plugin is no longer open source** (removed 2024-04-24; now paid, 0 free rows).
4. GUAC has **no `IsVulnerability`** (renamed `VulnEqual`) and no separate `OSV`/`GHSA`/`CVE` nodes;
   `docs.guac.sh` is stale relative to the schema.
5. CDEvents v0.5.0 removed `subject.type`, renamed `context.version` → `specversion`, and moved to
   **camelCase** — so it is `chainId`, not `chain_id`. Testing is its own stage and the subjects are
   `testCaseRun`/`testSuiteRun`, not `testCase`/`testSuite`.
6. `@octokit/webhooks-schemas` reports **66** events; the authoritative count is **75**
   (`x-webhooks` in the REST OpenAPI). The nine it is missing include **`repository_ruleset`**.
7. Gitea's `templates/swagger/v1_json.tmpl` path is dead (use the generated OpenAPI 3.0.3 file), and
   `try.gitea.io` no longer resolves.
8. `ossf/security-insights-spec` redirects to `ossf/security-insights`, and GitHub reports its
   licence as **NOASSERTION**.

**Known gaps in this survey, stated rather than hidden:**

- **The WebSearch budget was exhausted early.** Everything here was fetched directly from primary
  artifacts, which is a better method for schema lists but a worse one for *discovery*. Sources I did
  not already know to look for may be missing.
- **Academic "pipeline-graph" literature is not covered.** I could not run literature searches and
  will not invent citations.
- No public entity/graph model was found for **Jit, Cycode, Arnica, or OX Security's attack-path
  graph** within a bounded search. That is "not found", not "does not exist".
- I did not verify whether Backstage plugins contribute relation types beyond the 14 core constants.
- `SpecterOps/GitHound`'s git history is squashed (single commit, 2026-08-10), so the ~2025-07 launch
  date in the brief could not be confirmed or refuted.

**Licence summary for reuse.** Apache-2.0: BloodHound/OpenHound, Cartography, GUAC, CDEvents,
Eiffel, Protobom, Steampipe + its mods, legitify, Allstar, Backstage, OTel, Sigstore, Argo, Flux.
MIT: Terraform GitHub provider, `github/rest-api-description`, Gitea, GitLab's CE audit-event YAML,
octokit mirrors. CC-BY-4.0: GitHub docs (including the audit-log dictionary — attribution, no
share-alike). CC BY-SA 4.0: GitLab `doc/` — **share-alike attaches to verbatim descriptions**.
NOASSERTION: OpenSSF Security Insights. **Proprietary — read, do not copy:** CloudQuery's current
GitHub plugin, Endor Labs, OX Security, GitLab's EE audit-event YAML.

Names and structural facts are not copyrightable; verbatim descriptions are. Where we adopt a
*name*, no obligation attaches. Where we adopt *prose*, attribute it.
## Appendix 1 — BloodHound GitHub extension: all 148 relationship kinds

Source: `SpecterOps/openhound-github` `extension/schema.json` v1.3.1 (Apache-2.0), fetched 2026-08-27.
`T` = traversable in BloodHound pathfinding (28 of 148). Source→target pairs where published
in `SpecterOps/GitHound` `Documentation/EdgeDescriptions/` (118 of them).

| T | Relationship kind | Source → Target | Description |
|:-:|---|---|---|
|  | `GH_Contains` | `GH_Enterprise, GH_Organization, GH_Repository, GH_Environment` → `GH_Organization, GH_EnterpriseTeam, GH_Team, GH_Repository, GH_OrgRole, GH_RepoRole, GH_TeamRole, GH_OrgSecret, GH_AppInstallation, GH_PersonalAccessToken, GH_PersonalAccessTokenRequest, GH_RepoSecret, GH_EnvironmentSecret, GH_SecretScanningAlert` | Container relationship for organizational hierarchy (org contains secrets/variables, repo contains secrets/variables, environment contains secrets/variables) |
|  | `GH_CreateEnterpriseOrganizations` |  | [Enterprise] Enterprise role can create organizations |
|  | `GH_EditEnterpriseCustomPropertiesForOrganizations` |  | [Enterprise] Enterprise role can edit custom properties for organizations |
| **T** | `GH_ManageEnterpriseAdmins` |  | [Enterprise] Enterprise role can manage enterprise administrators |
|  | `GH_ManageEnterpriseIdentityProvider` |  | [Enterprise] Enterprise role can manage the enterprise identity provider |
| **T** | `GH_ManageEnterpriseMembers` |  | [Enterprise] Enterprise role can manage enterprise members |
| **T** | `GH_ManageEnterpriseOrganizationAdmins` |  | [Enterprise] Enterprise role can manage organization administrators |
|  | `GH_ManageEnterpriseOrganizations` |  | [Enterprise] Enterprise role can manage organizations |
|  | `GH_ManageEnterpriseReferrals` |  | [Enterprise] Enterprise role can manage referrals |
|  | `GH_ManageEnterpriseTeams` |  | [Enterprise] Enterprise role can manage enterprise teams |
|  | `GH_ReadEnterpriseAuditLog` |  | [Enterprise] Enterprise role can read the audit log |
|  | `GH_ReadEnterpriseDomainVerification` |  | [Enterprise] Enterprise role can read domain verification data |
|  | `GH_ReadEnterpriseMembers` |  | [Enterprise] Enterprise role can read enterprise members |
|  | `GH_ReadEnterpriseOrgProjects` |  | [Enterprise] Enterprise role can read organization projects |
|  | `GH_ReadEnterpriseOrganizationAdmin` |  | [Enterprise] Enterprise role can read organization administration data |
|  | `GH_SetEnterpriseInteractionLimits` |  | [Enterprise] Enterprise role can set interaction limits |
|  | `GH_ViewEnterpriseActionsUsageMetrics` |  | [Enterprise] Enterprise role can view Actions usage metrics |
|  | `GH_ViewEnterpriseBilling` |  | [Enterprise] Enterprise role can view billing data |
|  | `GH_ViewEnterpriseSecretScanningAlerts` |  | [Enterprise] Enterprise role can view secret-scanning alerts |
|  | `GH_WriteEnterpriseActionsPolicies` |  | [Enterprise] Enterprise role can write Actions policies |
|  | `GH_WriteEnterpriseBilling` |  | [Enterprise] Enterprise role can write billing settings |
|  | `GH_WriteEnterprisePersonalAccessTokenPolicies` |  | [Enterprise] Enterprise role can write personal access token policies |
|  | `GH_WriteEnterpriseSso` |  | [Enterprise] Enterprise role can write SSO settings |
|  | `GH_WriteEnterpriseTeamMembers` |  | [Enterprise] Enterprise role can write enterprise team membership |
|  | `GH_AssignedTo` | `GH_EnterpriseTeam` → `GH_Organization` | Enterprise-scoped team is assigned to an organization |
| **T** | `GH_InheritedFrom` |  | Organization runner group is inherited from an enterprise runner group |
| **T** | `GH_HasRunner` |  | Runner group exposes a directly assigned self-hosted runner to authorized repositories or workflows |
| **T** | `GH_Owns` | `GH_Organization` → `GH_Repository` | Organization owns a repository |
| **T** | `GH_HasRole` | `GH_User, GH_Team, GH_EnterpriseTeam` → `GH_OrgRole, GH_RepoRole, GH_TeamRole, GH_EnterpriseRole` | User or team has a role assignment (org role, team role, or repo role) |
| **T** | `GH_MemberOf` | `GH_TeamRole, GH_Team, GH_EnterpriseTeam` → `GH_Team, GH_EnterpriseTeam` | Team role is a member of a team, or team is a nested member of a parent team |
|  | `GH_AddMember` | `GH_TeamRole` → `GH_Team` | Team role can add members to the team (maintainer privilege) |
| **T** | `GH_HasBaseRole` | `GH_OrgRole, GH_RepoRole` → `GH_OrgRole, GH_RepoRole` | Role inherits permissions from another role |
|  | `GH_CanCreateRepositories` |  | Role can create repositories in the organization |
|  | `GH_CanCreatePublicRepositories` |  | Role can create public repositories in the organization |
|  | `GH_CanCreateInternalRepositories` |  | Role can create internal repositories in the organization |
|  | `GH_CanCreatePrivateRepositories` |  | Role can create private repositories in the organization |
|  | `GH_ReadRepoContents` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can read repository contents |
|  | `GH_WriteRepoContents` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can write repository contents |
|  | `GH_WriteRepoPullRequests` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can create and merge pull requests |
| **T** | `GH_AdminTo` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role has admin access to the repository. |
|  | `GH_BypassBranchProtection` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can bypass merge-gate branch protections (PR reviews, lock branch). Suppressed by enforce_admins. |
|  | `GH_PushProtectedBranch` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can push to branches with push restrictions. Not affected by enforce_admins. |
|  | `GH_ManageWebhooks` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can manage repository webhooks |
|  | `GH_ManageDeployKeys` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can manage deploy keys |
|  | `GH_DeleteAlertsCodeScanning` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can delete code scanning alerts |
|  | `GH_ViewSecretScanningAlerts` | `GH_OrgRole, GH_RepoRole` → `GH_Organization, GH_Repository` | [Repository] Role can view secret scanning alerts |
|  | `GH_RunOrgMigration` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can run organization migrations |
|  | `GH_ManageSecurityProducts` | `GH_RepoRole` → `GH_Repository` | Repo role can manage security products |
|  | `GH_ManageRepoSecurityProducts` | `GH_RepoRole` → `GH_Repository` | Repo role can manage repo-level security products |
|  | `GH_EditRepoProtections` | `GH_RepoRole` → `GH_Repository` | Repo role can edit branch protection rules |
|  | `GH_JumpMergeQueue` | `GH_RepoRole` → `GH_Repository` | Repo role can jump the merge queue |
|  | `GH_CreateSoloMergeQueueEntry` | `GH_RepoRole` → `GH_Repository` | Repo role can create solo merge queue entries |
|  | `GH_EditRepoCustomPropertiesValues` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can edit custom property values on the repository |
|  | `GH_AddLabel` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can add labels to issues and pull requests |
|  | `GH_RemoveLabel` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can remove labels from issues and pull requests |
|  | `GH_CloseIssue` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can close issues |
|  | `GH_ReopenIssue` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can reopen closed issues |
|  | `GH_ClosePullRequest` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can close pull requests |
|  | `GH_ReopenPullRequest` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can reopen closed pull requests |
|  | `GH_AddAssignee` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can assign users to issues and pull requests |
|  | `GH_DeleteIssue` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can delete issues |
|  | `GH_RemoveAssignee` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can remove assignees from issues and pull requests |
|  | `GH_RequestPrReview` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can request pull request reviews |
|  | `GH_MarkAsDuplicate` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can mark issues or pull requests as duplicates |
|  | `GH_SetMilestone` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can set milestones on issues and pull requests |
|  | `GH_SetIssueType` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can set issue types |
|  | `GH_ManageTopics` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can manage repository topics |
|  | `GH_ManageSettingsWiki` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can manage wiki settings |
|  | `GH_ManageSettingsProjects` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can manage project settings |
|  | `GH_ManageSettingsMergeTypes` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can manage allowed merge types |
|  | `GH_ManageSettingsPages` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can manage GitHub Pages settings |
|  | `GH_EditRepoMetadata` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can edit repository metadata |
|  | `GH_SetInteractionLimits` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can set interaction limits on the repository |
|  | `GH_SetSocialPreview` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can set the repository social preview image |
|  | `GH_EditRepoAnnouncementBanners` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can edit repository announcement banners |
|  | `GH_ReadCodeScanning` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can read code scanning results |
|  | `GH_WriteCodeScanning` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can upload code scanning results |
|  | `GH_ViewDependabotAlerts` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can view Dependabot alerts |
|  | `GH_ResolveDependabotAlerts` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can resolve Dependabot alerts |
|  | `GH_DeleteDiscussion` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can delete discussions |
|  | `GH_ToggleDiscussionAnswer` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can toggle discussion answers |
|  | `GH_ToggleDiscussionCommentMinimize` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can minimize discussion comments |
|  | `GH_EditDiscussionCategory` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can edit discussion categories |
|  | `GH_CreateDiscussionCategory` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can create discussion categories |
|  | `GH_ConvertIssuesToDiscussions` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can convert issues to discussions |
|  | `GH_CloseDiscussion` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can close discussions |
|  | `GH_ReopenDiscussion` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can reopen discussions |
|  | `GH_EditCategoryOnDiscussion` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can change the category of a discussion |
|  | `GH_ManageDiscussionBadges` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can manage discussion badges |
|  | `GH_EditDiscussionComment` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can edit discussion comments |
|  | `GH_DeleteDiscussionComment` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can delete discussion comments |
|  | `GH_CreateTag` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can create tags and releases |
|  | `GH_DeleteTag` | `GH_RepoRole` → `GH_Repository` | [Repository] Repo role can delete tags and releases |
|  | `GH_CreateRepository` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can create repositories in the organization |
|  | `GH_InviteMember` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can invite members to the organization |
|  | `GH_AddCollaborator` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can add outside collaborators |
|  | `GH_CreateTeam` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can create teams in the organization |
|  | `GH_TransferRepository` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can transfer repositories |
|  | `GH_ManageOrganizationWebhooks` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can manage organization webhooks |
|  | `GH_OrgBypassCodeScanningDismissalRequests` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can bypass code scanning dismissal requests |
|  | `GH_OrgBypassSecretScanningClosureRequests` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can bypass secret scanning closure requests |
|  | `GH_OrgReviewAndManageSecretScanningBypassRequests` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can review and manage secret scanning bypass requests |
|  | `GH_OrgReviewAndManageSecretScanningClosureRequests` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can review and manage secret scanning closure requests |
|  | `GH_ReadOrganizationActionsUsageMetrics` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can read Actions usage metrics |
|  | `GH_ReadOrganizationCustomOrgRole` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can read custom org role definitions |
|  | `GH_ReadOrganizationCustomRepoRole` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can read custom repo role definitions |
|  | `GH_ResolveSecretScanningAlerts` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can resolve secret scanning alerts |
|  | `GH_WriteOrganizationActionsSecrets` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can write Actions secrets |
|  | `GH_WriteOrganizationActionsVariables` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can write Actions variables |
|  | `GH_WriteOrganizationActionsSettings` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can write Actions settings |
| **T** | `GH_WriteOrganizationCustomOrgRole` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can write custom org role definitions |
|  | `GH_WriteOrganizationCustomRepoRole` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can write custom repo role definitions |
|  | `GH_WriteOrganizationNetworkConfigurations` | `GH_OrgRole` → `GH_Organization` | [Organization] Org role can write network configurations |
|  | `GH_BypassPullRequestAllowances` | `GH_User, GH_Team` → `GH_BranchProtectionRule` | User or team can bypass pull request requirements on a branch protection rule |
|  | `GH_RestrictionsCanPush` | `GH_User, GH_Team` → `GH_BranchProtectionRule` | User or team is allowed to push to branches protected by this rule |
| **T** | `GH_CanEditProtection` | `GH_RepoRole` → `GH_Repository, GH_Branch` | [Repository - Computed] Repo role can modify or remove branch protection rules for the repository/branch (computed from GH_EditRepoProtections + GH_ProtectedBy) |
| **T** | `GH_CanReadSecret` |  | Org role can read an organization secret by creating a repository in scope |
| **T** | `GH_CanReadSecretScanningAlert` | `GH_OrgRole, GH_RepoRole` → `GH_SecretScanningAlert` | [Computed] Role can read secret scanning alerts (computed from GH_ViewSecretScanningAlerts permission + GH_Contains) |
|  | `GH_ProtectedBy` | `GH_BranchProtectionRule` → `GH_Branch` | Branch protection rule protects this branch |
| **T** | `GH_HasSecret` | `GH_Repository, GH_Environment` → `GH_OrgSecret, GH_RepoSecret, GH_EnvironmentSecret` | Repository or environment has access to this secret |
| **T** | `GH_HasVariable` | `GH_Repository` → `GH_OrgVariable, GH_RepoVariable` | Repository or environment has access to this variable |
| **T** | `GH_ValidToken` | `GH_SecretScanningAlert` → `GH_User` | Secret scanning alert contains a valid, active token belonging to this user |
|  | `GH_HasSamlIdentityProvider` | `GH_Organization, GH_Enterprise` → `GH_SamlIdentityProvider` | Organization has this SAML identity provider configured |
|  | `GH_HasExternalIdentity` | `GH_SamlIdentityProvider` → `GH_ExternalIdentity` | SAML identity provider has this external identity |
|  | `GH_MapsToUser` | `GH_ExternalIdentity, GH_EnterpriseManagedUser` → `GH_User` | External identity maps to a GitHub user or identity provider user |
|  | `GH_HasPersonalAccessToken` | `GH_User` → `GH_PersonalAccessToken` | User owns this personal access token that has been granted access to the organization |
|  | `GH_HasPersonalAccessTokenRequest` | `GH_User` → `GH_PersonalAccessTokenRequest` | User has a pending personal access token request for the organization |
| **T** | `GH_InstalledAs` | `GH_App` → `GH_AppInstallation` | GitHub App is installed as this app installation on an organization |
|  | `GH_CanAccess` | `GH_PersonalAccessToken, GH_AppInstallation` → `GH_Repository` | Personal access token or app installation can access this repository or organization |
| **T** | `GH_CanUseRunner` | `GH_Repository` → `GH_OrgRunner, GH_RepoRunner` | Repository or branch can dispatch workflows to this self-hosted runner execution surface |
|  | `GH_IsEligibleFor` |  | Repository is within the repository-access scope of this runner group |
| **T** | `GH_CanCreateRepositoryWithRunnerAccess` |  | Org role can create a repository that can dispatch workflows to this runner group |
| **T** | `GH_CanWriteBranch` | `GH_RepoRole, GH_User, GH_Team` → `GH_Branch` | [Repository - Computed] Role can push to this branch after evaluating branch protection rules, push restrictions, and bypass allowances |
| **T** | `GH_CanCreateBranch` | `GH_RepoRole, GH_User, GH_Team` → `GH_Repository` | [Repository - Computed] Role can create new branches in this repository (unprotected branches that bypass the merge gate) |
| **T** | `GH_CanCreateEnvironment` |  | Repo role can create new GitHub environments in this repository by editing a workflow that references a nonexistent environment name |
| **T** | `GH_CanEditEnvironment` |  | Repo admin role can edit the configuration of this GitHub environment |
| **T** | `GH_CanAssumeIdentity` | `GH_Repository, GH_Branch, GH_Environment` → `AZFederatedIdentityCredential, AWSRole` | Repository can assume this cloud identity via OIDC federation (Azure workload identity or AWS IAM role) |
| **T** | `GH_SyncedTo` | `AZUser, Okta_User, PingOneUser` → `GH_User` | External identity (Azure, Okta, PingOne) is synced to this GitHub user via SSO/SCIM |
|  | `GH_CallsWorkflow` | `GH_WorkflowJob` → `GH_Workflow` | [Workflow] Job calls a reusable workflow — GH_WorkflowJob → GH_Workflow |
| **T** | `GH_CanPwnRequest` | `GH_RepoRole` → `GH_Repository, GH_Branch` | [Computed] Repo role can exploit a pwn-requestable workflow to execute arbitrary code with the target's secrets and permissions — GH_RepoRole → GH_Repository / GH_Branch |
|  | `GH_DependsOn` | `GH_WorkflowJob` → `GH_WorkflowJob` | [Workflow] Job must run after another job (needs: dependency) — ordering only, not an access path |
|  | `GH_DeploysTo` | `GH_WorkflowJob` → `GH_Environment` | [Workflow] Job deploys to a GitHub Environment — GH_WorkflowJob → GH_Environment |
|  | `GH_HasMember` | `GH_Enterprise, GH_Organization` → `GH_User, GH_EnterpriseManagedUser` | Enterprise or organization has this user as a member |
|  | `GH_UsesSecret` | `GH_WorkflowStep` → `GH_RepoSecret or GH_OrgSecret` | [Workflow] Job or step references a secret by name — GH_WorkflowJob / GH_WorkflowStep → GH_RepoSecret / GH_OrgSecret / GH_EnvironmentSecret (scope match) |
|  | `GH_UsesVariable` | `GH_WorkflowStep` → `GH_RepoVariable or GH_OrgVariable` | [Workflow] Job or step references a variable by name — GH_WorkflowJob / GH_WorkflowStep → GH_RepoVariable / GH_OrgVariable / GH_EnvironmentVariable (scope match) |
| **T** | `GH_CanDeployToEnvironment` |  | [Computed] Repository, branch, repo role, or reviewer can deploy to this GitHub environment after evaluating deployment branch policy, reviewer gates, and admin bypass behavior; reviewer edges require both self-approval and a deployable code path |
|  | `GH_MatchesEnvironmentPolicy` |  | Branch matches this environment deployment branch policy |
|  | `GH_ApprovesDeploymentTo` |  | User or team is configured as a required reviewer for this environment |


## Appendix 2 — BloodHound GitHub extension: all 40 node kinds

| Node kind | Display name | Description |
|---|---|---|
| `GH_Enterprise` | GitHub Enterprise | A GitHub Enterprise account that contains organizations, enterprise teams, roles, and managed users |
| `GH_EnterpriseTeam` | GitHub Enterprise Team | A team managed at the GitHub Enterprise level and assignable across organizations |
| `GH_EnterpriseRole` | GitHub Enterprise Role | The role a user or team has at the GitHub Enterprise level |
| `GH_EnterpriseManagedUser` | GitHub Enterprise Managed User | A GitHub Enterprise managed user account linked to an enterprise identity provider |
| `GH_Organization` | GitHub Organization | A GitHub Organization—top-level container for repositories, teams, and settings |
| `GH_User` | GitHub User | An individual GitHub user account |
| `GH_Team` | GitHub Team | A team within an organization, grouping users for shared access and collaboration |
| `GH_Repository` | GitHub Repository | A code repository in an organization, containing files, issues, and other resources |
| `GH_Branch` | GitHub Branch | A named reference in a repository representing a line of development |
| `GH_BranchProtectionRule` | GitHub Branch Protection Rule | A branch protection rule that applies to one or more branches via pattern matching |
| `GH_OrgRole` | GitHub Org Role | The role a user has at the organization level (e.g., admin, member) |
| `GH_TeamRole` | GitHub Team Role | The role a user has within a team (e.g., maintainer, member) |
| `GH_RepoRole` | GitHub Repo Role | The permission granted to a user or team on a repository (e.g., admin, write, read) |
| `GH_Workflow` | GitHub Workflow | A GitHub Actions workflow defined in a repository |
| `GH_WorkflowJob` | GitHub Workflow Job | A job within a GitHub Actions workflow, with a runner, permissions, and an ordered list of steps |
| `GH_WorkflowStep` | GitHub Workflow Step | A single step within a GitHub Actions job — either a uses: action reference or a run: shell command |
| `GH_Environment` | GitHub Environment | A GitHub Actions deployment environment with protection rules and deployment branch policies |
| `GH_EnvironmentBranchPolicy` | GitHub Environment Branch Policy | A deployment branch policy attached to a GitHub environment, such as an exact branch name or wildcard pattern like release/* |
| `GH_OrgSecret` | GitHub Org Secret | An organization-level GitHub Actions secret that can be scoped to all, private, or selected repositories |
| `GH_RepoSecret` | GitHub Repo Secret | A repository-level GitHub Actions secret accessible only to workflows in that repository |
| `GH_EnvironmentSecret` | GitHub Environment Secret | An environment-level GitHub Actions secret scoped to a specific deployment environment |
| `GH_OrgVariable` | GitHub Org Variable | An organization-level GitHub Actions variable that can be scoped to all, private, or selected repositories. Unlike secrets, variable values are readable. |
| `GH_RepoVariable` | GitHub Repo Variable | A repository-level GitHub Actions variable accessible only to workflows in that repository. Unlike secrets, variable values are readable. |
| `GH_Secret` | GitHub Secret | Generic label applied to GitHub secret nodes across organization, repository, and environment scope |
| `GH_Variable` | GitHub Variable | Generic label applied to GitHub variable nodes across organization, repository, and environment scope |
| `GH_RunnerGroup` | GitHub Runner Group | Generic label applied to GitHub self-hosted runner group nodes across enterprise and organization scope |
| `GH_Runner` | GitHub Runner | Generic label applied to GitHub self-hosted runner nodes across enterprise, organization, and repository scope |
| `GH_EnterpriseRunnerGroup` | GitHub Enterprise Runner Group | An enterprise-scoped GitHub self-hosted runner group that controls runner access and visibility |
| `GH_OrgRunnerGroup` | GitHub Org Runner Group | An organization-scoped GitHub self-hosted runner group that controls runner access and visibility |
| `GH_EnterpriseRunner` | GitHub Enterprise Runner | An enterprise-scoped GitHub self-hosted runner available to organizations through enterprise runner groups |
| `GH_OrgRunner` | GitHub Org Runner | An organization-scoped GitHub self-hosted runner available to selected repositories or workflows |
| `GH_RepoRunner` | GitHub Repo Runner | A repository-scoped GitHub self-hosted runner available to jobs in a single repository |
| `GH_EnvironmentVariable` | GitHub Environment Variable | An environment-level GitHub Actions variable scoped to a specific deployment environment. Unlike secrets, variable values are readable. |
| `GH_SecretScanningAlert` | GitHub Secret Scanning Alert | A GitHub Advanced Security alert indicating a secret was accidentally committed to a repository |
| `GH_SamlIdentityProvider` | GitHub SAML Identity Provider | A SAML identity provider configured for the organization, enabling SSO |
| `GH_ExternalIdentity` | GitHub External Identity | An external identity from a SAML/SCIM provider linked to a GitHub user for SSO authentication |
| `GH_App` | GitHub App | A GitHub App definition representing the registered application. The app owner controls the private key used to generate installation tokens. |
| `GH_AppInstallation` | GitHub App Installation | A GitHub App installed on the organization with specific permissions and repository access |
| `GH_PersonalAccessToken` | GitHub Personal Access Token | A fine-grained personal access token granted access to organization resources |
| `GH_PersonalAccessTokenRequest` | GitHub Personal Access Token Request | A pending request from an organization member to access organization resources with a fine-grained personal access token |
