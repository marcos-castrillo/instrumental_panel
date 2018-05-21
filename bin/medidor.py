import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import tkinter.font as tkf

import math
from bin.redondeo import redondear

# Clase Medidor: Engloba cada uno de los medidores
class Medidor(tk.Canvas, object):
    def __init__(self, master, configuracion, **kwargs):
        super(Medidor, self).__init__(master, configuracion=None, **kwargs)
        self.master = master
        # Parámetros
        self.titulo = configuracion["nombre"]
        self.unidad = configuracion["unidad"]
        self.ancho = int(self['width'])
        self.altura = int(self['height'])
        self.minimo_rango = configuracion["minimo"]
        self.maximo_rango = configuracion["maximo"]
        self.umbrales_porc = configuracion["umbrales_porc"]
        self.umbrales_val = configuracion["umbrales_val"]
        self.tipo_umbral = configuracion["tipo_umbral"]
        self.colores = configuracion["colores"]
        self.n_colores = len(self.colores)
        # Se configura el medidor
        self.layoutparams()
        self.graphics(self.minimo_rango, self.maximo_rango)
        self.createhand()
        self.setrange(self.minimo_rango, self.maximo_rango)
        self.valores_array = []
        self.vuelta_actual = 0
        self.color = 'black'
        self.deg = 0

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
                                       , self.centrey * 2  - self.centrey*0.7
                                       , font=tkf.Font(size=-int(self.majortick*1.5)),width='150', justify='center')

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
            numero = rango_min + (angle + 60) / 30 * (rango_max - rango_min) / 10
            numero2 = redondear(numero)
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

    def set(self, valor, cambio_vuelta):
        try:
            self.valor_min
        except AttributeError:
            self.valor_min = valor
            self.valor_max = valor
        # Se llena el array de últimos valores
        if len(self.valores_array) < 360:
            self.valores_array.append(valor)
        else:
            self.valores_array.pop(0)
            self.valores_array.append(valor)
        # Se comprueban el máximo y minimo
        if valor < self.valor_min:
            self.valor_min = valor
        if valor > self.valor_max:
            self.valor_max = valor
        if cambio_vuelta:
            self.vuelta_actual += 1
            promedio = redondear(sum(self.valores_array) / len(self.valores_array))
            # Se asigna el número al medidor
            if self.tipo_umbral == "P":
                porcentaje = promedio/(self.minimo_rango + self.maximo_rango)
                if porcentaje < float(self.umbrales_porc[0]):
                    self.color = self.colores[0]
                elif float(self.umbrales_porc[0]) <= porcentaje < float(self.umbrales_porc[1]):
                    self.color = self.colores[1]
                else:
                    self.color = self.colores[2]
            else:
                if promedio < self.umbrales_val[0]:
                    self.color = self.colores[0]
                elif self.umbrales_val[0] <= promedio < self.umbrales_val[1]:
                    self.color = self.colores[1]
                else:
                    self.color = self.colores[2]
            if promedio <= self.minimo_rango:
                self.deg = 120
            elif promedio >= self.maximo_rango:
                self.deg = 60
            else:
                self.deg = 300 * (promedio - self.start) / self.range - 240
            self.itemconfigure(self.ovalo, outline=self.color)
            # reposition hand
            rad = math.radians(self.deg)
            self.coords(self.handid, self.centrex, self.centrey, self.centrex + self.handlen * math.cos(rad),
                        self.centrey + self.handlen * math.sin(rad))
        if valor == self.valor_min:
            self.itemconfigure(self.minimo, text=str(redondear(self.valor_min)), fill=self.color)
        else:
            self.itemconfigure(self.minimo, text=str(redondear(self.valor_min)), fill='black')
        if valor == self.valor_max:
            self.itemconfigure(self.maximo, text=str(redondear(self.valor_max)), fill=self.color)
        else:
            self.itemconfigure(self.maximo, text=str(redondear(self.valor_max)), fill='black')


    def set_ajustes(self, ajustes):
        self.colores = ajustes['colores']
        self.minimo_rango = float(ajustes['minimo'])
        self.maximo_rango = float(ajustes['maximo'])
        umbrales_porc_str = ajustes['umbrales_porc']
        umbrales_porc = [float(numeric_string) for numeric_string in umbrales_porc_str]
        self.umbrales_porc = umbrales_porc
        umbrales_val_str = ajustes['umbrales_porc']
        umbrales_val = [float(numeric_string) for numeric_string in umbrales_val_str]
        self.umbrales_val = umbrales_val
        self.tipo_umbral = ajustes['tipo_umbral']
        self.delete("all")
        self.layoutparams()
        self.graphics(self.minimo_rango, self.maximo_rango)
        self.createhand()
        self.setrange(self.minimo_rango, self.maximo_rango)
