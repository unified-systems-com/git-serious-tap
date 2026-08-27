---
title: The field's academic signal network — groups, professors, venues
date: 2026-08-27
status: research
audience:
  - developer
  - llm
related_docs:
  - docs/doc-git-serious-cicd-shape-review.md
  - docs/doc-git-serious-cicd-security-prior-art.md
---

> **Research pass, 2026-08-27.** Research centres, individual researchers, publication venues and machine-readable watch surfaces, with verification status recorded per claim.
> One of four gathering passes behind the domain vocabulary corpus, which lives with the
> vocabulary's owner as `spec-github-core-vocabulary.md`. Written by an AI research agent;
> claims carry citations and the report flags what it could not verify. Not canon.

# CI/CD & Software Supply Chain Security — Signal Network Map

**Research method and its limits (read this first — it determines how much to trust each row).**

WebSearch budget was exhausted at the start of this session (200/200 used), so **every item below was gathered by fetching primary sources directly** — faculty pages, lab sites, project governance files, the DBLP author/publication JSON APIs, GitHub's API, and conference sites. Nothing here comes from a search-result snippet.

Three systematic blind spots to hold in mind:

1. **Google Scholar is not fetchable.** Its search endpoint redirects every automated request to a Google login wall. Scholar `user=` IDs below were taken from researchers' *own websites* (reliable); where no such link existed, I have written "not verified — manual lookup required" rather than guessing.
2. **Several major sites block automated fetch with HTTP 403:** `usenix.org`, `blackhat.com`, `dl.acm.org`. Anything sourced from them is marked **UNVERIFIED-BY-FETCH**.
3. **DBLP affiliation records lag reality.** Confirmed concretely: DBLP still lists Georgios Gousios at TU Delft, but his own site records that he quit that post in March 2025. Use DBLP for *publications* (excellent, machine-readable) and personal/project sites for *affiliations*.

