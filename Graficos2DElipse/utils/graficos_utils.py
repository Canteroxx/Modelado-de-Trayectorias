import numpy as np
import matplotlib.pyplot as plt

def graficar_elipses(trayectorias, ax, colores=None, with_labels=True, linewidth=2):
    if colores is None:
        colores = ["blue", "green", "orange", "purple", "cyan", "brown", "magenta", "gold", "pink"]
    for i, tr in enumerate(trayectorias, 1):
        color = colores[(i - 1) % len(colores)]
        x, y = tr.puntos()
        label = f"RUT: {tr.rut}" if with_labels else None
        ax.plot(x, y, color=color, linewidth=linewidth, label=label)
    if with_labels:
        ax.legend()
    ax.set_aspect('equal')

def graficar_centros(trayectorias, ax, colores=None):
    if colores is None:
        colores = ["magenta", "orange", "cyan", "lime", "brown", "purple", "gold", "pink"]
    for i, tr in enumerate(trayectorias, 1):
        color_centro = colores[(i - 1) % len(colores)]
        ax.scatter([tr.h], [tr.k], s=80, marker="o", edgecolor=color_centro, facecolors='none',
                   linewidths=2, zorder=7, label=f"Centro O{i}")

def graficar_rutas_puntos_colision(resultados, trayectorias, ax):
    ya_mostrado = set()
    for res in resultados:
        e1, e2 = res["elipse1"], res["elipse2"]
        ruta = res["ruta_cruce"]
        puntos_cruce = res["puntos_cruce"]
        if ruta:
            x_col, y_col = zip(*ruta)
            centro = np.mean(np.column_stack((x_col, y_col)), axis=0)
            angulos = np.arctan2(np.array(y_col) - centro[1], np.array(x_col) - centro[0])
            orden = np.argsort(angulos)
            label_ruta = f"Ruta de cruce {trayectorias.index(e1)+1}-{trayectorias.index(e2)+1}"
            if label_ruta not in ya_mostrado:
                ax.plot(np.array(x_col)[orden], np.array(y_col)[orden],
                        color="red", linewidth=2, alpha=0.7, label=label_ruta)
                ya_mostrado.add(label_ruta)
        if puntos_cruce:
            x_pcr, y_pcr = zip(*puntos_cruce)
            label_puntos = f"Puntos cruce {trayectorias.index(e1)+1}-{trayectorias.index(e2)+1}"
            if label_puntos not in ya_mostrado:
                ax.scatter(x_pcr, y_pcr, color="black", s=50, zorder=6, label=label_puntos)
                ya_mostrado.add(label_puntos)

def graficar_dos_elipses(e1, e2, idx1, idx2, ruta, puntos_cruce, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    colores = ["blue", "green"]
    for i, (el, color) in enumerate(zip([e1, e2], colores)):
        x, y = el.puntos()
        ax.plot(x, y, color=color, linewidth=2, label=f"RUT: {el.rut}")
    centros_colores = ["magenta", "orange"]
    nombres = [f"Centro O{idx1+1}", f"Centro O{idx2+1}"]
    for i, (el, color, nombre) in enumerate(zip([e1, e2], centros_colores, nombres)):
        ax.scatter([el.h], [el.k], s=80, marker="o", edgecolor=color, facecolors='none', linewidths=2, zorder=7, label=nombre)
    if ruta:
        x_col, y_col = zip(*ruta)
        centro = np.mean(np.column_stack((x_col, y_col)), axis=0)
        angulos = np.arctan2(np.array(y_col) - centro[1], np.array(x_col) - centro[0])
        orden = np.argsort(angulos)
        ax.plot(np.array(x_col)[orden], np.array(y_col)[orden], color="red", linewidth=2, label="Ruta de cruce")
    if puntos_cruce:
        x_pcr, y_pcr = zip(*puntos_cruce)
        ax.scatter(x_pcr, y_pcr, color="black", s=50, zorder=6, label="Puntos de cruce")
    ax.set_title("Colisión específica: dos elipses seleccionadas")
    ax.set_aspect('equal')
    ax.legend()


def guardar_figura(fig, ruta_archivo):
    fig.savefig(ruta_archivo, bbox_inches='tight')
