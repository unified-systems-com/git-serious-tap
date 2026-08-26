---
title: The Linux kernel pipeline — a non-forge CI/CD system, and the delta from our model
date: 2026-08-26
status: research
audience:
  - developer
  - llm
related_docs:
  - docs/doc-git-serious-cicd-shape-review.md
---

> **Research pass, 2026-08-26.** How the kernel is developed, built, tested, signed and released without pull requests, rulesets or a required check — and what a kernel collector would imply for a forge-neutral vocabulary. Cursory research pass, 2026-08-26. Written by an AI research agent from public sources and
> read-only API calls; claims carry citations, and the report flags what it could not verify.
> Nothing here is canon — requirements live in specs, the fence lives in the roadmap.

# The Linux kernel's development pipeline, seen through git-serious

Cursory research pass, 2026-08-26. Purpose: ground how the kernel is developed, built, tested,
released and signed — a non-GitHub pipeline — and size the delta against what git-serious
models today (`github_core` collector; proposed forge-neutral `git_core` vocabulary, tap#144).
Time-sensitive facts carry a date. Items marked **[unverified]** come from background knowledge
where the primary source was unreachable this session (git.kernel.org and lore.kernel.org sit
behind the Anubis anti-scraper wall; kernel.org docs, korg docs, b4 docs, GitHub mirrors, LWN
and releases.json were reachable).

---

## 1. How code flows — the identity + authority model

**Cadence.** A mainline release every 9–10 weeks: a ~2-week *merge window* (≈1,000 patches/day
merged) followed by ~7 weeks of weekly `-rcN` candidates, typically to rc6–rc9; ≈13,000
changesets per cycle [1][2]. Today (releases.json, 2026-08-26): mainline **7.2** (2026-08-16),
stable 7.1.10, six longterm lines (6.18 → 5.10, all re-released 2026-08-23 in one batch), and
`next-20260826` [3].

**Path of a patch.** Developer → subsystem mailing list (archived at lore.kernel.org) → subsystem
maintainer's git tree → **linux-next** (daily integration of all maintainer trees; "a snapshot of
what the mainline is expected to look like after the next merge window closes", maintained by
Mark Brown) → Linus's tree during the merge window → stable/longterm backports [1][4].
Maintainers don't open pull requests on a platform: they send an **email** produced by
`git request-pull` pointing at a **PGP-signed tag**; "Linus will only accept pull requests based on
a signed tag", and the tag message becomes the merge-commit message [5]. Linus's own release
tags are PGP-signed too (GitHub shows `v7.2` tagged by torvalds@linux-foundation.org with a PGP
block; GitHub reports `verified: false, reason: unknown_key` — the trust root is the kernel.org
keyring, not the forge) [6]. Linus's tags were already signed at v3.0 (July 2011), i.e. before the
compromise — the post-2011 change was making signed tags the *requirement for pulls*, not
inventing them [6][7].

**Authority is a text file + trust, not platform config.** `MAINTAINERS` in-tree is the ACL:
per-subsystem `M:` (maintainer), `R:` (designated reviewer), `L:` (list), `S:` (status:
Supported / Maintained / Odd Fixes / Orphan / Obsolete), `T:` (SCM tree), `F:`/`X:`/`N:`/`K:`
(file globs / exclusions / path regex / content regex) plus `W: Q: B: C: P:` (web, patchwork,
bugs, chat, subsystem profile) [8]. Today's file: 30,173 lines, ~3,291 sections, 4,382 `M:`
lines (2,058 distinct people), 853 `T: git` trees, 284 distinct lists, 807 Supported /
2,233 Maintained / 141 Orphan / 106 Odd Fixes [8]. `scripts/get_maintainer.pl` derives
"who must be CC'd" from a diff — the kernel's CODEOWNERS, evaluated client-side by convention,
never enforced by a server.