A fourth finding is structural and worth stating up front: **the personnel movement in this field was tracked accurately only by project governance files (in-toto's steering committee, updated 2026-07-06) and by GitHub API `company` fields — not by university pages, and not by TUF's own maintainer file, which is two years stale.** Machine-readable governance beat human-maintained rosters every time.

---

## PART A — Academic groups and professors

### A0. The organizing insight: two funded centers, not thirty individuals

Before the individual records, two multi-institution programs dominate this field. Following each as a *unit* is far more efficient than following its members separately.

**S3C2 — Secure Software Supply Chain Center (US).** NSF Secure and Trustworthy Cyberspace **Frontiers** award; grant numbers CNS-2207008, CNS-2206859, CNS-2206865, CNS-2206921. Binds NC State + CMU + George Washington + University of Maryland into one program with a shared publication stream.
- Site https://s3c2.org/ · People https://s3c2.org/people/ · Publications https://s3c2.org/pubs/
- **RSS: https://s3c2.org/feed.xml** ← the single highest-value feed in this entire map
- **PIs (verified on the people page):** Laurie Williams (NC State, lead), William Enck (NC State), Alexandros Kapravelos (NC State), Dominik Wermke (NC State), Christian Kästner (CMU), Adam Aviv (GWU), Michel Cukier (UMD). Affiliated faculty: Yasemin Acar. Leadership personnel: Patrick Morrison, Isabella White, Lindsey Schrott. 2 postdocs (Ranindya "Nanin" Paramitha at NC State; Matthias Fassl at GWU), 17 named grad students, 10 REU undergrads.
- Runs **twice-yearly Industry and Government Secure Supply Chain Summits**, published as citable reports — a direct channel into practitioner sentiment that has no equivalent elsewhere.
- **One feed covers seven PIs.** [VERIFIED by fetch]

**CHAINS (Sweden).** KTH research project scoped explicitly to "hardening the software supply chain, incl. dependency engineering as well as reproducible, executable and verifiable builds and SBOMs." Funded by the **Swedish Foundation for Strategic Research (SSF)**. Focus areas: Maven, npm, and cryptocurrency supply chains.
- Site https://chains.proj.kth.se/ (note: `/publications.html` **404s** — the publication list is not at the obvious path)
- **Four PIs:** Musard Balliu, Benoit Baudry, Mathias Ekstedt, Martin Monperrus. Team includes postdocs, **nine PhD students**, research engineers.
- Publishes into IEEE TSE, ACM CCS, USENIX Security, FSE.
- **This is the European counterpart to S3C2.** [VERIFIED by fetch]

---

### A1. NYU Secure Systems Lab lineage — TUF / in-toto / Uptane / gittuf

---

**Justin Cappos** — Professor, Computer Science & Engineering, NYU Tandon School of Engineering; also affiliated with NYU Center for Cybersecurity. Lab Director, **Secure Systems Laboratory (SSL)**. [VERIFIED — NYU faculty profile at https://engineering.nyu.edu/faculty/justin-cappos, corroborated independently by the lab's own people page listing him as "Professor and Lab Director"]

- **Signal:** Foundational secure-update and supply-chain architecture. He originates *frameworks that become standards* rather than measurement studies — TUF, in-toto, Uptane, and now gittuf all trace to this lab. Publishes at NDSS / EuroS&P / ACSAC / ISSRE.
- **Why it matters to CI/CD security concretely:** This lab produced the specifications that supply-chain tooling is actually built on. **gittuf** in particular is directly relevant to build observability — it enforces repository security policy *independently of the source-control platform*, meaning the policy survives a compromised or misconfigured forge. If you are reasoning about "can I trust what this repo says happened," this is the primary literature.
- **Follow:**
  - Lab: **https://ssl.engineering.nyu.edu/** (live; active 2026 roster of 2 postdocs + 5 PhD + 7 other students at /people)
  - Publications: https://ssl.engineering.nyu.edu/publications
  - Press/coverage: https://ssl.engineering.nyu.edu/press
  - **DBLP: https://dblp.org/pid/27/5136**
  - Semantic Scholar: https://www.semanticscholar.org/author/2030168 (106 papers, h-index 23) [VERIFIED via API]
  - Google Scholar: **not verified** — login wall. Manual: `scholar.google.com/citations?view_op=search_authors&mauthors=Justin+Cappos`
  - **Mastodon/X/Bluesky: none found. The lab has NO RSS feed and no social account.** ← **no machine-readable feed; DBLP is the only automatable surface**
- **Recent papers:**
  - *SourceFabric: Consistent and Scalable Security Policies for Git Repositories* — **IEEE EuroS&P 2026** (Yelgundhalli, Zielinski, Melara, Roellke, Curtmola, Cappos)
  - *Enhancing Legal Document Security and Accessibility with TAF* — **NDSS 2026** (Vaderna, Nikolic, Zielinski, Greisen, Ard, Cappos)
  - *Rethinking Trust in Forge-Based Git Security* (gittuf) — **NDSS 2025, Distinguished Paper Award** (Yelgundhalli, Zielinski, Curtmola, Cappos)
  - *CovSBOM: Enhancing Software Bill of Materials with Integrated Code Coverage Analysis* — **ISSRE 2024** (Zhao, Zhang, Chacko, Cappos)
  - *Securing Automotive Software Supply Chains* (Scudo) — **VehicleSec 2024** (Moore, Yelgundhalli, Cappos)
  - *Artemis: Defanging Software Supply Chain Attacks in Multi-repository Update Systems* — **ACSAC 2023** (Moore, Kuppusamy, Cappos)
  - *Towards verifiable web-based code review systems* — **Journal of Computer Security 31(2), 2023** (Afzali, Torres-Arias, Curtmola, Cappos) — evidence the NYU↔Purdue tie is ongoing collaboration, not just alumni history
- **Cadence:** ~2-4 supply-chain-relevant papers/year, consistently at top-tier security venues. Steady, not prolific.
- **Tier: CORE**

---

**Santiago Torres-Arias** — **Assistant** Professor, Electrical and Computer Engineering (ECE), Purdue University. **No named lab found.** [VERIFIED three independent ways: his personal site https://badhomb.re; his GitHub profile `company` field via API, updated 2026-07-22; DBLP's affiliation tag "Purdue University, West Lafayette, IN, USA"]

- **On the missing lab:** guessed domains (purseclab.org, polyseclab.org, torresariaslab.com) do not resolve; `engineering.purdue.edu/~santiagotorres/` **404s**; his site has no `/group/` or `/people/` page. His site does say he is "currently looking for motivated students," so the group is active but appears to be informally named. **Use DBLP as the watch surface, not an institutional page.**
- **Signal:** Software signing, provenance, zero-trust dependencies, SBOM integration. **He is the single most consistently on-topic author in the field** — nearly every paper is squarely supply chain, with essentially no off-topic drift. Also a SCORED chair in both 2024 and 2025.
- **Why it matters to CI/CD security concretely:** His work is the empirical base for *whether signing actually works in practice* — adoption rates across public registries, why developers do or don't sign, and what tooling friction blocks it. If your product surfaces provenance or attestation, this is the literature that tells you what fraction of the ecosystem will have anything to show you. *ZTD_JAVA* is a directly implementable dependency-confinement design.
- **Follow:**
  - Personal site: **https://badhomb.re**
  - **DBLP: https://dblp.org/pid/185/1711** (48 publications listed 2024-2026)
  - Semantic Scholar: https://www.semanticscholar.org/author/2261287820 (28 papers, h-index 9) — **note: disambiguation is imperfect, multiple entries exist for this name**
  - GitHub: https://github.com/santiagotorres (129 repos, active 2026-07-22)
  - X: **@TorresAriasS** — https://twitter.com/torresariass (presence confirmed via his GitHub profile field; content not independently verified, X requires auth to fetch)
  - Google Scholar: **not verified** — login wall
  - **No blog, no RSS.** DBLP is the machine-readable surface.
- **Recent papers:**
  - *SoK: A Defense-Oriented Evaluation of Software Supply Chain Security* — **IEEE EuroS&P 2026**
  - *Establishing Provenance Before Coding: Traditional and Next-Generation Software Signing* — **IEEE Security & Privacy magazine 23(2), 2025**
  - *ZTD_JAVA: Mitigating Software Supply Chain Vulnerabilities via Zero-Trust Dependencies* — **ICSE 2025**
  - *An Industry Interview Study of Software Signing for Supply Chain Security* — **USENIX Security 2025**
  - *Signing in Four Public Software Package Registries: Quantity, Quality, and Influencing Factors* — **IEEE S&P 2024**
  - *Rust for Embedded Systems: Current State and Open Problems* — **ACM CCS 2024**
  - *A Study of Malware Prevention in Linux Distributions* — CoRR 2024
  - *Why Johnny Signs with Sigstore: Examining Tooling as a Factor in Software Signing Adoption in the Sigstore Ecosystem* — CoRR 2025
  - *Software Dark Matter: Gazing at Uncharted Files to Navigate SBOM Integrations* — CoRR 2026
  - *ARMS: A Vision for Actor Reputation Metric Systems in the Open-Source Software Supply Chain* — CoRR 2025
  - *Trustworthy and Confidential SBOM Exchange* — CoRR 2026
- **Cadence:** **Very high** — ~5+ substantive venue papers/year plus numerous arXiv preprints; the most prolific in this lineage.
- **Tier: CORE**

---

**Aditya Sirish A Yelgundhalli** — **Bloomberg (industry)**. [VERIFIED — listed explicitly as "Bloomberg (industry)" in the in-toto Steering Committee file, https://github.com/in-toto/community/blob/main/STEERING-COMMITTEE.md, **last commit 2026-07-06**]

- **Important correction to any earlier read of this space:** he is *not* an academic. He is first author on the two strongest recent NYU-lineage papers and sits on in-toto's steering committee, but his affiliation is industry. He is a **bridge node** — industry practitioner still publishing at NDSS/EuroS&P with NYU.
- **Signal:** Git-native security policy, forge-independent trust, repository integrity. First author of **gittuf**.
- **Why it matters to CI/CD security concretely:** gittuf and SourceFabric are the most directly applicable work in this entire map for anyone building repo/CI observability. The core thesis — that you cannot trust the forge to tell you the truth about its own history, so policy must be independently verifiable — is exactly the threat model a CI/CD observability product exists to address.
- **Follow:** in-toto steering committee file (above) · gittuf project https://gittuf.dev/ · **no personal site, DBLP PID, or social account verified** — **named gap**
- **Recent papers:** *SourceFabric* (EuroS&P 2026, first author); *Rethinking Trust in Forge-Based Git Security* (**NDSS 2025, Distinguished Paper**, first author); *Securing Automotive Software Supply Chains* / Scudo (VehicleSec 2024); SCORED '25 chair.
- **Cadence:** ~2/year, but exceptionally high-impact per paper.
- **Tier: CORE** (as a research signal; classify as industry, not academic)

---

**Marina Moore** — **Edera**, engineering role. **Title unconfirmed.** [VERIFIED employer via GitHub API `company` field = "Edera", profile updated 2026-07-06; corroborated by a 2025 co-authored paper with Edera's CTO]

- **Naming trap worth recording:** the company is **https://edera.dev** — a container-native isolation/hypervisor security startup. **NOT edera.com**, which is an unrelated healthcare company.
- She is **not** on Edera's public leadership page (https://edera.dev/about lists Emily Long CEO, Alex Zenla CTO, Ariadne Conill, Kaylin Trychon, Kavi Daula, Jed Salazar), implying an individual-contributor engineering role.
- **Signal:** Formerly TUF/Uptane specification work; **now hypervisor and VM isolation, not supply chain.** Her only Edera-era publication is *Goldilocks Isolation: High Performance VMs with Edera* (arXiv 2501.04580, 2025, with CTO Alex Zenla).
- **Why it matters to CI/CD security concretely:** Historically significant — she co-authored Artemis and the Uptane/multi-repository update work that underpins how update systems resist compromise. **Forward-looking relevance is now low**; her professional centre of gravity has moved.
- **Follow:** **DBLP: https://dblp.org/pid/236/5493** · GitHub https://github.com/mnm678 (pinned repos still include theupdateframework/specification, python-tuf, taps, uptane-standard, cncf/tag-security — continued but lighter involvement) · personal site attempted at mnm678.github.io — **404s** · Google Scholar not found
- **Cadence:** Sparse — one preprint in the 2023-2026 window outside her 2023 NYU-era paper.
- **Tier: PERIODIC** — check quarterly for any supply-chain output; do not expect much.

---

**Trishank Karthik Kuppusamy** — **CURRENT EMPLOYER UNKNOWN.** Last confirmed at Datadog through ~September 2025. [UNVERIFIED — and the negative evidence is strong]

- **The evidence trail:** GitHub handle is literally `trishankatdatadog`, but the bio reads **"Should be inactive after Sep 19th 2025"**; the account's `updated_at` timestamp is frozen at **2025-09-19T18:23:56Z**; the `company` field is **`null`**; and he belongs to **zero public GitHub organizations** (`gh api users/trishankatdatadog/orgs` → `[]`). No personal site, no active social account, no updated affiliation on DBLP or Semantic Scholar.
- **One signal of life:** a non-fork repo `private-sigstore`, pushed **2026-01-26**, no description — suggestive of continued Sigstore/supply-chain work somewhere, but not evidence of an employer.
- **Do not record him as "Datadog."** Treat as unknown.
- **Signal:** Historically a principal TUF/Uptane author. **Zero publications 2024-2026.**
- **Why it matters:** Historical only. Foundational to TUF's design; no current research signal.
- **Follow:** **DBLP: https://dblp.org/pid/44/8573** · GitHub https://github.com/trishankatdatadog (dormant since Sep 2025). Worth a manual LinkedIn check — automated tools cannot reach it.
- **Cadence:** Effectively zero.
- **Tier: CONTEXT**

---

**Marcela Melara** — **affiliation UNVERIFIED** (widely understood to be Intel Labs; **I did not confirm this from any primary source in this research**). **This is a real gap — she is a recurring, high-signal name.**

- **Signal:** Build environment integrity, CI/CD platform auditing, transparency infrastructure. SCORED '23 chair; co-author on SourceFabric (EuroS&P 2026).
- **Why it matters to CI/CD security concretely:** Her SCORED 2024 paper *Auditing the CI/CD Platform: Reproducible Builds vs. Hardware-Attested Build Environments* frames the exact architectural choice a CI/CD-integrity product has to make — reproduce the build to verify it, or attest the environment that produced it. That is the central design fork in this space.
- **Follow:** dblp record for the SCORED paper: https://dblp.org/rec/conf/scored/MelaraK24 · **no verified personal site, DBLP PID, or social account — named gap**
- **Recent papers:** *Auditing the CI/CD Platform: Reproducible Builds vs. Hardware-Attested Build Environments* — **SCORED 2024**; *SourceFabric* — **EuroS&P 2026**; SCORED '23 chair (https://dblp.org/rec/conf/ccs/MelaraTS23)
- **Cadence:** unverified.
- **Tier: CORE by topic relevance — but requires a verification pass before you can follow her.**

---

**Patrick Zielinski** — NYU SSL (inferred from co-authorship pattern; **affiliation UNVERIFIED**). Co-author on SourceFabric (2026), TAF (2026), gittuf (2025). Recurring across the 2025-2026 NYU output. **Tier: context** — watch as a rising name.

**Reza Curtmola** — **NJIT** (inferred from long-running collaboration; **affiliation UNVERIFIED in this pass**). Co-author on SourceFabric, gittuf, and the 2023 verifiable-code-review paper. Consistent NYU collaborator over many years. **Tier: context.**

---

### A2. Project governance — verified live 2026-08-27

This table matters because **governance files tracked personnel movement more accurately than any university page.**

| Project | URL | Governance home | Status of maintainer info |
|---|---|---|---|
| **TUF** | https://theupdateframework.io/ | **CNCF graduated** | ⚠️ **STALE — do not trust.** MAINTAINERS.md (https://github.com/theupdateframework/community/blob/main/MAINTAINERS.md) **last touched 2024-03-27**, lists Cappos, Kuppusamy, Kjell, Joshua Lock, Moore, Lukas Pühringer — including two people the per-person evidence shows have moved on. GitHub org self-describes as "based at NYU Tandon School of Engineering" |
| **in-toto** | https://in-toto.io/ | **CNCF graduated** | ✅ **FRESH — the best governance snapshot found anywhere.** STEERING-COMMITTEE.md last commit **2026-07-06**: Santiago Torres-Arias (Purdue, academia), Justin Cappos (NYU, academia), Aditya Sirish A Yelgundhalli (**Bloomberg**, industry), Jack Kelly (**ControlPlane**, industry), John Kjell (**ControlPlane**, industry). Note **ControlPlane holds 2 of 5 seats** — a consultancy worth knowing about |
| **Uptane** | https://uptane.org/ | **Linux Foundation Joint Development Foundation (JDF), "Uptane Series."** Originated as IEEE-ISTO standard 6100.1.0.0 (released 2019-07-31) | Current spec **v2.1.0, dated 2023-06-27** — has not moved in ~3 years. Governance process documented at https://github.com/uptane/uptane-standard/blob/main/governance/05-governance.md (JDF + Community Specification process); **no named individual roster published** |
| **gittuf** | https://gittuf.dev/ | **OpenSSF incubating**, Supply Chain Integrity Working Group, under LF Projects LLC | Cited authors: Yelgundhalli, Zielinski, Curtmola, Cappos. Peer-reviewed at NDSS 2025. Covered by LWN.net (2024-05-08) and the OpenSSF blog (2024-01-18) |
| **Sigstore** | https://www.sigstore.dev/ | ⚠️ **UNVERIFIED** | The site is a JavaScript SPA that returns only "Loading…" to automated fetch. Governance not confirmable this session |

---

### A3. NC State — the largest single concentration of supply-chain researchers

---

**Laurie Williams** — **Goodnight Distinguished University Professor in Security Sciences**, Department of Computer Science, NC State University. **Co-director, NC State Secure Computing Institute** (https://sci.ncsu.edu); **co-director, NC State Science of Security Lablet**; **lead PI of S3C2**. IEEE Fellow (2018), ACM Distinguished Scientist (2011), NSF CAREER (2004). 260+ refereed publications. [VERIFIED — NC State department profile https://www.csc.ncsu.edu/people/lawilli3, plus her own site https://lauriew.github.io/]

- **Signal:** The broadest and most authoritative output in the field — SBOM policy, attestation, supply-chain task adoption by organisations, malicious package detection, build-script quality. She writes the *survey and synthesis* papers that define the research agenda.
- **Why it matters to CI/CD security concretely:** *Research Directions in Software Supply Chain Security* (TOSEM 2025) is the field's map, written by 15 authors spanning all of S3C2 — it is the single best orientation document in existence. Her *Top Five Challenges* and *Establishing a Baseline of Supply Chain Security Task Adoption* papers are drawn from interviews with 30+ real industry and government organisations, i.e. they tell you what practitioners actually do and fail to do — directly relevant to product positioning, not just engineering.
- **Follow:** https://lauriew.github.io/ · https://www.csc.ncsu.edu/people/lawilli3 · **S3C2 RSS https://s3c2.org/feed.xml** (the right instrument — it captures her and six other PIs) · Google Scholar / DBLP: **not verified** — no links surfaced on the pages fetched · no personal blog or social account found
- **Recent papers:**
  - *Research Directions in Software Supply Chain Security* — **ACM TOSEM, Jan 2025** (Williams, Benedetti, Hamer, Paramitha, Rahman, Tamanna, Tystahl, Zahan, Morrison, Acar, Cukier, Kästner, Kapravelos, Wermke, Enck)
  - *Closing the Chain: How to reduce your risk of being SolarWinds, Log4j, or XZ Utils* — **ICSE 2026** (Hamer, Bowen, Haque, Hines, Madden, Williams)
  - *Which Is Better For Reducing Outdated And Vulnerable Dependencies: Pinning Or Floating?* — **ASE 2025** (Rahman, Marley, Enck, Williams)
  - *Your Build Scripts Stink: The State of Code Smells in Build Scripts* — **ASE 2025** (Tamanna, Chandrani, Burrows, Wroblewski, Williams, Wermke)
  - *Leveraging Large Language Models to Detect npm Malicious Packages* — **ICSE 2025** (Zahan, Hong, Burckhardt, Aboukhadijeh, Williams)
  - *Establishing a Baseline of Software Supply Chain Security Task Adoption by Software Organizations* — **SCORED 2025** (Williams, Migues) — https://dblp.org/rec/conf/scored/WilliamsM25
  - *Aggregating Security Measures from the Dependency Tree* — **SCORED 2025** (Elder, Klevans, Paramitha, d'Amorim, Williams) — https://dblp.org/rec/conf/scored/ElderKPdW25
  - *Can the Rising Tide of Software Supply Chain Attacks Raise All Software Engineering Boats?* — **FSE Companion 2025 (keynote)**
  - *Trusting code in the wild: Exploring contributor reputation measures to review dependencies in the Rust ecosystem* — **IEEE TSE 2025**
  - *Software Bills of Materials Are Required. Are We There Yet?* — **IEEE S&P Magazine, Mar 2023**
  - *Top Five Challenges in Software Supply Chain Security: Observations From 30 Industry and Government Organizations* — **IEEE S&P Magazine, Mar 2022 (best paper)**
- **Cadence:** Very high — 8-12 supply-chain-relevant items/year across venues and magazines.
- **Tier: CORE** — arguably the highest-value single person in the map.

---

**William Enck** — **Goodnight Distinguished Professor in Security Sciences**, Department of Computer Science, NC State. **Director, Wolfpack Security and Privacy Research (WSPR) Laboratory** (https://wspr.csc.ncsu.edu); co-director Secure Computing Institute; S3C2 PI. [VERIFIED — his own site https://www.enck.org/]

- **Signal:** Systems-security rigour applied to supply chain — static analysis of CI workflows, software composition analysis in practice, reproducible packaging, IDE/extension security.
- **Why it matters to CI/CD security concretely:** **Cosseter (IEEE S&P 2026) is the most directly actionable CI/CD-security paper found in this entire research pass** — demand-driven static analysis to automatically reduce GitHub Actions permissions. If you are building CI/CD observability, over-permissioned workflows are a primary finding class, and this is the state of the art for detecting them. His SCA interview study (USENIX Security 2025) tells you why developers ignore composition-analysis output — essential if your product generates findings.
- **Follow:** **https://www.enck.org/** · publications **https://www.enck.org/pubs/** · WSPR lab **https://wspr.csc.ncsu.edu** · S3C2 RSS · Google Scholar / DBLP / social: **not verified** — no links surfaced on the pages fetched
- **Recent papers:**
  - *Cosseter: GitHub Actions Permission Reduction Using Demand-Driven Static Analysis* — **IEEE S&P 2026** (Tystahl, Ghebremichael, Muralee, Cherupattamoolayil, Bianchi, Machiry, Kapravelos, Enck)
  - *Context Matters: Qualitative Insights into Developers' Approaches and Challenges with Software Composition Analysis* — **USENIX Security 2025** (Lin, Gowda, Enck, Wermke)
  - *An Empirical Study on Reproducible Packaging in Open-Source Ecosystems* — **ICSE 2025** (Benedetti, Solarin, Miller, Tystahl, Enck, Kästner, Kapravelos, Merlo, Verderame)
  - *Which Is Better For Reducing Outdated And Vulnerable Dependencies: Pinning Or Floating?* — **ASE 2025**
  - *ASN1spect: Uncovering ASN.1 Compiler-Generated Vulnerabilities in Critical Infrastructure* — **ACM SecDev 2026**
  - *Research Directions in Software Supply Chain Security* — **TOSEM 2025** (co-author)
- **Cadence:** ~4-6 relevant papers/year.
- **Tier: CORE**

---

**Dominik Wermke** — NC State, **S3C2 PI**. [VERIFIED as an S3C2 PI on the people page; title/rank not independently confirmed. Personal site `wermke.dev` **does not resolve** — DNS failure]

- **Signal:** Usable-security methods applied to supply chain — interview and qualitative studies of how developers actually handle trust, attribution, and tooling.
- **Why it matters to CI/CD security concretely:** *Attributing Open-Source Contributions is Critical but Difficult* (NDSS 2025) is a systematic analysis of GitHub practices and their supply-chain impact — directly relevant if your product attributes changes to actors. *UntrustIDE* (NDSS 2024, Distinguished Paper) covers VS Code extension weaknesses, an under-covered developer-endpoint attack surface.
- **Follow:** S3C2 RSS (his primary discoverable surface) · **no personal site (DNS fails), no verified DBLP/Scholar/social — named gap**
- **Recent papers:**
  - *Attributing Open-Source Contributions is Critical but Difficult: A Systematic Analysis of GitHub Practices and Their Impact on Software Supply Chain Security* — **NDSS 2025** (Holtgrave, Friedrich, Fischer, Huaman, Busch, Klemmer, Fourné, Wiese, Wermke, Fahl)
  - *UntrustIDE: Exploiting Weaknesses in VS Code Extensions* — **NDSS 2024, Distinguished Paper**
  - *Context Matters* — **USENIX Security 2025**; *Your Build Scripts Stink* — **ASE 2025**
- **Cadence:** ~3-4/year. Rising.
- **Tier: PERIODIC** (trending toward core)

---

**Alexandros Kapravelos** — NC State, **S3C2 PI**. [VERIFIED as PI on the S3C2 people page; title not independently confirmed]

- **Signal:** Web/systems security applied to ecosystem abuse — fake stars, malicious packages, reproducible packaging, workflow analysis.
- **Why it matters to CI/CD security concretely:** *Six Million (Suspected) Fake Stars on GitHub* (ICSE 2026) is an ecosystem-integrity result with immediate product implications — it demonstrates that GitHub popularity signals are systematically gamed and correlate with malware distribution. Any product using stars/popularity as a trust heuristic should read it.
- **Follow:** S3C2 RSS · **no personal site, DBLP, or social verified — named gap**
- **Recent papers:** *Cosseter* (**IEEE S&P 2026**); *Six Million (Suspected) Fake Stars on GitHub* (**ICSE 2026**); *An Empirical Study on Reproducible Packaging* (**ICSE 2025**); *Towards Verifiably Safe Tool Use for LLM Agents* (**ICSE-NIER 2026**)
- **Cadence:** ~3-4/year.
- **Tier: PERIODIC**

---

**Yasemin Acar** — **BOTH affiliations current and self-described:** "Professor in Computer Science at **Paderborn University**, Germany" AND "Research Assistant Professor at **The George Washington University**", Washington DC. S3C2 affiliated faculty. [VERIFIED — her own site https://yaseminacar.de/ lists both as current; DBLP also lists both]

- **Honest caveat on relevance:** her *own* listed 2024 output is four USENIX Security 2024 papers on **usable security and privacy — not supply chain** (digital security in relative poverty; software creators' perspectives on unintended consequences; recovery codes for E2E-encrypted services; bringing cryptography from papers to products). **Her supply-chain relevance is real but arrives through S3C2 co-authorship** (TOSEM 2025, the summit reports), not through her own research programme.
- **Why it matters to CI/CD security concretely:** She supplies the *human factors* methodology to the S3C2 programme. If you care why security tooling gets ignored — which is the central adoption problem for any CI/CD security product — her methods are the ones producing those answers.
- **Follow:** **https://yaseminacar.de/** · **Google Scholar: https://scholar.google.de/citations?user=cdFkUdcAAAAJ&hl=de** (one of the few Scholar URLs verified, because her own site links it) · S3C2 RSS · `acar-lab.org` **does not resolve** · **no DBLP/Mastodon/Bluesky/X link on her site**
- **Cadence:** High overall (~4-6/year), but only a fraction is supply-chain.
- **Tier: PERIODIC**

---

**Michel Cukier** — University of Maryland, **S3C2 PI**. [VERIFIED as PI on the S3C2 people page; title, department, and personal page **not verified**]

- **This resolves an open question:** he *is* genuinely in scope — but **as an S3C2 PI, not through his own supply-chain publication record.** He appears as a co-author on the S3C2 summit reports and the TOSEM survey. I found no independent supply-chain research programme under his name.
- **Follow:** S3C2 people page and RSS only. **No personal site, DBLP, or Scholar verified — named gap.**
- **Cadence:** Low as a distinct signal.
- **Tier: CONTEXT**

---

**Adam Aviv** — George Washington University, **S3C2 PI**. [VERIFIED as PI on the S3C2 people page only; nothing else verified]
- **Signal/relevance:** Not independently established in this pass; known primarily for authentication and usable-security work. **Named gap.**
- **Tier: CONTEXT**

---

**Trevor Dunlap** — **PhD complete; now at Chainguard.** [VERIFIED — listed under Alumni on the S3C2 people page]
- **Signal:** Dependency and vulnerability research during his PhD; now at a commercial supply-chain-security vendor.
- **Why it matters:** Not a research signal any more, but a **useful industry contact** — Chainguard is a direct player in this market.
- **Tier: CONTEXT**

**Igibek Koishybayev** — **PhD complete; now at Qualcomm.** [VERIFIED — S3C2 alumni list]
- **Note:** he was lead author on **ARGUS** (USENIX Security 2023), the staged static-taint-analysis framework for GitHub workflows and Actions that the original research brief asked about. **The ARGUS lineage traces to NC State/S3C2, and its lead author has left academia for industry.**
- **Tier: CONTEXT**

---

**Other NC State / S3C2 names appearing repeatedly in the author lists** (all **UNVERIFIED** as individuals, listed so they are not invisible): Sivana Hamer, Nusrat Zahan, Mahzabin Tamanna, Md Rayhanur Rahman, Chris Tystahl, Ranindya Paramitha (postdoc), Patrick Morrison, Matt Elder, Yu Lin, Courtney Miller (CMU), Marcelo d'Amorim.

---

### A4. Carnegie Mellon University

---

**Christian Kästner** — **Associate Professor, Software and Societal Systems Department (S3D)**, School of Computer Science, Carnegie Mellon University. **S3C2 PI.** [VERIFIED — his own page https://www.cs.cmu.edu/~ckaestne/. **Explicitly checked for a rumoured institutional move: no mention of relocating; he is still at CMU.** Note the department was renamed — it is S3D now, formerly the Institute for Software Research]

- **Signal:** Package ecosystems, dependency dynamics, build systems, open-source sustainability, and increasingly ML/AI engineering. Wins Distinguished Paper awards regularly (FSE 2025, ICSE 2025).
- **Why it matters to CI/CD security concretely:** ***Pinning Is Futile: You Need More Than Local Dependency Versioning to Defend Against Supply Chain Attacks* (FSE 2025) is directly load-bearing for anyone whose product recommends or relies on dependency pinning.** It is an empirical demonstration that local pinning does not deliver the protection commonly assumed. His dependency-abandonment work (ICSE 2025) addresses a risk class most tooling ignores entirely — a dependency that is *maintained by nobody* rather than *known-vulnerable*.
- **Follow:**
  - **https://www.cs.cmu.edu/~ckaestne/**
  - **Google Scholar: https://scholar.google.com/citations?user=PR-ZnJUAAAAJ** (verified via his own site)
  - **Blog: https://ckaestne.medium.com** ← one of the few genuine blog/RSS surfaces in this map
  - GitHub: https://github.com/ckaestne
  - S3C2 RSS
  - **Mastodon/X: not verified**
- **Recent papers:**
  - *Six Million (Suspected) Fake Stars on GitHub: A Growing Spiral of Popularity Contests, Spam, and Malware* — **ICSE 2026** (He, Yang, Burckhardt, Kapravelos, Vasilescu, Kästner)
  - *Designing Abandabot: When Does Open Source Dependency Abandonment Matter?* — **ICSE 2026** (Miller, He, Chen, Lin, Yang, Vasilescu, Kästner)
  - *Pinning Is Futile: You Need More Than Local Dependency Versioning to Defend Against Supply Chain Attacks* — **FSE 2025, Distinguished Paper** (He, Vasilescu, Kästner)
  - *Understanding the Response to Open-Source Dependency Abandonment in the npm Ecosystem* — **ICSE 2025, Distinguished Paper** (Miller, Jahanshahi, Mockus, Vasilescu, Kästner)
  - *An Empirical Study on Reproducible Packaging in Open-Source Ecosystems* — **ICSE 2025**
  - *Towards Verifiably Safe Tool Use for LLM Agents* — **ICSE-NIER 2026**
  - *We Feel Like We're Winging It* (dependency abandonment) — **ESEC/FSE 2023**
  - *Containing Malicious Package Updates in npm with a Lightweight Permission System* — **ICSE 2021** (still the reference work on npm package permissions)
- **Cadence:** High — ~4-6 relevant papers/year, disproportionately award-winning.
- **Tier: CORE**

---

**Bogdan Vasilescu** — **Associate Professor, Software and Societal Systems Department (S3D)**, CMU SCS. Leads **STRUDEL** (Socio-Technical Research Using Data Excavation Lab). [VERIFIED — his own page https://bvasiles.github.io/ and the lab site]

- **Signal:** Empirical/MSR-style work on software ecosystems, open-source sustainability, CI adoption, developer behaviour at scale. The lab's stated question is "How can we empower distributed teams to develop software effectively and productively?" Projects include open-source sustainability, diversity, **BugSwarm**, and **continuous integration studies**.
- **Why it matters to CI/CD security concretely:** He supplies the large-scale data methodology behind the Kästner supply-chain papers. His lab's CI studies and BugSwarm dataset work are relevant infrastructure if you need empirical baselines for CI behaviour.
- **Follow:**
  - **https://bvasiles.github.io/**
  - Lab: **https://cmustrudel.github.io** (publications at /publications/)
  - **Google Scholar: https://scholar.google.com/citations?user=bcXjlqYAAAAJ&hl=en** (verified via his own site)
  - **DBLP: http://dblp.uni-trier.de/pers/hd/v/Vasilescu:Bogdan** (verified via his own site)
  - **X: https://twitter.com/b_vasilescu**
  - GitHub: https://github.com/bvasiles
  - **No lab RSS found.**
- **Recent papers:** Co-author on *Six Million Fake Stars* (ICSE 2026), *Designing Abandabot* (ICSE 2026), *Pinning Is Futile* (FSE 2025), *npm dependency abandonment* (ICSE 2025).
- **Cadence:** High overall; supply-chain subset ~3-4/year, mostly via Kästner collaborations.
- **Tier: PERIODIC**

---

**Courtney Miller** — CMU (PhD student, Kästner/Vasilescu group; **UNVERIFIED** as an individual). First author on the dependency-abandonment line (*Understanding the Response to Open-Source Dependency Abandonment*, ICSE 2025 Distinguished Paper; *We Feel Like We're Winging It*, ESEC/FSE 2023) and Abandabot. **Tier: context** — a rising name to watch.

---

**CMU Software Engineering Institute (SEI)** — ⚠️ **NOT VERIFIED. This is the single largest unresolved gap in Part A.**

- `insights.sei.cmu.edu/topics/supply-chain-risk-management/` **301-redirects** to `www.sei.cmu.edu/topics/supply-chain-risk-management/`, which **404s.**
- I could **not** confirm: the current SEI supply-chain team; whether **Sam Weber** is at SEI, NYU, or elsewhere; the status of the Acquisition Security Framework work; or whether **Carol Woody, Charles Wallen, Michael Bandor, or Brett Tucker** are current. A working blog/RSS URL was not established.
- **Judgment:** CMU's live *academic* signal runs through Kästner and S3C2. SEI is at best **tier: CONTEXT** until someone confirms a working landing page. Given that its topic page 404s, it is plausible the programme has been reorganised.
- **Tier: CONTEXT — pending verification**

---

### A5. Europe

---

**Martin Monperrus** — **Professor of Software Technology, KTH Royal Institute of Technology**, Stockholm. **CHAINS PI.** [VERIFIED — https://www.monperrus.net/martin/]

- **Signal:** The broadest European output — build reproducibility, dependency bots, supply-chain smells, SBOM, software diversity, and increasingly AI/coding agents. **Extremely high volume.**
- **Why it matters to CI/CD security concretely:** *Causes and Canonicalization of Unreproducible Builds in Java* (IEEE TSE 2025) is the most detailed treatment of **why builds fail to reproduce and what can be normalised away** — essential reading if your product asserts anything about build integrity. *Dirty-Waters* (FSE 2025) is a shipped tool for detecting supply-chain smells. *Maven-Lockfile* addresses high-integrity rebuilds of past releases. And *Trusting-Trust Attack against an Entire Linux Distribution through Binary Manipulation* (July 2026) is a live demonstration of the deepest class of build-chain compromise.
- **Follow:**
  - **https://www.monperrus.net/martin/**
  - **Google Scholar: https://scholar.google.com/citations?user=dJQf4SYAAAAJ** (verified via his own site)
  - ⭐ **Custom RSS feed: https://www.monperrus.net/martin/dblp-rss.py?search=author:martin_monperrus** — a genuine machine-readable per-author feed, rare in this map
  - ⭐ **arXiv author page: https://arxiv.org/a/monperrus_m_1** — **157 papers**, verified live
  - LinkedIn: https://www.linkedin.com/in/martin-monperrus-369300a4/
  - CHAINS: https://chains.proj.kth.se/
  - **No Mastodon/Bluesky/X link found on his site.**
- **Recent papers:**
  - *Causes and Canonicalization of Unreproducible Builds in Java* — **IEEE Transactions on Software Engineering, 2025**
  - *Dirty-Waters: Detecting Software Supply Chain Smells* — **FSE 2025 (Tool Track)**
  - *Maven-Hijack: Software Supply Chain Attack Exploiting Packaging Order* — **SCORED 2025** — https://dblp.org/rec/conf/scored/ReyesBSBM25
  - *Software Bills of Materials in Maven Central* — **MSR 2025**
  - *Software Supply Chain Security of Web3* — **APSEC 2025**
  - *GoSurf: Identifying Software Supply Chain Attack Vectors in Go* — **SCORED 2024** — https://dblp.org/rec/conf/scored/CesaranoANM24
  - *BUMP: A Benchmark of Reproducible Breaking Dependency Updates* — **SANER 2024**
  - *BinEq — A Benchmark of Compiled Java Programs to Assess Alternative Builds* — **SCORED 2024** — https://dblp.org/rec/conf/scored/0001WAWH24
  - *Software Bill of Materials in Java* — **SCORED 2023** — https://dblp.org/rec/conf/scored/BalliuBBEMRSSSW23
  - *The Design Space of Lockfiles Across Package Managers* — **Empirical Software Engineering, 2026**
  - *Byam: Fixing Breaking Dependency Updates with Large Language Models* — **Empirical Software Engineering 31, 2026**
  - Preprints 2026: *Software Supply Chain Smells* (2603.24282), *FIKA: Expanding Dependency Reachability with Executability Guarantees* (2604.20015), *The Grand Software Supply Chain of AI Systems* (2604.27781), *zkSBOM: Privacy-Preserving SBOM Sharing with Zero-Knowledge Sets* (2605.00076), *Trusting-Trust Attack against an Entire Linux Distribution* (2607.24888), *Dependencies that Bundle Code and Execution* (2607.02618), *Maven-Lockfile* (2510.00730), *GoLeash: Mitigating Golang Supply Chain Attacks with Runtime Policy Enforcement* (2505.11016)
- **Cadence:** **Extreme.** 157 arXiv papers total; multiple new preprints per month. **Use the RSS feed — manual checking will not keep up.**
- **Tier: CORE**

---

**Benoit Baudry** — **Université de Montréal** (Canada). Also a **CHAINS PI at KTH** — he is a bridge, not a clean departure. [VERIFIED — DBLP author record lists affiliations in order: **Université de Montréal, Canada**; KTH; University of Rennes 1; INRIA. The move from KTH to Montréal is confirmed]

- **Signal:** Software diversity, dependency debloating, SBOM, build integrity — long-running collaboration with Monperrus.
- **Why it matters to CI/CD security concretely:** Debloating and reachability work bears directly on **which dependencies actually matter** — the difference between an SBOM that lists 800 packages and an analysis that shows 40 are reachable. That distinction is the difference between an alert-generating product and a useful one.
- **Follow:** DBLP author search **https://dblp.org/search/author/api?q=Benoit%20Baudry&format=json** (returns the record; alias "Benoît Baudry") · CHAINS **https://chains.proj.kth.se/** · **Personal site, Scholar, and social not verified — named gap**
- **Cadence:** High (co-author on much of the CHAINS output).
- **Tier: CORE**

**Musard Balliu** — KTH, **CHAINS PI**. [VERIFIED as PI on the CHAINS site only]. Signal: language-based security, runtime enforcement for Node.js, prototype-pollution detection. Co-author *Software Bill of Materials in Java* (SCORED 2023). **Relevance to CI/CD:** runtime enforcement is the complement to static SBOM analysis. **No personal site/DBLP/social verified — named gap. Tier: PERIODIC.**

**Mathias Ekstedt** — KTH, **CHAINS PI**. [VERIFIED as PI on the CHAINS site only]. Signal: threat modelling / security architecture. **Nothing else verified — named gap. Tier: CONTEXT.**

---

**Georgios Gousios** — **Head of Research, Endor Labs**, Palo Alto, CA. **NO LONGER AT TU DELFT.** [VERIFIED from the strongest possible source — his own site's changelog records: "**Quit part time job at TU Delft**", **March 2025**. Previously a researcher at Facebook/Meta, and formerly Associate Professor in TU Delft's Software Engineering Research Group]

- ⚠️ **This is the clearest DBLP trap in the map:** DBLP *still* lists him as "TU Delft, Department of Software Technology, The Netherlands." **His own site is authoritative; DBLP is stale.**
- **Signal:** Software analytics, ML for SE, **dependency management**. Now producing **vendor research** — Endor Labs is a commercial dependency/reachability-analysis company and he runs its research arm.
- **Why it matters to CI/CD security concretely:** He is now positioned exactly where academic dependency research meets a commercial product. His output is a good read on **how the vendor market frames these problems** — useful competitive and positioning intelligence, but read with the commercial interest visible.
- **Follow:** **https://gousios.org/** · blog at **https://gousios.org/blog** · **Google Scholar: http://scholar.google.gr/citations?user=-NI5S50AAAAJ** (verified via his own site) · ORCID http://orcid.org/0000-0002-8495-7939 · GitHub https://github.com/gousiosg · LinkedIn https://www.linkedin.com/in/gousiosg/ · email gousiosg@endor.ai
- **Cadence:** Reduced academic output post-move; blog is the live channel.
- **Tier: CORE — but reclassify as INDUSTRY, not academic.**

---

**Diomidis Spinellis** — **three concurrent, all-current roles:** Professor of Software Engineering, Department of Management Science and Technology, **Athens University of Economics and Business**; **Professor of Software Analytics, Department of Software Technology, TU Delft**; Director, Business Analytics Laboratory (BALab). [VERIFIED — https://www.spinellis.gr/index.en.html. **The part-time TU Delft appointment is confirmed current** — unlike Gousios, he has not left]

- **Signal:** Very broad software engineering — tooling, analytics, open-source history, developer practice. Supply chain is one thread among many, not his centre of gravity.
- **Why it matters to CI/CD security concretely:** Indirect but genuine — he is a consistently well-calibrated commentator on software tooling and practice, and his blog surfaces things before they reach papers.
- **Follow:** ⭐ **The best-instrumented follow surface of anyone in this map:**
  - **Blog with RSS: https://www.spinellis.gr/blog/index.html**
  - **Bluesky: https://bsky.app/profile/CoolSWEng.bsky.social**
  - **Mastodon: https://mastodon.acm.org/@CoolSWEng**
  - **Google Scholar: https://scholar.google.com/citations?user=RjXNgA8AAAAJ**
  - **DBLP: http://www.informatik.uni-trier.de/~ley/db/indices/a-tree/s/Spinellis:Diomidis.html**
  - Site: https://www.spinellis.gr/ (~14,000 pages, 98,000+ hyperlinks)
  - ⚠️ Note: the bare `https://www.spinellis.gr/` root is a language-selection redirect page that defeats automated fetch — **use `/index.en.html`**
- **Recent supply-chain-specific papers:** **none identified in this pass** — his publications page was not reachable in the time available. **Flagged gap.**
- **Cadence:** High overall; supply-chain subset low.
- **Tier: PERIODIC**

---

**Sebastian Proksch** — TU Delft (presumed). ⚠️ **UNVERIFIED — could not confirm.** `proksch.net` returns a **TLS certificate-expired error**. The TU Delft SERG site (https://se.ewi.tudelft.nl/) lists research areas but **publishes no faculty roster**, so I could not confirm him from the institutional side either.
- **Note:** TU Delft SERG *does* list "**DevOps practices and CI/CD understanding**" among its ten research areas, so the group has relevant activity even though individual attribution failed.
- **Follow:** TU Delft SERG https://se.ewi.tudelft.nl/ · **everything else unverified — named gap**
- **Tier: CONTEXT — pending verification**

---

**University of Mons (UMONS), Belgium — the GitHub Actions empirical powerhouse.**

**This is the answer to "who does large-scale empirical CI/CD security studies" — and it is Belgium, not the US.**

**Tom Mens** — **Professor and Director, Software Engineering Lab**, Department of Computer Science, University of Mons, Belgium (De Vinci building). [VERIFIED — https://informatique-umons.be/genlog/. ⚠️ Note the old URL `informatique.umons.ac.be/genlog/` **302-redirects** to the new domain]
- Lab research focus: "open source software, empirical software engineering, software ecosystems, software evolution, and software modeling."
- ⚠️ The lab site's front page **does not list members or publications** — use DBLP.

**Alexandre Decan** — University of Mons. [DBLP PID **84/7943** VERIFIED, ORCID 0000-0002-5824-5823. ⚠️ DBLP's author-search record carries **no affiliation string**; his personal site at `www.decan.lexpage.net` **does not resolve**. Affiliation inferred from universal co-authorship with Mens]

- **Signal:** **The most sustained empirical work on GitHub Actions anywhere.** Every paper below is Decan + Mens. They publish **datasets and tools**, not just findings — directly reusable.
- **Why it matters to CI/CD security concretely:** This is the closest thing to a ground-truth empirical baseline for how GitHub Actions workflows are actually written, how they evolve, and where they break. ***Quantifying Security Issues in Reusable JavaScript Actions in GitHub Workflows* (MSR 2024) targets exactly the reusable-action supply-chain surface** that every CI pipeline depends on. Their bot-identification work (RABBIT) is directly relevant to reasoning about Dependabot/Renovate activity at scale.
- **Follow:** **DBLP: https://dblp.org/pid/84/7943** · Lab: **https://informatique-umons.be/genlog/** · **no personal site (DNS fails), no verified Scholar or social — named gap.** DBLP is the only reliable surface.
- **Recent papers:**
  - *An empirical study of the evolution of GitHub Actions workflows* — **Journal of Systems and Software, 2026** (Decan, Rostami Mazrae, Mens, Wessel)
  - *An Empirical Analysis of Code Clones in GitHub Actions Workflows* — **SANER 2026** (Cardoen, Decan, Mens)
  - *A bot identification model and tool based on GitHub activity sequences* — **Journal of Systems and Software, 2025** (Chidambaram, Decan, Mens)
  - *Quantifying Security Issues in Reusable JavaScript Actions in GitHub Workflows* — **MSR 2024** (Onsori Delicheh, Decan, Mens)
  - *A dataset of GitHub Actions workflow histories* — **MSR 2024** (Cardoen, Decan, Mens)
  - *gawd: A Differencing Tool for GitHub Actions Workflows* — **MSR 2024** (Rostami Mazrae, Decan, Mens)
  - *RABBIT: A tool for identifying bot accounts based on their recent GitHub event history* — **MSR 2024** (Chidambaram, Decan, Mens)
  - *An Overview and Catalogue of Dependency Challenges in Open Source Software Package Registries* — **BENEVOL 2024** (Decan, Mens)
- **Cadence:** 3-5 GitHub-Actions papers/year, concentrated at MSR.
- **Tier: CORE for anyone running GitHub Actions.**

**Associated Mons researchers** (all **UNVERIFIED** individually): Pooya Rostami Mazrae, Guillaume Cardoen, Hassan Onsori Delicheh, Natarajan Chidambaram. External collaborator: Mairieli Wessel.

---

**European groups NOT examined — named gaps, all UNVERIFIED.** Search budget was exhausted before reaching these; each is a plausible lead that deserves a follow-up pass:
- **TU Darmstadt** — Mira Mezini (software ecosystems/dependencies), Ahmad-Reza Sadeghi (systems security), and the ATHENE national cybersecurity centre. **Supply-chain relevance unconfirmed.**
- **CISPA Helmholtz Center for Information Security** — flagged as a strong lead in the original brief. **Entirely unexamined.** Probably the highest-value item on this list.
- **University of Luxembourg SnT** — Jacques Klein, Tegawendé Bissyandé (Android/app supply chain, dependency research). **Unexamined.**
- **Vrije Universiteit Amsterdam** — Herbert Bos / VUSec (mostly systems/hardware security — supply-chain relevance likely weak), Ivano Malavolta. **Unexamined.**
- **Chalmers / University of Gothenburg** — Jan-Philipp Steghöfer (may have left for industry), Regina Hebig, Gregory Gay (CI/testing), Michel Chaudron, Riccardo Scandariato (may have moved to Hamburg). **All unexamined.** One indirect signal that Gothenburg is worth probing: **the 2026 Reproducible Builds Summit is being held there.**
- Also unexamined: INRIA (beyond Courtès), Politecnico di Milano, Radboud, ETH Zurich, University of Bern.

---

### A6. Reproducible builds

**Reproducible Builds project** — https://reproducible-builds.org/ — **alive, active, and funded.** [VERIFIED by fetch]

- Self-definition: "a set of software development practices that create an independently-verifiable path from source to binary code."
- **Named sponsor: the Sovereign Tech Agency.**
- ⚠️ **Correction to a common assumption: the reports are MONTHLY, not weekly.** News at **https://reproducible-builds.org/news/** — July 2026 report published 2026-08-09; June on 2026-07-11; May on 2026-06-04. **Cadence is reliably monthly and easy to track.**
- **Mastodon: @reproducible_builds@fosstodon.org** · Reddit: r/reproduciblebuilds
- ⚠️ **No RSS URL is advertised on the homepage** — flagged. The Mastodon account is the reliable machine-readable channel.
- **Summits: Vienna 2025** (announced 2025-08-20); **Gothenburg 2026** (announced 2026-08-12). **Still running annually.**
- **Tier: CORE as an organisation** (practitioner, not academic)

**Ludovic Courtès** — **Inria**, France. Associated with **GNU Guix** and **Guix-HPC** ("a joint effort between Inria, the Max Delbrück Center for Molecular Medicine (MDC), and the Utrecht Bioinformatics Center (UBC)"). [Affiliation inferred from the Guix-HPC institutional partnerships — **DBLP's author record carries no affiliation string**, so this is **PARTIALLY VERIFIED**]
- **Signal:** Functional package management and reproducible *scientific* computing. His listed publications skew to bioinformatics workflow reproducibility (GigaScience 2018; *Scalable Workflows and Reproducible Data Analysis for Genomics* in Evolutionary Genomics, 2019) rather than recent supply-chain security.
- **Why it matters to CI/CD security concretely:** Guix is the strongest existing demonstration that **fully reproducible, bootstrappable builds are achievable in practice** — the existence proof behind the whole reproducibility argument. Directly relevant if you assert build determinism.
- **Follow:** **DBLP: https://dblp.org/pid/712304** · **Blog: https://hpc.guix.info/blog/** (publishes annual activity reports) · **no verified Scholar or social — named gap**
- **Cadence:** Low in security venues.
- **Tier: CONTEXT**

**Chris Lamb** — Debian; long-associated with Reproducible Builds. **Practitioner, NOT an academic.** ⚠️ **His current role was NOT independently verified in this pass — named gap.** **Tier: CONTEXT.**

**The important structural finding on reproducible builds:** there is **no dedicated academic reproducibility group**. The peer-reviewed work is being done inside the supply-chain groups already listed — **KTH/CHAINS and NC State/S3C2**:
- *Causes and Canonicalization of Unreproducible Builds in Java* — **IEEE TSE 2025** (Monperrus/CHAINS)
- *An Empirical Study on Reproducible Packaging in Open-Source Ecosystems* — **ICSE 2025** (Benedetti, Solarin, Miller, Tystahl, Enck, Kästner, Kapravelos, Merlo, Verderame — an NC State/CMU/Genoa collaboration)
- *BinEq — A Benchmark of Compiled Java Programs to Assess Alternative Builds* — **SCORED 2024**
- *Auditing the CI/CD Platform: Reproducible Builds vs. Hardware-Attested Build Environments* — **SCORED 2024** (Melara)
- *Maven-Lockfile: High Integrity Rebuild of Past Java Releases* — arXiv 2510.00730
- *Trusting-Trust Attack against an Entire Linux Distribution through Binary Manipulation* — arXiv 2607.24888, July 2026

**Merlo and Verderame** (University of Genoa, **UNVERIFIED**) appear on the ICSE 2025 reproducible-packaging paper — an Italian group not otherwise on this map. **Named gap.**

---

## PART B — Venues

### B1. SCORED — the headline finding

**SCORED is the single most on-topic venue in existence, and it has just relocated away from ACM CCS.**

- **What it is:** now titled "**Conference** on Software Supply Chain Offensive Research and Ecosystem Defenses" — it was a **Workshop** through 2025. The rename is on its own site.
- **Status: RUNNING. 2026 edition confirmed.**
- **SCORED '26: October 6, 2026, Prague, Czechia — co-located with OpenSSF Community Day Europe, NOT with ACM CCS.**
- Site: **https://scored.dev/** · CFP: https://scored.dev/cfp.html · submissions: scored26.hotcrp.com · contact: scored26-chairs@googlegroups.com
- Still "in cooperation with **ACM**", plus **OpenSSF** and **Linux Foundation** (logos on site).
- **The move was confirmed from BOTH ends** — not inferred:
  1. scored.dev states the OpenSSF Community Day Europe co-location.
  2. The **CCS 2026 workshop list** (https://www.sigsac.org/ccs/CCS2026/workshops/workshops.html) — 3D-Sec, WATCH, AGENT-SEC, AISec, CPSIoTSec, WPES, LAMPS, WTMC (Nov 15) and SaTS, SURE, TAKEDOWN, TrustAICyberSec, WAHC, ACTIVE, DeFI, PLAS (Nov 19) — **does not include SCORED.**
- **2026 deadline was extended to July 19 and has already passed.** Next actionable CFP is SCORED '27.
- **History — four editions, all previously at CCS:** 2022 Los Angeles · 2023 Copenhagen · 2024 Salt Lake City · 2025 Taipei.
- ⭐ **BEST WATCH URL — the dblp venue stream: https://dblp.org/db/conf/scored/**
  Per-edition: `https://dblp.org/db/conf/scored/scored2025.html`, `.../scored2024.html`, `.../scored2023.html`, `.../scored2022.html`
  ⚠️ Note `scored.dev/past.html` exists but contains **no historical content**; and `dl.acm.org` returns **403** to automated fetch. **dblp is the only reliable programmatic surface.**
- **Machine-readable API:** `https://dblp.org/search/publ/api?q=scored&h=60&format=json` — returns full JSON. **Verified working.**
- **Volume: ~10 papers per edition — small, dense, essentially 100% on-topic.** This is the highest signal-to-noise venue in the field.
- **Chairs rotate through the core network** — a useful ascendancy indicator: SCORED '23 Melara/Torres-Arias/S. (https://dblp.org/rec/conf/ccs/MelaraTS23) · '24 Torres-Arias/M. (https://dblp.org/rec/conf/ccs/Torres-AriasM24) · '25 Yelgundhalli/H./R./D. (https://dblp.org/rec/conf/ccs/YelgundhalliHRD25)
- **Representative 2025 papers:** *Stepping out of Bounds: Security Impact of Allowing Packages on npm to Declare External Dependencies* · *From Hardware to Artifact: Trusted Software Builds with Remote Attestation* · *Spilling the Tea: Uncovering TEA Token Abuse in npm* · *ORCA: Unveiling Obscure Containers In The Wild* · *A Soundness and Precision Benchmark for Java Debloating Tools* · *Measuring Enterprise Software Supply Chain Security using Public Repositories* · *Aggregating Security Measures from the Dependency Tree* · *Establishing a Baseline of Software Supply Chain Security Task Adoption by Software Organizations* · *Maven-Hijack*
- **Representative 2024 papers:** *GoSurf* · *Nowhere to Hide: Using Transparency Logs to Secure Your Supply Chain* · *Impacts of SBOM Generation on Vulnerability Detection* · *What's in a URL? An Analysis of Hardcoded URLs in npm Packages* · *Auditing the CI/CD Platform: Reproducible Builds vs. Hardware-Attested Build Environments* · *Extending Cloud Build Systems to Eliminate Transitive Trust* · *Runtime Verification for Software Supply Chain Security using Confidential Computing* · *Developers' Approaches to Software Supply Chain Security: An Interview Study* · *On the Security Blind Spots of Software Composition Analysis* · *BinEq* · *Enhancing Transparency and Accountability of TPLs with PBOM: A Privacy Bill of Materials*

---

### B2. Academic security conferences

| Venue | What it is | Carries supply-chain/CI-CD? | Best watch URL | Feed/API |
|---|---|---|---|---|
| **IEEE S&P ("Oakland")** | Top-tier security. **May 18-21, 2026, Hilton San Francisco Union Square** (main May 18-20; workshops May 21) [VERIFIED https://sp2026.ieee-security.org/] | **YES, and rising — the venue to watch.** ~2-4/yr. *Cosseter* (GitHub Actions permission reduction, 2026); *Signing in Four Public Software Package Registries* (2024) | **https://sp2026.ieee-security.org/accepted-papers.html** · workshops at `/workshops.html` | No RSS found. Use `https://dblp.org/search/publ/api?q=stream:conf/sp:&format=json` |
| **NDSS** | Network & Distributed System Security. **Feb 23-27, 2026, San Diego — already held.** [VERIFIED https://www.ndss-symposium.org/ndss2026/] | **YES — punches above its weight.** ~2-3/yr. gittuf (2025 Distinguished Paper); OSS contribution attribution (2025); *UntrustIDE* (2024 Distinguished Paper); TAF (2026) | **https://www.ndss-symposium.org/ndss2026/accepted-papers/** · program `/program/` · co-located `/co-located-events/` (MADWeb, PRISM — supply-chain relevance not confirmed) | No RSS found; dblp API |
| **ACM CCS** | ACM SIGSAC flagship. **Nov 15-19, 2026, The Hague, Netherlands (World Forum).** Hosts: **TU Delft + University of Turku.** Cycle B submissions open via HotCRP [VERIFIED https://www.sigsac.org/ccs/CCS2026/] | **Reduced.** Was SCORED's home 2022-2025 — **that anchor is now gone.** Main track carries occasional supply-chain work (*Rust for Embedded Systems*, 2024) | **https://www.sigsac.org/ccs/CCS2026/** · workshops `/workshops/workshops.html` | dblp API |
| **USENIX Security** | Top-tier security; multi-cycle deadlines | **YES.** ~3-5/yr. Software-signing industry interview study (2025); SCA qualitative study (2025); **ARGUS** — staged static taint analysis of GitHub workflows/Actions (2023); Acar's 4 papers (2024) | ⚠️ **UNVERIFIED-BY-FETCH — usenix.org returns HTTP 403 to all automated requests.** Expected pattern: `https://www.usenix.org/conference/usenixsecurity26/technical-sessions` — **verify manually** | Use dblp: `https://dblp.org/search/publ/api?q=stream:conf/uss:&format=json` |

⚠️ **Security note worth flagging on CCS 2026:** the conference site itself discloses that "**A security breach in HotCRP allowed unauthorized parties to download approximately 500 PDF files**" before the submission deadline; affected authors were notified January 16. Review continued as scheduled. This is publicly disclosed on the official site — and is itself a supply-chain-adjacent incident in academic infrastructure.

**Verdict on the security venues:** **NDSS and IEEE S&P are currently the strongest carriers** of supply-chain and CI/CD work. USENIX Security carries the qualitative/interview studies. **CCS's relevance to this beat dropped materially when SCORED left.**

---

### B3. Software engineering conferences — where the actual volume is

**These carry substantially MORE supply-chain, dependency, and CI/CD work than the security venues do.** If you only watch security conferences you will miss most of the field.

| Venue | What it is | Carries it? | Best watch URL |
|---|---|---|---|
| **MSR** (Mining Software Repositories) | **April 13-14, 2026, Rio de Janeiro**, co-located with ICSE [VERIFIED https://conf.researchr.org/home/msr-2026] | ⭐ **The highest-density venue for empirical CI/CD work.** MSR 2024 alone carried **four** GitHub-Actions papers from Mons. Publishes **datasets and tools**, not just findings — directly reusable | **https://2026.msrconf.org/program/program-msr-2026/** · dates https://2026.msrconf.org/dates (Registered Reports deadline Mon 28 Sep 2026) |
| **ICSE** | International Conference on Software Engineering. **April 12-18, 2026, Rio de Janeiro** (core days Apr 15-17) [VERIFIED https://conf.researchr.org/home/icse-2026] | **YES — real and growing volume, ~4-6/yr.** 2026: Fake Stars, Closing the Chain, Abandabot. 2025: LLM npm malware detection, reproducible packaging, npm abandonment, ZTD_JAVA | **https://conf.researchr.org/program/icse-2026/program-icse-2026/** · Relevant co-located: **SVM 2026** (Software Vulnerability Management), EnCyCriS, STATIC, SESoS, WETSEB, SERS |
| **FSE** | ⚠️ **Name confirmed: "ACM International Conference on the Foundations of Software Engineering" — the ESEC prefix has been DROPPED.** **July 5-9, 2026, Concordia SGW Campus, Montreal, Canada** [VERIFIED https://conf.researchr.org/home/fse-2026] | **YES.** FSE 2025 carried *Pinning Is Futile* (Distinguished Paper), *Dirty-Waters* (Tool Track), and Williams' supply-chain keynote | **https://conf.researchr.org/program/fse-2026/program-fse-2026/** · **4 co-located conferences (AIWARE, PROMISE, SecDev, SSBSE) + 13 workshops** |
| **ASE** | **41st IEEE/ACM International Conference on Automated Software Engineering. Oct 12-16, 2026, Munich, Germany** (Holiday Inn Munich – City Center) [VERIFIED https://conf.researchr.org/home/ase-2026] | **Yes, moderate.** ASE 2025 carried *Pinning or Floating?* and *Your Build Scripts Stink* | **https://conf.researchr.org/home/ase-2026** · **18 co-located workshops**; relevant: **SECUTE** (software security testing), TRUST |

**Two important venue findings inside FSE 2026:**

1. **SecDev has moved from IEEE to ACM.** `secdev.ieee.org` shows only **IEEE SecDev 2025** (Oct 14-16, 2025, Purdue University, Indianapolis; accepted posters at `/2025/accepted-posters/`, schedule at `/2025/schedule/`, CFP at `/2025/cfp/`), while **FSE 2026 lists "ACM SecDev — ACM Secure Development Conference" as a co-located conference** with research papers, practitioner papers and poster tracks — and William Enck's own page cites a paper at "2026 ACM Secure Development Conference (SecDev)." ⚠️ **I did not locate the formal transition announcement — flagged as inference from two consistent sources.** **Watch it via the FSE 2026 site.**
2. ⭐ **LLMSC 2026 — "LLM Supply Chain Analysis"** — a **brand-new workshop** at FSE 2026, dedicated site **https://llmsc.github.io/** (the researchr page auto-redirects there). **Worth watching from edition one** — this is the AI/supply-chain intersection forming in real time.

---

### B4. Industry and practitioner events

**OpenSSF — ⚠️ the naming has changed.** The current official name is "**OpenSSF Community Day**". "**SOSS Community Day**" is **outdated** — do not use it. [VERIFIED https://openssf.org/events/]

- ⭐ **OpenSSF Community Day Europe 2026 — October 6, 2026, Prague, Czechia.** https://openssf.org/event/openssf-community-day-europe-2026/ · **agenda https://openssfcdeu2026.sched.com/** · registration https://events.linuxfoundation.org/openssf-community-day-europe/register/
  **This is now SCORED's host venue — one trip covers both the academic workshop and the practitioner community day.**
- **Open Source SecurityCon North America — November 9, 2026, Salt Lake City.** A **CNCF-hosted co-located event at KubeCon + CloudNativeCon NA** (Nov 9-12). https://openssf.org/event/open-source-securitycon-north-america/ — described as "a 1-day event uniting developers, security leaders & open source experts."
- Other OpenSSF-listed 2026 events: Open Source Summit Europe (Oct 7-9, Prague), AGNTCon + MCPCon NA (Oct 20-23, San Jose), All Things Open (Oct 19-20, Raleigh), Let's Talk Open Source Security (Sep 3, Bengaluru).

**SupplyChainSecurityCon — ⚠️ APPEARS RETIRED. Flagged as strong inference, NOT confirmed.**
- It is **not listed anywhere** on the Linux Foundation events calendar (https://events.linuxfoundation.org/) for late 2026 or 2027.
- The 2025 archive URL (`events.linuxfoundation.org/archive/2025/open-source-summit-north-america/about/supplychainsecuritycon/`) **404s**.
- **Cloud Native SecurityCon is likewise absent** from the calendar.
- The reasonable inference is that both were **consolidated into Open Source SecurityCon**. **Confirm directly before planning around this.**

**Linux Foundation calendar anchors** [VERIFIED https://events.linuxfoundation.org/]: Open Source Summit Europe **Oct 7-9, 2026, Prague** · KubeCon+CloudNativeCon NA **Nov 9-12, 2026, Salt Lake City** · Open Source Summit Japan **Dec 7-9, 2026, Tokyo** · KubeCon EU **Mar 15-18, 2027, Barcelona** · Open Source Summit NA **May 17-19, 2027, Vancouver** · KubeCon NA **Nov 8-11, 2027, New Orleans** · Linux Plumbers **Oct 5-7, 2026, Prague**.

**DEF CON** [VERIFIED https://defcon.org/html/links/dc-archives.html]
- **DEF CON 34 was held August 6-9, 2026, Las Vegas Convention Center, West Hall.**
- Archive sections: Archives By Show, File Downloads, CTF Archive, Tools Released, Press Archives.
- ⭐ **Best watch URL — the media server, where slides and papers actually land: `https://media.defcon.org/DEF CON 34/`**
- ⚠️ The archive page does **not** list villages — village programming must be tracked separately.

**AppSec Village** [VERIFIED https://www.appsecvillage.com/]
- A **100% volunteer-run 501(c)(3) not-for-profit**, **independent** of any single conference.
- **2026 appearances: RSAC Conference (March 24-26) and DEF CON 34 (August 7-9).**
- ⭐ **Talk archive: https://www.youtube.com/c/AppSecVillage** — also active on Twitter, LinkedIn, Discord.
- **Supply-chain relevance: probable but unconfirmed.** Sponsors include **Chainguard, Finite State, and Apiiro** — all supply-chain-security vendors — which strongly suggests coverage, but the site does not detail specific supply-chain programming.

**Black Hat USA / Europe** — ⚠️ **UNVERIFIED-BY-FETCH.** `blackhat.com` returns **HTTP 403** to automated requests on both `/html/archives.html` and `/upcoming.html`. **Dates, locations, and the briefings-archive URL all need manual confirmation.** Black Hat historically carries high-profile supply-chain offensive research, so this gap matters.

**Nullcon / OffensiveCon** — not verified this session. **Honest recommendation: deprioritise for this beat.** Both are exploitation and vulnerability-research focused; supply chain is not their centre of gravity.

**Reproducible Builds Summit** — **RUNNING ANNUALLY.** Vienna 2025; **Gothenburg 2026** (announced 2026-08-12). Watch **https://reproducible-builds.org/news/** — announcements appear there. [VERIFIED]

---

### B5. arXiv — preprints, where things land 6-12 months early

**All URLs below were fetched and confirmed working in this session.**

**Category firehose (RSS) — ✅ VERIFIED:**
```
https://rss.arxiv.org/rss/cs.CR
```
Feed title "cs.CR updates on arXiv.org"; **50 items/day**. Atom equivalent: `https://rss.arxiv.org/atom/cs.CR`. Also useful: `https://rss.arxiv.org/rss/cs.SE`.
⚠️ **Two gotchas:** (1) this is the **new** `rss.arxiv.org` host — the old `export.arxiv.org/rss/` endpoints were retired; (2) the human-readable listing page `https://arxiv.org/list/cs.CR/recent` **does not advertise the feed link at all**, so it cannot be discovered by browsing. **50 items/day is firehose volume — only usable with keyword filtering.**

**Term search — ✅ VERIFIED (239 results):**
```
https://arxiv.org/search/?searchtype=all&query=%22software+supply+chain%22
```
Recent hits confirming the beat is live: *The Software Supply Chain as a Market for Lemons: A Multivocal Review of Trust Signal Collapse* (2608.20678, cs.CR/cs.SE) · *The Rising Cost of Trust: Practitioners' Trust Signals, Controls, and Responses in the Software Supply Chain* (2608.20675, cs.CR) · *Evaluating Inference-Time Defenses Against Package Hallucination in LLM-Generated Code* (2608.22652, cs.SE/cs.AI).

**Advanced search scoped to computer science — ✅ VERIFIED (29 results for "reproducible build"):**
```
https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=%22reproducible+build%22&terms-0-field=all&classification-computer_science=y&classification-physics_archives=all&classification-include_cross_list=include&start=0
```
**Swap the `terms-0-term` value** for: `"SBOM"`, `"in-toto"`, `"SLSA"`, `"GitHub Actions"`, `"software signing"`, `"build provenance"`, `"dependency confusion"`, `"typosquatting"`, `"package registry"`.

**Per-author pages — ✅ VERIFIED:**
```
https://arxiv.org/a/monperrus_m_1        (157 papers)
```
The `/a/<lastname>_<initial>_<n>` pattern works and is a clean per-author watch surface.

⚠️ **I did NOT verify whether arXiv's *search* endpoint emits RSS/Atom for an arbitrary query.** If it does not, the robust substitutes are:
- **arXiv API** (pattern **NOT verified in this session — test before relying on it**):
  ```
  http://export.arxiv.org/api/query?search_query=all:%22software+supply+chain%22&sortBy=submittedDate&sortOrder=descending&max_results=50
  ```
- A **Google Scholar alert** on the same query (manual setup; Scholar is not fetchable programmatically).

---

### B6. ⭐ DBLP as a feed source — the most underrated instrument in this map

This deserves its own section because it repeatedly **succeeded where everything else failed**. It resolved SCORED's complete four-edition history when `dl.acm.org` returned 403 and `scored.dev/past.html` was empty; it produced Decan's entire GitHub-Actions corpus when his personal site's DNS failed; and it produced Torres-Arias's full 2024-2026 output when his Purdue page 404'd.

**Publication search (returns clean JSON):**
```
https://dblp.org/search/publ/api?q=<query>&h=<count>&format=json
```
**Author search (returns affiliation strings):**
```
https://dblp.org/search/author/api?q=<name>&format=json
```
**Venue streams:** `https://dblp.org/db/conf/scored/` · query form `q=stream:conf/<venue>:`

**Verified DBLP PIDs from this research:**
Cappos `27/5136` · Torres-Arias `185/1711` · Moore `236/5493` · Kuppusamy `44/8573` · Decan `84/7943` · Courtès `712304` · Vasilescu `pers/hd/v/Vasilescu:Bogdan` · Spinellis `indices/a-tree/s/Spinellis:Diomidis`

**Caveat, restated because it bit twice:** DBLP is authoritative for *publications*, unreliable for *current affiliations*.

---

## PART C — 8 papers to actually read, for someone building a CI/CD-observability product

Ordered by directness of application. Where I have only a listing-page source rather than a canonical DOI, I say so.

**1. *Cosseter: GitHub Actions Permission Reduction Using Demand-Driven Static Analysis***
Tystahl, Ghebremichael, Muralee, Cherupattamoolayil, Bianchi, Machiry, Kapravelos, Enck — **IEEE S&P 2026**
Source: https://www.enck.org/pubs/ · watch https://sp2026.ieee-security.org/accepted-papers.html
**Why:** The most directly actionable paper found. Automatically determining the minimum permissions a workflow actually needs is precisely the analysis a CI/CD-observability product should perform. Over-permissioned workflows are a primary finding class, and this is the current state of the art for detecting them.

**2. *Research Directions in Software Supply Chain Security***
Williams, Benedetti, Hamer, Paramitha, Rahman, Tamanna, Tystahl, Zahan, Morrison, Acar, Cukier, Kästner, Kapravelos, Wermke, Enck — **ACM TOSEM, January 2025**
Source: https://s3c2.org/pubs/
**Why:** Read this **first** for orientation. Fifteen authors spanning the entire S3C2 programme mapping the whole field — the taxonomy, the open problems, and the vocabulary the research community uses. It will tell you which of the other seven papers you most need.

**3. *Pinning Is Futile: You Need More Than Local Dependency Versioning to Defend Against Supply Chain Attacks***
He, Vasilescu, Kästner — **FSE 2025, Distinguished Paper**
Source: https://cmustrudel.github.io/publications/ and https://www.cs.cmu.edu/~ckaestne/
**Why:** Directly challenges a defence most tooling (and most engineering teams) treat as settled. If your product reports on or recommends pinning, this is the empirical case that local pinning alone does not deliver the protection assumed.

**4. *Which Is Better For Reducing Outdated And Vulnerable Dependencies: Pinning Or Floating?***
Rahman, Marley, Enck, Williams — **ASE 2025**
Source: https://s3c2.org/pubs/ and https://www.enck.org/pubs/
**Why:** The necessary companion to #3 — the same question from an independent group, framed as an operational trade-off rather than a security refutation. **Read them together;** the pair is what lets you give calibrated advice instead of a slogan.

**5. *Quantifying Security Issues in Reusable JavaScript Actions in GitHub Workflows***
Onsori Delicheh, Decan, Mens — **MSR 2024**
Source: https://dblp.org/pid/84/7943
**Why:** Targets exactly the reusable-third-party-action surface that every GitHub Actions pipeline depends on and few teams audit. From the Mons group, so it comes with the ecosystem-scale empirical grounding and, typically, a reusable dataset.

**6. *Causes and Canonicalization of Unreproducible Builds in Java***
CHAINS/KTH (Monperrus group) — **IEEE Transactions on Software Engineering, 2025**
Source: https://www.monperrus.net/martin/publications
**Why:** The most detailed treatment of **why builds fail to reproduce and which differences can legitimately be normalised away**. If your product asserts anything about build integrity or determinism, this is the taxonomy of what actually goes wrong in practice.

**7. *Rethinking Trust in Forge-Based Git Security* (gittuf)**
Yelgundhalli, Zielinski, Curtmola, Cappos — **NDSS 2025, Distinguished Paper Award**
Source: https://ssl.engineering.nyu.edu/publications · project https://gittuf.dev/
**Why:** The core thesis — that you cannot trust the forge to tell the truth about its own history, so policy must be independently verifiable — is the exact threat model a CI/CD-observability product exists to address. It is also a shipped OpenSSF project, not just a paper, so it doubles as a potential integration target.

**8. *Auditing the CI/CD Platform: Reproducible Builds vs. Hardware-Attested Build Environments***
Melara, K. — **SCORED 2024** — https://dblp.org/rec/conf/scored/MelaraK24
**Why:** Frames the central architectural fork for anyone building build-integrity tooling: **reproduce the build to verify it, or attest the environment that produced it.** Short, workshop-length, and squarely about the design decision rather than a measurement result.

**Two honourable mentions** if the AI angle matters to you: *The Grand Software Supply Chain of AI Systems* (Monperrus, arXiv 2604.27781, 2026) and *Six Million (Suspected) Fake Stars on GitHub* (He, Yang, Burckhardt, Kapravelos, Vasilescu, Kästner — ICSE 2026) — the latter because it demonstrates that GitHub popularity signals are systematically gamed and correlate with malware distribution, which invalidates a trust heuristic many products rely on.

---

## Recommended minimum viable watchlist

**Five feeds cover roughly 80% of the field:**
1. **https://s3c2.org/feed.xml** — Williams, Enck, Kästner, Cukier, Acar, Kapravelos, Wermke in one stream
2. **https://www.monperrus.net/martin/dblp-rss.py?search=author:martin_monperrus** — KTH/CHAINS, extremely high volume
3. **https://dblp.org/db/conf/scored/** — the on-topic venue; ~10 papers/yr at near-100% relevance
4. **MSR + ICSE programs** (co-located, Rio de Janeiro, April 2026) — where the empirical CI/CD volume actually is
5. **arXiv `"software supply chain"` search** — 6-12 month lead on everything above

**Three calendar entries:** SCORED '27 CFP (~July) · MSR/ICSE (April, Rio) · OpenSSF Community Day EU + SCORED '26 (October 6, Prague).

**One structural recommendation:** **watch the in-toto STEERING-COMMITTEE.md file and the SCORED chair line rather than institutional pages.** Both are current, both are machine-readable, and both tracked personnel movement — Yelgundhalli→Bloomberg, Moore→Edera, Kuppusamy→unknown — that faculty pages and TUF's own maintainer file missed entirely.

---

## Complete list of named gaps and unverified items

**Highest priority (likely to change conclusions):**
1. **CISPA Helmholtz Center** — flagged as a strong lead, entirely unexamined
2. **CMU SEI** — supply-chain topic page 404s; team, Sam Weber's location, and RSS all unconfirmed; programme may have been reorganised
3. **USENIX Security** and **Black Hat** — both return HTTP 403 to automated fetch; need manual verification
4. **Marcela Melara's affiliation** — recurring high-signal name, no primary source confirmed

**Medium priority:**
5. **SupplyChainSecurityCon's fate** — absence from the LF calendar is strong but circumstantial
6. **SecDev's IEEE→ACM transition** — inferred from two consistent sources; no formal announcement located
7. **European long tail** — TU Darmstadt, VU Amsterdam, Luxembourg SnT, Chalmers/Gothenburg, INRIA, ETH Zurich all unexamined
8. **Trishank Kuppusamy's current employer** — needs a manual LinkedIn check
9. **Sebastian Proksch** — site has an expired TLS certificate; TU Delft publishes no faculty roster
10. **Sigstore governance** — the site is a JS SPA that defeats fetch

**Lower priority:**
11. **Google Scholar profile URLs** for Cappos, Torres-Arias, Williams, Enck — Scholar is not fetchable; all need manual lookup
12. **Aditya Yelgundhalli, Dominik Wermke, Alexandros Kapravelos, Michel Cukier, Adam Aviv, Benoit Baudry, Musard Balliu** — no personal site, DBLP PID, or social account verified for any of them
13. **Merlo and Verderame (University of Genoa)** — appear on the ICSE 2025 reproducible-packaging paper; an Italian group not otherwise on this map
14. **Chris Lamb's current role** at Debian/Reproducible Builds
15. **arXiv query-RSS support** and the export API pattern — untested
16. **Spinellis's supply-chain-specific publications** — his publications page was not reached

---

## Two observations beyond the original scope

**1. The AI/supply-chain intersection is forming right now, within the last ~12 months.** *The Grand Software Supply Chain of AI Systems* (Monperrus, arXiv 2604.27781); *Towards Verifiably Safe Tool Use for LLM Agents* (ICSE-NIER 2026); *Evaluating Inference-Time Defenses Against Package Hallucination in LLM-Generated Code* (arXiv 2608.22652); *Leveraging Large Language Models to Detect npm Malicious Packages* (ICSE 2025); and the **brand-new LLMSC workshop at FSE 2026**. If AI agents are part of the product picture, this sub-beat may matter more than the classical one — and it is early enough that a small number of papers constitutes the whole literature.

**2. Several findings are directly load-bearing for engineering practice, not just map entries.** *Pinning Is Futile* (FSE 2025) and *Pinning or Floating?* (ASE 2025) both bear on any pinned-dependency or pinned-digest strategy; *Cosseter* (S&P 2026) is precisely GitHub Actions permission reduction; *Quantifying Security Issues in Reusable JavaScript Actions* (MSR 2024) targets the reusable-action surface that most CI workflows sit on; and *Six Million Fake Stars* (ICSE 2026) invalidates GitHub popularity as a trust signal. These are worth reading as engineering input, not only as competitive intelligence.
