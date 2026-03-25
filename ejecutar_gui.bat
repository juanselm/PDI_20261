@echo off
setlocal enabledelayedexpansion

echo.
echo ====================================================
echo   ANALIZADOR DE MOVIMIENTO DE VEHICULO
echo   Vision Artificial - Procesamiento IMG
echo ====================================================
echo.

REM Intentar usar el venv local primero, si no existe usar python del sistema
if exist "venv\Scripts\python.exe" (
    set PYTHON_PATH=venv\Scripts\python.exe
    echo [*] Usando entorno virtual local: venv
) else if exist ".venv\Scripts\python.exe" (
    set PYTHON_PATH=.venv\Scripts\python.exe
    echo [*] Usando entorno virtual local: .venv
) else (
    set PYTHON_PATH=python
    echo [*] Usando Python del sistema
)

echo [*] Iniciando interfaz grafica...
"%PYTHON_PATH%" gui_analisis.py

if !ERRORLEVEL! neq 0 (
    echo.
    echo [ERROR] Se produjo un error al ejecutar la aplicacion
    echo         Asegurate de tener las dependencias instaladas:
    echo         pip install -r requirements.txt
    pause
    exit /b 1
)

endlocal
