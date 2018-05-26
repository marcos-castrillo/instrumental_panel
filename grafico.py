# coding=utf-8
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from redondeo import redondear


# Clase Grafico: Engloba cada uno de los graficos
class Grafico(tk.Canvas, object):
    def __init__(self, master, configuracion, **kwargs):
        super(Grafico, self).__init__(master,configuracion=None, **kwargs)
        # Parámetros
        if hasattr(configuracion, 'titulo'):
            self.titulo = configuracion["titulo"]
        else:
            self.titulo = ""
        self.nombreX = configuracion["nombreX"]
        self.nombreY = configuracion["nombreY"]
        self.ancho = int(self['width'])
        self.altura = int(self['height'])
        self.arrayX = []
        self.arrayY = []

        # 1 inch = 96 pixels
        self.container = tk.Frame(self)
        self.container.grid()

        f = Figure(figsize=(self.altura*1.5, self.ancho), dpi=100)
        self.grafico = f.add_subplot(111)
        self.config_grafico()

        self.canvas = FigureCanvasTkAgg(f, master=self.container)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)

    def set(self, valorX, valorY, cambio_vuelta):
        if cambio_vuelta:
            if len(self.arrayX) == 10:
                self.arrayX.pop(0)
            if len(self.arrayY) == 10:
                self.arrayY.pop(0)
            self.arrayX.append(redondear(valorX, 0))
            self.arrayY.append(redondear(valorY, 0))

            self.grafico.clear()
            self.grafico.plot(self.arrayX,self.arrayY, linestyle='--', marker='o', color='b')
            self.config_grafico()
            self.canvas.draw()

    def config_grafico(self):
        self.grafico.set_title(self.titulo)
        self.grafico.set_xlabel(self.nombreX)
        self.grafico.set_ylabel(self.nombreY)
        self.grafico.set_xlim(xmin=0, xmax=1)
        self.grafico.set_ylim(ymin=0, ymax=1)
