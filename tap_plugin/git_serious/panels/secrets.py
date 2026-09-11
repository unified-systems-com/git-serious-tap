"""What the grid knows about the estate's Actions secrets — derived once, read by both secrets panels.

Spec: specs/spec-git-serious-secrets.md (req-git-serious-secrets, req-git-serious-secret-page).

github_core lands the facts: `actions_secret` nodes (a NAME at a scope — never a value; GitHub's API
has none), `DEFINES_SECRET` from the holder (organisation, repository or environment), and
`REFERENCES_SECRET` from every workflow whose file names the secret inside an expression, one edge per
defining scope. What a workflow names that no readable scope defines lives on the workflow itself,
`tags.secret_refs.unresolved`, beside `scopes_read` — so "cannot find" is only ever a claim about the
scopes that were actually listed. This module joins those with what the grid already holds about the
consumers: the workflow's triggers (exposure), its runs in the collected window, its repository's
visibility and criticality, and — when zizmor is installed — the findings on the file.

Three states throughout. A secret nobody references is *never referenced*, not fine. A name defined
nowhere we could see is *cannot find*, not broken — on this estate every such name is deliberate. A
workflow with no collected body is *not read*, and its secrets are unknown, not none.
"""

from __future__ import annotations

import logging
from collections import Counter, defaultdict
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from tap_plugin.github_core.models.actions_secret import ActionsSecret
from tap_plugin.github_core.models.github_actions_run import GithubActionsRun
from tap_plugin.github_core.models.github_environment import GithubEnvironment
from tap_plugin.github_core.models.github_repository import GithubRepository
from tap_plugin.github_core.models.github_workflow import GithubWorkflow

from tap_grid.models import Edge, Entity

if TYPE_CHECKING:
    from uuid import UUID

    from tap_web.models import Panel

logger = logging.getLogger(__name__)

EDGE_DEFINES = "DEFINES_SECRET__github_core"
EDGE_REFERENCES = "REFERENCES_SECRET__github_core"
EDGE_FLAGS_WORKFLOW = "FLAGS_WORKFLOW__zizmor"

#: Triggers under which a workflow runs with a secret in hand on someone else's input. A
#: `pull_request_target` workflow reads the base branch's file but runs for a fork's PR with the
#: repository's secrets — the shape every CI/CD security incident of the last five years has taken.
EXPOSED_TRIGGERS = frozenset(
    {
        "pull_request_target",
        "workflow_run",
        "issue_comment",
        "discussion_comment",
        "pull_request_review",
        "pull_request_review_comment",
    }
)

#: zizmor audits that are about how a workflow handles the secrets it holds.
SECRET_AUDITS = frozenset({"secrets-outside-env", "template-injection", "dangerous-triggers", "artipacked"})

SCOPE_LABEL = {
    "organization": "organisation secret",
    "repository": "repository secret",
    "environment": "environment secret",
}


def page_url(template: str, **fields: Any) -> str:
    """Fill a consumer-declared page template; "" on a missing value or when no such Page exists."""
    from tap_web.models import Page

    template = (template or "").strip()
    if not template:
        return ""
    url = template
    for key, value in fields.items():
        token = "{" + key + "}"
        if token not in url:
            continue
        if value in (None, ""):
            return ""
        url = url.replace(token, quote(str(value), safe="/"))
    slug = url.split("?", 1)[0]
    return url if Page.objects.filter(slug=slug).exists() else ""


def _age_days(when: datetime | None) -> int | None:
    if when is None:
        return None
    return max(0, (datetime.now(UTC) - when).days)


