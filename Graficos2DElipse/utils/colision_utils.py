import numpy as np

def ordenar_puntos_curva(puntos):
    if not puntos:
        return []
    puntos_array = np.array(puntos)
    centroide = np.mean(puntos_array, axis=0)
    angulos = np.arctan2(puntos_array[:, 1] - centroide[1], puntos_array[:, 0] - centroide[0])
    indices_ordenados = np.argsort(angulos)
    return [tuple(puntos_array[i]) for i in indices_ordenados]

def hay_colision_trayectorias(elipse_1, elipse_2, cantidad_puntos=200):
    x_1, y_1 = elipse_1.puntos(cantidad_puntos)
    if any(elipse_2.contiene_punto(x, y) for x, y in zip(x_1, y_1)):
        return True
    x_2, y_2 = elipse_2.puntos(cantidad_puntos)
    if any(elipse_1.contiene_punto(x, y) for x, y in zip(x_2, y_2)):
        return True
    return False

def ruta_cruce(elipse_1, elipse_2, cantidad_puntos=500, tolerancia=1e-5):
    puntos_cruce = []
    x_1, y_1 = elipse_1.puntos(cantidad_puntos)
    puntos_cruce += [(x, y) for x, y in zip(x_1, y_1) if elipse_2.contiene_punto(x, y)]
    x_2, y_2 = elipse_2.puntos(cantidad_puntos)
    puntos_cruce += [(x, y) for x, y in zip(x_2, y_2) if elipse_1.contiene_punto(x, y)]
    puntos_filtrados = []
    for punto_x, punto_y in puntos_cruce:
        if not any(np.hypot(punto_x - filtrado_x, punto_y - filtrado_y) < tolerancia for filtrado_x, filtrado_y in puntos_filtrados):
            puntos_filtrados.append((punto_x, punto_y))
    return ordenar_puntos_curva(puntos_filtrados)

def puntos_interseccion_aproximados(elipse_1, elipse_2, cantidad_puntos=1000, tolerancia=1e-4):
    puntos_cruce = []
    x_1, y_1 = elipse_1.puntos(cantidad_puntos)
    for i in range(cantidad_puntos - 1):
        en_otra_elipse_actual = elipse_2.contiene_punto(x_1[i], y_1[i])
        en_otra_elipse_siguiente = elipse_2.contiene_punto(x_1[i+1], y_1[i+1])
        if en_otra_elipse_actual != en_otra_elipse_siguiente:
            punto_medio_x = (x_1[i] + x_1[i+1]) / 2
            punto_medio_y = (y_1[i] + y_1[i+1]) / 2
            puntos_cruce.append((punto_medio_x, punto_medio_y))

    x_2, y_2 = elipse_2.puntos(cantidad_puntos)
    for i in range(cantidad_puntos - 1):
        en_otra_elipse_actual = elipse_1.contiene_punto(x_2[i], y_2[i])
        en_otra_elipse_siguiente = elipse_1.contiene_punto(x_2[i+1], y_2[i+1])
        if en_otra_elipse_actual != en_otra_elipse_siguiente:
            punto_medio_x = (x_2[i] + x_2[i+1]) / 2
            punto_medio_y = (y_2[i] + y_2[i+1]) / 2
            puntos_cruce.append((punto_medio_x, punto_medio_y))

    puntos_filtrados = []
    for punto_x, punto_y in puntos_cruce:
        if not any(np.hypot(punto_x - filtrado_x, punto_y - filtrado_y) < tolerancia for filtrado_x, filtrado_y in puntos_filtrados):
            puntos_filtrados.append((punto_x, punto_y))
    return ordenar_puntos_curva(puntos_filtrados)
