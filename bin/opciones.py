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
        intervalo = configuracion["intervalo"]
        # Elementos
        self.guardarButton = tk.Button(master, text='Guardar', width=10, command=self.save_opciones)
        self.intervaloLabel = tk.Label(master, text="Intervalo de medición")
        self.intervaloEntry = tk.Entry(master, bd=5, width=6)
        self.intervaloEntry.insert(0, intervalo)

        self.intervaloLabel.grid(row=0, column=0)
        self.intervaloEntry.grid(row=1, column=0)
        self.guardarButton.grid(row=2, column=0)

    def save_opciones(self):
        intervalo = self.intervaloEntry.get()
        opciones = {
            "intervalo": intervalo
        }
        self.app.set_opciones(opciones)

