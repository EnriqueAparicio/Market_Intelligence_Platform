@echo off
REM Load environment variables from .env file
for /f "delims== tokens=1,2" %%A in (.env) do (
    set "%%A=%%B"
)
REM Run dbt debug
cd dbt
dbt debug
