from utils.colision_utils import (
    hay_colision_trayectorias,
    ruta_cruce,
    puntos_interseccion_aproximados,
)

class ColisionadorTrayectorias:
    @staticmethod
    def hay_colision_trayectorias(elipse1, elipse2, n=200):
        return hay_colision_trayectorias(elipse1, elipse2, n)
    
    @staticmethod
    def ruta_cruce(e1, e2, n=500, tol=1e-5):
        return ruta_cruce(e1, e2, n, tol)
    
    @staticmethod
    def puntos_interseccion_aproximados(e1, e2, n=500):
        return puntos_interseccion_aproximados(e1, e2, n)

    @staticmethod
    def buscar_colisiones_trayectorias(lista_elipses, n=200):
        colisiones = []
        for i in range(len(lista_elipses)):
            for j in range(i + 1, len(lista_elipses)):
                if hay_colision_trayectorias(lista_elipses[i], lista_elipses[j], n):
                    colisiones.append((lista_elipses[i], lista_elipses[j]))
        return colisiones

    @staticmethod
    def buscar_colisiones_global(trayectorias, detectar_ruta=False, detectar_puntos=False):
        resultados = []
        n = len(trayectorias)
        for i in range(n):
            for j in range(i+1, n):
                e1, e2 = trayectorias[i], trayectorias[j]
                conflicto = False
                ruta, puntos_cruce = None, None

                if detectar_ruta:
                    ruta = ruta_cruce(e1, e2)
                    if ruta:
                        conflicto = True

                if detectar_puntos:
                    puntos_cruce = puntos_interseccion_aproximados(e1, e2)
                    if puntos_cruce:
                        conflicto = True

                if not detectar_ruta and not detectar_puntos:
                    ruta = ruta_cruce(e1, e2)
                    if ruta:
                        conflicto = True

                if conflicto:
                    resultados.append({
                        "elipse1": e1,
                        "elipse2": e2,
                        "ruta_cruce": ruta,
                        "puntos_cruce": puntos_cruce,
                    })
        return resultados
