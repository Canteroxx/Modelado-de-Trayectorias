import numpy as np

def _ordenar_puntos_curva(puntos):
    if not puntos:
        return []
    puntos = np.array(puntos)
    centro = np.mean(puntos, axis=0)
    angulos = np.arctan2(puntos[:, 1] - centro[1], puntos[:, 0] - centro[0])
    orden = np.argsort(angulos)
    return [tuple(puntos[i]) for i in orden]

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
    return _ordenar_puntos_curva(filtrados)

def puntos_interseccion_aproximados(e1, e2, n=2000, tol=1e-4):
    x1, y1 = e1.puntos(n)
    puntos_cruce = []
    for i in range(n-1):
        esta = e2.contiene_punto(x1[i], y1[i])
        prox = e2.contiene_punto(x1[i+1], y1[i+1])
        if esta != prox:
            mx = (x1[i] + x1[i+1]) / 2
            my = (y1[i] + y1[i+1]) / 2
            puntos_cruce.append((mx, my))

    x2, y2 = e2.puntos(n)
    for i in range(n-1):
        esta = e1.contiene_punto(x2[i], y2[i])
        prox = e1.contiene_punto(x2[i+1], y2[i+1])
        if esta != prox:
            mx = (x2[i] + x2[i+1]) / 2
            my = (y2[i] + y2[i+1]) / 2
            puntos_cruce.append((mx, my))

    filtrados = []
    for px, py in puntos_cruce:
        if not any(np.hypot(px - fx, py - fy) < tol for fx, fy in filtrados):
            filtrados.append((px, py))
    return _ordenar_puntos_curva(filtrados)
