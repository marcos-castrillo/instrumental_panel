# coding=utf-8
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

from tkinter.colorchooser import *
from redondeo import redondear

class AjustesGraficos(tk.Frame, object):
    def __init__(self, master, main, app, configuracion, **kwargs):
        super(AjustesGraficos, self).__init__(master, configuracion=None, **kwargs)
        self.master = master
        self.master.configure(bg='white', highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.main = main
        self.app = app
        self.live = configuracion["live"]
        self.minX = configuracion["minX"]
        self.maxX = configuracion["maxX"]
        self.stepX = configuracion["stepX"]
        if self.live:
            self.minY1 = configuracion["minY1"]
            self.maxY1 = configuracion["maxY1"]
            self.stepY1 = configuracion["stepY1"]
            self.minY2 = configuracion["minY2"]
            self.maxY2 = configuracion["maxY2"]
            self.stepY2 = configuracion["stepY2"]
        else:
            self.minY = configuracion["minY"]
            self.maxY = configuracion["maxY"]
            self.stepY = configuracion["stepY"]
        self.ejeXLabel = tk.Label(master, text="Rango del eje X", bg='white', font='Helvetica 10 bold')
        self.minXEntry = tk.Entry(master, bd=5, width=5)
        self.minXEntry.insert(0, self.minX)
        self.maxXEntry = tk.Entry(master, bd=5, width=5)
        self.maxXEntry.insert(0, self.maxX)
        self.stepXLabel = tk.Label(master, text="Paso del eje X", bg='white', font='Helvetica 10 bold')
        self.stepXEntry = tk.Entry(master, bd=5, width=5)
        self.stepXEntry.insert(0, self.stepX)
        if self.live:
            self.ejeY1Label = tk.Label(master, text="Rango del eje Y1", bg='white', font='Helvetica 10 bold')
            self.minY1Entry = tk.Entry(master, bd=5, width=5)
            self.minY1Entry.insert(0, self.minY1)
            self.maxY1Entry = tk.Entry(master, bd=5, width=5)
            self.maxY1Entry.insert(0, self.maxY1)
            self.stepY1Label = tk.Label(master, text="Paso del eje Y1", bg='white', font='Helvetica 10 bold')
            self.stepY1Entry = tk.Entry(master, bd=5, width=5)
            self.stepY1Entry.insert(0, self.stepY1)
            self.ejeY2Label = tk.Label(master, text="Rango del eje Y2", bg='white', font='Helvetica 10 bold')
            self.minY2Entry = tk.Entry(master, bd=5, width=5)
            self.minY2Entry.insert(0, self.minY2)
            self.maxY2Entry = tk.Entry(master, bd=5, width=5)
            self.maxY2Entry.insert(0, self.maxY2)
            self.stepY2Label = tk.Label(master, text="Paso del eje Y2", bg='white', font='Helvetica 10 bold')
            self.stepY2Entry = tk.Entry(master, bd=5, width=5)
            self.stepY2Entry.insert(0, self.stepY2)
        else:
            self.ejeYLabel = tk.Label(master, text="Rango del eje Y", bg='white', font='Helvetica 10 bold')
            self.minYEntry = tk.Entry(master, bd=5, width=5)
            self.minYEntry.insert(0, self.minY)
            self.maxYEntry = tk.Entry(master, bd=5, width=5)
            self.maxYEntry.insert(0, self.maxY)
            self.stepYLabel = tk.Label(master, text="Paso del eje Y", bg='white', font='Helvetica 10 bold')
            self.stepYEntry = tk.Entry(master, bd=5, width=5)
            self.stepYEntry.insert(0, self.stepY)
        self.aceptarButton = tk.Button(master, text='Aceptar', width=10, command= lambda: self.aceptar_ajustes('aceptar'))
        self.aplicarButton = tk.Button(master, text='Aplicar', width=10,command= lambda: self.aceptar_ajustes('aplicar'))
        # Ajustar la posición de los elementos
        self.ejeXLabel.grid(row=0, column=0, padx=(25, 25), pady=(25,0))
        self.minXEntry.grid(row=1, column=0, padx=(25, 25), sticky='W')
        self.maxXEntry.grid(row=1, column=0, padx=(25, 25), sticky='E')
        self.stepXLabel.grid(row=2, column=0, padx=(25, 25), pady=(25,0))
        self.stepXEntry.grid(row=3, column=0, padx=(25, 25))
        if self.live:
            self.ejeY1Label.grid(row=0, column=1, padx=(25, 25), pady=(25,0))
            self.minY1Entry.grid(row=1, column=1, padx=(25, 25), sticky='W')
            self.maxY1Entry.grid(row=1, column=1, padx=(25, 25), sticky='E')
            self.stepY1Label.grid(row=2, column=1, padx=(25, 25), pady=(25,0))
            self.stepY1Entry.grid(row=3, column=1, padx=(25, 25))
            self.ejeY2Label.grid(row=0, column=2, padx=(25, 25), pady=(25,0))
            self.minY2Entry.grid(row=1, column=2, padx=(25, 25), sticky='W')
            self.maxY2Entry.grid(row=1, column=2, padx=(25, 25), sticky='E')
            self.stepY2Label.grid(row=2, column=2, padx=(25, 25), pady=(25,0))
            self.stepY2Entry.grid(row=3, column=2, padx=(25, 25))
            self.aceptarButton.grid(row=8, column=0, columnspan=2, padx=(25, 25), pady=(25, 25))
            self.aplicarButton.grid(row=8, column=1, columnspan=2, padx=(0, 25), pady=(25, 25))
        else:
            self.ejeYLabel.grid(row=0, column=1, padx=(25, 25), pady=(25,0))
            self.minYEntry.grid(row=1, column=1, padx=(25, 25), sticky='W')
            self.maxYEntry.grid(row=1, column=1, padx=(25, 25), sticky='E')
            self.stepYLabel.grid(row=2, column=1, padx=(25, 25), pady=(25,0))
            self.stepYEntry.grid(row=3, column=1, padx=(25, 25))
            self.aceptarButton.grid(row=6, column=0, padx=(25, 25), pady=(25,25))
            self.aplicarButton.grid(row=6, column=1, padx=(0, 25), pady=(25,25))

    def guardar_umbral(self, evento, umbral):
        umbral_index = str(evento.widget)[-1:]
        if umbral_index == '3':
            umbral_index = 0
        elif umbral_index == '4':
            umbral_index = 1
        if self.tipo_umbral == 'P':
            self.umbrales_porc[umbral_index] = redondear(float(umbral.get()),0)
        else:
            self.umbrales_val[umbral_index] = redondear(float(umbral.get()),0)

    def aceptar_ajustes(self, tipo_accion):
        minX = self.minXEntry.get()
        maxX = self.maxXEntry.get()
        stepX = self.stepXEntry.get()
        if self.live:
            minY1 = self.minY1Entry.get()
            maxY1 = self.maxY1Entry.get()
            stepY1 = self.stepY1Entry.get()
            minY2 = self.minY2Entry.get()
            maxY2 = self.maxY2Entry.get()
            stepY2 = self.stepY2Entry.get()
            ajustes = {
                "minX": minX,
                "maxX": maxX,
                "stepX": stepX,
                "minY1": minY1,
                "maxY1": maxY1,
                "stepY1": stepY1,
                "minY2": minY2,
                "maxY2": maxY2,
                "stepY2": stepY2
            }
        else:
            minY = self.minYEntry.get()
            maxY = self.maxYEntry.get()
            stepY = self.stepYEntry.get()
            ajustes = {
                "minX": minX,
                "maxX": maxX,
                "stepX": stepX,
                "minY": minY,
                "maxY": maxY,
                "stepY": stepY
            }
        self.main.save_ajustes_grafico(self, ajustes, tipo_accion)

    def set_ajustes(self, ajustes):
        self.minX = float(ajustes["minX"])
        self.maxX = float(ajustes["maxX"])
        self.stepX = float(ajustes["stepX"])
        if self.live:
            self.minY1 = float(ajustes["minY1"])
            self.maxY1 = float(ajustes["maxY1"])
            self.stepY1 = float(ajustes["stepY1"])
            self.minY2 = float(ajustes["minY2"])
            self.maxY2 = float(ajustes["maxY2"])
            self.stepY2 = float(ajustes["stepY2"])
        else:
            self.minY = float(ajustes["minY"])
            self.maxY = float(ajustes["maxY"])
            self.stepY = float(ajustes["stepY"])
