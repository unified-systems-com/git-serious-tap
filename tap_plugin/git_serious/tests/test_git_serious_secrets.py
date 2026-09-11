"""The secrets pages (spec-git-serious-secrets.md): every secret with its holder and consumers, the
names nothing defines, reach derived with its third state, exposure from triggers, and a name that is
a page. Seeds go through the service layer inside the test transaction; edges are created below it
(the collector's own idiom), function-scoped."""

from __future__ import annotations

import uuid
from typing import Any

from django.utils import timezone
from tap_plugin.git_serious.panels.secret_detail import GitSeriousSecretDetailPanelType
from tap_plugin.git_serious.panels.secrets import Estate
from tap_plugin.git_serious.panels.secrets_overview import GitSeriousSecretsOverviewPanelType

from tap_grid.models import Edge, Entity
from tap_grid.services import create_node

DEFINES = "DEFINES_SECRET__github_core"
REFERENCES = "REFERENCES_SECRET__github_core"


class _Req:
    def __init__(self, **params: str) -> None:
        self.GET = params


class _Panel:
    def __init__(self, **config: Any) -> None:
        self.config = config


def _node(entity_type: str, fields: dict[str, Any]) -> uuid.UUID:
    result = create_node(entity_type, fields)
    assert result.success, (entity_type, result.errors)
    return result.entity_id


def _edge(edge_type: str, src: uuid.UUID, dst: uuid.UUID) -> None:
    Edge.objects.create(
        entity=Entity.objects.create(id=uuid.uuid7(), entity_type="edge", name=edge_type, dimensions={}),
        from_entity_id=src,
        to_entity_id=dst,
        edge_type=edge_type,
        properties={},
    )


def _account() -> uuid.UUID:
    return _node(
        "github_core__github_account",
        {"login": "acme", "account_type": "Organization", "html_url": "https://github.com/acme"},
    )


def _secret(
    name: str, scope: str = "organization", visibility: str = "all", full_name: str = "", env: str = ""
) -> uuid.UUID:
    now = timezone.now().isoformat()
    return _node(
        "github_core__actions_secret",
        {
            "scope": scope,
            "owner_login": "acme",
            "full_name": full_name,
            "environment_name": env,
            "name": name,
            "visibility": visibility,
            "created_at": now,
            "updated_at": now,
            "configuration": {},
            "tags": {},
        },
    )


def _workflow(
    full_name: str, path: str, workflow_id: int, triggers: list[str], refs: dict[str, Any] | None
) -> uuid.UUID:
    tags = {"secret_refs": refs} if refs is not None else {}
    return _node(
        "github_core__github_workflow",
        {
            "name": path.rsplit("/", 1)[-1],
            "full_name": full_name,
            "workflow_id": workflow_id,
            "path": path,
            "state": "active",
            "configuration": {"triggers": triggers},
            "tags": tags,
        },
    )


def _overview() -> dict[str, Any]:
    return GitSeriousSecretsOverviewPanelType.get_view_context(_Panel(), _Req())["estate"]


def test_every_secret_renders_with_its_holder_and_consumers_and_the_idle_one_is_named(db: None) -> None:
    org = _account()
    used, idle = _secret("OPENAI_API_KEY"), _secret("XAI_API_KEY")
    _edge(DEFINES, org, used)
    _edge(DEFINES, org, idle)
    wf = _workflow(
        "acme/a",
        ".github/workflows/ci.yml",
        1,
        ["push"],
        {
            "referenced": ["OPENAI_API_KEY"],
            "unresolved": [],
            "scopes_read": ["organization", "repository", "environment"],
        },
    )
    _edge(REFERENCES, wf, used)
    est = _overview()
    by_name = {s["name"]: s for s in est["secrets"]}
    assert by_name["OPENAI_API_KEY"]["holder"] == {"kind": "organisation", "label": "acme", "detail": ""}
    assert [c["path"] for c in by_name["OPENAI_API_KEY"]["consumers"]] == [".github/workflows/ci.yml"]
    assert by_name["XAI_API_KEY"]["in_use"] is False and [s["name"] for s in est["never_referenced"]] == ["XAI_API_KEY"]
    assert est["by_scope"]["organization"] == 2 and est["workflows_read"] == 1


