from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QListWidget, QLabel, QMessageBox, QComboBox,
    QDialog, QSizePolicy
)
import matplotlib.pyplot as plt
from PyQt6.QtGui import QPixmap
import io
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from modelos.trayectoria_eliptica import TrayectoriaEliptica
from servicios.colisionador_trayectorias import ColisionadorTrayectorias

from utils.trayectoria_utils import ecuacion_canonica
from utils.graficos_utils import (
    graficar_elipses,
    graficar_centros,
    graficar_rutas_puntos_colision,
    graficar_dos_elipses
)


import sys

class VentanaEcuacionCanonica(QDialog):
    def __init__(self, rut, label, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Ecuación canónica - RUT {rut}")
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        layout.addWidget(btn_cerrar)


# --- Ventana secundaria (puede ir en otro archivo) ---
class VentanaInterseccion(QDialog):
    def __init__(self, elipse1, elipse2, ruta_cruce, puntos_cruce, idx1, idx2, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Intersección: Elipse {idx1+1} y Elipse {idx2+1}")
        layout = QVBoxLayout(self)
        self.fig = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        self.plot_interseccion(elipse1, elipse2, ruta_cruce, puntos_cruce, idx1, idx2)
    
    def plot_interseccion(self, e1, e2, ruta, puntos_cruce, idx1, idx2):
        ax = self.fig.add_subplot(111)
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
            ax.plot(x_col, y_col, color="red", linewidth=2, label="Ruta de cruce")
        if puntos_cruce:
            x_pcr, y_pcr = zip(*puntos_cruce)
            ax.scatter(x_pcr, y_pcr, color="black", s=50, zorder=6, label="Puntos de cruce")
        ax.set_title("Colisión específica: dos elipses seleccionadas")
        ax.set_aspect('equal')
        ax.legend()
        self.canvas.draw()

# --- Ventana principal ---
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de Trayectorias Elípticas - Drones")
        self.trayectorias = []

        # Layouts
        layout = QVBoxLayout(self)
        input_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        col_inter_layout = QHBoxLayout()

        # Widgets
        self.rut_input = QLineEdit()
        self.rut_input.setPlaceholderText("Ingrese RUT (sin puntos, con guion)")
        self.add_btn = QPushButton("Agregar trayectoria")

        self.list_widget = QListWidget()
        self.list_widget.setMaximumHeight(120)   # Limita el alto de la lista (ajusta a tu gusto)
        self.list_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.list_widget.itemClicked.connect(self.mostrar_ventana_canonica)

        self.graficar_btn = QPushButton("Graficar 2D")
        self.colisiones_btn = QPushButton("Buscar colisiones globales")

        # Nuevos: Combobox para seleccionar elipses y botón para ver colisión específica
        self.combo1 = QComboBox()
        self.combo2 = QComboBox()
        self.combo1.setPlaceholderText("Elipse 1")
        self.combo2.setPlaceholderText("Elipse 2")
        self.colision_especifica_btn = QPushButton("Ver colisión entre 2 elipses")

        self.status_label = QLabel("Bienvenido al simulador")
        self.fig = Figure(figsize=(10, 8))
        self.canvas = FigureCanvas(self.fig)

        # Layout organization
        input_layout.addWidget(self.rut_input)
        input_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.graficar_btn)
        button_layout.addWidget(self.colisiones_btn)
        col_inter_layout.addWidget(self.combo1)
        col_inter_layout.addWidget(self.combo2)
        col_inter_layout.addWidget(self.colision_especifica_btn)

        layout.addLayout(input_layout)
        layout.addWidget(self.list_widget)
        layout.addLayout(button_layout)
        layout.addLayout(col_inter_layout)
        layout.addWidget(self.canvas)
        layout.addWidget(self.status_label)

        # Connect events
        self.add_btn.clicked.connect(self.agregar_trayectoria)
        self.graficar_btn.clicked.connect(self.graficar_trayectorias)
        self.colisiones_btn.clicked.connect(self.buscar_colisiones)
        self.colision_especifica_btn.clicked.connect(self.abrir_ventana_colision)

    def agregar_trayectoria(self):
        rut = self.rut_input.text().strip()
        try:
            nueva = TrayectoriaEliptica.desde_rut(rut)
            self.trayectorias.append(nueva)
            self.list_widget.addItem(f"RUT: {nueva.rut} | Centro: ({nueva.h}, {nueva.k}) | a: {nueva.a} | b: {nueva.b} | θ: {nueva.theta:.2f}")
            self.combo1.addItem(f"{nueva.rut}")
            self.combo2.addItem(f"{nueva.rut}")
            self.status_label.setText(f"Trayectoria para RUT {rut} agregada.")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
        self.rut_input.clear()

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QListWidget, QLabel, QMessageBox, QComboBox,
    QDialog, QSizePolicy
)
import matplotlib.pyplot as plt
from PyQt6.QtGui import QPixmap
import io
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from modelos.trayectoria_eliptica import TrayectoriaEliptica
from servicios.colisionador_trayectorias import ColisionadorTrayectorias

