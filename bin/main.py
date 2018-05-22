import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
    import Tkinter.font as tkf
else:
    import tkinter as tk
    import tkinter.font as tkf

from tkinter import filedialog

import bin.medidor as medidor
import bin.engranaje as engranaje
import bin.indicador as indicador
import bin.grafico as grafico
import bin.opciones as opciones
import bin.ajustes_medidores as ajustes_medidores

import math
import json
import configparser
import os.path
import csv

class Main(tk.Frame):
    def __init__(self, master):
        super(Main, self).__init__()
        self.master = master
        self.init()

    def init(self):
        # Configurar la aplicación
        self.crear_elementos()
        # Estado inicial de las variables
        self.paginaFlag = False
        self.opcionesFlag = False
        self.intervalo = self.master.intervalo
        self.vuelta = 0
        self.diente = 0
        self.vuelta_actual = 0
        self.cambio_vuelta = False
        # Leer el archivo de configuración
        self.configParser = configparser.RawConfigParser()
        self.configFile = 'settings.ini'
        if not os.path.exists(self.configFile):
            self.create_config_file()
        self.configParser.read(self.configFile)
        # Crear elementos gráficos
        self.crear_medidores()
        self.crear_indicadores()
        self.crear_graficos()
        self.crear_opciones()

    def crear_elementos(self):
        # Obtener ancho/alto de la pantalla
        self.ancho_total = self.master.winfo_screenwidth()
        self.altura_total = self.master.winfo_screenheight()
        # Frame master
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        # Resto de frames
        self.menuContainer = tk.Frame(self.master)
        self.opcionesContainer = tk.Frame(self.master)
        self.medidoresContainer = tk.Frame(self.master)
        self.graficosContainer = tk.Frame(self.master)
        self.indicadoresContainer = tk.Frame(self.master)
        # Ajustar el lugar de los frames
        self.opcionesContainer.grid(column=0, row=0, rowspan=2, sticky="NW")
        self.medidoresContainer.grid(column=0, row=0)
        self.graficosContainer.grid(column=0, row=0)
        self.menuContainer.grid(column=1, row=0, sticky="N")
        self.indicadoresContainer.grid(column=0, row=1, sticky="S", columnspan=2)
        # Botones
        stop = tk.PhotoImage(file='images/stop.png')
        play = tk.PhotoImage(file='images/play.png')
        record = tk.PhotoImage(file='images/record.png')
        pause = tk.PhotoImage(file='images/pause.png')
        open = tk.PhotoImage(file='images/open.png')
        reset = tk.PhotoImage(file='images/reset.png')
        ajustes = tk.PhotoImage(file='images/opciones.png')
        grafico = tk.PhotoImage(file='images/chart.png')
        medidor = tk.PhotoImage(file='images/gauge.png')
        salir = tk.PhotoImage(file='images/exit.png')
        self.paginaMedidoresButton = tk.Button(self.menuContainer, bg='white', text='Medidores', image=medidor, command=self.cambiar_pagina, compound="top")
        self.paginaMedidoresButton.image = medidor
        self.paginaGraficosButton = tk.Button(self.menuContainer, bg='white', text='Gráficos', image=grafico, command=self.cambiar_pagina, compound="top")
        self.paginaGraficosButton.image = grafico
        self.ajustesButton = tk.Button(self.menuContainer, bg='white', text='Ajustes', image=ajustes, command=self.desplegar_opciones, compound="top")
        self.ajustesButton.image = ajustes
        self.salirButton = tk.Button(self.menuContainer, bg='white', text='Salir', image=salir, command=self.master.destroy, compound="top")
        self.salirButton.image = salir
        self.stopButton = tk.Button(self.menuContainer, bg='white', text='Parar y guardar', image = stop, command=self.master.stop,compound="top")
        self.stopButton.image = stop
        self.playButton = tk.Button(self.menuContainer, bg='white', text='Reanudar', image = play, command=self.master.play,compound="top")
        self.playButton.image = play
        self.pauseButton = tk.Button(self.menuContainer, bg='white', text='Pausar', image = pause, command=self.master.pause,compound="top")
        self.pauseButton.image = pause
        self.recordButton = tk.Button(self.menuContainer, bg='white', text='Grabar', image = record, command=self.master.record,compound="top")
        self.recordButton.image = record
        self.openButton = tk.Button(self.menuContainer, bg='white', text='Abrir archivo', image = open, command=self.master.open,compound="top")
        self.openButton.image = open
        self.resetButton = tk.Button(self.menuContainer, bg='white', text='Reiniciar datos', image = reset, command=self.master.reset,compound="top")
        self.resetButton.image = reset
        # Ajustar el lugar de los botones
        self.stopButton.grid(row=0, column=0, pady=5)
        self.stopButton.configure(state='disabled')
        self.playButton.grid(row=0, column=1, pady=5)
        self.pauseButton.grid(row=0, column=1, pady=5)
        self.playButton.grid_remove()
        self.recordButton.grid(row=0, column=2, pady=5)
        self.openButton.grid(row=1, column=0, pady=5)
        self.resetButton.grid(row=1, column=1, pady=5)
        self.paginaMedidoresButton.grid(row=2, column=0, pady=5)
        self.paginaGraficosButton.grid(row=2, column=0, pady=5)
        self.paginaMedidoresButton.grid_remove()
        self.ajustesButton.grid(row=2, column=1, pady=5)
        self.salirButton.grid(row=2, column=2, pady=5)

    def crear_medidores(self):
        # Inicializar las variables
        self.image_medidor_button = tk.PhotoImage(file="images/ajustes.png")
        # Configuración de cada medidor
        # Si se quiere cambiar el nº de colores (3 por defecto), basta con modificar en las conf. siguientes
        # las variables "colores" y "umbrales" de forma adecuada
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
        medidor0 = medidor.Medidor(self.medidoresContainer, bd=2, height=altura_medidor, width=ancho_medidor, bg='white', highlightbackground="black", configuracion=medidor0_conf)
        medidor1 = medidor.Medidor(self.medidoresContainer, bd=2, height=altura_medidor, width=ancho_medidor, bg='white', highlightbackground="black", configuracion=medidor1_conf)
        medidor2 = medidor.Medidor(self.medidoresContainer, bd=2, height=altura_medidor, width=ancho_medidor, bg='white', highlightbackground="black", configuracion=medidor2_conf)
        medidor3 = medidor.Medidor(self.medidoresContainer, bd=2, height=altura_medidor, width=ancho_medidor, bg='white', highlightbackground="black", configuracion=medidor3_conf)
        medidor4 = engranaje.Engranaje(self.medidoresContainer ,bd=2, height=altura_medidor, width=ancho_medidor, bg='white', highlightbackground="black", configuracion=medidor4_conf)
        # Frame de la ventana de ajustes de cada medidor
        medidor0_container = tk.Frame(self.medidoresContainer)
        medidor1_container = tk.Frame(self.medidoresContainer)
        medidor2_container = tk.Frame(self.medidoresContainer)
        medidor3_container = tk.Frame(self.medidoresContainer)
        # Botones de ajustes
        medidor0_button = tk.Button(self.medidoresContainer, text="Ajustes", image=self.image_medidor_button, command=lambda: self.desplegar_ajustes_medidores(medidor0_container))
        medidor1_button = tk.Button(self.medidoresContainer, text="Ajustes", image=self.image_medidor_button, command=lambda: self.desplegar_ajustes_medidores(medidor1_container))
        medidor2_button = tk.Button(self.medidoresContainer, text="Ajustes", image=self.image_medidor_button, command=lambda: self.desplegar_ajustes_medidores(medidor2_container))
        medidor3_button = tk.Button(self.medidoresContainer, text="Ajustes", image=self.image_medidor_button, command=lambda: self.desplegar_ajustes_medidores(medidor3_container))
        # Configuración de los ajustes los medidores
        medidor0_ajustes_conf = {"nombre": medidor0_conf["nombre"], "unidad": medidor0_conf["unidad"], "colores": medidor0_conf["colores"], "umbrales_porc": medidor0_conf["umbrales_porc"], "umbrales_val": medidor0_conf["umbrales_val"], "tipo_umbral": medidor0_conf["tipo_umbral"], "minimo": medidor0_conf["minimo"], "maximo": medidor0_conf["maximo"]}
        medidor1_ajustes_conf = {"nombre": medidor1_conf["nombre"], "unidad": medidor1_conf["unidad"], "colores": medidor1_conf["colores"], "umbrales_porc": medidor1_conf["umbrales_porc"], "umbrales_val": medidor1_conf["umbrales_val"], "tipo_umbral": medidor1_conf["tipo_umbral"], "minimo": medidor1_conf["minimo"], "maximo": medidor1_conf["maximo"]}
        medidor2_ajustes_conf = {"nombre": medidor2_conf["nombre"], "unidad": medidor2_conf["unidad"], "colores": medidor2_conf["colores"], "umbrales_porc": medidor2_conf["umbrales_porc"], "umbrales_val": medidor2_conf["umbrales_val"], "tipo_umbral": medidor2_conf["tipo_umbral"], "minimo": medidor2_conf["minimo"], "maximo": medidor2_conf["maximo"]}
        medidor3_ajustes_conf = {"nombre": medidor3_conf["nombre"], "unidad": medidor3_conf["unidad"], "colores": medidor3_conf["colores"], "umbrales_porc": medidor3_conf["umbrales_porc"], "umbrales_val": medidor3_conf["umbrales_val"], "tipo_umbral": medidor3_conf["tipo_umbral"], "minimo": medidor3_conf["minimo"], "maximo": medidor3_conf["maximo"]}
        # Ajustes de los medidores
        medidor0_ajustes = ajustes_medidores.AjustesMedidores(medidor0_container, self, self.master, configuracion=medidor0_ajustes_conf)
        medidor1_ajustes = ajustes_medidores.AjustesMedidores(medidor1_container, self, self.master, configuracion=medidor1_ajustes_conf)
        medidor2_ajustes = ajustes_medidores.AjustesMedidores(medidor2_container, self, self.master, configuracion=medidor2_ajustes_conf)
        medidor3_ajustes = ajustes_medidores.AjustesMedidores(medidor3_container, self, self.master, configuracion=medidor3_ajustes_conf)
        # Ajustar el lugar de cada medidor
        medidor0.grid(column=2, row=0, columnspan=2)
        medidor1.grid(column=4, row=0, columnspan=2)
        medidor2.grid(column=1, row=1, columnspan=2)
        medidor3.grid(column=3, row=1, columnspan=2)
        medidor4.grid(column=5, row=1, columnspan=2)
        # Ajustar el lugar de cada ventana de ajustes
        medidor0_container.grid(column=2, row=0, columnspan=2)
        medidor0_container.grid_remove()
        medidor1_container.grid(column=4, row=0, columnspan=2)
        medidor1_container.grid_remove()
        medidor2_container.grid(column=1, row=1, columnspan=2)
        medidor2_container.grid_remove()
        medidor3_container.grid(column=3, row=1, columnspan=2)
        medidor3_container.grid_remove()
        # Ajustar el lugar del contenido de cada frame de ajustes
        medidor0_ajustes.grid(row=0, column=0)
        medidor1_ajustes.grid(row=0, column=0)
        medidor2_ajustes.grid(row=0, column=0)
        medidor3_ajustes.grid(row=0, column=0,)
        # Ajustar el lugar de los botones
        medidor0_button.grid(column=2, row=0, columnspan=2, sticky="NE")
        medidor1_button.grid(column=4, row=0, columnspan=2, sticky="NE")
        medidor2_button.grid(column=1, row=1, columnspan=2, sticky="NE")
        medidor3_button.grid(column=3, row=1, columnspan=2, sticky="NE")
        # Crear el diccionario de medidores
        self.medidores = {
            'medidor0': medidor0, 'medidor0_flag': medidor0_flag, 'medidor0_ajustes': medidor0_ajustes,
            'medidor1': medidor1, 'medidor1_flag': medidor1_flag, 'medidor1_ajustes': medidor1_ajustes,
            'medidor2': medidor2, 'medidor2_flag': medidor2_flag, 'medidor2_ajustes': medidor2_ajustes,
            'medidor3': medidor3, 'medidor3_flag': medidor3_flag, 'medidor3_ajustes': medidor3_ajustes,
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
        altura_indicador = self.altura_total / self.n_indicadores
        indicador0 = indicador.Indicador(self.indicadoresContainer, bd=2, height=altura_indicador, width=ancho_indicador, bg='white', highlightbackground="black",configuracion=indicador0_conf)
        indicador1 = indicador.Indicador(self.indicadoresContainer, bd=2, height=altura_indicador, width=ancho_indicador, bg='white', highlightbackground="black",configuracion=indicador1_conf)
        indicador2 = indicador.Indicador(self.indicadoresContainer, bd=2, height=altura_indicador, width=ancho_indicador, bg='white', highlightbackground="black",configuracion=indicador2_conf)
        indicador3 = indicador.Indicador(self.indicadoresContainer, bd=2, height=altura_indicador, width=ancho_indicador, bg='white', highlightbackground="black",configuracion=indicador3_conf)
        indicador4 = indicador.Indicador(self.indicadoresContainer, bd=2, height=altura_indicador, width=ancho_indicador, bg='white', highlightbackground="black",configuracion=indicador4_conf)
        indicador5 = indicador.Indicador(self.indicadoresContainer, bd=2, height=altura_indicador, width=ancho_indicador, bg='white', highlightbackground="black",configuracion=indicador5_conf)
        indicador6 = indicador.Indicador(self.indicadoresContainer, bd=2, height=altura_indicador, width=ancho_indicador, bg='white', highlightbackground="black",configuracion=indicador6_conf)
        indicador7 = indicador.Indicador(self.indicadoresContainer, bd=2, height=altura_indicador, width=ancho_indicador, bg='white', highlightbackground="black",configuracion=indicador7_conf)
        # Ajustar el lugar de cada indicador
        indicador0.grid(row=2, column=0, padx=5)
        indicador1.grid(row=2, column=1, padx=5)
        indicador2.grid(row=2, column=2, padx=5)
        indicador3.grid(row=2, column=3, padx=5)
        indicador4.grid(row=2, column=4, padx=5)
        indicador5.grid(row=2, column=5, padx=5)
        indicador6.grid(row=2, column=6, padx=5)
        indicador7.grid(row=2, column=7, padx=5)
        # Crear el diccionario de indicadores
        self.indicadores = {
            'indicador0': indicador0, 'indicador1': indicador1, 'indicador2': indicador2, 'indicador3': indicador3,
            'indicador4': indicador4, 'indicador5': indicador5, 'indicador6': indicador6, 'indicador7': indicador7
        }

    def crear_graficos(self):
        # Configuración de cada gráfico
        self.n_graficos = 5
        grafico0_conf = {
            "nombreX": self.configParser.get('Grafico0', 'nombreX'),
            "nombreY": self.configParser.get('Grafico0', 'nombreY')
        }
        grafico1_conf = {
            "nombreX": self.configParser.get('Grafico1', 'nombreX'),
            "nombreY": self.configParser.get('Grafico1', 'nombreY')
        }
        grafico2_conf = {
            "nombreX": self.configParser.get('Grafico2', 'nombreX'),
            "nombreY": self.configParser.get('Grafico2', 'nombreY')
        }

        ancho_grafico = self.ancho_total / self.n_graficos
        altura_grafico = self.altura_total / self.n_graficos*2.5

        # Gráficos
        grafico0 = grafico.Grafico(self.graficosContainer, height=altura_grafico, width=ancho_grafico, configuracion=grafico0_conf)
        grafico1 = grafico.Grafico(self.graficosContainer, height=altura_grafico, width=ancho_grafico, configuracion=grafico1_conf)
        grafico2 = grafico.Grafico(self.graficosContainer, height=altura_grafico, width=ancho_grafico, configuracion=grafico2_conf)
        # Ajustar el lugar de cada gráfico
        grafico0.grid(row=0, column=3, columnspan=2, padx=20, pady=10)
        grafico1.grid(row=1, column=2, columnspan=2, padx=20, pady=10)
        grafico2.grid(row=1, column=4, columnspan=2, padx=20, pady=10)
        self.graficosContainer.grid_remove()
        # Crear el diccionario de indicadores
        self.graficos = {
            'grafico0': grafico0, 'grafico1': grafico1, 'grafico2': grafico2
        }

    def crear_opciones(self):
        configuracion_opciones = {"intervalo": self.master.intervalo}
        self.ajustes = opciones.Opciones(self.opcionesContainer, self.master, configuracion=configuracion_opciones)
        self.ajustes.grid(row=0, column=0)
        self.opcionesContainer.grid_remove()

    def create_config_file(self):
        """Crea un archivo de configuración si no existe"""
        self.configParser.add_section('Medidor0')
        self.configParser.set('Medidor0', 'nombre', 'Presión')
        self.configParser.set('Medidor0', 'unidad', 'atm')
        self.configParser.set('Medidor0', 'minimo', '0')
        self.configParser.set('Medidor0', 'maximo', '100')
        self.configParser.set('Medidor0', 'colores', '["green", "yellow", "red"]')
        self.configParser.set('Medidor0', 'umbrales_porc', '[33, 66]')
        self.configParser.set('Medidor0', 'umbrales_val', '[5, 20]')
        self.configParser.set('Medidor0', 'tipo_umbral', 'P')
        self.configParser.add_section('Medidor1')
        self.configParser.set('Medidor1', 'nombre', 'Par')
        self.configParser.set('Medidor1', 'unidad', 'N*m')
        self.configParser.set('Medidor1', 'minimo', '0')
        self.configParser.set('Medidor1', 'maximo', '100')
        self.configParser.set('Medidor1', 'colores', '["green", "yellow", "red"]')
        self.configParser.set('Medidor1', 'umbrales_porc', '[33, 66]')
        self.configParser.set('Medidor1', 'umbrales_val', '[5, 20]')
        self.configParser.set('Medidor1', 'tipo_umbral', 'P')
        self.configParser.add_section('Medidor2')
        self.configParser.set('Medidor2', 'nombre', 'Velocidad angular')
        self.configParser.set('Medidor2', 'unidad', 'rad/s')
        self.configParser.set('Medidor2', 'minimo', '0')
        self.configParser.set('Medidor2', 'maximo', '100')
        self.configParser.set('Medidor2', 'colores', '["green", "yellow", "red"]')
        self.configParser.set('Medidor2', 'umbrales_porc', '[33, 66]')
        self.configParser.set('Medidor2', 'umbrales_val', '[5, 20]')
        self.configParser.set('Medidor2', 'tipo_umbral', 'P')
        self.configParser.add_section('Medidor3')
        self.configParser.set('Medidor3', 'nombre', 'Potencia')
        self.configParser.set('Medidor3', 'unidad', 'W')
        self.configParser.set('Medidor3', 'minimo', '0')
        self.configParser.set('Medidor3', 'maximo', '100')
        self.configParser.set('Medidor3', 'colores', '["green", "yellow", "red"]')
        self.configParser.set('Medidor3', 'umbrales_porc', '[33, 66]')
        self.configParser.set('Medidor3', 'umbrales_val', '[5, 20]')
        self.configParser.set('Medidor3', 'tipo_umbral', 'P')
        self.configParser.add_section('Medidor4')
        self.configParser.set('Medidor4', 'nombre', 'Ángulo cigüeñal')
        self.configParser.set('Medidor4', 'unidad', 'º')
        self.configParser.set('Medidor4', 'minimo', '0')
        self.configParser.set('Medidor4', 'maximo', '360')
        self.configParser.add_section('Indicador0')
        self.configParser.set('Indicador0', 'nombre', 'Presión')
        self.configParser.set('Indicador0', 'unidad', 'atm')
        self.configParser.add_section('Indicador1')
        self.configParser.set('Indicador1', 'nombre', 'Par')
        self.configParser.set('Indicador1', 'unidad', 'rad/s')
        self.configParser.add_section('Indicador2')
        self.configParser.set('Indicador2', 'nombre', 'Vuelta')
        self.configParser.set('Indicador2', 'unidad', 'rad/s')
        self.configParser.add_section('Indicador3')
        self.configParser.set('Indicador3', 'nombre', 'I/vuelta')
        self.configParser.set('Indicador3', 'unidad', 'rad/s')
        self.configParser.add_section('Indicador4')
        self.configParser.set('Indicador4', 'nombre', 'w inst.')
        self.configParser.set('Indicador4', 'unidad', 'atm')
        self.configParser.add_section('Indicador5')
        self.configParser.set('Indicador5', 'nombre', 'w promedio/vuelta')
        self.configParser.set('Indicador5', 'unidad', 'rad/s')
        self.configParser.add_section('Indicador6')
        self.configParser.set('Indicador6', 'nombre', 'Volumen')
        self.configParser.set('Indicador6', 'unidad', 'm^3')
        self.configParser.add_section('Indicador7')
        self.configParser.set('Indicador7', 'nombre', 'Potencia')
        self.configParser.set('Indicador7', 'unidad', 'W')
        self.configParser.add_section('Grafico0')
        self.configParser.set('Grafico0', 'nombreX', 'Nº de grado de cigüeñal')
        self.configParser.set('Grafico0', 'nombreY', 'Presión/Par')
        self.configParser.add_section('Grafico1')
        self.configParser.set('Grafico1', 'nombreX', 'Volumen')
        self.configParser.set('Grafico1', 'nombreY', 'Presión')
        self.configParser.add_section('Grafico2')
        self.configParser.set('Grafico2', 'nombreX', 'w promedio/vuelta')
        self.configParser.set('Grafico2', 'nombreY', 'Potencia/vuelta')
        with open(self.configFile, 'w') as output:
            self.configParser.write(output)

    def save_config_medidor(self, seccion, config):
        """Guarda la nueva configuración del medidor"""
        if not self.configParser.has_section(seccion):
            self.configParser.add_section(seccion)
        config['colores'] = str(config['colores']).replace("'", '"')
        self.configParser.set(seccion, 'colores', config['colores'])
        self.configParser.set(seccion, 'umbrales_porc', config['umbrales_porc'])
        self.configParser.set(seccion, 'umbrales_val', config['umbrales_val'])
        self.configParser.set(seccion, 'tipo_umbral', config['tipo_umbral'])
        self.configParser.set(seccion, 'minimo', config['minimo'])
        self.configParser.set(seccion, 'maximo', config['maximo'])
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

    def desplegar_ajustes_medidores(self, ajustes_medidores_container):
        """Desplegar/ocultar los ajustes de un medidor específico"""
        # Obtiene el número del frame en el que está el medidor:
        # (.!frame3.!frame, .!frame3.!frame2, .!frame3.!frame3, .!frame3.!frame4, .!frame3.!frame5 ...)
        # Se obtiene la última letra. Si es "e", es el frame 0. Si no, hay que restar 1.
        medidor_index = str(ajustes_medidores_container)[-1:]
        if medidor_index == "e":
            medidor_index = 1
        if self.medidores['medidor' + str(int(medidor_index) - 1) + "_flag"]:
            ajustes_medidores_container.grid_remove()
        else:
            ajustes_medidores_container.grid()
        self.medidores['medidor' + str(int(medidor_index) - 1) + "_flag"] = not self.medidores['medidor' + str(int(medidor_index) - 1) + "_flag"]

    def set(self, valores, reiniciar):
        """Actualizar los valores en la UI"""
        self.cambio_vuelta = False
        vuelta = valores["vuelta"]
        diente = valores["diente"]
        periodo = valores["tiempo"]
        presion = valores["presion"]
        par = valores["par"]
        # Fórmulas matemáticas
        frecuencia_diente = 1/periodo
        frecuencia_vuelta = frecuencia_diente/360
        vel_angular = 2*math.pi*frecuencia_vuelta
        potencia = par*vel_angular
        volumen = 0
        # Medidor0: Presión
        # Medidor1: Par
        # Medidor2: Velocidad angular
        # Medidor3: Potencia
        # Medidor4: Ángulo de cigüeñal
        if reiniciar:
            self.medidores['medidor0'].valor_min = presion
            self.medidores['medidor0'].valor_max = presion
            self.medidores['medidor1'].valor_min = par
            self.medidores['medidor1'].valor_max = par
            self.medidores['medidor2'].valor_min = vel_angular
            self.medidores['medidor2'].valor_max = vel_angular
            self.medidores['medidor3'].valor_min = potencia
            self.medidores['medidor3'].valor_max = potencia
        if (vuelta > self.vuelta_actual) or (vuelta == 0 and diente == 1):
            self.vuelta_actual += 1
            self.cambio_vuelta = True
        self.medidores['medidor0'].set(presion, self.cambio_vuelta)
        self.medidores['medidor1'].set(par, self.cambio_vuelta)
        self.medidores['medidor2'].set(vel_angular, self.cambio_vuelta)
        self.medidores['medidor3'].set(potencia, self.cambio_vuelta)
        self.medidores['medidor4'].set(diente)
        # Indicador0: Presión
        # Indicador1: Par
        # Indicador2: Número de vuelta de cigüeñal
        # Indicador3: Número de impulso dentro de la vuelta (grados girados)
        # Indicador4: Velocidad angular instantánea
        # Indicador5: Velocidad angular promedio en una vuelta
        # Indicador6: Volumen
        # Indicador7: Potencia
        self.indicadores['indicador0'].set(presion, self.cambio_vuelta)
        self.indicadores['indicador1'].set(par, self.cambio_vuelta)
        self.indicadores['indicador2'].set(vuelta, self.cambio_vuelta)
        self.indicadores['indicador3'].set(diente, True)
        self.indicadores['indicador4'].set(vel_angular, True)
        self.indicadores['indicador5'].set(vel_angular, self.cambio_vuelta)
        self.indicadores['indicador6'].set(volumen, self.cambio_vuelta)
        self.indicadores['indicador7'].set(potencia, self.cambio_vuelta)
        # Gráfico 0: Eje X: nº grado cigüeñal, eje Y: Presión y par -> Gráfico móvil
        # Gráfico 1: Eje X: Volumen, eje Y: Presión -> Diagrama P-V
        # Gráfico 2: Eje X: Velocidad angular promedio de vuelta, eje Y: Potencia de vuelta
        self.graficos['grafico0'].set(diente, presion, self.cambio_vuelta)
        self.graficos['grafico1'].set(volumen, presion, self.cambio_vuelta)
        self.graficos['grafico2'].set(vel_angular, potencia, self.cambio_vuelta)

    def save_ajustes_medidor(self, medidor_x, ajustes, tipo_accion):
        """Guardar los ajustes de un medidor específico"""
        # Obtiene el número del frame en el que está el medidor:
        # (.!frame3.!frame, .!frame3.!frame2, .!frame3.!frame3, .!frame3.!frame4, .!frame3.!frame5 ...)
        # Se obtiene la última letra. Si es "e", es el frame 0. Si no, hay que restar 1.
        medidor_index = str(medidor_x.master)[-1:]
        if medidor_index == 'e':
            medidor_index = 1
        # Guardar los ajustes
        self.medidores['medidor' + str(int(medidor_index) - 1)].set_ajustes(ajustes)
        self.medidores['medidor' + str(int(medidor_index) - 1) + '_ajustes'].set_ajustes(ajustes)
        self.save_config_medidor("Medidor" + str(int(medidor_index) - 1), ajustes)
        if tipo_accion == 'aceptar':
            self.desplegar_ajustes_medidores(medidor_x.master)
