# Script ejecutador para Windows - Analizador de Vehiculos
# Ejecuta la interfaz grafica con Python 3.13

Write-Host "`n"
Write-Host "====================================================" -ForegroundColor Green
Write-Host "  ANALIZADOR DE MOVIMIENTO DE VEHICULO" -ForegroundColor Green
Write-Host "  Vision Artificial - Procesamiento IMG" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Green
Write-Host "`n"

$PYTHON_PATH = "C:\Users\juanselm\AppData\Local\Programs\Python\Python313\python.exe"

if (Test-Path $PYTHON_PATH) {
    Write-Host "[OK] Iniciando interfaz grafica con Python 3.13..." -ForegroundColor Green
    & $PYTHON_PATH gui_analisis.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Se produjo un error al ejecutar la aplicacion" -ForegroundColor Red
        Read-Host "Presione Enter para continuar"
        exit 1
    }
} else {
    Write-Host "[ERROR] Python 3.13 no encontrado en:" -ForegroundColor Red
    Write-Host $PYTHON_PATH -ForegroundColor Red
    Write-Host "`nPor favor instala Python 3.13" -ForegroundColor Red
    Read-Host "Presione Enter para continuar"
    exit 1
}