from utils.trayectoria_utils import ecuacion_canonica

import sys

class VentanaEcuacionCanonica(QDialog):
    def __init__(self, rut, label, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Ecuación canónica - RUT {rut}")
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        layout.addWidget(btn_cerrar)


# --- Ventana secundaria (puede ir en otro archivo) ---
class VentanaInterseccion(QDialog):
    def __init__(self, elipse1, elipse2, ruta_cruce, puntos_cruce, idx1, idx2, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Intersección: Elipse {idx1+1} y Elipse {idx2+1}")
        layout = QVBoxLayout(self)
        self.fig = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        self.plot_interseccion(elipse1, elipse2, ruta_cruce, puntos_cruce, idx1, idx2)

    def plot_interseccion(self, e1, e2, ruta, puntos_cruce, idx1, idx2):
        ax = self.fig.add_subplot(111)
        graficar_dos_elipses(e1, e2, idx1, idx2, ruta, puntos_cruce, ax=ax)
        self.canvas.draw()


# --- Ventana principal ---
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de Trayectorias Elípticas - Drones")
        self.trayectorias = []

        # Layouts
        layout = QVBoxLayout(self)
        input_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        col_inter_layout = QHBoxLayout()

        # Widgets
        self.rut_input = QLineEdit()
        self.rut_input.setPlaceholderText("Ingrese RUT (sin puntos, con guion)")
        self.add_btn = QPushButton("Agregar trayectoria")

        self.list_widget = QListWidget()
        self.list_widget.setMaximumHeight(120)   # Limita el alto de la lista (ajusta a tu gusto)
        self.list_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.list_widget.itemClicked.connect(self.mostrar_ventana_canonica)

        self.graficar_btn = QPushButton("Graficar 2D")
        self.colisiones_btn = QPushButton("Buscar colisiones globales")

        # Nuevos: Combobox para seleccionar elipses y botón para ver colisión específica
        self.combo1 = QComboBox()
        self.combo2 = QComboBox()
        self.combo1.setPlaceholderText("Elipse 1")
        self.combo2.setPlaceholderText("Elipse 2")
        self.colision_especifica_btn = QPushButton("Ver colisión entre 2 elipses")

        self.status_label = QLabel("Bienvenido al simulador")
        self.fig = Figure(figsize=(10, 8))
        self.canvas = FigureCanvas(self.fig)

        # Layout organization
        input_layout.addWidget(self.rut_input)
        input_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.graficar_btn)
        button_layout.addWidget(self.colisiones_btn)
        col_inter_layout.addWidget(self.combo1)
        col_inter_layout.addWidget(self.combo2)
        col_inter_layout.addWidget(self.colision_especifica_btn)

        layout.addLayout(input_layout)
        layout.addWidget(self.list_widget)
        layout.addLayout(button_layout)
        layout.addLayout(col_inter_layout)
        layout.addWidget(self.canvas)
        layout.addWidget(self.status_label)

        # Connect events
        self.add_btn.clicked.connect(self.agregar_trayectoria)
        self.graficar_btn.clicked.connect(self.graficar_trayectorias)
        self.colisiones_btn.clicked.connect(self.buscar_colisiones)
        self.colision_especifica_btn.clicked.connect(self.abrir_ventana_colision)

    def agregar_trayectoria(self):
        rut = self.rut_input.text().strip()
        try:
            nueva = TrayectoriaEliptica.desde_rut(rut)
            self.trayectorias.append(nueva)
            self.list_widget.addItem(f"RUT: {nueva.rut} | Centro: ({nueva.h}, {nueva.k}) | a: {nueva.a} | b: {nueva.b} | θ: {nueva.theta:.2f}")
            self.combo1.addItem(f"{nueva.rut}")
            self.combo2.addItem(f"{nueva.rut}")
            self.status_label.setText(f"Trayectoria para RUT {rut} agregada.")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
        self.rut_input.clear()

    def graficar_trayectorias(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        graficar_elipses(self.trayectorias, ax)
        graficar_centros(self.trayectorias, ax)
        resultados = ColisionadorTrayectorias.buscar_colisiones_global(
            self.trayectorias, detectar_ruta=True, detectar_puntos=True
        )
        graficar_rutas_puntos_colision(resultados, self.trayectorias, ax)
        ax.set_title("Trayectorias, centros (O1...), rutas de cruce (rojo), puntos de cruce (negro)")
        ax.set_aspect('equal')
        ax.legend()
        self.canvas.draw()


    def buscar_colisiones(self):
        if len(self.trayectorias) < 2:
            self.status_label.setText("Agrega al menos dos trayectorias.")
            return
        colisiones = ColisionadorTrayectorias.buscar_colisiones_trayectorias(self.trayectorias)
        if not colisiones:
            self.status_label.setText("No hay colisiones detectadas.")
        else:
            msg = "¡Riesgo de colisión entre:\n"
            msg += '\n'.join([f"{e1.rut} y {e2.rut}" for e1, e2 in colisiones])
            self.status_label.setText(msg)

    def abrir_ventana_colision(self):
        idx1 = self.combo1.currentIndex()
        idx2 = self.combo2.currentIndex()
        if idx1 == idx2 or idx1 == -1 or idx2 == -1 or idx1 >= len(self.trayectorias) or idx2 >= len(self.trayectorias):
            QMessageBox.warning(self, "Selección inválida", "Debes seleccionar dos trayectorias diferentes.")
            return
        e1, e2 = self.trayectorias[idx1], self.trayectorias[idx2]
        ruta = ColisionadorTrayectorias.ruta_cruce(e1, e2)
        puntos_cruce = ColisionadorTrayectorias.puntos_interseccion_aproximados(e1, e2)
        ventana = VentanaInterseccion(e1, e2, ruta, puntos_cruce, idx1, idx2, parent=self)
        ventana.exec()

    def mostrar_ventana_canonica(self, item):
        idx = self.list_widget.row(item)
        if 0 <= idx < len(self.trayectorias):
            tr = self.trayectorias[idx]
            ecuacion = ecuacion_canonica(tr)
            label = self.label_ecuacion_latex(ecuacion)
            ventana = VentanaEcuacionCanonica(tr.rut, label, parent=self)
            ventana.exec()

    def label_ecuacion_latex(self, ecuacion_latex):
        fig = plt.figure(figsize=(0.1, 0.1), dpi=300)
        plt.axis('off')
        plt.text(0.5, 0.5, f"${ecuacion_latex}$", fontsize=16, ha='center', va='center')
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.3)
        plt.close(fig)
        buf.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        label = QLabel()
        label.setPixmap(pixmap)
        return label

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.resize(1100, 700)
    ventana.show()
    sys.exit(app.exec())


    def buscar_colisiones(self):
        if len(self.trayectorias) < 2:
            self.status_label.setText("Agrega al menos dos trayectorias.")
            return
        colisiones = ColisionadorTrayectorias.buscar_colisiones_trayectorias(self.trayectorias)
        if not colisiones:
            self.status_label.setText("No hay colisiones detectadas.")
        else:
            msg = "¡Riesgo de colisión entre:\n"
            msg += '\n'.join([f"{e1.rut} y {e2.rut}" for e1, e2 in colisiones])
            self.status_label.setText(msg)

    def abrir_ventana_colision(self):
        idx1 = self.combo1.currentIndex()
        idx2 = self.combo2.currentIndex()
        if idx1 == idx2 or idx1 == -1 or idx2 == -1 or idx1 >= len(self.trayectorias) or idx2 >= len(self.trayectorias):
            QMessageBox.warning(self, "Selección inválida", "Debes seleccionar dos trayectorias diferentes.")
            return
        e1, e2 = self.trayectorias[idx1], self.trayectorias[idx2]
        ruta = ColisionadorTrayectorias.ruta_cruce(e1, e2)
        puntos_cruce = ColisionadorTrayectorias.puntos_interseccion_aproximados(e1, e2)
        ventana = VentanaInterseccion(e1, e2, ruta, puntos_cruce, idx1, idx2, parent=self)
        ventana.exec()

    def mostrar_ventana_canonica(self, item):
        idx = self.list_widget.row(item)
        if 0 <= idx < len(self.trayectorias):
            tr = self.trayectorias[idx]
            ecuacion = ecuacion_canonica(tr)
            label = self.label_ecuacion_latex(ecuacion)
            ventana = VentanaEcuacionCanonica(tr.rut, label, parent=self)
            ventana.exec()

    def label_ecuacion_latex(self, ecuacion_latex):
        fig = plt.figure(figsize=(0.1, 0.1), dpi=300)
        plt.axis('off')
        plt.text(0.5, 0.5, f"${ecuacion_latex}$", fontsize=16, ha='center', va='center')
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.3)
        plt.close(fig)
        buf.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        label = QLabel()
        label.setPixmap(pixmap)
        return label

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.resize(1100, 700)
    ventana.show()
    sys.exit(app.exec())
