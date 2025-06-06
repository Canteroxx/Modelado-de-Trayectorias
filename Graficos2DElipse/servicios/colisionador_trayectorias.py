from utils.colision_utils import (
    hay_colision_trayectorias,
    ruta_cruce,
    puntos_interseccion_aproximados,
)

class ColisionadorTrayectorias:
    @staticmethod
    def existe_colision_entre_elipses(elipse_1, elipse_2, cantidad_puntos=200):
        return hay_colision_trayectorias(elipse_1, elipse_2, cantidad_puntos)
    
    @staticmethod
    def calcular_ruta_cruce(elipse_1, elipse_2, cantidad_puntos=500, tolerancia=1e-5):
        return ruta_cruce(elipse_1, elipse_2, cantidad_puntos, tolerancia)
    
    @staticmethod
    def calcular_puntos_interseccion_aproximados(elipse_1, elipse_2, cantidad_puntos=500):
        return puntos_interseccion_aproximados(elipse_1, elipse_2, cantidad_puntos)

    @staticmethod
    def buscar_pares_con_colision(lista_elipses, cantidad_puntos=200):
        lista_colisiones = []
        for indice_1 in range(len(lista_elipses)):
            for indice_2 in range(indice_1 + 1, len(lista_elipses)):
                elipse_1 = lista_elipses[indice_1]
                elipse_2 = lista_elipses[indice_2]
                if hay_colision_trayectorias(elipse_1, elipse_2, cantidad_puntos):
                    lista_colisiones.append((elipse_1, elipse_2))
        return lista_colisiones

    @staticmethod
    def buscar_colisiones_detalladas(lista_trayectorias, incluir_ruta_cruce=False, incluir_puntos_cruce=False):
        lista_resultados = []
        cantidad_trayectorias = len(lista_trayectorias)
        for indice_1 in range(cantidad_trayectorias):
            for indice_2 in range(indice_1 + 1, cantidad_trayectorias):
                elipse_1 = lista_trayectorias[indice_1]
                elipse_2 = lista_trayectorias[indice_2]
                hay_conflicto = False
                ruta_de_cruce = None
                lista_puntos_cruce = None

                if incluir_ruta_cruce:
                    ruta_de_cruce = ruta_cruce(elipse_1, elipse_2)
                    if ruta_de_cruce:
                        hay_conflicto = True

                if incluir_puntos_cruce:
                    lista_puntos_cruce = puntos_interseccion_aproximados(elipse_1, elipse_2)
                    if lista_puntos_cruce:
                        hay_conflicto = True

                if not incluir_ruta_cruce and not incluir_puntos_cruce:
                    ruta_de_cruce = ruta_cruce(elipse_1, elipse_2)
                    if ruta_de_cruce:
                        hay_conflicto = True

                if hay_conflicto:
                    lista_resultados.append({
                        "elipse1": elipse_1,
                        "elipse2": elipse_2,
                        "ruta_cruce": ruta_de_cruce,
                        "puntos_cruce": lista_puntos_cruce,
                    })
        return lista_resultados
