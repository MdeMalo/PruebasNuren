from comparador_angulo_modulo import RehabTechAngleComparator
import prueba_2
import prueba_3

def main():
    print("¿Quieres cargar la cámara (c), una foto (f), o comparar ángulos (a)?: ", end="")
    opcion = input().strip().lower()

    if opcion == "c":
        print("▶ Ejecutando cámara en tiempo real...")
        prueba_2.camara()
    elif opcion == "f":
        print("▶ Ejecutando análisis de foto...")
        prueba_3.foto()
    elif opcion == "a":
        print("▶ Ejecutando comparación de ángulos...")
        comparador = RehabTechAngleComparator()
        comparador.comparar_archivos("pose_referencia.json", "pose_actual.json")  # cambia por los que tú uses
    else:
        print("❌ Opción no válida. Usa 'c' para cámara, 'f' para foto, o 'a' para comparar ángulos.")

if __name__ == "__main__":
    main()
