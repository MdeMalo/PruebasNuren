import math
from typing import Dict, Tuple, Any, List

class RehabTechAngleComparator:
    def __init__(self, umbral_angulo: float = 15.0, porcentaje_max_errores: float = 0.3):
        """
        umbral_angulo: máximo ángulo en grados aceptable para considerar la pose correcta
        porcentaje_max_errores: porcentaje máximo de ángulos que pueden estar fuera del umbral para considerar la pose correcta
        """
        self.umbral = umbral_angulo
        self.porcentaje_max_errores = porcentaje_max_errores
        self.historial_errores: List[Dict[str, float]] = []

    @staticmethod
    def _calcular_angulo(p1: Dict[str, float], p2: Dict[str, float], p3: Dict[str, float]) -> float:
        """
        Calcula el ángulo en grados entre los vectores p1p2 y p3p2 en 3D.
        """
        def vector(a, b):
            return [b[axis] - a[axis] for axis in ('x', 'y', 'z')]

        v1 = vector(p2, p1)
        v2 = vector(p2, p3)

        dot = sum(a*b for a, b in zip(v1, v2))
        mag1 = math.sqrt(sum(a*a for a in v1))
        mag2 = math.sqrt(sum(b*b for b in v2))
        if mag1 * mag2 == 0:
            return 0.0

        cos_ang = dot / (mag1 * mag2)
        # Corrección por límite de precisión
        cos_ang = max(min(cos_ang, 1.0), -1.0)
        ang_rad = math.acos(cos_ang)
        ang_deg = math.degrees(ang_rad)
        return ang_deg

    def evaluar_angulos(self, json_ref: Dict[str, Any], json_actual: Dict[str, Any]) -> Dict[str, Tuple[float, float, float]]:
        """
        Compara ángulos definidos por tripletas de puntos entre pose de referencia y pose actual.

        Retorna un dict con:
          { "nombre_angulo": (angulo_ref, angulo_actual, diferencia) }
        """
        landmarks_ref = json_ref.get("landmarks", {})
        landmarks_act = json_actual.get("landmarks", {})

        # Define aquí los ángulos a comparar (puntos en tripletas)
        angulos = {
            "Codo_Izquierdo": ("Hombro_Izquierdo", "Codo_Izquierdo", "Muñeca_Izquierda"),
            "Codo_Derecho": ("Hombro_Derecho", "Codo_Derecho", "Muñeca_Derecha"),
            "Rodilla_Izquierda": ("Cadera_Izquierda", "Rodilla_Izquierda", "Tobillo_Izquierdo"),
            "Rodilla_Derecha": ("Cadera_Derecha", "Rodilla_Derecha", "Tobillo_Derecho"),
            # Agrega más ángulos según tu modelo
        }

        resultados = {}

        for nombre, (p1, p2, p3) in angulos.items():
            if p1 in landmarks_ref and p2 in landmarks_ref and p3 in landmarks_ref \
               and p1 in landmarks_act and p2 in landmarks_act and p3 in landmarks_act:
                ang_ref = self._calcular_angulo(landmarks_ref[p1], landmarks_ref[p2], landmarks_ref[p3])
                ang_act = self._calcular_angulo(landmarks_act[p1], landmarks_act[p2], landmarks_act[p3])
                diff = abs(ang_ref - ang_act)
                resultados[nombre] = (ang_ref, ang_act, diff)
            else:
                resultados[nombre] = (0.0, 0.0, 0.0)  # En caso de datos faltantes

        # Guardar diferencias para reportes acumulados
        self.historial_errores.append({k: v[2] for k, v in resultados.items()})

        return resultados

    def detectar_errores(self, resultados: Dict[str, Tuple[float, float, float]]) -> Dict[str, float]:
        """
        Detecta qué ángulos superan el umbral y retorna esos errores (nombre, diferencia)
        """
        errores = {nombre: dif for nombre, (_, _, dif) in resultados.items() if dif > self.umbral}
        return errores

    def generar_reporte_angular(self) -> Dict[str, float]:
        """
        Promedio acumulado de las diferencias angulares para cada ángulo
        """
        acumulado = {}
        conteo = {}

        for dict_errores in self.historial_errores:
            for angulo, dif in dict_errores.items():
                acumulado[angulo] = acumulado.get(angulo, 0.0) + dif
                conteo[angulo] = conteo.get(angulo, 0) + 1

        promedio = {angulo: acumulado[angulo] / conteo[angulo] for angulo in acumulado}
        return promedio

    def es_pose_correcta(self, resultados: Dict[str, Tuple[float, float, float]]) -> bool:
        """
        Determina si la pose es correcta según el porcentaje de ángulos que superan el umbral.
        Retorna True si está dentro del umbral, False si no.
        """
        total_angulos = len(resultados)
        errores = self.detectar_errores(resultados)
        cantidad_errores = len(errores)

        if total_angulos == 0:
            # Si no hay ángulos para comparar, considera pose incorrecta
            return False

        porcentaje_errores = cantidad_errores / total_angulos
        return porcentaje_errores <= self.porcentaje_max_errores