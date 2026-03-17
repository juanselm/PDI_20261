"""
=============================================================
INTERFAZ GRÁFICA - ANÁLISIS DE MOVIMIENTO DE VEHÍCULO
=============================================================
Proporciona una interfaz amigable para ejecutar el análisis
de movimiento del vehículo sin necesidad de editar código.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import subprocess
import threading
from pathlib import Path


class AnalizadorVehiculoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Movimiento de Vehículo - Visión Artificial")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        
        # Variable para almacenar la ruta del video
        self.video_path = tk.StringVar(value="video_vehiculo.mp4")
        
        # Variables para parámetros
        self.car_length_px = tk.DoubleVar(value=145.0)
        self.car_length_m = tk.DoubleVar(value=4.5)
        self.punto_a = tk.DoubleVar(value=50)
        self.punto_b = tk.DoubleVar(value=670)
        self.threshold = tk.IntVar(value=25)
        self.kernel_size = tk.IntVar(value=9)
        
        self.analyzing = False
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Crear los widgets de la interfaz"""
        
        # ===== ESTILO =====
        style = ttk.Style()
        style.theme_use('clam')
        
        # ===== FRAME SUPERIOR: Selección de Video =====
        frame_video = ttk.LabelFrame(self.root, text="[VIDEO] Selección de Video", padding=10)
        frame_video.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_video, text="Video:").pack(side=tk.LEFT)
        ttk.Entry(frame_video, textvariable=self.video_path, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_video, text="Examinar...", command=self._select_video).pack(side=tk.LEFT)
        
        # ===== FRAME PARÁMETROS CALIBRACIÓN =====
        frame_calib = ttk.LabelFrame(self.root, text="[CALIB] Calibración (Escala)", padding=10)
        frame_calib.pack(fill=tk.X, padx=10, pady=5)
        
        # Fila 1: Largo del vehículo
        ttk.Label(frame_calib, text="Largo del vehículo en video (píxeles):").grid(row=0, column=0, sticky=tk.W)
        ttk.Spinbox(frame_calib, from_=10, to=500, textvariable=self.car_length_px, width=15).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(frame_calib, text="Largo real del vehículo (metros):").grid(row=1, column=0, sticky=tk.W)
        ttk.Spinbox(frame_calib, from_=1, to=10, increment=0.1, textvariable=self.car_length_m, width=15).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # Fila 2: Puntos de referencia
        ttk.Label(frame_calib, text="Punto A (posición X en píxeles):").grid(row=2, column=0, sticky=tk.W)
        ttk.Spinbox(frame_calib, from_=0, to=2000, textvariable=self.punto_a, width=15).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(frame_calib, text="Punto B (posición X en píxeles):").grid(row=3, column=0, sticky=tk.W)
        ttk.Spinbox(frame_calib, from_=0, to=2000, textvariable=self.punto_b, width=15).grid(row=3, column=1, sticky=tk.W, padx=5)
        
        # ===== FRAME PARÁMETROS PROCESAMIENTO =====
        frame_proc = ttk.LabelFrame(self.root, text="[CONFIG] Parámetros de Procesamiento", padding=10)
        frame_proc.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_proc, text="Umbral de diferencia (0-255):").grid(row=0, column=0, sticky=tk.W)
        ttk.Spinbox(frame_proc, from_=0, to=255, textvariable=self.threshold, width=15).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(frame_proc, text="Tamaño kernel morfología (impar):").grid(row=1, column=0, sticky=tk.W)
        ttk.Spinbox(frame_proc, from_=3, to=21, increment=2, textvariable=self.kernel_size, width=15).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # ===== FRAME INFORMACIÓN =====
        frame_info = ttk.LabelFrame(self.root, text="[INFO] Información", padding=10)
        frame_info.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.info_text = scrolledtext.ScrolledText(frame_info, height=12, width=80, 
                                                     state=tk.DISABLED, bg="#f0f0f0", 
                                                     relief=tk.FLAT, wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Agregar información inicial
        self._update_info()
        
        # ===== FRAME BOTONES =====
        frame_botones = ttk.Frame(self.root)
        frame_botones.pack(fill=tk.X, padx=10, pady=10)
        
        self.btn_analizar = ttk.Button(frame_botones, text="[RUN] INICIAR ANÁLISIS", 
                                       command=self._iniciar_analisis, width=40)
        self.btn_analizar.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_botones, text="[RESET] Resetear Parámetros", 
                  command=self._resetear_parametros).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_botones, text="[EXIT] Salir", 
                  command=self.root.quit).pack(side=tk.RIGHT, padx=5)
        
    def _select_video(self):
        """Permitir seleccionar un video"""
        file = filedialog.askopenfilename(
            title="Seleccionar video",
            filetypes=[("Video files", "*.mp4 *.avi *.mov"), ("All files", "*.*")],
            initialdir=os.getcwd()
        )
        if file:
            self.video_path.set(file)
            self._update_info()
    
    def _resetear_parametros(self):
        """Resetear parámetros a valores por defecto"""
        self.video_path.set("video_vehiculo.mp4")
        self.car_length_px.set(145.0)
        self.car_length_m.set(4.5)
        self.punto_a.set(50)
        self.punto_b.set(670)
        self.threshold.set(25)
        self.kernel_size.set(9)
        self._update_info()
    
    def _update_info(self):
        """Actualizar el área de información"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        
        info = """
