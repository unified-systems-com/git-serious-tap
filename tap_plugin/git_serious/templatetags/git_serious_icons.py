"""Entity-type icons by SLUG, for pages that know a type's name but hold no EntityType object.

`tap_web`'s `{% entity_icon et %}` takes an EntityType row; a content page (the query pack, the secrets
cards) knows only the slug — `github_core__github_account` — and wants the type's canonical icon beside
it. Resolution stays where it lives (`tap_grid.icon.resolve_icon_url`, req-grid-icon-key); this tag only
looks the row up by slug and caches the URL per process. Icons are decorative (aria-hidden) and the text
they sit beside carries the identity (req-grid-icon-render-2). A slug with no icon renders nothing.

Candidate for tap_web's `tap_icons` (a by-slug variant is a core affordance, not a git-serious one).
"""

from __future__ import annotations

from functools import lru_cache

from django import template
from django.utils.html import format_html
from django.utils.safestring import SafeString

register = template.Library()


@lru_cache(maxsize=256)
def _icon_url(slug: str) -> str:
    from tap_grid.icon import resolve_icon_url
    from tap_grid.models import EntityType

    row = EntityType.objects.filter(slug=slug).first()
    return (resolve_icon_url(row) or "") if row is not None else ""


@register.simple_tag
def type_icon(slug: str, css_class: str = "tap-gs-icon") -> SafeString | str:
    """`<img>` for the entity type's icon, or an empty string when the type has none."""
    url = _icon_url(str(slug or ""))
    if not url:
        return ""
    return format_html('<img src="{}" class="{}" alt="" aria-hidden="true">', url, css_class)


@register.filter
def type_label(slug: str) -> str:
    """`github_core__github_account` → `account`: the type's own name for chips, prefix dropped."""
    tail = str(slug or "").rsplit("__", 1)[-1]
    for prefix in ("github_", "git_", "actions_"):
        if tail.startswith(prefix) and tail != prefix.rstrip("_"):
            tail = tail[len(prefix) :]
            break
    return tail.replace("_", " ")


_HOLDER_TYPES = {
    "organisation": "github_core__github_account",
    "organization": "github_core__github_account",
    "repository": "github_core__github_repository",
    "environment": "github_core__github_environment",
}


@register.filter
def holder_type(kind: str) -> str:
    """A secret holder's kind word → the entity type whose icon stands for it (empty when unknown)."""
    return _HOLDER_TYPES.get(str(kind or "").lower(), "")
