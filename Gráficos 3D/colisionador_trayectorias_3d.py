import numpy as np

class ColisionadorElipticas3D:
    @staticmethod
    def hay_colision_xy(elipse1, elipse2, n=300, tolerancia=0.5, tolerancia_z=None):
        """
        Devuelve True si hay al menos un punto de la proyección XY de una elipse
        suficientemente cercano a un punto de la otra (colisión en 2D),
        opcionalmente sólo si sus coordenadas z son similares.
        """
        x1, y1, z1 = elipse1.puntos_3d(n)
        x2, y2, z2 = elipse2.puntos_3d(n)
        for xi, yi, zi in zip(x1, y1, z1):
            dist_xy = np.hypot(x2 - xi, y2 - yi)
            if tolerancia_z is not None:
                # Sólo compara puntos donde la diferencia en z sea pequeña
                idx = np.where(np.abs(z2 - zi) < tolerancia_z)[0]
                if np.any(dist_xy[idx] < tolerancia):
                    return True
            else:
                if np.any(dist_xy < tolerancia):
                    return True
        return False

    @staticmethod
    def puntos_interseccion_xy(elipse1, elipse2, n=400, tolerancia=0.5, tolerancia_z=None):
        """
        Devuelve una lista de puntos (x, y, z_prom) aproximados donde ambas elipses
        se intersectan en el plano XY, opcionalmente sólo si z es similar.
        """
        x1, y1, z1 = elipse1.puntos_3d(n)
        x2, y2, z2 = elipse2.puntos_3d(n)
        intersecciones = []
        for xi, yi, zi in zip(x1, y1, z1):
            dist_xy = np.hypot(x2 - xi, y2 - yi)
            if tolerancia_z is not None:
                idx_cercanos = np.where((dist_xy < tolerancia) & (np.abs(z2 - zi) < tolerancia_z))[0]
            else:
                idx_cercanos = np.where(dist_xy < tolerancia)[0]
            for idx in idx_cercanos:
                punto = (
                    (xi + x2[idx]) / 2,
                    (yi + y2[idx]) / 2,
                    (zi + z2[idx]) / 2
                )
                if not any(np.allclose(punto, p, atol=1e-2) for p in intersecciones):
                    intersecciones.append(punto)
        return intersecciones

    @staticmethod
    def puntos_interseccion_xyz(elipse1, elipse2, n=400, tolerancia=0.5):
        """
        Busca intersecciones considerando (x, y, z). Útil si las trayectorias usan z != 0.
        """
        x1, y1, z1 = elipse1.puntos_3d(n)
        x2, y2, z2 = elipse2.puntos_3d(n)
        intersecciones = []
        for xi, yi, zi in zip(x1, y1, z1):
            dist = np.sqrt((x2 - xi)**2 + (y2 - yi)**2 + (z2 - zi)**2)
            idx_cercanos = np.where(dist < tolerancia)[0]
            for idx in idx_cercanos:
                punto = (
                    (xi + x2[idx]) / 2,
                    (yi + y2[idx]) / 2,
                    (zi + z2[idx]) / 2
                )
                if not any(np.allclose(punto, p, atol=1e-2) for p in intersecciones):
                    intersecciones.append(punto)
        return intersecciones

    @staticmethod
    def buscar_colisiones_xy(lista_elipses, n=300, tolerancia=0.5, tolerancia_z=None):
        """
        Devuelve una lista de diccionarios con cada par de elipses que colisiona en XY.
        """
        resultados = []
        for i in range(len(lista_elipses)):
            for j in range(i + 1, len(lista_elipses)):
                e1, e2 = lista_elipses[i], lista_elipses[j]
                inters = ColisionadorElipticas3D.puntos_interseccion_xy(
                    e1, e2, n, tolerancia, tolerancia_z
                )
                if inters:
                    resultados.append({
                        "elipse1": e1,
                        "elipse2": e2,
                        "intersecciones_xy": inters
                    })
        return resultados

    @staticmethod
    def buscar_colisiones_xyz(lista_elipses, n=300, tolerancia=0.5):
        """
        Devuelve una lista de diccionarios con cada par de elipses que colisiona en XYZ.
        """
        resultados = []
        for i in range(len(lista_elipses)):
            for j in range(i + 1, len(lista_elipses)):
                e1, e2 = lista_elipses[i], lista_elipses[j]
                inters = ColisionadorElipticas3D.puntos_interseccion_xyz(e1, e2, n, tolerancia)
                if inters:
                    resultados.append({
                        "elipse1": e1,
                        "elipse2": e2,
                        "intersecciones_xyz": inters
                    })
        return resultados
