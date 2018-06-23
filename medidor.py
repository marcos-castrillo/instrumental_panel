# coding=utf-8
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import tkinter.font as tkf

import json
import math
from redondeo import redondear

class Medidor(tk.Canvas, object):
    def __init__(self, master, configuracion, **kwargs):
        super(Medidor, self).__init__(master, configuracion=None, **kwargs)
        # Parámetros
        self.master = master
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
        self.index = configuracion["index"]
        # Inicializar las variables
        self.n_colores = len(self.colores)
        self.valor_min = ''
        self.valor_max = ''
        self.vuelta_actual = 0
        self.color = 'black'
        self.deg = 0
        self.deg_anterior = 0
        # Flag para controlar el mostrar u ocultar la ventana de ajustes
        self.flag = False
        # Crear el medidor
        self.crear_estructura(self.altura, self.ancho)
        self.crear_interfaz(self.minimo_rango, self.maximo_rango)
        self.set_rango(self.minimo_rango, self.maximo_rango)

    def crear_estructura(self, altura, ancho):
        # Marco del medidor
        if altura * 2 > ancho:
            lado = self.ancho
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

    def crear_interfaz(self, rango_min, rango_max):
        # Elementos estáticos
        self.ovalo = self.create_oval(self.centroX - self.radio
                         , self.centroY - self.radio
                         , self.centroX + self.radio
                         , self.centroY + self.radio
                         , width=self.bisel
                         , outline=self.color_bisel_2)

        self.create_arc(self.centroX - self.radio
                        , self.centroY - self.radio
                        , self.centroX + self.radio
                        , self.centroY + self.radio
                        , width=self.bisel * 1.25
                        , outline="white"
                        , start=242, extent=55)

        self.create_arc(self.centroX - 1.25 * self.radio
                        , self.centroY - 1.25 * self.radio
                        , self.centroX + 1.25 * self.radio
                        , self.centroY + 1.25 * self.radio
                        , width=self.bisel * 1.5
                        , outline="white"
                        , start=242, extent=55)

        self.create_oval(self.centroX - self.radio - 2 * self.bisel
                         , self.centroY - self.radio - 2 * self.bisel
                         , self.centroX + self.radio + 2 * self.bisel
                         , self.centroY + self.radio + 2 * self.bisel
                         , width=self.bisel
                         , outline=self.color_bisel_1)
        
        self.create_oval(self.centroX - self.radio_circulo_interno
                                       , self.centroY - self.radio_circulo_interno
                                       , self.centroX + self.radio_circulo_interno
                                       , self.centroY + self.radio_circulo_interno
                                       , outline='black', fill='black')
        # Elementos dinámicos
        self.aguja = self.create_line(self.centroX, self.centroY
                                       , self.centroX - self.largo_aguja, self.centroY
                                       , width=2 * self.linewidth
                                       , fill="red")
        # Ticks
        for deg in range(-60, 241, 6):
            self.crear_tick(deg, self.tick_peq, rango_min, rango_max)
        for deg in range(-60, 241, 30):
            self.crear_tick(deg, self.tick_gran, rango_min, rango_max)
        # Texto
        self.maximo = self.create_text(self.centroX * 1.5
                                       , self.centroY * 2.1
                                       , font=tkf.Font(size=-int(2.5 * self.tick_gran)))
        self.maximoid = self.create_text(self.centroX * 1.5
                                       , self.centroY * 1.9
                                       , font=tkf.Font(size=int(self.tick_gran)))
        self.minimo = self.create_text(self.centroX / 2
                                        , self.centroY * 2.1
                                        , font=tkf.Font(size=-int(2.5 * self.tick_gran)))
        self.minimoid = self.create_text(self.centroX / 2.5
                                        , self.centroY * 1.9
                                        , font=tkf.Font(size=int(self.tick_gran)))

        self.unidadid = self.create_text(self.centroX
                                       , self.centroY * 2 - self.centroY*0.3
                                       , font=tkf.Font(size=-int(1.5*self.tick_gran)))
        self.tituloid = self.create_text(self.centroX
                                       , self.centroY * 2  - self.centroY*0.7
                                       , font=tkf.Font(size=-int(self.tick_gran*1.25)),width='150', justify='center')
        
        # Configurar estado inicial de los elementos
        if self.valor_min != '':
            self.itemconfigure(self.minimo, text=str(redondear(self.valor_min, self.maximo_rango)), fill='black')
        if self.valor_max != '':
            self.itemconfigure(self.maximo, text=str(redondear(self.valor_max, self.maximo_rango)), fill='black')
        self.itemconfigure(self.minimoid, text="Mín", fill='black')
        self.itemconfigure(self.maximoid, text="Máx", fill='black')
        self.itemconfigure(self.unidadid, text=str(self.unidad), fill='black')
        self.itemconfigure(self.tituloid, text=str(self.titulo), fill='black')

    def crear_tick(self, angulo, longitud, rango_min, rango_max):
        rad = math.radians(angulo)
        cos = math.cos(rad)
        sin = math.sin(rad)
        radio = self.radio - self.bisel
        if longitud == self.tick_gran:
            canvas_id = self.create_text(self.centroX - 0.73 * radio * cos, self.centroY - 0.73 * radio * sin)
            numero = redondear(rango_min + (angulo + 60) / 30 * (rango_max - rango_min) / 10, self.maximo_rango)
            self.itemconfig(canvas_id, text=str(numero), font=tkf.Font(size=int(1.5 * self.tick_peq)))
        self.create_line(self.centroX - radio * cos
                         , self.centroY - radio * sin
                         , self.centroX - (radio - longitud) * cos
                         , self.centroY - (radio - longitud) * sin
                         , width=self.linewidth)

    def set_rango(self, start=0, end=100):
        self.start = start
        self.range = end - start

    def set(self, valor, valor_promedio, cambio_vuelta):
        """Actualizael medidor con los datos pasados por parámetro"""
        # Si no hay valores guardados, se establecen los nuevos valores como min y max
        try:
            self.valor_min
        except AttributeError:
            self.valor_min = valor
            self.valor_max = valor
        else:
            # Se comprueban el máximo y minimo
            if valor < self.valor_min:
                self.valor_min = valor
            if valor > self.valor_max:
                self.valor_max = valor
        # Si es una vuelta nueva
        if cambio_vuelta:
            self.vuelta_actual += 1
            # Se asigna el número al medidor
            if self.tipo_umbral == "P":
                porcentaje = 100*(valor_promedio - self.minimo_rango)/(self.maximo_rango - self.minimo_rango)
                if porcentaje < float(self.umbrales_porc[0]):
                    self.color = self.colores[0]
                elif float(self.umbrales_porc[0]) <= porcentaje < float(self.umbrales_porc[1]):
                    self.color = self.colores[1]
                else:
                    self.color = self.colores[2]
            elif self.tipo_umbral == "V":
                if valor_promedio < self.umbrales_val[0]:
                    self.color = self.colores[0]
                elif self.umbrales_val[0] <= valor_promedio < self.umbrales_val[1]:
                    self.color = self.colores[1]
                else:
                    self.color = self.colores[2]
            if valor_promedio <= self.minimo_rango:
                self.deg = 120
            elif valor_promedio >= self.maximo_rango:
                self.deg = 60
            else:
                self.deg = 300 * (valor_promedio - self.start) / self.range - 240
            self.itemconfigure(self.ovalo, outline=self.color)
            # Posición de la aguja, no se actualiza si es la misma que antes
            if self.deg != self.deg_anterior:
                rad = math.radians(self.deg)
                self.coords(self.aguja, self.centroX, self.centroY, self.centroX + self.largo_aguja * math.cos(rad), self.centroY + self.largo_aguja * math.sin(rad))
                self.deg_anterior = self.deg
        if valor == self.valor_min:
            self.itemconfigure(self.minimo, text=str(redondear(self.valor_min, self.maximo_rango)), fill='black')
        if valor == self.valor_max:
            self.itemconfigure(self.maximo, text=str(redondear(self.valor_max, self.maximo_rango)), fill='black')

    def set_ajustes(self, ajustes):
        """Aplica los ajustes"""
        # Parámetros
        self.colores = json.loads(ajustes['colores'])
        self.minimo_rango = float(ajustes['minimo'])
        self.maximo_rango = float(ajustes['maximo'])
        umbrales_porc_str = ajustes['umbrales_porc']
        umbrales_porc = [float(numeric_string) for numeric_string in umbrales_porc_str]
        self.umbrales_porc = umbrales_porc
        umbrales_val_str = ajustes['umbrales_val']
        umbrales_val = [float(numeric_string) for numeric_string in umbrales_val_str]
        self.umbrales_val = umbrales_val
        self.tipo_umbral = ajustes['tipo_umbral']
        # Reinicia gráficamente el medidor
        self.delete("all")
        self.crear_estructura()
        self.crear_interfaz(self.minimo_rango, self.maximo_rango)
        self.set_rango(self.minimo_rango, self.maximo_rango)