========================================================================
   ANALISIS CINEMATICO DE MOVIMIENTO DE VEHICULO
   Vision Artificial & Procesamiento de Imagenes
========================================================================

[PARAMETROS ACTUALES]:
------------------------------------------------------------------------
  Video:                    {video}
  
  Calibracion:
    - Largo vehiculo (px):  {px} pixeles
    - Largo real (m):       {m} metros
    - Escala:               {scale:.5f} m/px
    
  Puntos de referencia:
    - Punto A:              {pa} pixeles
    - Punto B:              {pb} pixeles
    
  Procesamiento:
    - Umbral diferencia:    {thresh}
    - Kernel morfologia:    {kernel}x{kernel}

[DESCRIPCION]:
------------------------------------------------------------------------
Este programa analiza el movimiento de un vehiculo en video desde
una vista aerea usando tecnicas de:
  - Sustraccion de fondo
  - Deteccion de contornos
  - Analisis cinematico (posicion, velocidad, aceleracion)
  - Comparacion con modelo MRU (Movimiento Rectilineо Uniforme)

[INSTRUCCIONES]:
------------------------------------------------------------------------
1. Selecciona un archivo de video (formato .mp4, .avi, .mov)
2. Ajusta los parametros segun sea necesario
3. Click en INICIAR ANALISIS
4. El analisis generara:
   - graficas_cinematica.png     (graficas de analisis)
   - frames_anotados.png        (deteccion del vehiculo)
   - trayectoria.png            (trayectoria superpuesta)
   - trayectoria_plot.png       (grafico de trayectoria)

