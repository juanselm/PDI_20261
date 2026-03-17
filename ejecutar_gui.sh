#!/bin/bash
# Script lanzador para Linux/Mac - Analizador de Vehículos
# Activa el entorno virtual y ejecuta la interfaz gráfica

echo ""
echo "╔════════════════════════════════════════════╗"
echo "║   ANALIZADOR DE MOVIMIENTO DE VEHICULO    ║"
echo "║   Vision Artificial - Procesamiento IMG   ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Intenta activar el venv en la carpeta padre
VENV_PATH="../../.venv"

if [ -d "$VENV_PATH/bin" ]; then
    echo "[*] Activando entorno virtual..."
    source "$VENV_PATH/bin/activate"
else
    echo "[!] Advertencia: No se encontró el entorno virtual"
    echo "[!] Asegúrate de tener instaladas las dependencias:"
    echo "    pip install opencv-python numpy matplotlib"
    echo ""
fi

echo "[*] Iniciando interfaz gráfica..."
python gui_analisis.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[!] Error al ejecutar la aplicación"
    echo "[*] Verifica que tengas instaladas las dependencias:"
    echo "    pip install -r requirements.txt"
fi
