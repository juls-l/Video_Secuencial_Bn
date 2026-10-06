import cv2              # OpenCV: lectura y escritura de videos
import numpy as np
from PIL import Image   # Pillow: manipulación de imágenes
import time
import sys

# ------------------------------
# 1. Definir rutas de entrada (.webm) y salida (.mp4)
# ------------------------------
ruta_entrada = "Video/video_color.webm"
ruta_salida = "resultado/video_bn.mp4"

# ------------------------------
# 2. Abrir el video original con OpenCV
# ------------------------------
cap = cv2.VideoCapture(ruta_entrada)

if not cap.isOpened():
    print("No se pudo abrir el video de entrada. Verifica el nombre y la ruta.")
    exit()

# ------------------------------
# 3. Obtener propiedades del video
# ------------------------------
fps = int(cap.get(cv2.CAP_PROP_FPS))                     # Cuadros por segundo
ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))           # Ancho en píxeles
alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))           # Alto en píxeles
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))    # Número total de fotogramas

if fps > 0 and total_frames > 0:
    duracion = total_frames / fps
    print(f"Duración del video: {duracion/60:.2f} minutos")
print(f"Resolución: {ancho}x{alto} a {fps} fps")
print(f"Total de fotogramas a procesar: {total_frames}\n")

# ------------------------------02.......
# 4. Crear objeto para escribir el nuevo video (MP4)
# ------------------------------
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(ruta_salida, fourcc, fps, (ancho, alto), isColor=True)

# ------------------------------
# 5. Medir tiempo total de la tarea
# ------------------------------
inicio = time.time()
frame_actual = 0

# ------------------------------
# 6. Procesar fotogramas uno por uno
# ------------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_actual += 1

    # Convertir fotograma a formato Pillow
    pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Convertir a blanco y negro con Pillow
    pil_bn = pil_img.convert("L")

    # Volver a NumPy y a 3 canales para OpenCV
    frame_bn = cv2.cvtColor(np.array(pil_bn), cv2.COLOR_GRAY2BGR)

    # Guardar el fotograma en el nuevo video
    out.write(frame_bn)

    # Impresión de progreso en vivo
    if total_frames > 0:
        porcentaje = (frame_actual / total_frames) * 100
        # Imprime en la misma línea usando '\r' para no saturar la consola
        sys.stdout.write(f"\rProcesando: {frame_actual}/{total_frames} frames ({porcentaje:.1f}%)")
        sys.stdout.flush()

# Salto de línea al terminar el bucle
print("\n")

# ------------------------------
# 7. Liberar recursos
# ------------------------------
cap.release()
out.release()

# ------------------------------
# 8. Calcular tiempo total
# ------------------------------
fin = time.time()
tiempo_total = fin - inicio

print(f"Tiempo total de procesamiento: {tiempo_total:.2f} segundos ({tiempo_total/60:.2f} minutos)")
print(f"Video generado con éxito en: {ruta_salida}")