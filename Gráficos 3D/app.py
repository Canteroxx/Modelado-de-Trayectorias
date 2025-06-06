import tkinter as tk
from tkinter import messagebox
import re
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D

# Lista para almacenar los RUTs procesados
rut_lista = []

def actualizar_label():
    """Actualiza la label con la lista de RUTs ingresados"""
    if not rut_lista:
        label_ruts.config(text="No se ha ingresado ningún RUT")
    else:
        ruts_formateados = "\n".join([rut[0] + "-" + rut[1] for rut in rut_lista])
        label_ruts.config(text=f"RUTs almacenados:\n{ruts_formateados}")

def procesar_rut():
    rut = entrada_rut.get().strip()  # Quita espacios
    # Validar formato: 8 dígitos, un guion y verificador (1-9 o 'k')
    if not re.fullmatch(r"\d{8}-[1-9k]", rut, re.IGNORECASE):
        messagebox.showerror("Error", "Formato de RUT incorrecto (debe ser XXXXXXXX-Y, donde Y es 1-9 o k)")
        return
    numeros, verificador = rut.split('-')
    rut_lista.append([numeros, verificador])
    actualizar_label()

def compute_ellipse(rut):
    """
    Dado un RUT (formato [numeros, verificador]), calcula:
      - Centro (h, k)
      - Semiejes: a y b
      - Orientación: se decide si se intercambian los semiejes
    Retorna:
      x, y, z: arrays de la elipse en 3D.
      params: diccionario con {h, k, a, b, rut}
    """
    numeros, verificador = rut
    digitos = list(map(int, numeros))
    # Determinar si el dígito verificador es impar
    es_impar = verificador.isdigit() and int(verificador) % 2 == 1

    if es_impar:
        h, k = digitos[0], digitos[1]
        a = digitos[2] + digitos[3]
        b = digitos[4] + digitos[5]
        orientacion_horizontal = (digitos[7] % 2 == 0)
    else:
        h, k = digitos[0], digitos[1]
        a = digitos[5] + digitos[6]
        b = digitos[7] + digitos[2]
        orientacion_horizontal = (digitos[3] % 2 == 0)
    
    theta = np.linspace(0, 2 * np.pi, 100)
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    z = np.sin(theta) * (a + b) / 2  # Se usa esta función para la altura
    
    # Si la orientación no es horizontal, intercambiamos x e y:
    if not orientacion_horizontal:
        x, y = y, x

    # Trasladar la elipse al centro (h, k)
    x += h
    y += k
    params = {"h": h, "k": k, "a": a, "b": b, "rut": f"{numeros}-{verificador}"}
    return x, y, z, params

def detectar_intersecciones(x1, y1, x2, y2, tol=0.5):
    """
    Dadas dos curvas (x1, y1) y (x2, y2), detecta puntos cuya distancia sea menor a 'tol'.
    Retorna una lista de puntos (x, y) únicos.
    """
    intersecciones = []
    for i in range(len(x1)):
        for j in range(len(x2)):
            d = sqrt((x1[i] - x2[j])**2 + (y1[i] - y2[j])**2)
            if d < tol:
                xi = (x1[i] + x2[j]) / 2  # promedio de los puntos
                yi = (y1[i] + y2[j]) / 2
                intersecciones.append( (round(xi,2), round(yi,2)) )
    # Eliminar duplicados
    unique_inters = []
    for pt in intersecciones:
        if pt not in unique_inters:
            unique_inters.append(pt)
    return unique_inters

