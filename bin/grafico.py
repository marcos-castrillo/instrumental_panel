import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from numpy import arange, sin, pi, random
from matplotlib.figure import Figure

import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

from bin.redondeo import redondear

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
        self.punto_anterior = 'a','a'

        # 1 inch = 96 pixels
        f = Figure(figsize=(self.altura/96, self.ancho/96), dpi=100)

        self.grafico = f.add_subplot(111)
        self.config_grafico()

        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(f, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid()

    def set(self, valorX, valorY, cambio_vuelta):
        if cambio_vuelta:
            valorX = redondear(valorX)
            valorY= redondear(valorY)
            self.dibujar_grafico(valorX, valorY)

    def config_grafico(self):
        self.grafico.set_title(self.titulo)
        self.grafico.set_xlabel(self.nombreX)
        self.grafico.set_ylabel(self.nombreY)

    def dibujar_grafico(self, x , y):
        punto = x, y
        if self.punto_anterior != ('a','a'):
            for i in range(0, len(punto), 2):
                self.grafico.plot(self.punto_anterior[i:i + 2], punto[i:i + 2], 'ro-')
        else:
            self.grafico.plot(punto, 'ro')
        self.punto_anterior = punto