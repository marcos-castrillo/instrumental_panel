import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

import medidor as Medidor
import indicador as Indicador
import grafico as Grafico
import opciones as Opciones
import ajustes_medidores as AjustesMedidores

import json
import configparser
import os.path

class Main(tk.Frame):
    def __init__(self, master):
        super(Main, self).__init__()
        self.master = master
        # Leer el archivo de configuración
        self.configParser = configparser.RawConfigParser()
        self.configFile = 'settings.cfg'
        if not os.path.exists(self.configFile):
            self.create_config_file()
        self.configParser.read(self.configFile)
        # Obtener ancho/alto de la pantalla
        self.ancho_total = master.winfo_screenwidth()
        self.altura_total = master.winfo_screenheight()
        # Frame master
        self.master = master
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        # Resto de frames
        self.topContainer = tk.Frame(self.master)
        self.opcionesContainer = tk.Frame(self.master)
        self.medidoresContainer = tk.Frame(self.master)
        self.graficosContainer = tk.Frame(self.master)
        self.bottomContainer = tk.Frame(self.master)
        # Ajustar el lugar de los frames
        self.topContainer.grid(column=0, row=0)
        self.opcionesContainer.grid(column=0, row=0, rowspan=2, sticky="NW")
        self.medidoresContainer.grid(column=0, row=1)
        self.graficosContainer.grid(column=0, row=1)
        self.bottomContainer.grid(column=0, row=2)
        # Botones
        self.paginaButton_text = tk.StringVar()
        self.salirButton = tk.Button(self.topContainer, text='Salir', width=10, command=master.destroy)
        self.paginaButton = tk.Button(self.topContainer, textvariable=self.paginaButton_text, width=10, command=lambda: self.cambiar_pagina())
        self.ajustesButton = tk.Button(self.topContainer, text="Ajustes", width=10, command=lambda: self.desplegar_opciones())
        # Ajustar el lugar de los botones
        self.salirButton.grid(row=0, column=0, sticky="NE")
        self.paginaButton.grid(row=0, column=1, sticky="NE")
        self.ajustesButton.grid(row=0, column=2, sticky="NE")
        # Estado inicial de las variables
        self.paginaButton_text.set("Gráficos")
        self.paginaFlag = False
        self.opcionesFlag = False
        # Medidores ****************************************************************************************************
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
            "n_promedios": self.configParser.getint('Medidor0', 'n_promedios'),
            "colores": json.loads(self.configParser.get('Medidor0', 'colores')),
            "umbrales": json.loads(self.configParser.get('Medidor0', 'umbrales'))
        }
        medidor1_conf = {
            "nombre": self.configParser.get('Medidor1', 'nombre'),
            "unidad": self.configParser.get('Medidor1', 'unidad'),
            "minimo": self.configParser.getfloat('Medidor1', 'minimo'),
            "maximo": self.configParser.getfloat('Medidor1', 'maximo'),
            "n_promedios": self.configParser.getint('Medidor1', 'n_promedios'),
            "colores": json.loads(self.configParser.get('Medidor1', 'colores')),
            "umbrales": json.loads(self.configParser.get('Medidor1', 'umbrales'))
        }
        medidor2_conf = {
            "nombre": self.configParser.get('Medidor2', 'nombre'),
            "unidad": self.configParser.get('Medidor2', 'unidad'),
            "minimo": self.configParser.getfloat('Medidor2', 'minimo'),
            "maximo": self.configParser.getfloat('Medidor2', 'maximo'),
            "n_promedios": self.configParser.getint('Medidor2', 'n_promedios'),
            "colores": json.loads(self.configParser.get('Medidor2', 'colores')),
            "umbrales": json.loads(self.configParser.get('Medidor2', 'umbrales'))
        }
        medidor3_conf = {
            "nombre": self.configParser.get('Medidor3', 'nombre'),
            "unidad": self.configParser.get('Medidor3', 'unidad'),
            "minimo": self.configParser.getfloat('Medidor3', 'minimo'),
            "maximo": self.configParser.getfloat('Medidor3', 'maximo'),
            "n_promedios": self.configParser.getint('Medidor3', 'n_promedios'),
            "colores": json.loads(self.configParser.get('Medidor3', 'colores')),
            "umbrales": json.loads(self.configParser.get('Medidor3', 'umbrales'))
        }
        medidor4_conf = {
            "nombre": self.configParser.get('Medidor4', 'nombre'),
            "unidad": self.configParser.get('Medidor4', 'unidad'),
            "minimo": self.configParser.getfloat('Medidor4', 'minimo'),
            "maximo": self.configParser.getfloat('Medidor4', 'maximo'),
            "n_promedios": self.configParser.getint('Medidor4', 'n_promedios'),
            "colores": json.loads(self.configParser.get('Medidor4', 'colores')),
            "umbrales": json.loads(self.configParser.get('Medidor4', 'umbrales'))
        }
        # Flags para controlar el mostrar u ocultar la ventana de ajustes
        medidor0_flag = False
        medidor1_flag = False
        medidor2_flag = False
        medidor3_flag = False
        medidor4_flag = False
        # Medidores
        ancho_medidor = self.ancho_total / self.n_medidores
        altura_medidor = self.altura_total/ self.n_medidores*2
        medidor0 = Medidor.Medidor(self.medidoresContainer, bd=2, height=altura_medidor, width=ancho_medidor, bg='white', highlightbackground="black", configuracion=medidor0_conf)
        medidor1 = Medidor.Medidor(self.medidoresContainer, bd=2, height=altura_medidor, width=ancho_medidor, bg='white', highlightbackground="black", configuracion=medidor1_conf)
        medidor2 = Medidor.Medidor(self.medidoresContainer, bd=2, height=altura_medidor, width=ancho_medidor, bg='white', highlightbackground="black", configuracion=medidor2_conf)
        medidor3 = Medidor.Medidor(self.medidoresContainer ,bd=2, height=altura_medidor, width=ancho_medidor, bg='white', highlightbackground="black", configuracion=medidor3_conf)
        medidor4 = Medidor.Medidor(self.medidoresContainer, bd=2, height=altura_medidor, width=ancho_medidor, bg='white', highlightbackground="black", configuracion=medidor4_conf)
        # Frame de la ventana de ajustes de cada medidor
        medidor0_container = tk.Frame(self.medidoresContainer)
        medidor1_container = tk.Frame(self.medidoresContainer)
        medidor2_container = tk.Frame(self.medidoresContainer)
        medidor3_container = tk.Frame(self.medidoresContainer)
        medidor4_container = tk.Frame(self.medidoresContainer)
        # Botones de ajustes
        medidor0_button = tk.Button(self.medidoresContainer, text="Ajustes", image=self.image_medidor_button, command=lambda: self.desplegar_ajustes_medidores(medidor0_container))
        medidor1_button = tk.Button(self.medidoresContainer, text="Ajustes", image=self.image_medidor_button, command=lambda: self.desplegar_ajustes_medidores(medidor1_container))
        medidor2_button = tk.Button(self.medidoresContainer, text="Ajustes", image=self.image_medidor_button, command=lambda: self.desplegar_ajustes_medidores(medidor2_container))
        medidor3_button = tk.Button(self.medidoresContainer, text="Ajustes", image=self.image_medidor_button, command=lambda: self.desplegar_ajustes_medidores(medidor3_container))
        medidor4_button = tk.Button(self.medidoresContainer, text="Ajustes", image=self.image_medidor_button, command=lambda: self.desplegar_ajustes_medidores(medidor4_container))
        # Configuración de los ajustes los medidores
        medidor0_ajustes_conf = {"n_promedios": medidor0_conf["n_promedios"], "colores": medidor0_conf["colores"], "umbrales": medidor0_conf["umbrales"], "minimo": medidor0_conf["minimo"], "maximo": medidor0_conf["maximo"]}
        medidor1_ajustes_conf = {"n_promedios": medidor1_conf["n_promedios"], "colores": medidor1_conf["colores"], "umbrales": medidor1_conf["umbrales"], "minimo": medidor1_conf["minimo"], "maximo": medidor1_conf["maximo"]}
        medidor2_ajustes_conf = {"n_promedios": medidor2_conf["n_promedios"], "colores": medidor2_conf["colores"], "umbrales": medidor2_conf["umbrales"], "minimo": medidor2_conf["minimo"], "maximo": medidor2_conf["maximo"]}
        medidor3_ajustes_conf = {"n_promedios": medidor3_conf["n_promedios"], "colores": medidor3_conf["colores"], "umbrales": medidor3_conf["umbrales"], "minimo": medidor3_conf["minimo"], "maximo": medidor3_conf["maximo"]}
        medidor4_ajustes_conf = {"n_promedios": medidor4_conf["n_promedios"], "colores": medidor4_conf["colores"], "umbrales": medidor4_conf["umbrales"], "minimo": medidor4_conf["minimo"], "maximo": medidor4_conf["maximo"]}
        # Ajustes de los medidores
        medidor0_ajustes = AjustesMedidores.AjustesMedidores(medidor0_container, self, master, configuracion=medidor0_ajustes_conf)
        medidor1_ajustes = AjustesMedidores.AjustesMedidores(medidor1_container, self, master, configuracion=medidor1_ajustes_conf)
        medidor2_ajustes = AjustesMedidores.AjustesMedidores(medidor2_container, self, master, configuracion=medidor2_ajustes_conf)
        medidor3_ajustes = AjustesMedidores.AjustesMedidores(medidor3_container, self, master, configuracion=medidor3_ajustes_conf)
        medidor4_ajustes = AjustesMedidores.AjustesMedidores(medidor4_container, self, master, configuracion=medidor4_ajustes_conf)
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
        medidor4_container.grid(column=5, row=1, columnspan=2)
        medidor4_container.grid_remove()
        # Ajustar el lugar del contenido de cada frame de ajustes
        medidor0_ajustes.grid(row=0, column=0)
        medidor1_ajustes.grid(row=0, column=0)
        medidor2_ajustes.grid(row=0, column=0)
        medidor3_ajustes.grid(row=0, column=0,)
        medidor4_ajustes.grid(row=0, column=0)
        # Ajustar el lugar de los botones
        medidor0_button.grid(column=2, row=0, columnspan=2, sticky="NE")
        medidor1_button.grid(column=4, row=0, columnspan=2, sticky="NE")
        medidor2_button.grid(column=1, row=1, columnspan=2, sticky="NE")
        medidor3_button.grid(column=3, row=1, columnspan=2, sticky="NE")
        medidor4_button.grid(column=5, row=1, columnspan=2, sticky="NE")
        # Crear el diccionario de medidores
        self.medidores = {
            'medidor0': medidor0, 'medidor0_flag': medidor0_flag, 'medidor0_ajustes': medidor0_ajustes,
            'medidor1': medidor1, 'medidor1_flag': medidor1_flag, 'medidor1_ajustes': medidor1_ajustes,
            'medidor2': medidor2, 'medidor2_flag': medidor2_flag, 'medidor2_ajustes': medidor2_ajustes,
            'medidor3': medidor3, 'medidor3_flag': medidor3_flag, 'medidor3_ajustes': medidor3_ajustes,
            'medidor4': medidor4, 'medidor4_flag': medidor4_flag, 'medidor4_ajustes': medidor4_ajustes,
        }

        # Indicadores **************************************************************************************************
        n_indicadores = 8
        ancho_indicador = (self.ancho_total / n_indicadores) - n_indicadores*2
        altura_indicador = self.altura_total / n_indicadores
        # [Título, descripción, unidad, ancho, altura, minimo, maximo, intervalo, color_bajo, color_medio, color_alto]
        configuracion_indicador = [
            {"nombre": "Presión", "unidad": "Pa", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 3000, "color_bajo": "green", "color_medio": "yellow", "color_alto": "red"},
            {"nombre": "Par", "unidad": "rad/s", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "yellow", "color_alto": "red"},
            {"nombre": "Vuelta de cigüeñal", "unidad": "rad/s", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "yellow", "color_alto": "red"},
            {"nombre": "I/vuelta", "unidad": "rad/s", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "yellow", "color_alto": "red"},
            {"nombre": "ω instantánea", "unidad": "Pa", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 3000, "color_bajo": "green", "color_medio": "yellow", "color_alto": "red"},
            {"nombre": "ω promedio/vuelta", "unidad": "rad/s", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "yellow", "color_alto": "red"},
            {"nombre": "Volumen", "unidad": "m^3", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "yellow", "color_alto": "red"},
            {"nombre": "Potencia", "unidad": "W", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "yellow", "color_alto": "red"}
        ]
        i = 0
        self.indicadores = [0]*n_indicadores
        while i < len(configuracion_indicador):
            altura = configuracion_indicador[i]['altura']
            ancho = configuracion_indicador[i]['ancho']
            self.indicadores[i] = Indicador.Indicador(self.bottomContainer,
                bd=2,height=altura,width=ancho, bg='white', highlightbackground="black",
                configuracion=configuracion_indicador[i])
            self.indicadores[i].grid(row=2, column=i, padx=5)
            i += 1

        # Gráficos **************************************************************************************************
        n_graficos = 5
        ancho_grafico = self.ancho_total / n_graficos
        altura_grafico = self.altura_total / n_graficos*2
        configuracion_grafico = [
            {"nombreX": "Nº de grado de cigüeñal", "nombreY": "Presión/Par",
             "ancho": ancho_grafico, "altura": altura_grafico, "intervalo": 3000},
            {"nombreX": "Volumen", "nombreY": "Presión",
             "ancho": ancho_grafico, "altura": altura_grafico, "intervalo": 3000},
            {"nombreX": "ω promedio/vuelta", "nombreY": "Potencia/vuelta",
             "ancho": ancho_grafico, "altura": altura_grafico,"intervalo": 3000},
            {"nombreX": "Volumen", "nombreY": "Presión",
             "ancho": ancho_grafico, "altura": altura_grafico, "intervalo": 3000},
            {"nombreX": "ω promedio/vuelta", "nombreY": "Potencia/vuelta",
             "ancho": ancho_grafico, "altura": altura_grafico, "intervalo": 3000}
        ]
        i = 0
        filas = [0, 0, 1, 1, 1]
        columnas = [2, 4, 1, 3, 5]
        self.graficos = [0] * n_graficos
        while i < len(configuracion_grafico):
            self.graficos[i] = Grafico.Grafico(self.graficosContainer, configuracion=configuracion_grafico[i])
            self.graficos[i].grid(row=filas[i], column=columnas[i], columnspan=2, padx=20, pady=10)
            i += 1
        self.graficosContainer.grid_remove()
        # OpcionesContainer ******************************************************************************************************
        configuracion_opciones = {"intervalo": self.master.intervalo}
        self.ajustes = Opciones.Opciones(self.opcionesContainer, master, configuracion=configuracion_opciones)
        self.ajustes.grid(row=0, column=0)
        self.opcionesContainer.grid_remove()

    def create_config_file(self):
        """Crea un archivo de configuración si no existe"""
        self.configParser.add_section('Medidor0')
        self.configParser.set('Medidor0', 'nombre', 'Presión')
        self.configParser.set('Medidor0', 'unidad', 'Pa')
        self.configParser.set('Medidor0', 'minimo', '0')
        self.configParser.set('Medidor0', 'maximo', '100')
        self.configParser.set('Medidor0', 'n_promedios', '20')
        self.configParser.set('Medidor0', 'colores', '["green", "yellow", "red"]')
        self.configParser.set('Medidor0', 'umbrales', '[0, 33, 66, 100]')
        self.configParser.add_section('Medidor1')
        self.configParser.set('Medidor1', 'nombre', 'Par')
        self.configParser.set('Medidor1', 'unidad', 'N*m')
        self.configParser.set('Medidor1', 'minimo', '0')
        self.configParser.set('Medidor1', 'maximo', '100')
        self.configParser.set('Medidor1', 'n_promedios', '20')
        self.configParser.set('Medidor1', 'colores', '["green", "yellow", "red"]')
        self.configParser.set('Medidor1', 'umbrales', '[0, 33, 66, 100]')
        self.configParser.add_section('Medidor2')
        self.configParser.set('Medidor2', 'nombre', 'V. angular')
        self.configParser.set('Medidor2', 'unidad', 'rad/s')
        self.configParser.set('Medidor2', 'minimo', '0')
        self.configParser.set('Medidor2', 'maximo', '100')
        self.configParser.set('Medidor2', 'n_promedios', '20')
        self.configParser.set('Medidor2', 'colores', '["green", "yellow", "red"]')
        self.configParser.set('Medidor2', 'umbrales', '[0, 33, 66, 100]')
        self.configParser.add_section('Medidor3')
        self.configParser.set('Medidor3', 'nombre', 'Áng. cig.')
        self.configParser.set('Medidor3', 'unidad', 'º')
        self.configParser.set('Medidor3', 'minimo', '0')
        self.configParser.set('Medidor3', 'maximo', '100')
        self.configParser.set('Medidor3', 'n_promedios', '20')
        self.configParser.set('Medidor3', 'colores', '["green", "yellow", "red"]')
        self.configParser.set('Medidor3', 'umbrales', '[0, 33, 66, 100]')
        self.configParser.add_section('Medidor4')
        self.configParser.set('Medidor4', 'nombre', 'Potencia')
        self.configParser.set('Medidor4', 'unidad', 'W')
        self.configParser.set('Medidor4', 'minimo', '0')
        self.configParser.set('Medidor4', 'maximo', '100')
        self.configParser.set('Medidor4', 'n_promedios', '20')
        self.configParser.set('Medidor4', 'colores', '["green", "yellow", "red"]')
        self.configParser.set('Medidor4', 'umbrales', '[0, 33, 66, 100]')
        with open(self.configFile, 'w') as output:
            self.configParser.write(output)

    def save_config_medidor(self, seccion, config):
        """Guarda la nueva configuración del medidor"""
        if not self.configParser.has_section(seccion):
            self.configParser.add_section(seccion)
        self.configParser.set(seccion, 'n_promedios', config['n_promedios'])
        config['colores'] = str(config['colores']).replace("'", '"')
        self.configParser.set(seccion, 'colores', config['colores'])
        self.configParser.set(seccion, 'umbrales', config['umbrales'])
        self.configParser.set(seccion, 'minimo', config['minimo'])
        self.configParser.set(seccion, 'maximo', config['maximo'])
        with open(self.configFile, 'w') as output:
            self.configParser.write(output)

    def cambiar_pagina(self):
        if self.paginaFlag:
            self.graficosContainer.grid_remove()
            self.medidoresContainer.grid()
            self.paginaButton_text.set("Gráficos")
        else:
            self.graficosContainer.grid()
            self.medidoresContainer.grid_remove()
            self.paginaButton_text.set("Medidores")
        self.paginaFlag = not self.paginaFlag

    def desplegar_opciones(self):
        if self.opcionesFlag:
            self.opcionesContainer.grid_remove()
        else:
            self.opcionesContainer.grid()
        self.opcionesFlag = not self.opcionesFlag

    def desplegar_ajustes_medidores(self, ajustes_medidores_container):
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

    def set(self, valores):
        vuelta = valores["vuelta"]
        diente = valores["diente"]
        tiempo = valores["tiempo"]
        presion = valores["presion"]
        par = valores["par"]
        # Fórmulas matemáticas
        for i in range(0, self.n_medidores):
            self.medidores['medidor' + str(i)].set(vuelta)
        i = 0
        while i < len(self.indicadores):
            self.indicadores[i].set(vuelta)
            i += 1

    def save_ajustes_medidor(self, medidor, ajustes):
        # Obtener los ajustes
        n_promedios = int(ajustes['n_promedios'])
        colores = ajustes['colores']
        umbrales_str = ajustes['umbrales']
        umbrales = [int(numeric_string) for numeric_string in umbrales_str]
        minimo_rango = float(ajustes['minimo'])
        maximo_rango = float(ajustes['maximo'])
        # Obtiene el número del frame en el que está el medidor:
        # (.!frame3.!frame, .!frame3.!frame2, .!frame3.!frame3, .!frame3.!frame4, .!frame3.!frame5 ...)
        # Se obtiene la última letra. Si es "e", es el frame 0. Si no, hay que restar 1.
        medidor_index = str(medidor.master)[-1:]
        if medidor_index == 'e':
            medidor_index = 1
        self.medidores['medidor' + str(int(medidor_index) - 1)].n_promedios = n_promedios
        self.medidores['medidor' + str(int(medidor_index) - 1)].colores = colores
        self.medidores['medidor' + str(int(medidor_index) - 1)].umbrales = umbrales
        self.medidores['medidor' + str(int(medidor_index) - 1)].minimo_rango = minimo_rango
        self.medidores['medidor' + str(int(medidor_index) - 1)].maximo_rango = maximo_rango
        self.medidores['medidor' + str(int(medidor_index) - 1)].set_ajustes()
        self.medidores['medidor' + str(int(medidor_index) - 1) + '_ajustes'].n_promedios = n_promedios
        self.medidores['medidor' + str(int(medidor_index) - 1) + '_ajustes'].colores = colores
        self.medidores['medidor' + str(int(medidor_index) - 1) + '_ajustes'].umbrales = umbrales
        self.medidores['medidor' + str(int(medidor_index) - 1) + '_ajustes'].minimo = minimo_rango
        self.medidores['medidor' + str(int(medidor_index) - 1) + '_ajustes'].maximo = maximo_rango
        self.medidores['medidor' + str(int(medidor_index) - 1) + '_ajustes'].set_ajustes()
        self.save_config_medidor("Medidor" + str(int(medidor_index) - 1), ajustes)
