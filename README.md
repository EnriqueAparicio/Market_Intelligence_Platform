# Market Intelligence Platform

Portfolio-ready foundation for market intelligence and analytics automation.

## Overview

This repository combines Python, dbt, Snowflake, and GitHub-based CI to demonstrate a production-style analytics workflow.

Airflow orchestration is handled in a separate repository so the transformation and application layers remain focused here.

The main objective is to keep the codebase easy to review, easy to validate, and suitable for a company-facing portfolio.

## Repository Layout

- `src/market_intelligence_platform/`: main Python package and integration contracts.
- `tests/`: smoke tests and basic validations.
- `.github/workflows/`: GitHub Actions CI pipeline.
- `dbt/`: dbt project for transformations.
- `sql/snowflake/`: reproducible Snowflake bootstrap SQL.
- `docs/`: project and workflow documentation.

## Architecture

1. GitHub manages source control, reviews, and CI.
2. Python stores environment contracts and readiness checks.
3. Snowflake stores the warehouse, stage, and base tables.
4. dbt transforms RAW data into STAGING and MART layers.

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

## Included dbt Layer

This repository already includes a dbt project to transform data from RAW into STAGING and MART.

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

## GitHub Workflow Guide

The branch strategy, GitHub rulesets, and command workflow are documented in:

- [docs/github/BRANCH_RULESETS_GUIDE.md](docs/github/BRANCH_RULESETS_GUIDE.md)

## Documentation

Complete project documentation is available in `docs/PROJECT_DOCUMENTATION.md`.


