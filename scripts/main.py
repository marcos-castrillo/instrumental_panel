# coding=utf-8
import tkinter as tk

from scripts.medidor import Medidor
from scripts.engranaje import Engranaje
from scripts.indicador import Indicador
from scripts.grafico_multilinea import GraficoMultilinea
from scripts.grafico_pv import GraficoPV
from scripts.grafico_estandar import GraficoEstandar
from scripts.opciones import Opciones
from scripts.ajustes_medidores import AjustesMedidores
from scripts.ajustes_graficos import AjustesGraficos

from scripts.redondeo import redondear

import math
import json
import configparser
from os import path
import datetime
import random

class Main(tk.Frame):
    def __init__(self, master):
        super(Main, self).__init__()
        self.app = master

        # Inicializar las variables
        self.paginaFlag = False
        self.opcionesFlag = True
        self.vuelta = 0
        self.diente = 0
        self.tiempo = 0
        self.vuelta_actual = 0
        self.cambio_vuelta = False
        self.breakpoint = ''
        self.vuelta_limite = ''
        self.diente_limite = ''
        self.dientes_refresco = 1
        self.dientes_refresco_index = 1
        self.presion_array = []
        self.par_array = []
        self.vel_angular_array = []
        self.potencia_array = []
        # Constantes
        self.radio = 37.5 * 10 ** (-3)  # 37.5mm
        self.longitud_frio = 146 * 10 ** (-3)  # 146mm
        self.longitud_caliente = 130 * 10**(-3)  #130mm
        self.diametro_frio = 85 * 10 ** (-3)  # 85mm
        self.diametro_caliente = 96 * 10**(-3)  #96mm
        self.volumen_muerto_frio = 303.66 * 10 ** (-6)  # 303.66 cm3
        self.volumen_muerto_caliente = 226.47 * 10**(-6)  #226.47 cm3
        self.volumen_muerto_regenerador = 335.19 * 10**(-6)  #335.19 cm3
        self.area_caliente = math.pi * (self.diametro_caliente ** 2) / 4
        self.area_frio = math.pi * (self.diametro_frio ** 2) / 4
        self.y_max = self.radio + self.longitud_caliente
        self.y_min = self.longitud_caliente - self.radio
        self.x_max = self.radio + self.longitud_frio
        self.masa_total = 7.03 * (10**-3)  #7.03g
        self.resistencia_aire = 297 #J/Kg K
        self.temperatura_caliente = 693 #K
        self.temperatura_frio = 303 #K
        self.temperatura_r = 471.4 #K
        # Leer el archivo de configuración inicial
        self.configParser = configparser.RawConfigParser()
        self.configFile = 'settings.ini'
        if not path.exists(self.configFile):
            self.crear_config_file()
        self.configParser.read(self.configFile)
        # Crear elementos gráficos
        self.crear_elementos()
        self.crear_medidores()
        self.crear_indicadores()
        self.crear_graficos()
        self.crear_opciones()

    def crear_elementos(self):
        # Obtener ancho/alto de la pantalla
        self.ancho_total = self.app.winfo_screenwidth()
        self.altura_total = self.app.winfo_screenheight()
        # Frame master
        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_rowconfigure(0, weight=1)
        # Resto de frames
        self.menuContainer = tk.Frame(self.app)
        self.opcionesContainer = tk.Frame(self.menuContainer, bg='white', bd=2, highlightbackground="black", pady=5, relief="solid", padx=10)
        self.medidoresContainer = tk.Frame(self.app)
        self.graficosContainer = tk.Frame(self.app)
        self.indicadoresContainer = tk.Frame(self.app)
        # Ajustar el lugar de los frames
        self.medidoresContainer.grid(column=0, row=0)
        self.graficosContainer.grid(column=0, row=0)
        self.menuContainer.grid(column=1, row=0, sticky="N", padx=20)
        self.indicadoresContainer.grid(column=0, row=1, sticky="S", columnspan=2)
        # Elementos
        self.imagen_ajustes = tk.PhotoImage(file="images/ajustes.png")
        stop = tk.PhotoImage(file='images/stop.png')
        play = tk.PhotoImage(file='images/play.png')
        record = tk.PhotoImage(file='images/record.png')
        pause = tk.PhotoImage(file='images/pause.png')
        open = tk.PhotoImage(file='images/open.png')
        reset = tk.PhotoImage(file='images/reset.png')
        ajustes = tk.PhotoImage(file='images/opciones.png')
        grafico = tk.PhotoImage(file='images/chart.png')
        medidor = tk.PhotoImage(file='images/gauge.png')
        pantalla_completa = tk.PhotoImage(file='images/pantalla_completa.png')
        salir = tk.PhotoImage(file='images/exit.png')
        breakpoint = tk.PhotoImage(file='images/breakpoint.png')
        self.stopButton = tk.Button(self.menuContainer, bg='white', text='Parar', font='Helvetica 10 bold', image = stop, command=self.app.stop,compound="top")
        self.stopButton.image = stop
        self.playButton = tk.Button(self.menuContainer, bg='white', text='Reanudar', font='Helvetica 10 bold', image = play, command=self.app.play,compound="top")
        self.playButton.image = play
        self.pauseButton = tk.Button(self.menuContainer, bg='white', text='Pausar', font='Helvetica 10 bold', image = pause, command=self.app.pause,compound="top")
        self.pauseButton.image = pause
        self.recordButton = tk.Button(self.menuContainer, bg='white', text='Grabar', font='Helvetica 10 bold', image = record, command=self.app.record,compound="top")
        self.recordButton.image = record
        self.openButton = tk.Button(self.menuContainer, bg='white', text='Reproducir', font='Helvetica 10 bold', image = open, command=self.app.open,compound="top")
        self.openButton.image = open
        self.resetButton = tk.Button(self.menuContainer, bg='white', text='Borrar datos', font='Helvetica 10 bold', image = reset, command=self.app.reset,compound="top")
        self.resetButton.image = reset
        self.ajustesButton = tk.Button(self.menuContainer, bg='white', text='Opciones', font='Helvetica 10 bold',
                                       image=ajustes, command=self.desplegar_opciones, compound="top")
        self.ajustesButton.image = ajustes
        self.paginaMedidoresButton = tk.Button(self.menuContainer, bg='white', text='Medidores', font='Helvetica 10 bold', image=medidor, command=self.cambiar_pagina, compound="top")
        self.paginaMedidoresButton.image = medidor
        self.paginaGraficosButton = tk.Button(self.menuContainer, bg='white', text='Gráficos', font='Helvetica 10 bold', image=grafico, command=self.cambiar_pagina, compound="top")
        self.paginaGraficosButton.image = grafico
        self.pantallaCompletaButton = tk.Button(self.menuContainer, bg='white', text='P. completa', font='Helvetica 10 bold', image=pantalla_completa, command=self.app.switch_fullscreen, compound="top")
        self.pantallaCompletaButton.image = pantalla_completa
        self.salirButton = tk.Button(self.menuContainer, bg='white', text='Salir', font='Helvetica 10 bold', image=salir, command=self.app.destroy, compound="top")
        self.salirButton.image = salir
        self.estadoLabel = tk.Label(self.menuContainer, font='Helvetica 18 bold', bg='white', borderwidth=2, relief="solid", padx=10)
        self.estadoLabel.config(text=self.app.modo.get())
        self.breakpointLabel = tk.Label(self.menuContainer, font='Helvetica 18 bold', padx=10, image=breakpoint)
        self.breakpointLabel.image = breakpoint
        self.timeLabel = tk.Label(self.menuContainer, font='Helvetica 18 bold', bg='white', borderwidth=2, relief="solid", padx=10)
        self.timeLabel.config(text=str(datetime.timedelta(milliseconds=0)))
        # Ajustar el lugar de los elementos
        self.paginaMedidoresButton.grid(row=0, column=0, pady=2)
        self.paginaGraficosButton.grid(row=0, column=0, pady=2)
        self.paginaMedidoresButton.grid_remove()
        self.pantallaCompletaButton.grid(row=0, column=1, pady=2)
        self.salirButton.grid(row=0, column=2, pady=2)
        self.stopButton.grid(row=1, column=0, pady=2)
        self.stopButton.configure(state='disabled')
        self.playButton.grid(row=1, column=1, pady=2)
        self.playButton.grid_remove()
        self.pauseButton.grid(row=1, column=1, pady=2)
        self.recordButton.grid(row=1, column=2, pady=2)
        self.openButton.grid(row=2, column=0, pady=2)
        self.resetButton.grid(row=2, column=1, pady=2)
        self.ajustesButton.grid(row=2, column=2, pady=2)
        self.estadoLabel.grid(row=3, column=0, columnspan=3, pady=2)
        self.breakpointLabel.grid(row=3, column=0, columnspan=3, pady=2, padx=(0,10), sticky="E")
        self.breakpointLabel.grid_remove()
        self.timeLabel.grid(row=4, column=0, columnspan=3, pady=2)
        self.opcionesContainer.grid(row=5, column=0, columnspan=3, pady=2)

    def crear_medidores(self):
        # Configuración de cada medidor
        self.n_medidores = 5
        medidor0_conf = {
            "nombre": self.configParser.get('Medidor0', 'nombre'),
            "unidad": self.configParser.get('Medidor0', 'unidad'),
            "minimo": self.configParser.getfloat('Medidor0', 'minimo'),
            "maximo": self.configParser.getfloat('Medidor0', 'maximo'),
            "colores": json.loads(self.configParser.get('Medidor0', 'colores')),
            "umbrales_porc": json.loads(self.configParser.get('Medidor0', 'umbrales_porc')),
            "umbrales_val": json.loads(self.configParser.get('Medidor0', 'umbrales_val')),
            "tipo_umbral": self.configParser.get('Medidor0', 'tipo_umbral'),
            "index" : 0
        }
        medidor1_conf = {
            "nombre": self.configParser.get('Medidor1', 'nombre'),
            "unidad": self.configParser.get('Medidor1', 'unidad'),
            "minimo": self.configParser.getfloat('Medidor1', 'minimo'),
            "maximo": self.configParser.getfloat('Medidor1', 'maximo'),
            "colores": json.loads(self.configParser.get('Medidor1', 'colores')),
            "umbrales_porc": json.loads(self.configParser.get('Medidor1', 'umbrales_porc')),
            "umbrales_val": json.loads(self.configParser.get('Medidor1', 'umbrales_val')),
            "tipo_umbral": self.configParser.get('Medidor1', 'tipo_umbral'),
            "index" : 1
        }
        medidor2_conf = {
            "nombre": self.configParser.get('Medidor2', 'nombre'),
            "unidad": self.configParser.get('Medidor2', 'unidad'),
            "minimo": self.configParser.getfloat('Medidor2', 'minimo'),
            "maximo": self.configParser.getfloat('Medidor2', 'maximo'),
            "colores": json.loads(self.configParser.get('Medidor2', 'colores')),
            "umbrales_porc": json.loads(self.configParser.get('Medidor2', 'umbrales_porc')),
            "umbrales_val": json.loads(self.configParser.get('Medidor2', 'umbrales_val')),
            "tipo_umbral": self.configParser.get('Medidor2', 'tipo_umbral'),
            "index" : 2
        }
        medidor3_conf = {
            "nombre": self.configParser.get('Medidor3', 'nombre'),
            "unidad": self.configParser.get('Medidor3', 'unidad'),
            "minimo": self.configParser.getfloat('Medidor3', 'minimo'),
            "maximo": self.configParser.getfloat('Medidor3', 'maximo'),
            "colores": json.loads(self.configParser.get('Medidor3', 'colores')),
            "umbrales_porc": json.loads(self.configParser.get('Medidor3', 'umbrales_porc')),
            "umbrales_val": json.loads(self.configParser.get('Medidor3', 'umbrales_val')),
            "tipo_umbral": self.configParser.get('Medidor3', 'tipo_umbral'),
            "index" : 3
        }
        medidor4_conf = {
            "nombre": self.configParser.get('Medidor4', 'nombre'),
            "unidad": self.configParser.get('Medidor4', 'unidad'),
            "minimo": self.configParser.getfloat('Medidor4', 'minimo'),
            "maximo": self.configParser.getfloat('Medidor4', 'maximo')
        }
        # Flags para controlar el mostrar u ocultar la ventana de ajustes
        medidor0_flag = False
        medidor1_flag = False
        medidor2_flag = False
        medidor3_flag = False
        # Medidores
        ancho_medidor = self.ancho_total / self.n_medidores
        altura_medidor = self.altura_total/ self.n_medidores*2
        medidor0 = Medidor(self.medidoresContainer, bd=2, height=altura_medidor, width=ancho_medidor, bg='white', highlightbackground="black", configuracion=medidor0_conf)
        medidor1 = Medidor(self.medidoresContainer, bd=2, height=altura_medidor, width=ancho_medidor, bg='white', highlightbackground="black", configuracion=medidor1_conf)
        medidor2 = Medidor(self.medidoresContainer, bd=2, height=altura_medidor, width=ancho_medidor, bg='white', highlightbackground="black", configuracion=medidor2_conf)
        medidor3 = Medidor(self.medidoresContainer, bd=2, height=altura_medidor, width=ancho_medidor, bg='white', highlightbackground="black", configuracion=medidor3_conf)
        medidor4 = Engranaje(self.medidoresContainer, bd=2, height=altura_medidor, width=ancho_medidor, bg='white', highlightbackground="black", configuracion=medidor4_conf)
        # Frame de la ventana de ajustes de cada medidor
        medidor0_container = tk.Frame(self.medidoresContainer)
        medidor1_container = tk.Frame(self.medidoresContainer)
        medidor2_container = tk.Frame(self.medidoresContainer)
        medidor3_container = tk.Frame(self.medidoresContainer)
        # Botones de ajustes
        medidor0_button = tk.Button(self.medidoresContainer, text="Ajustes", image=self.imagen_ajustes, command=lambda: self.desplegar_ajustes(medidor0))
        medidor1_button = tk.Button(self.medidoresContainer, text="Ajustes", image=self.imagen_ajustes, command=lambda: self.desplegar_ajustes(medidor1))
        medidor2_button = tk.Button(self.medidoresContainer, text="Ajustes", image=self.imagen_ajustes, command=lambda: self.desplegar_ajustes(medidor2))
        medidor3_button = tk.Button(self.medidoresContainer, text="Ajustes", image=self.imagen_ajustes, command=lambda: self.desplegar_ajustes(medidor3))
        # Ajustes de los medidores
        medidor0_ajustes = AjustesMedidores(medidor0_container, self, self.app, configuracion=medidor0_conf)
        medidor1_ajustes = AjustesMedidores(medidor1_container, self, self.app, configuracion=medidor1_conf)
        medidor2_ajustes = AjustesMedidores(medidor2_container, self, self.app, configuracion=medidor2_conf)
        medidor3_ajustes = AjustesMedidores(medidor3_container, self, self.app, configuracion=medidor3_conf)
        # Ajustar el lugar de cada medidor
        medidor0.grid(column=2, row=0, columnspan=2, padx=(0,10), pady=(5,10))
        medidor1.grid(column=4, row=0, columnspan=2, padx=(10,0), pady=(5,10))
        medidor2.grid(column=1, row=1, columnspan=2, padx=(0,10), pady=(0,10))
        medidor3.grid(column=3, row=1, columnspan=2, padx=(10,10), pady=(0,10))
        medidor4.grid(column=5, row=1, columnspan=2, padx=(10,0), pady=(0,10))
        # Ajustar el lugar de cada ventana de ajustes
        medidor0_container.grid(column=2, row=0, columnspan=2)
        medidor0_container.grid_remove()
        medidor1_container.grid(column=4, row=0, columnspan=2)
        medidor1_container.grid_remove()
        medidor2_container.grid(column=1, row=1, columnspan=2)
        medidor2_container.grid_remove()
        medidor3_container.grid(column=3, row=1, columnspan=2)
        medidor3_container.grid_remove(

        )
        # Ajustar el lugar del contenido de cada frame de ajustes
        medidor0_ajustes.grid(row=0, column=0)
        medidor1_ajustes.grid(row=0, column=0)
        medidor2_ajustes.grid(row=0, column=0)
        medidor3_ajustes.grid(row=0, column=0)
        # Ajustar el lugar de los botones
        medidor0_button.grid(column=2, row=0, columnspan=2, sticky="NE", padx=(0,13), pady=(5,10))
        medidor1_button.grid(column=4, row=0, columnspan=2, sticky="NE", padx=(0,3), pady=(5,10))
        medidor2_button.grid(column=1, row=1, columnspan=2, sticky="NE", padx=(0,10), pady=(0,10))
        medidor3_button.grid(column=3, row=1, columnspan=2, sticky="NE", padx=(0,10), pady=(0,10))
        # Crear el diccionario de medidores
        self.medidores = {
            'medidor0': medidor0, 'medidor0_flag': medidor0_flag, 'medidor0_ajustes': medidor0_ajustes, 'medidor0_container': medidor0_container,
            'medidor1': medidor1, 'medidor1_flag': medidor1_flag, 'medidor1_ajustes': medidor1_ajustes, 'medidor1_container': medidor1_container,
            'medidor2': medidor2, 'medidor2_flag': medidor2_flag, 'medidor2_ajustes': medidor2_ajustes, 'medidor2_container': medidor2_container,
            'medidor3': medidor3, 'medidor3_flag': medidor3_flag, 'medidor3_ajustes': medidor3_ajustes, 'medidor3_container': medidor3_container,
            'medidor4': medidor4
        }

    def crear_indicadores(self):
        # Configuración de cada indicador
        self.n_indicadores = 8
        indicador0_conf = {
            "nombre": self.configParser.get('Indicador0', 'nombre'),
            "unidad": self.configParser.get('Indicador0', 'unidad')
        }
        indicador1_conf = {
            "nombre": self.configParser.get('Indicador1', 'nombre'),
            "unidad": self.configParser.get('Indicador1', 'unidad')
        }
        indicador2_conf = {
            "nombre": self.configParser.get('Indicador2', 'nombre'),
            "unidad": self.configParser.get('Indicador2', 'unidad')
        }
        indicador3_conf = {
            "nombre": self.configParser.get('Indicador3', 'nombre'),
            "unidad": self.configParser.get('Indicador3', 'unidad')
        }
        indicador4_conf = {
            "nombre": self.configParser.get('Indicador4', 'nombre'),
            "unidad": self.configParser.get('Indicador4', 'unidad')
        }
        indicador5_conf = {
            "nombre": self.configParser.get('Indicador5', 'nombre'),
            "unidad": self.configParser.get('Indicador5', 'unidad')
        }
        indicador6_conf = {
            "nombre": self.configParser.get('Indicador6', 'nombre'),
            "unidad": self.configParser.get('Indicador6', 'unidad')
        }
        indicador7_conf = {
            "nombre": self.configParser.get('Indicador7', 'nombre'),
            "unidad": self.configParser.get('Indicador7', 'unidad')
        }
        # Indicadores
        ancho_indicador = (self.ancho_total / self.n_indicadores) - self.n_indicadores*2
        altura_indicador = self.altura_total / self.n_indicadores * 1.15
        indicador0 = Indicador(self.indicadoresContainer, bd=2, height=altura_indicador, width=ancho_indicador, bg='white', highlightbackground="black",configuracion=indicador0_conf)
        indicador1 = Indicador(self.indicadoresContainer, bd=2, height=altura_indicador, width=ancho_indicador, bg='white', highlightbackground="black",configuracion=indicador1_conf)
        indicador2 = Indicador(self.indicadoresContainer, bd=2, height=altura_indicador, width=ancho_indicador, bg='white', highlightbackground="black",configuracion=indicador2_conf)
        indicador3 = Indicador(self.indicadoresContainer, bd=2, height=altura_indicador, width=ancho_indicador, bg='white', highlightbackground="black",configuracion=indicador3_conf)
        indicador4 = Indicador(self.indicadoresContainer, bd=2, height=altura_indicador, width=ancho_indicador, bg='white', highlightbackground="black",configuracion=indicador4_conf)
        indicador5 = Indicador(self.indicadoresContainer, bd=2, height=altura_indicador, width=ancho_indicador, bg='white', highlightbackground="black",configuracion=indicador5_conf)
        indicador6 = Indicador(self.indicadoresContainer, bd=2, height=altura_indicador, width=ancho_indicador, bg='white', highlightbackground="black",configuracion=indicador6_conf)
        indicador7 = Indicador(self.indicadoresContainer, bd=2, height=altura_indicador, width=ancho_indicador, bg='white', highlightbackground="black",configuracion=indicador7_conf)
        # Ajustar el lugar de cada indicador
        indicador0.grid(row=2, column=0, padx=(5,0), pady=(0,5))
        indicador1.grid(row=2, column=1, padx=(5,0), pady=(0,5))
        indicador2.grid(row=2, column=2, padx=(5,0), pady=(0,5))
        indicador3.grid(row=2, column=3, padx=(5,0), pady=(0,5))
        indicador4.grid(row=2, column=4, padx=(5,0), pady=(0,5))
        indicador5.grid(row=2, column=5, padx=(5,0), pady=(0,5))
        indicador6.grid(row=2, column=6, padx=(5,0), pady=(0,5))
        indicador7.grid(row=2, column=7, padx=(5,0), pady=(0,5))
        # Crear el diccionario de indicadores
        self.indicadores = {
            'indicador0': indicador0, 'indicador1': indicador1, 'indicador2': indicador2, 'indicador3': indicador3,
            'indicador4': indicador4, 'indicador5': indicador5, 'indicador6': indicador6, 'indicador7': indicador7
        }

    def crear_graficos(self):
        # Configuración de cada gráfico
        self.n_graficos = 5
        grafico0_conf = {
            "titulo": self.configParser.get('Grafico0', 'titulo'),
            "nombreX": self.configParser.get('Grafico0', 'nombreX'),
            "color0": self.configParser.get('Grafico0', 'color0'),
            "color1": self.configParser.get('Grafico0', 'color1'),
            "minX": self.configParser.get('Grafico0', 'minX'),
            "maxX": self.configParser.get('Grafico0', 'maxX'),
            "stepX": self.configParser.get('Grafico0', 'stepX'),
            "nombreY1": self.configParser.get('Grafico0', 'nombreY1'),
            "minY1": self.configParser.get('Grafico0', 'minY1'),
            "maxY1": self.configParser.get('Grafico0', 'maxY1'),
            "stepY1": self.configParser.get('Grafico0', 'stepY1'),
            "nombreY2": self.configParser.get('Grafico0', 'nombreY2'),
            "minY2": self.configParser.get('Grafico0', 'minY2'),
            "maxY2": self.configParser.get('Grafico0', 'maxY2'),
            "stepY2": self.configParser.get('Grafico0', 'stepY2'),
            "n_lineas": self.configParser.get('Grafico0', 'n_lineas'),
            "live": True,
            "index": 0
        }
        grafico1_conf = {
            "titulo": self.configParser.get('Grafico1', 'titulo'),
            "nombreX": self.configParser.get('Grafico1', 'nombreX'),
            "color": self.configParser.get('Grafico1', 'color'),
            "minX": self.configParser.get('Grafico1', 'minX'),
            "maxX": self.configParser.get('Grafico1', 'maxX'),
            "stepX": self.configParser.get('Grafico1', 'stepX'),
            "nombreY": self.configParser.get('Grafico1', 'nombreY'),
            "minY": self.configParser.get('Grafico1', 'minY'),
            "maxY": self.configParser.get('Grafico1', 'maxY'),
            "stepY": self.configParser.get('Grafico1', 'stepY'),
            "live": False,
            "index": 1
        }
        grafico2_conf = {
            "titulo": self.configParser.get('Grafico2', 'titulo'),
            "nombreX": self.configParser.get('Grafico2', 'nombreX'),
            "color": self.configParser.get('Grafico2', 'color'),
            "minX": self.configParser.get('Grafico2', 'minX'),
            "maxX": self.configParser.get('Grafico2', 'maxX'),
            "stepX": self.configParser.get('Grafico2', 'stepX'),
            "nombreY": self.configParser.get('Grafico2', 'nombreY'),
            "minY": self.configParser.get('Grafico2', 'minY'),
            "maxY": self.configParser.get('Grafico2', 'maxY'),
            "stepY": self.configParser.get('Grafico2', 'stepY'),
            "live": False,
            "index": 2
        }
        # Flags para controlar el mostrar u ocultar la ventana de ajustes
        grafico0_flag = False
        grafico1_flag = False
        grafico2_flag = False
        # Gráficos
        ancho_grafico = self.ancho_total / self.n_graficos / 88
        altura_grafico = self.altura_total / self.n_graficos / 30
        ancho_grafico_live = self.ancho_total / self.n_graficos / 70
        altura_grafico_live = self.altura_total / self.n_graficos / 15
        grafico0 = GraficoMultilinea(self.graficosContainer, height=altura_grafico_live, width=ancho_grafico_live, configuracion=grafico0_conf)
        grafico1 = GraficoPV(self.graficosContainer, height=altura_grafico, width=ancho_grafico, configuracion=grafico1_conf)
        grafico2 = GraficoEstandar(self.graficosContainer, height=altura_grafico, width=ancho_grafico, configuracion=grafico2_conf)
        # Ajustar el lugar de cada gráfico
        grafico0.grid(row=0, column=2, columnspan=2, padx=(5,5), pady=(5,5))
        grafico1.grid(row=1, column=2, padx=(5,5), pady=(0,5))
        grafico2.grid(row=1, column=3, padx=(5,5), pady=(0,5))
        self.graficosContainer.grid_remove()
        # Frame de la ventana de ajustes de cada medidor
        grafico0_container = tk.Frame(self.graficosContainer)
        grafico1_container = tk.Frame(self.graficosContainer)
        grafico2_container = tk.Frame(self.graficosContainer)
        # Botones de ajustes
        grafico0_button = tk.Button(self.graficosContainer, text="Ajustes", image=self.imagen_ajustes,
                                    command=lambda: self.desplegar_ajustes(grafico0))
        grafico1_button = tk.Button(self.graficosContainer, text="Ajustes", image=self.imagen_ajustes,
                                    command=lambda: self.desplegar_ajustes(grafico1))
        grafico2_button = tk.Button(self.graficosContainer, text="Ajustes", image=self.imagen_ajustes,
                                    command=lambda: self.desplegar_ajustes(grafico2))
        # Ajustes de los medidores
        grafico0_ajustes = AjustesGraficos(grafico0_container, self, self.app,
                                                              configuracion=grafico0_conf)
        grafico1_ajustes = AjustesGraficos(grafico1_container, self, self.app,
                                                              configuracion=grafico1_conf)
        grafico2_ajustes = AjustesGraficos(grafico2_container, self, self.app,
                                                              configuracion=grafico2_conf)
        # Ajustar el lugar de cada ventana de ajustes
        grafico0_container.grid(row=0, column=2, columnspan=2)
        grafico0_container.grid_remove()
        grafico1_container.grid(row=1, column=2)
        grafico1_container.grid_remove()
        grafico2_container.grid(row=1, column=3)
        grafico2_container.grid_remove()
        # Ajustar el lugar del contenido de cada frame de ajustes
        grafico0_ajustes.grid(row=0, column=0)
        grafico1_ajustes.grid(row=0, column=0)
        grafico2_ajustes.grid(row=0, column=0)
        # Ajustar el lugar de los botones
        grafico0_button.grid(column=2, row=0, columnspan=2, sticky="SW", padx=(10, 0), pady=(0, 5))
        grafico1_button.grid(column=2, row=1, columnspan=2, sticky="SW", padx=(5, 0), pady=(0, 5))
        grafico2_button.grid(column=3, row=1, columnspan=2, sticky="SW", padx=(5, 0), pady=(0, 5))
        # Crear el diccionario de indicadores
        self.graficos = {
            'grafico0': grafico0, 'grafico0_flag': grafico0_flag, 'grafico0_ajustes': grafico0_ajustes, 'grafico0_container': grafico0_container,
            'grafico1': grafico1, 'grafico1_flag': grafico1_flag, 'grafico1_ajustes': grafico1_ajustes, 'grafico1_container': grafico1_container,
            'grafico2': grafico2, 'grafico2_flag': grafico2_flag, 'grafico2_ajustes': grafico2_ajustes, 'grafico2_container': grafico2_container,
        }

    def crear_opciones(self):
        configuracion_opciones = {"modo": self.app.modo}
        self.opciones = Opciones(self.opcionesContainer, self.app, configuracion=configuracion_opciones)
        self.opciones.grid(row=0, column=0)

    def crear_config_file(self):
        """Crea un archivo de configuración"""
        self.configParser.add_section('Medidor0')
        self.configParser.set('Medidor0', 'nombre', 'Presión')
        self.configParser.set('Medidor0', 'unidad', 'bar')
        self.configParser.set('Medidor0', 'minimo', '0')
        self.configParser.set('Medidor0', 'maximo', '10')
        self.configParser.set('Medidor0', 'colores', '["green", "yellow", "red"]')
        self.configParser.set('Medidor0', 'umbrales_porc', '[50, 75]')
        self.configParser.set('Medidor0', 'umbrales_val', '[7.5, 8]')
        self.configParser.set('Medidor0', 'tipo_umbral', 'P')
        self.configParser.add_section('Medidor1')
        self.configParser.set('Medidor1', 'nombre', 'Par')
        self.configParser.set('Medidor1', 'unidad', 'N*m')
        self.configParser.set('Medidor1', 'minimo', '-10')
        self.configParser.set('Medidor1', 'maximo', '10')
        self.configParser.set('Medidor1', 'colores', '["green", "yellow", "red"]')
        self.configParser.set('Medidor1', 'umbrales_porc', '[50, 75]')
        self.configParser.set('Medidor1', 'umbrales_val', '[7, 9]')
        self.configParser.set('Medidor1', 'tipo_umbral', 'P')
        self.configParser.add_section('Medidor2')
        self.configParser.set('Medidor2', 'nombre', 'Velocidad angular')
        self.configParser.set('Medidor2', 'unidad', 'rad/s')
        self.configParser.set('Medidor2', 'minimo', '0')
        self.configParser.set('Medidor2', 'maximo', '500')
        self.configParser.set('Medidor2', 'colores', '["green", "yellow", "red"]')
        self.configParser.set('Medidor2', 'umbrales_porc', '[50, 75]')
        self.configParser.set('Medidor2', 'umbrales_val', '[250, 400]')
        self.configParser.set('Medidor2', 'tipo_umbral', 'P')
        self.configParser.add_section('Medidor3')
        self.configParser.set('Medidor3', 'nombre', 'Potencia')
        self.configParser.set('Medidor3', 'unidad', 'W')
        self.configParser.set('Medidor3', 'minimo', '0')
        self.configParser.set('Medidor3', 'maximo', '5000')
        self.configParser.set('Medidor3', 'colores', '["green", "yellow", "red"]')
        self.configParser.set('Medidor3', 'umbrales_porc', '[50, 75]')
        self.configParser.set('Medidor3', 'umbrales_val', '[2500, 4000]')
        self.configParser.set('Medidor3', 'tipo_umbral', 'P')
        self.configParser.add_section('Medidor4')
        self.configParser.set('Medidor4', 'nombre', 'Ángulo cigüeñal')
        self.configParser.set('Medidor4', 'unidad', 'º')
        self.configParser.set('Medidor4', 'minimo', '0')
        self.configParser.set('Medidor4', 'maximo', '360')
        self.configParser.add_section('Indicador0')
        self.configParser.set('Indicador0', 'nombre', 'Vuelta del cigüeñal')
        self.configParser.set('Indicador0', 'unidad', '')
        self.configParser.add_section('Indicador1')
        self.configParser.set('Indicador1', 'nombre', 'Grados girados')
        self.configParser.set('Indicador1', 'unidad', 'º')
        self.configParser.add_section('Indicador2')
        self.configParser.set('Indicador2', 'nombre', 'Presión instantánea')
        self.configParser.set('Indicador2', 'unidad', 'bar')
        self.configParser.add_section('Indicador3')
        self.configParser.set('Indicador3', 'nombre', 'Par motor instantáneo')
        self.configParser.set('Indicador3', 'unidad', 'N*m')
        self.configParser.add_section('Indicador4')
        self.configParser.set('Indicador4', 'nombre', 'Volumen instantáneo')
        self.configParser.set('Indicador4', 'unidad', 'l')
        self.configParser.add_section('Indicador5')
        self.configParser.set('Indicador5', 'nombre', 'Velocidad angular inst.')
        self.configParser.set('Indicador5', 'unidad', 'rad/s')
        self.configParser.add_section('Indicador6')
        self.configParser.set('Indicador6', 'nombre', 'Velocidad angular prom.')
        self.configParser.set('Indicador6', 'unidad', 'rad/s')
        self.configParser.add_section('Indicador7')
        self.configParser.set('Indicador7', 'nombre', 'Potencia promedio')
        self.configParser.set('Indicador7', 'unidad', 'W')
        self.configParser.add_section('Grafico0')
        self.configParser.set('Grafico0', 'titulo', 'Presión y par/grado de cigüeñal')
        self.configParser.set('Grafico0', 'color0', 'red')
        self.configParser.set('Grafico0', 'color1', 'green')
        self.configParser.set('Grafico0', 'nombreX', 'Grado de cigüeñal (º)')
        self.configParser.set('Grafico0', 'minX', '0')
        self.configParser.set('Grafico0', 'maxX', '360')
        self.configParser.set('Grafico0', 'stepX', '30')
        self.configParser.set('Grafico0', 'nombreY1', 'Presión (bar)')
        self.configParser.set('Grafico0', 'minY1', '0')
        self.configParser.set('Grafico0', 'maxY1', '10')
        self.configParser.set('Grafico0', 'stepY1', '2')
        self.configParser.set('Grafico0', 'nombreY2', 'Par (N*m)')
        self.configParser.set('Grafico0', 'minY2', '-10')
        self.configParser.set('Grafico0', 'maxY2', '10')
        self.configParser.set('Grafico0', 'stepY2', '2.5')
        self.configParser.set('Grafico0', 'n_lineas', '3')
        self.configParser.add_section('Grafico1')
        self.configParser.set('Grafico1', 'titulo', 'Diagrama P-V')
        self.configParser.set('Grafico1', 'color', 'red')
        self.configParser.set('Grafico1', 'nombreX', 'Volumen (l)')
        self.configParser.set('Grafico1', 'minX', '0')
        self.configParser.set('Grafico1', 'maxX', '3')
        self.configParser.set('Grafico1', 'stepX', '0.5')
        self.configParser.set('Grafico1', 'nombreY', 'Presión (bar)')
        self.configParser.set('Grafico1', 'minY', '0')
        self.configParser.set('Grafico1', 'maxY', '10')
        self.configParser.set('Grafico1', 'stepY', '2')
        self.configParser.add_section('Grafico2')
        self.configParser.set('Grafico2', 'titulo', 'Potencia / velocidad angular')
        self.configParser.set('Grafico2', 'color', 'red')
        self.configParser.set('Grafico2', 'nombreX', 'w promedio/vuelta (rad/s)')
        self.configParser.set('Grafico2', 'minX', '0')
        self.configParser.set('Grafico2', 'maxX', '1000')
        self.configParser.set('Grafico2', 'stepX', '200')
        self.configParser.set('Grafico2', 'nombreY', 'Potencia/vuelta (W)')
        self.configParser.set('Grafico2', 'minY', '0')
        self.configParser.set('Grafico2', 'maxY', '5000')
        self.configParser.set('Grafico2', 'stepY', '1000')
        with open(self.configFile, 'w') as output:
            self.configParser.write(output)

    def guardar_config(self, seccion, subsecciones, config):
        """Guarda la nueva configuracion en el archivo """
        if not self.configParser.has_section(seccion):
            self.configParser.add_section(seccion)
        for i in range(0, len(subsecciones), 1):
            self.configParser.set(seccion, subsecciones[i], config[subsecciones[i]])
        with open(self.configFile, 'w') as output:
            self.configParser.write(output)

    def cambiar_pagina(self):
        """Alternar entre la página de medidores o gráficos"""
        if self.paginaFlag:
            self.graficosContainer.grid_remove()
            self.medidoresContainer.grid()
            self.paginaGraficosButton.grid()
            self.paginaMedidoresButton.grid_remove()
        else:
            self.graficosContainer.grid()
            self.medidoresContainer.grid_remove()
            self.paginaGraficosButton.grid_remove()
            self.paginaMedidoresButton.grid()
        self.paginaFlag = not self.paginaFlag

    def desplegar_opciones(self):
        """Desplegar/ocultar las opciones generales"""
        if self.opcionesFlag:
            self.opcionesContainer.grid_remove()
        else:
            self.opcionesContainer.grid()
        self.opcionesFlag = not self.opcionesFlag

    def set(self, valores, reiniciar):
        """Actualizar los datos"""
        calculos = self.calcular(valores)
        self.actualizar_elementos(calculos, reiniciar)

    def calcular(self, valores):
        """Realiza todos los cálculos aplicando las fórmulas y los guarda en arrays"""
        vuelta = valores["vuelta"]
        diente = valores["diente"]
        periodo = valores["tiempo"]
        par = valores["par"]
        presion = valores["presion"]
        # Si ya es la vuelta siguiente
        if vuelta > self.vuelta_actual:
            self.vuelta_actual += 1
            self.cambio_vuelta = True
        # Si es el primer diente de la primera vuelta
        elif vuelta == 0 and diente == 1:
            self.cambio_vuelta = True
        else:
            self.cambio_vuelta = False
        # Fórmulas matemáticas
        frecuencia_diente = 1 / periodo #Hz
        vel_angular = 2 * math.pi * frecuencia_diente   #rad/s
        potencia = abs(par) * vel_angular    #W
        diente_rad = diente * math.pi/180
        diente_rad_2 = (270 + diente) * math.pi/180
        # VOLUMEN CALIENTE
        y = self.radio * math.cos(diente_rad_2) + self.longitud_caliente * math.sqrt(1 - (self.radio* math.sin(diente_rad_2) / self.longitud_caliente) ** 2)
        volumen_caliente_parcial = self.area_caliente * (self.y_max - y)
        volumen_caliente = volumen_caliente_parcial + self.volumen_muerto_caliente
        # VOLUMEN FRÍO
        x = self.radio * math.cos(diente_rad) + self.longitud_frio * math.sqrt(1 - (self.radio* math.sin(diente_rad) / self.longitud_frio) ** 2)
        volumen_frio_parcial = self.area_frio * (self.x_max - x) + self.area_caliente * (y - self.y_min)
        volumen_frio = volumen_frio_parcial + self.volumen_muerto_frio
        # VOLUMEN TOTAL
        volumen = volumen_caliente + volumen_frio + self.volumen_muerto_regenerador
        # Pasar el volumen de m^3 a litros
        volumen = volumen * 1000
        # PRESIÓN (Sólo en simulación)
        if presion == '':
            presion = (self.masa_total * self.resistencia_aire) / ( (volumen_caliente/self.temperatura_caliente) + (volumen_frio/self.temperatura_frio) + (self.volumen_muerto_regenerador/self.temperatura_r) )
            presion = presion * (10**-5)    # Pasar a bares
            self.app.presion = presion
        # Guardar datos en los arrays
        self.presion_array.append(presion)
        self.par_array.append(par)
        self.vel_angular_array.append(vel_angular)
        self.potencia_array.append(potencia)
        if len(self.presion_array) > 360:
            self.presion_array.pop(0)
            self.par_array.pop(0)
            self.vel_angular_array.pop(0)
            self.potencia_array.pop(0)
        if self.cambio_vuelta:
            presion_promedio = redondear(sum(self.presion_array) / len(self.presion_array), 0)
            par_promedio = redondear(sum(self.par_array) / len(self.par_array), 0)
            vel_angular_promedio = redondear(sum(self.vel_angular_array) / len(self.vel_angular_array), 0)
            potencia_promedio = redondear(sum(self.potencia_array) / len(self.potencia_array), 0)
        else:
            presion_promedio = 0
            par_promedio = 0
            vel_angular_promedio = 0
            potencia_promedio = 0
        # Devolver los valores calculados
        valores["vel_angular"] = vel_angular
        valores["potencia"] = potencia
        valores["presion"] = presion
        valores["volumen"] = volumen
        valores["presion_promedio"] = presion_promedio
        valores["par_promedio"] = par_promedio
        valores["vel_angular_promedio"] = vel_angular_promedio
        valores["potencia_promedio"] = potencia_promedio
        return valores

    def actualizar_elementos(self, calculos, reiniciar):
        """Actualizar los valores en la UI"""
        vuelta = calculos["vuelta"]
        diente = calculos["diente"]
        periodo = calculos["tiempo"]
        presion = redondear(calculos["presion"], 0)
        par = redondear(calculos["par"], 0)
        vel_angular = redondear(calculos["vel_angular"], 0)
        potencia = redondear(calculos["potencia"], 0)
        volumen = redondear(calculos["volumen"], 0)
        presion_promedio = calculos["presion_promedio"]
        par_promedio = calculos["par_promedio"]
        vel_angular_promedio = calculos["vel_angular_promedio"]
        potencia_promedio = calculos["potencia_promedio"]
        # Actualizar tiempo
        self.tiempo += periodo
        time_stamp = datetime.timedelta(milliseconds=self.tiempo)
        # Si la time_stamp es mayor que el breakpoint de tiempo definido, se pausa la app
        if self.breakpoint != '' and self.breakpoint <= time_stamp:
            if self.app.grabando:
                self.after(1, self.app.stop)
            else:
                self.after(1, self.app.pause)
            self.breakpoint = ''
            if self.vuelta_limite == '' and self.diente_limite == '':
                self.breakpointLabel.grid_remove()
        # Si la vuelta/diente es igual o mayor al limite establecido, se pausa la app
        elif (self.vuelta_limite != '' or self.diente_limite != '') and (
                (self.vuelta_limite == vuelta and self.diente_limite == diente) or (
                self.vuelta_limite == vuelta and self.diente_limite == '') or (
                        self.vuelta_limite == '' and self.diente_limite == diente)):
            if self.app.grabando:
                self.after(1, self.app.stop)
            else:
                self.after(1, self.app.pause)
            self.vuelta_limite = ''
            self.diente_limite = ''
            if self.breakpoint == '':
                self.breakpointLabel.grid_remove()
        else:
            self.timeLabel.config(text=str(time_stamp))
        if reiniciar:
            # Si reiniciar = True, los máximos y mínimos se actualizan a los valores actuales
            self.tiempo = periodo
            self.medidores['medidor0'].valor_min = presion
            self.medidores['medidor0'].valor_max = presion
            self.medidores['medidor1'].valor_min = par
            self.medidores['medidor1'].valor_max = par
            self.medidores['medidor2'].valor_min = vel_angular
            self.medidores['medidor2'].valor_max = vel_angular
            self.medidores['medidor3'].valor_min = potencia
            self.medidores['medidor3'].valor_max = potencia
        # Valores promedio
        if not self.paginaFlag:
            self.medidores['medidor0'].set(presion, presion_promedio, self.cambio_vuelta)
            self.medidores['medidor1'].set(par, par_promedio, self.cambio_vuelta)
            self.medidores['medidor2'].set(vel_angular, vel_angular_promedio, self.cambio_vuelta)
            self.medidores['medidor3'].set(potencia, potencia_promedio, self.cambio_vuelta)
        else:
            self.graficos['grafico0'].set(diente, presion, par, self.cambio_vuelta)
            self.graficos['grafico1'].set(volumen, presion, self.cambio_vuelta)
            self.graficos['grafico2'].set(vel_angular, potencia, self.cambio_vuelta)
        if self.cambio_vuelta:
            self.indicadores['indicador0'].set(vuelta)
            self.indicadores['indicador6'].set(vel_angular_promedio)
            self.indicadores['indicador7'].set(potencia_promedio)
        # Valores instantáneos
        self.dientes_refresco_index -= 1
        if self.dientes_refresco_index == 0:
            self.dientes_refresco_index = self.dientes_refresco
            if not self.paginaFlag:
                self.medidores['medidor4'].set(diente)
            self.indicadores['indicador1'].set(diente)
            self.indicadores['indicador2'].set(presion)
            self.indicadores['indicador3'].set(par)
            self.indicadores['indicador4'].set(volumen)
            self.indicadores['indicador5'].set(vel_angular)

    def guardar_ajustes(self, ajustes_elemento, ajustes, tipo_accion):
        """Guardar los ajustes de un medidor o gráfico"""
        index = ajustes_elemento.index
        if not self.paginaFlag:
            ajustes['colores'] = str(ajustes['colores']).replace("'", '"')
            elemento = self.medidores['medidor' + str(index)]
            seccion = "Medidor" + str(index)
        else:
            elemento = self.graficos['grafico' + str(index)]
            seccion = "Grafico" + str(index)
        elemento.set_ajustes(ajustes)
        subsecciones = list(ajustes)
        self.guardar_config(seccion,subsecciones, ajustes)
        if tipo_accion == 'aceptar':
            self.desplegar_ajustes(elemento)

    def desplegar_ajustes(self, elemento):
        """Desplegar/ocultar los ajustes de un medidor o gráfico"""
        index = elemento.index
        if not self.paginaFlag:
            container = self.medidores['medidor' + str(index) + "_container"] 
        else:
            container = self.graficos['grafico' + str(index) + "_container"]
        if elemento.flag:
            container.grid_remove()
        else:
            container.grid()
        elemento.flag = not elemento.flag