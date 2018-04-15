import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from numpy import arange, sin, pi
from matplotlib.figure import Figure

import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

# Clase Grafico: Engloba cada uno de los graficos
class Grafico(tk.Canvas, object):
    def __init__(self, master, configuracion, **kwargs):
        super(Grafico, self).__init__(master,configuracion=None, **kwargs)
        # Parámetros
        if hasattr(configuracion, 'titulo'):
            self.titulo = configuracion["titulo"]
        self.nombreX = configuracion["nombreX"]
        self.nombreY = configuracion["nombreY"]
        self.ancho = configuracion["ancho"]
        self.altura = configuracion["altura"]
        self.intervalo = configuracion["intervalo"]

        # 1 inch = 96 pixels
        f = Figure(figsize=(self.altura/96, self.ancho/96), dpi=100)
        a = f.add_subplot(111)
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)

        a.plot(t, s)
        if hasattr(configuracion, 'titulo'):
            a.set_title(self.titulo)
        a.set_xlabel(self.nombreX)
        a.set_ylabel(self.nombreY)

        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(f, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid()
