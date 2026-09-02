# git-serious — Agent-operable review — the third player reads the graph

> **Skeleton.** Header, sources, the top-line requirement and its done-test only, written in the
> 2026-09-02 convergence (git-serious-tap#26 → tap#211). Depth follows the MVP trim. The
> `Feature:` / `Milestone:` marker lines are read by the corpus parser once tap#288 lands and are
> inert prose until then. Milestone targets are a DRAFT mapping for review, not a ruling.

## Philosophy

*Can my agent, or yours, review this system without a human driving every click?*

The attacker side already automates; the defender's loop must be at least as automated, so the Player-3 posture is table stakes for security and an innovation for the product: the graph, the finding taxonomy and each collector's permission needs shipped as machine-legible, described, queryable metadata from day one, and a read-only surface (MCP first) an external agent can operate. v0 AI is read-only: it reads, summarises and suggests, and never writes core graph state.

## Roadmap Alignment

Governing step: `step-products-git-serious-self` in `plan/road-products.md` (tap core). Feature target: **everyone** milestone (git-serious-tap epic #3).

## Prior Art

Prior art §6 item 11 ([`doc-git-serious-cicd-security-prior-art.md`](../docs/doc-git-serious-cicd-security-prior-art.md)); the README's fourth promise (*agent-driven security review*); `plan/product-map.md`'s note that the MCP surface may be worth pulling into git-serious early; `specs/spec-ai-integration.md` (tap core) for the read-only rule.

Provenance of every claim in this skeleton: **documented** (drawn from the sources above) unless
marked *observed* or *inferred* (tap#206's provenance markers).

## Requirements

| RID | Name | Status | Notes |
| --- | --- | :---: | --- |
| req-git-serious-agent-operable-review | [Agent-operable review — the third player reads the graph](#agent-operable-review-the-third-player-reads-the-graph) | Proposed | Innovation (register disposition CANON unless noted); falsifier field is the MVP entry gate |

### Agent-operable review — the third player reads the graph
----
RID: `req-git-serious-agent-operable-review`
Status: `Proposed`
Feature: `innovation`
Milestone: `everyone`

An external AI agent can, through a read-only surface, enumerate the account's graph, run the shipped queries and principles, and produce a review — with every finding traceable to the collected fact — without any write path to the grid.

**Falsifier (MVP entry gate, tap#211):** *(unfilled — required before this innovation may enter the MVP, tap#211; a proposal that cannot say what would falsify it is a hunch)*

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-git-serious-agent-operable-review-1 | Agent Review, Read-Only | Proposed | An agent holding only the read-only surface produces a review of the observed account naming at least one finding with its graph path, and no call available to it can mutate a node, edge or dimension. | The done-test: the feature's Status flips only when this is OBSERVED on a running instance. |

---
