import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

from tkinter.colorchooser import *

class AjustesMedidores(tk.Frame, object):
    def __init__(self, master, main, app, configuracion, **kwargs):
        super(AjustesMedidores, self).__init__(master, configuracion=None, **kwargs)
        self.master = master
        self.master.configure(bg='white', highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.main = main
        self.app = app
        n_promedios = configuracion["n_promedios"]
        self.umbrales = configuracion["umbrales"]
        self.colores = configuracion["colores"]
        self.n_colores = len(self.colores)
        self.elementos = {}
        # Elementos de los ajustes
        self.promedioLabel = tk.Label(master, text="Promedios por vuelta", bg='white')
        self.promedioEntry = tk.Entry(master, bd=5, width=5)
        self.promedioEntry.insert(0, n_promedios)
        for i in range(self.n_colores - 1):
            self.elementos["umbralLabel" + str(i)] = tk.Label(master, text="Umbral " + str(i+1) + " (%)", bg='white')
            self.elementos["umbralEntry" + str(i)] = tk.Entry(master, bd=5, width="4")
            self.elementos["umbralEntry" + str(i)].insert(0, self.umbrales[i + 1])
        for i in range(self.n_colores):
            self.elementos["colorLabel" + str(i)] = tk.Label(master, text="Color si: " + str(self.umbrales[i]) + "% < valor <=" + str(self.umbrales[i + 1]) + "%", bg='white')
            self.elementos["colorEntry" + str(i)] = tk.Button(master, width="10", command = lambda i=i: self.set_color(i))
            self.elementos["colorEntry" + str(i)].config(text=self.colores[i], bg=self.colores[i])
        self.guardarButton = tk.Button(master, text='Guardar', width=10, command=self.save_ajustes)
        # Ajustar la posición de los elementos
        self.promedioLabel.grid(row=0, column=0, columnspan=2)
        self.promedioEntry.grid(row=1, column=0, columnspan=2)
        for i in range(self.n_colores - 1):
            self.elementos["umbralLabel" + str(i)].grid(row=2*i+2, column=0)
            self.elementos["umbralEntry" + str(i)].grid(row=2*i+3, column=0)
        for i in range(self.n_colores):
            self.elementos["colorLabel" + str(i)].grid(row=2*i+2, column=1)
            self.elementos["colorEntry" + str(i)].grid(row=2*i+3, column=1)
        self.guardarButton.grid(row=2*i+self.n_colores+5, column=0, columnspan=2)

    def set_color(self, i):
        color = askcolor(initialcolor = self.colores[i])
        self.elementos["colorEntry" + str(i)].config(text=color[1], bg=color[1])

    def save_ajustes(self):
        n_promedios = self.promedioEntry.get()
        umbrales = []
        for i in range(self.n_colores - 1):
            umbrales.append(self.elementos["umbralEntry" + str(i)].get())
        colores = []
        for i in range(self.n_colores):
            colores.append(self.elementos["colorEntry" + str(i)].cget('text'))
        ajustes = {
            "n_promedios": n_promedios,
            "umbrales": umbrales,
            "colores": colores
        }
        self.main.save_ajustes_medidor(self, ajustes)

    def set_ajustes(self):
        for i in range(self.n_colores):
            self.elementos["colorLabel" + str(i)].configure(text="Color si: " + str(self.umbrales[i]) + "% < valor <=" + str(self.umbrales[i + 1]) + "%", bg='white')
