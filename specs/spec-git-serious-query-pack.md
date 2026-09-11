# git-serious — The BloodHound query pack: their questions, our Gryphon, an honest state for each

> First pass, 2026-09-11 (git-serious-tap#80), from the BloodHound GitHub parity assessment of the same day
> (tap `docs/misc/doc-dev-bloodhound-parity-pass.md`). The pack is CONTENT the plugin ships; the sample
> organisation, the oracle answers and the tests over them live in gryphon-playground (its issue #8), not here.

## Philosophy

*Take the best-known attack-path corpus for GitHub and make every question in it legible on the TAP grid.*

SpecterOps ships 79 saved queries (87 files, 8 with two variants) with its BloodHound GitHub extension —
posture checkboxes, branch-protection gaps, app and token reach, and the reachability walks that are the
point of an attack-path graph. A rule pack is transferable knowledge (the impressions register's item 4);
intent stays local. The pack makes the transfer legible one query at a time: the question in plain words,
their Cypher verbatim and attributed, our Gryphon, what the grid must hold for it, and — where it runs —
the answer here, executed live.

Three states, never two, is the whole design. A translation either **runs**, or is **written and waiting**
on a named collector build, or is **blocked** on a named Gryphon construct with the break-glass hatch
stated, or asks about something this organisation **cannot expose** (Enterprise, SAML, another cloud). A
page never renders an empty table for a query whose types are not on the grid, because that empty table
would read as a clean bill; it says which build makes the query askable instead.

## Roadmap Alignment

Feature: BloodHound parity (tap-plugin-github-core#109 is the collector side; this is the surface).
Milestone: git-serious-friends.

## Requirements

| RID | Title | Status | Summary |
| --- | --- | --- | --- |
| req-git-serious-query-pack | [The pack](#the-pack) | Implemented | `data/bloodhound_queries.json` + `/git-serious/queries` — every query, by the stage that answers it, with the ladder |
| req-git-serious-query-page | [The query page](#the-query-page) | Implemented | `/git-serious/query?id=…` — the question, both texts, needs, hatch, and the live answer for the ones that run |

### The pack
----
RID: `req-git-serious-query-pack`

Status: `Implemented`

`tap_plugin/git_serious/data/bloodhound_queries.json` is the pack: one record per BloodHound query id with
`sources[]` (every upstream variant verbatim, repos, pinned commits, paths), their description, our `about`,
`gryphon` (a list of lines or null), `status` ∈ runs | expressible | blocked | not_observable, `stage` ∈
today | A | A2 | B | C | later | na (each stage naming the github_core issue that delivers it), `needs`,
`returns`, `blocked_on`, `hatch`, `caveat`. Translations are authored per query, not regex-rewritten;
the page shows exactly what the file says.

`grift/queries.grift.json` is GENERATED from the pack by `scripts/build_query_pack_grift.py`: the two
pages, the two panels, and one Gryphon `Search` per translation whose `status` is `runs` — the Search entity
id is `panels/query_pack.py::search_entity_id(bh_id)`, the same function the query page calls, so the
Search a page executes is the Search the bundle seeded (derive a fact once). A translation that is not
runnable is NOT seeded: a Search over types that do not exist yet would execute to an empty answer.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-query-pack-1 | Every Upstream Query, Attributed | Implemented | The pack carries every saved query, documentation-only query and privilege-zone rule from both upstream repositories at their pinned commits, verbatim, with licence and paths; ids with two variants keep both. | `tests/test_git_serious_query_pack.py` |
| req-git-serious-query-pack-2 | Four States, Named Stages | Implemented | Every record has one of the four statuses and one of the seven stages; a `blocked` record names its construct and a hatch; a `runs`/`expressible` record has Gryphon; an `expressible`/`blocked` record's stage names an issue. | same |
| req-git-serious-query-pack-3 | Generated Bundle Is Current | Implemented | `scripts/build_query_pack_grift.py --check` passes against the committed bundle; exactly the `runs` translations are seeded; every seeded Search's id is `search_entity_id(id)`. | same |
| req-git-serious-query-pack-4 | The Ladder Is Derived | Implemented | The pack page's cumulative ladder is computed from the records; no count is typed. | same |
| req-git-serious-query-pack-5 | Every Seeded Query Parses | Implemented | Each `runs` translation parses under the Gryphon parser; a translation the parser rejects fails the suite, so a grammar change cannot leave a seeded Search silently broken. | same |

### The query page
----
RID: `req-git-serious-query-page`

Status: `Implemented`

`/git-serious/query?id=<bloodhound-id>` renders one record in the format the finding and secret pages
established: kind line, title, the subject block, sections each opened by a meaning line, provenance. Its
sections: *What it asks* (ours, then theirs, then the caveat the answer must be read with); *Their Cypher,
our Gryphon* side by side, the Gryphon captioned by its state; *What it needs on the grid* (types and
edges as chips, the blocker, the hatch, the returned columns); *The answer on this grid* — for a seeded
query the Search is executed at render over the read-only connection and rendered as a table, with zero
rows stated as a fact beside the caveat; for the others, the reason it was not run. Previous / next follow
the pack's order.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-query-page-1 | Bad Input Is A State | Implemented | No `id`, or an id not in the pack, renders a state with a link back to the pack — never an error. | `tests/test_git_serious_query_pack.py` |
| req-git-serious-query-page-2 | The Answer Has Three States | Implemented | A seeded query renders `ran` (rows, possibly zero), `absent` (bundle not imported) or `failed` (executor text); an unseeded query renders `not_seeded` with the stage that makes it runnable. | same |
| req-git-serious-query-page-3 | Nothing Rendered From Nothing | Implemented | An `expressible`, `blocked` or `not_observable` query never shows an empty results table. | template: the *not run* branch |

## Out Of Scope (v0)

- Executing the `expressible` translations on a grid that has the types (they seed automatically once the
  pack marks them `runs`; the pack is the switch).
- The reachability module runner the `blocked` records point at — its own issue (git-serious-tap#80, part 2).
- Per-query result history ("this answer changed since last week") — the grid keeps field history; a
  page over it is the *what changed* spec's.
