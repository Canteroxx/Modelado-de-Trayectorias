from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QListWidget, QLabel, QMessageBox, QComboBox,
    QDialog, QSizePolicy, QGroupBox, QFormLayout, QDoubleSpinBox
)
from PyQt6.QtGui import QPixmap

import io
import sys

from PyQt6.QtCore import Qt
import pyqtgraph as pg

from modelos.trayectoria_eliptica import TrayectoriaEliptica
from servicios.colisionador_trayectorias import ColisionadorTrayectorias
from utils.graficos_utils_pg import agregar_puntos_interactivos
from utils.trayectoria_utils import ecuacion_canonica, ecuacion_general, texto_parametros_elipse, parametros_elipse
from utils.graficos_utils_pg import (
    graficar_elipses,
    graficar_centros,
    graficar_rutas_y_puntos_colision,
    graficar_dos_elipses
)

import matplotlib.pyplot as plt  # Solo para el label de ecuación

# ------------------ Ventanas auxiliares ------------------

class VentanaDetalleElipse(QDialog):
    def __init__(self, tr, parent=None, on_delete=None):
        super().__init__(parent)

        self.setWindowTitle(f"Detalles de la elipse - RUT {tr.rut}")
        layout = QVBoxLayout(self)

        self.tr = tr
        self.on_delete = on_delete

        # Ecuación canónica LaTeX
        eq_label = QLabel("<b>Ecuación canónica:</b>")
        layout.addWidget(eq_label)
        label_img = self.label_ecuacion_latex(ecuacion_canonica(tr))
        formula_general = ecuacion_general(tr)
        latex_label = self.label_ecuacion_latex(formula_general)
        layout.addWidget(label_img, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(latex_label)

        # Parámetros matemáticos
        param_label = QLabel("<b>Parámetros:</b>")
        layout.addWidget(param_label)
        param_txt = QLabel(texto_parametros_elipse(parametros_elipse(tr)))
        param_txt.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(param_txt)

        btn_eliminar = QPushButton("Eliminar este RUT")
        btn_eliminar.setStyleSheet("background-color: #e57373; color: white;")
        btn_eliminar.clicked.connect(self.eliminar_rut)
        layout.addWidget(btn_eliminar)

        # Botón cerrar
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        layout.addWidget(btn_cerrar)

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

    def eliminar_rut(self):
        res = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Seguro que quieres eliminar esta trayectoria?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if res == QMessageBox.StandardButton.Yes:
            if self.on_delete:
                self.on_delete(self.tr)
            self.accept()

class VentanaInterseccion(QDialog):
    def __init__(self, elipse1, elipse2, ruta_cruce, puntos_cruce, idx1, idx2, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Intersección: Elipse {idx1+1} y Elipse {idx2+1}")
        layout = QVBoxLayout(self)
        self.pg_widget = pg.GraphicsLayoutWidget()
        layout.addWidget(self.pg_widget)
        self.plot_interseccion(elipse1, elipse2, ruta_cruce, puntos_cruce, idx1, idx2)

    def plot_interseccion(self, elipse1, elipse2, ruta_cruce, puntos_cruce, idx1, idx2):
        plot = self.pg_widget.addPlot()
        graficar_dos_elipses(elipse1, elipse2, idx1, idx2, ruta_cruce, puntos_cruce, plot)

        # Agregar centros interactivos
        centros = [(elipse1.h, elipse1.k), (elipse2.h, elipse2.k)]
        agregar_puntos_interactivos(plot, centros, nombre="Centro")

        # Agregar puntos de intersección interactivos
        if puntos_cruce:
            agregar_puntos_interactivos(plot, puntos_cruce, nombre="Cruce")
# ------------------ Ventana principal ------------------

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
        self.editor_box = self.create_editor_box()

        # Widgets
        self.rut_input = QLineEdit()
        self.rut_input.setPlaceholderText("Ingrese RUT (sin puntos, con guion)")
        self.add_btn = QPushButton("Agregar trayectoria")

        self.list_widget = QListWidget()
        self.list_widget.setMaximumHeight(120)
        self.list_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.list_widget.itemDoubleClicked.connect(self.mostrar_detalle_elipse)

        self.graficar_btn = QPushButton("Graficar 2D")
        self.colisiones_btn = QPushButton("Buscar colisiones globales")

        self.combo1 = QComboBox()
        self.combo2 = QComboBox()
        self.combo1.setPlaceholderText("Elipse 1")
        self.combo2.setPlaceholderText("Elipse 2")
        self.colision_especifica_btn = QPushButton("Ver colisión entre 2 elipses")

        self.status_label = QLabel("Bienvenido al simulador")

        self.pg_widget = pg.GraphicsLayoutWidget()
        self.plot = self.pg_widget.addPlot()
        self.plot.showGrid(x=True, y=True)
        self.plot.setAspectLocked(True)

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
        layout.addWidget(self.pg_widget)
        layout.addWidget(self.status_label)
        layout.addWidget(self.editor_box)
        layout.addWidget(self.pg_widget)
        layout.addWidget(self.status_label)

        # Connect events
        self.add_btn.clicked.connect(self.agregar_trayectoria)
        self.graficar_btn.clicked.connect(self.graficar_trayectorias)
        self.colisiones_btn.clicked.connect(self.buscar_colisiones)
        self.colision_especifica_btn.clicked.connect(self.abrir_ventana_colision)
        self.combo_editar.currentIndexChanged.connect(self.cargar_elipse_en_editor)

    def create_editor_box(self):
        box = QGroupBox("Editar Elipse")
        form = QFormLayout(box)
        self.combo_editar = QComboBox()
        self.spin_h = QDoubleSpinBox()
        self.spin_k = QDoubleSpinBox()
        self.spin_a = QDoubleSpinBox()
        self.spin_b = QDoubleSpinBox()
        self.spin_h.setDecimals(2)
        self.spin_k.setDecimals(2)
        self.spin_a.setDecimals(2)
        self.spin_b.setDecimals(2)
        self.spin_a.setMinimum(0.1)
        self.spin_b.setMinimum(0.1)
        for w in [self.spin_h, self.spin_k, self.spin_a, self.spin_b]:
            w.setRange(-1000, 1000)

        self.spin_h.valueChanged.connect(self.editar_elipse_seleccionada)
        self.spin_k.valueChanged.connect(self.editar_elipse_seleccionada)
        self.spin_a.valueChanged.connect(self.editar_elipse_seleccionada)
        self.spin_b.valueChanged.connect(self.editar_elipse_seleccionada)

        form.addRow("Seleccionar elipse", self.combo_editar)
        form.addRow("Centro h", self.spin_h)
        form.addRow("Centro k", self.spin_k)
        form.addRow("a", self.spin_a)
        form.addRow("b", self.spin_b)
        return box

    def agregar_trayectoria(self):
        rut = self.rut_input.text().strip()
        try:
            nueva = TrayectoriaEliptica.desde_rut(rut)
            self.trayectorias.append(nueva)
            self.list_widget.addItem(f"RUT: {nueva.rut} | Centro: ({nueva.h}, {nueva.k}) | a: {nueva.a} | b: {nueva.b}")
            self.combo1.addItem(f"{nueva.rut}")
            self.combo2.addItem(f"{nueva.rut}")
            self.combo_editar.addItem(f"{nueva.rut}")
            self.status_label.setText(f"Trayectoria para RUT {rut} agregada.")
            self.graficar_trayectorias()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
        self.rut_input.clear()

    def mostrar_detalle_elipse(self, item):
        idx = self.list_widget.row(item)
        if 0 <= idx < len(self.trayectorias):
            tr = self.trayectorias[idx]
            def eliminar_callback(eliminada):
                del self.trayectorias[idx]
                self.list_widget.takeItem(idx)
                self.combo1.removeItem(idx)
                self.combo2.removeItem(idx)
                self.combo_editar.removeItem(idx)
                self.graficar_trayectorias()
                self.status_label.setText(f"RUT {eliminada.rut} eliminado.")
            ventana = VentanaDetalleElipse(tr, parent=self, on_delete=eliminar_callback)
            ventana.exec()

    def editar_elipse_seleccionada(self):
        idx = self.combo_editar.currentIndex()
        if 0 <= idx < len(self.trayectorias):
            el = self.trayectorias[idx]
            el.h = self.spin_h.value()
            el.k = self.spin_k.value()
            el.a = self.spin_a.value()
            el.b = self.spin_b.value()
            self.graficar_trayectorias()

    def cargar_elipse_en_editor(self):
        idx = self.combo_editar.currentIndex()
        if 0 <= idx < len(self.trayectorias):
            el = self.trayectorias[idx]
            self.spin_h.blockSignals(True)
            self.spin_k.blockSignals(True)
            self.spin_a.blockSignals(True)
            self.spin_b.blockSignals(True)
            self.spin_h.setValue(el.h)
            self.spin_k.setValue(el.k)
            self.spin_a.setValue(el.a)
            self.spin_b.setValue(el.b)
            self.spin_h.blockSignals(False)
            self.spin_k.blockSignals(False)
            self.spin_a.blockSignals(False)
            self.spin_b.blockSignals(False)

    def graficar_trayectorias(self):
        self.plot.clear()
        colores = ["blue", "green", "orange", "purple", "cyan", "brown", "magenta", "gold", "pink"]
        graficar_elipses(self.trayectorias, self.plot, colores)
        graficar_centros(self.trayectorias, self.plot)
        resultados = ColisionadorTrayectorias.buscar_colisiones_detalladas(self.trayectorias, incluir_ruta_cruce=True, incluir_puntos_cruce=True)
        graficar_rutas_y_puntos_colision(resultados, self.trayectorias, self.plot)
        centros = [(t.h, t.k) for t in self.trayectorias]
        agregar_puntos_interactivos(self.plot, centros, nombre='Centro')

        # Mostrar puntos de cruce interactivos
        puntos_cruce = []
        for colision in resultados:
            if colision['puntos_cruce']:
                puntos_cruce.extend(colision['puntos_cruce'])
        if puntos_cruce:
            agregar_puntos_interactivos(self.plot, puntos_cruce, nombre='Cruce')

        self.plot.setTitle("Trayectorias, centros (O1...), rutas de cruce (rojo), puntos de cruce (negro)")
        self.plot.setAspectLocked(True)

    def buscar_colisiones(self):
        if len(self.trayectorias) < 2:
            self.status_label.setText("Agrega al menos dos trayectorias.")
            return
        colisiones = ColisionadorTrayectorias.buscar_pares_con_colision(self.trayectorias)
        if not colisiones:
            self.status_label.setText("No hay colisiones detectadas.")
        else:
            msg = "¡Riesgo de colisión entre:\n"
            msg += '\n'.join([f"{el1.rut} y {el2.rut}" for el1, el2 in colisiones])
            self.status_label.setText(msg)

    def abrir_ventana_colision(self):
        idx1 = self.combo1.currentIndex()
        idx2 = self.combo2.currentIndex()
        if idx1 == idx2 or idx1 == -1 or idx2 == -1 or idx1 >= len(self.trayectorias) or idx2 >= len(self.trayectorias):
            QMessageBox.warning(self, "Selección inválida", "Debes seleccionar dos trayectorias diferentes.")
            return
        elipse_1, elipse_2 = self.trayectorias[idx1], self.trayectorias[idx2]
        ruta = ColisionadorTrayectorias.calcular_ruta_cruce(elipse_1, elipse_2)
        puntos_cruce = ColisionadorTrayectorias.calcular_puntos_interseccion_aproximados(elipse_1, elipse_2)
        ventana = VentanaInterseccion(elipse_1, elipse_2, ruta, puntos_cruce, idx1, idx2, parent=self)
        ventana.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.resize(1100, 700)
    ventana.show()
    sys.exit(app.exec())