**Provenance is in the commit message.** The DCO 1.1 `Signed-off-by:` chain (each hand-off adds a
sign-off; "records … maintained indefinitely and … publicly redistributed") originated in the
kernel in 2004 under SCO-lawsuit pressure and is now the Linux Foundation's DCO — the same text
TAP's own `.githooks/prepare-commit-msg` appends [9][10]. Review authority is carried as
trailers: `Acked-by` (approval by someone not involved, possibly partial), `Reviewed-by` (formal
technical-review statement), `Tested-by`, `Reported-by` + `Closes:`/`Link:` (lore URLs),
`Suggested-by`, `Co-developed-by` (must be followed by that co-author's sign-off), `Fixes: <12+
hex sha> ("subject")`, and `Cc: stable@vger.kernel.org` in the sign-off area to route into
stable [9]. **b4** (`b4 am/shazam/prep/send/trailers/ty/pr/kr`) is the tool that turns a lore
thread into an applied series, collects trailers from replies, refuses trailers whose `From:`
doesn't match the trailer address unless `-S`, adds a `Link:` to lore, and verifies attestations
[11][12].

## 2. How it is built and tested — no single required check

There is **no gate** in the GitHub-Actions sense: nothing blocks a merge mechanically. What stands
in for it is (a) a *constellation* of independent CI systems that all watch the same public trees
and email the same lists, (b) the maintainer's judgement, and (c) the -rc soak. The main actors:

| System | What it tests | Where results go |
|---|---|---|
| **KernelCI** (LF project; premier members Arm, Collabora, Google, Linaro, Microsoft, Qualcomm, Red Hat, TI…) — *Maestro* API/pipeline, LAVA labs, new dashboard.kernelci.org, `kci-dev` CLI [13][14] | builds + boot/tests across trees/arches/boards | dashboard, email, and **KCIDB** |
| **KCIDB** (kcidb.kernelci.org) — the *common results database* that independent CIs submit to; objects: `checkout`, `build`, `test`, `issue`, `incident`, keyed by `origin:` prefix, with `git_repository_url`/`git_commit_hash`/`patchset_hash`; submit via `kcidb-submit`/REST, view via dashboard [15] | aggregation | Grafana dashboard, notifications |
| **Intel 0-day / kbuild test robot (LKP)** — builds hundreds of trees + list patches across configs/arches, perf regressions; reports `kernel test robot <lkp@intel.com>` with a `Reported-by` tag **[scope unverified this session — repo docs only cover local use]** [16] | compile/perf | email to author + oe-kbuild-all list |
| **syzbot** (syzkaller) — continuous fuzzing of upstream, linux-next, subsystem trees; auto-bisects back to v4.19; controlled by `#syz fix:/test:/dup/invalid` email commands; dashboard syzkaller.appspot.com [17] | crashes | email + dashboard |
| **Red Hat CKI** — "CI-as-a-service": stable-rc, mainline, net-next, list patches via Patchwork; GitLab pipelines + Beaker hardware; DataWarehouse; submits to KCIDB [18] | build/boot/test | email to submitter/maintainer, KCIDB |
| **Linaro LKFT** — functional regression testing on Arm via LAVA, LTS/stable/mainline/next; reports to the stable list [19] | LTP/kselftest on boards | email, SQUAD |
| In-tree: **kselftest** (`tools/testing/selftests`, userspace, TAP output), **KUnit** (in-kernel unit tests via `kunit.py` under UML/QEMU, KTAP), **LTP** (external suite), plus KASAN/KCSAN/UBSAN/KFENCE/lockdep instrumentation and sparse/smatch/Coccinelle static analysis [20][21][22] | | consumed by the CIs above |

**Regression bookkeeping** is `regzbot` (linux-regtracking.leemhuis.info): `#regzbot
introduced:/fix:/summary:/relate:/duplicate:` commands in list mail; a regression counts as
resolved when a commit with a matching `Link:`/`Fixes:` lands in mainline or next [23].
**Stable review** is a 48-hour ACK/NAK window on a `-rc` queue published to the stable list,
patches must already be in mainline and ≤100 lines, be "obviously correct and tested"; security
patches bypass normal review via the security team [24].

So the "gate" is *social + temporal*: results arrive as email threads on the same archive the
patch lives in, and the maintainer decides. The closest machine-legible analogue to a required
check is a KCIDB/KernelCI regression object tied to a checkout hash.

## 3. How it is released and signed

- **Tarballs**: each release is signed by the *person* making it (Linus, Greg KH, Sasha Levin,
  Ben Hutchings…) with a detached `.sign` over the uncompressed `.tar`; verify with
  `gpg --verify`, keys fetched via WKD `gpg --locate-keys <user>@kernel.org` [25].
  `releases.json` publishes per release: `moniker` (mainline/stable/longterm/linux-next),
  `version`, `iseol`, `released.{timestamp,isodate}`, `source`, `pgp`, `patch.{full,incremental}`,
  `changelog`, `gitweb`, `diffview` [3].
- **Upload path**: `kup` — "any software uploaded to kernel.org is cryptographically verified
  against a list of pre-approved maintainers"; signature must be over the raw tar; the
  `git-archive-signer` backend publishes tarballs from **signed git tags** every 5 minutes [26].
- **Git tags**: Linus's release tags and every maintainer pull tag are PGP-signed (§1).
- **Security**: security@kernel.org is a private list of security officers; fixes go out
  immediately if public, otherwise ≤7 days (extensible to 14) after a fix exists; report details are
  confidential in perpetuity; the team does **not** assign CVEs [27].
- **CVEs**: the kernel became its own CNA on **2024-02-13** (Greg KH, Sasha Levin, Lee Jones);
  CVEs are assigned during the stable release process for security-relevant fixes, only for
  actively supported stable/LTS versions, announced on `linux-cve-announce`; disputes go to the
  subsystem maintainer; contact cve@kernel.org [28][29]. The philosophy is "any bugfix may be a
  CVE" — LWN flagged a "fire-hose of identifiers" (6.1 got 12,639 fixes in its first year). The
  per-CVE JSON/mbox records live in a public `vulns.git` tree on git.kernel.org **[layout
  unverified this session; volume of several thousand CVEs/year since 2024 from memory]**.
- **Stable cadence**: stable point releases "as-needed, typically weekly"; LTS lines start with a
  2-year EOL that gets extended (current EOLs: 6.18/6.12 → Dec 2028, 6.6/6.1 → Dec 2027,
  5.15/5.10 → Dec 2026) [30].

## 4. Credentials and blast radius

- **Accounts**: kernel.org accounts are "reserved for Linux kernel maintainers or high-profile
  developers"; a PGP key is mandatory and must carry signatures from **≥2 existing kernel.org
  account holders** (video keysigning allowed); SSH access via a PGP auth subkey or a FIDO2 key
  (`ed25519-sk`, resident + verify-required), the FIDO2 pubkey submitted *signed by the PGP key*.
  FIDO2 2FA is **optional** ("you can request that we switch to it") [31][32].
- **Keyring**: `pgpkeys.git` (keys/, trust-path graphs to Linus's key, scripts) + the keysigning
  map; anyone in `MAINTAINERS` `M:` or with an account qualifies for a free Nitrokey; the PGP
  guide recommends hardware-backed subkeys and TOFU+PGP over a pure web of trust [33][34].
- **2011 compromise** (discovered 2011-08-28, announced 08-31): multiple kernel.org hosts rooted
  via a trojan on a developer's machine that logged SSH keys; git repos believed intact because
  of hashing + signed tags. Recovery: monolithic "hera" replaced by split boxes, **gitolite** with
  ssh keys (no shell accounts, ever again), `kup` with mandatory personal GPG signatures replacing
  central auto-signing, mailing lists moved to vger, root limited to full-time admins, and the
  web-of-trust account requirement. Operating principle since: "assume that any part of the
  infrastructure can be compromised at any time" [7][35][34].
- **Transparency**: gitolite writes every `git-receive` (repo, user, refs, commits, optional push
  signature) to a public-inbox-format git log that others are asked to mirror — explicitly because
  LF IT staff have backend access [36].
- **Patch-level attestation**: **patatt** adapts DKIM — `X-Developer-Signature` /
  `X-Developer-Key` headers over the patch (ed25519, OpenPGP, OpenSSH keys), keys managed in a git
  ref keyring; `b4 am` shows ✓/✗ per patch and accepts DKIM as a weaker signal ("✓ Signed:
  DKIM/chromium.org"). `b4 send` via the kernel.org web endpoint *requires* a patatt key
  (`--web-auth-new/--web-auth-verify`) and writes every message to a public-inbox feed [11][12][37][38].
- **sigstore**: no mention in patatt, b4, or korg docs; I found no evidence of a kernel.org
  sigstore experiment **[absence-of-evidence, not verified]**.

Blast radius, in git-serious terms: the trust roots are *people's keys* (Linus's, Greg's, each
maintainer's), not platform tokens; a stolen kernel.org SSH key can push to one gitolite repo
(logged publicly) but cannot forge a signed tag, a signed tarball, or a patatt-signed patch.

## 5. Where git-serious's model fits, and where it doesn't

Mapping the kernel's objects onto the `git_core` vocabulary (repo, branch, pipeline run,
protection rule, release, identity — tap#144) and the `github_core` inventory (account, repo,
workflow, run, job, runner, app, OIDC issuer, rulesets/required checks planned):

| Kernel object | Nearest git_core / github_core shape | Verdict |
|---|---|---|
| Linus's tree, ~850 `T: git` maintainer trees, linux-next, stable trees | **repo** + **branch** (with a `role` facet: mainline / subsystem / integration / stable) | same shape; fan-in edges *between* repos (`MERGES_INTO`, `BACKPORTS_FROM`) are new |
| Signed release tag / tarball + `.sign` / releases.json row | **release** (+ signature + signer identity) | same shape; signature is PGP over a person, not a platform-verified badge |
| Pull request (email + signed tag) | GitHub PR | **different**: a PR is an *email* that references a tag; state lives in the archive and the merge commit |
| Patch series + cover letter (lore thread, message-ids, versions v1..vN) | nothing today (PR head commits are the closest) | **new node type** `patch_series` with `SUPERSEDES` versions; keyed by Message-ID |
| `MAINTAINERS` entry (`M/R/L/S/T/F`) | CODEOWNERS + protection rule + team | **different**: authority = text file + trust + convention; no server enforces it. Model as `subsystem` node with `MAINTAINS`/`REVIEWS`/`OWNS_PATHS` edges |
| Trailers (Signed-off-by, Reviewed-by, Acked-by, Tested-by) | PR review / approval | same *intent*, but carried in the commit body and cryptographically weak (b4 checks only From:-match) — model as `ATTESTS` edges with a strength facet |
| KernelCI/KCIDB checkout/build/test, syzbot bug, 0-day report, CKI run | **pipeline run** / job | same shape *per system*, but many origins and no repo-owned pipeline definition; KCIDB's `origin:` is the analogue of a workflow's provenance |
| KCIDB `issue`/`incident`, regzbot regression | (none — closest is a failed required check) | new: `regression` node with `INTRODUCED_BY`/`FIXED_BY` edges to commits |
| CVE (linux-cve-announce, vulns.git) | (none; Dependabot alert is a distant cousin) | new: `cve` node keyed by ID → `FIXED_BY` commit → `AFFECTS` stable versions |
| kernel.org account, PGP key, WoT signatures, FIDO2 key | **identity** + credential | same shape; credential is a key with a signature graph rather than a PAT/app |
| gitolite transparency log | audit log / push event | same shape, and *better*: it is public and mirrorable |
| Rulesets, required checks, environments, secrets, OIDC | (no kernel equivalent) | **absent**: nothing to collect; the "protection rule" is `S:`/`M:` plus Linus |

Genuinely different: email-driven (Message-ID is the primary key, not a PR number); no rulesets or
required checks; many independent CI systems that never block anything; authority encoded in
`MAINTAINERS` + web of trust rather than platform config; releases are signed by humans and
mirrored by a CDN, not built by a workflow. A **kernel collector** would read: lore.kernel.org
(public-inbox: `/<list>/<msgid>/raw`, `/t.mbox.gz`, `new.atom`, `git clone --mirror` of list
epochs, `?q=` Xapian search) [39][40]; `MAINTAINERS` from the git mirror; `releases.json` [3];
signed tags via `gh api` on the GitHub mirror or `git ls-remote` + local verify; KCIDB dashboard /
Maestro API via `kci-dev` [14][15]; syzbot dashboard (JSON export exists **[unverified]**);
regzbot pages [23]; `linux-cve-announce` + `vulns.git`; `pgpkeys.git` + the transparency log [33][36].

## 6. Demo potential

**Candidate story: "one patch, five trust boundaries."** Pick a recent CVE from linux-cve-announce
and walk backwards: CVE → `Fixes:`-tagged stable commit → mainline commit (`Link:` to lore) → the
lore thread (v1…vN, who Reviewed/Acked/Tested, patatt/DKIM attestation) → the maintainer's signed
pull tag → Linus's signed release tag → the signed tarball in releases.json → the six stable lines
it was backported into. Overlay KCIDB/syzbot results on the same commit hash, and the
`MAINTAINERS` entry that says who was *entitled* to merge it. Every hop is public, keyed by a hash
or a Message-ID, and needs **zero credentials** (the only auth surfaces are `kci-dev` writes and
Maestro triggers, which the demo never touches). The picture that lands: "here is a CI/CD system
with no platform, where every gate is a person with a key — and git-serious can still draw it."

Alternates: (b) the **web-of-trust graph** from `pgpkeys.git` (trust paths to Linus, ≥2-signature
account rule) — pure graph, very pretty in cytoscape; (c) the **CI-lab constellation** — KCIDB
origins × trees × architectures as a bipartite graph, showing which trees nobody tests.

**Effort, relative to the GitHub collector (M).** A read-only lore + MAINTAINERS + releases.json
+ signed-tag collector for story (a): **M** (public-inbox parsing and Message-ID threading are the
real work; the graph shapes are 5 new node types + ~8 edges). Web-of-trust (b): **S** (one git
clone, one GPG parse). CI constellation (c): **M–L** (KCIDB/Maestro schemas are broad and the
dashboard API is undocumented from the outside; Anubis blocks naive HTTP scraping of
git.kernel.org/lore, so the collector must speak git and public-inbox, not HTML). None of it
requires — or can even use — the GitHub-shaped `protection rule` / `secret` / `OIDC` vocabulary,
which is the useful pressure test for keeping `git_core` genuinely forge-neutral.

## 7. Sources

1. https://www.kernel.org/doc/html/latest/process/2.Process.html
2. https://www.kernel.org/category/releases.html
3. https://www.kernel.org/releases.json (fetched 2026-08-26)
4. https://www.kernel.org/doc/man-pages/linux-next.html
5. https://www.kernel.org/doc/html/latest/maintainer/pull-requests.html
6. GitHub API, torvalds/linux tag objects v3.0–v3.3 and v7.2 (`gh api repos/torvalds/linux/git/tags/<sha>`), 2026-08-26
7. https://lwn.net/Articles/464233/ (kernel.org's road to recovery, 2011)
8. https://raw.githubusercontent.com/torvalds/linux/master/MAINTAINERS (header + counts computed 2026-08-26)
9. https://www.kernel.org/doc/html/latest/process/submitting-patches.html
10. https://developercertificate.org/
11. https://b4.docs.kernel.org/en/latest/
12. https://b4.docs.kernel.org/en/latest/maintainer/am-shazam.html
13. https://kernelci.org/ ; https://docs.kernelci.org/
14. https://kci.dev/
15. https://github.com/kernelci/kcidb (README + doc/submitter_guide.md)
16. https://github.com/intel/lkp-tests
17. https://github.com/google/syzkaller/blob/master/docs/syzbot.md
18. https://cki-project.org/ ; https://cki-project.org/docs/
19. https://lkft.linaro.org/ ; https://lkft.linaro.org/about/
20. https://www.kernel.org/doc/html/latest/dev-tools/kselftest.html
21. https://www.kernel.org/doc/html/latest/dev-tools/kunit/index.html
22. https://www.kernel.org/doc/html/latest/dev-tools/testing-overview.html
23. https://linux-regtracking.leemhuis.info/regzbot/mainline/
24. https://www.kernel.org/doc/html/latest/process/stable-kernel-rules.html
25. https://www.kernel.org/signature.html
26. https://korg.docs.kernel.org/kup.html
27. https://www.kernel.org/doc/html/latest/process/security-bugs.html
28. https://www.kernel.org/doc/html/latest/process/cve.html
29. https://lwn.net/Articles/961978/ (kernel becomes a CNA, 2024-02-13)
30. https://www.kernel.org/category/releases.html
31. https://korg.docs.kernel.org/accounts.html
32. https://korg.docs.kernel.org/fido2.html
33. https://korg.docs.kernel.org/pgpkeys.html
34. https://www.kernel.org/doc/html/latest/process/maintainer-pgp-guide.html
35. https://lwn.net/Articles/457142/ (the 2011 compromise)
36. https://korg.docs.kernel.org/gitolite/transparency-log.html
37. https://github.com/mricon/patatt
38. https://b4.docs.kernel.org/en/latest/contributor/send.html
39. https://public-inbox.org/design_www.txt
40. https://korg.docs.kernel.org/lore.html

Not reachable this session (Anubis wall): git.kernel.org (`vulns.git`, tag pages, MAINTAINERS
plain view), lore.kernel.org (search help, linux-cve-announce). Claims depending on them are
flagged **[unverified]** above.
