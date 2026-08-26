"""The in-package git_serious boot record cold-resolves (req-boot-bootstrap-git_serious-rehome-4).

This is the re-homed shipped-profiles gate: when ``boot/git_serious.boot.json`` lived in
the core repo, core's ``ProfileResolutionGuard`` / ``test_shipped_profiles_resolve``
covered it per-commit — and caught a real break (the 2026-07-02 stale module-path
collector keys after the collector-identity refactor). With the record shipping in
this plugin (``tap_plugin/git_serious/boot/``), that protection moves here: the plugin's
own suite stage-0-loads the record and cold-resolves it against the live registries,
running in plugin CI against core-main (the two-mains model). Core's gate no longer
sees this profile; this test owns the coverage — see the Validation Map rows in
``spec-dev-validation.md``.

Registry-only (no DB): the resolve preflight mutates nothing. Requires the git_serious
plugin set installed (any git_serious-provisioned instance or the plugin CI boot).
"""

from __future__ import annotations

import hashlib
import json
import tomllib
from pathlib import Path

from tap.jsonfiles import load_json_file
from tap_boot.orchestrator import check_profile
from tap_boot.profile import _SCHEMA_PATH, _parse

_PKG_ROOT = Path(__file__).resolve().parent.parent
_RECORD = _PKG_ROOT / "boot" / "git_serious.boot.json"
_TOML = _PKG_ROOT / "tap-plugin.toml"


def _canonical_digest(raw: bytes) -> str:
    """Mirror ``tap.boot_records.canonical_digest_bytes`` (bytes-first, sorted keys)."""
    data = json.loads(raw.decode("utf-8"))
    canon = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def test_record_ships_and_matches_declared_digest():
    """The record exists as package data and the toml-declared sha256 matches its content.

    The pointer flow (``tap.boot_pointer``) fail-closes on this digest at fetch time;
    this assertion keeps the declaration honest at build time, standing in for core's
    ``test_boot_records`` bijection guard, which cannot see an evicted plugin's tree.
    """
    assert _RECORD.is_file(), f"in-package boot record missing at {_RECORD}"
    declared = {
        r["name"]: r["sha256"] for r in tomllib.loads(_TOML.read_text()).get("boot", {}).get("records", [])
    }
    assert "git_serious" in declared, "tap-plugin.toml must enumerate the git_serious record under [[boot.records]]"
    actual = _canonical_digest(_RECORD.read_bytes())
    assert actual == declared["git_serious"], (
        f"declared sha256 {declared['git_serious']} != actual {actual} — "
        "regenerate the [[boot.records]] digest (scripts/boot-record-hash --refresh)"
    )


def test_record_cold_resolves_schema_coherence_and_collector_keys():
    """Schema-validate, parse, and cold-resolve the shipped record.

    ``check_profile`` resolves every fire-collector key against the registered
    collector registry — the stale-collector-key rot class stays caught here now
    that core's shipped-profiles axis no longer includes git_serious.
    """
    data = load_json_file(_RECORD, schema=_SCHEMA_PATH)
    profile = _parse("git_serious", data)
    check_profile(profile)  # raises BootError on any unresolvable step


def test_record_self_installs_git_serious_pinned():
    """The app-of-apps self-reference (req-boot-bootstrap-stage0-3): the record's
    install set includes git_serious itself, git-pinned to an immutable tag."""
    data = json.loads(_RECORD.read_text())
    entries = {p["slug"]: p for p in data["install"]["plugins"]}
    assert "git_serious" in entries, "record must self-install the git_serious plugin"
    source = entries["git_serious"]["source"]
    assert source["type"] == "git"
    assert source["rev"].startswith("v"), "self-reference must pin an immutable tag"
    assert data.get("required_secrets"), "required_secrets must ride the record (req-boot-required-secrets-6)"
