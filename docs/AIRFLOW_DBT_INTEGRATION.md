# Airflow + dbt + Snowflake Integration

## Arquitectura

```
GitHub Repo
    ↓
    └─→ Airflow (Scheduler)
         ├─ Extract: GitHub API → Snowflake RAW
         ├─ Transform: dbt (staging → marts)
         └─ Load: Snowflake → Power BI

Cron/Schedule: Diario @ 2 AM
```

## Setup en Airflow

### 1. Airflow Connection para Snowflake

```python
# En Airflow UI: Admin → Connections → Create

{
    "conn_type": "snowflake",
    "login": "KIKESNOW5",
    "password": "",  # Dejar vacío, usar private_key_path
    "host": "AHRRHGX-FJ87753.snowflakecomputing.com",
    "port": 443,
    "database": "MARKET_INTELLIGENCE_DB",
    "schema": "RAW",
    "extra": {
        "warehouse": "COMPUTE_WH",
        "role": "ACCOUNTADMIN",
        "private_key_path": "/opt/airflow/keys/rsa_key.p8"
    }
}
```

### 2. Airflow Variable para ruta de dbt

En Airflow UI: Admin → Variables

```json
{
    "key": "dbt_project_path",
    "value": "/opt/airflow/repos/market_intelligence_platform/dbt"
}
```

### 3. DAG básico

```python
# airflow/dags/market_intelligence_pipeline.py

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'market_intelligence_pipeline',
    default_args=default_args,
    description='GitHub data extraction → dbt transformation → Snowflake',
    schedule_interval='0 2 * * *',  # 2 AM daily
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    # Step 1: Ejecutar dbt
    run_dbt = BashOperator(
        task_id='run_dbt',
        bash_command='''
            cd {{ var.value.dbt_project_path }} && \
            dbt run --profiles-dir . --target prod && \
            dbt test --profiles-dir . --target prod
        '''
    )

    # Step 2: Validar datos en Snowflake
    validate_data = SnowflakeOperator(
        task_id='validate_data',
        snowflake_conn_id='snowflake_prod',
        sql='''
            SELECT COUNT(*) as record_count 
            FROM MARKET_INTELLIGENCE_DB.MART.REPOSITORY_KPI 
            WHERE METRIC_DATE = CURRENT_DATE()
        '''
    )

    run_dbt >> validate_data
```

### 4. Secrets en Airflow

Para almacenar `rsa_key.p8` de forma segura:

```bash
# Opción 1: Variables (menos seguro)
airflow variables set snowflake_private_key "$(cat rsa_key.p8)"

# Opción 2: Secrets Backend (recomendado)
# Configurar en airflow.cfg:
# [secrets]
# backend = airflow.providers.google.cloud.secrets_manager.CloudSecretsManagerBackend
```

### 5. GitHub Actions → Airflow

Para deployar cambios en dbt automáticamente:

```yaml
# .github/workflows/deploy-dbt.yml

name: Deploy dbt to Airflow

on:
  push:
    branches: [main]
    paths: ['dbt/**']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Sync dbt to Airflow
        run: |
          ssh -i ${{ secrets.AIRFLOW_PRIVATE_KEY }} \
              user@airflow-server \
              "cd /opt/airflow/repos && git pull origin main"
```

## Monitoreo

### Logs en Airflow
- Task logs: Airflow UI → DAG → Task Instance
- dbt logs: `/opt/airflow/logs/dbt/` (configurar en `profiles.yml`)

### Alertas
```python
# Agregar al DAG
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

send_alert = SlackWebhookOperator(
    task_id='send_alert',
    http_conn_id='slack',
    message='Pipeline failed! Check Airflow logs.',
    trigger_rule='one_failed'
)
```

## CI/CD

### GitHub Secrets necesarios
```
SNOWFLAKE_ACCOUNT
SNOWFLAKE_USER
SNOWFLAKE_PRIVATE_KEY_PATH (contenido completo del archivo)
SNOWFLAKE_DATABASE
SNOWFLAKE_WAREHOUSE
SNOWFLAKE_ROLE
```

### Testing en CI
```bash
# .github/workflows/test-dbt.yml
dbt parse
dbt run-operation validate_environment
dbt test
```

---

**Ver:** SETUP_GUIDE.md para configuración inicial
