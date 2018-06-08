# coding=utf-8
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

class Opciones(tk.Frame, object):
    def __init__(self, master, app, configuracion, **kwargs):
        super(Opciones, self).__init__(master,configuracion=None, **kwargs)
        # Parámetros
        self.master = master
        self.app = app
        self.modo = configuracion["modo"]
        self.n_lineas = int(configuracion["n_lineas"])
        # Elementos
        self.aplicarButton = tk.Button(master, text='Aplicar', width=10, command=self.guardar_opciones)
        self.aceptarButton = tk.Button(master, text='Aceptar', width=10, command=self.aceptar_opciones)

        self.modoRadioLabel = tk.Label(master, text="Modo de funcionamiento", bg='white', font='Helvetica 10 bold')
        self.modoRadio0 = tk.Radiobutton(master, text="Adquisición de datos", variable=self.modo, value='Adquisición', bg='white')
        self.modoRadio1 = tk.Radiobutton(master, text="Simulación de datos", variable=self.modo, value='Simulación', bg='white')

        self.lineasLabel = tk.Label(master, text="Nº de líneas superpuestas", bg='white', font='Helvetica 10 bold')
        self.lineasEntry = tk.Entry(master, bd=5, width="5")
        self.lineasEntry.insert(0, str(self.n_lineas))
        self.modoRadioLabel.grid(row=0, column=0, columnspan=2)
        self.modoRadio0.grid(row=1, column=0, columnspan=2)
        self.modoRadio1.grid(row=2, column=0, columnspan=2)
        self.lineasLabel.grid(row=3, column=0, columnspan=2)
        self.lineasEntry.grid(row=4, column=0, columnspan=2)
        self.aplicarButton.grid(row=5, column=0)
        self.aceptarButton.grid(row=5, column=1)

    def aceptar_opciones(self):
        self.app.main.desplegar_opciones()
        self.guardar_opciones()

    def guardar_opciones(self):
        opciones = {
            "modo": self.modo.get(),
            "n_lineas": int(self.lineasEntry.get())
        }
        self.app.main.estadoLabel.config(text=self.modo.get())
        self.app.set_opciones(opciones)

