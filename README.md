# Market Intelligence Platform

Production-style foundation for market intelligence and analytics automation.

## Repository Scope

This repository contains core application logic, shared utilities, environment configuration, and validation checks.

Airflow orchestration is managed in a separate repository.

The primary integration handled in this repository is the connection between application code, GitHub-based delivery, and Snowflake as the analytics warehouse.

## Initial Structure

- `src/market_intelligence_platform/`: main Python package.
- `tests/`: smoke tests and basic validations.
- `.github/workflows/`: CI workflows.
- `dbt/`: transformation layer and data model definitions.
- `sql/snowflake/`: repeatable storage bootstrap SQL.

## Local Setup

```bash
pip install -r requirements.txt
pytest
```

## Environment Variables

Base variables are defined in `.env.example`.

- GitHub: `GITHUB_OWNER`, `GITHUB_REPOSITORY`, `GITHUB_BRANCH`
- Snowflake: `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, `SNOWFLAKE_ROLE`, `SNOWFLAKE_WAREHOUSE`, `SNOWFLAKE_DATABASE`, `SNOWFLAKE_SCHEMA`

## Project Snowflake Storage

Provisioned structure:

- Database: `MARKET_INTELLIGENCE_DB`
- Schemas: `CORE`, `RAW`, `STAGING`, `MART`
- Initial ingestion stage: `MARKET_INTELLIGENCE_DB.RAW.GITHUB_STAGE`
- Base tables:
	- `CORE.PROJECT_RUN_AUDIT`
	- `RAW.GITHUB_REPOSITORY_SNAPSHOT`
	- `STAGING.REPOSITORY_DAILY_METRICS`
	- `MART.REPOSITORY_KPI`

Reproducible SQL is available in `sql/snowflake/bootstrap_storage.sql`.

## Git Branching Strategy

- `main`: stable branch for production-ready code.
- `dev`: integration branch for active development.

Recommended flow: open pull requests from `dev` into `main` after tests and reviews pass.

## Included dbt Layer

The repository already includes a dbt project to transform data from RAW to STAGING and MART.

- dbt project: `dbt/dbt_project.yml`
- Source RAW: `dbt/models/sources/sources.yml`
- STAGING model: `dbt/models/staging/stg_github_repository_snapshot.sql`
- MART model: `dbt/models/marts/mart_repository_kpi.sql`

Base commands:

```bash
pip install -r requirements.txt
dbt debug --project-dir dbt --profiles-dir dbt
dbt run --project-dir dbt --profiles-dir dbt
dbt test --project-dir dbt --profiles-dir dbt
```

## Documentation

Complete project documentation is available in `docs/PROJECT_DOCUMENTATION.md`.


