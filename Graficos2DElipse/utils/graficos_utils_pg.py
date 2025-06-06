from PyQt6.QtWidgets import QToolTip
from PyQt6 import QtGui
from PyQt6.QtCore import QPoint
import pyqtgraph as pg
import numpy as np

def graficar_elipses(lista_trayectorias, grafico, lista_colores=None, mostrar_etiquetas=True, grosor_linea=2):
    if lista_colores is None:
        lista_colores = ["blue", "green", "orange", "purple", "cyan", "brown", "magenta", "gold", "pink"]
    for indice, trayectoria in enumerate(lista_trayectorias, 1):
        coordenadas_x, coordenadas_y = trayectoria.puntos()
        color = lista_colores[(indice - 1) % len(lista_colores)]
        etiqueta = f"RUT: {trayectoria.rut}" if mostrar_etiquetas else None
        grafico.plot(coordenadas_x, coordenadas_y, pen=pg.mkPen(color, width=grosor_linea), name=etiqueta)
    grafico.setAspectLocked(True)

def graficar_centros(lista_trayectorias, grafico, lista_colores=None):
    if lista_colores is None:
        lista_colores = ["magenta", "orange", "cyan", "lime", "brown", "purple", "gold", "pink"]
    lista_puntos = []
    for indice, trayectoria in enumerate(lista_trayectorias, 1):
        color_centro = lista_colores[(indice - 1) % len(lista_colores)]
        lista_puntos.append({
            'pos': (trayectoria.h, trayectoria.k),
            'data': indice-1,
            'brush': pg.mkBrush(color_centro),
            'symbol': 'o',
            'size': 18,
            'pen': pg.mkPen('k', width=2)
        })
    objeto_scatter = pg.ScatterPlotItem()
    objeto_scatter.addPoints(lista_puntos)
    grafico.addItem(objeto_scatter)
    return objeto_scatter

def graficar_rutas_y_puntos_colision(resultados_colisiones, lista_trayectorias, grafico):
    etiquetas_mostradas = set()
    for resultado in resultados_colisiones:
        elipse_1 = resultado["elipse1"]
        elipse_2 = resultado["elipse2"]
        ruta_de_cruce = resultado["ruta_cruce"]
        puntos_de_cruce = resultado["puntos_cruce"]

        if ruta_de_cruce:
            coordenadas_x_ruta, coordenadas_y_ruta = zip(*ruta_de_cruce)
            etiqueta_ruta = f"Ruta de cruce {lista_trayectorias.index(elipse_1)+1}-{lista_trayectorias.index(elipse_2)+1}"
            if etiqueta_ruta not in etiquetas_mostradas:
                grafico.plot(coordenadas_x_ruta, coordenadas_y_ruta, pen=pg.mkPen('r', width=2), name=etiqueta_ruta)
                etiquetas_mostradas.add(etiqueta_ruta)
        if puntos_de_cruce:
            coordenadas_x_puntos, coordenadas_y_puntos = zip(*puntos_de_cruce)
            etiqueta_puntos = f"Puntos cruce {lista_trayectorias.index(elipse_1)+1}-{lista_trayectorias.index(elipse_2)+1}"
            if etiqueta_puntos not in etiquetas_mostradas:
                objeto_scatter = pg.ScatterPlotItem(coordenadas_x_puntos, coordenadas_y_puntos, symbol='o', size=16, brush=pg.mkBrush('k'))
                grafico.addItem(objeto_scatter)
                etiquetas_mostradas.add(etiqueta_puntos)

def graficar_dos_elipses(elipse_1, elipse_2, indice_1, indice_2, ruta_de_cruce, puntos_de_cruce, grafico):
    lista_colores = ["blue", "green"]
    for trayectoria, color, indice in zip([elipse_1, elipse_2], lista_colores, [indice_1, indice_2]):
        coordenadas_x, coordenadas_y = trayectoria.puntos()
        grafico.plot(coordenadas_x, coordenadas_y, pen=pg.mkPen(color, width=2), name=f"RUT: {trayectoria.rut}")
        objeto_scatter = pg.ScatterPlotItem([trayectoria.h], [trayectoria.k], symbol='o', size=18, pen=pg.mkPen('k', width=2), brush=pg.mkBrush(color))
        grafico.addItem(objeto_scatter)
    if ruta_de_cruce:
        coordenadas_x_ruta, coordenadas_y_ruta = zip(*ruta_de_cruce)
        grafico.plot(coordenadas_x_ruta, coordenadas_y_ruta, pen=pg.mkPen('r', width=2), name="Ruta de cruce")
    if puntos_de_cruce:
        coordenadas_x_puntos, coordenadas_y_puntos = zip(*puntos_de_cruce)
        objeto_scatter = pg.ScatterPlotItem(coordenadas_x_puntos, coordenadas_y_puntos, symbol='o', size=18, brush=pg.mkBrush('k'))
        grafico.addItem(objeto_scatter)
    grafico.setTitle("Colisión específica: dos elipses seleccionadas")
    grafico.setAspectLocked(True)

def agregar_puntos_interactivos(plot, puntos, nombre="Punto", color="k", tolerancia=0.05):
    if not puntos:
        return
    xs, ys = zip(*puntos)
    scatter = pg.ScatterPlotItem(xs, ys, symbol='o', size=12, brush=pg.mkBrush(color))

    def hover_event(event):
        if event.isExit():
            QToolTip.hideText()
            return

        pos = event.pos()
        x, y = pos.x(), pos.y()

        for px, py in puntos:
            distancia = np.hypot(px - x, py - y)
            if distancia <= tolerancia:
                screen_pos = event.screenPos()
                tooltip_pos = QPoint(int(screen_pos.x()), int(screen_pos.y()))
                QToolTip.showText(tooltip_pos, f"{nombre}: ({px:.2f}, {py:.2f})")
                return
        QToolTip.hideText()

    scatter.hoverEvent = hover_event
    plot.addItem(scatter)
