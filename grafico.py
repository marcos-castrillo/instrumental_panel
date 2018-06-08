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

import numpy as np
from scipy.interpolate import spline

from redondeo import redondear


# Clase Grafico: Engloba cada uno de los graficos
class Grafico(tk.Canvas, object):
    def __init__(self, master, configuracion, **kwargs):
        super(Grafico, self).__init__(master,configuracion=None, **kwargs)
        # Parámetros
        self.titulo = configuracion["titulo"]
        self.nombreX = configuracion["nombreX"]
        self.minX = float(configuracion["minX"])
        self.maxX = float(configuracion["maxX"])
        self.stepX = float(configuracion["stepX"])
        self.nombreY = configuracion["nombreY"]
        self.minY = float(configuracion["minY"])
        self.maxY = float(configuracion["maxY"])
        self.stepY = float(configuracion["stepY"])
        self.ancho = int(self['width'])
        self.altura = int(self['height'])
        self.arrayX = []
        self.arrayY = []
        self.config_grafico()

    def set(self, valorX, valorY, cambio_vuelta):
        self.arrayX.append(redondear(valorX, 0))
        self.arrayY.append(redondear(valorY, 0))
        if cambio_vuelta and len(self.arrayX) > 1:
            self.line.set_xdata(self.arrayX)
            self.line.set_ydata(self.arrayY)
            self.canvas.draw()
            self.canvas.flush_events()
            self.arrayX = []
            self.arrayY = []

    def config_grafico(self):
        f = Figure(figsize=(self.altura, self.ancho), dpi=100)
        self.grafico = f.add_subplot(111)
        self.line, = self.grafico.plot(0, 0, 'red', linewidth=1)
        f.subplots_adjust(left=0.12, right=0.97, bottom=0.15, top=0.9)
        self.grafico.set_title(self.titulo)
        self.grafico.set_xlabel(self.nombreX)
        self.grafico.set_ylabel(self.nombreY)
        self.grafico.set_xlim(xmin=self.minX, xmax=self.maxX)
        self.grafico.set_ylim(ymin=self.minY, ymax=self.maxY)
        self.grafico.set_xticks(np.arange(self.minX, self.maxX+1, self.stepX))
        self.grafico.set_yticks(np.arange(self.minY, self.maxY+1, self.stepY))
        self.grafico.grid()
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)

    def set_ajustes(self, ajustes):
        self.minX = float(ajustes["minX"])
        self.maxX = float(ajustes["maxX"])
        self.stepX = float(ajustes["stepX"])
        self.minY = float(ajustes["minY"])
        self.maxY = float(ajustes["maxY"])
        self.stepY = float(ajustes["stepY"])
        self.config_grafico()
