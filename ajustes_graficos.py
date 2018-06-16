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
            self.color0 = configuracion["color0"]
            self.color1 = configuracion["color1"]
            self.minY1 = configuracion["minY1"]
            self.maxY1 = configuracion["maxY1"]
            self.stepY1 = configuracion["stepY1"]
            self.minY2 = configuracion["minY2"]
            self.maxY2 = configuracion["maxY2"]
            self.stepY2 = configuracion["stepY2"]
            self.n_lineas = configuracion["n_lineas"]
        else:
            self.color = configuracion["color"]
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
            self.lineasLabel = tk.Label(master, text="Vueltas representadas simultáneamente", bg='white', font='Helvetica 10 bold', wraplength='150')
            self.lineasEntry = tk.Entry(master, bd=5, width="5")
            self.lineasEntry.insert(0, str(self.n_lineas))
            self.colorButton0 = tk.Button(master, width="18", command=lambda: self.set_color(self.colorButton0))
            self.colorButton0.config(font='Helvetica 9 bold', text="Color de línea 1", bg=self.color0)
            self.colorButton1 = tk.Button(master, width="18", command=lambda: self.set_color(self.colorButton1))
            self.colorButton1.config(font='Helvetica 9 bold', text="Color de línea 2", bg=self.color1)
        else:
            self.colorButton = tk.Button(master, width="18", command=lambda: self.set_color(self.colorButton))
            self.colorButton.config(font='Helvetica 9 bold', text="Color de línea", bg=self.color)
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
        self.cancelarButton = tk.Button(master, text='Cancelar', width=10,command= self.cancelar_ajustes)
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
            self.lineasLabel.grid(row=4, column=0, pady=(25, 0))
            self.lineasEntry.grid(row=5, column=0)
            self.colorButton0.grid(row=4, column=1, pady=(25, 0))
            self.colorButton1.grid(row=5, column=1)
            self.aceptarButton.grid(row=8, column=0, padx=(25, 25), pady=(25, 25))
            self.aplicarButton.grid(row=8, column=1, padx=(0, 25), pady=(25, 25))
            self.cancelarButton.grid(row=8, column=2, padx=(0, 25), pady=(25, 25))
        else:
            self.ejeYLabel.grid(row=0, column=1, padx=(25, 25), pady=(25,0))
            self.minYEntry.grid(row=1, column=1, padx=(25, 25), sticky='W')
            self.maxYEntry.grid(row=1, column=1, padx=(25, 25), sticky='E')
            self.stepYLabel.grid(row=2, column=1, padx=(25, 25), pady=(25,0))
            self.stepYEntry.grid(row=3, column=1, padx=(25, 25))
            self.colorButton.grid(row=4, column=0, columnspan=2, pady=(25, 0))
            self.aceptarButton.grid(row=6, column=0, padx=(25, 25), pady=(25,25), sticky="W")
            self.aplicarButton.grid(row=6, column=0, columnspan=2, padx=(25, 25), pady=(25,25))
            self.cancelarButton.grid(row=6, column=1, padx=(0, 25), pady=(25,25), sticky="E")

    def set_color(self, widget):
        button_index = str(widget)[-1:]
        if button_index == 'n':
            button_index = 1
        button_index = int(button_index)-1
        if self.live:
            if button_index == 0:
                color = askcolor(initialcolor = self.color0)
                widget.config(font='Helvetica 9 bold', text="Color de línea 1", bg=color[1])
                self.color0 = color[1]
            elif button_index == 1:
                color = askcolor(initialcolor = self.color1)
                widget.config(font='Helvetica 9 bold', text="Color de línea 0", bg=color[1])
                self.color1 = color[1]
        else:
            color = askcolor(initialcolor=self.color)
            widget.config(font='Helvetica 9 bold', text="Color de línea", bg=color[1])
            self.color = color[1]
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
        minX = redondear(float(self.minXEntry.get()), float(self.maxXEntry.get()))
        maxX = redondear(float(self.maxXEntry.get()), float(self.maxXEntry.get()))
        stepX = redondear(float(self.stepXEntry.get()), 0)
        if self.live:
            color0 = self.colorButton0.cget('background')
            color1 = self.colorButton1.cget('background')
            minY1 = redondear(float(self.minY1Entry.get()), float(self.maxY1Entry.get()))
            maxY1 =redondear(float( self.maxY1Entry.get()), float(self.maxY1Entry.get()))
            stepY1 = redondear(float(self.stepY1Entry.get()), 0)
            minY2 = redondear(float(self.minY2Entry.get()), float(self.maxY2Entry.get()))
            maxY2 = redondear(float(self.maxY2Entry.get()), float(self.maxY2Entry.get()))
            stepY2 = redondear(float(self.stepY2Entry.get()), 0)
            n_lineas = self.lineasEntry.get()
            if not float(n_lineas).is_integer():
                n_lineas = int(float(n_lineas))
                self.lineasEntry.delete(0, 'end')
                self.lineasEntry.insert(0, str(n_lineas))
            ajustes = {
                "color0": color0,
                "color1": color1,
                "minX": minX,
                "maxX": maxX,
                "stepX": stepX,
                "minY1": minY1,
                "maxY1": maxY1,
                "stepY1": stepY1,
                "minY2": minY2,
                "maxY2": maxY2,
                "stepY2": stepY2,
                "n_lineas": n_lineas
            }
        else:
            color = self.colorButton.cget('background')
            minY = redondear(float(self.minYEntry.get()), float(self.maxYEntry.get()))
            maxY = redondear(float(self.maxYEntry.get()), float(self.maxYEntry.get()))
            stepY = redondear(float(self.stepYEntry.get()), 0)
            ajustes = {
                "color": color,
                "minX": minX,
                "maxX": maxX,
                "stepX": stepX,
                "minY": minY,
                "maxY": maxY,
                "stepY": stepY
            }
        self.main.save_ajustes_grafico(self, ajustes, tipo_accion)

    def cancelar_ajustes(self):
        self.minXEntry.delete(0, 'end')
        self.minXEntry.insert(0, self.minX)
        self.maxXEntry.delete(0, 'end')
        self.maxXEntry.insert(0, self.maxX)
        self.stepXEntry.delete(0, 'end')
        self.stepXEntry.insert(0, self.stepX)
        if self.live:
            self.minY1Entry.delete(0, 'end')
            self.minY1Entry.insert(0, self.minY1)
            self.maxY1Entry.delete(0, 'end')
            self.maxY1Entry.insert(0, self.maxY1)
            self.stepY1Entry.delete(0, 'end')
            self.stepY1Entry.insert(0, self.stepY1)
            self.minY2Entry.delete(0, 'end')
            self.minY2Entry.insert(0, self.minY2)
            self.maxY2Entry.delete(0, 'end')
            self.maxY2Entry.insert(0, self.maxY2)
            self.stepY2Entry.delete(0, 'end')
            self.stepY2Entry.insert(0, self.stepY2)
            self.lineasEntry.delete(0, 'end')
            self.lineasEntry.insert(0, str(self.n_lineas))
        else:
            self.minYEntry.delete(0, 'end')
            self.minYEntry.insert(0, self.minY)
            self.maxYEntry.delete(0, 'end')
            self.maxYEntry.insert(0, self.maxY)
            self.stepYEntry.delete(0, 'end')
            self.stepYEntry.insert(0, self.stepY)
        self.main.desplegar_ajustes(self.master)

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
            self.n_lineas = int(ajustes["stepY2"])
        else:
            self.minY = float(ajustes["minY"])
            self.maxY = float(ajustes["maxY"])
            self.stepY = float(ajustes["stepY"])
