# Market Intelligence Platform - Explicación Completa

## 🎯 ¿Qué es este proyecto?

**Objetivo:** Extraer datos de repositorios GitHub, transformarlos con dbt, almacenarlos en Snowflake y visualizarlos en Power BI.

### Flujo de datos:
```
GitHub API → Snowflake RAW → dbt (STAGING/MART) → Snowflake → Power BI
```

---

## 🔧 Configuración realizada

### 1. **Autenticación con Snowflake - Key Pair**

**¿Por qué Key Pair?**
- ✅ Más seguro que contraseña
- ✅ Ideal para CI/CD y Airflow (automatización)
- ✅ No requiere guardar passwords en código

**Cómo funciona:**
```
claves/rsa_key.p8 (PRIVADA)     ← Tu máquina/Airflow
     ↓
Snowflake (verifica con clave pública)
     ↓
Conexión autenticada ✅
```

**Archivos creados:**
- `claves/rsa_key.p8` - Clave privada (NUNCA commitear ❌)
- `claves/rsa_key.pub` - Clave pública (registrada en Snowflake)

**Configuración en `.env`:**
```env
SNOWFLAKE_ACCOUNT=AHRRHGX-FJ87753
SNOWFLAKE_USER=KIKESNOW5
SNOWFLAKE_PRIVATE_KEY_PATH=claves/rsa_key.p8    # ← Ruta a la clave privada
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=MARKET_INTELLIGENCE_DB
```

**Cómo se usa en dbt:**
```yaml
# dbt/profiles.yml
private_key_path: "{{ env_var('SNOWFLAKE_PRIVATE_KEY_PATH') }}"
# dbt lee la variable de .env y usa la clave privada para conectar
```

---

### 2. **dbt - Transformación de datos**

**¿Qué es dbt?**
dbt es un framework que convierte SQL en código versionable y reutilizable.

**Estructura:**
```
dbt/
├── profiles.yml         ← Config conexión Snowflake
├── dbt_project.yml      ← Config del proyecto
├── models/
│   ├── staging/         ← STAGING (limpiar datos crudos)
│   │   └── stg_github_repository_snapshot.sql
│   ├── marts/           ← MART (agregaciones finales)
│   │   └── mart_repository_kpi.sql
│   └── sources/
│       └── sources.yml  ← Define fuentes de datos
└── tests/               ← Validaciones
```

**Modelos que creamos:**

| Modelo | Tipo | Qué hace |
|--------|------|----------|
| `stg_github_repository_snapshot` | VIEW | Limpia datos crudos de GitHub |
| `mart_repository_kpi` | TABLE | Calcula scores de popularidad |

**Cómo se ejecuta:**
```powershell
cd dbt
dbt run      # Crea/actualiza modelos en Snowflake
dbt test     # Valida integridad de datos
```

---

### 3. **Snowflake - Data Warehouse**

**Base de datos estructura:**
```
MARKET_INTELLIGENCE_DB
├── RAW          ← Datos crudos de GitHub
├── STAGING      ← Datos limpios por dbt
└── MART         ← Agregaciones finales (para Power BI)
```

**Tablas creadas por bootstrap SQL:**
- `RAW.GITHUB_REPOSITORY_SNAPSHOT` - Datos crudos
- `STAGING.REPOSITORY_DAILY_METRICS` - Métricas diarias
- `MART.REPOSITORY_KPI` - KPIs finales ← **Conectar Power BI aquí**

---

### 4. **Variables de entorno (`.env`)**

```env
# Datos del proyecto
PROJECT_NAME=market_intelligence_platform
APP_ENV=local
LOG_LEVEL=INFO

# GitHub (para extraer datos)
GITHUB_OWNER=tu-usuario
GITHUB_REPOSITORY=market_intelligence_platform
GITHUB_BRANCH=main

# Snowflake (conexión y credenciales)
SNOWFLAKE_ACCOUNT=AHRRHGX-FJ87753
SNOWFLAKE_USER=KIKESNOW5
SNOWFLAKE_PRIVATE_KEY_PATH=claves/rsa_key.p8    ← Punto clave
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=MARKET_INTELLIGENCE_DB
SNOWFLAKE_SCHEMA=RAW

# dbt
DBT_TARGET=dev
```

