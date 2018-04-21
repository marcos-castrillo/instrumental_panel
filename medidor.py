import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import tkinter.font as tkf

import math
from redondeo import redondear
import random

# Clase Medidor: Engloba cada uno de los medidores
class Medidor(tk.Canvas, object):
    def __init__(self, master, configuracion, **kwargs):
        super(Medidor, self).__init__(master, configuracion=None, **kwargs)
        # Parámetros
        self.titulo = configuracion["nombre"]
        self.unidad = configuracion["unidad"]
        self.ancho = configuracion["ancho"]
        self.altura = configuracion["altura"]
        self.minimo_rango = configuracion["minimo"]
        self.maximo_rango = configuracion["maximo"]
        self.intervalo = configuracion["intervalo"]
        self.color_bajo = configuracion["color_bajo"]
        self.color_medio = configuracion["color_medio"]
        self.color_alto = configuracion["color_alto"]
        self.layoutparams()
        # Se configura el medidor
        self.graphics(self.minimo_rango, self.maximo_rango)
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

    def graphics(self, rango_min, rango_max):
        # create the static components
        self.ovalo = self.create_oval(self.centrex - self.radius
                         , self.centrey - self.radius
                         , self.centrex + self.radius
                         , self.centrey + self.radius
                         , width=self.bezel
                         , outline=self.bezelcolour2)

        self.create_arc(self.centrex - self.radius
                        , self.centrey - self.radius
                        , self.centrex + self.radius
                        , self.centrey + self.radius
                        , width=self.bezel * 1.25
                        , outline="white"
                        , start=242, extent=55)

        self.create_arc(self.centrex - 1.25 * self.radius
                        , self.centrey - 1.25 * self.radius
                        , self.centrex + 1.25 * self.radius
                        , self.centrey + 1.25 * self.radius
                        , width=self.bezel * 1.5
                        , outline="white"
                        , start=242, extent=55)

        self.create_oval(self.centrex - self.radius - 2 * self.bezel
                         , self.centrey - self.radius - 2 * self.bezel
                         , self.centrex + self.radius + 2 * self.bezel
                         , self.centrey + self.radius + 2 * self.bezel
                         , width=self.bezel
                         , outline=self.bezelcolour1)

        for deg in range(-60, 241, 6):
            self.createtick(deg, self.minortick, rango_min, rango_max)
        for deg in range(-60, 241, 30):
            self.createtick(deg, self.majortick, rango_min, rango_max)

    def createhand(self):
        # create text display
        self.maximo = self.create_text(self.centrex * 1.7
                                       , self.centrey * 2.1
                                       , font=tkf.Font(size=-int(3 * self.majortick)))
        self.maximoid = self.create_text(self.centrex * 1.75
                                       , self.centrey * 1.9
                                       , font=tkf.Font(size=int(self.majortick)))
        self.minimo = self.create_text(self.centrex / 2.5
                                        , self.centrey * 2.1
                                        , font=tkf.Font(size=-int(3 * self.majortick)))
        self.minimoid = self.create_text(self.centrex / 3
                                        , self.centrey * 1.9
                                        , font=tkf.Font(size=int(self.majortick)))

        self.unidadid = self.create_text(self.centrex
                                       , self.centrey * 2 - self.centrey*0.3
                                       , font=tkf.Font(size=-int(1.5*self.majortick)))
        self.tituloid = self.create_text(self.centrex
                                       , self.centrey * 2  - self.centrey*0.8
                                       , font=tkf.Font(size=-int(self.majortick)*2))
        # self.descripcionid = self.create_text(self.centrex, self.centrey - self.centrey*0.85, font=tkf.Font(size=-int(self.majortick)))

        # create moving and changeable bits
        self.handid = self.create_line(self.centrex, self.centrey
                                       , self.centrex - self.handlen, self.centrey
                                       , width=2 * self.linewidth
                                       , fill="red")

        self.blobid = self.create_oval(self.centrex - self.blobrad
                                       , self.centrey - self.blobrad
                                       , self.centrex + self.blobrad
                                       , self.centrey + self.blobrad
                                       , outline='black', fill='black')

        self.itemconfigure(self.minimoid, text="Mín", fill='black')
        self.itemconfigure(self.maximoid, text="Máx", fill='black')
        self.itemconfigure(self.unidadid, text=str(self.unidad), fill='black')
        self.itemconfigure(self.tituloid, text=str(self.titulo), fill='black')

    def createtick(self, angle, length, rango_min, rango_max):
        # helper function to create one tick
        rad = math.radians(angle)
        cos = math.cos(rad)
        sin = math.sin(rad)
        radius = self.radius - self.bezel
        if length == self.majortick:
            canvas_id = self.create_text(self.centrex - 0.73 * radius * cos, self.centrey - 0.73 * radius * sin)
            numero = (angle + 60) / 30 * (rango_max - rango_min) / 10
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
        # Se llena el array de últimos valores
        n_promedio = 20
        if len(self.valores_array) < n_promedio:
            self.valores_array.append(valor)
        else:
            self.valores_array.pop(0)
            self.valores_array.append(valor)
        if len(self.valores_array) > 1:
            promedio = sum(self.valores_array) / len(self.valores_array)
        else:
            promedio = sum(self.valores_array)
        promedio = redondear(promedio)
        if len(self.promedios_array) < n_promedio:
            self.promedios_array.append(promedio)
        else:
            self.promedios_array.pop(0)
            self.promedios_array.append(promedio)
        minimo = min(self.promedios_array)
        maximo = max(self.promedios_array)
        # Se asigna el numero al medidor
        if valor < self.maximo_rango / 3:
            color = self.color_bajo
        elif valor > 2 * self.maximo_rango / 3:
            color = self.color_alto
        else:
            color = self.color_medio
        deg = 300 * (valor - self.start) / self.range - 240

        # self.itemconfigure(self.descripcionid, text=str(descripcion), fill='black')
        self.itemconfigure(self.ovalo, outline=color)
        self.itemconfigure(self.minimo, text=str(minimo), fill=color)
        self.itemconfigure(self.maximo, text=str(maximo), fill=color)
        rad = math.radians(deg)
        # reposition hand
        self.coords(self.handid, self.centrex, self.centrey, self.centrex + self.handlen * math.cos(rad),
                    self.centrey + self.handlen * math.sin(rad))