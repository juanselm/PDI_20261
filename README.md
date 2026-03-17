# 🚗 Analizador de Movimiento de Vehículo - Visión Artificial

## 📋 Descripción General

Este proyecto realiza un **análisis cinemático de movimiento de un vehículo** capturado desde una vista aérea utilizando técnicas de **procesamiento digital de imágenes** y **visión artificial**.

### Características Principales

- ✅ **Detección automática** del vehículo en video mediante sustracción de fondo
- ✅ **Análisis cinemático**: calcula posición, velocidad y aceleración en tiempo real
- ✅ **Comparación con modelo teórico**: MRU (Movimiento Rectilíneo Uniforme)
- ✅ **Generación de gráficas**: visualización temporal de cinemática
- ✅ **Anotación de frames**: detección del centroide y trayectoria del vehículo
- ✅ **Interfaz gráfica (GUI)**: fácil de usar, sin necesidad de código

---

## 📊 Técnicas Utilizadas

| Técnica | Propósito |
|---------|-----------|
| **Sustracción de Fondo** | Aislar el vehículo del fondo estático |
| **Conversión de Color** | Pasar de BGR a escala de grises |
| **Operaciones Morfológicas** | Apertura y cierre para limpiar la máscara |
| **Detección de Contornos** | Encontrar el límite del vehículo |
| **Cálculo de Centroide** | Detectar la posición central del vehículo |
| **Análisis Diferencial** | Calcular velocidad y aceleración |

---

## 🛠️ Requisitos del Sistema

### Dependencias Python

```
opencv-python==4.13.0.92
numpy==2.4.2
matplotlib==3.10.8
```

### Sistema Operativo
- Windows, Linux o macOS
- Python 3.8 o superior
- 2 GB RAM mínimo

---

## 📦 Instalación

### 1. **Clonar o descargar el proyecto**

```bash
cd tu-carpeta-proyecto
```

### 2. **Crear entorno virtual (opcional pero recomendado)**

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. **Instalar dependencias**

```bash
pip install opencv-python numpy matplotlib
```

