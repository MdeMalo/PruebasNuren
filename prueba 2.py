import cv2
import mediapipe as mp
import json
import time
import os

# Configuración inicial
OUTPUT_DIR = "C:\\Users\\maloj\\OneDrive\\Documents\\Pruebas\\pose_capturas"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Traducciones de los nombres de los landmarks
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

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("❌ No se pudo acceder al frame de la cámara.")
            continue

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

        # Mostrar imagen
        cv2.imshow("Presiona 's' para guardar landmarks | 'ESC' para salir", image)

        key = cv2.waitKey(5) & 0xFF
        if key == 27:  # ESC
            break
        elif key == ord('s') and results.pose_landmarks:
            timestamp = int(time.time())
            output_json = os.path.join(OUTPUT_DIR, f"landmarks_{timestamp}_CAMARA.json")

            landmarks_dict = {}
            for idx, lm in enumerate(results.pose_landmarks.landmark):
                nombre_en = mp_pose.PoseLandmark(idx).name
                nombre_es = nombres_es.get(nombre_en, f"Punto_{idx}")

                landmarks_dict[nombre_es] = {
                    'x': lm.x,
                    'y': lm.y,
                    'z': lm.z,
                    'visibilidad': lm.visibility
                }

            with open(output_json, 'w', encoding='utf-8') as f:
                json.dump(landmarks_dict, f, indent=4, ensure_ascii=False)

            print(f"✅ Landmarks guardados: {output_json}")

cap.release()
cv2.destroyAllWindows()
