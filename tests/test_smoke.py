from market_intelligence_platform import __version__
from market_intelligence_platform.config import Settings
from market_intelligence_platform.integrations import (
    GitHubRepositoryConfig,
    ProjectIntegrations,
    SnowflakeConfig,
)


def test_package_version_is_defined() -> None:
    assert __version__ == "0.1.0"


def test_settings_can_load_defaults() -> None:
    settings = Settings.from_env()

    assert settings.project_name == "market_intelligence_platform"
    assert settings.app_env == "local"
    assert settings.log_level == "INFO"


def test_integrations_are_unconfigured_by_default() -> None:
    integrations = ProjectIntegrations.from_env()

    assert integrations.readiness() == {"github": False, "snowflake": False}


def test_github_repository_full_name() -> None:
    github = GitHubRepositoryConfig(owner="acme", repository="market-intelligence", branch="main")

    assert github.full_name == "acme/market-intelligence"
    assert github.is_configured() is True


def test_snowflake_is_configured_when_all_values_exist() -> None:
    snowflake = SnowflakeConfig(
        account="account",
        user="user",
        password="password",
        role="role",
        warehouse="warehouse",
        database="database",
        schema="schema",
    )

    assert snowflake.is_configured() is True