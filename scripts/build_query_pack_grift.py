#!/usr/bin/env python3
"""Generate grift/queries.grift.json from the BloodHound query pack — the pages, the two panels, and one
Search per RUNNABLE translation.

Run from the plugin root after editing data/bloodhound_queries.json:

    python3 scripts/build_query_pack_grift.py            # rewrite the bundle
    python3 scripts/build_query_pack_grift.py --check    # exit 1 if the committed bundle is stale

Derive-once: the Search entity ids come from `panels/query_pack.py::search_entity_id`, the same function the
query page calls at render time, so the page executes exactly the Search this file seeded. The batch id is
the ONE hand-minted value (a GRIFT batch is re-imported only under a fresh id — bump `BATCH` with
scripts/uuid7 whenever the bundle changes). Everything else is derived from the pack.
"""

from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tap_plugin.git_serious.panels.query_pack import is_seeded, load_pack, search_entity_id  # noqa: E402

OUT = ROOT / "tap_plugin" / "git_serious" / "grift" / "queries.grift.json"

#: The batch id — the only value minted by hand. New bundle content ⇒ new id (scripts/uuid7) + version bump.
BATCH = "01a0918c-525b-7520-9151-4f01b4809e89"
VERSION = "0.1.0"

# Page and panel ids are stable across bundle versions (upsert applies); minted once with scripts/uuid7.
PAGE_PACK = "01a0918c-525b-7520-9151-4f0202dfa306"
PAGE_QUERY = "01a0918c-525b-7520-9151-4f03e6b51d79"
PANEL_PACK = "01a0918c-525b-7520-9151-4f04e1ead2c8"
PANEL_QUERY = "01a0918c-525b-7520-9151-4f0571292e95"
EDGE_PACK = "01a0918c-525b-7520-9151-4f06138f4c6d"
EDGE_QUERY = "01a0918c-525b-7520-9151-4f076f01e148"

_EDGE_NS = uuid.UUID("2c9e6f1a-8d4b-4a7e-b3f5-6e0a9d2c1b88")

WEB = {"tap.graph": "web"}


def node(entity_id: str, entity_type: str, name: str, fields: dict) -> dict:
    return {
        "entity": {"entity_id": entity_id, "entity_type": entity_type, "name": name, "dimensions": dict(WEB)},
        "node": fields,
    }


def edge(entity_id: str, name: str, src: str, dst: str, edge_type: str, properties: dict) -> dict:
    return {
        "entity": {"entity_id": entity_id, "entity_type": "edge", "name": name, "dimensions": {}},
        "edge": {"from_entity_id": src, "to_entity_id": dst, "edge_type": edge_type, "properties": properties},
    }


def build() -> dict:
    pack = load_pack()
    nodes = [
        node(
            PAGE_PACK,
            "page",
            "Query pack",
            {
                "slug": "/git-serious/queries",
                "name": "Query pack",
                "description": "The SpecterOps BloodHound GitHub saved-query corpus, translated to Gryphon: what each asks, whether it runs on this grid, and which build lands the rest.",
                "nav_weight": 113,
                "layout": {
                    "columns": {
                        "col-1": {"width": "1fr", "rows": {"row-1-pack": {"panel-id": "pack", "height": "auto"}}}
                    }
                },
            },
        ),
        node(
            PAGE_QUERY,
            "page",
            "Query",
            {
                "slug": "/git-serious/query",
                "name": "Query",
                "description": "One query from the pack: the question, the Cypher, the Gryphon, what it needs, and its answer on this grid.",
                "discoverable": False,
                "layout": {
                    "columns": {
                        "col-1": {"width": "1fr", "rows": {"row-1-query": {"panel-id": "query", "height": "auto"}}}
                    }
                },
            },
        ),
        node(
            PANEL_PACK,
            "panel",
            "The pack",
            {
                "slug": "git-serious-query-pack",
                "name": "The pack",
                "view": "git_serious/panels/query_pack.html",
                "editor_view": "",
                "description": "Every query in the pack, grouped by the stage that makes it answerable; row click opens the query page.",
                "config": {"hide_header": True},
            },
        ),
        node(
            PANEL_QUERY,
            "panel",
            "One query",
            {
                "slug": "git-serious-query-detail",
                "name": "One query",
                "view": "git_serious/panels/query_detail.html",
                "editor_view": "",
                "description": "The query page body: attribution, Cypher, Gryphon, needs, expected columns, live answer.",
                "config": {
                    "hide_header": True,
                    "workflow_page_template": "/github_core/workflow?workflow_id={workflow_id}",
                },
            },
        ),
    ]
    edges = [
        edge(
            EDGE_PACK,
            "Queries page USES_PANEL pack",
            PAGE_PACK,
            PANEL_PACK,
            "USES_PANEL",
            {"hotlink": {"model": "page", "spec": "page-panels", "value": "pack"}},
        ),
        edge(
            EDGE_QUERY,
            "Query page USES_PANEL query",
            PAGE_QUERY,
            PANEL_QUERY,
            "USES_PANEL",
            {"hotlink": {"model": "page", "spec": "page-panels", "value": "query"}},
        ),
    ]
    seeded = 0
    for q in pack["queries"]:
        if not is_seeded(q):
            continue
        seeded += 1
        sid = str(search_entity_id(q["id"]))
        src = q["sources"][0]
        nodes.append(
            node(
                sid,
                "search",
                f"bloodhound — {q['name']}",
                {
                    "name": f"bloodhound — {q['name']}",
                    "description": (
                        f"BloodHound `{q['id']}` ({q['category']}), translated to Gryphon. {q['about']} "
                        f"Upstream: {', '.join(src['repos'])} @ {', '.join(src['pins'])}, {src['paths'][0]} — Apache-2.0. "
                        f"Stage: {q['stage']}. Seeded from data/bloodhound_queries.json by scripts/build_query_pack_grift.py; edit the pack, not this node."
                    ),
                    "search_type": "gryphon",
                    "root": "node",
                    "definition": {"query": list(q["gryphon"])},
                    "input_schema": {"type": "object", "properties": {}},
                    "max_limit": 1000,
                },
            )
        )
        # The query page finds its Search by derived id; the edge makes the join visible on the grid too.
        edges.append(
            edge(
                str(uuid.uuid5(_EDGE_NS, q["id"])),
                f"Query panel USES_SEARCH {q['id']}",
                PANEL_QUERY,
                sid,
                "USES_SEARCH",
                {},
            )
        )
    return {
        "metadata": {"grift_version": "0"},
        "_reserved": {},
        "batches": [
            {
                "batch_entity": {
                    "entity_id": BATCH,
                    "entity_type": "batch",
                    "name": f"git-serious query pack v{VERSION}",
                    "dimensions": {},
                },
                "batch_node": {
                    "source": "tap_plugin.git_serious",
                    "name": f"git-serious query pack v{VERSION}",
                    "description": f"The BloodHound GitHub query pack: two pages, two panels, {seeded} seeded Searches (the translations that run on a github_core grid). GENERATED from data/bloodhound_queries.json — do not hand-edit.",
                },
                "nodes": nodes,
                "edges": edges,
            }
        ],
    }


def main(argv: list[str]) -> int:
    text = json.dumps(build(), indent=2, ensure_ascii=False) + "\n"
    if "--check" in argv:
        if OUT.exists() and OUT.read_text() == text:
            print("queries.grift.json is current")
            return 0
        print("queries.grift.json is STALE — re-run without --check (and bump BATCH if content changed)")
        return 1
    OUT.write_text(text)
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
