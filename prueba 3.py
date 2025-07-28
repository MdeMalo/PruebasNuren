import cv2
import mediapipe as mp
import json
import os
import time

timestamp = int(time.time())

# === Configuración de rutas ===
RUTA_IMAGEN = "C:\\Users\\maloj\\OneDrive\\Documents\\Pruebas\\OIP.jpg"
RUTA_SALIDA = f"C:\\Users\\maloj\\OneDrive\\Documents\\Pruebas\\pose_capturas\\pose_landmarks_{timestamp}_IMG.json"

# === Diccionario de nombres en español ===
nombres_es = {
    "NOSE": "Nariz",
    "LEFT_EYE_INNER": "Ojo_Izquierdo_Interno",
    "LEFT_EYE": "Ojo_Izquierdo",
    "LEFT_EYE_OUTER": "Ojo_Izquierdo_Externo",
    "RIGHT_EYE_INNER": "Ojo_Derecho_Interno",
    "RIGHT_EYE": "Ojo_Derecho",
    "RIGHT_EYE_OUTER": "Ojo_Derecho_Externo",
    "LEFT_EAR": "Oreja_Izquierda",
    "RIGHT_EAR": "Oreja_Derecha",
    "MOUTH_LEFT": "Boca_Izquierda",
    "MOUTH_RIGHT": "Boca_Derecha",
    "LEFT_SHOULDER": "Hombro_Izquierdo",
    "RIGHT_SHOULDER": "Hombro_Derecho",
    "LEFT_ELBOW": "Codo_Izquierdo",
    "RIGHT_ELBOW": "Codo_Derecho",
    "LEFT_WRIST": "Muñeca_Izquierda",
    "RIGHT_WRIST": "Muñeca_Derecha",
    "LEFT_PINKY": "Meñique_Izquierdo",
    "RIGHT_PINKY": "Meñique_Derecho",
    "LEFT_INDEX": "Índice_Izquierdo",
    "RIGHT_INDEX": "Índice_Derecho",
    "LEFT_THUMB": "Pulgar_Izquierdo",
    "RIGHT_THUMB": "Pulgar_Derecho",
    "LEFT_HIP": "Cadera_Izquierda",
    "RIGHT_HIP": "Cadera_Derecha",
    "LEFT_KNEE": "Rodilla_Izquierda",
    "RIGHT_KNEE": "Rodilla_Derecha",
    "LEFT_ANKLE": "Tobillo_Izquierdo",
    "RIGHT_ANKLE": "Tobillo_Derecho",
    "LEFT_HEEL": "Talón_Izquierdo",
    "RIGHT_HEEL": "Talón_Derecho",
    "LEFT_FOOT_INDEX": "Punta_Pie_Izquierdo",
    "RIGHT_FOOT_INDEX": "Punta_Pie_Derecho"
}

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

# === Extraer landmarks a diccionario con nombres en español ===
landmarks_dict = {}
for idx, lm in enumerate(resultados.pose_landmarks.landmark):
    nombre_ing = mp_pose.PoseLandmark(idx).name
    nombre_esp = nombres_es.get(nombre_ing, nombre_ing)  # Si no está traducido, deja el nombre en inglés
    landmarks_dict[nombre_esp] = {
        "x": lm.x,
        "y": lm.y,
        "z": lm.z,
        "visibilidad": lm.visibility
    }

# === Guardar en JSON ===
with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
    json.dump(landmarks_dict, f, indent=4, ensure_ascii=False)
print(f"✅ Landmarks guardados en: {RUTA_SALIDA}")

# Mostrar imagen con puntos
cv2.imshow("Pose detectada", imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()
