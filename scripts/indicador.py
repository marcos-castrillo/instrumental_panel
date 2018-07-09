# coding=utf-8
import tkinter as tk
import tkinter.font as tkf

class Indicador(tk.Canvas, object):
    def __init__(self, master, configuracion, **kwargs):
        super(Indicador, self).__init__(master, configuracion=None, **kwargs)
        # Parámetros
        self.titulo = configuracion["nombre"]
        self.unidad = configuracion["unidad"]
        self.ancho = int(self['width'])
        self.altura = int(self['height'])
        # Inicializar las variables
        self.valor_anterior = ""
        # Se configura el indicador
        self.crear_estructura(self.altura, self.ancho)
        self.crear_interfaz()

    def crear_estructura(self, altura, ancho):
        # Marco del indicador
        if altura * 2 > ancho:
            self.lado = ancho
        else:
            self.lado = altura * 2
        # Ejes
        self.centroX = self.lado / 2
        self.centroY = self.lado / 2

    def crear_interfaz(self):
        # Texto
        self.tituloid = self.create_text(self.centroX
                                       ,  self.centroY - self.centroY*0.6
                                       , font=tkf.Font(size=-int(self.lado/8),weight="bold"),width='180')
        self.valorid = self.create_text(self.centroX
                                       , self.centroY/1
                                       , font=tkf.Font(size=-int(self.lado/4)))
        self.unidadid = self.create_text(self.centroX
                                       , self.centroY*1.3
                                       , font=tkf.Font(size=-int(self.lado/10)))
        # Estado inicial de los elementos
        self.itemconfigure(self.unidadid, text=str(self.unidad), fill='black')
        self.itemconfigure(self.tituloid, text=str(self.titulo), fill='black')

    def set(self, valor):
        """Actualiza el valor pasado por parámetro si es distinto del anterior"""
        if self.valor_anterior != str(valor):
            self.itemconfigure(self.valorid, text=str(valor))
            self.valor_anterior = str(valor)
