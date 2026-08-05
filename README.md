# Market Intelligence Platform

Base del proyecto para inteligencia de mercado y automatización de analítica.

## Alcance del repositorio

Este repositorio concentra la lógica principal del proyecto, utilidades compartidas, configuración y validaciones.

El orquestado de Airflow se mantiene en un repositorio aparte.

La integración principal que vive aquí es la relación entre el código del repositorio, GitHub como control de versiones y Snowflake como destino de datos y analítica.

## Estructura inicial

- `src/market_intelligence_platform/`: paquete principal de Python.
- `tests/`: tests de humo y validaciones básicas.
- `.github/workflows/`: pipeline de CI.
- `src/market_intelligence_platform/`: configuración y contratos de integración.

## Arranque local

```bash
pip install -r requirements.txt
pytest
```

## Variables de entorno

Las variables base están en `.env.example`.

- GitHub: `GITHUB_OWNER`, `GITHUB_REPOSITORY`, `GITHUB_BRANCH`
- Snowflake: `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, `SNOWFLAKE_ROLE`, `SNOWFLAKE_WAREHOUSE`, `SNOWFLAKE_DATABASE`, `SNOWFLAKE_SCHEMA`

## Snowflake storage del proyecto

Estructura provisionada:

- Base de datos: `MARKET_INTELLIGENCE_DB`
- Schemas: `CORE`, `RAW`, `STAGING`, `MART`
- Stage de ingesta inicial: `MARKET_INTELLIGENCE_DB.RAW.GITHUB_STAGE`
- Tablas base:
	- `CORE.PROJECT_RUN_AUDIT`
	- `RAW.GITHUB_REPOSITORY_SNAPSHOT`
	- `STAGING.REPOSITORY_DAILY_METRICS`
	- `MART.REPOSITORY_KPI`

SQL reproducible en `sql/snowflake/bootstrap_storage.sql`.

## Capa dbt incluida

El repositorio ya incluye el proyecto dbt para transformar datos desde RAW a STAGING y MART.

- Proyecto dbt: `dbt/dbt_project.yml`
- Source RAW: `dbt/models/sources/sources.yml`
- Modelo STAGING: `dbt/models/staging/stg_github_repository_snapshot.sql`
- Modelo MART: `dbt/models/marts/mart_repository_kpi.sql`

Comandos base:

```bash
pip install -r requirements.txt
dbt debug --project-dir dbt --profiles-dir dbt
dbt run --project-dir dbt --profiles-dir dbt
dbt test --project-dir dbt --profiles-dir dbt
```

## Documentacion

Documentacion completa del proyecto en `docs/PROJECT_DOCUMENTATION.md`.


