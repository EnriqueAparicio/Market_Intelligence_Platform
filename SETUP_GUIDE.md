# Market Intelligence Platform - Setup Guide

## Key Pair Authentication ✅ Configurado

### Qué se ha hecho:

1. **Claves RSA generadas:**
   - `claves/rsa_key.p8` (Privada - GUARDAR EN SECRETO)
   - `claves/rsa_key.pub` (Pública - para Snowflake)

2. **Configuración Snowflake:**
   - Usuario: `KIKESNOW5`
   - Base de datos: `MARKET_INTELLIGENCE_DB`
   - Rol: `ACCOUNTADMIN`

3. **dbt configurado:**
   - Profile: `market_intelligence_snowflake`
   - Método: Key Pair Authentication
   - ✅ Conexión verificada con `dbt debug`

### Próximos pasos:

#### 1. Completar setup en Snowflake
Ejecuta en Snowflake SQL Editor:

```sql
ALTER USER KIKESNOW5 SET RSA_PUBLIC_KEY='MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqZO7XGC37yAV4Wz2uAhk
cpk1aBnKwcnZ9+HtkRAxBwZyFFSbdWcGRrH+Yu2Uzqcv8VvZ5gBhsN7EssRusLWI
TIPgn9VV6pAiL/ZQEFKamy2Pxl+8s6qLfhptvX+RIOqNlkd2hR2k0GmqzrJpN2ET
bNDiRsicfu0K+8MCoIk5nVc26d+HYtclyuoenGptwfu9bXuHQUWCJ47L2dvVr9SA
zoZ3XYx2VcZvDJUXyKeDNZkj+xJP3PVsUjkHYQxCFgTMAVBn6fANRxf7orPb+uJM
jm8RAlMwIY4qZBYPDIQSC10GNCr+QjLZaGaefz70THJMRBzyxkT7HYivsDVeeQrW
tQIDAQAB';

-- Ejecutar bootstrap
-- (Copiar y pegar contenido de sql/snowflake/bootstrap_storage.sql)
```

#### 2. Ejecutar dbt
```powershell
cd dbt
dbt run      # Ejecutar modelos
dbt test     # Ejecutar tests
```

#### 3. Integración con Airflow
Ver: `docs/AIRFLOW_DBT_INTEGRATION.md`

#### 4. Power BI Connection
- Server: `AHRRHGX-FJ87753.snowflakecomputing.com`
- Database: `MARKET_INTELLIGENCE_DB`
- Warehouse: `COMPUTE_WH`
- Auth: Service Principal (clave pública/privada)

### Seguridad

🔒 **Nunca commitear:**
- `claves/rsa_key.p8` (agregar a .gitignore ✅)
- `.env` (agregar a .gitignore ✅)

✅ **En GitHub Actions / Airflow:**
- Usar GitHub Secrets / Airflow Variables para `claves/rsa_key.p8`
- No hardcodear valores sensibles

### Archivos importantes

- `.env` - Variables de entorno locales
- `dbt/profiles.yml` - Configuración dbt
- `generate_snowflake_keys.py` - Script para generar claves
- `sql/snowflake/bootstrap_storage.sql` - Inicialización base de datos

---
**Última actualización:** 2026-09-03  
**Estado:** ✅ Listo para desarrollo
