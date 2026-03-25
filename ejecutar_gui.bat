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
    REM Intentar python, si no py
    where python >nul 2>&1
    if !ERRORLEVEL! equ 0 (
        set PYTHON_PATH=python
    ) else (
        set PYTHON_PATH=py
    )
    echo [*] Usando Python del sistema

    REM Instalar dependencias si no estan instaladas
    echo [*] Verificando dependencias...
    "!PYTHON_PATH!" -c "import cv2, numpy, matplotlib" >nul 2>&1
    if !ERRORLEVEL! neq 0 (
        echo [*] Instalando dependencias faltantes...
        "!PYTHON_PATH!" -m pip install opencv-python numpy matplotlib
        if !ERRORLEVEL! neq 0 (
            echo.
            echo [ERROR] No se pudieron instalar las dependencias.
            echo         Ejecuta manualmente: pip install opencv-python numpy matplotlib
            pause
            exit /b 1
        )
        echo [OK] Dependencias instaladas.
        echo.
    ) else (
        echo [OK] Dependencias encontradas.
    )
)

echo [*] Iniciando interfaz grafica...
"!PYTHON_PATH!" gui_analisis.py

if !ERRORLEVEL! neq 0 (
    echo.
    echo [ERROR] Se produjo un error al ejecutar la aplicacion.
    pause
    exit /b 1
)

endlocal
