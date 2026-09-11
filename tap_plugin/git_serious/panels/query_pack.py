"""The BloodHound query pack — shared loader for the pack page, the query page and the GRIFT generator.

The pack is CONTENT: `data/bloodhound_queries.json` carries SpecterOps' saved queries (attributed, at pinned
commits) and our Gryphon translation, status and stage for each. It is not fixture data — no nodes, no
expected rows — so it ships in the wheel like a template does. One loader, one id derivation, one stage
vocabulary; the generator script that writes `grift/queries.grift.json` imports from here so the Search a
page executes is the Search the bundle seeded (derive a fact once).

Spec: specs/spec-git-serious-query-pack.md (req-git-serious-query-pack, req-git-serious-query-page).
"""

from __future__ import annotations

import json
import logging
import uuid
from functools import lru_cache
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

PACK_PATH = Path(__file__).resolve().parent.parent / "data" / "bloodhound_queries.json"

#: uuid5 namespace for the pack's Search entities: `search_entity_id(bh_id)` is the SAME value in the
#: generator and in the page, so the page never has to look a Search up by name.
_SEARCH_NS = uuid.UUID("7b1f0a2e-6c3d-4f9a-9e2b-0d5c8a1b4e77")

#: Order pages list stages in; label is the human phrase, `issue` the build that delivers it.
STAGES: dict[str, dict[str, str]] = {
    "today": {"label": "runs today", "issue": ""},
    "A": {"label": "after settings (slice A)", "issue": "tap-plugin-github-core#110"},
    "A2": {"label": "after ruleset rule types (slice A2)", "issue": "tap-plugin-github-core#114"},
    "B": {"label": "after the people graph (slice B)", "issue": "tap-plugin-github-core#111"},
    "C": {"label": "after roles and PAT grants (slice C)", "issue": "tap-plugin-github-core#112"},
    "later": {"label": "needs a type not yet scheduled", "issue": ""},
    "na": {"label": "not observable for this organisation", "issue": ""},
}
STAGE_ORDER = list(STAGES)

STATUS_LABEL: dict[str, str] = {
    "runs": "runs",
    "expressible": "written, waiting on data",
    "blocked": "blocked on Gryphon",
    "not_observable": "not observable",
}

SEVERITY_ORDER = ["critical", "high", "medium", "low", "tier-zero", "enterprise", "demo", "unlisted"]


@lru_cache(maxsize=1)
def load_pack() -> dict[str, Any]:
    """The pack, read once per process. A missing or malformed file is a hard error: the pack is code."""
    return json.loads(PACK_PATH.read_text())


def queries() -> list[dict[str, Any]]:
    return list(load_pack()["queries"])


def query(bh_id: str) -> dict[str, Any] | None:
    return next((q for q in queries() if q["id"] == bh_id), None)


def search_entity_id(bh_id: str) -> uuid.UUID:
    """Deterministic Search entity id for a pack query — shared by the generator and the page."""
    return uuid.uuid5(_SEARCH_NS, f"git_serious.bloodhound_pack.search:{bh_id}")


def is_seeded(q: dict[str, Any]) -> bool:
    """Only translations that RUN on a github_core grid are seeded as Searches; the rest are shown as text.

    A Search whose types do not exist yet would fail at execution and read as an empty answer.
    """
    return q["status"] == "runs" and bool(q.get("gryphon"))


def gryphon_text(q: dict[str, Any]) -> str:
    lines = q.get("gryphon") or []
    return "\n".join(lines)


def decorate(q: dict[str, Any]) -> dict[str, Any]:
    """The record plus the display fields every template wants."""
    stage = STAGES.get(q["stage"], STAGES["later"])
    # A need that is an entity-type slug (`plugin__type`) gets the type's icon; prose needs stay chips.
    type_needs = [n for n in q.get("needs") or [] if "__" in n and " " not in n]
    return {
        **q,
        "stage_label": stage["label"],
        "stage_issue": stage["issue"],
        "status_label": STATUS_LABEL.get(q["status"], q["status"]),
        "gryphon_text": gryphon_text(q),
        "seeded": is_seeded(q),
        "search_id": str(search_entity_id(q["id"])) if is_seeded(q) else "",
        "url": f"/git-serious/query?id={q['id']}",
        "variant_count": len(q.get("sources") or []),
        "type_needs": type_needs,
        "other_needs": [n for n in q.get("needs") or [] if n not in type_needs],
        "primary_type": type_needs[0] if type_needs else "",
    }


def overview() -> dict[str, Any]:
    """Counts for the pack page: by status, by stage, by severity — derived from the records, never typed."""
    rows = [decorate(q) for q in queries()]
    by_status: dict[str, int] = {}
    by_stage: dict[str, int] = {}
    by_severity: dict[str, int] = {}
    for r in rows:
        by_status[r["status"]] = by_status.get(r["status"], 0) + 1
        by_stage[r["stage"]] = by_stage.get(r["stage"], 0) + 1
        by_severity[r["severity"]] = by_severity.get(r["severity"], 0) + 1
    rows.sort(key=lambda r: (STAGE_ORDER.index(r["stage"]), SEVERITY_ORDER.index(r["severity"]), r["name"]))
    ladder = []
    running = 0
    for key in ("today", "A", "A2", "B", "C"):
        running += sum(1 for r in rows if r["stage"] == key and r["status"] in ("runs", "expressible"))
        ladder.append(
            {"stage": key, "label": STAGES[key]["label"], "cumulative": running, "issue": STAGES[key]["issue"]}
        )
    return {
        "pack": {k: v for k, v in load_pack().items() if k != "queries"},
        "rows": rows,
        "total": len(rows),
        "by_status": by_status,
        "by_stage": by_stage,
        "by_severity": by_severity,
        "ladder": ladder,
        "stages": [{"key": k, **v, "count": by_stage.get(k, 0)} for k, v in STAGES.items()],
        "seeded": sum(1 for r in rows if r["seeded"]),
        "blocked_hatch": sum(1 for r in rows if r["status"] == "blocked" and r.get("hatch")),
    }
