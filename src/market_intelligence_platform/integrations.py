"""Integration configuration for GitHub and Snowflake."""

import os
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class GitHubRepositoryConfig:
    """GitHub repository coordinates used by the project."""

    owner: str
    repository: str
    branch: str

    @classmethod
    def from_env(cls) -> "GitHubRepositoryConfig":
        return cls(
            owner=os.getenv("GITHUB_OWNER", ""),
            repository=os.getenv("GITHUB_REPOSITORY", ""),
            branch=os.getenv("GITHUB_BRANCH", "main"),
        )

    @property
    def full_name(self) -> str:
        return f"{self.owner}/{self.repository}"

    def is_configured(self) -> bool:
        return bool(self.owner and self.repository)


@dataclass(frozen=True, slots=True)
class SnowflakeConfig:
    """Snowflake connection settings used by the project."""

    account: str
    user: str
    password: str = field(repr=False)
    role: str
    warehouse: str
    database: str
    schema: str
    authenticator: str = "externalbrowser"

    @classmethod
    def from_env(cls) -> "SnowflakeConfig":
        return cls(
            account=os.getenv("SNOWFLAKE_ACCOUNT", ""),
            user=os.getenv("SNOWFLAKE_USER", ""),
            password=os.getenv("SNOWFLAKE_PASSWORD", ""),
            role=os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
            database=os.getenv("SNOWFLAKE_DATABASE", "SNOWFLAKE_SAMPLE_DATA"),
            schema=os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC"),
            authenticator=os.getenv("SNOWFLAKE_AUTHENTICATOR", "externalbrowser"),
        )

    def is_configured(self) -> bool:
        required_values = [
            self.account,
            self.user,
            self.role,
            self.warehouse,
            self.database,
            self.schema,
            self.authenticator,
        ]
        credentials_configured = self.authenticator == "externalbrowser" or bool(self.password)
        return all(required_values) and credentials_configured


@dataclass(frozen=True, slots=True)
class ProjectIntegrations:
    """Current integration state for the project."""

    github: GitHubRepositoryConfig
    snowflake: SnowflakeConfig

    @classmethod
    def from_env(cls) -> "ProjectIntegrations":
        return cls(
            github=GitHubRepositoryConfig.from_env(),
            snowflake=SnowflakeConfig.from_env(),
        )

    def readiness(self) -> dict[str, bool]:
        return {
            "github": self.github.is_configured(),
            "snowflake": self.snowflake.is_configured(),
        }
