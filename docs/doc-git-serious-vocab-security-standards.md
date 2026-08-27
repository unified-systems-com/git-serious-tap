---
title: Concept dictionaries — 29 security and supply-chain standards
date: 2026-08-27
status: research
audience:
  - developer
  - llm
related_docs:
  - docs/doc-git-serious-cicd-shape-review.md
  - docs/doc-git-serious-cicd-security-prior-art.md
---

> **Research pass, 2026-08-27.** Formal schemas, ontologies and control catalogues surveyed for the entities and relationships they name, each with a version, a poll target and an adopt/align/reference/ignore verdict.
> One of four gathering passes behind the domain vocabulary corpus, which lives with the
> vocabulary's owner as `spec-github-core-vocabulary.md`. Written by an AI research agent;
> claims carry citations and the report flags what it could not verify. Not canon.

# git-serious vocabulary survey — security, supply-chain and compliance dictionaries

**Research direction:** "Standards and schemas" (Step 2 of `build-domain-vocabulary`).
**Date of survey:** 2026-08-27. **Surveyor:** research agent (standards cluster).
**Sibling direction (NOT covered here):** platform and tooling schemas — GitHub API, BloodHound,
Cartography, GUAC, Steampipe, CDEvents, OpenTelemetry. Cross-references only.

