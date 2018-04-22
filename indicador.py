import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import tkinter.font as tkf

from redondeo import redondear


# Clase Indicador: Engloba cada uno de los indicadores
class Indicador(tk.Canvas, object):
    def __init__(self, master,configuracion, **kwargs):
        super(Indicador, self).__init__(master, configuracion=None, **kwargs)
        # Parámetros
        self.titulo = configuracion["nombre"]
        self.unidad = configuracion["unidad"]
        self.ancho = configuracion["ancho"]
        self.altura = configuracion["altura"]
        self.intervalo = configuracion["intervalo"]
        self.color_bajo = configuracion["color_bajo"]
        self.color_medio = configuracion["color_medio"]
        self.color_alto = configuracion["color_alto"]
        # Se configura el indicador
        self.layoutparams(self.altura, self.ancho)
        self.createhand(self.altura, self.ancho)

    def layoutparams(self, altura, ancho):
        # find a square that fits in the window
        if altura * 2 > ancho:
            self.side = ancho
        else:
            self.side = altura * 2

        # set axis for hand
        self.centrex = self.side / 2
        self.centrey = self.side / 2


    def createhand(self,altura, ancho):
        # create text display
        self.tituloid = self.create_text(self.centrex
                                       ,  self.centrey - self.centrey*0.8
                                       , font=tkf.Font(size=-int(self.side/7),weight="bold"))
        self.valorid = self.create_text(self.centrex
                                       , self.centrey/1.5
                                       , font=tkf.Font(size=-int(self.side/4)))
        self.unidadid = self.create_text(self.centrex
                                       , self.centrey
                                       , font=tkf.Font(size=-int(self.side/10)))
        self.itemconfigure(self.unidadid, text=str(self.unidad), fill='black')
        self.itemconfigure(self.tituloid, text=str(self.titulo), fill='black')

    def set(self, valor):
        valor = redondear(valor)
        self.itemconfigure(self.valorid, text=str(valor))


