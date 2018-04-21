import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

import medidor as Medidor
import indicador as Indicador
import grafico as Grafico


class Pagina2(tk.Frame):
    def __init__(self, master):
        super(Pagina2, self).__init__()
        # Obtener ancho/alto de la pantalla
        self.ancho_total = master.winfo_screenwidth()
        self.altura_total = master.winfo_screenheight()
        # Elementos
        self.master = master
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        self.mainContainer = tk.Frame(self.master)
        self.mainContainer.grid(column=0, row=0)

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
        while i < len(configuracion_grafico):
            self.grafico = Grafico.Grafico(self.mainContainer, configuracion=configuracion_grafico[i])
            self.grafico.grid(row=filas[i], column=columnas[i], columnspan=2,padx=20,pady=10)
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
        while i < len(configuracion_indicador):
            altura = configuracion_indicador[i]['altura']
            ancho = configuracion_indicador[i]['ancho']
            self.indicador = Indicador.Indicador(self.mainContainer,
                bd=2,height=altura,width=ancho, bg='white',highlightbackground="black",
                configuracion=configuracion_indicador[i])
            self.indicador.grid(row=2, column=i, pady=50)
            i += 1

        # Botón de salir ***********************************************************************************************
        self.salirButton = tk.Button(self.mainContainer, text='Salir', width=10, command=master.destroy)
        self.salirButton.grid(row=0, column=7, sticky="N")
        self.paginaButton = tk.Button(self.mainContainer, text="<-", width=10, command=lambda: master.cambiar_pagina())
        self.paginaButton.grid(row=0, column=6, sticky="N")
