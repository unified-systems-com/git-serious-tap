# git-serious — The workflow page

> **First light, 2026-09-02** (viz-git-serious session; git-serious-tap#6). The page is the SURFACE on
> which two table-stakes capabilities land — [reliability history](spec-git-serious-reliability-history.md)
> and [time and money](spec-git-serious-time-and-money.md) — and it carries a placeholder for the
> workflow-scoped machinery view. This spec owns the page's shape and the element ranking; the
> capabilities own their claims. `Feature:` / `Milestone:` marker lines follow the corpus convention.

## Philosophy

*Should I trust this red, and where are my ten minutes going?* — asked of ONE workflow.

Every incumbent answers with a run list and a duration chart plotted against a run index. None
places runs on a real time axis, so cadence — the nightly that stopped, the PR storm, the schedule
that drifted — has to be inferred. None holds the workflow *as written*, so "why is this run an
outlier" stops at "slower than p95". git-serious holds configuration, runs and the relationships
between them, with history; the page is where that difference becomes visible: a sparkline of
elapsed time at actual start time with the workflow's own baseline, the declared machinery with the
latest run painted on, and — later — configuration changes on the same axis as the runs.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature
target: **self** milestone (git-serious-tap epic #1). Pulled by git-serious-tap#6.

## Prior Art

The 2026-09-02 survey of workflow-level pages (GitHub Actions usage/performance metrics, GitLab CI/CD
analytics, CircleCI Insights, Buildkite, Datadog CI Visibility, Jenkins/Blue Ocean, BuildPulse,
Trunk, Argo, LinearB/Sleuth) — recorded in the git-serious-tap#6 thread; its convergence matrix is
the element ranking below. Two findings shaped the page: **only Jenkins' classic build-time trend
positions runs on a time axis** (everything else uses a run index or period buckets), and the
GitHub run-timing endpoints are closing down with no successor that carries workflow detail, so
minutes are DERIVED from job timestamps and billable minutes are *not observable* by API.

Provenance: **documented** unless marked *observed* (a running instance on 2026-09-02) or *inferred*.

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-workflow-page | [The workflow page](#the-workflow-page) | In Development | Surface for reliability history + time and money; parameterised by workflow id |
| req-git-serious-workflow-page-elements | [Element ranking](#element-ranking) | Proposed | The ranked list, each element naming the capability it serves and the data it needs |

### The workflow page
----
RID: `req-git-serious-workflow-page`
Status: `In Development`
Feature: `table-stakes`
Milestone: `self`

One page at `/git-serious/workflow?workflow_id=<GitHub numeric workflow id>` shows one workflow
across its collected runs: a machinery slot at the top, the workflow's identity, and its runs
newest first. Every panel derives from the grid through searches that declare `workflow_id` as an
integer input; the page passes the URL parameter to them, coerced by the search's own schema
(tap `inputs_from_query`), so the page is a query with a parameter, never a special-cased view.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-workflow-page-1 | One Workflow, Its Runs | Implemented | Opening the page with a valid `workflow_id` shows that workflow's identity row and every collected run of it, newest first, with trigger, branch, conclusion, timestamps and elapsed; an unknown id shows empty panels, never another workflow's runs. | *Observed* 2026-09-02 on the viz-git-serious instance: workflow 344142324 → 1 identity row, 14 runs. |
| req-git-serious-workflow-page-2 | Machinery Slot | Proposed | The top slot renders github_core's machinery projection scoped to this workflow (declared jobs, needs-edges, actions, environments, secrets; latest run's job conclusions painted on). | Placeholder text panel until github-core#28 / git-serious-tap#35 ship the module. |
| req-git-serious-workflow-page-3 | Outlier Against Its Own Baseline | Implemented | Each run's elapsed time carries its ratio to the median of the workflow's other successful runs with the same trigger, in three states: slower than baseline, within, not enough history (sample size shown). | Client-side over the loaded rows (tap `elapsed` formatter); server-side once Gryphon has a median. |
| req-git-serious-workflow-page-4 | Reachable From The Wall | Proposed | Every row of the status wall links to its workflow's page. | Needs the workflow id on the run node (present as `configuration.workflow_id`) — a `history` link column. |

---
### Element ranking
----
RID: `req-git-serious-workflow-page-elements`
Status: `Proposed`
Feature: `table-stakes`
Milestone: `self`

Ranked by (incumbent convergence × what our model adds), each naming the capability it serves and
whether github_core collects the data today. Elements 1–7 need no new permission.

| # | Element | Serves | Data | Collected today |
| --- | --- | --- | --- | --- |
| 1 | Machinery: declared `workflow_job` graph with the latest run's job conclusions; skipped/missing jobs as gaps | machinery projection | declared jobs + needs; run jobs | yes |
| 2 | Sparkline: elapsed per run at actual `run_started_at`; failures coloured; the median as a hairline; cadence reads from the spacing | reliability history, time and money | `run_started_at`, `completed_at`, `conclusion` | yes — with a defect: `completed_at` is the API's `updated_at` (github-core#46) |
| 3 | Outlier ratio against the workflow's own baseline, per trigger | time and money | as above + `event` | yes (ACID -3) |
| 4 | Outcome strip: success / failure / other / **not observed** | reliability history | `conclusion`; observation gaps | yes |
| 5 | Per-job aggregate: slowest job, most-failed job, share of duration; step breakdown | time and money | job + step timestamps | yes (steps in `configuration.steps`, unused) |
| 6 | Critical path of the latest run (longest `needs` chain by timestamps) | time and money | declared `needs` + job timestamps | yes — derivable; only Datadog has it |
| 7 | Trigger / branch split (default branch vs PR vs schedule) | reliability history | `event`, `head_branch` | yes |
| 8 | Queue time, run and job | time and money | run/job `created_at` | **no** — github-core#47 |
| 9 | Attempt awareness: attempt N of M; first-attempt vs final success | reliability history | `run_attempt` | **no** — github-core#47 |
| 10 | "What changed" strip: config edits (pins, `runs-on`, `needs`) on the sparkline's axis | what changed (the tenth feature) | workflow history on the grid | partial — history kept; nothing aligns the layers yet |
| 11 | Minutes consumed (derived, labelled as an estimate) | time and money | job durations × runner label | derivable; billable minutes not observable |
| 12 | Actor split (human / bot / manual by whom) | reliability history | `actor`, `triggering_actor` | **no** — github-core#47 |
| 13 | Failure-reason clustering, flaky tests | reliability history | logs, test reports | no; outside Actions-read; defer |
| 14 | Alerting | tell me when it breaks | thresholds | defer |

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-workflow-page-elements-1 | Sparkline On A Time Axis | Proposed | The sparkline places each run at its actual start time over the collected window; two runs a day apart are twice as far apart as two an hour apart. | The switching argument; nobody in the survey but Jenkins' legacy timeline does it. Load the data-visualization skill before building it. |
| req-git-serious-workflow-page-elements-2 | Three-State Outcome | Proposed | The outcome strip distinguishes not-observed from every real outcome; a window with no collected run renders as a gap, never as green. | Same rule as the status wall (req-git-serious-status-wall-1). |