O si tienes un `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 🚀 Modo de Uso

### **Opción A: Interfaz Gráfica (Recomendado)**

```bash
python gui_analisis.py
```

**Pasos:**
1. Click en el botón **"Examinar..."** para seleccionar un video
2. Ajusta los parámetros de calibración:
   - Largo del vehículo en píxeles (ej: 145 px)
   - Largo real del vehículo en metros (ej: 4.5 m)
   - Puntos A y B de referencia
3. Personaliza parámetros de procesamiento si es necesario
4. Click en **"INICIAR ANÁLISIS"**
5. Espera a que termine (30-60 segundos típicamente)
6. Revisa los archivos PNG generados

### **Opción B: Script Directo (Avanzado)**

Edita los parámetros en `tarea1_analisis_vehiculo.py`:

```python
VIDEO_PATH = 'video_vehiculo.mp4'
CAR_LENGTH_PX = 145.0   # píxeles que mide el carro
CAR_LENGTH_M = 4.5      # metros reales
```

Luego ejecuta:

```bash
python tarea1_analisis_vehiculo.py
```

---

## 📐 Calibración de Escala

### ¿Cómo calibrar correctamente?

1. **Abre el video** en la interfaz GUI
2. **Mide el vehículo** en píxeles (ancho o largo)
3. **Ingresa el valor real** en metros
4. La **escala se calcula automáticamente**: 
   ```
   escala = largo_metros / largo_píxeles
   ```

### Ejemplo

Si el vehículo ocupa ~145 píxeles en el video y mide 4.5 metros de largo:
```
escala = 4.5 / 145 = 0.0310 m/px
```

---

## 📤 Salidas Generadas

| Archivo | Descripción |
|---------|------------|
| **graficas_cinematica.png** | Gráficas de posición, velocidad y aceleración vs tiempo |
| **frames_anotados.png** | Mosaico de 6 frames con detección anotada |
| **trayectoria.png** | Trayectoria superpuesta sobre un frame del video |
| **trayectoria_plot.png** | Gráfico de la trayectoria del centroide |

---

## 📊 Interpretación de Resultados

### Gráfica 1: Posición vs Tiempo
- **Línea azul**: posición experimental medida por visión artificial
- **Línea roja punteada**: modelo teórico MRU

Si ambas coinciden, el vehículo se mueve con velocidad aproximadamente constante.

### Gráfica 2: Velocidad vs Tiempo
- Muestra cómo varía la velocidad instantánea
- **Línea naranja**: velocidad media
- Si es plana, el movimiento es uniforme (MRU)

### Gráfica 3: Aceleración vs Tiempo
- Indica cambios en la velocidad
- Cerca de 0 → movimiento uniforme
- Picos → cambios en velocidad

---

## ⚙️ Parámetros Ajustables

### Calibración
- **CAR_LENGTH_PX**: Largo del vehículo en píxeles (medido en el video)
- **CAR_LENGTH_M**: Largo real del vehículo en metros
- **PUNTO_A_X**: Posición X del punto de referencia A (píxeles)
- **PUNTO_B_X**: Posición X del punto de referencia B (píxeles)

### Procesamiento
- **THRESHOLD**: Umbral de diferencia para sustracción de fondo (recomendado: 20-30)
- **KERNEL_SIZE**: Tamaño del kernel para operaciones morfológicas (debe ser impar: 3, 5, 7, 9...)

---

## 🐛 Troubleshooting

### Problema: "No se encontró el video"
**Solución**: Verifica que:
- La ruta del video sea correcta
- El archivo exista en esa ubicación
- El formato sea compatible (MP4, AVI, MOV)

### Problema: "El vehículo no se detecta bien"
**Solución**:
1. Aumenta el umbral de diferencia (THRESHOLD)
2. Aumenta el tamaño del kernel (KERNEL_SIZE)
3. Verifica que los primeros 3 frames no contengan el vehículo (se usan como fondo)

### Problema: "Muchos falsos positivos"
**Solución**:
1. Disminuye el umbral (THRESHOLD)
2. Aumenta el área mínima de contorno (MIN_AREA)

### Problema: "Python no reconoce OpenCV"
**Solución**:
```bash
pip install --upgrade opencv-python
```

---

## 📚 Referencias Teóricas

### Movimiento Rectilíneo Uniforme (MRU)
- Velocidad constante (aceleración = 0)
- Ecuación: `x(t) = x₀ + v₀·t`

### Cálculo Diferencial en Análisis
```
velocidad = dx/dt ≈ Δx/Δt
aceleración = dv/dt ≈ Δv/Δt
```

---

## 👨‍💻 Estructura del Proyecto

```
trabajo1/
├── tarea1_analisis_vehiculo.py     # Script principal (versión avanzada)
├── gui_analisis.py                 # Interfaz gráfica
├── README.md                       # Este archivo
├── video_vehiculo.mp4              # Video de entrada
├── graficas_cinematica.png         # Salida: gráficas
├── frames_anotados.png             # Salida: frames
├── trayectoria.png                 # Salida: trayectoria
└── trayectoria_plot.png            # Salida: gráfico trayectoria
```

---

## 📝 Notas Importantes

1. ✅ **Calibración es crítica**: Una calibración incorrecta invalida todos los resultados
2. ✅ **Iluminación**: Asegúrate de que el video tenga buena iluminación
3. ✅ **Fondo estático**: Los primeros frames deben mostrar el fondo sin vehículo
4. ✅ **Movimiento horizontal**: Funciona mejor con movimiento en el eje X (izquierda-derecha)

---

## 📧 Contacto y Soporte

Para preguntas o problemas, revisa primero:
- Este README
- Los comentarios en el código
- Las salidas de error en la terminal

---

**Última actualización**: Marzo 2026

**Curso**: Procesamiento Digital de Imágenes  
**Universidad**: Universidad de Antioquia  
**Autor**: Análisis Cinemático de Vehículos
