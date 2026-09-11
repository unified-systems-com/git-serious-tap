# git-serious — Secrets: held where, used by whom, and the names nothing defines

> First pass, 2026-09-11 (git-serious-tap#78), on the day Actions secret NAMES landed on the grid
> (tap-plugin-github-core PR# 105). Depth follows what the grid can say today; the `Feature:` /
> `Milestone:` marker lines are inert prose until tap#288 lands.

## Philosophy

*Which credentials does this estate hold, who actually uses each one, and what runs on a name nobody
defined?*

GitHub's API returns a secret's **name** and never its value, so a secrets page is a page about
plumbing, not about material: where each name is held (organisation, repository, environment), how far
GitHub's visibility rule lets it reach, and which workflow files name it — a claim about the file, since
what a run consumed is not observable. The page earns its place with the two things a listing cannot
show. First, a workflow that names a secret **no scope defines**: GitHub hands the step an empty string
and the job runs green doing the wrong thing, silently — the finding is the absence, and it is recorded
on the workflow, never minted as a node, because minting a secret from a reference would assert a
credential exists on the evidence that somebody typed its name. Second, the inverse: a live credential
**nothing consumes**.

Three states, never two, throughout: *never referenced* is not fine; *cannot find* is not broken (on
this estate every such name is vestigial, left behind when the organisation went public); a workflow
whose body was never read has secrets that are *unknown*, not none; a `selected` org secret whose list
the grid does not hold *reaches somewhere we cannot see*.

The pages pull what the grid already knows about each consumer — its triggers (a `pull_request_target`
workflow holding a secret runs it on someone else's input), its runs in the collected window, its
repository's visibility and criticality, its environments' protection rules, and, when zizmor is
installed, the findings on the file — because that context is what turns a name into a risk statement.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target:
**self** milestone. Prior art: `doc-git-serious-cicd-security-prior-art.md` §6 item 3 (*granted vs
used*), CICD-SEC-6 (insufficient credential hygiene).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-secrets | [The secrets page](#the-secrets-page) | Implemented | `/git-serious/secrets` — estate rollup, the names nothing defines, a card per secret, the rows-mode table beneath |
| req-git-serious-secret-page | [The secret page](#the-secret-page) | Implemented | `/git-serious/secret?secret_id=…` or `?name=…` — one secret, or one unfound name, in full |

### The secrets page
----
RID: `req-git-serious-secrets`

Status: `Implemented`
Feature: `table-stakes`
Milestone: `self`

`/git-serious/secrets`, in the navigation. Two slots: `overview` mounts `git-serious-secrets-overview`,
this plugin's first custom panel type; `named` mounts a standard table over the projection *what every
read workflow names, and cannot find* (rows mode, tap#432; `ORDER BY missing DESC`).

The overview reads top to bottom: the kind line and title (*N secrets the estate holds*, names only);
a subject block — defined by scope, in use (workflows and repositories naming them), never referenced,
cannot find (names and workflows), files read of files total with the unread count named as
*unknown, not none*; the section **Named in workflows, defined nowhere we can see** — one row per name
with the workflows and repositories naming it, whether every scope was read for every one of them, and
an *exposed trigger* badge when a naming workflow runs on someone else's input; the section **Each
secret** — a card per secret (name, holder kind and label, visibility, consumers and repositories or
*never referenced*, derived reach with *N of them never name it*, created/updated age, and secret-
handling findings when the scanner is present); provenance collapsed.

#### Implementation

`tap_plugin/git_serious/panels/secrets.py` — `Estate`: one read of the secret nodes, both edges, every
workflow, repository, environment, the runs by workflow id and (optionally) zizmor's `FLAGS_WORKFLOW`
edges; `secret_facts`, `phantoms`, `overview`. `panels/secrets_overview/__init__.py` renders
`templates/git_serious/panels/secrets_overview.html`; `static/git_serious/css/secrets.css` carries the
finding page's type scale. Registered in `apps.py::ready`. Bundle `grift/secrets.grift.json`. Panel
config: `workflow_page_template`, `findings_page_template`, `secret_page_template`, `name_page_template`
— URL templates the instance names; each renders only when the page exists on the grid.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-secrets-1 | Every Secret, Its Holder, Its Consumers | Implemented | Every `actions_secret` node renders as a card with its holder (from `DEFINES_SECRET`) and the workflows naming it (from `REFERENCES_SECRET`); a secret with none is marked *never referenced*. | `tests/test_git_serious_secrets.py` |
| req-git-serious-secrets-2 | The Names Nothing Defines | Implemented | Every distinct name (case-folded) in any workflow's `tags.secret_refs.unresolved` renders as a row with its workflow and repository counts and whether every scope was read for all of them; spellings are listed. | same |
| req-git-serious-secrets-3 | Read Is Not Whole | Implemented | The subject block states files read of files total and names the unread count as unknown, not none. | same |
| req-git-serious-secrets-4 | Exposure Is Grid-Derived | Implemented | A consumer starting on `pull_request_target`, `workflow_run`, `issue_comment` (or the other exposed triggers) marks its secret and its name row *exposed trigger*. | same |

### The secret page
----
RID: `req-git-serious-secret-page`

Status: `Implemented`
Feature: `table-stakes`
Milestone: `self`

`/git-serious/secret`, not discoverable. `?secret_id=<entity id>` renders one secret: kind line
(*organisation / repository / environment secret*), the name, holder and visibility, badges (in use /
never referenced, exposed, same name elsewhere); a subject block (holder, visibility, created and
updated with age, used by); **Where it reaches** — derived from GitHub's rule for the scope, with the
selected list marked *not observable* until github-core#108 records it, and *N of them never name it*
when reach exceeds use; **Who uses it** — each consuming workflow with its triggers (exposed ones
marked), runs in the collected window and last conclusion, findings on the file, repository visibility
and criticality; **Does this matter here?** — exposure, reach vs use, age (*never rotated since it was
set*), same name at another scope (*two credentials, not one*), findings; provenance collapsed.

`?name=<NAME>` renders the same page for a name no scope defines: who names it, with each row's scopes
read, spellings, exposure, and what an empty string at runtime means. A `?name=` that matches a real
secret renders that secret. A bad or unknown parameter renders a not-found state, never a 500.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-secret-page-1 | Reach Is Derived, Third State Kept | Implemented | `all` → every repository (count); `private` → private/internal repositories (count, none on an all-public estate); `selected` → *not observable* until the list is on the grid; repository/environment → the holder. | `tests/test_git_serious_secrets.py` |
| req-git-serious-secret-page-2 | Consumers Carry Their Context | Implemented | Each consumer row carries triggers with exposed ones marked, runs in window, last conclusion, and findings when the scanner is present. | same |
| req-git-serious-secret-page-3 | A Name Is A Page Too | Implemented | `?name=` for an unresolved name renders its workflows, scopes read, spellings; for a defined name renders that secret; for nothing renders not-found. | same |
| req-git-serious-secret-page-4 | Bad Input Is A State | Implemented | A malformed `secret_id` or an absent parameter renders a state, not an error. | same |

## Out Of Scope (v0)

Secret values (GitHub never returns them). Which environment a job selects at runtime (chosen at
runtime; a same-name secret at two scopes renders as two credentials). The `selected` repository list
(github-core#108). A per-repository secrets slot on the repository page (mount the overview with a
`repo` pin once the derivation takes one).
