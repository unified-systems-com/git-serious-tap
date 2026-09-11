"""git-serious-secret-detail — one Actions secret in full, or one NAME no scope defines.
Spec: specs/spec-git-serious-secrets.md (req-git-serious-secret-page)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from django.core.exceptions import ValidationError
from tap_plugin.git_serious.panels.secrets import Estate
from tap_plugin.github_core.models.actions_secret import ActionsSecret

if TYPE_CHECKING:
    from django.http import HttpRequest

    from tap_web.models import Panel


class GitSeriousSecretDetailPanelType:
    slug: ClassVar[str] = "git-serious-secret-detail"
    label: ClassVar[str] = "git-serious Secret"
    view: ClassVar[str] = "git_serious/panels/secret_detail.html"
    css: ClassVar[list[str]] = ["git_serious/css/secrets.css"]
    js: ClassVar[list[str]] = []
    editor_view: ClassVar[str] = ""
    config_defaults: ClassVar[dict[str, Any]] = {}

    @classmethod
    def get_view_context(cls, panel: Panel, request: HttpRequest) -> dict[str, Any]:
        secret_id = (request.GET.get("secret_id") or "").strip() if request else ""
        name = (request.GET.get("name") or "").strip() if request else ""
        if not secret_id and not name:
            return {"state": "no_selection"}
        estate = Estate(panel)
        if secret_id:
            try:
                secret = ActionsSecret.objects.filter(entity_id=secret_id).first()
            except ValueError, TypeError, ValidationError:
                secret = None  # a mistyped id from a URL is a not-found page, not a 500
            if secret is None:
                return {"state": "not_found", "requested": secret_id}
            return {"state": "found", "mode": "secret", "s": estate.secret_facts(secret), "estate": estate}
        phantom = next((p for p in estate.phantoms() if p["key"] == name.upper()), None)
        if phantom is None:
            # The name may be a real secret reached by name rather than id: send the reader there.
            match = next((s for s in estate.secrets if s.name.upper() == name.upper()), None)
            if match is not None:
                return {"state": "found", "mode": "secret", "s": estate.secret_facts(match), "estate": estate}
            return {"state": "not_found", "requested": name}
        return {"state": "found", "mode": "phantom", "p": phantom, "estate": estate}
