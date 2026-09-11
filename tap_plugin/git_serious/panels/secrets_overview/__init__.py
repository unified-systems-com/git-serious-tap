"""git-serious-secrets-overview — the estate's Actions secrets: held where, used by whom, and the names
nothing defines. Spec: specs/spec-git-serious-secrets.md (req-git-serious-secrets)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from tap_plugin.git_serious.panels.secrets import Estate

if TYPE_CHECKING:
    from django.http import HttpRequest

    from tap_web.models import Panel


class GitSeriousSecretsOverviewPanelType:
    slug: ClassVar[str] = "git-serious-secrets-overview"
    label: ClassVar[str] = "git-serious Secrets"
    view: ClassVar[str] = "git_serious/panels/secrets_overview.html"
    css: ClassVar[list[str]] = ["git_serious/css/secrets.css"]
    js: ClassVar[list[str]] = []
    editor_view: ClassVar[str] = ""
    config_defaults: ClassVar[dict[str, Any]] = {}

    @classmethod
    def get_view_context(cls, panel: Panel, request: HttpRequest) -> dict[str, Any]:
        estate = Estate(panel)
        return {"estate": estate.overview(), "state": "found" if estate.secrets or estate.workflows else "empty"}
