@echo off
setlocal enabledelayedexpansion

echo.
echo ====================================================
echo   ANALIZADOR DE MOVIMIENTO DE VEHICULO
echo   Vision Artificial - Procesamiento IMG
echo ====================================================
echo.

set PYTHON_PATH=C:\Users\juanselm\AppData\Local\Programs\Python\Python313\python.exe

echo [*] Iniciando interfaz grafica...
"%PYTHON_PATH%" gui_analisis.py

if !ERRORLEVEL! neq 0 (
    echo.
    echo [ERROR] Se produjo un error al ejecutar la aplicacion
    pause
    exit /b 1
)

endlocal
