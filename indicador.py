import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import tkinter.font as tkf

from redondeo import redondear
import random


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
        # Se selecciona el puerto serial a utilizar
        # tasa_baudios = 9600
        # ser = serial.Serial('/dev/ttyACM0', tasa_baudios)
        ser = ""
        msg = [0]
        # (Se genera el primer valor aleatorio)
        self.nuevo_valor(ser, msg)

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

    def set(self, value, color, titulo, unidad):
        self.itemconfigure(self.valorid, text=str(value), fill=color)
        self.itemconfigure(self.unidadid, text=str(unidad), fill='black')
        self.itemconfigure(self.tituloid, text=str(titulo), fill='black')

    def blob(self, colour):
        # call this to change the colour of the blob
        self.itemconfigure(self.blobid, fill=colour, outline=colour)

    # Función para cargar un nuevo valor en la vista
    def nuevo_valor(self, serial, mensaje):
        # Se lee el serial y se convierte
        # valor = str(int(serial.readline(), 16))
        maximo = 100
        # Se utiliza un numero aleatorio dentro del rango
        valor = maximo * float(random.random())
        # Se redondea utiizando la funcion redondeo
        valor = redondear(valor)
        # Se asigna el numero al indicador
        if valor < maximo/3:
            color = self.color_bajo
        elif valor > 2*maximo/3:
            color = self.color_alto
        else:
            color = self.color_medio
        self.set(valor, color, self.titulo, self.unidad)
        # Se calcula un nuevo valor aleatorio cuando termina el intervalo
        self.after(self.intervalo, self.nuevo_valor, serial, mensaje)
