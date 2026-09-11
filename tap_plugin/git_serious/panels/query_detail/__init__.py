"""git-serious-query-detail — one BloodHound query: the question, their Cypher, our Gryphon, what it needs,
and its answer on this grid. Spec: specs/spec-git-serious-query-pack.md (req-git-serious-query-page)."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, ClassVar

from tap_plugin.git_serious.panels import query_pack

if TYPE_CHECKING:
    from django.http import HttpRequest

    from tap_web.models import Panel

logger = logging.getLogger(__name__)

#: Rows the page renders inline before it says "and N more" — the answer is a table, not a dump.
ROW_CAP = 200


def run_seeded_search(search_id: str) -> dict[str, Any]:
    """Execute the pack's Search for this query and shape the answer for the template.

    Three states, never two: `ran` with rows (possibly zero — a clean bill is a fact), `absent` when the Search
    is not on this grid (the bundle was not imported), `failed` with the error text (an executor refusal is a
    fact about the language, and the page says so rather than rendering an empty table).
    """
    from tap_grid.models import Search
    from tap_grid.search import execute_search

    search = Search.objects.filter(entity_id=search_id).first()
    if search is None:
        return {"state": "absent"}
    try:
        envelope = execute_search(search, inputs={})
    except Exception as exc:  # noqa: BLE001 — the page reports the executor's refusal verbatim
        logger.warning("[044d] bloodhound pack search %s failed: %s", search_id, exc)
        return {"state": "failed", "error": str(exc)}
    payload = envelope.get("results", envelope) if isinstance(envelope, dict) else {}
    rows = list(payload.get("rows") or [])
    nodes = list(payload.get("nodes") or [])
    columns = list(rows[0].keys()) if rows else []
    # Cells in column order, so the template never has to index a dict by a variable key.
    cells = [[row.get(c) for c in columns] for row in rows[:ROW_CAP]]
    return {
        "state": "ran",
        "rows": cells,
        "row_count": len(rows),
        "truncated": max(0, len(rows) - ROW_CAP),
        "node_count": len(nodes),
        "columns": columns,
        "total_count": (payload.get("info") or {}).get("total_count")
        if isinstance(payload.get("info"), dict)
        else None,
    }


class GitSeriousQueryDetailPanelType:
    slug: ClassVar[str] = "git-serious-query-detail"
    label: ClassVar[str] = "git-serious Query"
    view: ClassVar[str] = "git_serious/panels/query_detail.html"
    css: ClassVar[list[str]] = ["git_serious/css/secrets.css", "git_serious/css/queries.css"]
    js: ClassVar[list[str]] = []
    editor_view: ClassVar[str] = ""
    config_defaults: ClassVar[dict[str, Any]] = {}

    @classmethod
    def get_view_context(cls, panel: Panel, request: HttpRequest) -> dict[str, Any]:
        bh_id = (request.GET.get("id") or "").strip() if request else ""
        if not bh_id:
            return {"state": "no_selection", "pack_url": "/git-serious/queries"}
        record = query_pack.query(bh_id)
        if record is None:
            return {"state": "not_found", "requested": bh_id, "pack_url": "/git-serious/queries"}
        q = query_pack.decorate(record)
        answer = run_seeded_search(q["search_id"]) if q["seeded"] else {"state": "not_seeded"}
        # Neighbours in the pack, for the reader who came to browse: previous/next by the pack's order.
        rows = query_pack.overview()["rows"]
        idx = next((i for i, r in enumerate(rows) if r["id"] == bh_id), -1)
        prev_q = rows[idx - 1] if idx > 0 else None
        next_q = rows[idx + 1] if 0 <= idx < len(rows) - 1 else None
        return {
            "state": "found",
            "q": q,
            "answer": answer,
            "pack": query_pack.load_pack(),
            "stage": query_pack.STAGES.get(q["stage"], {}),
            "prev_q": prev_q,
            "next_q": next_q,
            "pack_url": "/git-serious/queries",
        }
