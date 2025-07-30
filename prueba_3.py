import cv2
import mediapipe as mp
import json
import math
import time

UMBRAL_VISIBILIDAD = 0.5

def calcular_angulo(p1, p2, p3):
    a = [p1[i] - p2[i] for i in range(3)]
    b = [p3[i] - p2[i] for i in range(3)]

    dot_product = sum(a[i] * b[i] for i in range(3))
    norm_a = math.sqrt(sum(a[i] ** 2 for i in range(3)))
    norm_b = math.sqrt(sum(b[i] ** 2 for i in range(3)))

    if norm_a == 0 or norm_b == 0:
        return None

    cos_theta = dot_product / (norm_a * norm_b)
    cos_theta = min(1.0, max(-1.0, cos_theta))
    return math.degrees(math.acos(cos_theta))

def foto():
    timestamp = int(time.time())
    RUTA_IMAGEN = "C:\\Users\\maloj\\OneDrive\\Documents\\Pruebas\\OIP.jpg"
    RUTA_SALIDA = f"C:\\Users\\maloj\\OneDrive\\Documents\\Pruebas\\Ejemplos\\pose_landmarks_{timestamp}_IMG.json"

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
        "MOUTH_LEFT": "Comisura_Izquierda",
        "MOUTH_RIGHT": "Comisura_Derecha",
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
        "LEFT_FOOT_INDEX": "Dedos_Pie_Izquierdo",
        "RIGHT_FOOT_INDEX": "Dedos_Pie_Derecho"
    }


    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose = mp_pose.Pose(static_image_mode=True)

    imagen = cv2.imread(RUTA_IMAGEN)
    if imagen is None:
        print("❌ No se pudo cargar la imagen.")
        exit()

    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    resultados = pose.process(imagen_rgb)

    if not resultados.pose_landmarks:
        print("❌ No se detectaron puntos de pose.")
        exit()

    mp_drawing.draw_landmarks(imagen, resultados.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Diccionarios para guardar puntos y ángulos
    landmarks_dict = {}
    puntos = {}
    angulos_dict = {}

    # Procesar cada landmark
    for idx, lm in enumerate(resultados.pose_landmarks.landmark):
        nombre_ing = mp_pose.PoseLandmark(idx).name
        nombre_esp = nombres_es.get(nombre_ing, nombre_ing)
        puntos[nombre_esp] = (lm.x, lm.y, lm.z, lm.visibility)
        landmarks_dict[nombre_esp] = {
            "x": lm.x,
            "y": lm.y,
            "z": lm.z,
            "visibilidad": lm.visibility
        }

    # Función para calcular y guardar el ángulo si los puntos son visibles
    def agrega_angulo(nombre, a, b, c):
        if all(p in puntos for p in [a, b, c]):
            vis_minima = 0.8  # Umbral mínimo de visibilidad
            visibilidades = [
                landmarks_dict[a]['visibilidad'],
                landmarks_dict[b]['visibilidad'],
                landmarks_dict[c]['visibilidad']
            ]
            if all(v >= vis_minima for v in visibilidades):
                angulo = calcular_angulo(puntos[a], puntos[b], puntos[c])
                if angulo is not None:
                    angulos_dict[nombre] = round(angulo, 2)

    agrega_angulo("Codo_Izquierdo", "Hombro_Izquierdo", "Codo_Izquierdo", "Muñeca_Izquierda")
    agrega_angulo("Codo_Derecho", "Hombro_Derecho", "Codo_Derecho", "Muñeca_Derecha")
    agrega_angulo("Rodilla_Izquierda", "Cadera_Izquierda", "Rodilla_Izquierda", "Tobillo_Izquierdo")
    agrega_angulo("Rodilla_Derecha", "Cadera_Derecha", "Rodilla_Derecha", "Tobillo_Derecho")
    agrega_angulo("Hombro_Izquierdo", "Codo_Izquierdo", "Hombro_Izquierdo", "Cadera_Izquierda")
    agrega_angulo("Hombro_Derecho", "Codo_Derecho", "Hombro_Derecho", "Cadera_Derecha")

    # Guardar JSON con landmarks y ángulos
    datos_salida = {
        "landmarks": landmarks_dict,
        "angulos": angulos_dict
    }

    with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
        json.dump(datos_salida, f, indent=4, ensure_ascii=False)
    print(f"✅ Landmarks y ángulos guardados en: {RUTA_SALIDA}")

    cv2.imshow("Pose detectada", imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()