class Estate:
    """One read of everything secret-shaped on the grid, joined. Build once per request."""

    def __init__(self, panel: Panel | None = None) -> None:
        cfg = (getattr(panel, "config", None) or {}) if panel else {}
        self.workflow_page_template = str(cfg.get("workflow_page_template") or "")
        self.findings_page_template = str(cfg.get("findings_page_template") or "")
        self.secret_page_template = str(cfg.get("secret_page_template") or "/git-serious/secret?secret_id={secret_id}")
        self.name_page_template = str(cfg.get("name_page_template") or "/git-serious/secret?name={name}")

        self.secrets: list[ActionsSecret] = list(
            ActionsSecret.objects.all().order_by("scope", "owner_login", "full_name", "name")
        )
        self.workflows: dict[UUID, GithubWorkflow] = {w.entity_id: w for w in GithubWorkflow.objects.all()}
        self.repos: dict[str, GithubRepository] = {r.full_name: r for r in GithubRepository.objects.all()}
        self.environments: dict[tuple[str, str], GithubEnvironment] = {
            (e.full_name, e.name): e for e in GithubEnvironment.objects.all()
        }
        self._holder_type: dict[UUID, str] = {}
        self._consumers_of: dict[UUID, list[UUID]] = defaultdict(list)
        for edge in Edge.objects.filter(edge_type=EDGE_REFERENCES).only("from_entity_id", "to_entity_id"):
            self._consumers_of[edge.to_entity_id].append(edge.from_entity_id)
        holder_edges = list(Edge.objects.filter(edge_type=EDGE_DEFINES).only("from_entity_id", "to_entity_id"))
        types = dict(
            Entity.objects.filter(id__in=[e.from_entity_id for e in holder_edges]).values_list("id", "entity_type")
        )
        for edge in holder_edges:
            self._holder_type[edge.to_entity_id] = types.get(edge.from_entity_id, "")

        self._runs: dict[int, list[dict[str, Any]]] = defaultdict(list)
        for row in GithubActionsRun.objects.values("configuration", "conclusion", "run_started_at"):
            wid = (row.get("configuration") or {}).get("workflow_id")
            if wid:
                self._runs[int(wid)].append(row)

        # zizmor is optional: git-serious depends on github_core, not on any scanner. When it is
        # present its findings on a consuming workflow are the sharpest fact this page can add.
        self._findings: dict[UUID, Counter[str]] = defaultdict(Counter)
        self.scanner_present = False
        try:
            from tap_plugin.zizmor.models.finding import ZizmorFinding  # noqa: PLC0415

            self.scanner_present = True
            audits = dict(ZizmorFinding.objects.values_list("entity_id", "audit_id"))
            for edge in Edge.objects.filter(edge_type=EDGE_FLAGS_WORKFLOW).only("from_entity_id", "to_entity_id"):
                self._findings[edge.to_entity_id][audits.get(edge.from_entity_id, "")] += 1
        except ImportError:
            logger.debug("[cf28] git-serious secrets: zizmor not installed; findings join is not observable")

    # ------------------------------------------------------------------ per-workflow facts

    def consumer(self, wf: GithubWorkflow) -> dict[str, Any]:
        cfg = wf.configuration or {}
        triggers = [str(t) for t in (cfg.get("triggers") or [])]
        runs = self._runs.get(int(wf.workflow_id or 0), [])
        latest = max(runs, key=lambda r: r.get("run_started_at") or datetime.min.replace(tzinfo=UTC), default=None)
        repo = self.repos.get(wf.full_name)
        findings = self._findings.get(wf.entity_id, Counter())
        refs = (wf.tags or {}).get("secret_refs") or {}
        return {
            "entity_id": str(wf.entity_id),
            "full_name": wf.full_name,
            "path": wf.path,
            "name": wf.name,
            "workflow_id": wf.workflow_id,
            "url": page_url(
                self.workflow_page_template, workflow_id=wf.workflow_id, full_name=wf.full_name, path=wf.path
            ),
            "findings_url": page_url(self.findings_page_template, workflow_id=wf.workflow_id) if findings else "",
            "triggers": triggers,
            "exposed": sorted(set(triggers) & EXPOSED_TRIGGERS),
            "runs": len(runs),
            "last_conclusion": (latest or {}).get("conclusion") or "",
            "visibility": getattr(repo, "visibility", "") or "",
            "criticality": ((getattr(repo, "custom_properties", None) or {}).get("criticality") or "") if repo else "",
            "findings": sum(findings.values()),
            "secret_findings": sum(n for audit, n in findings.items() if audit in SECRET_AUDITS),
            "named": list(refs.get("referenced") or []),
            "missing": list(refs.get("unresolved") or []),
            "scopes_read": list(refs.get("scopes_read") or []),
        }

    # ------------------------------------------------------------------ per-secret facts

    def holder(self, secret: ActionsSecret) -> dict[str, str]:
        if secret.scope == "organization":
            return {"kind": "organisation", "label": secret.owner_login, "detail": ""}
        if secret.scope == "environment":
            return {"kind": "environment", "label": secret.environment_name, "detail": secret.full_name}
        return {"kind": "repository", "label": secret.full_name, "detail": ""}

    def reach(self, secret: ActionsSecret) -> dict[str, Any]:
        """Where the secret can be received — derived from visibility; the third state is explicit."""
        if secret.scope == "repository":
            return {
                "kind": "repository",
                "text": f"the workflows of {secret.full_name}",
                "count": 1,
                "observable": True,
            }
        if secret.scope == "environment":
            env = self.environments.get((secret.full_name, secret.environment_name))
            rules = len(getattr(env, "protection_rules", None) or []) if env else None
            return {
                "kind": "environment",
                "text": f"jobs in {secret.full_name} that deploy to the {secret.environment_name} environment",
                "count": 1,
                "observable": True,
                "protection_rules": rules,
            }
        vis = (secret.visibility or "").lower()
        org_repos = [r for r in self.repos.values() if r.owner_login == secret.owner_login] or list(self.repos.values())
        if vis == "all":
            return {
                "kind": "all",
                "text": f"every repository in {secret.owner_login} — {len(org_repos)} on the grid",
                "count": len(org_repos),
                "observable": True,
            }
        if vis == "private":
            reached = [r.full_name for r in org_repos if (r.visibility or "").lower() in ("private", "internal")]
            return {
                "kind": "private",
                "text": f"private and internal repositories only — {len(reached)} of {len(org_repos)} on the grid"
                + (" (none: an all-public estate)" if not reached else ""),
                "count": len(reached),
                "repos": reached,
                "observable": True,
            }
        if vis == "selected":
            recorded = ((secret.tags or {}).get("reach") or {}).get("repos")
            if recorded is None:
                return {
                    "kind": "selected",
                    "text": "a selected list of repositories — which ones is NOT on the grid yet (github-core#108); the collector reads the list to resolve references but does not record it",
                    "count": None,
                    "observable": False,
                }
            return {
                "kind": "selected",
                "text": f"{len(recorded)} selected repositor{'y' if len(recorded) == 1 else 'ies'}",
                "count": len(recorded),
                "repos": list(recorded),
                "observable": True,
            }
        return {
            "kind": "unknown",
            "text": "not observable — GitHub returned no visibility",
            "count": None,
            "observable": False,
        }

    def secret_facts(self, secret: ActionsSecret) -> dict[str, Any]:
        consumers = [
            self.consumer(self.workflows[wid])
            for wid in self._consumers_of.get(secret.entity_id, [])
            if wid in self.workflows
        ]
        consumers.sort(key=lambda c: (c["full_name"], c["path"]))
        repos = sorted({c["full_name"] for c in consumers})
        same_name = [
            s for s in self.secrets if s.name.upper() == secret.name.upper() and s.entity_id != secret.entity_id
        ]
        reach = self.reach(secret)
        exposed = [c for c in consumers if c["exposed"]]
        # "workflow_run ×5", not the same word five times — the trigger histogram across exposed consumers.
        exposed_triggers = Counter(t for c in exposed for t in c["exposed"])
        return {
            "exposed_triggers": [f"{t} ×{n}" if n > 1 else t for t, n in exposed_triggers.most_common()],
            "secret": secret,
            "entity_id": str(secret.entity_id),
            "name": secret.name,
            "scope": secret.scope,
            "kind_label": SCOPE_LABEL.get(secret.scope, "secret"),
            "holder": self.holder(secret),
            "visibility": secret.visibility or "",
            "created_at": secret.created_at,
            "updated_at": secret.updated_at,
            "age_days": _age_days(secret.created_at),
            "since_update_days": _age_days(secret.updated_at),
            "url": page_url(self.secret_page_template, secret_id=secret.entity_id),
            "consumers": consumers,
            "repos": repos,
            "exposed": exposed,
            "in_use": bool(consumers),
            "reach": reach,
            # reach vs use: an `all` secret used by 2 of 24 repositories reaches 22 that never name it
            "unused_reach": (
                (reach["count"] - len(repos))
                if reach.get("count") and reach["kind"] in ("all", "private", "selected")
                else None
            ),
            "same_name": [
                {
                    "scope": s.scope,
                    "holder": self.holder(s),
                    "url": page_url(self.secret_page_template, secret_id=s.entity_id),
                }
                for s in same_name
            ],
            "secret_findings": sum(c["secret_findings"] for c in consumers),
        }

    # ------------------------------------------------------------------ names no scope defines

    def phantoms(self) -> list[dict[str, Any]]:
        by_name: dict[str, dict[str, Any]] = {}
        for wf in self.workflows.values():
            refs = (wf.tags or {}).get("secret_refs") or {}
            for name in refs.get("unresolved") or []:
                entry = by_name.setdefault(
                    name.upper(), {"name": name, "variants": set(), "workflows": [], "scopes": Counter()}
                )
                entry["variants"].add(name)
                entry["workflows"].append(self.consumer(wf))
                entry["scopes"][tuple(refs.get("scopes_read") or [])] += 1
        out = []
        for key, entry in by_name.items():
            wfs = sorted(entry["workflows"], key=lambda c: (c["full_name"], c["path"]))
            full = sum(1 for c in wfs if set(c["scopes_read"]) >= {"organization", "repository"})
            out.append(
                {
                    "key": key,
                    "name": entry["name"],
                    "variants": sorted(entry["variants"]),
                    "workflows": wfs,
                    "workflow_count": len(wfs),
                    "repos": sorted({c["full_name"] for c in wfs}),
                    "exposed": [c for c in wfs if c["exposed"]],
                    "all_scopes_read": full == len(wfs),
                    "url": page_url(self.name_page_template, name=entry["name"]),
                }
            )
        out.sort(key=lambda p: (-p["workflow_count"], p["name"].lower()))
        return out

    # ------------------------------------------------------------------ the estate at a glance

    def overview(self) -> dict[str, Any]:
        facts = [self.secret_facts(s) for s in self.secrets]
        tagged = [w for w in self.workflows.values() if (w.tags or {}).get("secret_refs") is not None]
        naming = [w for w in tagged if (w.tags["secret_refs"].get("referenced") or [])]
        phantoms = self.phantoms()
        return {
            "secrets": facts,
            "by_scope": Counter(f["scope"] for f in facts),
            "in_use": [f for f in facts if f["in_use"]],
            "never_referenced": [f for f in facts if not f["in_use"]],
            "exposed": [f for f in facts if f["exposed"]],
            "phantoms": phantoms,
            "phantom_workflows": len({c["entity_id"] for p in phantoms for c in p["workflows"]}),
            "workflows_total": len(self.workflows),
            "workflows_read": len(tagged),
            "workflows_unread": len(self.workflows) - len(tagged),
            "workflows_naming": len(naming),
            "repos_total": len(self.repos),
            "repos_naming": len({w.full_name for w in naming}),
            "scanner_present": self.scanner_present,
        }