TIEMPO ESTIMADO: 30-60 segundos segun duracion del video
        """.format(
            video=self.video_path.get() if self.video_path.get() else "No seleccionado",
            px=int(self.car_length_px.get()),
            m=self.car_length_m.get(),
            scale=self.car_length_m.get() / self.car_length_px.get(),
            pa=int(self.punto_a.get()),
            pb=int(self.punto_b.get()),
            thresh=self.threshold.get(),
            kernel=self.kernel_size.get()
        )
        
        self.info_text.insert(tk.END, info)
        self.info_text.config(state=tk.DISABLED)
    
    def _log(self, mensaje):
        """Agregar mensaje al log"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.insert(tk.END, f"\n{mensaje}")
        self.info_text.see(tk.END)
        self.info_text.config(state=tk.DISABLED)
        self.root.update()
    
    def _iniciar_analisis(self):
        """Iniciar el análisis en un thread separado"""
        if self.analyzing:
            messagebox.showwarning("En progreso", "Ya hay un análisis en ejecución")
            return
        
        if not os.path.exists(self.video_path.get()):
            messagebox.showerror("Error", f"No se encontró el video: {self.video_path.get()}")
            return
        
        # Desactivar botón y cambiar interfaz
        self.btn_analizar.config(state=tk.DISABLED)
        self.analyzing = True
        
        # Ejecutar análisis en thread separado para no congelar interfaz
        thread = threading.Thread(target=self._ejecutar_analisis, daemon=True)
        thread.start()
    
    def _ejecutar_analisis(self):
        """Ejecutar el análisis (en thread)"""
        try:
            self._log("\n" + "="*65)
            self._log("[*] INICIANDO ANÁLISIS...")
            self._log("="*65)
            
            # Crear script temporal con parámetros
            script_path = "analisis_temp.py"
            
            video_path = self.video_path.get().replace("\\", "\\\\")
            
            script_content = f"""
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Solicitar UTF-8 para stdout
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

VIDEO_PATH = '{video_path}'
CAR_LENGTH_PX = {self.car_length_px.get()}
CAR_LENGTH_M = {self.car_length_m.get()}
SCALE = CAR_LENGTH_M / CAR_LENGTH_PX
PUNTO_A_X = {int(self.punto_a.get())}
PUNTO_B_X = {int(self.punto_b.get())}
THRESHOLD = {self.threshold.get()}
KERNEL_SIZE = {self.kernel_size.get()}

# Cargar video
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise FileNotFoundError(f"No se pudo abrir: {{VIDEO_PATH}}")

FPS = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
dt = 1.0 / FPS

print(f"[INFO] Video cargado: {{width}}x{{height}} @{{FPS:.1f}}fps, {{total_frames}} frames")

frames = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)
cap.release()

background = np.median([frames[0], frames[1], frames[2]], axis=0).astype(np.uint8)
kernel = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)

positions_px = []
positions_m = []
times = []
annotated_list = []

for i, frame in enumerate(frames):
    t = i * dt
    diff = cv2.absdiff(frame, background)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, THRESHOLD, 255, cv2.THRESH_BINARY)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.dilate(mask, kernel, iterations=1)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        continue
    
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    best_contour = None
    for c in contours:
        area = cv2.contourArea(c)
        if area > (width * height * 0.5) or area < 3000:
            continue
        best_contour = c
        break
    
    if best_contour is None:
        continue
    
    M = cv2.moments(best_contour)
    if M['m00'] == 0:
        continue
    
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    
    positions_px.append(cx)
    positions_m.append(cx * SCALE)
    times.append(t)
    
    ann = frame.copy()
    cv2.drawContours(ann, [best_contour], -1, (0, 255, 0), 2)
    x, y, w, h = cv2.boundingRect(best_contour)
    cv2.rectangle(ann, (x, y), (x + w, y + h), (255, 165, 0), 2)
    cv2.circle(ann, (cx, cy), 7, (0, 0, 255), -1)
    cv2.line(ann, (PUNTO_A_X, 0), (PUNTO_A_X, height), (0, 255, 255), 2)
    cv2.line(ann, (PUNTO_B_X, 0), (PUNTO_B_X, height), (0, 255, 255), 2)
    cv2.putText(ann, 'A', (PUNTO_A_X - 15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(ann, 'B', (PUNTO_B_X + 5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(ann, f't={{t:.2f}}s  X={{cx}}px={{cx*SCALE:.2f}}m', (10, height - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    annotated_list.append(ann)
    
    if (i + 1) % max(1, len(frames) // 10) == 0:
        print(f"Procesado {{i+1}}/{{len(frames)}}")

print(f"Frames detectados: {{len(positions_px)}}")

positions_px = np.array(positions_px)
positions_m = np.array(positions_m)
times = np.array(times)

velocities_ms = np.gradient(positions_m, times)
velocities_kmh = velocities_ms * 3.6
accel_ms2 = np.gradient(velocities_ms, times)

v0_teorico = velocities_ms.mean()
x0_teorico = positions_m[0]
t0 = times[0]
pos_teorico = x0_teorico + v0_teorico * (times - t0)

fig, axes = plt.subplots(3, 1, figsize=(12, 11))
fig.suptitle(f'Análisis Cinemático | Escala: {{SCALE:.4f}} m/px | Vel. media: {{velocities_kmh.mean():.1f}} km/h', fontsize=13, fontweight='bold')

axes[0].plot(times, positions_m, 'b-o', markersize=3, linewidth=1.5, label='Experimental')
axes[0].plot(times, pos_teorico, 'r--', linewidth=2, label=f'MRU (v₀={{v0_teorico:.2f}} m/s)')
axes[0].set_xlabel('Tiempo (s)')
axes[0].set_ylabel('Posición X (m)')
axes[0].set_title('Posición vs Tiempo')
axes[0].legend()
axes[0].grid(True, alpha=0.4)

axes[1].plot(times, velocities_ms, 'g-o', markersize=3, linewidth=1.5)
axes[1].axhline(velocities_ms.mean(), color='orange', linestyle='--', linewidth=2, label=f'Media={{velocities_ms.mean():.2f}} m/s')
axes[1].set_xlabel('Tiempo (s)')
axes[1].set_ylabel('Velocidad (m/s)')
axes[1].set_title('Velocidad vs Tiempo')
axes[1].legend()
axes[1].grid(True, alpha=0.4)

axes[2].plot(times, accel_ms2, 'r-o', markersize=3, linewidth=1.5)
axes[2].axhline(0, color='black', linestyle='--', linewidth=1)
axes[2].axhline(accel_ms2.mean(), color='orange', linestyle='--', linewidth=2, label=f'Media={{accel_ms2.mean():.2f}} m/s²')
axes[2].set_xlabel('Tiempo (s)')
axes[2].set_ylabel('Aceleración (m/s²)')
axes[2].set_title('Aceleración vs Tiempo')
axes[2].legend()
axes[2].grid(True, alpha=0.4)

plt.tight_layout()
plt.savefig('graficas_cinematica.png', dpi=150, bbox_inches='tight')

fig2, axes2 = plt.subplots(2, 3, figsize=(15, 8))
fig2.suptitle('Detección y Segmentación del Vehículo', fontsize=11, fontweight='bold')
step = max(1, len(annotated_list) // 6)
samples = annotated_list[::step][:6]
for ax, frm in zip(axes2.flat, samples):
    ax.imshow(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
    ax.axis('off')

plt.tight_layout()
plt.savefig('frames_anotados.png', dpi=120, bbox_inches='tight')

cap2 = cv2.VideoCapture(VIDEO_PATH)
raw_frames = []
while cap2.isOpened():
    ret, f = cap2.read()
    if not ret: 
        break
    raw_frames.append(f)
cap2.release()

base_idx = min(40, len(raw_frames) - 1)
traj_img = raw_frames[base_idx].copy()
for i in range(len(positions_px)):
    cy_approx = 135
    color_factor = int(255 * i / len(positions_px))
    cv2.circle(traj_img, (positions_px[i], cy_approx), 4, (0, color_factor, 255 - color_factor), -1)
    if i > 0:
        cv2.line(traj_img, (positions_px[i-1], cy_approx), (positions_px[i], cy_approx), (0, 200, 255), 2)

cv2.line(traj_img, (PUNTO_A_X, 0), (PUNTO_A_X, height), (0, 255, 255), 2)
cv2.line(traj_img, (PUNTO_B_X, 0), (PUNTO_B_X, height), (0, 255, 255), 2)
cv2.putText(traj_img, 'Trayectoria del centroide', (10, height-15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
cv2.imwrite('trayectoria.png', traj_img)

plt.figure(figsize=(10, 5))
plt.imshow(cv2.cvtColor(traj_img, cv2.COLOR_BGR2RGB))
plt.title('Trayectoria del centroide del vehículo')
plt.axis('off')
plt.tight_layout()
plt.savefig('trayectoria_plot.png', dpi=120, bbox_inches='tight')

print("[OK] ANÁLISIS COMPLETADO")
print(f"Velocidad media: {{velocities_kmh.mean():.1f}} km/h")
"""
            
            # Guardar script temporal con encoding UTF-8
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            # Ejecutar script con encoding UTF-8
            import os
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            
            result = subprocess.run(['python', script_path], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=600,
                                  env=env,
                                  encoding='utf-8')
            
            if result.returncode == 0:
                self._log(result.stdout)
                self._log("\n[OK] ANÁLISIS COMPLETADO EXITOSAMENTE")
                self._log("\nArchivos generados:")
                self._log("  - graficas_cinematica.png")
                self._log("  - frames_anotados.png")
                self._log("  - trayectoria.png")
                self._log("  - trayectoria_plot.png")
                messagebox.showinfo("Exito", "Análisis completado. Revisa los archivos PNG generados.")
            else:
                self._log("\n[ERROR] EN EL ANÁLISIS:")
                self._log(result.stderr)
                messagebox.showerror("Error", f"Error durante el análisis:\n{result.stderr}")
            
            # Limpiar
            if os.path.exists(script_path):
                os.remove(script_path)
                
        except Exception as e:
            self._log(f"\n[ERROR] {str(e)}")
            messagebox.showerror("Error", f"Error: {str(e)}")
        
        finally:
            self.analyzing = False
            self.btn_analizar.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    app = AnalizadorVehiculoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
