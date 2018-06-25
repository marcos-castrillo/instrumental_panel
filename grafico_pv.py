# coding=utf-8
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import numpy as np

from redondeo import redondear

class GraficoPV(tk.Canvas, object):
    def __init__(self, master, configuracion, **kwargs):
        super(GraficoPV, self).__init__(master, configuracion=None, **kwargs)
        # Parámetros
        self.titulo = configuracion["titulo"]
        self.color = configuracion["color"]
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
        self.index = configuracion["index"]
        # Inicializar las variables
        self.arrayX = []
        self.arrayY = []
        # Flag para controlar el mostrar u ocultar la ventana de ajustes
        self.flag = False
        self.config_grafico()

    def config_grafico(self):
        # Crear la figura
        f = Figure(figsize=(self.altura, self.ancho), dpi=100)
        # Añadir el subplot a la figura
        self.grafico = f.add_subplot(111)
        # Ajustar la posición del gráfico en el marco
        f.subplots_adjust(left=0.12, right=0.97, bottom=0.15, top=0.9)
        # Parámetros
        self.grafico.set_title(self.titulo)
        self.grafico.set_xlabel(self.nombreX)
        self.grafico.set_ylabel(self.nombreY)
        self.grafico.set_xlim(xmin=self.minX, xmax=self.maxX)
        self.grafico.set_ylim(ymin=self.minY, ymax=self.maxY)
        self.grafico.set_xticks(np.arange(self.minX, self.maxX+1, self.stepX))
        self.grafico.set_yticks(np.arange(self.minY, self.maxY+1, self.stepY))

        # Hacer el plot y guardarlo en self.line
        self.line, = self.grafico.plot(0, 0, self.color, linewidth=1.5, ls="-")
        self.grafico.grid()
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)

    def set(self, valorX, valorY, cambio_vuelta):
        """Actualizar el gráfico"""
        # Guardar los datos
        self.arrayX.append(redondear(valorX, 0))
        self.arrayY.append(redondear(valorY, 0))
        # Si es una nueva vuelta
        if cambio_vuelta and len(self.arrayX) > 1:
            self.line.set_xdata(self.arrayX)
            self.line.set_ydata(self.arrayY)
            self.grafico.fill_between(self.arrayX, self.arrayY, color='gray')
            self.canvas.draw()
            self.canvas.flush_events()
            self.arrayX = []
            self.arrayY = []

    def set_ajustes(self, ajustes):
        """Aplicar los ajustes"""
        self.color = ajustes["color"]
        self.minX = float(ajustes["minX"])
        self.maxX = float(ajustes["maxX"])
        self.stepX = float(ajustes["stepX"])
        self.minY = float(ajustes["minY"])
        self.maxY = float(ajustes["maxY"])
        self.stepY = float(ajustes["stepY"])
        self.config_grafico()