**Importante:** `.env` está en `.gitignore` (no se commite). Cada máquina/Airflow tiene la suya.

---

### 5. **Seguridad - .gitignore**

```
.env                    ← Variables sensibles
claves/rsa_key.p8             ← Clave privada
dbt/profiles.yml       ← Conexiones
target/                ← Archivos compilados
```

---

## 🚀 ¿Cómo funciona todo junto?

### Flujo completo:

1. **Local (tu máquina):**
   - Editas SQL/modelos en `dbt/models/`
   - Ejecutas `dbt run` → crea tablas en Snowflake
   - Ejecutas `dbt test` → valida datos

2. **GitHub (CI/CD):**
   - Haces push a main
   - GitHub Actions ejecuta tests automáticamente
   - Si pasan, se mergeea

3. **Airflow (producción):**
   - DAG diario ejecuta `dbt run` @ 2 AM
   - Snowflake se actualiza automáticamente
   - Power BI actualiza dashboards

4. **Power BI (visualización):**
   - Conecta a `MART.mart_repository_kpi`
   - Lee datos frescos cada hora
   - Usuarios ven dashboards en tiempo real

---

## 📋 Archivos claves en el proyecto

| Archivo | Propósito |
|---------|-----------|
| `.env` | Variables de entorno (local, no committear) |
| `dbt/profiles.yml` | Config dbt → Snowflake |
| `dbt/dbt_project.yml` | Config proyecto dbt |
| `dbt/models/staging/*.sql` | Transformaciones iniciales |
| `dbt/models/marts/*.sql` | Agregaciones finales |
| `sql/snowflake/bootstrap_storage.sql` | Inicializa DB/schemas |
| `SETUP_GUIDE.md` | Guía de configuración |
| `docs/AIRFLOW_DBT_INTEGRATION.md` | Cómo integrar con Airflow |

---

## ⚠️ Cosas importantes de recordar

### ✅ HACER
- Editar modelos SQL en `dbt/models/`
- Agregar tests en `dbt/tests/`
- Commitear cambios en modelos a GitHub
- Usar variables de entorno para credenciales

### ❌ NO HACER
- ❌ Commitear `.env`
- ❌ Commitear `claves/rsa_key.p8`
- ❌ Editardatos directamente en Snowflake
- ❌ Modificar `profiles.yml` con valores hardcodeados

---

## 🔄 Ciclo de desarrollo típico

```bash
# 1. Cambiar algo en SQL
vim dbt/models/staging/stg_github_repository_snapshot.sql

# 2. Probar localmente
cd dbt && dbt run

# 3. Validar datos
dbt test

# 4. Si todo ok, commit
git add .
git commit -m "Mejorar transformación de repositorios"
git push

# 5. Airflow ejecuta automáticamente en producción
# (los datos se actualizan sin hacer nada)
```

---

## 🎓 Resumen técnico

| Componente | Función | Estado |
|------------|---------|--------|
| **Autenticación** | Key Pair RSA | ✅ Configurada |
| **dbt** | Transformación SQL | ✅ Funcionando |
| **Snowflake** | Data Warehouse | ✅ Conectado |
| **Bootstrap** | Crear DB/schemas | ✅ Ejecutado |
| **Testing** | Validar datos | ✅ 7/7 tests pasan |
| **Power BI** | Visualización | 🔄 Listo para conectar |
| **Airflow** | Orquestación | 📝 Próximamente |
| **GitHub Actions** | CI/CD | 📝 Próximamente |

---

**Siguiente paso:** Conectar Power BI a `MART.mart_repository_kpi` en Snowflake