def test_the_names_nothing_defines_are_grouped_case_folded_with_their_read_coverage(db: None) -> None:
    _workflow(
        "acme/a",
        ".github/workflows/x.yml",
        1,
        ["push"],
        {
            "referenced": ["TAP_CORE_RO_PAT"],
            "unresolved": ["TAP_CORE_RO_PAT"],
            "scopes_read": ["organization", "repository", "environment"],
        },
    )
    _workflow(
        "acme/b",
        ".github/workflows/y.yml",
        2,
        ["pull_request_target"],
        {
            "referenced": ["tap_core_ro_pat"],
            "unresolved": ["tap_core_ro_pat"],
            "scopes_read": ["organization", "repository"],
        },
    )
    _workflow("acme/c", ".github/workflows/z.yml", 3, ["push"], None)  # never read: no tag, no row, counted unread
    est = _overview()
    assert len(est["phantoms"]) == 1
    p = est["phantoms"][0]
    assert (
        p["workflow_count"] == 2
        and p["repos"] == ["acme/a", "acme/b"]
        and p["variants"] == ["TAP_CORE_RO_PAT", "tap_core_ro_pat"]
    )
    assert p["all_scopes_read"] is True and [c["path"] for c in p["exposed"]] == [".github/workflows/y.yml"]
    assert est["workflows_total"] == 3 and est["workflows_read"] == 2 and est["workflows_unread"] == 1


def test_reach_is_derived_and_keeps_its_third_state(db: None) -> None:
    org = _account()
    _node(
        "github_core__github_repository",
        {
            "full_name": "acme/pub",
            "owner_login": "acme",
            "name": "pub",
            "github_id": 1,
            "default_branch": "main",
            "visibility": "public",
            "html_url": "https://github.com/acme/pub",
        },
    )
    _node(
        "github_core__github_repository",
        {
            "full_name": "acme/priv",
            "owner_login": "acme",
            "name": "priv",
            "github_id": 2,
            "default_branch": "main",
            "visibility": "private",
            "html_url": "https://github.com/acme/priv",
        },
    )
    est = Estate()
    everyone, private, selected = (
        _secret("A", visibility="all"),
        _secret("B", visibility="private"),
        _secret("C", visibility="selected"),
    )
    for s in (everyone, private, selected):
        _edge(DEFINES, org, s)
    est = Estate()
    facts = {s.name: est.secret_facts(s) for s in est.secrets}
    assert (
        facts["A"]["reach"]["kind"] == "all" and facts["A"]["reach"]["count"] == 2 and facts["A"]["unused_reach"] == 2
    )
    assert facts["B"]["reach"]["repos"] == ["acme/priv"] and facts["B"]["reach"]["count"] == 1
    assert facts["C"]["reach"]["observable"] is False and facts["C"]["unused_reach"] is None


def test_a_consumer_carries_its_triggers_and_marks_exposure(db: None) -> None:
    org = _account()
    s = _secret("DEPLOY_KEY")
    _edge(DEFINES, org, s)
    wf = _workflow(
        "acme/a",
        ".github/workflows/deploy.yml",
        9,
        ["pull_request_target", "workflow_dispatch"],
        {"referenced": ["DEPLOY_KEY"], "unresolved": [], "scopes_read": ["organization", "repository"]},
    )
    _edge(REFERENCES, wf, s)
    ctx = GitSeriousSecretDetailPanelType.get_view_context(_Panel(), _Req(secret_id=str(s)))
    assert ctx["state"] == "found" and ctx["mode"] == "secret"
    c = ctx["s"]["consumers"][0]
    assert (
        c["exposed"] == ["pull_request_target"]
        and c["runs"] == 0
        and c["triggers"] == ["pull_request_target", "workflow_dispatch"]
    )
    assert [x["path"] for x in ctx["s"]["exposed"]] == [".github/workflows/deploy.yml"]


def test_a_name_is_a_page_too_and_a_defined_name_redirects_to_its_secret(db: None) -> None:
    org = _account()
    s = _secret("REAL")
    _edge(DEFINES, org, s)
    _workflow(
        "acme/a",
        ".github/workflows/x.yml",
        1,
        ["push"],
        {"referenced": ["GHOST"], "unresolved": ["GHOST"], "scopes_read": ["organization", "repository"]},
    )
    ghost = GitSeriousSecretDetailPanelType.get_view_context(_Panel(), _Req(name="ghost"))
    assert ghost["state"] == "found" and ghost["mode"] == "phantom" and ghost["p"]["workflow_count"] == 1
    real = GitSeriousSecretDetailPanelType.get_view_context(_Panel(), _Req(name="real"))
    assert real["state"] == "found" and real["mode"] == "secret" and real["s"]["name"] == "REAL"
    assert GitSeriousSecretDetailPanelType.get_view_context(_Panel(), _Req(name="NOPE"))["state"] == "not_found"


def test_bad_input_is_a_state_not_a_500(db: None) -> None:
    assert GitSeriousSecretDetailPanelType.get_view_context(_Panel(), _Req())["state"] == "no_selection"
    assert (
        GitSeriousSecretDetailPanelType.get_view_context(_Panel(), _Req(secret_id="not-a-uuid"))["state"] == "not_found"
    )
    assert (
        GitSeriousSecretDetailPanelType.get_view_context(_Panel(), _Req(secret_id=str(uuid.uuid7())))["state"]
        == "not_found"
    )
