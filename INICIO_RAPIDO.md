# 🚀 Inicio Rápido

## Opción 1: Interfaz Gráfica (Recomendado)

### Windows
```bash
ejecutar_gui.bat
```

### Linux / Mac
```bash
chmod +x ejecutar_gui.sh
./ejecutar_gui.sh
```

### O manualmente
```bash
# Activar entorno virtual (Windows)
..\..\..\..venv\Scripts\activate

# O (Linux/Mac)
source ../../.venv/bin/activate

# Ejecutar
python gui_analisis.py
```

---

## Opción 2: Script Directo (Línea de comandos)

```bash
python tarea1_analisis_vehiculo.py
```

> ⚠️ Antes edita los parámetros en el archivo

---

## ✅ Checklist Rápido

- [ ] Tengo instalado Python 3.8+
- [ ] Tengo las dependencias: `pip install -r requirements.txt`
- [ ] Tengo un video en formato MP4/AVI/MOV
- [ ] El video muestra un vehículo desde vista aérea (superior)
- [ ] Los primeros 3 frames del video NO contienen el vehículo

---

## 📊 Qué esperar

1. **Interfaz gráfica abre** - permite seleccionar video y parámetros
2. **Procesamiento commence** - análisis automático de frames
3. **Se generan 4 archivos PNG** con resultados
4. **Listo en 30-60 segundos** típicamente

---

## 🐛 Si algo falla

### Error: "ModuleNotFoundError: No module named 'cv2'"
```bash
pip install opencv-python numpy matplotlib
```

### Error: "No se pudo abrir el video"
- Verifica la ruta del archivo
- Usa formato MP4 o AVI

### Error: "El vehículo no se detecta"
- Aumenta el umbral de diferencia (THRESHOLD)
- Verifica que el fondo sea uniforme en primeros frames

---

## 📧 Preguntas Frecuentes

**P: ¿Cómo calibro correctamente?**  
R: Mide el vehículo en píxeles, ingresa su largo real en metros.

**P: ¿Funciona con cualquier video?**  
R: Mejor funciona con vista aérea, movimiento horizontal, fondo estático.

**P: ¿Puedo cambiar parámetros después?**  
R: Sí, la GUI lo permite sin editar código.

---

¡Listo! Procede a ejecutar y disfrutar del análisis. 🚗📊
