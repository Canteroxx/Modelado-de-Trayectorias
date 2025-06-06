import pyqtgraph as pg

def graficar_elipses_pg(trayectorias, plot, colores=None, with_labels=True, linewidth=2):
    if colores is None:
        colores = ["blue", "green", "orange", "purple", "cyan", "brown", "magenta", "gold", "pink"]
    for i, tr in enumerate(trayectorias, 1):
        x, y = tr.puntos()  # Usa el método de la clase
        color = colores[(i - 1) % len(colores)]
        name = f"RUT: {tr.rut}" if with_labels else None
        plot.plot(x, y, pen=pg.mkPen(color, width=linewidth), name=name)
    plot.setAspectLocked(True)

def graficar_centros_pg(trayectorias, plot, colores=None):
    if colores is None:
        colores = ["magenta", "orange", "cyan", "lime", "brown", "purple", "gold", "pink"]
    spots = []
    for i, tr in enumerate(trayectorias, 1):
        color_centro = colores[(i - 1) % len(colores)]
        spots.append({
            'pos': (tr.h, tr.k),
            'data': i-1,
            'brush': pg.mkBrush(color_centro),
            'symbol': 'o',
            'size': 18,
            'pen': pg.mkPen('k', width=2)
        })
    scatter = pg.ScatterPlotItem()
    scatter.addPoints(spots)
    plot.addItem(scatter)
    return scatter

def graficar_rutas_puntos_colision_pg(resultados, trayectorias, plot):
    ya_mostrado = set()
    for res in resultados:
        e1, e2 = res["elipse1"], res["elipse2"]
        ruta = res["ruta_cruce"]
        puntos_cruce = res["puntos_cruce"]
        print("Puntos de cruce:", puntos_cruce)
        if ruta:
            x_col, y_col = zip(*ruta)
            label_ruta = f"Ruta de cruce {trayectorias.index(e1)+1}-{trayectorias.index(e2)+1}"
            if label_ruta not in ya_mostrado:
                plot.plot(x_col, y_col, pen=pg.mkPen('r', width=2), name=label_ruta)
                ya_mostrado.add(label_ruta)
        if puntos_cruce:
            x_pcr, y_pcr = zip(*puntos_cruce)
            label_puntos = f"Puntos cruce {trayectorias.index(e1)+1}-{trayectorias.index(e2)+1}"
            if label_puntos not in ya_mostrado:
                scatter = pg.ScatterPlotItem(x_pcr, y_pcr, symbol='o', size=16, brush=pg.mkBrush('k'))
                plot.addItem(scatter)
                ya_mostrado.add(label_puntos)

def graficar_dos_elipses_pg(e1, e2, idx1, idx2, ruta, puntos_cruce, plot):
    colores = ["blue", "green"]
    for el, color, idx in zip([e1, e2], colores, [idx1, idx2]):
        x, y = el.puntos()
        plot.plot(x, y, pen=pg.mkPen(color, width=2), name=f"RUT: {el.rut}")
        scatter = pg.ScatterPlotItem([el.h], [el.k], symbol='o', size=18,
                                     pen=pg.mkPen('k', width=2), brush=pg.mkBrush(color))
        plot.addItem(scatter)
    if ruta:
        x_col, y_col = zip(*ruta)
        plot.plot(x_col, y_col, pen=pg.mkPen('r', width=2), name="Ruta de cruce")
    if puntos_cruce:
        x_pcr, y_pcr = zip(*puntos_cruce)
        scatter = pg.ScatterPlotItem(x_pcr, y_pcr, symbol='o', size=18, brush=pg.mkBrush('k'))
        plot.addItem(scatter)
    plot.setTitle("Colisión específica: dos elipses seleccionadas")
    plot.setAspectLocked(True)
