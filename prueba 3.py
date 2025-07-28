import cv2
import mediapipe as mp
import json
import os
import time

timestamp = int(time.time())

# === Configuración de rutas ===
RUTA_IMAGEN = "C:\\Users\\maloj\\OneDrive\\Documents\\Pruebas\\OIP.jpg"
RUTA_SALIDA = f"C:\\Users\\maloj\\OneDrive\\Documents\\Pruebas\\pose_capturas\\pose_landmarks_{timestamp}_IMG.json"

# === Inicializar MediaPipe Pose ===
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=True)

# === Cargar imagen ===
imagen = cv2.imread(RUTA_IMAGEN)
if imagen is None:
    print("❌ No se pudo cargar la imagen.")
    exit()

# Convertir a RGB
imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
resultados = pose.process(imagen_rgb)

if not resultados.pose_landmarks:
    print("❌ No se detectaron puntos de pose.")
    exit()

# Dibujar landmarks sobre la imagen
mp_drawing.draw_landmarks(imagen, resultados.pose_landmarks, mp_pose.POSE_CONNECTIONS)

# === Extraer landmarks a diccionario ===
landmarks_dict = {}
for idx, lm in enumerate(resultados.pose_landmarks.landmark):
    nombre = mp_pose.PoseLandmark(idx).name  # Ej: "LEFT_ELBOW"
    landmarks_dict[nombre] = {
        "x": lm.x,
        "y": lm.y,
        "z": lm.z,
        "visibility": lm.visibility
    }

# === Guardar en JSON ===
with open(RUTA_SALIDA, "w") as f:
    json.dump(landmarks_dict, f, indent=4)
print(f"✅ Landmarks guardados en: {RUTA_SALIDA}")

# Mostrar imagen con puntos
cv2.imshow("Pose detectada", imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()
