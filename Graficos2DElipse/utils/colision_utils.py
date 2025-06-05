import numpy as np

def hay_colision_trayectorias(elipse1, elipse2, n=200):
    x1, y1 = elipse1.puntos(n)
    for xi, yi in zip(x1, y1):
        if elipse2.contiene_punto(xi, yi):
            return True
    x2, y2 = elipse2.puntos(n)
    for xi, yi in zip(x2, y2):
        if elipse1.contiene_punto(xi, yi):
            return True
    return False

def ruta_cruce(e1, e2, n=500, tol=1e-5):
    puntos = []
    x1, y1 = e1.puntos(n)
    for xi, yi in zip(x1, y1):
        if e2.contiene_punto(xi, yi):
            puntos.append((xi, yi))
    x2, y2 = e2.puntos(n)
    for xi, yi in zip(x2, y2):
        if e1.contiene_punto(xi, yi):
            puntos.append((xi, yi))
    filtrados = []
    for px, py in puntos:
        if not any(np.hypot(px - fx, py - fy) < tol for fx, fy in filtrados):
            filtrados.append((px, py))
    return filtrados

def puntos_interseccion_aproximados(e1, e2, n=500):
    x1, y1 = e1.puntos(n)
    dentro_anterior = e2.contiene_punto(x1[0], y1[0])
    puntos_cruce = []
    for i in range(1, n):
        dentro_actual = e2.contiene_punto(x1[i], y1[i])
        if dentro_actual != dentro_anterior:
            puntos_cruce.append((x1[i], y1[i]))
        dentro_anterior = dentro_actual

    x2, y2 = e2.puntos(n)
    dentro_anterior = e1.contiene_punto(x2[0], y2[0])
    for i in range(1, n):
        dentro_actual = e1.contiene_punto(x2[i], y2[i])
        if dentro_actual != dentro_anterior:
            puntos_cruce.append((x2[i], y2[i]))
        dentro_anterior = dentro_actual

    filtrados = []
    for px, py in puntos_cruce:
        if not any(np.hypot(px - fx, py - fy) < 1e-3 for fx, fy in filtrados):
            filtrados.append((px, py))
    return filtrados
