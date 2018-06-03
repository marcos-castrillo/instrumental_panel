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
        self.modo = self.app.modo
        # Elementos
        self.guardarButton = tk.Button(master, text='Guardar', width=10, command=self.save_opciones)

        self.modoRadioLabel = tk.Label(master, text="Modo de funcionamiento", bg='white')
        self.modoRadio0 = tk.Radiobutton(master, text="Adquisición de datos", variable=self.modo, value='Adquisición')
        self.modoRadio1 = tk.Radiobutton(master, text="Simulación de datos", variable=self.modo, value='Simulación')

        self.modoRadioLabel.grid(row=0, column=0)
        self.modoRadio0.grid(row=1, column=0)
        self.modoRadio1.grid(row=2, column=0)
        self.guardarButton.grid(row=3, column=0)

    def save_opciones(self):
        opciones = {
            "modo": self.modo.get()
        }
        self.app.main.estadoLabel.config(text=self.modo.get())
        self.app.set_opciones(opciones)

