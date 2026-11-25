@echo off
chcp 65001 >nul
echo ============================================================
echo   PlanoIA - Assistente de Planejamento de Aulas (BNCC)
echo ============================================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Criando ambiente virtual Python...
    python -m venv .venv
)

echo [2/3] Verificando dependencias...
.venv\Scripts\python.exe -m pip install -q -r requirements.txt

echo [3/3] Iniciando servidor em http://localhost:8000
echo Pressione CTRL+C para encerrar.
echo.
start "" http://localhost:8000
.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
