"""The BloodHound query pack (git-serious-tap#80, req-git-serious-query-pack / req-git-serious-query-page).

Content tests: the pack is a file the plugin ships, so what is asserted is its SHAPE and its HONESTY — every
upstream query is present and attributed, every record is in exactly one of four states with a named stage,
the generated bundle matches the pack, and every translation we claim runs at least parses. Nothing here
touches a grid except the page-state tests, which exercise the panel's three "answer" states without one.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from tap_plugin.git_serious.panels import query_pack
from tap_plugin.git_serious.panels.query_detail import GitSeriousQueryDetailPanelType
from tap_plugin.git_serious.panels.query_pack_overview import GitSeriousQueryPackPanelType

PLUGIN_ROOT = Path(query_pack.__file__).resolve().parents[3]
BUNDLE = PLUGIN_ROOT / "tap_plugin" / "git_serious" / "grift" / "queries.grift.json"

STATUSES = {"runs", "expressible", "blocked", "not_observable"}
STAGES = set(query_pack.STAGES)


class _Request:
    def __init__(self, **params: str) -> None:
        self.GET = params


# ---------------------------------------------------------------------------------------------
# The pack file
# ---------------------------------------------------------------------------------------------


@pytest.mark.spec("req-git-serious-query-pack-1")
def test_every_upstream_query_is_present_and_attributed() -> None:
    pack = query_pack.load_pack()
    ids = [q["id"] for q in pack["queries"]]
    assert len(ids) == len(set(ids)) == 79, "one record per BloodHound id; 79 at the pinned commits"
    assert pack["upstream"] == {"SpecterOps/GitHound": "bcd3da1", "SpecterOps/openhound-github": "056c0f8"}
    assert "Apache-2.0" in pack["license"]
    for q in pack["queries"]:
        assert q["sources"], q["id"]
        for s in q["sources"]:
            assert s["cypher"].strip().upper().startswith("MATCH"), (q["id"], s["cypher"][:40])
            assert s["repos"] and s["pins"] and s["paths"], q["id"]
            assert all(p.startswith(("GitHound/", "openhound-github/")) for p in s["paths"]), q["id"]
    two_variants = [q["id"] for q in pack["queries"] if len(q["sources"]) == 2]
    assert len(two_variants) == 8, two_variants


@pytest.mark.spec("req-git-serious-query-pack-2")
def test_four_states_and_named_stages() -> None:
    for q in query_pack.queries():
        assert q["status"] in STATUSES, q["id"]
        assert q["stage"] in STAGES, q["id"]
        assert q["about"].strip(), f"{q['id']} has no meaning line"
        if q["status"] in ("runs", "expressible"):
            assert q["gryphon"], f"{q['id']} claims to be expressible without Gryphon"
            assert q["returns"], f"{q['id']} names no columns"
        if q["status"] == "blocked":
            assert q["blocked_on"], f"{q['id']} is blocked on nothing named"
            assert q["hatch"], f"{q['id']} is blocked without a hatch"
        if q["status"] == "not_observable":
            assert q["stage"] == "na" and not q["gryphon"], q["id"]
        if q["stage"] in ("A", "A2", "B", "C"):
            assert query_pack.STAGES[q["stage"]]["issue"].startswith("tap-plugin-github-core#"), q["stage"]
    counts = query_pack.overview()["by_status"]
    # The pack says what it can do; a regression that silently flips a record to `runs` should be seen here.
    assert counts["not_observable"] == 14
    assert counts["runs"] >= 35


@pytest.mark.spec("req-git-serious-query-pack-3")
def test_generated_bundle_is_current_and_seeds_exactly_the_runnable() -> None:
    result = subprocess.run(
        [sys.executable, str(PLUGIN_ROOT / "scripts" / "build_query_pack_grift.py"), "--check"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    bundle = json.loads(BUNDLE.read_text())
    batch = bundle["batches"][0]
    searches = [n for n in batch["nodes"] if n["entity"]["entity_type"] == "search"]
    runnable = [q for q in query_pack.queries() if query_pack.is_seeded(q)]
    assert len(searches) == len(runnable)
    seeded_ids = {n["entity"]["entity_id"] for n in searches}
    assert seeded_ids == {str(query_pack.search_entity_id(q["id"])) for q in runnable}
    for n in searches:
        assert n["node"]["search_type"] == "gryphon" and n["node"]["definition"]["query"], n["entity"]["name"]
    pages = [n for n in batch["nodes"] if n["entity"]["entity_type"] == "page"]
    assert {p["node"]["slug"] for p in pages} == {"/git-serious/queries", "/git-serious/query"}
    uses_panel = [e for e in batch["edges"] if e["edge"]["edge_type"] == "USES_PANEL"]
    assert len(uses_panel) == 2, "one slot per page, exactly filled (Page.HOTLINKS is exact)"


@pytest.mark.spec("req-git-serious-query-pack-4")
def test_the_ladder_is_derived_and_monotone() -> None:
    o = query_pack.overview()
    values = [step["cumulative"] for step in o["ladder"]]
    assert values == sorted(values)
    assert values[0] == sum(1 for q in query_pack.queries() if q["stage"] == "today" and q["status"] == "runs")
    assert o["total"] == len(query_pack.queries()) == sum(o["by_stage"].values())
    assert o["seeded"] == sum(1 for q in query_pack.queries() if query_pack.is_seeded(q))


@pytest.mark.spec("req-git-serious-query-pack-5")
def test_every_seeded_translation_parses() -> None:
    from tap_grid.gryphon.parser import parse_gryphon

    for q in query_pack.queries():
        if not query_pack.is_seeded(q):
            continue
        parse_gryphon(list(q["gryphon"]))  # raises on a grammar rejection


def test_search_ids_are_deterministic_and_distinct() -> None:
    ids = {query_pack.search_entity_id(q["id"]) for q in query_pack.queries()}
    assert len(ids) == len(query_pack.queries())
    assert all(i.version == 5 for i in ids), "uuid5 of the BloodHound id — reproducible in the generator and the page"


# ---------------------------------------------------------------------------------------------
# The pages' states (no grid needed)
# ---------------------------------------------------------------------------------------------


@pytest.mark.spec("req-git-serious-query-page-1")
def test_bad_input_is_a_state() -> None:
    assert GitSeriousQueryDetailPanelType.get_view_context(None, _Request())["state"] == "no_selection"  # type: ignore[arg-type]
    ctx = GitSeriousQueryDetailPanelType.get_view_context(None, _Request(id="not-a-query"))  # type: ignore[arg-type]
    assert ctx["state"] == "not_found" and ctx["requested"] == "not-a-query"


@pytest.mark.spec("req-git-serious-query-page-2")
def test_an_unseeded_query_is_not_run() -> None:
    blocked = next(q for q in query_pack.queries() if q["status"] == "blocked")
    ctx = GitSeriousQueryDetailPanelType.get_view_context(None, _Request(id=blocked["id"]))  # type: ignore[arg-type]
    assert ctx["state"] == "found"
    assert ctx["answer"] == {"state": "not_seeded"}
    assert ctx["q"]["hatch"]
    unobservable = next(q for q in query_pack.queries() if q["status"] == "not_observable")
    ctx = GitSeriousQueryDetailPanelType.get_view_context(None, _Request(id=unobservable["id"]))  # type: ignore[arg-type]
    assert ctx["answer"] == {"state": "not_seeded"} and not ctx["q"]["gryphon_text"]


@pytest.mark.spec("req-git-serious-query-page-2")
@pytest.mark.django_db
def test_a_seeded_query_whose_search_is_absent_says_so() -> None:
    """Bundle not imported on this grid: the page says `absent`, never renders an empty table."""
    seeded = next(q for q in query_pack.queries() if query_pack.is_seeded(q))
    ctx = GitSeriousQueryDetailPanelType.get_view_context(None, _Request(id=seeded["id"]))  # type: ignore[arg-type]
    assert ctx["answer"]["state"] in ("absent", "ran", "failed")
    if ctx["answer"]["state"] == "ran":
        assert "rows" in ctx["answer"] and "columns" in ctx["answer"]


def test_pack_overview_context_shape() -> None:
    ctx = GitSeriousQueryPackPanelType.get_view_context(None, _Request())  # type: ignore[arg-type]
    o = ctx["o"]
    assert o["total"] == 79 and len(o["rows"]) == 79
    assert all(r["url"].startswith("/git-serious/query?id=") for r in o["rows"])
    stages_in_order = [r["stage"] for r in o["rows"]]
    order = [query_pack.STAGE_ORDER.index(s) for s in stages_in_order]
    assert order == sorted(order), "rows are grouped by stage in ladder order"


# ---------------------------------------------------------------------------------------------
# Icons by slug (design-page skill): the type's own ENTITY_ICON, decorative, nothing for an unknown slug
# ---------------------------------------------------------------------------------------------


@pytest.mark.django_db
def test_type_icon_renders_the_registered_icon_and_nothing_for_an_unknown_slug() -> None:
    from tap_plugin.git_serious.templatetags import git_serious_icons as tags

    tags._icon_url.cache_clear()
    html = str(tags.type_icon("github_core__actions_secret"))
    # Under the test harness the EntityType row exists only when github_core is registered on this grid;
    # either the icon renders as a decorative <img> or nothing renders — never a broken tag.
    assert html == "" or (html.startswith("<img ") and 'aria-hidden="true"' in html and "/icons/" in html), html
    assert tags.type_icon("no_such_plugin__no_such_type") == ""
    assert tags.type_label("github_core__github_account") == "account"
    assert tags.type_label("git_core__git_ref") == "ref"
    assert tags.type_label("github_core__actions_secret") == "secret"
    assert tags.holder_type("organisation") == "github_core__github_account"
    assert tags.holder_type("weird") == ""


def test_decorated_records_separate_typed_needs_from_prose() -> None:
    q = query_pack.decorate(query_pack.query("t0-apps-all-repos"))  # type: ignore[arg-type]
    assert q["type_needs"] == ["github_core__github_app", "github_core__app_installation"]
    assert q["primary_type"] == "github_core__github_app"
    blocked = query_pack.decorate(query_pack.query("dangerous-branch-perms"))  # type: ignore[arg-type]
    assert all("__" in n for n in blocked["type_needs"]) and blocked["other_needs"]
