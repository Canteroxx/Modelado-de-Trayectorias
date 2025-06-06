import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import re
from trayectoria_eliptica_3d import TrayectoriaEliptica3D
from colisionador_trayectorias_3d import ColisionadorElipticas3D

class Elipses3DApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestor de RUTs y Gráfico de Elipses 3D")
        self.ruts = []  # Lista de [rut, z, theta, es_radian]

        # Frame de entrada
        frm_input = tk.Frame(master, padx=10, pady=10)
        frm_input.pack(fill="x")
        tk.Label(frm_input, text="RUT (XXXXXXXX-Y):").pack(side="left")
        self.rut_entry = tk.Entry(frm_input, width=15)
        self.rut_entry.pack(side="left", padx=2)
        tk.Label(frm_input, text="Coordenada z:").pack(side="left")
        self.z_entry = tk.Entry(frm_input, width=6)
        self.z_entry.pack(side="left", padx=2)
        self.z_entry.insert(0, "0")
        tk.Label(frm_input, text="Rotación (θ):").pack(side="left")
        self.theta_entry = tk.Entry(frm_input, width=6)
        self.theta_entry.pack(side="left", padx=2)
        self.theta_entry.insert(0, "0")
        self.is_radian = tk.BooleanVar(value=False)
        self.chk_radian = tk.Checkbutton(frm_input, text="En radianes", variable=self.is_radian)
        self.chk_radian.pack(side="left", padx=2)
        tk.Button(frm_input, text="Agregar", command=self.agregar_rut).pack(side="left", padx=5)

        # Frame de listado y acciones
        frm_list = tk.Frame(master, padx=10, pady=10)
        frm_list.pack(fill="x")
        self.lstbox = tk.Listbox(frm_list, height=6, width=50)
        self.lstbox.pack(side="left")
        btn_frame = tk.Frame(frm_list)
        btn_frame.pack(side="left", padx=10)
        tk.Button(btn_frame, text="Eliminar seleccionado", command=self.eliminar_rut).pack(fill="x", pady=2)
        tk.Button(btn_frame, text="Actualizar lista", command=self.actualizar_lista).pack(fill="x", pady=2)

        # Frame para seleccionar 2 RUTs
        frm_select = tk.Frame(master, padx=10, pady=10)
        frm_select.pack(fill="x")
        tk.Label(frm_select, text="Elipse 1:").pack(side="left")
        self.sel_rut1 = tk.StringVar()
        self.opt_rut1 = tk.OptionMenu(frm_select, self.sel_rut1, ())
        self.opt_rut1.pack(side="left", padx=5)
        tk.Label(frm_select, text="Elipse 2:").pack(side="left")
        self.sel_rut2 = tk.StringVar()
        self.opt_rut2 = tk.OptionMenu(frm_select, self.sel_rut2, ())
        self.opt_rut2.pack(side="left", padx=5)
        tk.Button(frm_select, text="Graficar 3D", command=self.graficar).pack(side="left", padx=10)

        # Frame gráfico
        self.frame_graf = tk.Frame(master, padx=10, pady=10)
        self.frame_graf.pack(fill="both", expand=True)

        self.actualizar_lista()

    def agregar_rut(self):
        rut = self.rut_entry.get().strip()
        z_str = self.z_entry.get().strip()
        theta_str = self.theta_entry.get().strip()
        is_rad = self.is_radian.get()
        # Validación de z
        try:
            z = float(z_str)
        except ValueError:
            messagebox.showerror("Error", "La coordenada z debe ser un número.")
            return
        # Validación de theta
        try:
            theta = float(theta_str)
        except ValueError:
            messagebox.showerror("Error", "El ángulo debe ser un número.")
            return
        # Si no es radianes, convertir de grados a radianes
        if not is_rad:
            theta = np.deg2rad(theta)
        # Validación de RUT
        if not re.fullmatch(r"\d{8}-[\dkK]", rut):
            messagebox.showerror("Error", "Formato de RUT incorrecto (debe ser XXXXXXXX-Y)")
            return
        for rut_guardado, z_guardado, theta_guardado, rad_guardado in self.ruts:
            if rut == rut_guardado and z == z_guardado and theta == theta_guardado:
                messagebox.showwarning("Atención", "Este RUT, z y theta ya fue ingresado.")
                return
        try:
            TrayectoriaEliptica3D.desde_rut(rut, z0=z, theta=theta)  # Valida el RUT, z y theta
            self.ruts.append([rut, z, theta, is_rad])
            self.actualizar_lista()
            self.rut_entry.delete(0, tk.END)
            self.z_entry.delete(0, tk.END)
            self.z_entry.insert(0, "0")
            self.theta_entry.delete(0, tk.END)
            self.theta_entry.insert(0, "0")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_rut(self):
        seleccion = self.lstbox.curselection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un RUT para eliminar.")
            return
        idx = seleccion[0]
        del self.ruts[idx]
        self.actualizar_lista()

    def actualizar_lista(self):
        # Actualiza Listbox y OptionMenus
        self.lstbox.delete(0, tk.END)
        for rut, z, theta, is_rad in self.ruts:
            grados = np.rad2deg(theta) if is_rad else theta
            self.lstbox.insert(
                tk.END,
                f"{rut}   z={z}   θ={'{:.2f}'.format(theta)} rad"
            )
        menu1 = self.opt_rut1["menu"]
        menu2 = self.opt_rut2["menu"]
        menu1.delete(0, tk.END)
        menu2.delete(0, tk.END)
        for rut, z, theta, is_rad in self.ruts:
            label = f"{rut}   z={z}   θ={'{:.2f}'.format(theta)} rad"
            combo_val = f"{rut}|{z}|{theta}"
            menu1.add_command(label=label, command=lambda v=combo_val: self.sel_rut1.set(v))
            menu2.add_command(label=label, command=lambda v=combo_val: self.sel_rut2.set(v))
        # Desmarcar selección previa
        if self.ruts:
            first = f"{self.ruts[0][0]}|{self.ruts[0][1]}|{self.ruts[0][2]}"
            self.sel_rut1.set(first)
            self.sel_rut2.set(first if len(self.ruts) == 1 else f"{self.ruts[1][0]}|{self.ruts[1][1]}|{self.ruts[1][2]}")
        else:
            self.sel_rut1.set('')
            self.sel_rut2.set('')

    def graficar(self):
        v1 = self.sel_rut1.get()
        v2 = self.sel_rut2.get()
        if not v1 or not v2 or v1 == v2:
            messagebox.showerror("Error", "Selecciona dos RUTs distintos.")
            return
        rut1, z1, theta1 = v1.split('|')
        rut2, z2, theta2 = v2.split('|')
        try:
            elipse1 = TrayectoriaEliptica3D.desde_rut(rut1, z0=float(z1), theta=float(theta1))
            elipse2 = TrayectoriaEliptica3D.desde_rut(rut2, z0=float(z2), theta=float(theta2))
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        for w in self.frame_graf.winfo_children():
            w.destroy()

        fig = plt.Figure(figsize=(7, 5))
        ax = fig.add_subplot(111, projection='3d')

        # Graficar ambas elipses en sus planos z y con rotación
        x1, y1, z1s = elipse1.puntos_3d()
        x2, y2, z2s = elipse2.puntos_3d()
        ax.plot(x1, y1, z1s, label=f"Elipse 1: {rut1}  z={z1}", color='blue')
        ax.plot(x2, y2, z2s, label=f"Elipse 2: {rut2}  z={z2}", color='red')
        ax.scatter([elipse1.h], [elipse1.k], [float(z1)], color='blue', marker='o', s=50, label='Centro 1')
        ax.scatter([elipse2.h], [elipse2.k], [float(z2)], color='red', marker='o', s=50, label='Centro 2')

        # Mostrar intersecciones (si las quieres)
        intersecciones = ColisionadorElipticas3D.puntos_interseccion_xyz(elipse1, elipse2, n=400, tolerancia=0.5)
        if intersecciones:
            inters = np.array(intersecciones)
            ax.scatter(inters[:, 0], inters[:, 1], inters[:, 2], color='green', s=80, marker='x', label='Intersección')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Elipses 3D (z y θ variables)')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_graf)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()


# ----------- Lanzar la app ------------
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1050x700")
    app = Elipses3DApp(root)
    root.mainloop()
