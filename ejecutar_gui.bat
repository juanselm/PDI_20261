@echo off
setlocal enabledelayedexpansion

echo.
echo ====================================================
echo   ANALIZADOR DE MOVIMIENTO DE VEHICULO
echo   Vision Artificial - Procesamiento IMG
echo ====================================================
echo.

REM Buscar Python: primero venv local, luego sistema
if exist "venv\Scripts\python.exe" (
    set PYTHON_PATH=venv\Scripts\python.exe
    echo [*] Usando entorno virtual: venv
) else if exist ".venv\Scripts\python.exe" (
    set PYTHON_PATH=.venv\Scripts\python.exe
    echo [*] Usando entorno virtual: .venv
) else (
    set PYTHON_PATH=python
    echo [*] Usando Python del sistema
)

echo [*] Iniciando interfaz grafica...
"%PYTHON_PATH%" gui_analisis.py

if !ERRORLEVEL! neq 0 (
    echo.
    echo [ERROR] Se produjo un error al ejecutar la aplicacion.
    echo         Si faltan dependencias ejecuta:
    echo         pip install -r requirements.txt
    pause
    exit /b 1
)

endlocal
