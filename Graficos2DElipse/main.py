from modelos.trayectoria_eliptica import TrayectoriaEliptica
from servicios.colisionador_trayectorias import ColisionadorTrayectorias
from utils.graficos_utils_mat import graficar_elipses, graficar_centros, graficar_rutas_puntos_colision, graficar_dos_elipses
import matplotlib.pyplot as plt

def mostrar_menu():
    print("\n=== SIMULADOR DE TRAYECTORIAS ELÍPTICAS ===")
    print("1. Agregar trayectoria por RUT")
    print("2. Listar trayectorias agregadas")
    print("3. Graficar trayectorias (2D)")
    print("4. Buscar colisiones")
    print("5. Limpiar todas las trayectorias")
    print("6. Buscar colisiones específicas (dos elipses)")
    print("0. Salir")

def testear_funcionalidad():
    trayectorias = []
    colores = ["magenta", "orange", "cyan", "lime", "brown", "purple", "gold", "pink"]

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            rut = input("Ingrese el RUT (sin puntos, con guion): ").strip()
            try:
                tr = TrayectoriaEliptica.desde_rut(rut)
                trayectorias.append(tr)
                print(f"Trayectoria creada: {tr}")
            except Exception as e:
                print("Error:", e)

        elif opcion == "2":
            if not trayectorias:
                print("No hay trayectorias agregadas.")
            else:
                for i, tr in enumerate(trayectorias, 1):
                    print(f"{i}. RUT: {tr.rut} | Centro: ({tr.h}, {tr.k}) | a: {tr.a} | b: {tr.b} | theta: {tr.theta:.2f}")

        elif opcion == "3":
            if not trayectorias:
                print("No hay trayectorias para graficar.")
            else:
                fig, ax = plt.subplots()
                graficar_elipses(trayectorias, ax)
                graficar_centros(trayectorias, ax, colores)
                resultados = ColisionadorTrayectorias.buscar_colisiones_global(
                    trayectorias, detectar_ruta=True, detectar_puntos=True
                )
                graficar_rutas_puntos_colision(resultados, trayectorias, ax)
                ax.legend()
                ax.set_title("Trayectorias, centros (O1...), rutas de cruce (rojo), puntos de cruce (negro)")
                plt.show()

        elif opcion == "4":
            if len(trayectorias) < 2:
                print("Agrega al menos dos trayectorias para buscar colisiones.")
            else:
                colisiones = ColisionadorTrayectorias.buscar_colisiones_trayectorias(trayectorias)
                if not colisiones:
                    print("No hay colisiones detectadas. Todas las trayectorias son seguras.")
                else:
                    print("¡Riesgo de colisión entre las siguientes trayectorias!")
                    for e1, e2 in colisiones:
                        print(f" - RUT {e1.rut} y RUT {e2.rut}")

        elif opcion == "5":
            trayectorias = []
            print("Todas las trayectorias han sido eliminadas.")

        elif opcion == "6":
            if len(trayectorias) < 2:
                print("Debes agregar al menos dos trayectorias.")
            else:
                for i, tr in enumerate(trayectorias, 1):
                    print(f"{i}. RUT: {tr.rut}")
                try:
                    idx1 = int(input("Elija el número de la primera elipse: ")) - 1
                    idx2 = int(input("Elija el número de la segunda elipse: ")) - 1
                    e1, e2 = trayectorias[idx1], trayectorias[idx2]
                except Exception:
                    print("Selección inválida.")
                    continue

                ruta = ColisionadorTrayectorias.ruta_cruce(e1, e2)
                puntos_cruce = ColisionadorTrayectorias.puntos_interseccion_aproximados(e1, e2)

                if ruta:
                    print(f"Ruta de cruce detectada. Total de puntos muestreados: {len(ruta)}")
                    if puntos_cruce:
                        print(f"Puntos aproximados de cruce/intersección encontrados: {len(puntos_cruce)}")
                        for p in puntos_cruce:
                            print(f"x={p[0]:.3f}, y={p[1]:.3f}")
                    else:
                        print("No se detectaron puntos exactos de cruce (solo zona de solapamiento).")

                    graficar_dos_elipses(e1, e2, idx1, idx2, ruta, puntos_cruce)
                else:
                    print("No hay ruta de cruce ni puntos de intersección entre las elipses seleccionadas.")

        elif opcion == "0":
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    testear_funcionalidad()
