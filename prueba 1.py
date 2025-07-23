import cv2
import mediapipe as mp

# Inicializar MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Umbral de visibilidad para aceptar puntos
VIS_THRESHOLD = 0.7

# Puntos que nos interesan
PUNTOS_CLAVE = {
    "LEFT_SHOULDER": mp_pose.PoseLandmark.LEFT_SHOULDER,
    "LEFT_ELBOW": mp_pose.PoseLandmark.LEFT_ELBOW,
    "LEFT_WRIST": mp_pose.PoseLandmark.LEFT_WRIST,
    "RIGHT_SHOULDER": mp_pose.PoseLandmark.RIGHT_SHOULDER,
    "RIGHT_ELBOW": mp_pose.PoseLandmark.RIGHT_ELBOW,
    "RIGHT_WRIST": mp_pose.PoseLandmark.RIGHT_WRIST,
}

# Función para obtener solo los puntos de interés
def extraer_landmarks_brazos(landmarks, width, height):
    puntos = {"LEFT": {}, "RIGHT": {}}
    for nombre, idx in PUNTOS_CLAVE.items():
        lm = landmarks[idx]
        if lm.visibility >= VIS_THRESHOLD:
            coord = (int(lm.x * width), int(lm.y * height))
            lado = "LEFT" if "LEFT" in nombre else "RIGHT"
            clave = nombre.split("_")[1]  # SHOULDER, ELBOW, WRIST
            puntos[lado][clave] = coord
    return puntos

# Inicializar cámara
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("❌ No se pudo acceder a la cámara.")
        break

    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        puntos_brazos = extraer_landmarks_brazos(results.pose_landmarks.landmark, w, h)

        # Dibujar solo los puntos de los brazos
        for lado in puntos_brazos:
            for nombre, punto in puntos_brazos[lado].items():
                cv2.circle(frame, punto, 6, (0, 255, 0), -1)
                cv2.putText(frame, f"{lado}_{nombre}", (punto[0] + 5, punto[1] - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Si quieres ver los valores en consola:
        print("🔍 Puntos de brazos:", puntos_brazos)

    # Mostrar el frame
    cv2.imshow("Pose Tracking - Brazos", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC para salir
        break

cap.release()
cv2.destroyAllWindows()
