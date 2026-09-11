"""git-serious-query-pack — the BloodHound corpus as a pack: every query, by the stage that answers it.
Spec: specs/spec-git-serious-query-pack.md (req-git-serious-query-pack)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from tap_plugin.git_serious.panels import query_pack

if TYPE_CHECKING:
    from django.http import HttpRequest

    from tap_web.models import Panel


class GitSeriousQueryPackPanelType:
    slug: ClassVar[str] = "git-serious-query-pack"
    label: ClassVar[str] = "git-serious Query Pack"
    view: ClassVar[str] = "git_serious/panels/query_pack.html"
    css: ClassVar[list[str]] = ["git_serious/css/secrets.css", "git_serious/css/queries.css"]
    js: ClassVar[list[str]] = ["git_serious/js/queries.js"]
    editor_view: ClassVar[str] = ""
    config_defaults: ClassVar[dict[str, Any]] = {}

    @classmethod
    def get_view_context(cls, panel: Panel, request: HttpRequest) -> dict[str, Any]:
        return {"o": query_pack.overview()}
