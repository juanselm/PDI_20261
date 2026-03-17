"""
=============================================================
TAREA 1 - ANÁLISIS DE MOVIMIENTO DE UN VEHÍCULO
Curso: Visión Artificial / Procesamiento de Imágenes
Herramientas: Python 3, OpenCV, NumPy, Matplotlib
=============================================================

DESCRIPCIÓN:
  Analiza el movimiento de un vehículo capturado desde una
  vista aérea. Se aplican técnicas de:
    - Sustracción de fondo (background subtraction)
    - Conversión de espacio de color (BGR → Escala de Grises)
    - Operaciones morfológicas (apertura y cierre)
    - Detección de contornos (cv2.findContours)
    - Cálculo de centroide (cv2.moments)
    - Análisis cinemático: posición, velocidad, aceleración
    - Comparación con modelo cinemático teórico (MRU)

CALIBRACIÓN DE ESCALA:
  El vehículo ocupa ~145 píxeles de largo en el video.
  Un SUV promedio mide ~4.5 m → escala = 4.5 / 145 m/px

=============================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# PARÁMETROS - ajustar según el video utilizado
# ============================================================
VIDEO_PATH = 'video_vehiculo.mp4'  # ruta al video de entrada

# FPS del video (se lee automáticamente, pero se puede forzar)
# FPS = 30.0

# Calibración de escala píxeles → metros
# Medido en el video: el carro ocupa ~145 px de largo (vista superior)
# Un SUV genérico mide ~4.5 m de largo → regla de tres: 145 px = 4.5 m
CAR_LENGTH_PX = 145.0   # píxeles que mide el carro en el video
CAR_LENGTH_M  = 4.5     # metros reales (largo del vehículo)
SCALE = CAR_LENGTH_M / CAR_LENGTH_PX   # metros por píxel

# Punto A y B virtuales (columnas en píxeles)
PUNTO_A_X = 50
PUNTO_B_X = 670

# ============================================================
# 1. CARGAR VIDEO Y EXTRAER INFORMACIÓN
# ============================================================
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    raise FileNotFoundError(f"No se pudo abrir el video: {VIDEO_PATH}")

FPS = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
dt = 1.0 / FPS   # tiempo entre frames en segundos

print("=" * 50)
print("INFORMACIÓN DEL VIDEO")
print("=" * 50)
print(f"  Resolución : {width} x {height} px")
print(f"  FPS        : {FPS:.2f}")
print(f"  Frames     : {total_frames}")
print(f"  Duración   : {total_frames / FPS:.2f} s")
print(f"  dt/frame   : {dt*1000:.2f} ms")
print(f"  Escala     : {SCALE:.4f} m/px  ({1/SCALE:.1f} px/m)")
print("=" * 50)

# Leer todos los frames
frames = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)
cap.release()

# ============================================================
# 2. CONSTRUIR FONDO DE REFERENCIA
#    Se usan los primeros 3 frames donde no hay vehículo.
#    Se aplica mediana para reducir el ruido del sensor.
# ============================================================
# Los primeros frames del video no tienen el carro visible
background = np.median([frames[0], frames[1], frames[2]], axis=0).astype(np.uint8)

# ============================================================
# 3. PROCESAMIENTO FRAME A FRAME
# ============================================================
kernel = np.ones((9, 9), np.uint8)  # elemento estructurante

positions_px   = []   # centroide X en píxeles
positions_m    = []   # centroide X en metros
times          = []   # tiempo en segundos de cada detección
annotated_list = []   # frames anotados para visualización

for i, frame in enumerate(frames):
    t = i * dt   # tiempo de este frame

    # --- 3.1 Conversión a escala de grises y sustracción de fondo ---
    # Calculamos la diferencia absoluta entre frame actual y el fondo
    diff = cv2.absdiff(frame, background)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Umbralización binaria: píxeles con diferencia > 25 son "objetos"
    _, mask = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)

    # --- 3.2 Operaciones morfológicas para limpiar la máscara ---
    # APERTURA (erosión + dilatación): elimina ruido pequeño
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # CIERRE (dilatación + erosión): rellena huecos internos del objeto
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # Dilatación extra para unir partes del carro (techo oscuro vs carrocería)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # --- 3.3 Detección de contornos ---
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        continue   # frame sin objetos detectados

    # Ordenar contornos por área (mayor primero)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Seleccionar el contorno del vehículo:
    # - Descartar si ocupa >50% de la imagen (puede ser el borde capturado)
    # - Descartar si es muy pequeño (<3000 px²) — es ruido
    best_contour = None
    for c in contours:
        area = cv2.contourArea(c)
        if area > (width * height * 0.5):
            continue   # borde de imagen, ignorar
        if area < 3000:
            continue   # ruido pequeño, ignorar
        best_contour = c
        break

    if best_contour is None:
        continue

    # --- 3.4 Cálculo del centroide usando momentos de imagen ---
    M = cv2.moments(best_contour)
    if M['m00'] == 0:
        continue

    cx = int(M['m10'] / M['m00'])   # centroide X
    cy = int(M['m01'] / M['m00'])   # centroide Y

    # Guardar datos
    positions_px.append(cx)
    positions_m.append(cx * SCALE)
    times.append(t)

    # --- 3.5 Anotar el frame para visualización ---
    ann = frame.copy()
    # Contorno verde
    cv2.drawContours(ann, [best_contour], -1, (0, 255, 0), 2)
    # Bounding box naranja
    x, y, w, h = cv2.boundingRect(best_contour)
    cv2.rectangle(ann, (x, y), (x + w, y + h), (255, 165, 0), 2)
    # Centroide rojo
    cv2.circle(ann, (cx, cy), 7, (0, 0, 255), -1)
    # Líneas A y B (puntos de referencia virtuales)
    cv2.line(ann, (PUNTO_A_X, 0), (PUNTO_A_X, height), (0, 255, 255), 2)
    cv2.line(ann, (PUNTO_B_X, 0), (PUNTO_B_X, height), (0, 255, 255), 2)
    cv2.putText(ann, 'A', (PUNTO_A_X - 15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(ann, 'B', (PUNTO_B_X + 5,  30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    # Info en pantalla
    cv2.putText(ann, f't={t:.2f}s  X={cx}px={cx*SCALE:.2f}m',
                (10, height - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    annotated_list.append(ann)

print(f"Frames con detección: {len(positions_px)} de {total_frames}")

# ============================================================
# 4. ANÁLISIS CINEMÁTICO
# ============================================================
positions_px = np.array(positions_px)
positions_m  = np.array(positions_m)
times        = np.array(times)

# --- Velocidad: diferencias finitas (Δx / Δt) ---
# v[i] = (x[i+1] - x[i-1]) / (2·Δt)  — gradiente centrado
velocities_ms  = np.gradient(positions_m, times)   # m/s
velocities_kmh = velocities_ms * 3.6               # km/h

# --- Aceleración: derivada de la velocidad ---
accel_ms2 = np.gradient(velocities_ms, times)      # m/s²

print("\n" + "=" * 50)
print("RESULTADOS CINEMÁTICOS")
print("=" * 50)
print(f"  Posición inicial : {positions_m[0]:.2f} m")
print(f"  Posición final   : {positions_m[-1]:.2f} m")
print(f"  Distancia total  : {positions_m[-1] - positions_m[0]:.2f} m")
print(f"  Velocidad media  : {velocities_ms.mean():.2f} m/s = {velocities_kmh.mean():.1f} km/h")
print(f"  Vel. máxima      : {velocities_ms.max():.2f} m/s = {velocities_kmh.max():.1f} km/h")
print(f"  Aceleración media: {accel_ms2.mean():.2f} m/s²")
print("=" * 50)

# ============================================================
# 5. MODELO CINEMÁTICO TEÓRICO (MRU — Movimiento Rectilíneo Uniforme)
#    El vehículo se mueve a velocidad aproximadamente constante,
#    por lo tanto el modelo MRU es el más adecuado.
#
#    Ecuación:  x(t) = x₀ + v₀ · (t - t₀)
# ============================================================
v0_teorico  = velocities_ms.mean()   # velocidad constante teórica
x0_teorico  = positions_m[0]         # posición inicial
t0          = times[0]               # tiempo inicial
pos_teorico = x0_teorico + v0_teorico * (times - t0)

# ============================================================
# 6. GRÁFICAS
# ============================================================
fig, axes = plt.subplots(3, 1, figsize=(12, 11))
fig.suptitle(
    'Análisis Cinemático del Vehículo — Vista Aérea\n'
    f'Escala: {SCALE:.4f} m/px | FPS: {FPS:.1f} | Vel. media: {velocities_kmh.mean():.1f} km/h',
    fontsize=13, fontweight='bold'
)

# --- Gráfica 1: Posición ---
axes[0].plot(times, positions_m, 'b-o', markersize=3, linewidth=1.5,
             label='Posición experimental (visión artificial)')
axes[0].plot(times, pos_teorico, 'r--', linewidth=2,
             label=f'Modelo MRU teórico  (v₀ = {v0_teorico:.2f} m/s)')
axes[0].axvline(times[0],  color='cyan', linestyle=':', label='Punto A (inicio)')
axes[0].axvline(times[-1], color='cyan', linestyle=':', label='Punto B (fin)')
axes[0].set_xlabel('Tiempo (s)')
axes[0].set_ylabel('Posición X (m)')
axes[0].set_title('Posición vs Tiempo')
axes[0].legend(fontsize=9)
axes[0].grid(True, alpha=0.4)

# --- Gráfica 2: Velocidad ---
ax2 = axes[1].twinx()
axes[1].plot(times, velocities_ms,  'g-o', markersize=3, linewidth=1.5, label='Velocidad (m/s)')
ax2.plot(times, velocities_kmh, 'g--', alpha=0.3, linewidth=1)
axes[1].axhline(velocities_ms.mean(), color='orange', linestyle='--', linewidth=2,
                label=f'Velocidad media = {velocities_ms.mean():.2f} m/s ({velocities_kmh.mean():.1f} km/h)')
axes[1].set_xlabel('Tiempo (s)')
axes[1].set_ylabel('Velocidad (m/s)')
ax2.set_ylabel('Velocidad (km/h)', color='g')
axes[1].set_title('Velocidad vs Tiempo')
axes[1].legend(fontsize=9)
axes[1].grid(True, alpha=0.4)

# --- Gráfica 3: Aceleración ---
axes[2].plot(times, accel_ms2, 'r-o', markersize=3, linewidth=1.5, label='Aceleración (m/s²)')
axes[2].axhline(0, color='black', linestyle='--', linewidth=1)
axes[2].axhline(accel_ms2.mean(), color='orange', linestyle='--', linewidth=2,
                label=f'Aceleración media = {accel_ms2.mean():.2f} m/s²')
axes[2].set_xlabel('Tiempo (s)')
axes[2].set_ylabel('Aceleración (m/s²)')
axes[2].set_title('Aceleración vs Tiempo')
axes[2].legend(fontsize=9)
axes[2].grid(True, alpha=0.4)

plt.tight_layout()
plt.savefig('graficas_cinematica.png', dpi=150, bbox_inches='tight')
print("\nGráficas guardadas: graficas_cinematica.png")

# ============================================================
# 7. VISUALIZACIÓN DE FRAMES ANOTADOS
# ============================================================
fig2, axes2 = plt.subplots(2, 3, figsize=(15, 8))
fig2.suptitle('Detección y Segmentación del Vehículo\n'
              '(Verde: contorno | Rojo: centroide | Naranja: bounding box | Cyan: puntos A-B)',
              fontsize=11, fontweight='bold')

step = max(1, len(annotated_list) // 6)
samples = annotated_list[::step][:6]
for ax, frm in zip(axes2.flat, samples):
    ax.imshow(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
    ax.axis('off')
for ax in axes2.flat[len(samples):]:
    ax.axis('off')

plt.tight_layout()
plt.savefig('frames_anotados.png', dpi=120, bbox_inches='tight')
print("Frames anotados guardados: frames_anotados.png")

# ============================================================
# 8. TRAYECTORIA SUPERPUESTA EN UN FRAME
# ============================================================
# Dibujar todos los centroides detectados como puntos de trayectoria
cap2 = cv2.VideoCapture(VIDEO_PATH)
raw_frames = []
while cap2.isOpened():
    ret, f = cap2.read()
    if not ret: break
    raw_frames.append(f)
cap2.release()

if not raw_frames:
    raise RuntimeError("No se pudieron leer frames para construir la trayectoria")

base_idx = min(40, len(raw_frames) - 1)
traj_img = raw_frames[base_idx].copy()

# Crear imagen de trayectoria simple
traj_img = raw_frames[base_idx].copy()
for i in range(len(positions_px)):
    cy_approx = 135  # los centroides Y varían poco (movimiento horizontal)
    color_factor = int(255 * i / len(positions_px))
    cv2.circle(traj_img, (positions_px[i], cy_approx), 4,
               (0, color_factor, 255 - color_factor), -1)
    if i > 0:
        cv2.line(traj_img, (positions_px[i-1], cy_approx),
                 (positions_px[i], cy_approx), (0, 200, 255), 2)

cv2.line(traj_img, (PUNTO_A_X, 0), (PUNTO_A_X, height), (0, 255, 255), 2)
cv2.line(traj_img, (PUNTO_B_X, 0), (PUNTO_B_X, height), (0, 255, 255), 2)
cv2.putText(traj_img, 'A', (PUNTO_A_X - 15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
cv2.putText(traj_img, 'B', (PUNTO_B_X + 5, 30),  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
cv2.putText(traj_img, 'Trayectoria del centroide', (10, height-15),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)

cv2.imwrite('trayectoria.png', traj_img)
print("Trayectoria guardada: trayectoria.png")

plt.figure(figsize=(10, 5))
plt.imshow(cv2.cvtColor(traj_img, cv2.COLOR_BGR2RGB))
plt.title('Trayectoria del centroide del vehículo (A -> B)')
plt.axis('off')
plt.tight_layout()
plt.savefig('trayectoria_plot.png', dpi=120, bbox_inches='tight')

print("\n[OK] PROCESAMIENTO COMPLETO")
print(f"   Tipo de movimiento detectado: MRU (Movimiento Rectilíneo Uniforme)")
print(f"   Velocidad estimada: {velocities_kmh.mean():.1f} km/h")

# Comentar plt.show() para permitir ejecución sin interfaz gráfica
# plt.show()
