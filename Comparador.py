import math
import json
from typing import Dict, List
import os

class RehabTechComparator:
    def crear_archivo_notas():
        """
        Crea un archivo de notas en la carpeta actual con información sobre el uso del script.
        """
        with open("notas.txt", "w", encoding="utf-8") as f:
            f.write("Notas sobre el uso del script:\n")
            f.write("- Asegúrate de tener los archivos JSON en la ruta correcta.\n")
            f.write("- El umbral de distancia se puede ajustar en la inicialización del comparador.\n")
            f.write("- Los resultados se imprimirán en la consola y se pueden redirigir a un archivo si es necesario.\n")

    def evaluar_pose_global(self, distancias: Dict[str, float]) -> str:
        """
        Evalúa si la pose es correcta en términos generales.
        Devuelve un mensaje: 'Excelente', 'Aceptable', 'Incorrecta'
        """
        total_puntos = len(distancias)
        errores = self.detectar_errores(distancias)
        total_errores = len(errores)

        if total_puntos == 0:
            return "No se detectaron puntos válidos."

        porcentaje_error = total_errores / total_puntos
        print(f"\n  Porcentaje de error: {porcentaje_error}")

        if porcentaje_error < 0.1:
            return "Excelente pose"
        elif porcentaje_error < 0.3:
            return "Pose aceptable"
        else:
            return "Pose incorrecta"

    def __init__(self, umbral_distancia: float = 0.1):
        """
        umbral_distancia: distancia mínima para considerar una desviación como error
        """
        self.umbral = umbral_distancia
        self.historial_distancias: List[Dict[str, float]] = []

    @staticmethod
    def distancia_puntos(p1: Dict[str, float], p2: Dict[str, float]) -> float:
        """Calcula distancia euclidiana 3D entre dos puntos"""
        return math.sqrt(
            (p2['x'] - p1['x']) ** 2 +
            (p2['y'] - p1['y']) ** 2 +
            (p2['z'] - p1['z']) ** 2
        )

    def evaluar_progreso(self, json_ref: Dict, json_actual: Dict) -> Dict[str, float]:
        """
        Compara landmarks de referencia vs actuales
        Retorna un diccionario con las distancias por punto
        """
        distancias = {}
        lm_ref = json_ref.get('landmarks', {})
        lm_actual = json_actual.get('landmarks', {})

        for punto in lm_ref:
            if punto in lm_actual:
                d = self.distancia_puntos(lm_ref[punto], lm_actual[punto])
                distancias[punto] = d

        # Guarda el resultado para análisis posterior
        self.historial_distancias.append(distancias)
        return distancias

    def detectar_errores(self, distancias: Dict[str, float]) -> Dict[str, float]:
        """
        Revisa qué distancias superan el umbral y retorna esas como errores
        """
        errores = {p: d for p, d in distancias.items() if d > self.umbral}
        return errores

    def generar_reporte(self) -> Dict[str, float]:
        """
        Calcula promedio de distancias para cada punto en el historial acumulado
        """
        acumulado = {}
        conteo = {}

        for resultado in self.historial_distancias:
            for punto, dist in resultado.items():
                acumulado[punto] = acumulado.get(punto, 0) + dist
                conteo[punto] = conteo.get(punto, 0) + 1

        promedio = {p: acumulado[p] / conteo[p] for p in acumulado}
        return promedio


# Ejemplo rápido de uso:
if __name__ == "__main__":
    RehabTechComparator.crear_archivo_notas()
    # Cargar tus JSON (puedes adaptar la ruta o usar tus variables)
    with open("C:\\Users\\maloj\\OneDrive\\Documents\\Pruebas\\Ejemplos\\pose_landmarks_1753750511_IMG.json", "r",  encoding="utf-8") as f1, open("C:\\Users\\maloj\\OneDrive\\Documents\\Pruebas\\pose_capturas\\landmarks_1753835756_CAMARA.json", "r",  encoding="utf-8") as f2:
        json1 = json.load(f1)
        json2 = json.load(f2)

    comparator = RehabTechComparator(umbral_distancia=0.1)

    # Evaluar progreso
    distancias = comparator.evaluar_progreso(json1, json2)
    print("Distancias por punto:")
    with open("notas.txt", "a", encoding="utf-8") as f:
        f.write("\nDistancias por punto:\n")
        for punto, d in distancias.items():
            linea = f"  {punto}: {d:.4f}\n"
            print(linea, end="")
            f.write(linea)

    # Detectar errores (desviaciones mayores a umbral)
    errores = comparator.detectar_errores(distancias)
    with open("notas.txt", "a", encoding="utf-8") as f:
        f.write("\nErrores detectados:\n")
        if errores:
            for punto, d in errores.items():
                linea = f"  {punto}: desviación {d:.4f}\n"
                print(linea, end="")
                f.write(linea)
        else:
            print("  No se detectaron desviaciones significativas.")
            f.write("  No se detectaron desviaciones significativas.\n")

    # Simula agregar más sesiones para reporte acumulado
    # Por ejemplo, evaluamos json2 contra json1 otra vez (solo demo)
    comparator.evaluar_progreso(json2, json1)

    # Generar reporte promedio de distancias
    reporte = comparator.generar_reporte()
    print("\nReporte promedio acumulado:")
    with open("notas.txt", "a", encoding="utf-8") as f:
        f.write("\nReporte promedio acumulado:\n")
        for punto, promedio in reporte.items():
            linea = f"  {punto}: promedio de desviación {promedio:.4f}\n"
            print(linea, end="")
            f.write(linea)

        # Evaluación general de la pose
    evaluacion = comparator.evaluar_pose_global(distancias)
    print(f"\nEvaluación global de la pose: {evaluacion}")
    with open("notas.txt", "a", encoding="utf-8") as f:
        f.write(f"\nEvaluación global de la pose: {evaluacion}\n")
