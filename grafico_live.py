# coding=utf-8
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from redondeo import redondear


# Clase Grafico: Engloba cada uno de los graficos
class GraficoLive(tk.Canvas, object):
    def __init__(self, master, configuracion, **kwargs):
        super(GraficoLive, self).__init__(master,configuracion=None, **kwargs)
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
        f = Figure(figsize=(self.altura*3.5, self.ancho), dpi=100)
        self.grafico = f.add_subplot(111)
        self.config_grafico()

        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid()
        f.subplots_adjust(left=0.04, right=0.85, top=0.96, bottom=0.15)

    def set(self, valorX, valorY, cambio_vuelta):
        if cambio_vuelta:
            if len(self.arrayX) == 10:
                self.arrayX.pop(0)
            if len(self.arrayY) == 10:
                self.arrayY.pop(0)
            self.arrayX.append(redondear(valorX, 0))
            self.arrayY.append(redondear(valorY, 0))

            self.grafico.clear()
            self.grafico.plot(self.arrayX,self.arrayY,'ro')
            self.config_grafico()
            self.canvas.draw()

    def config_grafico(self):
        self.grafico.set_title(self.titulo)
        self.grafico.set_xlabel(self.nombreX)
        self.grafico.set_ylabel(self.nombreY)