**Bias of this direction (per the skill's table):** standards give industry-standard names and
interoperability, but they **over-abstract and lag reality by years**. Read the accepted list here
against the adversarial/incident direction before committing anything.

**How to read the verdicts**
- **ADOPT** — use their names and structure directly; a private synonym would be a defect.
- **ALIGN** — map our concept to theirs and record the mapping; keep our name.
- **REFERENCE** — cite in docs, do not model.
- **IGNORE** — with reason.

**Honesty markers used below:** `VERIFIED` (I fetched the primary artifact and read the value),
`REPORTED` (primary source says so but I did not read the underlying artifact),
`UNVERIFIED` (could not confirm — treat as a claim to check).

> **Tooling caveat that affects confidence.** The session's web-search budget was exhausted early,
> so this survey was done by **direct fetch of primary artifacts** (raw JSON schemas, raw spec
> markdown, GitHub API) rather than by search. That makes the fetched facts *more* reliable than a
> search-summarised survey — several enum lists below were extracted from the schema file itself and
> **contradict** what a summarising fetch of the human-readable docs claimed (see the CycloneDX
> `taskType` note). It also means **discovery** was narrower: sources I did not already know to look
> for may be missing. Flagged again in "Known gaps".

---

## Contents

**Part 1 — Source-by-source** (verdict in brackets)

1. SLSA (Supply-chain Levels for Software Artifacts)
2. in-toto Attestation Framework
3. CycloneDX — *the direct competitor vocabulary*
4. SPDX 3.x
5. STIX 2.1 (OASIS)
6. MITRE D3FEND — **the strongest single source in this survey**
7. MITRE ATT&CK, CAPEC, CWE, ATLAS, System of Trust
8. Identity schemes (short section — these are keys, not models)
9. OpenSSF Open Source Project Security Baseline (OSPS Baseline) — **best polling candidate**
10. OpenSSF Scorecard
11. OpenSSF Allstar
12. OpenVEX
13. Sigstore — the richest CI/CD *provenance attribute* vocabulary
14. TUF and gittuf
15. OpenSSF Security Insights — an under-appreciated find
16. S2C2F and OWASP SCVS — mine, don't poll
17. IETF SCITT and RATS — **two entity models the brief did not name, and both belong here**
18. OCSF (Open Cybersecurity Schema Framework)
19. OWASP Top 10 CI/CD Security Risks — the entity extraction
20. OWASP adjacent
21. SARIF — **the best structural match in the whole survey**
22. The identity / finding family
23. NIST SP 800-204D — **the citable authority for a CI/CD entity model**
24. NIST SSDF — SP 800-218 and SP 800-218A
25. CISA SBOM guidance — **the 2021 seven-field list is now superseded**
26. Other NIST material
27. CIS Software Supply Chain Security Guide — **the best-shaped entity taxonomy in this cluster**
28. Cloud Security Alliance
29. ENISA and the EU

**Part 2 — Synthesis**
- 2.1 Union list of ENTITY concepts
- 2.2 Union list of RELATIONSHIP concepts (+ the edge *properties* standards insist on)
- 2.3 The strong signal — concepts named by three or more independent standards
- 2.4 Naming guidance — the industry lingua franca, and where standards disagree
- 2.5 Update cadence and the polling seam (Tier 1 / 2 / 3)
- 2.6 Known gaps, UNVERIFIED items, and corrections to the brief

**If you read only three things:** §2.3 (the mandatory seventeen), §2.4 (what to call them),
§2.5 (how to keep this alive). **If you read only one source section:** §3 CycloneDX `formulation`.

---

## Part 1 — Source-by-source

### 1. SLSA (Supply-chain Levels for Software Artifacts)

| | |
|---|---|
| **Version / date** | **v1.2**, tag `v1.2` committed **2025-11-24** (VERIFIED via GitHub API on `slsa-framework/slsa`). Predecessors: v1.1 (2025-04-21), v1.0 (2023). Spec page banner: "This is Version 1.2 of the SLSA specification", status **Approved** (VERIFIED). |
| **URL** | https://slsa.dev/spec/v1.2/ · repo https://github.com/slsa-framework/slsa |
| **Kind** | Maturity-level control framework **plus** a genuine attestation *schema* (the provenance predicate). Two artifacts in one. |
| **Licence** | Spec text CC-BY-4.0; repo tooling Apache-2.0 (REPORTED — confirm before quoting text verbatim). OpenSSF project. |
| **Verdict** | **ADOPT** for the provenance entity names; **ALIGN** for the level model. |

SLSA v1.2 has **two tracks**:

**Build track** (L1–L3; a speculative L4 lives in *future directions*). Roles/entities it names
(VERIFIED from `/spec/v1.2/build-requirements`):
`producer`, `build platform`, `builder`, `consumer`, `verifier`, `package ecosystem`,
`external parameters`, `resolved dependencies`, `provenance`, `isolation`.
Named requirements: *Provenance Exists* (L1), *Provenance is Authentic* (L2), *Provenance is
Unforgeable* (L3); isolation strength *Hosted* (L2) and *Isolated* (L3).
⚠️ Unlike the Source track, the Build track's **levels do not carry short titles** in v1.2 — the
`/spec/v1.2/tracks` and `/about` pages describe them prosaically and defer to the requirement names
above (VERIFIED by fetching all three pages). Cite the requirement names, not invented level titles.

**Source track** (L1–L4) — new in the 2025 wave and **the most directly relevant thing in this whole
survey to a CI/CD graph**, because it is an entity model of a *forge*, not of a build. VERIFIED from
`/spec/v1.2/source-requirements`:

- Levels: **L1 Version Controlled**, **L2 History & Provenance**, **L3 Continuous Technical
  Controls**, **L4 Two-Party Review**.
- Entities: **Source Control System (SCS)**, **Organization**, **Repository**, **Revision**
  (logically immutable snapshot, e.g. a git commit SHA), **Named Reference** (branch = moving
  reference; tag = immutable pointer), **Protected Named Reference**, **Technical Control**,
  **Continuity** (an explicit first-class concept: a control is only meaningful if enforced
  *continuously* over a branch's history; a lapse *resets* continuity from a new revision),
  **Source Provenance Attestation**, **Source VSA**.
- Actor roles, enumerated: **Administrator**, **Trusted Person**, **Trusted Robot**, **Untrusted
  Person**. This is a small, opinionated authority vocabulary and it is *unusually well suited* to
  a graph — `Trusted Robot` in particular is the concept most models lack (a bot identity that is
  authorised, in scope, and exempt from two-party review under policy).

**Provenance predicate** (`https://slsa.dev/provenance/v1`) — this is literally an entity model
(VERIFIED from `/spec/v1.2/build-provenance`):

```
Provenance
├── buildDefinition
│   ├── buildType          (TypeURI — the template for how the build is performed)
│   ├── externalParameters (attacker-influenceable inputs; MUST be complete at Build L3)
│   ├── internalParameters (builder-controlled)
│   └── resolvedDependencies[]  → ResourceDescriptor
└── runDetails
    ├── builder { id (TypeURI), builderDependencies[] → ResourceDescriptor, version{} }
    ├── metadata { invocationId, startedOn, finishedOn }
    └── byproducts[] → ResourceDescriptor

ResourceDescriptor { uri, digest{sha256|sha512|gitCommit|…}, name,
                     downloadLocation, mediaType, content, annotations{} }
```

The `externalParameters` / `internalParameters` split is a **modelling idea worth stealing outright**:
it is exactly the trust-boundary distinction a CI/CD graph needs on a run's inputs, and no other
source in this survey draws it as cleanly.

**Machine-readable / update seam.** Git repo `slsa-framework/slsa`; the spec is markdown, not a
schema, but the provenance predicate has a **protobuf/JSON schema** in `in-toto/attestation`
(`spec/predicates/provenance.md` + the generated Go/proto types). Cadence is roughly annual
(v1.0 2023 → v1.1 2025-04 → v1.2 2025-11). "What changed" signal: GitHub **tags** on
`slsa-framework/slsa` (there are no GitHub *Releases* — VERIFIED, the releases endpoint is empty; poll
`/repos/slsa-framework/slsa/tags`), plus the versioned doc tree under `slsa.dev/spec/vX.Y/` and the
**`slsa.dev/blog`** feed — "Announcing SLSA v1.2" is dated **2025-11-24**, matching the tag exactly
(VERIFIED), so the blog is a reliable human-readable release signal.

**Future tracks** (explicitly speculative — VERIFIED from `/spec/v1.2/future-directions`): a **Build
L4** (pinned dependencies, hermetic builds, complete dependency documentation, reproducible builds)
and a **Platform Operations track** (approval/logging/auditing of physical and remote access to
platform infrastructure, cryptographic secrets, and privileged debugging interfaces). Do not model
these; do watch them — the Platform Operations track is where "who can SSH into the runner" becomes
a standard-named concept.

---

### 2. in-toto Attestation Framework

| | |
|---|---|
| **Version / date** | Framework spec **v1.2**; repo release **v1.2.0 published 2026-03-18** (VERIFIED via GitHub API). History: v1.0 2023-03-22, v1.1 2024-05-28, v1.1.1 2025-01-24, v1.1.2 2025-06-14, v1.2.0 2026-03-18. Core in-toto spec (layouts) is **v1.0.0** and has been stable for years. |
| **URL** | https://github.com/in-toto/attestation · core spec https://github.com/in-toto/docs/blob/master/in-toto-spec.md · ITEs https://github.com/in-toto/ITE |
| **Kind** | Schema (envelope/statement/predicate) **+** an authority model (the layout). CNCF-graduated project. |
| **Licence** | Apache-2.0 (VERIFIED — the ITE README states "developed under the Apache license"). |
| **Verdict** | **ADOPT** — for `subject`, `predicate`, `ResourceDescriptor`, and the predicate-type URIs as our attestation vocabulary. **ADOPT (concept)** for the layout's `functionary` / `step` / `inspection` authority model. |

**Layered model** (VERIFIED): **Envelope** (DSSE — authentication + serialisation) → **Statement**
(binds to subject, names the predicate type) → **Predicate** (type-specific payload) → **Bundle**
(grouping). Statement schema:

```
{ "_type": "https://in-toto.io/Statement/v1",
  "subject": [ ResourceDescriptor(digest REQUIRED) … ],
  "predicateType": "<URI>",
  "predicate": { … } }
```

Note the semantics: **subjects are matched purely by digest**, and are assumed immutable. That is a
strong hint for our own identity rules on artifacts.

**Vetted predicate registry** (VERIFIED — directory listing of `spec/predicates` plus each file's
`Type URI`/`Version` header):

| Predicate | Type URI | Version |
|---|---|---|
| SLSA Provenance | `https://slsa.dev/provenance/v1` | v1 |
| SLSA Verification Summary (VSA) | `https://slsa.dev/verification_summary/v1` | 1.0 |
| SCAI (Supply Chain Attribute Integrity) | `https://in-toto.io/attestation/scai` | 0.3 |
| Test Result | `https://in-toto.io/attestation/test-result/v0.1` | 0.1.0 |
| Runtime Traces | `https://in-toto.io/attestation/runtime-trace/v0.1` | 0.1.0 |
| Reference | `https://in-toto.io/attestation/reference/v0.1` | 0.1.0 |
| Release | `https://in-toto.io/attestation/release` | 0.2 |
| Simple Verification Result (SVR) | `https://in-toto.io/attestation/svr/v0.2` | 0.2 |
| VULNS (vuln scan results) | `https://in-toto.io/attestation/vulns` | 0.2 |
| CycloneDX BOM | `https://cyclonedx.org/bom` | 1.4 (predicate binding lags the 1.7 spec) |
| SPDX3 BOM | `https://spdx.dev/Document/v3` | 3.0 |
| SPDX2 BOM | see `spdx2.md` | — |
| Link (legacy, for in-toto 0.9 migration) | `https://in-toto.io/attestation/link/v0.3` | 0.3 |

This registry is a **taxonomy of "kinds of claim you can make about a CI/CD artifact"** — i.e. an
edge-type list in disguise: *provenance-of*, *verification-of*, *test-result-of*, *bom-of*,
*vuln-scan-of*, *release-of*, *runtime-trace-of*.

**The layout model** (core spec v1.0.0, VERIFIED). This is the part almost nobody quotes and it is an
**authority graph**:

- **Project owner** — defines the layout (the authoritative figure).
- **Functionary** — "an individual **or automated script**" authorised to perform a step. (Again the
  human/robot unification that CI/CD graphs need.)
- **Step** — `{ name, threshold, expected_materials[], expected_products[], pubkeys[],
  expected_command }`. `threshold` is an *n-of-m* requirement — multi-party control expressed as data.
- **Inspection** — `{ name, expected_materials[], expected_products[], run }` — a check performed at
  *verification* time on the client, not at build time.
- **Link** — the signed record of a step actually performed: materials, products, byproducts.
- **Materials / Products / Byproducts / Artifact / Final product / Sublayout.**

**Artifact rules — a genuine relationship vocabulary between steps** (VERIFIED, spec §4.3.3):
`MATCH <pattern> [IN <prefix>] WITH (MATERIALS|PRODUCTS) [IN <prefix>] FROM <step>`, `CREATE`,
`DELETE`, `MODIFY`, `ALLOW`, `REQUIRE`, `DISALLOW`. They are processed **like firewall rules** —
sequentially over a queue, first match consumes. `MATCH … FROM <step>` is precisely the
"this step's input is that step's output" edge that a pipeline graph must carry.

**ITEs (in-toto Enhancements)** (VERIFIED from the ITE README):
*Accepted* — ITE-1 (ITE format), ITE-2 (combining TUF + in-toto for compromise-resilient CI/CD),
ITE-3 (real-world TUF+in-toto: Datadog Agent integrations), ITE-4 (**generic URI schemes** — lets
artifacts be abstract, not just file paths; relevant to naming non-file nodes), ITE-5 (disassociate
signature envelope → DSSE), ITE-6 (**contextual attestations**), ITE-9 (new attestation types).
*Draft* — ITE-7 (X.509 signing/verification), ITE-10 (contextual attestations in layouts),
ITE-11 (**verifying attributes in attestations**).

**Update seam.** GitHub releases on `in-toto/attestation` (semver, ~2–3 per year), plus the
`spec/predicates/` directory listing via the GitHub contents API — a new file there is a new
predicate type and is exactly the kind of thing a scheduled job should raise a proposal for. Core
layout spec is effectively frozen at 1.0.0; watch the **ITE** repo for movement instead.

---

### 3. CycloneDX — *the direct competitor vocabulary*

| | |
|---|---|
| **Version / date** | **1.7** released **2025-10-21**; patch **1.7.1** on **2026-06-02** (VERIFIED via GitHub tag commit dates). Published as international standard **ECMA-424, 2nd edition, December 2025**, which specifies CycloneDX v1.7 (VERIFIED at ecma-international.org/publications-and-standards/standards/ecma-424/; the cyclonedx.org overview page gives the precise date 2025-12-10). Governance: OWASP + Ecma International **TC54**. |
| **URL** | https://cyclonedx.org/specification/overview/ · schema https://github.com/CycloneDX/specification/blob/master/schema/bom-1.7.schema.json |
| **Kind** | JSON/XML/protobuf **schema** — the most rigorously machine-readable artifact in this survey. |
| **Licence** | Apache-2.0 (VERIFIED — `$comment` in the schema file: "CycloneDX JSON schema is published under the terms of the Apache License 2.0"). |
| **Verdict** | **ADOPT** for `formulation` (workflow/task/step/trigger/input/output/workspace) and for `dependency` semantics. This is the single most important source in this survey for a CI/CD graph. |

**Top-level document properties (1.7, VERIFIED from the schema file):**
`bomFormat`, `specVersion`, `serialNumber`, `version`, `metadata`, `components`, `services`,
`externalReferences`, `dependencies`, `compositions`, `vulnerabilities`, `annotations`,
**`formulation`**, `declarations`, `definitions`, **`citations`** (new in 1.7), `properties`,
`signature`. (1.6 is identical minus `citations` — VERIFIED by diffing both schema files.)

#### 3a. `formulation` — CycloneDX's CI/CD model

> **Correction worth recording.** A summarising fetch of the human-readable 1.6 docs returned a
> 20-value `taskType` enum (analyze, assemble, attest, …). That is **wrong** — it does not exist in
> the schema. The real enum, read out of both `bom-1.6.schema.json` and `bom-1.7.schema.json`, is
> below. Always extract enums from the schema file.

```
formula   { bom-ref, components[], services[], workflows[], properties[] }
workflow  { bom-ref, uid, name, description, resourceReferences[], tasks[],
            taskDependencies[], taskTypes[], trigger, steps[], inputs[], outputs[],
            timeStart, timeEnd, workspaces[], runtimeTopology, properties[] }
            required: bom-ref, uid, taskTypes
task      { …identical shape to workflow, minus tasks/taskDependencies… }
step      { name, description, commands[], properties[] }
command   { executed, properties[] }
trigger   { bom-ref, uid, name, description, resourceReferences[], type, event,
            conditions[], timeActivated, inputs[], outputs[], properties[] }
event     { uid, description, timeReceived, data, source, target, properties[] }
condition { description, expression, properties[] }
workspace { bom-ref, uid, name, aliases[], description, resourceReferences[],
            accessMode, mountPath, managedDataType, volumeRequest, volume, properties[] }
volume    { uid, name, mode, path, sizeAllocated, persistent, remote, properties[] }
inputType { source, target, resource, parameters[], environmentVars[], data, properties[] }
outputType{ type, source, target, resource, data, environmentVars[], properties[] }
parameter { name, value, dataType }
resourceReferenceChoice { ref | externalReference }
```

- **`taskType` enum (VERIFIED, identical in 1.6 and 1.7):** `copy`, `clone`, `lint`, `scan`, `merge`,
  `build`, `test`, `deliver`, `deploy`, `release`, `clean`, `other`.
- **`trigger.type` enum (VERIFIED):** `manual`, `api`, `webhook`, `scheduled`.
- **`workflow.taskDependencies[]`** is an explicit **DAG edge list between tasks** — CycloneDX already
  models the pipeline as a graph, not a list.
- **`runtimeTopology`** on both workflow and task — a further dependency-graph field.
- `inputType.source`/`target` are documented with examples "source code repository", "database",
  "workspace" — i.e. **data-flow edges from a repo into a task and out to a workspace**.

This is the closest thing in the standards world to what git-serious is modelling. **We should not
invent a different word for `workflow`, `task`, `step`, `trigger`, or `workspace`.**

**What 1.7 added** (from the release notes; note that a summarising fetch of the releases page returned
badly wrong *years* — trust the tag commit dates above instead): data provenance & **citations**;
intellectual-property transparency (patents); cryptographic assurance (CBOM); multiple SPDX licence
expressions; **external components with version ranges**; **Traffic Light Protocol distribution
constraints** (`metadata.distributionConstraints`); and — most relevant to us — **"expanded
formulations", extended to describe how *any* referenceable BOM object came together**. The formulation
model is actively growing in our direction.

#### 3b. `dependencies` — the relationship object (VERIFIED)
`dependency { ref, dependsOn[], provides[] }`. Only two relationship kinds: **`dependsOn`** and
**`provides`** (the latter added for "implements a specification/standard", e.g. a crypto library
providing TLS 1.3). Deliberately thin compared to SPDX.

#### 3c. `declarations` — attestations/claims (VERIFIED)
`assessors[]` `{bom-ref, thirdParty, organization}` · `attestations[]` `{summary, assessor, map,
signature}` · `claims[]` `{bom-ref, target, predicate, mitigationStrategies, reasoning, evidence,
counterEvidence, externalReferences, signature}` · `evidence[]` `{bom-ref, propertyName, description,
data, created, expires, author, reviewer, signature}` · `targets` `{organizations, components,
services}` · `affirmation` `{statement, signatories, signature}`.
The **`evidence` / `counterEvidence`** pair is unusual and good — a claim that carries what argues
*against* it. Worth stealing for any compliance-flavoured edge.

#### 3d. `definitions.standards` — a compliance-catalogue model (VERIFIED)
`standard { bom-ref, name, version, description, owner, requirements[], levels[],
externalReferences[], signature }`; `requirement { bom-ref, identifier, title, text, descriptions[],
openCre, parent, properties, externalReferences }`; `level { bom-ref, identifier, title, description,
requirements[] }`. Note `requirement.parent` (a requirement hierarchy) and `openCre` (a cross-standard
mapping id). CycloneDX 1.7 also adds top-level `definitions.patents`.

#### 3e. Other 1.7 enums worth having in front of you (all VERIFIED from the schema)
- `component.type`: `application`, `framework`, `library`, `container`, `platform`,
  `operating-system`, `device`, `device-driver`, `firmware`, `file`, `machine-learning-model`,
  `data`, `cryptographic-asset`.
- `metadata.lifecycles[].phase`: `design`, `pre-build`, `build`, `post-build`, `operations`,
  `discovery`, `decommission`.
- `externalReference.type` (46 values — an under-appreciated dictionary of *"kinds of thing a
  project links to"*): `vcs`, `issue-tracker`, `website`, `advisories`, `bom`, `mailing-list`,
  `social`, `chat`, `documentation`, `support`, `source-distribution`, `distribution`,
  `distribution-intake`, `license`, `build-meta`, `build-system`, `release-notes`,
  `security-contact`, `model-card`, `log`, `configuration`, `evidence`, `formulation`,
  `attestation`, `threat-model`, `adversary-model`, `risk-assessment`, `vulnerability-assertion`,
  `exploitability-statement`, `pentest-report`, `static-analysis-report`, `dynamic-analysis-report`,
  `runtime-analysis-report`, `component-analysis-report`, `maturity-report`, `certification-report`,
  `codified-infrastructure`, `quality-metrics`, `poam`, `electronic-signature`, `digital-signature`,
  `rfc-9116`, `patent`, `patent-family`, `patent-assertion`, `citation`, `other`.
- `component.pedigree`: `ancestors`, `descendants`, `variants`, `commits`, `patches`, `notes` — a
  **lineage relationship vocabulary** for components. `commit { uid, url, author, committer, message }`.
- `componentEvidence.identity.field`: `group`, `name`, `version`, `purl`, `cpe`, `omniborId`,
  `swhid`, `swid`, `hash`; `.methods[].technique`: `source-code-analysis`, `binary-analysis`,
  `manifest-analysis`, `ast-fingerprint`, `hash-comparison`, `instrumentation`, `dynamic-analysis`,
  `filename`, `attestation`, `other`. **This is a confidence-and-provenance model for identity
  claims** — directly applicable to "how do we know this node is that thing".
- VEX: `impactAnalysisState` = `resolved`, `resolved_with_pedigree`, `exploitable`, `in_triage`,
  `false_positive`, `not_affected`; `impactAnalysisJustification` = `code_not_present`,
  `code_not_reachable`, `requires_configuration`, `requires_dependency`, `requires_environment`,
  `protected_by_compiler`, `protected_at_runtime`, `protected_at_perimeter`,
  `protected_by_mitigating_control`.
- `compositions.aggregate`: `complete`, `incomplete`, `incomplete_first_party_only`,
  `incomplete_first_party_proprietary_only`, `incomplete_first_party_opensource_only`,
  `incomplete_third_party_only`, `incomplete_third_party_proprietary_only`,
  `incomplete_third_party_opensource_only`, `unknown`, `not_specified`. **A completeness-of-knowledge
  vocabulary** — the honest answer to "is this subgraph the whole story?", which a graph product
  needs and rarely has.
- `service`: `{bom-ref, provider, group, name, version, description, endpoints[], authenticated,
  x-trust-boundary, trustZone, data[], …}` — `x-trust-boundary` and `trustZone` are the SaaSBOM
  trust-boundary concepts.

**Update seam.** Poll the raw schema files
`https://raw.githubusercontent.com/CycloneDX/specification/master/schema/bom-1.<N>.schema.json`
(and `.xsd`, `.proto`); diff the `enum` arrays. Tags on `CycloneDX/specification` give the version
signal (1.7 → 2025-10-21, 1.7.1 → 2026-06-02). Minor versions roughly annual; patch releases in
between. Because it is now **ECMA-424**, expect Ecma's own edition cadence to become a second signal.

---

### 4. SPDX 3.x

| | |
|---|---|
| **Version / date** | **3.0.1** released **2024-12-17**; **3.1-RC1** pre-release **2026-01-24** (VERIFIED via GitHub releases on `spdx/spdx-spec`). 3.0 was 2024-04-15. SPDX 2.x (ISO/IEC 5962:2021) remains widely deployed. |
| **URL** | https://spdx.github.io/spdx-spec/v3.0.1/ · model repo https://github.com/spdx/spdx-3-model |
| **Kind** | A real **class model / ontology** (RDF-shaped, serialised as JSON-LD), not just a file format. This is the big change in 3.x. |
| **Licence** | Model files carry `SPDX-License-Identifier: Community-Spec-1.0` (VERIFIED from the file headers). Community Spec 1.0 is permissive for implementation; check before copying prose. |
| **Verdict** | **ADOPT** the `RelationshipType` vocabulary (see below — it is the single best relationship dictionary found). **ALIGN** the class model. |

**Profiles present in the model repo `main` branch (VERIFIED via GitHub contents API):**
`Core`, `Software`, `SimpleLicensing`, `ExpandedLicensing`, `Licensing`, `Security`, `Build`, `AI`,
`Dataset`, `Extension`, `Lite`, **`SupplyChain`**, **`Operations`**, **`Service`**,
**`FunctionalSafety`**, **`Hardware`**.
⚠️ The `ProfileIdentifierType` vocabulary on `main` still lists only `core, software,
simpleLicensing, expandedLicensing, security, build, ai, dataset, extension, lite` — so the four/six
newer profile directories are **in-development for 3.1 and not yet released**. Treat `SupplyChain`,
`Operations`, `Service`, `FunctionalSafety`, `Hardware` as **UNVERIFIED / pre-release**.

**Core classes (VERIFIED):** `Element`, `Artifact`, `Agent`, `Person`, `Organization`,
`SoftwareAgent`, `Tool`, `Relationship`, `LifecycleScopedRelationship`, `SupportRelationship`,
`RoleRelationship`, `ContactPointRelationship`, `Annotation`, `Bundle`, `Bom`, `ElementCollection`,
`ElementMap`, `SpdxDocument`, `CreationInfo`, `Hash`, `IntegrityMethod`, `ExternalIdentifier`,
`ExternalRef`, `ExternalMap`, `NamespaceMap`, `PackageVerificationCode`, `Location`,
`PhysicalLocation`, `DefinedProcess`, `DefinedType`, `Specification`, `Regulation`, `Requirement`,
`Role`, `IndividualElement`, `DictionaryEntry`, `PositiveIntegerRange`, plus measurement classes.

**Build profile — one class (VERIFIED):**
`Build { buildId, buildType (anyURI, required), buildStartTime, buildEndTime, configSourceUri[],
configSourceDigest[] → Hash, configSourceEntrypoint[], parameter[] → DictionaryEntry,
environment[] → DictionaryEntry }` + inherited `Element` properties.
Deliberately minimal: SPDX models the **build as a node** and pushes everything else onto
relationships (`hasInput`, `hasOutput`, `hasHost`, `invokedBy`). That is a design choice worth
copying — a build node plus rich typed edges beats a fat build record.

**Software profile (VERIFIED):** classes `SoftwareArtifact`, `Package`, `File`, `Snippet`, `Sbom`,
`ContentIdentifier`. Vocabularies: `SoftwarePurpose` (`application, archive, bom, configuration,
container, data, device, diskImage, deviceDriver, documentation, evidence, executable, file,
filesystemImage, firmware, framework, install, library, manifest, model, module, operatingSystem,
other, patch, platform, requirement, source, specification, test`), `SbomType`
(`design, source, build, deployed, runtime, analyzed`), `FileKindType`, `ContentIdentifierType`.

**Security profile (VERIFIED):** `Vulnerability`, `VulnAssessmentRelationship` and its subclasses —
`CvssV2/V3/V4VulnAssessmentRelationship`, `EpssVulnAssessmentRelationship`,
`ExploitCatalogVulnAssessmentRelationship`, `SsvcVulnAssessmentRelationship`,
`VexVulnAssessmentRelationship` and its four states (`VexAffected…`, `VexFixed…`, `VexNotAffected…`,
`VexUnderInvestigation…`). Vocabularies: `CvssSeverityType`, `ExploitCatalogType`,
`SsvcDecisionType`, `VexJustificationType`.
**Architecturally important:** SPDX makes an *assessment* a **subclass of Relationship**, not a node.
A CVSS score is an edge from a vulnerability to an element, carrying `score`/`severity`/`vectorString`.
This is the cleanest existing answer to the skill's Step-4 question "is the fact about the
relationship rather than either end?"

**SupplyChain profile (pre-release, UNVERIFIED as released):** an Action/Process pair for nearly every
verb — `AssemblyAction/Process`, `BoundaryCrossingAction`, `BoundaryDefinitionAction/Process`,
`ChangeAction/Process`, `CreateAction/Process`, `DestroyAction/Process`, `HarvestAction/Process`,
`InspectionAction/Process`, `InstantiateVirtualHardwareProcess`, `ManufactureAction/Process`,
`ModifyAction/Process`, `OutOfSpecAction`, `PlanAction/Process`, `ReproduceAction/Process`,
`ResolutionAction`, `ResponsibilityChangeAction/Process`, `State`, `StateAction`,
`StorageAction/Process`, `TestAction/Process`, `TransportAction/Process`, `UseAction/Process`,
`DefinedStateProcess`; vocabulary `ResponsibilityType`. This is a physical-supply-chain lens grafted
onto SPDX. **Verdict for this profile alone: REFERENCE** — it over-abstracts badly for software CI/CD
(a `TransportAction` is not a concept a pipeline graph needs), and it is not yet released.

#### SPDX 3 `RelationshipType` — the best relationship dictionary in this survey

The naming rule is stated in the vocabulary itself and is a good rule for us too:
> "`from` (is) (a) `RELATIONSHIP` `to`" — the name must complete that sentence.

Full entry list (VERIFIED, read from `model/Core/Vocabularies/RelationshipType.md`). **Bold = directly
CI/CD-relevant.**

`affects`, `amendedBy`, `ancestorOf`, `availableFrom`, **`configures`**, **`contains`**,
`coordinatedBy`, `copiedTo`, **`delegatedTo`**, **`dependsOn`**, `descendantOf`, `describes`,
`doesNotAffect`, `expandsTo`, `exploitCreatedBy`, `fixedBy`, `fixedIn`, `foundBy`, **`generates`**,
`hasAddedFile`, `hasAssessmentFor`, `hasAssociatedVulnerability`, `hasConcludedLicense`,
`hasDataFile`, `hasDeclaredLicense`, `hasDeletedFile`, **`hasDependencyManifest`**,
`hasDistributionArtifact`, `hasDocumentation`, `hasDynamicLink`, **`hasEvidence`**, `hasExample`,
**`hasHost`**, **`hasInput`**, `hasMetadata`, `hasOptionalComponent`, `hasOptionalDependency`,
**`hasOutput`**, `hasPrerequisite`, `hasProvidedDependency`, `hasRequirement`, `hasSpecification`,
`hasStaticLink`, **`hasTest`**, `hasTestCase`, `hasVariant`, **`invokedBy`**, `modifiedBy`, `other`,
`packagedBy`, `patchedBy`, `publishedBy`, `reportedBy`, `republishedBy`, `serializedInArtifact`,
`testedOn`, `trainedOn`, `underInvestigationFor`, **`usesTool`**.

Two structural features worth adopting wholesale:

1. **`LifecycleScopedRelationship`** — a relationship carries a **`scope`** drawn from
   `LifecycleScopeType`: `design`, `development`, `build`, `test`, `runtime`, `other`. So
   "A `dependsOn` B **at build time**" and "A `dependsOn` B **at runtime**" are the *same* edge type
   with different scope. This directly answers the skill's Step-4 "propose the edge's properties in
   the same breath" rule, and it is exactly the distinction a CI/CD graph gets wrong if it models
   dependency as a bare line.
2. **`RelationshipCompleteness`** — `complete` / `incomplete` / `noAssertion` **on the edge**. An
   honest "we do not know if this list is exhaustive" marker. Extremely rare in graph models and
   extremely useful in one.

Also: `ExternalIdentifierType` = `cpe22`, `cpe23`, `cve`, `email`, `gitoid`, `packageUrl`,
`securityOther`, `swhid`, `swid`, `urlScheme`, `other` — the identity-scheme dictionary.
`ExternalRefType` (46 values) is SPDX's sibling of CycloneDX's `externalReference.type`, including
`buildMeta`, `buildSystem`, `vcs`, `secureSoftwareAttestation`, `securityPolicy`,
`securityThreatModel`, `securityAdversaryModel`, `staticAnalysisReport`, `dynamicAnalysisReport`,
`runtimeAnalysisReport`, `vulnerabilityExploitabilityAssessment`, `eolNotice`, `funding`, `metrics`.

**Update seam.** GitHub releases on `spdx/spdx-spec` (3.0 → 3.0.1 → 3.1-RC1). The **model itself is
machine-readable** in `spdx/spdx-3-model` — one markdown file per class/property/vocabulary under
`model/<Profile>/{Classes,Properties,Vocabularies}/`, from which the official JSON-LD context,
OWL/SHACL and JSON schema are generated (`spdx/spdx-3-model` releases; also `spdx/spdx-spec` gh-pages).
**The cheapest possible poll:** `GET /repos/spdx/spdx-3-model/contents/model/Core/Vocabularies/RelationshipType.md`
and diff the entry list; a new relationship type appearing there is precisely a vocabulary proposal
for us. Same for `model/<Profile>/Classes` directory listings.

---

### 5. STIX 2.1 (OASIS)

| | |
|---|---|
| **Version / date** | **OASIS Standard, published 2021-06-10** (VERIFIED from the spec title page). **STIX 2.2: UNVERIFIED / no evidence found.** The CTI TC work-product repo shows a five-part 2.x split (Core, Objects, Cyber Observable Core, Cyber Observable Objects, Patterning) and 78 open issues, but no announced 2.2 draft. |
| **URL** | https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html · schemas https://github.com/oasis-open/cti-stix2-json-schemas · TC repo https://github.com/oasis-tcs/cti-stix2 |
| **Kind** | Schema + serialisation + **relationship taxonomy**. The JSON Schemas repo is explicitly *non-normative*. |
| **Licence** | OASIS IPR Policy — freely readable/implementable; the vocabulary terms are unencumbered. JSON Schemas repo is BSD-3-Clause. Reusing the *names* is unambiguously fine. |
| **Verdict** | **ADOPT (relationship vocabulary)** + **ALIGN (object types)**. |

**Objects.** 19 SDOs: Attack Pattern, Campaign, Course of Action, Grouping, **Identity**, Incident (a
deliberate stub in 2.1), Indicator, **Infrastructure**, Intrusion Set, Location, Malware, Malware
Analysis, Note, Observed Data, Opinion, Report, Threat Actor, **Tool**, Vulnerability.
2 SROs: **Relationship** (generic, carries `relationship_type`) and **Sighting**.
18 SCOs: Artifact, Autonomous System, Directory, Domain Name, Email Address, Email Message, **File**,
IPv4/IPv6 Address, MAC Address, Mutex, Network Traffic, **Process**, **Software**, **URL**,
**User Account**, Windows Registry Key, **X.509 Certificate**.

In 2.1 **SCOs can be the source or target of an SRO directly** — which is exactly the shape a CI/CD
graph needs.

**The relationship vocabulary — the reason this source matters.** Full de-duplicated
`relationship_type` set (VERIFIED against the OASIS validator's machine-encoded enum,
`stix2validator/v21/enums.py`):

`accesses-remote-machines`, `analysis-of`, `anti-debugging`, `anti-disassembly`, `anti-emulation`,
`anti-memory-forensics`, `anti-sandbox`, `anti-vm`, `attributed-to`, `authored-by`, `based-on`,
`beacons-to`, `belongs-to`, `characterizes`, `communicates-with`, `comprises`, `compromises`,
`consists-of`, `controls`, `delivers`, `derived-from`, `downloads`, `drops`, `duplicate-of`,
`dynamic-analysis-of`, `exfiltrates-to`, `exploits`, `has`, `hosts`, `impersonates`, `indicates`,
`investigates`, `located-at`, `mitigates`, `originates-from`, `owns`, `related-to`, `remediates`,
`resolves-to`, `static-analysis-of`, `targets`, `uses`, `variant-of`.

**The design lesson worth copying:** `COMMON_RELATIONSHIPS` — legal between *any* two objects — is
exactly **three**: `derived-from`, `duplicate-of`, `related-to`. Everything else is constrained by
source/target type pair. A tiny universal edge set plus a large typed-pair-constrained set is a
better model than either a free-for-all or a rigid schema.

Selected constraints relevant to us: `infrastructure —consists-of→` observed-data **and all 18 SCO
types**; `infrastructure —hosts→ tool|malware`; `threat-actor —owns|hosts|compromises→
infrastructure`; `tool —uses→ infrastructure`; `X —has→ vulnerability`; `course-of-action
—mitigates→ attack-pattern|indicator|malware|tool|vulnerability`; `indicator —based-on→
observed-data`.

**Update seam.** Git repo `oasis-open/cti-stix2-json-schemas` (JSON Schema, branch per STIX version;
no formal release feed — poll commits). Spec-level signal: the `docs.oasis-open.org/cti/stix/`
directory listing and the CTI TC issue tracker. Cadence: glacial (2021 → present, no minor release).

---

### 6. MITRE D3FEND — **the strongest single source in this survey**

| | |
|---|---|
| **Version / date** | **1.5.0** — ontology changelog says **2026-07-31**; git tag `1.5.0` dated **2026-08-04**. Tag history: 1.0.0 (2024-12-20), 1.1.0 (2025-04-21), 1.2.0 (2025-08-02), 1.3.0 (2025-12-16), 1.4.0 (2026-04-01), 1.5.0. ~4-month cadence. 1.5.0 refreshed its mappings to ATT&CK v19.0 and ATLAS v2026.06. |
| **URL** | https://d3fend.mitre.org/ · ontology https://d3fend.mitre.org/resources/ontology/ · artifact browser https://d3fend.mitre.org/dao/ · repo https://github.com/d3fend/d3fend-ontology |
| **Kind** | An explicit **OWL ontology / knowledge graph** — formal classes, object properties with domains/ranges, inverses, and inference. The only true ontology in this survey. |
| **Licence** | Ontology repo is **MIT** (VERIFIED) — the most permissive licence of any source here. Website/KG carries MITRE Terms of Use + public-release approval. |
| **Verdict** | **ADOPT** — class names, property names, the inverse-pair discipline, and the `may-*` modality. |

**Why it matters here:** D3FEND's `d3f:DigitalArtifact` tree already names the build/CI nouns, and its
**Model** tactic *is literally the product git-serious is building*.

**Build/CI subtree (VERIFIED from the artifact browser):**
`d3f:BuildTool` ("automates the process of creating a software build … compiling source code into
binary code, packaging binary code, and running automated tests"), superclass chain
`Artifact → DigitalArtifact → DigitalInformation → Software → Application → UserApplication →
DeveloperApplication → BuildTool`, subclasses **Compiler**, **SoftwarePackagingTool**,
**ContainerBuildTool**, **OperatingSystemPackagingTool**. Siblings: **VersionControlTool**,
**CodeAnalyzer** (Static / Dynamic / SourceCode), **TestExecutionTool** (Unit / Integration),
**SoftwareDeploymentTool**, **ApplicationInstaller**, **ContainerRuntime**,
**ContainerOrchestrationSoftware**, **CompilerConfigurationFile**, **ApplicationConfigurationFile**,
**ConfigurationManagementDatabase**.
`d3f:CodeRepository` — "a form of database where code, typically source code, is stored and managed"
(Git/Mercurial/SVN/CVS/Perforce); synonyms *Version Control Repository, Repository*.
`d3f:SoftwarePackage` — chain `… → DigitalInformationBearer → ComputingImage → ContainerImage →
SoftwarePackage`; subclasses **ContainerImage**, **JavaArchive**, **PythonPackage**; and it
**cross-references the OCSF `package` object**.
`d3f:Credential` subclasses: **AccessToken, WebAccessToken, SessionToken, SessionCookie,
WebIdentityToken, Password, EncryptedPassword, EncryptedCredential, KerberosTicket (+TGT/TGS),
DigitalAccessBadge**. Plus **UserAccount** variants (Local, Domain, Global, **Service**, Privileged),
Process/Thread/ChildProcess/ParentProcess/ProcessTree, ExecutableFile, ConfigurationFile, **Log**,
**JobSchedule**, **Dependency**, **Repository**, **Resource**, **Identifier**, **Metadata**.

**Object properties (~200, systematically paired with inverses and shadowed by `may-*` possibility
variants).** Relevant selections:

- *Structural:* `contains`/`contained-by`/`may-contain`/`may-be-contained-by`, `has-member`/`member-of`,
  `depends-on`/`dependent`/`has-dependent`, `derived-from`, `copies`/`copy-of`, `extends`,
  `has-input`/`input-of`, `has-output`/`output-of`, `has-prerequisite`, `precedes`/`preceded-by`,
  `next`, `start`/`end`, `fork`.
- *Action:* `accesses`/`accessed-by`/`may-access`, `creates`/`created-by`, `produces`/`produced-by`,
  `executes`/`executed-by`, `runs`, `invokes`/`invoked-by`, `loads`/`loaded-by`, `installs`, `reads`,
  `writes`, `updates`, `deletes`, `modifies`/`modified-by`, `transmits`, `receives`, `queries`,
  `records`/`recorded-in`, `encrypts`, **`signs`/`signed-by`**, `validates`/`validated-by`, `verifies`,
  `configures`, `manages`, `operates`, `owns`, `uses`/`used-by`, `employs`/`employed-by`,
  `implements`/`implemented-by`, `prescribes`/`prescribed-by` (new 1.5.0), `carries`/`carried-by`
  (new 1.4.0), `identifies`/`identified-by`, `inventories`/`inventoried-by`,
  `has-weakness`/`weakness-of`/`may-have-weakness`, `causes`/`caused-by`, `communicates-with`,
  `connects`/`connected-to`, `originates-from`, `participates-in`.
- *Tactical verbs (the seven tactics as edges):* `hardens`, `detects`, `isolates`, `deceives`,
  `evicts`, `restores`, `analyzes`, `evaluates`, `monitors`, `enumerates`, `filters`, `blocks`,
  `neutralizes`, `quarantines`, `restricts`, `terminates`, `suspends`, `counters`, `enforces`,
  `authenticates`, `authorizes`, `mediates-access-to`/`access-mediated-by`, `limits`, `disables`.
- *Semantic scaffolding:* `broader`/`narrower` (+ transitive), `related`,
  `associated-with`/`may-be-associated-with`, `semantic-relation`, `kb-reference`.

**Tactics:** Model, Harden, Detect, Isolate, Deceive, Evict, Restore. The **Model** tactic's 27 base
techniques read like our feature list: **D3-AI Asset Inventory**, **D3-SWI Software Inventory**,
**D3-CI Configuration Inventory**, D3-DI Data Inventory, **D3-CIA Container Image Analysis**,
**D3-AVE Asset Vulnerability Enumeration**, **D3-SYSM System Mapping**, **D3-SYSDM System Dependency
Mapping**, **D3-SVCDM Service Dependency Mapping**, D3-ODM Operational Dependency Mapping,
**D3-AM Access Modeling**, **D3-OM Organization Mapping**, D3-NM Network Mapping.

**Known limitation (VERIFIED, and important).** Artifact pages for `CodeRepository`, `BuildTool`,
`SoftwarePackage` and `Credential` currently show **empty "Neighbors" / "Inferred Relationships"
sections** in 1.5.0. The *classes* are rich; the *instance-level artifact-to-artifact assertions* for
the build subtree are thin. **So: adopt the vocabulary, expect to author our own edges using their
names.** That is still a large win — we get the names and the discipline without the debt.

**Update seam.** `https://d3fend.mitre.org/ontologies/d3fend.ttl` / `.owl` / `.json` (JSON-LD), plus
versioned CSV at `https://d3fend.mitre.org/ontologies/d3fend/1.5.0/d3fend.csv`, plus inferred-
relationship CSV/JSON. Git source `d3fend/d3fend-ontology` (`src/ontology/d3fend-protege.ttl` →
`dist/`). **GitHub Releases are empty — poll the git *tags*** plus `https://d3fend.mitre.org/changelog/`.
An alpha REST API exists at `/api-docs` (exact endpoint paths UNVERIFIED). A standalone public
**SPARQL endpoint URL was NOT confirmed** — SPARQL is available inside the D3FEND CAD tool's query
tab, and the ontology page says the queries are "being open sourced soon". **Do not promise SPARQL.**

---

### 7. MITRE ATT&CK, CAPEC, CWE, ATLAS, System of Trust

These are **threat/weakness taxonomies, not entity models.** They belong in our *findings* vocabulary,
not our *node* vocabulary. Reported compactly for that reason.

**MITRE ATT&CK — v19.2, released 2026-08-06** (VERIFIED; the first "Agile release", a narrower
out-of-cycle update). Preceding major: **v19, 2026-04-28** (+ v19.1 patch).
⚠️ *Correction to the brief:* the April 2026 release is **v19, not v18**.
Object model (from `attack-stix-data/USAGE.md`): Technique/Sub-technique → `attack-pattern`
(+`x_mitre_is_subtechnique`); Tactic → `x-mitre-tactic`; Group → `intrusion-set`; Software →
`tool`/`malware`; Mitigation → `course-of-action`; Campaign → `campaign`; Matrix → `x-mitre-matrix`;
**Detection Strategy → `x-mitre-detection-strategy`**; plus `x-mitre-data-source`,
`x-mitre-data-component`, `x-mitre-asset`, `x-mitre-analytic`, `x-mitre-log-source`. v17–v19
restructured detections into **Detection Strategy (DET####) → platform Analytics (AN####)**. v19 also
**split Defense Evasion into "Stealth" and "Defense Impairment"**. Enterprise v19: 15 tactics, 222
techniques, 475 sub-techniques, 949 software, 178 groups, 59 campaigns.
Relationship types (small verb set, large node set): `uses`, `mitigates`, **`subtechnique-of`**,
`attributed-to`, **`detects`**, `revoked-by`.
CI/CD-relevant techniques (all individually VERIFIED): **T1195** Supply Chain Compromise (v1.7,
mod. 2025-10-24) → **.001 Compromise Software Dependencies and Development Tools** (v1.3, mod.
2026-05-12 — explicitly names GitHub Actions, "the building, testing, and deployment cycles",
runtime credential collection, npm/PyPI/yarn/cargo/maven/gradle/Homebrew, typosquatting, abandoned-
package re-registration, VS Code extensions, Xcode/CocoaPods; cites ShinyHunters compromising CI/CD
via Git/BrowserStack/JFrog, and TeamPCP across NPM/VS Code/Docker/PyPI), .002, .003;
**T1554** Compromise Host Software Binary (v2.2); **T1078** Valid Accounts (v3.0) + .001–.004
(.004 Cloud Accounts); **T1199** Trusted Relationship (v2.4; platforms now include Identity Provider,
SaaS); **T1072** Software Deployment Tools (v3.2 — explicitly says these are "integrated into CI/CD
pipelines"); **T1552** Unsecured Credentials (v1.5) + .001 Credentials In Files, .004 Private Keys,
.005 Cloud Instance Metadata API, **.007 Container API**; **T1528** Steal Application Access Token
(v1.5 — explicitly covers **CI/CD pipeline tokens** and Kubernetes service-account tokens; names
TeamPCP, Shai-Hulud, Mini Shai-Hulud, Peirates); **T1526** Cloud Service Discovery; **T1648**
Serverless Execution.
**Is there a CI/CD matrix? No** (VERIFIED). Enterprise/Mobile/ICS only; CI/CD appears as prose inside
techniques and as new *platforms* (Containers, IaaS, SaaS, Identity Provider). The "CI/CD matrix"
people cite is OWASP's, not MITRE's.
Licence: ATT&CK Terms of Use — non-exclusive, royalty-free, **including commercial**, with a mandatory
copyright/permission notice.
Update seam: `https://github.com/mitre-attack/attack-stix-data`, STIX 2.1 JSON at
`{domain}/{domain}.json` and pinned `{domain}/{domain}-{version}.json`; **`index.json` is the
machine-readable collection index — poll that.** Human signal: `attack.mitre.org/resources/updates/`.
**Verdict: REFERENCE** (+ narrow **ALIGN** on `subtechnique-of` / `mitigates` / `detects` spellings).

**MITRE CAPEC — 3.9, released 2023-01-24**, 559 attack patterns (VERIFIED; no newer release found on
any primary page as of 2026-08-27 — i.e. **dormant for over three years**). Schema 3.5.
Relationship natures: **ChildOf, ParentOf, CanPrecede, CanFollow, PeerOf, CanAlsoBe, MemberOf,
HasMember**. Cross-taxonomy links use separate mechanisms (`Related_Weaknesses` → CWE;
`Taxonomy_Mappings` → ATT&CK).
Supply-chain patterns: 437 (Supply Chain category), 438, 439, 441, 442, 443, **444 Development
Alteration** (the hub: ParentOf 206, 443, 445, 446, 511, 516, 520, 532, 537, 538, 539, 670, 672, 673,
678), 445, 446, 447, 452, **511 Infiltration of Software Development Environment**, **538 Open-Source
Library Manipulation**, **669 Alteration of a Software Update**, **670 Software Development Tools
Maliciously Altered** (670 CanPrecede 669).
Machine-readable: `https://capec.mitre.org/data/xml/capec_latest.xml` (**XML only — no JSON, no git
mirror**; the worst plumbing in this survey). Licence: MITRE custom terms, royalty-free incl.
commercial, mandatory attribution.
**Verdict: REFERENCE** — but **borrow the `CanPrecede`/`CanFollow` sequencing idea**, which STIX lacks
and a pipeline graph needs.

**MITRE CWE — 4.20, released 2026-04-30** (homepage news; ⚠️ a separate `/data/index.html` page said
"Last Updated: November 19, 2024" — inconsistent; treat 4.20 as current and the 2024 date as a stale
page artifact). 944 weaknesses. Relationship natures (richer than CAPEC's): **ChildOf, ParentOf,
StartsWith, CanPrecede, CanFollow, Requires, RequiredBy, CanAlsoBe, PeerOf, MemberOf, HasMember**.
Relevant CWEs: 1104, 1357 (discusses SBOMs), 1395, 506, 507, 494, 829, 798, 540, 522.
Note CWE-699 (Software Development view) has **no dedicated supply-chain branch**.
Machine-readable: XML+XSD, per-view CSV, plus a REST API, at `cwe.mitre.org/data/downloads.html`.
**Verdict: REFERENCE** — finding labels only.

**MITRE ATLAS — v2026.07, published 2026-08-07** (VERIFIED; data file carries
`collection.version: '2026.07'`, `modified-date: '2026-05-27'`). Versioning split May 2026: content
is `YYYY.MM[.N]`, the data *format* schema is independent semver (currently **6.0.0**). 16 tactics,
101 techniques + 77 sub-techniques, 37 mitigations, 68 case studies.
CI/CD relevance is real: **AML.T0010 AI Supply Chain Compromise** (renamed from "ML Supply Chain
Compromise") now has six sub-techniques including **.004 Container Registry** (explicitly names CI/CD
pipelines pulling manipulated container images) and **.005 AI Agent Tool** (poisoned MCP servers,
npm-hosted tools); plus **AML.T0109 AI Supply Chain Rug Pull**, **AML.T0110 AI Agent Tool Poisoning**,
**AML.T0018 Manipulate AI Model** (.002 Embed Malware — pickle RCE).
Relationship types: a typed `relationships` section with **`employs`** (carrying `tactic`, `step-id`)
and **`leads-to`** — a chained-procedure model.
Licence **Apache-2.0** on `mitre-atlas/atlas-data` (VERIFIED). Machine-readable YAML at
`dist/v6/ATLAS-*.yaml`; **real GitHub Releases** name added/changed techniques per release — the
cleanest thing to poll in the MITRE family.
**Verdict: REFERENCE** — adopt only if model/dataset artifacts enter scope.

**MITRE System of Trust (SoT)** — Body of Knowledge risk catalog **v1.4.1** with a v1.5 draft;
**release date UNVERIFIED**. https://sot.mitre.org/
Structure: three trust aspects — **Suppliers, Supplies, Services** — decomposed four levels:
15 top-level risk areas → 200+ sub-areas → 700+ risk factors → 1,300+ risk measurement questions.
Top-level categories (wording **approximate/UNVERIFIED**): *Suppliers* — financial stability,
organizational security, susceptibility to external influence, quality culture, organizational
effectiveness, ethical risks, external influences; *Supplies* — malicious taint, counterfeit,
hygiene, availability; *Services* — quality, resilience, security, integrity.
**Relationship types: none typed** — containment/decomposition only.
Machine-readable: **none found.** The Risk Model Manager prototype exports spreadsheets; access
requires registration; the only version signal is a filename (`SoT_BoK_Risk_Catalog_v1.4.1.docx`).
Licence permissiveness **UNVERIFIED**.
**Verdict: REFERENCE, not ADOPT.** The Supplier/Supply/Service trichotomy and the "malicious taint /
counterfeit / hygiene" risk labels are useful framings to cite. But there is nothing to poll, nothing
typed, and the artifact is Word documents behind a registration wall — it fails every reusability
test D3FEND passes.

**MITRE EMB3D — 2.0.2, released 2026-06-01.** Device Properties → 226 Threats → 89 Mitigations, for
embedded/IoT/OT. **IGNORE** — device-centric, no CI/CD, build-system, or provenance surface.

---

### 8. Identity schemes (short section — these are keys, not models)

| Scheme | Version / date | Verdict |
|---|---|---|
| **PURL (Package URL)** | **ECMA-427, 1st edition, December 2025** (VERIFIED at ecma-international.org/…/ecma-427/), developed by Ecma **TC54**; "in process to also become an ISO standard" (REPORTED). Form `pkg:type/namespace/name@version?qualifiers#subpath` — seven components. ⚠️ ECMA-427 standardises the **syntax and the type-definition schema only**; it deliberately does **not** define the ecosystem types (`maven`, `pypi`, `npm`, …), which remain in the `package-url/purl-spec` repo — so poll *both*. https://tc54.org/purl/ · https://github.com/package-url/purl-spec | **ADOPT.** The best cross-ecosystem identity key for dependencies and build artifacts, and now a real standards-body product. SPDX, CycloneDX, OSV, OpenVEX and D3FEND all speak it. |
| **CVE Record Format** | JSON 5.x line, `dataVersion` **5.2.0** (VERIFIED). Model: CVE Record → one `cnaContainer` + zero-or-more `adpContainers` (ADP enrichment, e.g. CISA). https://github.com/CVEProject/cve-schema | **ADOPT as an identifier**, not as a model. |
| **CPE 2.3** | NIST IR 7695, final **2011-08-19**. 11 WFN attributes (part, vendor, product, version, update, edition, language, sw_edition, target_sw, target_hw, other) — list is well-established but **not re-quoted verbatim from IR 7695 this pass**. | **REFERENCE.** Aging; PURL is the better key for build artifacts. Keep CPE only for matching against NVD. |
| **SWHID / OmniBOR / gitoid / SWID** | Named as `ExternalIdentifierType` values by SPDX 3 and as `componentEvidence.identity.field` values by CycloneDX 1.7 (both VERIFIED). Individual specs not surveyed. | **REFERENCE** — carry them as identifier fields because the BOM standards do; do not model them. |

---

### 9. OpenSSF Open Source Project Security Baseline (OSPS Baseline) — **best polling candidate**

| | |
|---|---|
| **Version / date** | **v2026.02.19** (released 2026-02-19; single git tag `v2026.02.19`). ⚠️ The repo publishes **no GitHub Releases** — versioning is by tag and by site version directories. |
| **URL** | https://baseline.openssf.org/ · https://github.com/ossf/security-baseline |
| **Kind** | **Machine-readable control catalogue in YAML**, conforming to the **Gemara** meta-schema. Ships an accompanying **lexicon** — literally a dictionary of entities. |
| **Licence** | **Apache-2.0** (VERIFIED). |
| **Verdict** | **ADOPT** — this should be our primary external vocabulary anchor. |

8 families, 41 controls, ~60 assessment requirements. ID scheme `OSPS-<FAMILY>-<NN>` for controls,
`OSPS-<FAMILY>-<NN>.<NN>` for assessment requirements. YAML shape (VERIFIED by fetching `OSPS-BR.yaml`):
top-level keys `groups` and `controls`; each control is `{id, title, objective, group,
assessment-requirements[]}`; each requirement is `{id, text (MUST/MUST NOT), applicability:
[maturity-1|maturity-2|maturity-3], recommendation, state?}`. Note the optional **`state: Retired`**
field with the retiring PR URL in `text` — the catalogue carries its own requirement lifecycle, which
is exactly what an update-seam ledger needs to consume.

- **OSPS-AC Access Control** (4): MFA for Sensitive Actions; Restrict Collaborator Permissions;
  Protect Primary Branch from Accidental Modification; **Enforce Least Privilege on CI/CD Pipelines**.
- **OSPS-BR Build and Release** (7): Prevent Untrusted Input When Building & Releasing; Assign Unique
  Version Identifiers; Use Encrypted Channels for Development & Release Activity; Publish Change Log
  With Release; Use Standardized Dependency Management Tools; Include Signatures and Hashes With
  Release; Secure Secrets and Credentials.
- **OSPS-DO Documentation** (7): user guides; defect reporting; **provenance verification
  instructions**; support scope/duration; security update scope; dependency management policy;
  build-from-source instructions.
- **OSPS-GV Governance** (4): roles & responsibilities; public discussion; contribution guide;
  **formal review of permission grants**.
- **OSPS-LE Legal** (3): contributors assert right to commit (DCO/CLA); licences fully open source;
  licences in a well-known location.
- **OSPS-QA Quality** (7): publish source & change history; publish dependencies; pass/fail checks
  before accepting changes; security requirements on all codebases; prevent executables in codebase;
  automated testing in CI/CD; require merge approvals.
- **OSPS-SA Security Assessment** (3): design descriptions of **system actors and actions**; external
  interface descriptions; project security assessment.
- **OSPS-VM Vulnerability Management** (6): CVD policy; reporting contacts/process; private
  vulnerability reporting; publish discovered vulns; dependency remediation policy; appsec testing
  policy.

Maturity levels (from `metadata.yaml`): **maturity-1** any project/any maintainer count;
**maturity-2** code project, ≥2 maintainers, small consistent user base; **maturity-3** large
consistent user base.

**`baseline/lexicon.yaml` is the find of this survey** — 486 lines, **51 terms, 28 with synonym
lists**, Apache-2.0, machine-readable, and scoped to exactly our domain. Terms include:
*Administrator, Arbitrary Code, Automated Test Suite, **Build and Release Pipeline**, **CI/CD
Pipeline**, Change, Code, Collaborator, **Commit**, Contributor, Contributor License Agreement,
Coordinated Vulnerability Disclosure, Defect, Developer Certificate of Origin, Exploitable
Vulnerabilities, Known Vulnerabilities, License, **Maintainer**, Multi-factor Authentication,
**Primary Branch**, Private Vulnerability Reporting, **Project**, Project Documentation, **Release**,
**Released Software Asset**, **Repository**, Sensitive Data, Sensitive Resource, Software Bill of
Materials, Software Composition Analysis, **Software Provenance**, **Status Check**, **Subproject**,
Threat Modeling, **User**, **Version Control System**, Version Identifier, Vulnerability Reporting.*

Note the deliberate distinction between *CI/CD Pipeline* (generic) and *Build and Release Pipeline*
("excludes some pipelines, such as pre-merge status checks"). That boundary is one a naive graph model
gets wrong, and OSPS has already argued it out.

**The definitions that would actually settle naming arguments for us** (VERIFIED by fetching
`lexicon.yaml` directly — 52 entries; these are the load-bearing ones):

| Term | OSPS definition (condensed) |
|---|---|
| **Administrator** | "Any human who can modify settings on the target resource." |
| **Collaborator** | "Any entity with permissions issued by repository administrators." |
| **Contributor** | "Any entity that has made a change to repository contents." |
| **Maintainer** | "**Human** collaborator authorized to approve changes to repository contents." |
| **User** | "**Human** using project resources including software and documentation." (syn. Person) |
| **Project** | "Group of people **and resources** coordinating to produce a release." |
| **Subproject** | "Codebase part of the project maintained in a **separate repository**." |
| **Repository** | "Storage location managed by version control system for code and resources." |
| **Primary Branch** | "Main development branch representing the latest stable codebase for releases." |
| **Commit** | "Single change record in version control with modifications, contributor details, and timestamp." |
| **Change** | "Any alteration to project codebase, **CI/CD pipelines, or documentation**." |
| **Status Check** | "Automated validations running on commits **before merging**." |
| **CI/CD Pipeline** | "Automated pipelines for continuous integration, testing, building, and delivery of changes." |
| **Build and Release Pipeline** | "Automated processes that compile and deploy software." |
| **Release** | *verb* making version-controlled assets available; *noun* the version-controlled bundle provided to users. |
| **Released Software Asset** | "Deliverables provided to users as part of a release (binaries, libraries, containers)." |
| **Software Provenance** | "Information about the origin and history of released software assets." |
| **Sensitive Resource** | "Resources that, if compromised, would provide vectors for **compromising software delivery**." |
| **Arbitrary Code** | "Code from an external source executed by a system without validation or restriction." |

Three of these settle real modelling questions on their own: **Contributor vs Collaborator vs
Maintainer** are cleanly separated by *made a change* / *holds permissions* / *human who can approve*;
**Maintainer and User are explicitly human** while Contributor and Collaborator are "any entity" (so a
bot can be a contributor but not a maintainer); and **Project explicitly includes resources**, not just
people. The lexicon also carries pointers to the other frameworks as terms (CRA, CSF, SSDF, SLSA,
SAMM, P-SSCRM, PCIDSS, OpenChain/ISO 5230+18974, OpenCRE, OpenEoX, Scorecard, 800-161) — i.e. it
doubles as a cross-standard index.

**Update seam — the most concrete in this report.** All raw and unauthenticated:
- `https://raw.githubusercontent.com/ossf/security-baseline/main/baseline/OSPS-{AC,BR,DO,GV,LE,QA,SA,VM}.yaml`
- `https://raw.githubusercontent.com/ossf/security-baseline/main/baseline/lexicon.yaml`
- `https://raw.githubusercontent.com/ossf/security-baseline/main/baseline/metadata.yaml` — declares
  `gemara-version: 1.2.0`, `type: ControlCatalog`, `draft: true`, the three maturity definitions, and
  **20 `mapping-references`** (VERIFIED by fetching the file): `BPB` (OpenSSF Best Practices Badge,
  2024), `Scorecard` (5.0), `CSF` (NIST CSF 2.0), `CRA` (2024-11-20), `SSDF` (1.1), `ISO-18974`
  (1.0, 2023-12), `OpenCRE` (2024), `SLSA` (1.0), `PSSCRM` (1.0), `SAMM` (2.0), `PCIDSS` (4.0.1),
  `800-161` (r1-upd1), `UKSSCOP` (UK NCSC Software Security Code of Practice, 2025-05-07), `DORA`,
  `NIS2`, `CSbDP` (CISA Secure by Design Pledge), `CSAG` (CISA Software Acquisition Guide), `USCTM`
  (US Cyber Trust Mark), `MAF` (MITRE ATT&CK, **v18**), `BSI-TR-03185-2` (v1.1.0).
  **This single file is the best cross-standard index found anywhere in this survey.**
  ⚠️ And it is *itself* a live demonstration of standards lag: it pins Scorecard at **5.0** (current
  5.5.0), SLSA at **1.0** (current 1.2), and ATT&CK at **v18** (current v19.2). Even the best-
  maintained crosswalk in the field is one-to-three versions behind its sources — which is precisely
  the argument for building our own update seam rather than relying on someone else's map.
- **Crosswalks in `baseline/mappings/`** — `osps-to-800-161.yaml`, `osps-to-bpb.yaml`,
  `osps-to-bsi-tr-03185-2.yaml`, `osps-to-cra.yaml`, `osps-to-csf.yaml`, `osps-to-iso-18974.yaml`,
  `osps-to-opencre.yaml`, `osps-to-pcidss.yaml`, `osps-to-psscrm.yaml`, `osps-to-samm.yaml`.
  **These are ready-made relationship data *between vocabularies* — free interoperability**, and
  exactly the kind of thing that could land on the grid as edges.
- OSCAL JSON is generable via the in-repo `baseline-compiler`.
- Change signal: date-versioned git tags + commits touching `baseline/`.

⚠️ **Caveat to record:** `metadata.yaml` sets `draft: true`, and `OSPS-BR-03` carries an in-file
`# TODO: These ARs need to be refined or split`. Stabilising, not stable.

#### 9b. Gemara (the meta-schema underneath OSPS)
**v1.5.0, 2026-08-14** (fast cadence: v1.3.0 2026-06-13, v1.4.0 2026-07-21, v1.4.1 2026-07-23).
Apache-2.0. https://github.com/ossf/gemara — a layered meta-model for governance artifacts; OSPS
Baseline is an instance of its Layer-2 `ControlCatalog` type.
**Verdict: ALIGN** — if we model controls/evidence generically, this is the type system OpenSSF is
standardising on. Pin a version; it is moving fast.

---

### 10. OpenSSF Scorecard

| | |
|---|---|
| **Version / date** | **v5.5.0, released 2026-04-23** (VERIFIED twice: GitHub releases API, and the live `api.scorecard.dev` response self-reporting `scorecard.version: v5.5.0`). Repo last pushed 2026-08-24. ⚠️ *Correction to the brief:* this is a 2026 release, not 2025. |
| **URL** | https://github.com/ossf/scorecard · https://github.com/ossf/scorecard/blob/main/docs/checks.md · https://api.scorecard.dev/projects/github.com/<owner>/<repo> |
| **Kind** | Control/heuristic list **plus a running observation engine** with a stable JSON output schema. Uniquely, it is a *live entity-observation feed* — more useful to us than most static taxonomies. |
| **Licence** | **Apache-2.0** (VERIFIED). |
| **Verdict** | **ADOPT** the check names as a controlled finding vocabulary; **ALIGN** the entity mapping. Do **not** adopt Scorecard's flat repo→score shape as our graph shape — it has no relationships. |

Each check is an observable condition; the value to us is the **entity each one implies**:

| Check | Risk | Entity observed |
|---|---|---|
| Binary-Artifacts | High | repository → **binary file in tree** |
| Branch-Protection | High | repository → **branch** → **protection rule / ruleset** |
| CI-Tests | Low | **pull request** → **check run / status check** |
| CII-Best-Practices | Low | repository → **external badge/attestation** |
| Code-Review | High | **pull request** → **review** → **reviewer** (distinct from author) |
| Contributors | Low | repository → **contributor** → **org affiliation** |
| Dangerous-Workflow | Critical | repository → **workflow file** → **dangerous pattern** (script injection, untrusted checkout) |
| Dependency-Update-Tool | High | repository → **bot/tool config** (Dependabot, Renovate) |
| Fuzzing | Medium | repository → **fuzzing integration** |
| License | Low | repository → **licence file** |
| Maintained | High | repository → **commit/issue activity over a time window** |
| Packaging | Medium | repository → **package registry publication** |
| Pinned-Dependencies | Medium | **workflow / Dockerfile / manifest** → **dependency pin** (digest vs tag) |
| SAST | Medium | **pull request** → **SAST tool run** |
| **SBOM** | Medium | repository → **SBOM artifact** |
| Security-Policy | Medium | repository → **SECURITY.md** → contact/disclosure fields |
| Signed-Releases | High | **release** → **release artifact** → **signature / provenance attestation** |
| Token-Permissions | High | **workflow** → **GITHUB_TOKEN permission scope** (job- and top-level) |
| Vulnerabilities | High | repository → **open vulnerability** (OSV) |
| Webhooks | Critical | repository → **webhook** → **secret configured?** |

**A subtlety worth modelling:** the public dataset returns only **18** checks — **Webhooks** (needs an
admin PAT, experimental) and **SBOM** (postdates the cron dataset's check set) are absent.
*The public feed is a subset of the documented check set.*

**Update seam.** Per-repo JSON: `https://api.scorecard.dev/projects/github.com/<owner>/<repo>`
(VERIFIED live; shape `{date, repo:{name,commit}, scorecard:{version,commit}, score,
checks:[{name,score,reason,details,documentation}]}` — the `scorecard.version` field is itself the
change signal). Weekly bulk: BigQuery public dataset `openssf:scorecardcron.scorecard-v2`, latest
view `…scorecard-v2_latest`, covering the 1M most critical OSS repos; scanned list at
`cron/internal/data/projects.csv`. "What changed": GitHub releases feed + diffs to `docs/checks.md`.
The older `api.securityscorecards.dev` host is superseded by `api.scorecard.dev`.

---

### 11. OpenSSF Allstar

**v4.5, 2025-10-01** — ⚠️ *Correction to the brief:* **not archived, not sunset** (`archived: false`;
commits as recent as 2026-08-19). Apache-2.0. https://github.com/ossf/allstar
Policies (VERIFIED from `pkg/policies/`, the authoritative source): `action` (GitHub Actions
allow/deny), `admin` (Repository Administrators), `binary`, `branch`, `codeowners`, `outside`
(Outside Collaborators), `scorecard`, `security` (SECURITY.md), `workflow` (Dangerous Workflow).
Entities: **organization**, **repository**, **branch**, **collaborator** (inside vs outside),
**admin/permission level**, **GitHub Action** (allow/deny by name+version), **workflow**, **issue**
(the enforcement artifact).
**The genuinely useful part:** it encodes *config inheritance* (`baseConfig` → org → repo), *opt-in/
opt-out* (`optConfig`), and **enforcement action as a first-class four-valued vocabulary:
`log | issue | fix | block`.** That names the exact spectrum from "observed" to "prevented" — worth
stealing verbatim.
**Verdict: ALIGN.** Adopt `log/issue/fix/block` and the org→repo config-inheritance relation; prefer
Scorecard's names for the checks themselves, since Allstar's policy names largely duplicate them and
two vocabularies for one fact is a defect.

---

### 12. OpenVEX

**Spec v0.2.0**; revision history runs to **2023-07-18**; repo last pushed 2026-01-16. Tags `v0.2.0`,
`v0.0.2`. https://github.com/openvex/spec
**Licence: CC0-1.0** (VERIFIED) — public-domain dedication, the most permissive here.
Document: `@context`*, `@id`*, `author`*, `role`, `timestamp`*, `last_updated`, `version`* (integer,
increments on any content change), `tooling`, `statements`*.
Statement: `@id`, `version`, `vulnerability`*, `timestamp`, `last_updated`, `products`, `status`*,
`supplier`, `status_notes`, `justification` (required iff `not_affected`), `impact_statement`,
`action_statement`, `action_statement_timestamp`.
Product/Subcomponent: `@id`, `identifiers` (`purl`, `cpe22`, `cpe23`), `hashes`, `subcomponents`.
**Status (4):** `not_affected`, `affected`, `fixed`, `under_investigation`.
**Justification (5):** `component_not_present`, `vulnerable_code_not_present`,
`vulnerable_code_not_in_execute_path`, `vulnerable_code_cannot_be_controlled_by_adversary`,
`inline_mitigations_already_exist`. (All five in the brief confirmed verbatim.)
Relationships: `product → subcomponents` containment, and the ternary `(vulnerability, product,
status)` assertion — **a reified relationship with an author and a timestamp.** The cleanest
"claim as a first-class node" model found.
Cross-references CSAF (as an "encapsulating format") and CycloneDX VEX. **Three serialisations, one
underlying assertion — model the assertion, not the serialisation.**
Poll `https://raw.githubusercontent.com/openvex/spec/main/openvex_json_schema.json` (12.6 KB).
**Verdict: ADOPT** the status/justification enums verbatim. Private synonyms here would be pure loss.

---

### 13. Sigstore — the richest CI/CD *provenance attribute* vocabulary

Fulcio **v1.8.8 (2026-07-08)**, Rekor **v1.5.4 (2026-08-20)**, both **Apache-2.0** (VERIFIED).
`sigstore/protobuf-specs` release tag **UNVERIFIED**.
https://github.com/sigstore/fulcio/blob/main/docs/oid-info.md

**Fulcio X.509 certificate extensions, root arc `1.3.6.1.4.1.57264` (VERIFIED, full list):**

| OID | Name |
|---|---|
| `.1.1`–`.1.6` | Issuer, GitHub Workflow Trigger / SHA / Name / Repository / Ref — **all deprecated** |
| `.1.7` | OtherName SAN (username identity) |
| `.1.8` | **Issuer (V2)** |
| `.1.9` / `.1.10` | **Build Signer URI** / **Build Signer Digest** |
| `.1.11` | **Runner Environment** (platform-hosted vs self-hosted) |
| `.1.12`–`.1.15` | **Source Repository URI / Digest / Ref / Identifier** |
| `.1.16` / `.1.17` | **Source Repository Owner URI / Identifier** |
| `.1.18` / `.1.19` | **Build Config URI** / **Build Config Digest** |
| `.1.20` | **Build Trigger** |
| `.1.21` | **Run Invocation URI** |
| `.1.22` | **Source Repository Visibility At Signing** |
| `.1.23` | **Deployment Environment** *(beyond the brief's list)* |
| `.1.24` | **Token Subject** (raw OIDC `sub`) *(beyond the brief's list)* |
| `.2` | Policy OID for the Sigstore Timestamp Authority |

**Two lessons here, both directly applicable:**
1. `.1.1`–`.1.6` were the **GitHub-specific** names and are now **deprecated in favour of the generic
   `.1.8`–`.1.22` set**. That is a lived precedent for the skill's Step-5 neutrality test: *name the
   entity generically (Source Repository), not per-forge (GitHub Workflow Repository)* — the forge-
   specific naming had to be walked back.
2. The **URI + digest + stable identifier triple** repeats across six entity kinds. Mutable locator,
   immutable content hash, and durable ID are three different things and deserve three fields.

**Rekor entry types** (from `pkg/types/`): `alpine`, `cose`, `dsse`, `hashedrekord`, `helm`, `intoto`,
`jar`, `rekord`, `rfc3161`, `rpm`, `tuf`. Entities: log entry, log index, inclusion proof, signed
entry timestamp.
**Bundle/trust root protos** (`sigstore/protobuf-specs/protos/`): `sigstore_bundle`,
`sigstore_common`, `sigstore_rekor`, `sigstore_trustroot`, `sigstore_verification`, `envelope`,
`events`, `sigstore_monitor`. Poll these `.proto` files + `docs/oid-info.md`.
**Verdict: ADOPT** — the generic (non-deprecated) extension names as canonical attribute names on our
build/run/source entities.

---

### 14. TUF and gittuf

**TUF** — specification **1.0.36, last modified 2026-08-05** (VERIFIED from the spec page).
https://theupdateframework.github.io/specification/latest/
Roles: `root` (delegates trust to keys for all other roles), `targets` (may delegate),
`snapshot`, `timestamp`, optional `mirrors`, plus **delegated targets roles** (multi-level).
Relationship types: *delegates-to* (role → role, **with a threshold**), *signs* (key → metadata),
*supersedes* (version → version), *expires-at*.
**Verdict: ALIGN** — the threshold-delegation model is the right abstraction for "who may authorise
what", even though TUF itself is about update distribution.
**TUF TAPs: IGNORE** for entity naming.

**gittuf** — **v0.15.0, 2026-06-30** (prior v0.14.1 2026-05-06, v0.14.0 2026-05-01, v0.13.1
2026-03-09); still self-described **beta**. **Apache-2.0.** OpenSSF **incubating** project.
https://github.com/gittuf/gittuf · design doc `docs/design-document.md`

**This is the closest existing thing to "a git repository authority graph" and deserves close study.**
Metadata namespaces (all in-repo, platform-agnostic — "not tied to your source control platform"):
`refs/gittuf/policy`, `refs/gittuf/policy-staging`, `refs/gittuf/reference-state-log`,
`refs/gittuf/attestations`.

- **Root of trust** — declares repository-owner keys plus a numerical **threshold**; bootstrapped
  out-of-band or TOFU; rotation requires a threshold of previously-trusted root keys.
- **Rule files** — primary (typically `targets.json`) plus secondary files forming delegation chains.
- **Principals** — "fundamentally just a single signing key," but may represent a person owning
  multiple keys. **gittuf explicitly rejects git's author/committer email as unreliable and
  authenticates on signatures only.** A hard-won modelling lesson: *identity ≠ the email in the commit
  header.*
- **Protected namespaces**, three kinds: git refs (`git:refs/heads/*`, `git:refs/tags/*`), file paths
  (`file:path/*`), and arbitrary refs. Rules bind (namespace → threshold, {principals}), e.g.
  `(2, {Alice, Bob, Carol})`.
- **Permissive default** — unprotected namespaces accept any key; after explicit rules are exhausted
  an implicit allow-rule succeeds. Deny-by-exception, not deny-by-default. Worth noting explicitly.
- **RSL (Reference State Log)** — append-only, signed, hash-chained. Two entry types: **Reference
  Entry** (`ref`, `targetID`, `number`) and **Annotation Entry** (attaches messages/skip markers to
  prior entries, "since the RSL history cannot be overwritten"). Structurally: **a temporal edge
  history over ref state.**
- **Attestations** — signed in-toto attestations. Current type **reference authorization**,
  predicate `https://gittuf.dev/reference-authorization/v<VERSION>`, fields `TargetRef`,
  `FromTargetID`, `ToTargetID`. Lets multiple developers independently approve a state transition
  without touching the original commit signature — i.e. **approval is an edge, not a commit attribute.**
- CLI surface as a de-facto vocabulary: `policy {init, add-rule, update-rule, remove-rule,
  reorder-rules, list-rules, add-key, remove-key, add-person, update-person, remove-person,
  list-principals, stage, apply, discard, sign, inspect, increment-version, remote push/pull}`;
  `trust add-controller-repository` (multi-repo control).

**Verdict: ADOPT as the reference model for repository authority.** gittuf has already solved the
hardest naming problems: principal vs key, protected namespace, rule-with-threshold,
state-transition-as-signed-event, approval-as-attestation. Beta status → borrow the *vocabulary*, do
not hard-depend on the wire format.

---

### 15. OpenSSF Security Insights — an under-appreciated find

**v2.2.0, released 2026-01-31** (VERSION file confirms; repo pushed 2026-08-25 — actively maintained).
Prior: v1.0.0 (2023-10-02), v2.0.0 (2025-01-01), v2.1.0 (2025-05-09).
https://github.com/ossf/security-insights-spec · tooling https://github.com/ossf/si-tooling
**Kind:** a YAML manifest schema **authored in CUE** (`spec/schema.cue`; `docs/schema.md` is generated
— "Do not edit this file directly"). Purpose: "fill the gaps between simplified solutions such as
SECURITY.md and comprehensive automated solutions such as SBOMs."
**Licence:** GitHub reports `NOASSERTION` though a LICENSE file exists — **flag for manual review**
before reusing text (reusing the *shape* is not the concern).

Type inventory (`*` = required):
`SecurityInsights` → `header*`, `project`, `repository` ·
`Header` → `last-reviewed*`, `last-updated*`, `schema-version*`, `url*`, `comment`, `project-si-source` ·
`Project` → `administrators*[Contact]`, `name*`, `repositories*[ProjectRepository]`,
`vulnerability-reporting*`, `documentation`, `funding`, `homepage`, `roadmap`, `steward` ·
`Repository` → `accepts-automated-change-request*`, `accepts-change-request*`, `core-team*[Contact]`,
`license*`, `security*`, `status*`, `url*`, `bug-fixes-only`, `documentation`,
`no-third-party-packages`, `release` ·
`ReleaseDetails` → `automated-pipeline*`, `distribution-points*[Link]`, `attestations[Attestation]`,
`changelog`, `license` ·
**`Attestation` → `location*`, `name*`, `predicate-uri*`, `comment`** — *explicitly an in-toto
attestation reference* ·
`SecurityPosture` → `assessments*`, `champions[Contact]`, `tools[SecurityTool]` ·
`SecurityTool` → `integration*`, `name*`, `results*`, `rulesets*`, `type*`, `comment`, `version` ·
**`SecurityToolIntegration` → `adhoc*`, `ci*`, `release*`** — *where in the lifecycle the tool runs* ·
`SecurityToolResults` → `adhoc`, `ci`, `release` (each an **Attestation**) ·
`VulnerabilityReporting` → `bug-bounty-available*`, `reports-accepted*`, `bug-bounty-program`,
`comment`, `contact`, `in-scope[]`, `out-of-scope[]`, `pgp-key`, `policy` ·
`Assessment`, `Contact`, `ProjectDocumentation`, `RepositoryDocumentation`, `ProjectRepository`,
`License`, `Link`.

Relationships: *project has-many repositories* (with an explicit parent/child mechanism across
documents via `header.project-si-source` — a modelled composition edge **between files**), *repository
has release*, *release has attestations*, *posture has tools*, **tool → integration(adhoc|ci|release)
→ results(Attestation)**. That last chain is a precise, reusable model of *"a scanner ran at a
lifecycle stage and here is the signed evidence."*

Poll `spec/schema.cue` (note: **not** at repo root) and `VERSION`. Release assets include
`template-full.yml`, `template-minimum.yml`, `template-multi-repository-project*.yml` (v2.1.0).
`docs/versioning-policy.md` documents the version-change contract.
**Verdict: ADOPT** — the best *self-reported project posture* schema available, CUE-typed so genuinely
machine-checkable. Resolve the licence question before copying text.

---

### 16. S2C2F and OWASP SCVS — mine, don't poll

**S2C2F (Secure Supply Chain Consumption Framework)** — **v1.1, dated 2022-10-19** (VERIFIED from the
spec's own revision table; v1.0 2022-08-01 by Adrian Diglio/Microsoft). Repo last pushed 2025-05-26 —
**effectively static.** https://github.com/ossf/s2c2f
⚠️ *Correction to the brief:* **25 requirement IDs, not ~50** (the "50" likely conflates requirements
× maturity levels). Full list, VERIFIED by extraction:
*Ingest It* ING-1 (L1 trusted public package managers), ING-2 (L1 OSS binary repository manager),
ING-3 (L3 deny-list capability), ING-4 (L3 mirror OSS source internally) ·
*Scan It* SCA-1 (L1 known vulns), SCA-2 (L1 licences), SCA-3 (L2 end-of-life), SCA-4 (L3 malware),
SCA-5 (L3 proactive security analysis) ·
*Inventory It* INV-1 (L1 automated inventory), INV-2 (L2 OSS incident response plan) ·
*Update It* UPD-1 (L1 manual), UPD-2 (L2 automated), UPD-3 (L2 vulns in PR flow) ·
*Audit It* AUD-1 (L3 verify provenance), AUD-2 (L2 audit ingestion method), AUD-3 (L2 validate
integrity), AUD-4 (L4 validate SBOMs) ·
*Enforce It* ENF-1 (L2 secure package source files), ENF-2 (L3 curated OSS feed) ·
*Rebuild It* REB-1 (L4 trusted/reproducible rebuild), REB-2 (L4 sign rebuilt OSS), REB-3 (L4 SBOMs
for rebuilds), REB-4 (L4 sign SBOMs) ·
*Fix It + Upstream* FIX-1 (L4).
Entities implied: **OSS component**, **package manager**, **binary repository manager / internal
mirror**, **curated feed**, **deny list**, **package source config file** (`nuget.config`, `.npmrc`,
`pip.conf`, `pom.xml` — pleasingly concrete), **lock file / version pin**, **inventory**, **SBOM**,
**provenance record**, **build environment**, **upstream project**. Its core insight: **the ingestion
point is a modellable edge, not an attribute** — *how* a dependency entered matters.
Licence: GitHub reports `NOASSERTION` — **needs manual review.** No machine-readable artifact (one
56 KB markdown file). **Verdict: REFERENCE.** Mine the ingestion/rebuild concepts; do not build a poll.

**OWASP SCVS** — **v1.0, released 2020-06-25** (VERIFIED via releases API). **There is no v2.** The
standard is **static/dormant.** Licence **CC BY-SA 4.0** — note ShareAlike: reusing the *text* carries
obligations; reusing the *concepts/IDs* does not.
Six families (counts VERIFIED by fetching the source markdown): **V1 Inventory** (10) — recommends
**PURL** for normalised identity; **V2 SBOM** (18) — SBOM as a first-class artifact with unique
identifier, signature, timestamp; **V3 Build Environment** (21) — *the richest CI/CD family*:
repeatable build, CI build pipeline, build job, build script, package management settings,
DNS/network settings, certificate trust store, system audit log, build job audit log, compilers/VCS
clients/SDKs, checksums per build, unused components, authn/authz "defaults to deny" (3.10/3.11),
separation of concerns for system settings (3.12); **V4 Package Management** (19) — keeps **package
repository** and **package manager** rigorously distinct (a distinction many models blur), correlates
component version → source code in VCS (4.10), and 4.18 "package manager does not execute component
code"; **V5 Component Analysis** (12); **V6 Pedigree and Provenance** (7) — point of origin, chain of
custody, pedigree of modification, **modified variant as a distinct component** (6.5).
Relationships implied: *component contains component* (direct/transitive), *component originates-from
point-of-origin*, *modified-variant derives-from origin-component*, *package-version corresponds-to
source-commit*, *SBOM describes asset*.
**SCVS BOM Maturity Model: UNVERIFIED** — could not confirm it in the repository; not asserting a
version, URL, or content without a primary source.
**Verdict: REFERENCE.** V3 and V6 name entities nothing else names as precisely — but it is six years
old, unmaintained, copyleft on text, and has no machine-readable form. Mine it; don't cite it as live.

---

### 17. IETF SCITT and RATS — **two entity models the brief did not name, and both belong here**

#### 17a. SCITT — Supply Chain Integrity, Transparency and Trust

| | |
|---|---|
| **Version / date** | **RFC 9943, published June 2026** (VERIFIED). Standards Track. Formerly `draft-ietf-scitt-architecture`. |
| **URL** | https://datatracker.ietf.org/doc/draft-ietf-scitt-architecture/ (redirects to the RFC) |
| **Kind** | **Architecture + terminology standard** — a defined entity model with normative definitions. |
| **Licence** | IETF Trust / BCP 78 — freely reusable; RFC terminology is the definition of lingua franca. |
| **Verdict** | **ADOPT (terminology)** — this is now *the* IETF-blessed vocabulary for supply-chain transparency, and it is only two months old. |

Entity model (VERIFIED, quoting the RFC's own definitions):
- **Issuer** — "an identifier representing an organization, device, user, or entity securing
  Statements about supply chain Artifacts".
- **Artifact** — "a physical or non-physical item that is moving along a supply chain".
- **Statement** — "any serializable information about an Artifact", with a media type.
- **Signed Statement** — "an identifiable and non-repudiable Statement about an Artifact signed by an
  Issuer" (COSE_Sign1).
- **Receipt** — a COSE Single Signer Data Object proving inclusion in the verifiable data structure.
- **Transparent Statement** — a Signed Statement augmented with a Receipt.
- **Transparency Service (TS)** — "maintains and extends the VDS and endorses its state".
- **Registration Policy** — "the precondition enforced by the TS before registering a Signed Statement".
- **Append-only Log** — the entire registration history of the TS.
- **Auditor** — "checks the correctness and consistency of all Transparent Statements".
- **Relying Party** — consumes Transparent Statements, verifies proofs, inspects payload.
- **Subject** — the organization, device, user, entity, or Artifact that Statements are about.

⚠️ The brief's "Feed" concept did **not** appear in the fetched RFC terminology — it may have been
renamed or removed between draft and RFC. **UNVERIFIED; do not use "Feed" without re-checking.**

Why it matters to us: SCITT gives normative, RFC-grade names to the **Issuer / Statement / Subject /
Relying Party / Auditor** quartet that in-toto, Sigstore, and OpenVEX each name slightly differently.
If we want one word for "the party asserting a claim" and one for "the party consuming it", these are
the words with the strongest claim to being industry-standard.

**Update seam.** RFC is frozen; watch the SCITT WG datatracker page for companion documents
(architecture → COSE receipts → reference implementations). Cadence: slow, but this is fresh.

#### 17b. RATS — Remote Attestation Procedures Architecture

**RFC 9334, published January 2023** (VERIFIED). https://www.rfc-editor.org/rfc/rfc9334.html
Seven roles: **Attester**, **Verifier**, **Relying Party**, **Endorser**, **Reference Value Provider**,
**Verifier Owner**, **Relying Party Owner**.
Five conceptual messages: **Evidence**, **Endorsements**, **Reference Values**, **Attestation
Results**, **Appraisal Policies**.
Two topological patterns: **Passport Model** (Attester receives the Attestation Result and presents it
onward) and **Background-Check Model** (Attester presents Evidence to the Relying Party, which
forwards it to a Verifier).
**Verdict: ALIGN.** RATS is about device/platform attestation rather than CI/CD, but the
Evidence → Verifier → Attestation Result → Relying Party pipeline is the same shape as
provenance → policy → VSA → consumer, and the **Reference Value Provider** role names something SLSA
and in-toto leave implicit (*who says what "good" looks like*). Borrow the role names when we model
policy evaluation; do not adopt the whole architecture.

---

### 18. OCSF (Open Cybersecurity Schema Framework)

| | |
|---|---|
| **Version / date** | **v1.9.0, released 2026-08-03** (VERIFIED via GitHub releases). `main` carries `version.json = 1.10.0-dev`. Cadence ~3–4 months: 1.5.0 (2025-04-28), 1.6.0 (2025-08-01), 1.7.0 (2025-11-14), 1.8.0 (2026-03-18), 1.9.0 (2026-08-03). |
| **Governance** | **Linux Foundation project since 2024-11-19.** Steering Committee: Splunk, AWS, IBM. |
| **URL** | https://github.com/ocsf/ocsf-schema · https://schema.ocsf.io · https://ocsf.io |
| **Kind** | JSON-defined **event/telemetry schema** + global attribute dictionary + taxonomy. Not an ontology; not graph-shaped by design. |
| **Licence** | **Apache-2.0** (VERIFIED via the GitHub API `spdx_id`). |
| **Verdict** | **ALIGN strongly; do not ADOPT wholesale.** |

**Meta-model (5 constructs).** *Attributes + one global `dictionary.json`* (currently **963 attributes**,
23 data types) — the single naming authority; an attribute means the same thing everywhere.
Naming convention by suffix: `_id, _ids, _uid, _uuid, _ip, _name, _info, _detail, _time, _dt,
_process, _ver, _list`. *Objects* (**192 files**) — reusable structured types, composing by nesting
and inheriting via `extends` (`device extends endpoint`, `affected_package extends package`,
`user extends _entity`). *Event classes* (**79 with UIDs** across 88 files) — requirements
(`required`/`recommended`/`optional`) and `constraints` (`at_least_one`, `just_one`) live on the
**class-attribute pairing**, never on the attribute itself. *Categories* (8). *Profiles* (13
mix-ins: `ai_operation, cloud, container, data_classification, datetime, host, incident,
load_balancer, network_proxy, osint, record_integrity, security_control, trace`).
*Extensions* — namespaced with registered UIDs (native `linux` 1, `win` 2, `macos` 3; vendor 988–999).

UID arithmetic: `class_uid = category_uid × 1000 + ordinal`; `type_uid = class_uid × 100 + activity_id`.

**Categories:** 1 system · 2 findings · 3 iam · 4 network · 5 discovery · 6 application ·
7 remediation · 8 unmanned_systems.

**Classes that matter to us.** *Application Activity:* 6001 Web Resources Activity, 6002 Application
Lifecycle, 6003 API Activity, 6005 Datastore Activity, 6006 File Hosting Activity, 6007 Scan
Activity, 6008 Application Error. *Findings:* 2002 Vulnerability Finding, 2003 Compliance Finding,
2004 Detection Finding, 2005 Incident Finding, 2006 Data Security Finding, **2007 Application
Security Posture Finding** (added v1.5.0; attributes `application, compliance, remediation, resources,
vulnerabilities` — the closest OCSF gets to "a scanner reported something about our software"), 2008
IAM Analysis Finding. *IAM:* 3002 Authentication, 3003 Authorize Session, 3004 Entity Management,
3006 Group Management, **3007 User Management** and **3008 Role Management** (new in 1.9.0 — note
3001 Account Change and 3005 User Access Management were **deprecated in 1.9.0**). *Discovery:* 5001
Device Inventory, 5002 Device Config State, 5003 User Inventory, 5004 OS Patch State, **5010 Job
Query**, **5020 Software Inventory Info**, 5023 Cloud Resources Inventory. *System:* **1006 Scheduled
Job**, 1007 Process, 1009 Script.

#### The question the brief asked: does OCSF have CI/CD, appsec, SBOM or software-inventory classes?

**SBOM yes. CI/CD no — and nothing proposed.** (VERIFIED by grepping a full clone and by issue/PR
search.) Searches for `ci/cd`, `cicd`, `devops`, `build`, `commit`, `artifact`, `repository`
(source-code sense) returned **zero hits**; the only `pipeline` hits are the *logging* pipeline.
There is no pipeline, job run, workflow, runner, branch, pull request, commit, deployment, or
registry concept anywhere. Issue/PR search on `ocsf/ocsf-schema` for `cicd`, `CI/CD`, `supply chain`,
`pipeline`, `build` in titles returned **`total_count = 0` on every query**. The extension registry
contains no CI/CD, DevOps, or supply-chain extension.

What it *does* have: **`sbom` object** and **`software_component` object**, added **v1.4.0
(2025-01-31)**. `sbom = {created_time, package, product, software_components, type, type_id, uid,
version}` with `type_id ∈ {SPDX, CycloneDX, SWID}`. `software_component = {author, hash, license,
name, purl, related_component, relationship, relationship_id, type, type_id, version}`.
`sbom` hangs off 5020 Software Inventory Info and off the `application` object; `package` in 5020 was
**deprecated in favour of `sbom`**.
⚠️ **Name-collision warning:** OCSF's **`attestation` object** (v1.9.0) is a *tamper-evident event
chain* (`fingerprint`, `signatures`, `prev_event`, `chain_uid`, `authority_uid`) for the
`record_integrity` profile. It is **not** in-toto/SLSA provenance. Do not let the two meet in one
namespace without a qualifier.

**This is a genuinely valuable negative result: the pipeline half of our graph is unclaimed naming
territory in the single largest security schema.**

#### The graph story — better than expected, but uncontrolled

- **`graph` / `node` / `edge` objects added v1.5.0 (2025-04-28)**, citing the JSON Graph
  Specification. `graph = {name, uid, desc, nodes (required), edges, is_directed, type,
  query_language_id}` — and **`query_language_id` enumerates Cypher, GraphQL, Gremlin, GQL, G-CORE,
  PGQL, SPARQL**. `edge = {uid, name, source (required), target (required), relation, is_directed,
  data}`. `node = {uid (required), name, type, desc, data}`.
- `resource_details.resource_relationship` (type `graph`); `finding_info.attack_graph` (v1.6.0).
- `software_component.relationship_id` — a thin enum: `0 Unknown`, `1 Depends On` ("both direct and
  transitive"), `99 Other`, with `related_component` holding the other end's **purl**.
- `vulnerability.dependency_chain` — a **string**, e.g. `serverless-offline -> @serverless/utils ->
  memoizee -> es5-ext`. A path, unhelpfully unstructured.
- **`edge.relation` is a free string** ("is-attached-to, depends-on"). OCSF gives you a graph
  *container* with **no controlled edge vocabulary**. That gap is precisely what git-serious fills.

#### `observable.type_id` — OCSF's entity-type dictionary (30 core values)
`1 Hostname · 2 IP Address · 3 MAC Address · 4 User Name · 5 Email Address · 6 URL String ·
7 File Name · 8 Hash · 9 Process Name · 10 Resource UID · 11 Port · 12 Subnet · 13 Command Line ·
14 Country · 15 Process ID · 16 HTTP User-Agent · 19 User Credential ID · 20 Endpoint · 21 User ·
22 Email · 23 URL · 24 File · 25 Process · 26 Geo Location · 27 Container · 30 Fingerprint ·
36 Script Content · 37 Serial Number · 42 Message UID · 45 File Path`; Windows extension adds
28 Registry Key, 29 Registry Value; 1.9.0 added 49/50 `iam_role.name`/`.uid`.
**Note what is absent: no repository, no commit, no build, no package/purl observable.** `Container`
is the only CI/CD-adjacent entity type.

#### Key objects (attribute highlights)
`actor {user, process, session, invoked_by, app_name, app_uid, application, authorizations, iam_role,
idp}` · `api {operation, request, response, service, group, token, version}` ·
`user {uid, uid_alt, name, type_id, account, credential_uid, domain, email_addr, full_name, groups,
has_mfa, ldap_person, org, programmatic_credentials, risk_level_id, risk_score}` ·
`group {uid, uid_alt, name, desc, domain, privileges, type}` ·
`policy {uid, name, desc, group, data, is_applied, type, version}` ·
`resource_details {name, uid, type, owner, group, namespace, region, zone, provider,
cloud_partition, criticality_id, resource_relationship, role_id, version, labels, tags, data}` ·
**`affected_code {file, owner, rule, remediation, start_line, end_line, start_column, end_column}`**
— *the only place OCSF names source-code position* ·
`affected_package (extends package) + {fixed_in_version, path, remediation}` ·
`package {name, version, purl, cpe_name, hash, architecture, epoch, license, license_url,
package_manager, package_manager_url, release, src_url, type_id, uid, vendor_name}` ·
`digital_signature {algorithm_id, certificate, created_time, developer_uid, digest,
serialization_id, state_id}` ·
`container {uid, name, hash, image, labels, network_driver, orchestrator, pod_uuid, runtime, size,
tag}` and `image {uid, name, path, tag, labels}` ·
`cvss {base_score, overall_score, severity, vector_string, version, metrics, depth, src_url}` ·
`agent {uid, uid_alt, name, type_id, policies, vendor_name, version}` — *security sensors, not AI
agents* (1.9.0 added a separate `ai_agent`) ·
`analytic {uid, name, algorithm, category, desc, related_analytics, sensor_info_list, state_id,
type_id, version}` ·
`evidences {actor, ai_agent, api, connection_info, container, data, database, databucket, device,
dst_endpoint, email, file, http_request, http_response, job, process, query, resources, script,
src_endpoint, tls, url, user, verdict_id}` ·
`finding_info {uid, uid_alt, title, desc, analytic, attack_graph, attacks, created_time,
data_sources, first_seen_time, kill_chain, product, related_analytics, related_events,
related_events_count, src_url, tags, traits, types}` ·
**`job {uid, name, cmd_line, desc, file, job_actions, job_triggers, run_state_id, type_id, user,
created_time, last_run_time, next_run_time}`** with `job_action {cmd_line, com_class_uuid, file,
properties, type_id, working_directory}` and `job_trigger {event_codes, log_sources, last_run_time,
next_run_time, properties, type_id, user}` (both new in 1.9.0) — the closest structural analogue to a
CI job, **but it means OS scheduled tasks, not pipeline runs**.

**Update seam.** Files: `categories.json`, `dictionary.json`, `objects/*.json`,
`events/<category>/*.json`, `profiles/*.json`, `extensions/`, plus a `metaschema/` (14 JSON Schemas
that validate the schema definitions themselves). **Live JSON API (VERIFIED 200):**
`https://schema.ocsf.io/api/versions`, `/api/classes`, `/api/objects`, `/api/objects/<name>`,
`/api/dictionary`, `/api/profiles`, `/api/extensions`, and versioned `/api/1.9.0/...`.
**"What changed":** `CHANGELOG.md` is Keep-a-Changelog with sections for Categories / Event Classes /
Profiles / Objects / Observables / Platform Extensions / Dictionary Attributes plus **Deprecated** and
**Breaking changes**, every entry PR-linked; GitHub Releases mirror it; and
**`ocsf/ocsf-validate-compatibility` diffs two versions programmatically** — the best automated
"what changed" tooling of any source here.

**Why ALIGN and not ADOPT:** OCSF is the right vocabulary for the *observation* half (findings, IAM
events, actors, packages, containers, vulnerabilities), Apache-2.0, with a real API and disciplined
changelog. But the unit is an **event, not a node**, and its 1.8/1.9 momentum is AI and IAM, not
supply chain. Align by emitting our findings as 2007/2002/2003, using `package`/`purl`/`container`/
`image`/`user`/`group`/`policy` spellings verbatim, and exporting graphs through `graph`/`node`/`edge`.
Define the pipeline nouns ourselves — and if they mature, **a registered OCSF extension UID is the
sanctioned path to contribute them back.**

---

### 19. OWASP Top 10 CI/CD Security Risks — the entity extraction

| | |
|---|---|
| **Version / date** | **v1.0, initial release September 2022**; "project promotion, additional reviews: October 2022". ⚠️ **No revision exists** — the brief's "published 2023" is off, and there is no 2024/2025/2026 edition. Content repo `cider-security-research/top-10-cicd-security-risks` **last pushed 2023-01-18**; the OWASP mirror has had only metadata commits since. **Treat as frozen, not maintained.** |
| **URL** | https://owasp.org/www-project-top-10-ci-cd-security-risks/ · https://github.com/cider-security-research/top-10-cicd-security-risks |
| **Kind** | Risk taxonomy with stable IDs. Prose; **no schema, no machine-readable artifact** (ten markdown files + a PDF). Change signal = commits, of which there are none. |
| **Licence** | `project.owasp.yaml` declares **Apache-2.0 AND CC-BY-SA-4.0**; the repo LICENSE is CC-BY-SA-4.0. |
| **Verdict** | **ADOPT the risk IDs; MINE the entity list.** CICD-SEC-1..10 are the only stable, citable, CI/CD-native risk labels in existence. |

**Entities implied by each risk** — this extraction is the deliverable:

- **CICD-SEC-1 Insufficient Flow Control Mechanisms** — SCM, repository, **branch**, **branch
  protection rule** (including its *exclusions* for users/branches), **pull request**, **required
  review/approval**, **auto-merge rule**, CI service account, pipeline, **deployment pipeline**,
  artifact, **artifact repository**, package, container, production environment, IaC resource, and
  **drift** between prod and its CI/CD origin.
- **CICD-SEC-2 Inadequate Identity and Access Management** — human account, **programmatic account**,
  service account, IdP/federation, **local identity**, **external identity** (non-owned email domain;
  external collaborator), **self-registered identity**, **shared identity**, **stale identity**,
  permission grant (**granted vs actually used**), and the access methods: username+password,
  **personal access token**, **marketplace application**, **OAuth application**, **plugin**, **SSH key**.
- **CICD-SEC-3 Dependency Chain Abuse** — package, **package version / version lock**, **package
  manager client**, **public registry**, **internal registry / proxy**, **scope / namespace**,
  **pre-install script**, checksum, signature, **package-manager config file** (`.npmrc`), maintainer
  account. Sub-types named: *dependency confusion, dependency hijacking, typosquatting, brandjacking*.
- **CICD-SEC-4 Poisoned Pipeline Execution (PPE)** — **CI configuration file** (in-repo vs
  protected-branch vs separate-repo vs CI-defined), **trigger** (`push`, `pull_request`), fork,
  **build node / runner**, **referenced file** (Makefile, script, **test file**, **linter/scanner
  config**), pipeline identity. Three named variants: **D-PPE** (direct), **I-PPE** (indirect),
  **3PE / Public-PPE** (anonymous contributor).
- **CICD-SEC-5 Insufficient PBAC (Pipeline-Based Access Controls)** — **pipeline**, **pipeline
  step/stage**, **execution node** (shared vs dedicated), **controller node**, secret, **environment
  variable**, vault, cloud metadata service, **OS user on the node**, network **ingress/egress
  filter**, node **pristine-state reset**, patch level.
- **CICD-SEC-6 Insufficient Credential Hygiene** — credential/secret, **commit history**, **container
  image layer**, **console output / build log**, log management system, **deploy key**, static vs
  **temporary credential**, rotation age, **conditional scoping** (source IP, identity), secret
  scanner (IDE plugin, push-time, historical).
- **CICD-SEC-7 Insecure System Configuration** — **system instance** (self-managed vs SaaS: SCM, CI,
  artifact repository), **version**, **security patch**, **system owner**, network ACL, **security
  configuration setting**, default credential, **debug permission on execution node**.
- **CICD-SEC-8 Ungoverned Usage of 3rd Party Services** — **third-party app** and its five
  integration methods (**GitHub App**, **OAuth app**, **access token**, **SSH key**, **webhook**),
  **marketplace plugin** (GitHub Action, CircleCI Orb), permission granted vs used,
  **approval/vetting record**.
- **CICD-SEC-9 Improper Artifact Integrity Validation** — artifact, **signed commit**, **signing key
  per contributor**, **signing authority**, **verification step**, hash/checksum vs published hash,
  **IaC template**, config drift. Names in-toto, SLSA and Sigstore as the tooling.
- **CICD-SEC-10 Insufficient Logging and Visibility** — the system inventory itself (**SCM, CI,
  artifact repository, package management software, container registry, CD, orchestration engine**);
  **audit log** vs **applicative log** (push event, build execution, artifact upload); SIEM;
  alert/anomaly rule.

**Discount for age:** it predates GitHub Actions OIDC, reusable workflows, and modern provenance. But
the nouns hold, and nothing has replaced them.

---

### 20. OWASP adjacent

**OWASP Top 10:2025 — this landed, and it changes the answer.** https://owasp.org/Top10/2025/
(content committed 2025-10-28 → 2025-12-13; **exact release day UNVERIFIED**, no GitHub releases).
It promotes supply chain to **A03:2025 Software Supply Chain Failures** — top-ranked in the community
survey at exactly 50% of first-place votes. Full list: A01 Broken Access Control · A02 Security
Misconfiguration · **A03 Software Supply Chain Failures** · A04 Cryptographic Failures · A05
Injection · A06 Insecure Design · A07 Authentication Failures · A08 Software **or** Data Integrity
Failures · A09 Security Logging & Alerting Failures · A10 Mishandling of Exceptional Conditions.
A03 names the change-management surface **verbatim**: *"CI/CD settings (all build tools and
pipelines), code repositories, sandbox areas, developer IDEs, SBOM tooling and created artifacts,
logging systems and logs, third party integrations, artifact repositories, container registries"* —
plus transitive dependencies, signed packages, provenance, staged rollout/canary. Licence CC BY-SA 4.0
(the site footer inconsistently says CC BY 3.0).
**Verdict: ALIGN.** This is now the most authoritative *current* statement of the CI/CD supply-chain
noun set, and it corroborates the CICD-SEC extraction almost item-for-item. **When we need one
citation that a reviewer will already know, this is it.**

**OWASP ASVS v5.0.0, 2025-05-30.** 17 chapters, 345 requirements. Measured: **"pipeline" appears 0
times, "CI/CD" 0 times.** Relevant: 15.1.2 (SBOM, trusted repositories), 15.2.4 (transitive deps,
dependency confusion), 13.3.1 (no secrets in source or build artifacts). Ships JSON / flat-JSON / CSV
/ XML **and CycloneDX** under `5.0/docs_en/`. CC BY-SA 4.0.
**Verdict: REFERENCE** — excellent machine-readable control corpus, near-zero CI/CD vocabulary.

**OWASP DevSecOps Guideline** (restructured 2026-07-11; version number UNVERIFIED, no release tags).
Its value is a **seven-stage spine — Design → Develop → Build → Test → Release → Deploy → Operate** —
plus a scanner-type list (secret scanning, SAST, DAST, SCA, IaC, container, IAST, API).
**Verdict: ALIGN (cheap)** — adopt as our `stage` and `check_type` enumerations.

**OWASP Top 10 Risks for Open Source Software — v0.1, 2024-02-29, Incubator, untouched since.**
OSS-RISK-1 Known Vulnerabilities · 2 Compromise of Legitimate Package · 3 Name Confusion Attacks ·
4 Unmaintained Software · 5 Outdated Software · 6 Untracked Dependencies · 7 License Risk ·
8 Immature Software · 9 Unapproved Change · 10 Under/over-sized Dependency. Uniquely treats
**maintainer** and **license** as first-class *risk-bearing entities*, and models an explicit
root-project → direct → transitive dependency graph. **Verdict: ALIGN, caveat v0.1.**

**OWASP CI/CD Goat — v1.2.7, 2024-07-14**, still at `cider-security-research/cicd-goat`, **not in the
OWASP org**. Apache-2.0. Its `docker-compose.yaml` instantiates the graph concretely (Jenkins server
+ agent, Gitea, GitLab + runner, CTFd, LocalStack, DinD, prod). The challenge manifest is a **CTFd
SQLite DB**; the CICD-SEC mapping lives only as a badge line in each `solutions/*.md`
(White Rabbit / Caterpillar / Mad Hatter / Cheshire Cat → SEC-4; Duchess → SEC-6;
Twiddledum / Gryphon → SEC-3; Dodo / Mock Turtle → SEC-1; Hearts → SEC-2; Dormouse → SEC-8).
**Verdict: REFERENCE** — not a vocabulary, but **a genuine labelled test corpus with known-bad edges**
to validate our model against. Worth flagging to the adversarial/incident research direction.

---

### 21. SARIF — **the best structural match in the whole survey**

| | |
|---|---|
| **Version / date** | **2.1.0 Plus Errata 01 — OASIS Standard incorporating Approved Errata, 2023-08-28.** **2.2 is in progress**: prerelease tag `sarif-v2.2-wd20250807-dev` (2025-08-07), repo last pushed 2026-07-19 — active, not yet a Committee Specification. |
| **URL** | https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html · https://github.com/oasis-tcs/sarif-spec |
| **Kind** | JSON Schema (draft 2020-12, **54 definitions**) — and genuinely an entity model for analysis results. |
| **Licence** | OASIS IPR Policy, **RF on RAND Terms Mode** (`LICENSE.md`). Schema freely usable. ⚠️ **Not an SPDX-clean OSS licence** — `gh api` reports `NOASSERTION`. Flag before vendoring text. |
| **Verdict** | **ADOPT.** |

**All 54 entity types:** `address, artifact, artifactChange, artifactContent, artifactLocation,
attachment, codeFlow, configurationOverride, conversion, **edge**, **edgeTraversal**, exception,
externalProperties, externalPropertyFileReference(s), fix, **graph**, **graphTraversal**, guid,
**invocation**, language, location, **locationRelationship**, logicalLocation, message,
multiformatMessageString, **node**, notification, physicalLocation, propertyBag, rectangle, region,
replacement, reportingConfiguration, reportingDescriptor, reportingDescriptorReference,
**reportingDescriptorRelationship**, result, resultProvenance, run, runAutomationDetails,
specialLocations, stack, stackFrame, suppression, threadFlow, threadFlowLocation, tool, toolComponent,
toolComponentReference, translationMetadata, **versionControlDetails**, webRequest, webResponse`.

**SARIF has a real graph.** `graph = {description, nodes, edges}`; `node = {id (req), label, location,
children}`; `edge = {id (req), sourceNodeId (req), targetNodeId (req), label}`; plus `graphTraversal`
and `edgeTraversal`. `graphs` appear on both `run` and `result`.

**Relationship vocabularies — the load-bearing bit:**
- `locationRelationship.kinds` — well-known: **`includes`, `isIncludedBy`, `relevant`**
  (default `["relevant"]`).
- `reportingDescriptorRelationship.kinds` — well-known: **`canPrecede`, `canFollow`, `willPrecede`,
  `willFollow`, `superset`, `subset`, `equal`, `disjoint`, `relevant`, `incomparable`**. This is a
  proper **relation algebra** for rule-to-rule and rule-to-taxonomy links — **the richest typed-edge
  vocabulary found anywhere in this survey**, and the only one that distinguishes *can* from *will*.
- Both are **open arrays of strings**, so private kinds extend cleanly. A model to copy.

**CI entities, named directly:**
- **`versionControlDetails = {repositoryUri (required), revisionId, branch, revisionTag, asOfTimeUtc,
  mappedTo}`**, carried on `run.versionControlProvenance[]`. *Repository + revision + branch as a
  first-class object.*
- **`invocation = {commandLine, arguments, responseFiles, startTimeUtc, endTimeUtc, exitCode,
  exitCodeDescription, exitSignalName/Number, executionSuccessful (required), machine, account,
  processId, executableLocation, workingDirectory, environmentVariables, stdin/stdout/stderr/
  stdoutStderr, ruleConfigurationOverrides, toolExecutionNotifications}`** — *a build/scan run node in
  all but name.*
- **`resultProvenance = {firstDetectionTimeUtc, lastDetectionTimeUtc, firstDetectionRunGuid,
  lastDetectionRunGuid, invocationIndex, conversionSources}`** — run-to-run finding lineage.
- `artifact.roles` (24 values): `analysisTarget, attachment, responseFile, resultFile, scannedFile,
  standardStream, tracedFile, unmodified, modified, added, deleted, renamed, uncontrolled, driver,
  extension, translation, taxonomy, policy, referencedOnCommandLine, memoryContents, directory,
  userSpecifiedConfiguration, toolSpecifiedConfiguration, debugOutputFile`.
- `result.baselineState ∈ {new, unchanged, updated, absent}` — **finding lifecycle across runs**;
  `result.kind ∈ {notApplicable, pass, fail, review, open, informational}`;
  `level ∈ {none, note, warning, error}`; `suppression.kind ∈ {inSource, external}`,
  `status ∈ {accepted, underReview, rejected}`.
- `toolComponent = {name (req), guid, version, semanticVersion, organization, product, productSuite,
  releaseDateUtc, downloadUri, informationUri, rules, taxa, supportedTaxonomies,
  associatedComponent}` — driver/extension/plugin identity.
- `logicalLocation.kind`: `function, member, module, namespace, parameter, resource, returnType, type,
  variable, object, array, property, value, element, text, attribute, comment, declaration, dtd,
  processingInstruction`.

**Update seam.** `https://raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.2/schema/sarif.json`
(+ the external-property-file schema). Change signal: git history on `sarif-2.2/schema/`, the single
prerelease tag, `sarif-2.2/comment-resolution/`, `meeting_minutes/`, and `Future.md`.

**Why ADOPT:** SARIF already models *tool → invocation → run → result → location → artifact →
repository@revision@branch*, has a typed-relationship vocabulary, and ships a `graph`/`node`/`edge`
trio. **Every scanner in a CI pipeline already emits it.** Adopt `versionControlDetails` and
`invocation` field names verbatim, seed our relation algebra from
`reportingDescriptorRelationship.kinds`, and ingest SARIF as a native input format.

---

### 22. The identity / finding family

**OSV Schema — v1.9.0, 2026-08-06.** https://github.com/ossf/osv-schema · Apache-2.0.
One `Vulnerability` root. **Its relationship model is the best-specified in the survey because it
documents edge *algebra*:** `aliases` (symmetric **and** transitive), `upstream` (transitive,
**not** symmetric — added v1.7.0, 2025-03-05), `related` (symmetric, **not** transitive). Nothing
else here states its edge properties formally, and it costs nothing to copy the practice.
Enums: `ranges[].type ∈ {GIT, SEMVER, ECOSYSTEM}`; `references[].type ∈ {ADVISORY, ARTICLE,
DETECTION, DISCUSSION, REPORT, FIX, INTRODUCED, GIT, PACKAGE, EVIDENCE, WEB}`;
`credits[].type ∈ {FINDER, REPORTER, ANALYST, COORDINATOR, REMEDIATION_DEVELOPER,
REMEDIATION_REVIEWER, REMEDIATION_VERIFIER, TOOL, SPONSOR, OTHER}`;
`severity[].source ∈ {NVD, CNA, SELF}` (v1.8.0).
**51 ecosystems — and `GitHub Actions` is a first-class ecosystem**, meaning OSV already treats CI
workflow actions as identifiable packages. `ranges[].type = "GIT"` carries `repo` (clone URL) with
**commit hashes** as `introduced`/`fixed` events — a genuine vulnerability → (repo, commit) edge.
Poll `validation/schema.json` + `ecosystems.json`; signal in `CHANGELOG.md` + releases.
**Verdict: ADOPT.**

**CSAF — 2.0 OASIS Standard 2022-11-18 (+ Errata 01, 2024-02-12); 2.1 is CSD02, 2026-02-25** (not yet
CS or OS — **still mutable**).
The relationship deliverable: `product_tree.relationships[]` in 2.0 = `{category, full_product_name,
product_reference, relates_to_product_reference}` — a directed, categorised binary edge that
**mints a new product node**. **2.1 removes `relationships` entirely** and replaces it with
`product_paths[]` = `{beginning_product_reference, full_product_name, subpaths[]{category,
next_product_reference}}` — a binary edge generalised into an ordered N-hop path.
**The five category labels survive byte-identically across both versions:** `default_component_of`,
`external_component_of`, `installed_on`, `installed_with`, `optional_component_of`.
Also breaking in 2.1: branch category `legacy` removed, `platform` added; `scores`→`metrics`;
`cwe`→`cwes`; `product_status` gains `unknown`.
`product_identification_helper = {cpe, purl, hashes, model_numbers, sbom_urls, serial_numbers, skus,
x_generic_uris}` — **a reusable identifier-bag pattern** (cf. SPDX `ExternalIdentifierType`,
CycloneDX `componentEvidence.identity.field`).
OASIS **Non-Assertion Mode**.
**Verdict: ADOPT the five labels; ALIGN on the 2.1 structure but do not pin to it yet.**

**CVE Record Format — v5.2.0, 2025-10-29.** **CC0 1.0** — the most permissive licence in the survey.
`affected[]` properties: `vendor, product, collectionURL, packageName, **packageURL** (new in 5.2.0),
cpes, modules, platforms, **repo**, **programFiles**, **programRoutines**, defaultStatus,
versions[]{version, status, versionType, lessThan, lessThanOrEqual, limit, changes[]}`.
**It is the only standard here that names source files and functions as entities.**
`taxonomyMappings[].taxonomyRelations[]{taxonomyId, relationshipName, relationshipValue}` is an open
reified-triple escape hatch **with no controlled predicate list** — a cautionary example, not a model.
**Verdict: ADOPT the code-level names (`repo`, `programFiles`, `programRoutines`, `modules`);
IGNORE `taxonomyRelations` as vocabulary.**

**PURL — ECMA-427 confirmed independently by this cluster too.** Repo releases v1.0.1 (2026-08-03).
**42 registered types** in `purl-types-index.json`, including **`git`, `github`, `bitbucket`,
`docker`, `oci`, `bazel`, `swid`, `vscode-extension`** — repository, container and build-system
identity are *already registered types*. Repo is **MIT**; the ECMA standard *text* carries a separate
ECMA copyright licence.
**Verdict: ADOPT unconditionally as the canonical node key** — it is what OCSF (`purl`), CSAF
(`product_identification_helper.purl`), OSV (`package.purl`), SPDX (`packageUrl`), CycloneDX (`purl`)
and now CVE (`packageURL`) all point at. **This is the single strongest cross-standard convergence in
the entire survey.**

**OmniBOR — spec v0.2, status Draft**, repo HEAD 2025-11-17, Community Specification License 1.0.
https://github.com/omnibor/spec
Names *Artifact*, *Artifact Identifier* (Reproducible / Unique / Immutable), *GitOID*
(`gitoid:blob:sha256`), *Input Manifest*, and the *Artifact Dependency Graph* — but **the ADG has no
normative definition clause in v0.2** and there is exactly **one untyped edge** (artifact → build
input). No JSON schema, no releases.
**Conceptually the closest fit to git-serious of anything found; practically not yet adoptable.**
**Verdict: REFERENCE, and watch closely** — take the gitoid if we need content-addressed artifact
identity.

**EPSS** — model `v2026.06.15`, observed live 2026-08-27. The authoritative version signal is
**line 1 of the CSV** (`#model_version:…,score_date:…`). One tuple `{cve, epss, percentile, date}`,
no relationships; licence terms **UNVERIFIED**. **REFERENCE** — a time-varying *property* on a CVE
node, not an entity.

**SSVC — v2026.7.0, 2026-07-20** (registry `schemaVersion 2.0.0`). 105 decision points across
namespaces `basic, cisa, cvss, nist#800-30, ssvc, x_com.yahooinc#…`.
⚠️ **Split licence: the JSON under `data/` is MIT-SEI; the surrounding prose is CC BY-NC 4.0.**
Its content is triage semantics, not CI/CD entities — but **two patterns are worth copying**:
(a) a `namespace#key@version` object registry with **`x_`-prefixed private namespaces**, and
(b) **per-concept versioning with old versions retained**.
**Verdict: ALIGN on the patterns, not the content.**

**CPE 2.3 / NIST IR 7695** — frozen for 15 years, hardware/OS-oriented, no relationships. **REFERENCE
only** (carry it in an identifier bag, as CSAF does).
**SWID / ISO 19770-2** — edition, date and element inventory **UNVERIFIED** (iso.org returned 403);
paywalled, therefore **IGNORE** for adoption, reachable only via the `swid` purl type.

---

### 23. NIST SP 800-204D — **the citable authority for a CI/CD entity model**

| | |
|---|---|
| **Version / date** | *Strategies for the Integration of Software Supply Chain Security in DevSecOps CI/CD Pipelines*, **NIST SP 800-204D, February 2024** (final; ERB-approved 2024-01-31; draft 2023-08-30). DOI 10.6028/NIST.SP.800-204D. Authors: Chandramouli (NIST), Kautz (TestifySec), **Torres-Arias (Purdue — the in-toto lead)**. |
| **URL** | https://csrc.nist.gov/pubs/sp/800/204/d/final · https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204D.pdf |
| **Kind** | Prose reference model + requirement list. Not a schema — but **the closest thing the US government has published to a CI/CD entity/actor ontology**. |
| **Licence** | US Government work — "not subject to copyright in the United States." Fully reusable. |
| **Verdict** | **ADOPT.** |

Its own keyword list is effectively its entity dictionary: *actor; artifact; attestation; CI/CD
pipeline; package; provenance; repository; SBOM; SDLC; SLSA; software supply chain.*

**The three primitives (§2.4).** An SSC is "a collection of steps that create, transform, and assess"
artifacts. **step** (an SSC activity, e.g. build) · **actor** — explicitly *"can also be a non-human,
such as a build orchestrator"* · **artifact**. Figure 1 is an interaction diagram of exactly these
three.

**The relationship triple, quoted verbatim** — and it is the cleanest sentence in this whole survey:
> "a build step **uses** a series of artifacts as tools (e.g., a compiler and a linker) and
> **consumes** artifacts (i.e., source code) to **produce** a new artifact (i.e., the compiled binary)."

Relationship verbs named: **uses** (a step uses artifacts as *tools*), **consumes** (a step consumes
artifacts as *inputs*), **produces**, **is stored in** (artifact → repository), *is associated with an
owner*, *attests to*, *depends on*.
The **uses vs consumes** distinction is exactly SLSA's `resolvedDependencies` vs `externalParameters`
split, arrived at independently — a genuine convergence.

**Table 1, "Top-level entities in the trust chain of typical CI/CD pipelines"** — an artifact ↔
repository pairing: first-party code → SCM; third-party code → artifact managers; **builds** → build
repository; **packages** → package repository. Footnote 3 adds sub-entities: *"sub-elements,
components, workers, attestors, and other mechanisms."*

**Attestation entities (§5.1.1) — four kinds:** **Environment attestation**, **Process attestation**,
**Materials attestation**, **Artifacts attestation** — plus **policy** ("a signed document that encodes
the requirements for an artifact to be validated"), **functionary**, **verifier** (in-toto's
vocabulary, blessed by NIST).

**Risk-factor entities (§3.1):** developer environment, threat actors, attack vectors, and **attack
targets (assets)** = source code, credentials, sensitive data, internal operations, build systems.
**Threats (§3.1.5):** injection of vulnerable/malicious dependencies; stolen credentials; injection of
malicious code into repositories; **secret theft via merge requests**; fork → pull-request poisoning.

**Requirement ID scheme (usable as-is):** `PULL-PUSH_REQ-1..4`, `COMMIT-REQ-1..2`, `DEPLOY-REQ-1..5`,
`GitOps-REQ-1..4`. Appendix A crosswalks each to SSDF practices; Appendix B documents **deliberate
omissions** (a practice worth copying in our own corpus).

**Siblings:** SP 800-204 (2019-08-07), 204A (2020-05-27), 204B (2021-08-06), **204C** (2022-03-08 —
names the five pipeline stages **build, test, package, deploy, operate** and the five code types:
application code, infrastructure as code, policy as code, configuration code). No 800-204E exists.

**Update seam.** **None machine-readable.** Poll the CSRC publication page for "potential updates" and
document history. Cadence: the 800-204 series has issued roughly one document a year.

---

### 24. NIST SSDF — SP 800-218 and SP 800-218A

**SP 800-218 v1.1, February 2022.** DOI 10.6028/NIST.SP.800-218. Supersedes CSWP 13.
https://csrc.nist.gov/pubs/sp/800/218/final · Public domain.
Four groups, ID scheme `GROUP.practice.task`: **PO** Prepare the Organization · **PS** Protect the
Software · **PW** Produce Well-Secured Software · **RV** Respond to Vulnerabilities.
Pipeline-relevant practices: **PO.3 Implement Supporting Toolchains**, PO.4 Define and Use Criteria
for Software Security Checks, **PO.5 Implement and Maintain Secure Environments for Software
Development**, **PS.1 Protect All Forms of Code from Unauthorized Access and Tampering**, **PS.2
Provide a Mechanism for Verifying Software Release Integrity**, **PS.3 Archive and Protect Each
Software Release**, PW.4 Reuse Existing Well-Secured Software, **PW.6 Configure the Compilation,
Interpreter, and Build Processes**, PW.7 Review/Analyze Human-Readable Code, PW.8 Test Executable Code.
Entities named: toolchain, **development endpoints**, **environments**, forms of code (source,
executable, **configuration-as-code**), software release, **release integrity verification
information**, archive, **provenance data** (PS.3.2), repositories of modules, compiler/interpreter/
build tools, code review, third-party components, artifacts of toolchain operation.

**One instruction from PO.5 is directly on-point for us and worth quoting:**
> "the names of environments, like 'development,' 'build,' 'staging,' 'integration,' 'test,'
> 'production,' and 'distribution' … vary widely. **Enumerating your environments is necessary in
> order to secure them properly.**"

That is NIST telling you the environment is a node, and that its *name* is site-specific — i.e. model
the type, let the instance name vary.

**Rev. 2 status (VERIFIED):** **no SP 800-218 Rev. 2 exists or is announced.** The SSDF project page
(updated 2026-04-13) lists only 218, 218A and the superseded CSWP 13, and describes future work as
**interactive repositories and Community Profiles, not a revision.** That is NIST's stated evolution
path — so watch for *profiles*, not a Rev 2.

**Update seam.** The **SSDF 1.1 table as Excel (.xlsx)** on the CSRC page, plus delta / "potential
updates" spreadsheets — that is the "what changed" signal, and it is genuinely machine-readable.
NIST already publishes the crosswalk to BSAFSS, BSIMM, IEC 62443-4-1, ISO 27034, OWASP SAMM/SCVS,
PCI SSLC and SP 800-53 in that same table. **Don't rebuild it.**

**SP 800-218A, 2024-07-26** — *…for Generative AI and Dual-Use Foundation Models: An SSDF Community
Profile*. ⚠️ **Correction to a common claim: it DOES add new task IDs**, each labelled "[Not part of
SSDF 1.1]" — `PO.5.3`, `PS.1.2` (protect all training/testing/fine-tuning data), `PS.1.3` (protect all
model weights), and a wholly new practice **PW.3 "Confirm the Integrity of Training, Testing, … Data"**
(`PW.3.1`–`PW.3.3`). New nouns: AI model, model weights, training/testing/fine-tuning/aligning data,
pipelines, reward models, adversarial samples. New actor roles: **AI model producer, AI system
producer, AI system acquirer**. Adds a **Priority** field (High/Medium/Low) per task.
**Verdict: ALIGN** for 800-218 (use PO/PS/PW/RV IDs as compliance-claim labels on nodes; do not
restructure the graph around them); **REFERENCE** for 218A unless AI pipelines enter scope.

**CISA Secure Software Development Attestation Form** — released 2024-03-11, **form revision
2024-05-14**, OMB Control # 1670-0052, expires 2027-03-31.
⚠️ **Status change worth knowing:** the older CISA landing page is now flagged **"Archived Content"**,
and the live resource page says that under **OMB Memorandum M-26-05 ("Adopting a Risk-Based Approach
to Software and Hardware Security")** agencies *"may choose to use"* the form. **It has moved from
mandatory gate to optional resource — do not model it as binding.**
Its four claims are a compact entity list: (1) software developed and built in **secure
environments**, secured by separating/protecting **each environment**, logging/monitoring/auditing
**trust relationships** used for authorization and access to dev+build environments *and among
components within each environment*, MFA + conditional access, minimizing undue-risk software in
build environments, encrypting credentials, continuous monitoring; (2) **trusted source code supply
chains**; (3) **maintains provenance** for internal code and third-party components; (4) **automated
vulnerability-checking tools** run ongoing and pre-release + remediation policy + **vulnerability
disclosure program**. Scope trigger explicitly includes *"the producer delivers continuous changes to
the software code (as is the case for … continuous delivery/continuous deployment)."*
The **"trust relationship"** framing is directly graph-shaped. **Verdict: REFERENCE.**

---

### 25. CISA SBOM guidance — **the 2021 seven-field list is now superseded**

#### 25a. *2026 Minimum Elements for a Software Bill of Materials (SBOM)* — **published 2026-07-29**

TLP:CLEAR, joint CISA/NSA/FBI + 17 international partners (ACSC, Cyber Centre, NÚKIB, ANSSI, BSI,
CERT-In, ACN, METI, NCSC-NL/NZ, KISA, NASK, NBU…). It **"updates and replaces"** the NTIA 2021 minimum
elements. Predecessor draft: 2025-08-22 (comments closed 2025-10-03).
https://www.cisa.gov/resources-tools/resources/2026-minimum-elements-software-bill-materials-sbom
US Government work / TLP:CLEAR — freely reusable.

**17 data fields in two categories (VERIFIED; ✨ = new since 2021):**
*SBOM Metadata* — SBOM Author · ✨SBOM Author Signature · ✨SBOM Data Format Name · ✨SBOM Data Format
Version · **✨SBOM Generation Context** (*"before build", "build", "after build"*) · SBOM Timestamp ·
✨SBOM Tool Name · ✨SBOM Tool Version · ✨SBOM Version.
*Component Data* — Component Producer *(renamed from Supplier Name)* · Component Name · Component
Version · Component Identifiers *(renamed from Other Unique Identifiers)* · ✨Component Hash Value ·
✨Component Hash Algorithm · ✨Component License · Component Dependency Relationship.

**Practices & Processes elements (6):** Accommodation of Updates to SBOM Data · **Coverage**
*(replaces "Depth"; horizontal breadth + transitive depth, explicitly **"no minimum depth"**)* ·
Distribution and Delivery · **Explicitly Identifying Unknown Information** *(replaces "Known
Unknowns"; now separates **withheld** from **unknown** — a distinction our graph should carry too)* ·
Frequency · **Machine-Processable Data** *(**SWID tags removed**; SPDX and CycloneDX only)*.

Relationship semantics: *"The relationship between two components, where one component is necessary
for the operation of the other… reflects that a component **includes** another component… supports the
capability to build a dependency graph."* Explicit **first-party vs third-party** distinction;
**target component** is the root.
**Verdict: ADOPT** for SBOM field names. ⚠️ **Anything citing the NTIA 2021 seven-field list is now
stale** — this landed a month before this survey.
Access note: **cisa.gov returns 403 to WebFetch**; use curl with a browser User-Agent.

#### 25b. *Framing Software Component Transparency*, third edition, **2024-10-15**

**This is the relationship-semantics source, and it contains explicit edge-direction guidance:**
> "The default relationship type is **'includes.'** This represents the inclusion of or dependency on
> a separate upstream Component… this document reverses the direction to **'included in.'**
> **The choice of direction is not important to the model, as long as one direction is chosen and used
> consistently.**"

Relationship types defined: **Primary** (the component the SBOM is about) · **Included In** ·
**Heritage or Pedigree** (fork/modification; maps to SPDX `GENERATED_FROM`/`DESCENDANT_OF` and
CycloneDX `pedigree`) · **Relationship Completeness**. "Included in" is refined into: *directly
including an unchanged upstream binary* / *including unchanged upstream source by linking or
compiling* / **forking then including**.
Baseline Attributes: *SBOM Meta-Information* (Author Name, Timestamp, Type, **Primary Component / Root
of Dependencies**) and *Component Attributes* (Component Name, Version, Supplier Name, Unique
Identifier, Cryptographic Hash, **Relationship**, License, Copyright Notice).
Undeclared-data taxonomy: Unknown Component Attributes, **Redacted Components**, Unknown Dependencies.
Roles: **Produce / Choose / Operate** (Supplier, Chooser, Operator); and from CISA's *SBOM Sharing
Roles*: **SBOM Author, SBOM Consumer, SBOM Distributor**.
**Verdict: ADOPT** for relationship naming and the direction-discipline rule.

---

### 26. Other NIST material

**SP 800-161r1 (upd1)** — *Cybersecurity Supply Chain Risk Management Practices*, Rev. 1 May 2022,
**updated 2024-11-01**. Entity nouns: supplier, developer, system integrator, external service
provider, acquirer, component. Machine-readable: SCRM Assessment Scoping Questionnaire (.xlsx).
No Rev. 2 announced. **Verdict: REFERENCE** — enterprise-risk altitude, not pipeline altitude.

**NIST IR 8397**, *Guidelines on Minimum Standards for Developer Verification of Software*, **October
2021**. Eleven techniques: threat modeling; automated testing; static code scanning; **heuristic
hardcoded-secret detection**; built-in checks and protections; black-box test cases; code-based
structural test cases; historical test cases; **fuzzing**; web-app scanners; **analysis of included
code (libraries, packages, services)**. **Verdict: REFERENCE** — a useful **check-kind vocabulary**
for typing CI job nodes.

**NIST CSF 2.0** (CSWP 29, 2024-02-26) — **GV.SC-01 … GV.SC-10**. Entity nouns are org-level only:
supplier, customer, partner, third party, technology product and service. Machine-readable via
**CPRT** (csrc.nist.gov/projects/cprt/catalog) and the CSF 2.0 Reference Tool.
**Verdict: IGNORE for pipeline entities; REFERENCE for governance mapping.**

**SP 800-53 Rev. 5 — SR and SA families.** VERIFIED directly from the official **OSCAL catalog**
(`github.com/usnistgov/oscal-content` → `nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json`
— **a genuinely pollable machine-readable artifact; git commits are the change signal**).
*SR family:* SR-1 Policy · SR-2 SCRM Plan (+Establish SCRM Team) · SR-3 Supply Chain Controls and
Processes (+Diverse Supply Base, Limitation of Harm, **Sub-tier Flow Down**) · **SR-4 Provenance**
(+**Identity**, **Track and Trace**, **Validate as Genuine and Not Altered**, **Supply Chain Integrity
— Pedigree**) · SR-5 Acquisition Strategies · SR-6 Supplier Assessments · SR-7 Supply Chain OPSEC ·
SR-8 Notification Agreements · SR-9 Tamper Resistance and Detection · SR-10 Inspection · SR-11
Component Authenticity · SR-12 Component Disposal.
*Pipeline-relevant SA/CM:* SA-3 SDLC (+**Manage Preproduction Environment**) · **SA-10 Developer
Configuration Management** (+Software/Firmware Integrity Verification, **Trusted Generation**,
**Mapping Integrity for Version Control**, **Trusted Distribution**) · **SA-11 Developer Testing and
Evaluation** (+Static Code Analysis, Threat Modeling, Manual Code Reviews, Penetration Testing, Attack
Surface Reviews, Dynamic Code Analysis, IAST) · **SA-15 Development Process, Standards, and Tools**
(+Security and Privacy Tracking Tools, Criticality Analysis, **Archive System or Component**, Logging
Syntax) · SA-22 Unsupported System Components · CM-3 Configuration Change Control · CM-7 Least
Functionality.
**Verdict: REFERENCE** — but **SR-4's Provenance / Identity / Track-and-Trace / Pedigree quartet is the
best-named provenance vocabulary in the corpus** and is worth borrowing verbatim, and the OSCAL JSON
makes it the easiest US-government artifact to poll.

---

### 27. CIS Software Supply Chain Security Guide — **the best-shaped entity taxonomy in this cluster**

| | |
|---|---|
| **Version / date** | **v1.0.** ⚠️ Two dates in circulation and both are real: the **document cover says June 2022**; the **CIS website publish date is 2022-08-31**. Report both. **No v1.1+ found.** Authored with Aqua Security (Eylam Milner, Resheet Kosef) via CIS consensus; contributors from Microsoft, PayPal, Red Hat, CyberArk, Axonius, Sysdig. |
| **URL** | https://www.cisecurity.org/insights/white-papers/cis-software-supply-chain-security-guide (registration-walled) · the full 139-page PDF is redistributed openly at https://raw.githubusercontent.com/aquasecurity/chain-bench/main/docs/CIS-Software-Supply-Chain-Security-Guide-v1.0.pdf |
| **Kind** | Control list whose **section structure is an entity taxonomy**. **113 recommendations**, `N.N.N` scheme. |
| **Verdict** | **ADOPT the taxonomy shape; REFERENCE the text** (licence — see below). |

| # | Category | Sub-entities (recommendation counts) |
|---|---|---|
| 1 | **Source Code** | 1.1 Code Changes (19) · 1.2 Repository Management (7) · 1.3 Contribution Access (13) · 1.4 Third-Party (3) · 1.5 Code Risks (6) |
| 2 | **Build Pipelines** | 2.1 Build Environment (6) · 2.2 Build Worker (8) · 2.3 Pipeline Instructions (8) · 2.4 **Pipeline Integrity** (6) |
| 3 | **Dependencies** | 3.1 Third-Party Packages (8) · 3.2 Validate Packages (4) |
| 4 | **Artifacts** | 4.1 Verification (3) · 4.2 Access to Artifacts (5) · 4.3 **Package Registries** (4) · 4.4 **Origin Traceability** (2) |
| 5 | **Deployment** | 5.1 Deployment Configuration (7) · 5.2 Deployment Environment (4) |

⚠️ *Corrections to the brief's guesses:* there is **no "3.3 Trusted Package Registries"** — registries
sit at **4.3**; and section 2's fourth sub-entity is **"Pipeline Integrity"**, not artifact/build.

Sample recommendation IDs, to show the noun-verb granularity: 1.1.12 *Ensure verification of signed
commits for new changes before merging* · 1.1.14 *Ensure branch protection rules are enforced for
administrators* · 1.1.19 *Ensure any changes to branch protection rules are audited* · 2.3.1 *Ensure
all build steps are defined as code* · 1.2.1 *Ensure all public repositories contain a SECURITY.md file*.

The Guide is **explicitly designed as the parent of platform benchmarks** (its own diagram spawns
**CIS GitHub Benchmark** and **CIS Azure DevOps Benchmark**) and states the vision is *"to support key
emerging standards like SLSA and TUF."*

**⚠️ Licence — read carefully.** The CIS Terms of Use for Non-Member CIS Products draws a distinction:
**CIS Benchmark PDFs → CC BY-NC-SA 4.0**; **CIS Controls and associated guidance documents →
CC BY-NC-ND 4.0 (No Derivatives)**. **Which bucket the *Guide* falls into is not stated — UNVERIFIED.**
Either way it is **NonCommercial**. Do not embed CIS prose. Structure and section *names* are facts,
not expression — cite them; don't copy the recommendation text.

**Machine-readable: none official** (PDF only; CIS-CAT/XCCDF/OVAL cover platform Benchmarks, not this
Guide). **But a high-quality third-party derivative exists and is the actually-reusable artifact:**
**[aquasecurity/chain-bench](https://github.com/aquasecurity/chain-bench), Apache-2.0**, with
`rules.metadata.json` per section. **Its metadata carries an explicit `entity` field, and the distinct
values are: `Organization`, `Repository`, `Branch`, `Pipeline`, `Dependencies`, `PackageRegistry`** —
plus a `type` field (`SCM`, `BUILD`, `DEPENDENCIES`, `ARTIFACT`) and an `slsa_level` array.
**This is the closest existing thing to a git-serious node-type list, and unlike CIS's own text it is
Apache-2.0.** ⚠️ Caveat: chain-bench's last push was 2024-12-11 and it covers only **9 of the 17
subsections**.

**CIS platform benchmarks.** **CIS GitHub Benchmark** — v1.0.0 (2022-12-28), v1.0.1 (2024-04-19),
v1.1.0 (2025-09-02), **v1.2.0 (2026-02-27, current)**. **CIS GitLab Benchmark** — v1.0.0 (2024-04-04),
v1.0.1 (current). Both filed under the CIS technology category **"Software Supply Chain Security"**.
⚠️ **Their entity lists (organization / repository / branch / member / action / runner / secret /
webhook / app / token) are UNVERIFIED** — the PDFs are behind a registration form. Expect the Guide's
1.x–5.x skeleton specialised to GitHub objects, but **treat that as inference, not finding.**
**Useful poll signal:** the `/cis-benchmarks` page ships an **embedded JSON blob** with
`benchmarkTitle`, `benchmarkVersion` and a `published` timestamp (`YYYYMMDDTHHMMSS`) for every
version — a scrapable "what changed" feed with **no login required**.
Machine-readable YAML/XCCDF/OVAL and CIS-CAT are **SecureSuite-member-only**.
**Verdict: ALIGN** — version-track for the GitHub object vocabulary, but re-verify the section list.

---

### 28. Cloud Security Alliance

**Cloud Controls Matrix (CCM) — v4.0.13** (extraction generated 2024-10-31), **197 controls, 17
domains** (A&A, AIS, BCR, CCC, CEK, DSP, DCS, GRC, HRS, IAM, IPY, IVS, LOG, SEF, **STA**, TVM, UEM).
The landing page advertises "v4.1 with combined CCM and CAIQ" — **v4.1 control count UNVERIFIED.**
**STA — Supply Chain Management, Transparency, and Accountability (14):** STA-01 SSRM Policy · STA-02
SSRM Supply Chain · STA-03 SSRM Guidance · STA-04 SSRM Control Ownership · STA-05 SSRM Documentation
Review · STA-06 SSRM Control Implementation · **STA-07 Supply Chain Inventory** ("Develop and maintain
an inventory of all supply chain **relationships**" — an explicitly graph-shaped control) · STA-08
Supply Chain Risk Management · STA-09 Primary Service and Contractual Agreement · STA-10 Supply Chain
Agreement Review · STA-11 Internal Compliance Testing · STA-12 Supply Chain Service Agreement
Compliance · STA-13 Supply Chain Governance Review · STA-14 Supply Chain Data Security Assessment.
**AIS (7):** Policy · Application Security Baseline Requirements · Application Security Metrics ·
**Secure Application Design and Development** · **Automated Application Security Testing** ·
**Automated Secure Application Deployment** · Application Vulnerability Remediation.
**CCC (9):** Change Management Policy · Quality Testing · Change Management Technology ·
**Unauthorized Change Protection** · Change Agreements · Change Management Baseline · **Detection of
Baseline Deviation** · Exception Management · Change Restoration.
**Does it name CI/CD entities? Barely.** AIS-04/05/06 gesture at SDLC/testing/deployment automation
but define **no pipeline nouns** — no build, no artifact, no repository, no runner. CCM's entity model
is *cloud service provider / cloud service customer / supply chain relationship / asset*.
**Licence (VERIFIED): CC BY-NC-SA 4.0** (`LicenseRef-CSA-CC-BY-NC-SA-4.0`).
**Verdict on content: REFERENCE.**

**⚠️ But two CSA machine-readable artifacts are genuinely important:**
1. **`CloudSecurityAlliance-DataSets/dataset-public-laws-regulations-standards`** — normalised
   **CSV + JSON** extractions of CCM 3.0.1, **CCM 4.0.13**, CCM-CAIQ 4.0.3, AICM 1.0.3/1.1.0/1.1.1,
   plus BSI C5/AI-C4, ISO 27001/27002/42001, CIS Controls v8 — with per-version metadata files
   carrying an explicit **SPDX licence block** and a **`known_source_issues`** field. That last field
   is a practice worth copying.
2. **`CloudSecurityAlliance/SecurityControlsCatalog`** — CSA's canonical machine-readable catalogue,
   **expressing controls as a graph in STIX 2.1** with custom SDOs **`x-control`, `x-regulation`,
   `x-gap-mapping`, `x-control-implementation`, `x-capability`, `x-control-assessment`**, connected by
   standard STIX `relationship` objects and interoperating with MITRE ATT&CK. Currently 987 controls /
   423 gap-mappings / 320 relationships / 106 regulations. Self-described as *"early-stage /
   research-grade… exploratory and provisional."* Deliberately **interoperates with rather than
   replaces OSCAL**.
   **Verdict: ALIGN — and read this before naming any compliance-edge type.** It is direct prior art
   for "controls-and-relationships as a graph". Inventing a private control-edge vocabulary without
   reading it would be exactly the failure this survey exists to prevent.

**CSA AI Controls Matrix (AICM)** — **v1.1.0** (workbook generated 2026-06-18); **v1.1.1 shipped
2026-07-13**. ⚠️ *Both were published upstream under the bare label "v1.1", distinguishable only by
filename and a stamp in cell A1* — a cautionary tale about pinning by label. **247 controls, 18
domains** (243 in v1.0.3). STA grows to **16**; AIS grows to **15**, adding AIS-08 API Security,
AIS-09 Input Validation, AIS-10 Output Validation, **AIS-11 Agents Security Boundaries**, **AIS-12
Source Code Management**, AIS-13 AI Sandboxing, AIS-14 AI Cache Protection, AIS-15 Prompt
Differentiation. Each control carries `threat_category` (e.g. `insecure_supply_chain`) and a
**`typical_control_applicability_and_ownership`** object with a closed 10-value ownership vocabulary.
CC BY-NC-SA 4.0. **Verdict: REFERENCE.**

**CSA DevSecOps pillars** — *Six Pillars of DevSecOps*, 2019-08-07. **The pillar names are
UNVERIFIED** (artifact PDF is login-walled; the landing page does not enumerate them). *Information
Security Management through Reflexive Security* — **UNVERIFIED, could not retrieve.** Both are
2019-era organisational-practice vocabulary, not pipeline entities. **Verdict: IGNORE.**

---

### 29. ENISA and the EU

#### 29a. ENISA *Threat Landscape for Supply Chain Attacks* — **a genuinely compact entity model**

**July 2021** (covering Jan 2020 – early July 2021). ISBN 978-92-9204-509-8, DOI 10.2824/168593.
57 pp. https://www.enisa.europa.eu/publications/threat-landscape-for-supply-chain-attacks
**Licence: "© ENISA, 2021. Reproduction is authorised provided the source is acknowledged."** —
attribution-only and **commercially reusable**. *The most permissive non-US-Government source in this
survey.*

**The four key elements, verbatim:**
- **Supplier** — "an entity that supplies a product or service to another entity."
- **Supplier Assets** — "valuable elements used by the supplier to produce the product or service."
- **Customer** — "the entity that consumes the product or service produced by the supplier."
- **Customer Assets** — "valuable elements owned by the target."
- Plus: "An entity can be individuals, groups of individuals, or organizations. Assets can be people,
  software, documents, finances, hardware, or others."

**The definitional invariant — a real rule, worth stealing:**
> "A supply chain attack is a combination of at least two attacks… for an attack to be classified as
> a supply chain one, **both the supplier and the customer have to be targets**. If no customer is
> attacked, or no supplier attacked, then it is probably not a supply chain attack."

**Table 1 — the full four-column taxonomy:**
- *Attack Techniques Used to Compromise the Supply Chain (7):* Malware Infection · Social Engineering ·
  Brute-Force Attack · Exploiting Software Vulnerability · Exploiting Configuration Vulnerability ·
  Physical Attack or Modification · Open-Source Intelligence (OSINT). *(Table 1 lists six; §2.2's
  Table 2 adds Physical Attack or Modification and Counterfeiting.)*
- *Supplier Assets Targeted (8):* **Pre-existing Software** ("software used by the supplier… does not
  include software libraries") · **Software Libraries** ("third party libraries, software packages
  installed from third parties such as npm, ruby") · **Code** ("source code or software produced by
  the supplier") · **Configurations** ("passwords, API keys, firewall rules, URLs") · **Data** ·
  **Processes** ("updates, backups or validation processes, signing certificates processes") ·
  **Hardware** · **People**.
- *Attack Techniques Used to Compromise the Customer (6):* Trusted Relationship [T1199] · Drive-by
  Compromise [T1189] · Phishing [T1566] · Malware Infection · Physical Attack or Modification ·
  Counterfeiting. *(ATT&CK IDs are given inline — a ready-made cross-reference.)*
- *Customer Assets Targeted (7):* Data · Personal Data · Intellectual Property · Software · Processes ·
  Bandwidth · Financial · People.

Explicitly positioned as *complementary to, not a replacement for*, MITRE ATT&CK.
**Verdict: ADOPT** for the attack/threat side. The supplier/supplier-assets/customer/customer-assets
quadrant is the cleanest four-node schema published by anyone in this cluster, and "Supplier Assets"
enumerates exactly the CI/CD nouns we care about (Code, Configurations, Processes, Software Libraries).

#### 29b. Newer ENISA material
*Good Practices for Supply Chain Cybersecurity*, **2023-06-13** — aimed at NIS2 "essential and
important entities"; entity vocabulary **UNVERIFIED**. **REFERENCE, low priority.**
***ENISA Threat Landscape 2025***, published 2025-10-01, **revised v1.2 on 2026-01-09** (4,875
incidents, 2024-07-01 → 2025-06-30). **VERIFIED: it has no supply-chain chapter and does NOT restate
the 2021 four-part taxonomy.** "Supply chain compromise" appears only as a technique inside threat
narratives (including "targeting of the AI supply chain, with poisoned hosted machine learning
models"). **Verdict: IGNORE for vocabulary — the 2021 report remains the taxonomy of record.**

#### 29c. BSI TR-03183 Part 2 — the strictest SBOM field list
*Cyber Resilience Requirements for Manufacturers and Products, **Part 2: Software Bill of Materials
(SBOM)*, version 2.1.0, dated 2025-08-20.** Family: Part 1 *General Requirements* v1.0.0; Part 2
v2.1.0; Part 3 *Vulnerability Reports* v1.0.0; Part H *Module H Conformity* v1.1.0.
**Formats mandated:** JSON or XML, and a valid **CycloneDX ≥ 1.6** or **SPDX ≥ 3.0.1** document —
officially released spec versions only.
**REQUIRED for the SBOM (2):** Creator of the SBOM (email, or URL if none) · Timestamp.
**REQUIRED per component (10):** Component creator · Component name · Component version (SemVer or
CalVer preferred; else the file's modification date per RFC 3339) · **Filename of the component** ·
**Dependencies on other components** (*"the completeness of this enumeration MUST be clearly
indicated"*) · Distribution licences · **Hash value of the deployable component (SHA-512)** ·
**Executable property** · **Archive property** · **Structured property**.
*The last three are a BSI-only tri-axis you will not find in the CISA or NTIA lists.*
**ADDITIONAL (MUST if it exists):** SBOM-URI · Source code URI · URI of the deployable form · other
unique identifiers (CPE, purl) · original licences. **OPTIONAL:** effective licence · hash of source
code · URL of the component creator's `security.txt`.
**Entity terms defined (§3.2):** Component · **Logical component** · **External component** ·
**Identified component** · **Component referenced by another BOM** · Executable file · Dependency ·
Licence information · **Vendor/Supplier vs. creator** (the same distinction CISA now draws via SBOM
Author vs Component Producer — an independent convergence).
**Level-of-detail taxonomy (§8.3):** Top-level SBOM · n-level SBOM · Transitive SBOM · **Delivery item
SBOM** · Complete SBOM.
**SBOM classification (§8.4): Design / Source / Build / Analysed / Deployed / Runtime SBOM** — the
sharpest version of what CISA calls "SBOM Generation Context" and SPDX calls `SbomType`. **Three
standards, three names, one concept** (see the naming-guidance section).
Rule worth noting: *"An SBOM compliant with this Technical Guideline MUST contain the same information
as available during the build process."*
Licence: German federal publication; reuse terms **UNVERIFIED** (no CC statement observed).
Poll signal: the PDF's own **Table 1 "Document History"** with version + ISO date.
**Verdict: ALIGN.** Its Design/Source/Build/Analysed/Deployed/Runtime axis is directly usable as an
SBOM node subtype, and it is the field list to satisfy if EU defensibility matters.

#### 29d. EU Cyber Resilience Act
Regulation (EU) **2024/2847**; **in force December 2024, full application 11 December 2027**. CRA is
the reason TR-03183 exists. The CISA 2026 document notes the CRA obligation "of products with digital
elements to provide an SBOM as part of the technical documentation."
⚠️ **Article 3 definitions and the exact Annex I Part II / Annex VII SBOM wording (including the
top-level-dependencies scope) are UNVERIFIED** — EUR-Lex returned HTTP 202 bot challenges on every
endpoint tried. Retrieve via a browser or the EUR-Lex ELI XML API before relying on specifics.

#### 29e. Others in this family — all UNVERIFIED, all paywalled
**ISO/IEC 5230:2020** (OpenChain licence compliance, December 2020; functionally identical to OpenChain
2.1) — the specific programme-entity terms are **UNVERIFIED**. **ISO/IEC 18974** (OpenSSF security
assurance) — **UNVERIFIED**. **IEC 62443-4-1** — **not verified this session**. **PCI DSS v4.0
Requirement 6** — **not verified this session** (though CSA's SecurityControlsCatalog lists PCI DSS as
an `x-control` publisher, so a machine-readable route may exist there).
**Verdict for the ISO/IEC family: REFERENCE at most.** Paywalled standards are poor adoption
candidates on licensing grounds alone — we cannot cite the text, and readers cannot check us.

---

# Part 2 — Synthesis

## 2.1 Union list of ENTITY concepts

Deduplicated across all 29 sources above. **"Sources"** counts *independent* standards bodies/projects
that name the concept — not every mention. The **Name to use** column is my recommendation; the
reasoning is in §2.4.

### A. Actors and organisations

| Concept | Named by | Name to use |
|---|---|---|
| **Organization** | SLSA Source, SPDX (`Organization`), OCSF (`organization`), Allstar, Scorecard, chain-bench (`Organization`), CycloneDX (`organizationalEntity`), STIX (`identity`), OSPS | `organization` |
| **Project** | OSPS (defined: "group of people **and resources**"), Security Insights (`Project`), OWASP OSS-Risk, SCVS | `project` |
| **Subproject** | OSPS (defined: "codebase part of the project maintained in a separate repository") | `subproject` |
| **Person / human identity** | SPDX (`Person`), SLSA Source (`Trusted Person`/`Untrusted Person`), STIX (`identity`), OCSF (`user`), gittuf (`principal`), OSPS (`User`, `Maintainer` — both explicitly human), D3FEND (`UserAccount`) | `person` |
| **Bot / machine identity** | **SLSA Source `Trusted Robot`**, in-toto `functionary` ("individual **or automated script**"), SP 800-204D `actor` ("can also be a non-human, such as a build orchestrator"), SPDX `SoftwareAgent`, OCSF `programmatic_credentials`, OWASP CICD-SEC-2 "programmatic account", D3FEND `ServiceAccount` | `robot` (SLSA's word) or `service_account` |
| **Role / authority level** | SLSA Source (Administrator/Trusted Person/Trusted Robot/Untrusted Person), SPDX (`Role`, `RoleRelationship`), TUF (root/targets/snapshot/timestamp), OSPS (Administrator/Maintainer/Collaborator/Contributor), OCSF (`iam_role`), RATS (7 roles), SCITT (Issuer/Auditor/Relying Party) | `role` |
| **Supplier** | ENISA (`Supplier`), SP 800-161r1, CSF 2.0 GV.SC, SPDX (`suppliedBy`), CycloneDX (`supplier`), CISA SBOM (`Component Producer`), BSI (Vendor/Supplier vs creator), MITRE SoT | `supplier` |
| **Consumer / relying party** | SLSA (`consumer`), SCITT (`Relying Party`), RATS (`Relying Party`), ENISA (`Customer`), CISA Framing (`Chooser`/`Operator`) | `consumer` |
| **Group / team** | OCSF (`group`, class 3006), OSPS, Allstar, SPDX (`has-member`/`member-of`) | `group` |

### B. Source control

| Concept | Named by | Name to use |
|---|---|---|
| **Source control system / forge** | **SLSA Source (`Source Control System`/SCS)**, D3FEND (`VersionControlTool`), OSPS (`Version Control System`), OWASP CICD-SEC (`SCM`), CIS Guide §1, SCVS V3 | `source_control_system` |
| **Repository** | SLSA Source, SPDX, D3FEND (`CodeRepository`), OSPS, OCSF (*absent*), chain-bench (`Repository`), Sigstore (`Source Repository URI`), SARIF (`repositoryUri`), CVE 5.2 (`repo`), gittuf, Scorecard, SP 800-204D | `repository` |
| **Revision / commit** | **SLSA Source (`Revision`)**, OSPS (`Commit`), CycloneDX (`commit`), SARIF (`revisionId`), Sigstore (`Source Repository Digest`), OSV (`GIT` range events), gittuf (`targetID`), D3FEND | `revision` for the immutable snapshot; `commit` as the git-flavoured alias |
| **Named reference (branch/tag)** | **SLSA Source (`Named Reference`; branch = moving, tag = immutable)**, gittuf (`git:refs/heads/*`), OSPS (`Primary Branch`), SARIF (`branch`), Sigstore (`Source Repository Ref`), Scorecard, Allstar, chain-bench (`Branch`), CIS 1.1 | `named_reference` (with `branch`/`tag` subtypes) |
| **Protected reference / protection rule** | **SLSA Source (`Protected Named Reference`)**, gittuf (`protected namespace` + rule), Scorecard (`Branch-Protection`), Allstar (`branch`), OWASP CICD-SEC-1, CIS 1.1.14/1.1.19 | `protection_rule` |
| **Change request / pull request** | OWASP CICD-SEC-1/4, Scorecard (`Code-Review`), OSPS (`Change`), CIS 1.1, SP 800-204D (`PULL-PUSH_REQ`) | `change_request` |
| **Review / approval** | **SLSA Source L4 (`Two-Party Review`)**, gittuf (**reference authorization attestation** — approval as an edge), OSPS (`require merge approvals`), Scorecard, in-toto (`threshold`), TUF (`threshold`) | `approval` — **as an edge, not a field** |
| **Status check** | **OSPS (`Status Check`, defined)**, Scorecard (`CI-Tests`), OWASP CICD-SEC-1 | `status_check` |
| **Source file / source code** | SPDX (`File`, `Snippet`), D3FEND (`SourceCode`), CVE 5.2 (`programFiles`, `programRoutines`), SARIF (`artifact`, `logicalLocation`), OCSF (`affected_code`), ENISA (`Code`), CycloneDX (`componentData.type: source-code`) | `file` |
| **Config-as-code / pipeline definition file** | **OWASP CICD-SEC-4 (`CI configuration file`)**, SLSA (`Build Config URI`), Sigstore (`.1.18/.1.19`), SSDF (configuration-as-code), 800-204C (policy-as-code, config code), D3FEND (`ApplicationConfigurationFile`, `CompilerConfigurationFile`), S2C2F (`package source config file`), CIS 2.3.1 | `pipeline_definition` |

### C. Build and pipeline

| Concept | Named by | Name to use |
|---|---|---|
| **Pipeline / workflow** | **CycloneDX (`workflow`)**, OSPS (`CI/CD Pipeline` **and** `Build and Release Pipeline` — distinguished), OWASP CICD-SEC, CIS §2, chain-bench (`Pipeline`), SP 800-204D, SCVS V3, A03:2025 | `workflow` (CycloneDX) or `pipeline` (everyone else) — see §2.4 |
| **Task** | **CycloneDX (`task`, `taskType`, `taskDependencies`)**, SP 800-204D (`step`), in-toto (`step`) | `task` |
| **Step / command** | **CycloneDX (`step`, `command.executed`)**, in-toto (`step`, `expected_command`), SARIF (`invocation.commandLine`), OCSF (`cmd_line`) | `step` |
| **Run / invocation** | **SARIF (`invocation`)**, SLSA (`runDetails`, `metadata.invocationId`), Sigstore (`Run Invocation URI`), in-toto (`link`), CycloneDX (`timeStart`/`timeEnd`) | `run` |
| **Trigger / event** | **CycloneDX (`trigger`: manual/api/webhook/scheduled + `event` + `conditions`)**, Sigstore (`Build Trigger`), OWASP CICD-SEC-4 (`push`/`pull_request`), OCSF (`job_trigger`) | `trigger` |
| **Runner / build node / worker** | **OWASP CICD-SEC-5 (`execution node`, `controller node`)**, CIS 2.2 (`Build Worker`), Sigstore (`Runner Environment`), SPDX (`hasHost`), D3FEND, SLSA (`Isolated`/`Hosted`), SCVS V3 | `runner` |
| **Build platform / builder** | **SLSA (`build platform`, `builder.id`)**, in-toto (`functionary`), SP 800-204D (**build control plane**, explicitly at higher trust than steps), D3FEND (`BuildTool`), SPDX (`Build.buildType`) | `build_platform` |
| **Workspace / volume** | **CycloneDX (`workspace`, `volume`, `accessMode`, `mountPath`)** — *the only standard that names it* | `workspace` |
| **Environment** | **SSDF PO.5 (explicitly instructs enumerating them)**, CISA Attestation Form ("each environment"), Sigstore (`Deployment Environment`), CIS 2.1/5.2, OWASP CICD-SEC-5/7, SP 800-53 SA-3(2) `Manage Preproduction Environment`, SLSA | `environment` |
| **Build input: external vs internal parameter** | **SLSA (`externalParameters` vs `internalParameters`)**, **SP 800-204D (`consumes` vs `uses`)**, in-toto (`materials` vs tools), CycloneDX (`inputs.source`/`.resource`) | keep both: `input` (consumed) vs `tool` (used) |

### D. Artifacts and distribution

| Concept | Named by | Name to use |
|---|---|---|
| **Artifact** | **in-toto (`Artifact` = material or product)**, SLSA (`ResourceDescriptor`), SPDX (`Artifact`), SARIF (`artifact` + 24 `roles`), SCITT (`Artifact`), OmniBOR (`Artifact`), SP 800-204D, CIS §4, OWASP CICD-SEC-9 | `artifact` |
| **Package** | SPDX (`Package`), CycloneDX (`component`), OCSF (`package`), OSV, D3FEND (`SoftwarePackage`), PURL, S2C2F, SCVS V4 | `package` |
| **Container image** | CycloneDX (`component.type: container`), D3FEND (`ContainerImage`), OCSF (`image`, `container`), PURL (`docker`, `oci`), ATLAS AML.T0010.004, A03:2025 | `container_image` |
| **Release** | **OSPS (`Release` — defined as both verb and noun)**, in-toto (`release` predicate), Security Insights (`ReleaseDetails`), Scorecard (`Signed-Releases`), SSDF PS.2/PS.3, SPDX (`releaseTime`) | `release` |
| **Released software asset** | **OSPS (`Released Software Asset` — "binaries, libraries, containers")** | fold into `artifact` |
| **Package registry / artifact repository** | **CIS 4.3**, SP 800-204D (Table 1: build repository, package repository), S2C2F (`binary repository manager`, `curated feed`), SCVS V4 (**registry ≠ manager**), OWASP CICD-SEC-3/10, chain-bench (`PackageRegistry`), A03:2025 | `package_registry` |
| **Deployment** | CIS §5, CycloneDX (`taskType: deploy`), OWASP CICD-SEC-1, D3FEND (`SoftwareDeploymentTool`), ATT&CK T1072, SP 800-204D (`DEPLOY-REQ`) | `deployment` |
| **Digest / hash** | Everywhere: in-toto (`digest`), SLSA, SPDX (`Hash`), CycloneDX (`hashes`), OpenVEX (`hashes`), BSI (SHA-512 mandated), CISA 2026 (`Component Hash Value` + `Algorithm`), OCSF, Sigstore | `digest` |
| **Signature** | Sigstore, in-toto (DSSE), TUF, gittuf, CycloneDX (`signature`), SPDX, OCSF (`digital_signature`), Scorecard (`Signed-Releases`), CIS 1.1.12 | `signature` |

### E. Dependencies

| Concept | Named by | Name to use |
|---|---|---|
| **Dependency** | SPDX (`dependsOn` + 6 variants), CycloneDX (`dependsOn`/`provides`), D3FEND (`Dependency`), OSV, SCVS V1, CISA SBOM (`Component Dependency Relationship`), BSI, CIS §3 | `dependency` — **as an edge with a lifecycle scope** |
| **Dependency manifest / lockfile** | **SPDX (`hasDependencyManifest`)**, S2C2F (`package source config file`, lock file), Scorecard (`Pinned-Dependencies`), OWASP CICD-SEC-3 (`version lock`) | `dependency_manifest` |
| **Ingestion point** | **S2C2F alone** ("how a dependency entered" — ING-1..4) | `ingestion` — **single-source; interrogate before adopting** |
| **SBOM** | SPDX (`Sbom` + 6 `SbomType`s), CycloneDX, OCSF (`sbom`), CISA 2026, BSI (6-way classification), OSPS, SCVS V2, Scorecard (`SBOM` check) | `sbom` |

### F. Identity, secrets and access

| Concept | Named by | Name to use |
|---|---|---|
| **Credential / secret** | D3FEND (`Credential` + 11 subclasses), OWASP CICD-SEC-6, OSPS-BR-07, ENISA (`Configurations`: "passwords, API keys"), ATT&CK T1552, CIS, SCVS, SSDF | `credential` |
| **Token** | D3FEND (`AccessToken`, `SessionToken`, `WebIdentityToken`), ATT&CK **T1528 (names CI/CD pipeline tokens)**, OCSF (`api.token`), Scorecard (`Token-Permissions`), OWASP CICD-SEC-2/8 | `token` |
| **Key** | TUF, gittuf (`principal` ≈ signing key), Sigstore, in-toto (`pubkeys`), OWASP CICD-SEC-2/8 (`SSH key`, `deploy key`) | `key` |
| **Permission grant** | **OWASP CICD-SEC-2/8 (granted vs *actually used* — a distinction almost nobody else draws)**, Scorecard (`Token-Permissions`), Allstar, OSPS-GV-04, OCSF (`privileges`) | `permission_grant` — **as an edge with `granted` and `last_used`** |
| **Policy** | OCSF (`policy`), in-toto (`layout`), SP 800-204D ("a signed document that encodes the requirements"), TUF, gittuf (`rule file`), Allstar, RATS (`Appraisal Policy`), SCITT (`Registration Policy`) | `policy` |
| **Threshold / n-of-m rule** | **TUF (`threshold`)**, **gittuf (`(2, {Alice, Bob, Carol})`)**, **in-toto (`step.threshold`)**, SLSA Source L4 | `threshold` — **an edge property** |
| **Webhook** | Scorecard (`Webhooks`, Critical), OWASP CICD-SEC-8, CycloneDX (`trigger.type: webhook`), Allstar | `webhook` |
| **Third-party integration / app** | **OWASP CICD-SEC-8 (five methods: GitHub App, OAuth app, access token, SSH key, webhook)**, Allstar (`action` policy), CSA STA-07, A03:2025 | `integration` |

### G. Claims, evidence and findings

| Concept | Named by | Name to use |
|---|---|---|
| **Attestation** | **in-toto (the framework)**, SLSA, SCITT (`Signed Statement`/`Transparent Statement`), gittuf, Security Insights (`Attestation` w/ `predicate-uri`), CycloneDX (`declarations.attestations`), SP 800-204D (4 kinds), OCSF (⚠️ *different meaning*) | `attestation` |
| **Provenance** | SLSA (the predicate), SP 800-53 **SR-4 Provenance/Identity/Track-and-Trace/Pedigree**, OSPS (`Software Provenance`), SSDF PS.3.2, CISA Attestation Form claim 3, SCVS V6, CIS 4.4 (`Origin Traceability`) | `provenance` |
| **Claim / statement** | SCITT (`Statement`), CycloneDX (`declarations.claims` + **`evidence`/`counterEvidence`**), OpenVEX (`statement`), RATS (`Evidence`/`Attestation Results`) | `claim` |
| **Evidence** | CycloneDX (`evidence`, `componentEvidence`), SPDX (`hasEvidence`), OCSF (`evidences`), RATS, OSPS | `evidence` |
| **Verification result** | **SLSA VSA**, in-toto (`svr`, `vsa`), RATS (`Attestation Results`), SCITT (`Receipt`) | `verification_summary` |
| **Vulnerability** | CVE, OSV, CVSS, SPDX (`Vulnerability`), CycloneDX, OCSF (2002), OpenVEX, CSAF | `vulnerability` |
| **VEX status** | **OpenVEX (4 statuses + 5 justifications)**, CycloneDX (`impactAnalysisState` + 9 justifications), CSAF, SPDX (4 Vex* classes) | adopt **OpenVEX**'s enums |
| **Finding** | OCSF (2002–2008), SARIF (`result` + `kind`/`level`/`baselineState`), Scorecard (check result) | `finding` |
| **Control / requirement** | OSPS (`OSPS-XX-NN`), SSDF (`PO.1.1`), CIS (`N.N.N`), CCM (`STA-07`), SP 800-53, CycloneDX (`definitions.standards.requirements`), Gemara (`ControlCatalog`), CSA (`x-control`) | `requirement` |
| **Tool / scanner** | SPDX (`Tool`, `usesTool`), SARIF (`tool`, `toolComponent`), CycloneDX (`tools`), OCSF (`product`, `analytic`), Security Insights (`SecurityTool`), D3FEND (`CodeAnalyzer`), IR 8397 (11 techniques) | `tool` |
| **Log / audit record** | OWASP CICD-SEC-10 (**audit log vs applicative log**), D3FEND (`Log`), SCVS V3 (system + build-job audit logs), CIS 1.1.19, gittuf (RSL), SCITT (append-only log), Rekor | `audit_record` |
| **Threat / technique label** | ATT&CK (T1195.001, T1554, T1552.007, T1528, T1072, T1199), CAPEC (444/511/538/669/670), CWE, OWASP CICD-SEC-N, A03:2025, ENISA, ATLAS | keep as **labels on findings**, not nodes |

---

## 2.2 Union list of RELATIONSHIP concepts

| Edge concept | Named by (spelling used) | Recommended |
|---|---|---|
| **produces / generates** | SP 800-204D (`produces`), SPDX (`hasOutput`, `generates`), D3FEND (`produces`/`produced-by`), in-toto (`products`), CycloneDX (`outputs`), STIX (—) | `produces` |
| **consumes / has input** | SP 800-204D (`consumes`), SPDX (`hasInput`), D3FEND (`has-input`/`input-of`), in-toto (`materials`), CycloneDX (`inputs`), SLSA (`resolvedDependencies`) | `consumes` |
| **uses (as a tool)** | **SP 800-204D (`uses` — explicitly tools, distinct from consumes)**, SPDX (`usesTool`), STIX (`uses`), D3FEND (`uses`/`used-by`), ATT&CK (`uses`) | `uses` |
| **depends on** | SPDX (`dependsOn` + `hasOptionalDependency`/`hasProvidedDependency`/`hasPrerequisite`/`hasRequirement`), CycloneDX (`dependsOn`), D3FEND (`depends-on`), OCSF (`Depends On`), CISA (`includes`/`included in`) | `depends_on` **+ lifecycle scope** |
| **contains / includes** | SPDX (`contains`), STIX (`consists-of`), D3FEND (`contains`/`may-contain`), CISA Framing (`included in`), CSAF (`default_component_of`), SARIF (`includes`/`isIncludedBy`) | `contains` |
| **runs on / hosted by** | **SPDX (`hasHost`)**, STIX (`hosts`), Sigstore (`Runner Environment`), OWASP CICD-SEC-5 | `runs_on` |
| **invoked by / triggered by** | **SPDX (`invokedBy`)**, CycloneDX (`trigger`), Sigstore (`Build Trigger`), D3FEND (`invokes`/`invoked-by`) | `triggered_by` |
| **derived from / lineage** | STIX (`derived-from` — one of only 3 universal), SPDX (`ancestorOf`/`descendantOf`/`hasVariant`), CycloneDX (`pedigree.ancestors/descendants/variants`), CISA Framing (`Heritage or Pedigree`), SP 800-53 SR-4(4) `Pedigree`, D3FEND (`derived-from`) | `derived_from` |
| **attests to / has evidence** | in-toto (`subject`), SPDX (`hasEvidence`), gittuf (reference authorization), SCITT (`Statement` about `Subject`), CycloneDX (`claims.evidence`) | `attests_to` |
| **signs / signed by** | **D3FEND (`signs`/`signed-by`)**, TUF, Sigstore, in-toto, gittuf | `signed_by` |
| **authored by / committed by** | STIX (`authored-by`), SPDX (`originatedBy`, `suppliedBy`), CycloneDX (`commit.author`/`committer`), ⚠️ **gittuf explicitly rejects the commit email as identity** | `authored_by` |
| **approves** | **gittuf (approval = an attestation edge)**, SLSA Source L4, in-toto (`threshold`), OSPS | `approves` **with `threshold` property** |
| **delegates to** | **TUF (delegated targets, with threshold)**, SPDX (`delegatedTo`), gittuf (delegation chains) | `delegates_to` |
| **grants permission** | OWASP CICD-SEC-2/8 (granted vs used), Allstar (config inheritance), OCSF (`privileges`) | `grants` **with `granted_at` / `last_used_at`** |
| **stored in** | **SP 800-204D (`is stored in`)**, SPDX (`hasDistributionArtifact`), CIS 4.3 | `stored_in` |
| **affects / does not affect** | SPDX (`affects`, `doesNotAffect`, `underInvestigationFor`, `fixedIn`), OpenVEX (statuses), CycloneDX (`affects`), CSAF | `affects` **with VEX status** |
| **mitigates / remediates** | STIX (`mitigates`, `remediates`), ATT&CK (`mitigates`), D3FEND (tactic verbs), SPDX | `mitigates` |
| **precedes / follows** | **CAPEC (`CanPrecede`/`CanFollow`)**, **CWE (+`StartsWith`, `Requires`)**, **SARIF (`canPrecede`/`canFollow`/`willPrecede`/`willFollow`)**, D3FEND (`precedes`/`preceded-by`), CycloneDX (`taskDependencies`), in-toto (`MATCH … FROM <step>`) | `precedes` |
| **matches output of** | **in-toto (`MATCH <pattern> WITH PRODUCTS FROM <step>`)** — *the pipeline data-flow edge; only in-toto states it as a rule* | `matches_output_of` |
| **alias of / related to** | **OSV (`aliases` symmetric+transitive, `related` symmetric-only, `upstream` transitive-only)**, STIX (`duplicate-of`, `related-to`) | copy **OSV's documented algebra** |
| **describes** | SPDX (`describes`), CISA (`Primary Component`), CycloneDX (`metadata.component`) | `describes` |

### Edge *properties* the standards insist on (per the skill's Step-4 adjudication rule)

A bare edge is a defect. These are the properties the field has already decided matter:

| Property | Source | Question it settles |
|---|---|---|
| **`scope` (design/development/build/test/runtime/other)** | **SPDX `LifecycleScopedRelationship`** | "depends on **when**?" — build-time vs runtime dependency is a different risk |
| **`completeness` (complete/incomplete/noAssertion)** | **SPDX `RelationshipCompleteness`**, CycloneDX `aggregate` (10 values), CISA "Coverage" + "Explicitly Identifying Unknown Information" (withheld ≠ unknown), BSI "completeness MUST be clearly indicated" | "is this the whole story?" |
| **`threshold` (n-of-m)** | TUF, gittuf, in-toto, SLSA Source L4 | "how many approvals?" |
| **`confidence` + `technique`** | **CycloneDX `componentEvidence.identity`** (10 techniques) | "how do we know this is that?" |
| **`granted_at` / `last_used_at`** | OWASP CICD-SEC-2/8 | "is this permission dormant?" |
| **`justification`** | OpenVEX (5), CycloneDX (9) | "why is this not exploitable?" |
| **`enforcement` (log/issue/fix/block)** | **Allstar** | "observed or actually prevented?" |
| **`continuity` (start revision, lapses)** | **SLSA Source** | "was the control enforced the whole time?" |
| **`author` + `timestamp` on the claim itself** | OpenVEX, in-toto, SCITT, gittuf, CycloneDX `declarations` | "who said so, and when?" |

---

## 2.3 The strong signal — concepts named by **three or more independent standards**

These are the ones the skill says to adopt without further argument. Ordered by strength of signal.

| # | Concept | Independent sources | Count |
|---|---|---|---|
| 1 | **Repository** | SLSA Source · SPDX · D3FEND · OSPS · gittuf · SARIF · Sigstore · CVE 5.2 · CIS · chain-bench · SP 800-204D · Scorecard | 12 |
| 2 | **Artifact** | in-toto · SLSA · SPDX · SARIF · SCITT · OmniBOR · SP 800-204D · CIS · OWASP CICD-SEC · D3FEND | 10 |
| 3 | **Credential / secret / token** | D3FEND · ATT&CK (T1552, T1528) · OWASP CICD-SEC-6 · OSPS-BR-07 · ENISA · CIS · SCVS · Scorecard · SSDF | 9 |
| 4 | **Dependency** (as a typed, scoped edge) | SPDX · CycloneDX · OSV · D3FEND · CISA SBOM · BSI · SCVS · CIS · S2C2F | 9 |
| 5 | **Named reference / branch** | SLSA Source · gittuf · OSPS · SARIF · Sigstore · Scorecard · Allstar · chain-bench · CIS | 9 |
| 6 | **Pipeline / workflow** | CycloneDX · OSPS · OWASP CICD-SEC · CIS · chain-bench · SP 800-204D · SCVS · OWASP A03:2025 | 8 |
| 7 | **Attestation** | in-toto · SLSA · SCITT · gittuf · Security Insights · CycloneDX · SP 800-204D | 7 |
| 8 | **Revision / commit** | SLSA Source · OSPS · CycloneDX · SARIF · Sigstore · OSV · gittuf | 7 |
| 9 | **Package registry / artifact repository** | CIS 4.3 · SP 800-204D · S2C2F · SCVS V4 · OWASP CICD-SEC · chain-bench · A03:2025 | 7 |
| 10 | **Environment** | SSDF PO.5 · CISA Attestation Form · Sigstore · CIS · OWASP CICD-SEC-5/7 · SP 800-53 SA-3(2) · SLSA | 7 |
| 11 | **Provenance** | SLSA · SP 800-53 SR-4 · OSPS · SSDF PS.3.2 · CISA · SCVS V6 · CIS 4.4 | 7 |
| 12 | **Runner / build node** | OWASP CICD-SEC-5 · CIS 2.2 · Sigstore · SPDX (`hasHost`) · SLSA · SCVS V3 | 6 |
| 13 | **Release** | OSPS · in-toto · Security Insights · Scorecard · SSDF PS.2/PS.3 · SPDX | 6 |
| 14 | **Robot / non-human actor** | SLSA Source (`Trusted Robot`) · in-toto (`functionary`) · SP 800-204D · SPDX (`SoftwareAgent`) · OWASP CICD-SEC-2 · D3FEND | 6 |
| 15 | **Policy / rule with a threshold** | TUF · gittuf · in-toto · SLSA Source L4 · Allstar · SCITT | 6 |
| 16 | **SBOM** | SPDX · CycloneDX · OCSF · CISA 2026 · BSI · OSPS · SCVS · Scorecard | 8 |
| 17 | **Vulnerability + VEX status** | CVE · OSV · OpenVEX · CycloneDX · SPDX · CSAF · OCSF | 7 |

**Verdict: all seventeen are mandatory.** Any of them missing from our node/edge corpus is a question
the product silently cannot answer.

**Three relationship verbs clear the same bar and should be spelled the standards' way:**
**`produces`** (SP 800-204D, SPDX `hasOutput`, D3FEND, in-toto, CycloneDX),
**`consumes`** (SP 800-204D, SPDX `hasInput`, D3FEND, in-toto, SLSA),
**`uses`** (SP 800-204D, SPDX `usesTool`, STIX, D3FEND, ATT&CK).

---

## 2.4 Naming guidance — where the industry lingua franca already exists

**The rule:** where a term is the field's common word, use it. A private synonym costs us legibility,
comparability and review-defensibility, and buys nothing.

### Use these exact spellings — they are settled

| Use | Not | Why |
|---|---|---|
| **`purl`** as the package identity key | a private component id | ECMA-427 + SPDX + CycloneDX + OSV + OCSF + CSAF + CVE 5.2 all point at it. **The single strongest convergence in the survey.** Registered types already include `git`, `github`, `docker`, `oci`, `bazel`. |
| **`workflow` / `task` / `step` / `trigger` / `workspace`** | `job`/`stage`/`phase`/`action` | CycloneDX `formulation` is the only real schema for this and it is now ECMA-424. Its `trigger.type` (`manual`/`api`/`webhook`/`scheduled`) is a complete, small enum. ⚠️ Its `taskType` enum is only 12 values (`copy, clone, lint, scan, merge, build, test, deliver, deploy, release, clean, other`) — extend it, but keep those spellings for the overlap. |
| **`buildDefinition` / `externalParameters` / `internalParameters` / `resolvedDependencies` / `builder` / `byproducts`** | invented provenance field names | SLSA provenance v1 is what every build platform already emits. |
| **`subject` / `predicate` / `predicateType` / `ResourceDescriptor`** | private attestation wrapper | in-toto v1.2 is the attestation lingua franca; SLSA, SPDX3, CycloneDX and gittuf all ride it. |
| **`Source Control System` / `Revision` / `Named Reference` / `Protected Named Reference` / `Trusted Robot` / `Continuity`** | forge-specific words | SLSA Source track (2025) is the newest and most CI-native forge vocabulary in existence, and `Trusted Robot` + `Continuity` are concepts nothing else names. |
| **`principal` (not "user email")** | keying identity off a commit email | **gittuf explicitly rejects git author/committer email as unreliable.** This also matches our own standing rule that email is not identity. |
| **VEX `status` and `justification` enums** | private status words | OpenVEX is CC0 and its four statuses / five justifications are already shared with CSAF and CycloneDX. |
| **`versionControlDetails {repositoryUri, revisionId, branch}` and `invocation {commandLine, exitCode, executionSuccessful, machine, account, environmentVariables}`** | private run/repo field names | SARIF 2.1.0 — every scanner in a CI pipeline already emits these. |
| **CICD-SEC-1..10** and **A03:2025** as risk labels; **T1195.001 / T1554 / T1552.007 / T1528 / T1072 / T1199** as technique labels; **CWE-nnnn** as weakness labels | private risk taxonomy | These are the labels a reviewer already knows. |
| **`OSPS-XX-NN`, `PO/PS/PW/RV`** as compliance-claim IDs | private control ids | Free crosswalks come with them. |

### Where the standards *disagree*, and what to do

- **"pipeline" vs "workflow".** CycloneDX says `workflow`; OSPS, OWASP, CIS, NIST and everyone in
  practice say *pipeline*. **Recommendation: use `pipeline` as the node name (it is what humans and
  agents will type) and carry `workflow` as the documented CycloneDX alias in the corpus.** This is
  the one place I would not follow the schema.
- **OSPS draws a line CycloneDX does not:** `CI/CD Pipeline` (generic) vs `Build and Release Pipeline`
  ("excludes some pipelines, such as pre-merge status checks"). **That line is real and we should carry
  it as a property, not two node types.**
- **Edge direction for containment.** SPDX says `contains` (from → to). CISA Framing deliberately
  reverses to `included in` — *and then says the choice does not matter as long as it is consistent.*
  **Recommendation: follow SPDX's stated naming rule** ("`from` (is) (a) `RELATIONSHIP` `to`") and use
  `contains`; record the CISA inverse in the corpus.
- **"SBOM lifecycle stage" has three names for one concept:** SPDX `SbomType`
  (`design/source/build/deployed/runtime/analyzed`), BSI §8.4
  (`Design/Source/Build/Analysed/Deployed/Runtime`), CISA 2026 `SBOM Generation Context`
  (`before build`/`build`/`after build`). **Recommendation: adopt SPDX's six-value enum** (it is the
  finest-grained and BSI matches it exactly), and map CISA's coarse three onto it.
- **`attestation` is overloaded.** in-toto/SLSA/SCITT mean *a signed claim about an artifact*; **OCSF
  means a tamper-evident event chain**. If we ever emit OCSF, qualify the name.
- **`agent` is overloaded.** OCSF `agent` means a security sensor; SPDX `Agent` means a person or
  organisation; everyone now also means "AI agent". **Avoid the bare word.**

### Where we are ahead of the standards (say so explicitly in the corpus)

Per the skill's Step 3: *"a concept the incidents demand but no standard names is the most valuable
thing you will find."* From this direction, the gaps are:

1. **No standard models the CI/CD graph as a graph.** OCSF has `graph`/`node`/`edge` but
   `edge.relation` is a **free string** with no controlled vocabulary. SARIF has a real graph but only
   inside a single analysis run. OmniBOR names an "Artifact Dependency Graph" but **has no normative
   definition for it and exactly one untyped edge**. CSA's `SecurityControlsCatalog` graphs *controls*,
   not pipelines. **Nobody has published node and edge kind lists for a CI/CD estate.**
2. **No standard names the *runner* as a first-class node with properties.** It appears as prose
   ("build worker", "execution node", "Runner Environment") but never as a typed entity with an
   identity that persists across runs — which is exactly what self-hosted-runner risk requires.
3. **No standard connects a permission grant to its *use*.** OWASP CICD-SEC-2/8 names the
   granted-vs-used gap in prose; no schema carries `last_used_at` on the grant.
4. **No standard models the pipeline-definition file's *trust position*** (in-repo vs
   protected-branch vs separate-repo vs CI-defined) as data — OWASP CICD-SEC-4 describes it in prose,
   and it is the single most load-bearing distinction in poisoned-pipeline-execution.
5. **`Continuity` (SLSA Source) is named once and by nobody else** — a control that was enforced *most
   of the time* is a different risk from one enforced continuously, and only SLSA says so.

⚠️ Items 2–5 are **single-source or zero-source**, which the skill says makes them *questions, not
answers*. They should be put to the adversarial/incident research direction before being modelled.

---

## 2.5 Update cadence and the polling seam

Per skill Step 9: record, don't build. **A ledger that opens a proposal — never auto-mutation.**

**Tier 1 — poll these; they are machine-readable, permissive, and move.**

| Source | Artifact URL | Format | Cadence | "What changed" signal |
|---|---|---|---|---|
| **OSPS Baseline** | `raw.githubusercontent.com/ossf/security-baseline/main/baseline/OSPS-{AC,BR,DO,GV,LE,QA,SA,VM}.yaml`, `lexicon.yaml`, `metadata.yaml`, `mappings/*.yaml` | YAML | date-versioned tags; ~2/yr | git tags `vYYYY.MM.DD` + commits under `baseline/`. **No GitHub Releases.** |
| **CycloneDX** | `raw.githubusercontent.com/CycloneDX/specification/master/schema/bom-1.<N>.schema.json` (+ `.xsd`, `.proto`) | JSON Schema | minor ~annual, patch between (1.7 2025-10-21, 1.7.1 2026-06-02) | tags on `CycloneDX/specification`; **diff the `enum` arrays** |
| **SPDX 3 model** | `raw.githubusercontent.com/spdx/spdx-3-model/main/model/Core/Vocabularies/RelationshipType.md`; `model/<Profile>/Classes/` dir listings | Markdown → JSON-LD/OWL/SHACL | 3.0 2024-04, 3.0.1 2024-12, **3.1-RC1 2026-01-24** | GitHub Releases on `spdx/spdx-spec`; **a new entry in `RelationshipType.md` is a vocabulary proposal for us** |
| **OCSF** | `schema.ocsf.io/api/versions`, `/api/objects`, `/api/classes`, `/api/dictionary`; repo `objects/*.json` | JSON + live API | **~3–4 months** (fastest here) | `CHANGELOG.md` with explicit **Deprecated** and **Breaking changes** sections; **`ocsf/ocsf-validate-compatibility` diffs two versions programmatically** |
| **OSV Schema** | `github.com/ossf/osv-schema` → `validation/schema.json`, `ecosystems.json` | JSON Schema | v1.9.0 2026-08-06; ~2–3/yr | `CHANGELOG.md` + Releases |
| **D3FEND** | `d3fend.mitre.org/ontologies/d3fend.ttl` / `.owl` / `.json`; versioned CSV `…/d3fend/1.5.0/d3fend.csv`; repo `d3fend/d3fend-ontology` | OWL / Turtle / JSON-LD / CSV | **~4 months** (1.0.0 2024-12 → 1.5.0 2026-08) | **git tags** (GitHub Releases are empty) + `d3fend.mitre.org/changelog/` |
| **MITRE ATT&CK** | `github.com/mitre-attack/attack-stix-data` → **`index.json`** (collection index), `{domain}/{domain}-{version}.json` | STIX 2.1 JSON | 2/yr + patches; **v19.2 2026-08-06** | `index.json` + `attack.mitre.org/resources/updates/` |
| **in-toto attestation** | `github.com/in-toto/attestation` → **`spec/predicates/` directory listing** | Markdown + proto | v1.2.0 2026-03-18; ~2–3/yr | Releases; **a new file in `spec/predicates/` is a new predicate type** |
| **Sigstore Fulcio** | `github.com/sigstore/fulcio/blob/main/docs/oid-info.md`; `sigstore/protobuf-specs/protos/*.proto` | Markdown registry + protobuf | Fulcio v1.8.8 2026-07-08; frequent | Releases |
| **Scorecard** | `api.scorecard.dev/projects/github.com/<o>/<r>`; BigQuery `openssf:scorecardcron.scorecard-v2_latest`; `docs/checks.md` | JSON API + BigQuery | v5.5.0 2026-04-23 | the response's own `scorecard.version` field; Releases; `docs/checks.md` diffs |
| **OpenVEX** | `raw.githubusercontent.com/openvex/spec/main/openvex_json_schema.json` | JSON Schema | **static since 2023-07-18** | tags |
| **SARIF** | `raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.2/schema/sarif.json` | JSON Schema | 2.1.0 frozen 2023; **2.2 in progress** | git history on `sarif-2.2/schema/`; `Future.md` |
| **PURL** | `github.com/package-url/purl-spec` → `purl-types-index.json` | JSON | v1.0.1 2026-08-03 | Releases. ⚠️ **ECMA-427 standardises syntax only — the ecosystem types live in the repo. Poll both.** |
| **CSA datasets** | `github.com/CloudSecurityAlliance-DataSets/…`; `github.com/CloudSecurityAlliance/SecurityControlsCatalog` | CSV/JSON; **STIX 2.1** | irregular | git commits. Note per-version metadata with SPDX licence + `known_source_issues` |
| **SP 800-53** | `github.com/usnistgov/oscal-content` → `nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json` | OSCAL JSON | rare (Rev 5 stable) | git commits |
| **Gemara** | `github.com/ossf/gemara` | Go/schema | **fast — v1.3.0 2026-06 → v1.5.0 2026-08** | Releases. **Pin a version.** |
| **Security Insights** | `raw.githubusercontent.com/ossf/security-insights-spec/main/spec/schema.cue` + `VERSION` | CUE | v2.2.0 2026-01-31; ~1–2/yr | Releases + `docs/versioning-policy.md` |
| **ATLAS** | `raw.githubusercontent.com/mitre-atlas/atlas-data/main/dist/v6/ATLAS-latest.yaml` | YAML | `YYYY.MM`; v2026.07 | **real GitHub Releases naming added/changed techniques** — the cleanest in the MITRE family |

**Tier 2 — no machine-readable artifact; poll the page or the tag.**

| Source | Signal | Cadence |
|---|---|---|
| **SLSA** | `/repos/slsa-framework/slsa/tags` (**Releases endpoint is empty**) + `slsa.dev/blog` + versioned doc tree | ~annual (1.0 2023 → 1.1 2025-04 → 1.2 2025-11) |
| **SSDF 800-218** | the **.xlsx table** + "potential updates" spreadsheets on the CSRC page | **No Rev 2 planned** — NIST's path is *Community Profiles*. Watch for profiles. |
| **SP 800-204D** | CSRC publication page, document history | ~annual for the 800-204 series |
| **CISA SBOM** | `cisa.gov/sbom` + the dated "Related Resources" list; `/sites/default/files/YYYY-MM/` path convention | 2021 → 2024 → 2026. ⚠️ **cisa.gov 403s WebFetch; use curl with a browser UA.** |
| **CIS Benchmarks** | **the embedded JSON blob on `cisecurity.org/cis-benchmarks`** with `benchmarkTitle`/`benchmarkVersion`/`published` — scrapable, no login | GitHub Benchmark ~annual (v1.2.0 2026-02-27) |
| **BSI TR-03183** | the PDF's own **Table 1 "Document History"**; the BSI page's per-part version numbers | Part 2 at v2.1.0 (2025-08-20) |
| **CAPEC** | News page changelog | **dormant — 3.9 since 2023-01-24** |
| **STIX 2.1** | commits on `oasis-open/cti-stix2-json-schemas`; OASIS directory listing | **glacial — no minor release since 2021** |
| **SCITT** | IETF datatracker WG page (RFC 9943 itself is frozen) | new — watch for companion docs |

**Tier 3 — do not poll.** S2C2F (dormant since 2022), OWASP SCVS (dormant since 2020), OWASP CI/CD
Top 10 (frozen since 2023-01), MITRE System of Trust (Word docs behind registration), CIS Guide text
(NC licence, no machine-readable form), ISO/IEC standards (paywalled), CSA Six Pillars (login-walled),
EU CRA text (EUR-Lex bot-challenges automated fetches).

**Two design notes for whoever builds the ledger.**
1. **The strongest form is grid data.** Several of these publish catalogues that could be *landed as
   nodes* — OSPS YAML (+ its ten crosswalks), the SPDX `RelationshipType` list, the CycloneDX enums,
   the D3FEND CSV, the ATT&CK `index.json`, SP 800-53's OSCAL JSON. Then "what changed in the standard"
   is a graph query with history rather than a diff someone remembers to run. Precedent: the FedRAMP
   KSI catalogue collector.
2. **Expect the crosswalks to lag.** OSPS's `metadata.yaml` — the best cross-standard index found —
   currently pins Scorecard at 5.0 (actual 5.5.0), SLSA at 1.0 (actual 1.2) and ATT&CK at v18 (actual
   v19.2). **Even the best-maintained map in the field is one to three versions stale.** Poll the
   sources, not the maps.

---

## 2.6 Known gaps and honest limits of this survey

- **Discovery was narrower than intended.** The session's WebSearch budget was exhausted at the first
  call, so everything here came from direct fetches of primary artifacts. That made the *facts*
  stronger (enums read out of schema files, versions from the GitHub API) but the *search* weaker —
  a dictionary nobody in this room already knew about could have been missed.
- **UNVERIFIED items, collected:** STIX 2.2 existence; MITRE SoT release date, category wording and
  licence; CIS GitHub/GitLab Benchmark entity lists (registration-walled); which CC licence the CIS
  Software Supply Chain Security Guide falls under; CSA CCM v4.1 control count; CSA Six Pillars names;
  ENISA Good Practices 2023 vocabulary; EU CRA Article 3 / Annex I & VII wording (EUR-Lex 202
  challenges); BSI TR-03183 reuse terms; ISO/IEC 5230, 18974, 19770-2 (SWID), IEC 62443-4-1, PCI DSS
  v4.0 Req 6; SCVS BOM Maturity Model; `sigstore/protobuf-specs` release tag; the D3FEND public SPARQL
  endpoint (**do not promise SPARQL**); OWASP Top 10:2025 exact release day; OWASP DevSecOps Guideline
  version number; EPSS licence terms.
- **Corrections to the brief, for the record:** ATT&CK's April 2026 release is **v19**, not v18 (now
  v19.2, 2026-08-06); Allstar is **not** sunset (v4.5, active); S2C2F has **25** requirements, not ~50;
  Scorecard v5.5.0 is **2026**; the OWASP CI/CD Top 10 has **no** revision (2022, not 2023, and frozen);
  the NTIA 2021 seven-field SBOM list is **superseded** by CISA's 17-field 2026 document; CIS has no
  "3.3 Trusted Package Registries" (registries are 4.3); SP 800-218A **does** add new task IDs;
  CycloneDX's `taskType` enum is 12 values, not the 20 a doc-summary claimed.
- **Bias to correct elsewhere.** This is the standards direction: it over-abstracts and lags. The
  ENISA taxonomy is five years old; CAPEC is three; SCVS and S2C2F are dormant; the OWASP CI/CD Top 10
  predates GitHub Actions OIDC and reusable workflows. **Read §2.3 against the adversarial/incident
  direction before freezing anything**, and treat §2.4's "where we are ahead" list as the specific
  place where the incident corpus should be asked to arbitrate.
- **This document is a dated artefact with a maintenance obligation.** Survey date **2026-08-27**.
  §2.5 is the seam that keeps it alive.
