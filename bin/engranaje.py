import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import tkinter.font as tkf

import math
from bin.redondeo import redondear

# Clase Medidor: Engloba cada uno de los medidores
class Engranaje(tk.Canvas, object):
    def __init__(self, master, configuracion, **kwargs):
        super(Engranaje, self).__init__(master, configuracion=None, **kwargs)
        self.master = master
        # Parámetros
        self.titulo = configuracion["nombre"]
        self.ancho = int(self['width'])
        self.altura = int(self['height'])
        self.minimo_rango = configuracion["minimo"]
        self.maximo_rango = configuracion["maximo"]
        self.unidad = configuracion["unidad"]
        # Se configura el medidor
        self.layoutparams()
        self.graphics()
        self.createhand()
        self.setrange(self.minimo_rango, self.maximo_rango)
        self.promedios_array = []
        self.valores_array = []

    def layoutparams(self):
        # find a square that fits in the window
        if self.altura * 2 > self.ancho:
            side = self.ancho
        else:
            side = self.altura * 2

        # set axis for hand
        self.centrex = side / 2
        self.centrey = side / 2

        # standard with of lines
        self.linewidth = 2

        # outer radius for dial
        self.radius = int(0.40 * float(side))

        # set width of bezel
        self.bezel = self.radius / 20
        self.bezelcolour1 = '#000000'
        self.bezelcolour2 = '#808080'

        # set lengths of ticks and hand
        self.majortick = self.radius / 8
        self.minortick = self.majortick / 2
        self.handlen = self.radius - self.majortick - self.bezel - 1
        self.blobrad = self.handlen / 6

    def graphics(self):
        # create the static components
        self.rueda = tk.PhotoImage(file='images/gear.png')

        # put gif image on canvas
        # pic's upper left corner (NW) on the canvas is at x=50 y=10
        self.create_image(self.centrex,self.centrey,image=self.rueda)



    def createhand(self):

        self.tituloid = self.create_text(self.centrex
                                       , self.centrey * 2  - self.centrey*0.7
                                       , font=tkf.Font(size=-int(self.majortick*1.5)),width='100', justify='center')

        self.valor = self.create_text(self.centrex
                                        , self.centrey * 2.1
                                        , font=tkf.Font(size=-int(3 * self.majortick)))

        self.handid = self.create_line(self.centrex, self.centrey
                                       , self.centrex - self.handlen, self.centrey
                                       , width=2 * self.linewidth
                                       , fill="red")

        self.blobid = self.create_oval(self.centrex - self.blobrad
                                       , self.centrey - self.blobrad
                                       , self.centrex + self.blobrad
                                       , self.centrey + self.blobrad
                                       , outline='black', fill='black')

        self.itemconfigure(self.tituloid, text=str(self.titulo), fill='black')

    def createtick(self, angle, length, rango_min, rango_max):
        # helper function to create one tick
        rad = math.radians(angle)
        cos = math.cos(rad)
        sin = math.sin(rad)
        radius = self.radius - self.bezel
        if length == self.majortick:
            canvas_id = self.create_text(self.centrex - 0.73 * radius * cos, self.centrey - 0.73 * radius * sin)
            numero = rango_min + (angle + 60) / 30 * (rango_max - rango_min) / 10
            if numero.is_integer():
                numero = int(numero)
            self.itemconfig(canvas_id, text=str(numero), font=tkf.Font(size=int(1.5 * self.minortick)))
        self.create_line(self.centrex - radius * cos
                         , self.centrey - radius * sin
                         , self.centrex - (radius - length) * cos
                         , self.centrey - (radius - length) * sin
                         , width=self.linewidth)

    def setrange(self, start=0, end=100):
        self.start = start
        self.range = end - start

    def set(self, valor):
        # Se asigna el número al medidor
        deg = 360 * (valor - self.start) / self.range - 270

        rad = math.radians(deg)
        # reposition hand
        self.coords(self.handid, self.centrex, self.centrey, self.centrex + self.handlen * math.cos(rad),
                    self.centrey + self.handlen * math.sin(rad))

        self.itemconfigure(self.valor, text=str(valor) + self.unidad)


