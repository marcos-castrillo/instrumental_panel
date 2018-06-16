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
from scipy.interpolate import spline

from redondeo import redondear


# Clase Grafico: Engloba cada uno de los graficos
class GraficoLive(tk.Canvas, object):
    def __init__(self, master, configuracion, **kwargs):
        super(GraficoLive, self).__init__(master, configuracion=None, **kwargs)
        # Parámetros
        self.titulo = configuracion["titulo"]
        self.color0 = configuracion["color0"]
        self.color1 = configuracion["color1"]
        self.nombreX = configuracion["nombreX"]
        self.minX = float(configuracion["minX"])
        self.maxX = float(configuracion["maxX"])
        self.stepX = float(configuracion["stepX"])
        self.nombreY = configuracion["nombreY1"]
        self.minY1 = float(configuracion["minY1"])
        self.maxY1 = float(configuracion["maxY1"])
        self.stepY1 = float(configuracion["stepY1"])
        self.nombreY2 = configuracion["nombreY2"]
        self.minY2 = float(configuracion["minY2"])
        self.maxY2 = float(configuracion["maxY2"])
        self.stepY2 = float(configuracion["stepY2"])
        self.ancho = int(self['width'])
        self.altura = int(self['height'])
        self.n_lineas = int(configuracion["n_lineas"])
        self.arrayX = []
        self.arrayY = []
        self.arrayY2 = []
        self.listaX = []
        self.listaY = []
        self.listaY2 = []
        self.line = []
        self.line2 = []
        self.config_grafico()

    def set(self, valorX, valorY, valorY2, cambio_vuelta):
        self.arrayX.append(redondear(valorX, 0))
        self.arrayY.append(redondear(valorY, 0))
        self.arrayY2.append(redondear(valorY2, 0))
        if cambio_vuelta and len(self.arrayX) >= 1:
            a, = self.grafico.plot(self.arrayX, self.arrayY, self.color0, linewidth=1.5)
            a2, = self.second_axis.plot(self.arrayX, self.arrayY2, self.color1, linewidth=1.5)
            self.line.append(a)
            self.line2.append(a2)
            self.canvas.draw()
            self.canvas.flush_events()
            self.listaX.append(self.arrayX)
            self.listaY.append(self.arrayY)
            self.listaY2.append(self.arrayY2)
            n_lineas = len(self.listaX)
            if n_lineas - 1 > 0:
                self.line[n_lineas-1].set_color(self.color0)
                self.line[n_lineas-1].set_linewidth(0.5)
                self.line2[n_lineas-1].set_color(self.color1)
            self.line2[n_lineas - 1].set_linewidth(0.5)
            if n_lineas >= self.n_lineas:
                self.listaX.pop(0)
                self.listaY.pop(0)
                self.listaY2.pop(0)
                if len(self.line) > 0:
                    erase = self.line.pop(0)
                    erase.remove()
                if len(self.line2) > 0:
                    erase = self.line2.pop(0)
                    erase.remove()
            self.arrayX = []
            self.arrayY = []
            self.arrayY2 = []

    def config_grafico(self):
        f = Figure(figsize=(self.altura, self.ancho), dpi=100)
        self.grafico = f.add_subplot(111)
        self.second_axis = self.grafico.twinx()
        f.subplots_adjust(left=0.06, right=0.94, bottom=0.12, top=0.92)
        self.grafico.set_title(self.titulo)
        self.grafico.set_xlabel(self.nombreX)
        self.grafico.set_ylabel(self.nombreY)
        self.second_axis.set_ylabel(self.nombreY2)
        a = self.grafico.plot(self.arrayX, self.arrayY, self.color0, linewidth=1, label='Presión')
        a2 = self.second_axis.plot(self.arrayX, self.arrayY2, self.color1, linewidth=1, label='Par')
        self.grafico.set_xlim(xmin=self.minX, xmax=self.maxX)
        self.grafico.set_ylim(ymin=self.minY1, ymax=self.maxY1)
        self.second_axis.set_ylim(ymin=self.minY2, ymax=self.maxY2)
        self.grafico.set_xticks(np.arange(self.minX, self.maxX+1, self.stepX))
        self.grafico.set_yticks(np.arange(self.minY1, self.maxY1+1, self.stepY1))
        self.second_axis.set_yticks(np.arange(self.minY2, self.maxY2+1, self.stepY2))
        lines = a + a2
        labs = [l.get_label() for l in lines]
        self.grafico.legend(lines, labs, loc='lower right')
        self.grafico.grid()
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid()

    def set_ajustes(self, ajustes):
        self.color0 = ajustes["color0"]
        self.color1 = ajustes["color1"]
        self.minX = float(ajustes["minX"])
        self.maxX = float(ajustes["maxX"])
        self.stepX = float(ajustes["stepX"])
        self.minY1 = float(ajustes["minY1"])
        self.maxY1 = float(ajustes["maxY1"])
        self.stepY1 = float(ajustes["stepY1"])
        self.minY2 = float(ajustes["minY2"])
        self.maxY2 = float(ajustes["maxY2"])
        self.stepY2 = float(ajustes["stepY2"])
        n_lineas = int(ajustes["n_lineas"])
        # Ajustar el número de líneas
        if self.n_lineas != n_lineas:
            self.n_lineas = n_lineas
            i = n_lineas
            while i <= len(self.line):
                erase = self.line.pop(0)
                erase.remove()
                erase = self.line2.pop(0)
                erase.remove()
            self.arrayX = []
            self.arrayY = []
            self.arrayY2 = []
            self.listaX = []
            self.listaY = []
            self.listaY2 = []
        self.canvas.get_tk_widget().destroy()
        self.config_grafico()