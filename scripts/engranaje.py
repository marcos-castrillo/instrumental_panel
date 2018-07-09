# coding=utf-8
import sys
import tkinter as tk
import tkinter.font as tkf

import math

class Engranaje(tk.Canvas, object):
    def __init__(self, master, configuracion, **kwargs):
        super(Engranaje, self).__init__(master, configuracion=None, **kwargs)
        # Parámetros
        self.master = master
        self.titulo = configuracion["nombre"]
        self.ancho = int(self['width'])
        self.altura = int(self['height'])
        self.minimo_rango = configuracion["minimo"]
        self.maximo_rango = configuracion["maximo"]
        self.unidad = configuracion["unidad"]
        # Inicializar las variables
        self.promedios_array = []
        self.valores_array = []
        # Crear el engranaje
        self.crear_estructura(self.altura, self.ancho)
        self.crear_interfaz()
        self.set_rango(self.minimo_rango, self.maximo_rango)

    def crear_estructura(self, altura, ancho):
        # Marco del engranaje
        if altura * 2 > ancho:
            lado = ancho
        else:
            lado = altura * 2
        # Ejes
        self.centroX = lado / 2
        self.centroY = lado / 2
        # Ancho de las líneas
        self.linewidth = 2
        # Radio externo del disco
        self.radio = int(0.40 * float(lado))
        # Bisel
        self.bisel = self.radio / 20
        self.color_bisel_1 = '#000000'
        self.color_bisel_2 = '#808080'
        # Longitud de los ticks y la aguja
        self.tick_gran = self.radio / 8
        self.tick_peq = self.tick_gran / 2
        self.largo_aguja = self.radio - self.tick_gran - self.bisel - 1
        self.radio_circulo_interno = self.largo_aguja / 6

    def crear_interfaz(self):
        # Elementos estáticos
        self.rueda = tk.PhotoImage(file='images/gear.png')
        self.create_image(self.centroX, self.centroY, image=self.rueda)

        self.tituloid = self.create_text(self.centroX
                                       , self.centroY * 1.22
                                       , font=tkf.Font(size=-int(self.tick_gran*1.25)),width='100', justify='center')

        self.valor = self.create_text(self.centroX
                                        , self.centroY * 2.1
                                        , font=tkf.Font(size=-int(3 * self.tick_gran)))

        self.handid = self.create_line(self.centroX, self.centroY
                                       , self.centroX - self.largo_aguja, self.centroY
                                       , width=2 * self.linewidth
                                       , fill="red")

        self.blobid = self.create_oval(self.centroX - self.radio_circulo_interno
                                       , self.centroY - self.radio_circulo_interno
                                       , self.centroX + self.radio_circulo_interno
                                       , self.centroY + self.radio_circulo_interno
                                       , outline='black', fill='black')
        # Configurar estado inicial de los elementos
        self.itemconfigure(self.tituloid, text=str(self.titulo), fill='black')

    def crear_tick(self, angulo, longitud, rango_min, rango_max):
        rad = math.radians(angulo)
        cos = math.cos(rad)
        sin = math.sin(rad)
        radio = self.radio - self.bisel
        if longitud == self.tick_gran:
            canvas_id = self.create_text(self.centroX - 0.73 * radio * cos, self.centroY - 0.73 * radio * sin)
            numero = rango_min + (angulo + 60) / 30 * (rango_max - rango_min) / 10
            if numero.is_integer():
                numero = int(numero)
            self.itemconfig(canvas_id, text=str(numero), font=tkf.Font(size=int(1.5 * self.tick_peq)))
        self.create_line(self.centroX - radio * cos
                         , self.centroY - radio * sin
                         , self.centroX - (radio - longitud) * cos
                         , self.centroY - (radio - longitud) * sin
                         , width=self.linewidth)

    def set_rango(self, start=0, end=100):
        self.start = start
        self.range = end - start

    def set(self, valor):
        """Actualiza el engranaje con los datos pasados por parámetro"""
        deg = 360 * (valor - self.start) / self.range - 270
        rad = math.radians(deg)
        # Aguja
        self.coords(self.handid, self.centroX, self.centroY, self.centroX + self.largo_aguja * math.cos(rad),
                    self.centroY + self.largo_aguja * math.sin(rad))
        # Texto
        self.itemconfigure(self.valor, text=str(valor) + self.unidad)


