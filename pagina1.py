import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

import medidor as Medidor
import indicador as Indicador


class Pagina1(tk.Frame):
    def __init__(self, master):
        super(Pagina1, self).__init__()
        # Obtener ancho/alto de la pantalla
        self.ancho_total = master.winfo_screenwidth()
        self.altura_total = master.winfo_screenheight()
        # Elementos
        self.master = master
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        self.mainContainer = tk.Frame(self.master)
        self.mainContainer.grid(column=0, row=0)


        # Medidores ****************************************************************************************************
        n_medidores = 5
        ancho_medidor = self.ancho_total / n_medidores
        altura_medidor = self.altura_total/ n_medidores*2
        # [Título, descripción, unidad, ancho, altura, minimo, maximo, intervalo, color_bajo, color_medio, color_alto]
        configuracion_medidor = [
            {"nombre": "Presión", "unidad": "Pa", "ancho": ancho_medidor, "altura": altura_medidor, "minimo": 0,
             "maximo": 100,"intervalo": 3000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Par", "unidad": "N*m", "ancho": ancho_medidor, "altura": altura_medidor, "minimo": 0,
             "maximo": 100, "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "V. angular", "unidad": "rad/s", "ancho": ancho_medidor, "altura": altura_medidor, "minimo": 0,
             "maximo": 100, "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Ángulo cig", "unidad": "º", "ancho": ancho_medidor, "altura": altura_medidor, "minimo": 0,
             "maximo": 100, "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Potencia", "unidad": "W", "ancho": ancho_medidor, "altura": altura_medidor, "minimo": 0,
             "maximo": 100, "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"}
        ]
        filas = [0, 0, 1, 1, 1]
        columnas = [2, 4, 1, 3, 5]
        i = 0
        self.medidores = [0]*n_medidores
        while i < len(configuracion_medidor):
            altura = configuracion_medidor[i]['altura']
            ancho = configuracion_medidor[i]['ancho']
            self.medidores[i] = Medidor.Medidor(self.mainContainer, configuracion=configuracion_medidor[i],
                bd=2, height=altura, width=ancho, bg='white', highlightbackground="black")
            self.medidores[i].grid(column=columnas[i], row=filas[i], columnspan=2,pady=10, padx=40)
            i += 1

        # Indicadores **************************************************************************************************
        n_indicadores = 8
        ancho_indicador = (self.ancho_total / n_indicadores) - n_indicadores*2
        altura_indicador = self.altura_total / n_indicadores
        # [Título, descripción, unidad, ancho, altura, minimo, maximo, intervalo, color_bajo, color_medio, color_alto]
        configuracion_indicador = [
            {"nombre": "Presión", "unidad": "Pa", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 3000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Par", "unidad": "rad/s", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Vuelta de cigüeñal", "unidad": "rad/s", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "I/vuelta", "unidad": "rad/s", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "ω instantánea", "unidad": "Pa", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 3000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "ω promedio/vuelta", "unidad": "rad/s", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Volumen", "unidad": "m^3", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Potencia", "unidad": "W", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"}
        ]
        i = 0
        self.indicadores = [0]*n_indicadores
        while i < len(configuracion_indicador):
            altura = configuracion_indicador[i]['altura']
            ancho = configuracion_indicador[i]['ancho']
            self.indicadores[i] = Indicador.Indicador(self.mainContainer,
                bd=2,height=altura,width=ancho, bg='white',highlightbackground="black",
                configuracion=configuracion_indicador[i])
            self.indicadores[i].grid(row=2, column=i)
            i += 1

        # Botón de salir ***********************************************************************************************
        self.salirButton = tk.Button(self.mainContainer, text='Salir', width=10, command=master.destroy)
        self.salirButton.grid(row=0, column=7, sticky="N")
        self.paginaButton = tk.Button(self.mainContainer, text="->", width=10, command=lambda: master.cambiar_pagina())
        self.paginaButton.grid(row=0, column=6, sticky="N")

    def set(self, valores):
        i = 0
        vuelta = valores["vuelta"]
        diente = valores["diente"]
        tiempo = valores["tiempo"]
        presion = valores["presion"]
        par = valores["par"]
        # Fórmulas matemáticas
        while i < len(self.medidores):
            self.medidores[i].set(vuelta)
            i += 1
