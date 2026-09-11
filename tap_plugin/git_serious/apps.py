"""git-serious plugin AppConfig — composition-only; the base ready() registers the manifest."""

from tap_plugins.base import TapPluginConfig


class GitSeriousConfig(TapPluginConfig):
    def ready(self) -> None:
        super().ready()
        # The secrets pages are this plugin's first custom panel types (spec-git-serious-secrets.md).
        # Registration must run here, after every app has loaded.
        from tap_plugin.git_serious.panels.secret_detail import GitSeriousSecretDetailPanelType
        from tap_plugin.git_serious.panels.secrets_overview import GitSeriousSecretsOverviewPanelType

        from tap_web.registry import panel_type_registry

        panel_type_registry.register(GitSeriousSecretsOverviewPanelType.slug, GitSeriousSecretsOverviewPanelType)
        panel_type_registry.register(GitSeriousSecretDetailPanelType.slug, GitSeriousSecretDetailPanelType)
        # The BloodHound query pack (spec-git-serious-query-pack.md): the pack page and the page per query.
        from tap_plugin.git_serious.panels.query_detail import GitSeriousQueryDetailPanelType
        from tap_plugin.git_serious.panels.query_pack_overview import GitSeriousQueryPackPanelType

        panel_type_registry.register(GitSeriousQueryPackPanelType.slug, GitSeriousQueryPackPanelType)
        panel_type_registry.register(GitSeriousQueryDetailPanelType.slug, GitSeriousQueryDetailPanelType)