def graficar_elipses():
    """
    Grafica las 2 últimas elipses en 3D y detecta intersecciones en (x, y).
    Si hay menos de 2 RUTS se muestra un error.
    """
    if len(rut_lista) < 2:
        messagebox.showerror("Error", "Se deben ingresar al menos 2 antes de graficar")
        return
    
    # Calcular las dos últimas elipses
    x1, y1, z1, params1 = compute_ellipse(rut_lista[-2])
    x2, y2, z2, params2 = compute_ellipse(rut_lista[-1])

    # Limpiar el área gráfica previa
    for widget in frame_grafico.winfo_children():
        widget.destroy()
        
    # Crear la figura y el eje 3D
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    # Graficar ambas elipses
    ax.plot(x1, y1, z1, label=f"Elipse 1 (RUT: {params1['rut']})", color="#E74C3C")
    ax.plot(x2, y2, z2, label=f"Elipse 2 (RUT: {params2['rut']})", color="#3498DB")
    
    # Marcar los centros de cada elipse
    ax.scatter([params1["h"]], [params1["k"]], [0], color='red', marker='o', s=50, label="Centro 1")
    ax.scatter([params2["h"]], [params2["k"]], [0], color='blue', marker='o', s=50, label="Centro 2")
    
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Altura (Z)")
    ax.legend(loc="upper right")
    ax.set_title("Elipses 3D generadas")
    ax.grid()
    
    # Detectar intersecciones en la proyección (x, y)
    inters = detectar_intersecciones(x1, y1, x2, y2, tol=0.5)
    if inters:
        # Limitar resultados a un máximo de 2
        if len(inters) > 2:
            inters = inters[:2]
        inters_arr = np.array(inters)
        # Marcar los puntos de intersección en el gráfico (con marcador rojo)
        ax.scatter(inters_arr[:,0], inters_arr[:,1], [0]*len(inters_arr), color="red", marker="o", s=80, label="Intersecciones")
    
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.get_tk_widget().pack()
    canvas.draw()
    
    # Actualizar la cuarta label con información de ambas elipses y de las intersecciones
    texto = (
        f"Elipse 1:\n"
        f"RUT: {params1['rut']}\n"
        f"Centro: ({params1['h']}, {params1['k']})\n"
        f"a = {params1['a']}, b = {params1['b']}\n\n"
        f"Elipse 2:\n"
        f"RUT: {params2['rut']}\n"
        f"Centro: ({params2['h']}, {params2['k']})\n"
        f"a = {params2['a']}, b = {params2['b']}\n"
    )
    if inters:
        texto += "\nIntersecciones:\n"
        for pt in inters:
            texto += f"({pt[0]}, {pt[1]})  "
    else:
        texto += "\nIntersecciones: Ninguna."
        
    label_valores.config(text=texto)

# -------------------------------------------------
# Configuración de la ventana principal y distribución de labels

ventana = tk.Tk()
ventana.title("Ingreso de RUT y Gráfica de Elipses en 3D")
ventana.geometry("1200x800")

# Primera label (Esquina superior izquierda): Input de RUT y botón "Guardar RUT"
frame_input = tk.Frame(ventana, relief="ridge", bd=5)
frame_input.place(x=20, y=20,width=750,height=160)
tk.Label(frame_input, text="Ingrese RUT:", font=("Arial", 12, "bold")).pack(pady=5)
entrada_rut = tk.Entry(frame_input, font=("Arial", 12))
entrada_rut.pack(pady=5)
tk.Button(frame_input, text="Guardar RUT", font=("Arial", 12), command=procesar_rut).pack(pady=10)

# Segunda label (Esquina superior derecha): Lista de RUTS ingresados
frame_ruts = tk.Frame(ventana, relief="ridge", bd=5)
frame_ruts.place(x=800, y=20,width=350,height=160)
label_ruts = tk.Label(frame_ruts, text="No se ha ingresado ningún RUT", font=("Arial", 12), justify="left", anchor="w")
label_ruts.pack(pady=10, fill="both")

# Tercera label (Parte inferior izquierda): Área gráfica y botón "Graficar"
frame_grafico = tk.Frame(ventana, relief="ridge", bd=5)
frame_grafico.place(x=20, y=200, width=750, height=550)
tk.Button(frame_grafico, text="Graficar", font=("Arial", 12), command=graficar_elipses).pack(pady=5)

# Cuarta label (Parte inferior derecha): Datos de ambas elipses e intersecciones
frame_datos = tk.Frame(ventana, relief="ridge", bd=5)
frame_datos.place(x=800, y=200, width=350, height=550)
label_valores = tk.Label(frame_datos, text="Datos de elipses e intersecciones aparecerán aquí.", 
                         font=("Arial", 12), justify="left", anchor="nw")
label_valores.pack(pady=10, padx=5, fill="both")

ventana.mainloop()