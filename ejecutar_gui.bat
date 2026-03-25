@echo off
setlocal enabledelayedexpansion

echo.
echo ====================================================
echo   ANALIZADOR DE MOVIMIENTO DE VEHICULO
echo   Vision Artificial - Procesamiento IMG
echo ====================================================
echo.

REM Verificar si existe el entorno virtual, si no, crearlo
if not exist "venv\Scripts\python.exe" (
    echo [*] Entorno virtual no encontrado. Creando venv...
    python -m venv venv
    if !ERRORLEVEL! neq 0 (
        echo [ERROR] No se pudo crear el entorno virtual.
        echo         Asegurate de tener Python instalado y en el PATH.
        pause
        exit /b 1
    )
    echo [*] Instalando dependencias...
    venv\Scripts\pip install -r requirements.txt
    if !ERRORLEVEL! neq 0 (
        echo [ERROR] No se pudieron instalar las dependencias.
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual listo.
    echo.
)

echo [*] Iniciando interfaz grafica...
venv\Scripts\python gui_analisis.py

if !ERRORLEVEL! neq 0 (
    echo.
    echo [ERROR] Se produjo un error al ejecutar la aplicacion
    pause
    exit /b 1
)

endlocal
