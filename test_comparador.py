from comparador_angulo_modulo import RehabTechAngleComparator
import json

# Carga tus archivos JSON de referencia y actual
with open("C:/Users/maloj/OneDrive/Documents/Pruebas/Ejemplos/pose_landmarks_1753750511_IMG.json", "r", encoding="utf-8") as f1, open("C:/Users/maloj/OneDrive/Documents/Pruebas/pose_capturas/landmarks_1753835756_CAMARA.json", "r", encoding="utf-8") as f2:
    json_ref = json.load(f1)
    json_actual = json.load(f2)

# Inicializa el comparador con un umbral de ángulo de 15 grados
comparador = RehabTechAngleComparator(umbral_angulo=15.0)

# Evalúa los ángulos
resultados = comparador.evaluar_angulos(json_ref, json_actual)

# Imprime las diferencias por ángulo
for nombre, (ref, act, dif) in resultados.items():
    print(f"{nombre}: Ref={ref:.2f}°, Act={act:.2f}°, Dif={dif:.2f}°")

# Detecta y muestra errores
errores = comparador.detectar_errores(resultados)
if errores:
    print("\n⚠️ Errores detectados:")
    for angulo, dif in errores.items():
        print(f"- {angulo}: {dif:.2f}° fuera de rango")
else:
    print("\n✅ Pose correcta dentro del umbral.")

# Genera y muestra reporte acumulado
reporte = comparador.generar_reporte_angular()
print("\n📊 Promedios de error angular acumulado:")
for angulo, prom in reporte.items():
    print(f"{angulo}: {prom:.2f}°")

comparador = RehabTechAngleComparator(umbral_angulo=35.0, porcentaje_max_errores=0.3)
resultados = comparador.evaluar_angulos(json_ref, json_actual)

if comparador.es_pose_correcta(resultados):
    print("✅ Pose correcta dentro del umbral.")
else:
    print("❌ Pose incorrecta, muchas desviaciones.")
