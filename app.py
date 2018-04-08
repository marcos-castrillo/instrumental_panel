import tkinter as tk
import medidor_marco as Medidor
import indicador_marco as Indicador
import grafico_marco as Grafico


class App(tk.Tk):
    def __init__(self):
        super(App, self).__init__()
        # Obtener ancho/alto de la pantalla
        ancho_total = self.winfo_screenwidth()
        altura_total = self.winfo_screenheight()
        # Título de la ventana
        self.title('Gauge')
        container = tk.Frame(self).grid(column=0, row=0)
        # Medidores ****************************************************************************************************
        n_medidores = 2
        ancho_medidor = ancho_total / n_medidores / 2.5
        altura_medidor = altura_total/2
        # [Título, descripción, unidad, ancho, altura, minimo, maximo, intervalo, color_bajo, color_medio, color_alto]
        configuracion_medidor = [
            {"nombre": "Presión", "unidad": "Pa", "ancho": ancho_medidor, "altura": altura_medidor, "minimo": 0,
             "maximo": 100,
             "intervalo": 3000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Par", "unidad": "rad/s", "ancho": ancho_medidor, "altura": altura_medidor, "minimo": 0,
             "maximo": 100, "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"}
        ]
        i = 0
        while i < len(configuracion_medidor):
            gauge = Medidor.MedidorMarco(container, configuracion=configuracion_medidor[i])
            gauge.grid(row=0, column=i*2, columnspan=2, sticky="NSEW")
            i += 1
        # Indicadores **************************************************************************************************
        n_indicadores = 2
        ancho_indicador = ancho_total / n_indicadores / 4
        altura_indicador = altura_total/3.5
        # [Título, descripción, unidad, ancho, altura, minimo, maximo, intervalo, color_bajo, color_medio, color_alto]
        configuracion_indicador = [
            {"nombre": "Presión", "unidad": "Pa", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 3000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Par", "unidad": "rad/s", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Par", "unidad": "rad/s", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Par", "unidad": "rad/s", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Presión", "unidad": "Pa", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 3000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Par", "unidad": "rad/s", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Par", "unidad": "rad/s", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
            {"nombre": "Par", "unidad": "rad/s", "ancho": ancho_indicador, "altura": altura_indicador,
             "intervalo": 1000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"}
        ]
        i = 0
        j = 0
        while i < len(configuracion_indicador)/2:
            indicador = Indicador.IndicadorMarco(container, configuracion=configuracion_indicador[i])
            indicador.grid(row=j+1, column=i)
            i += 1
            if i > len(configuracion_indicador)/2 -1 and j == 0:
                j = 1
                i = 0

        # Gráfico **************************************************************************************************
        n_graficos = 2
        ancho_grafico = ancho_total / n_graficos / 4
        altura_grafico = altura_total/3.5
        # [Título, descripción, unidad, ancho, altura, minimo, maximo, intervalo, color_bajo, color_medio, color_alto]
        configuracion_grafico = [
            {"nombre": "Presión", "unidad": "Pa", "ancho": ancho_grafico, "altura": altura_grafico,
             "intervalo": 3000, "color_bajo": "green", "color_medio": "#efdf00", "color_alto": "red"},
        ]
        i = 0
        while i < len(configuracion_grafico):
            #grafico = Grafico.GraficoMarco(container, configuracion=configuracion_grafico[i])
            #grafico.grid(row=0, column=4, columnspan=2, sticky="NSEW")
            i += 1

        # Configuración ************************************************************************************************
        # Pantalla completa
        self.attributes("-fullscreen", True)
        # Botón de salir
        salir = tk.Button(container, text='Salir', width=10, command=self.destroy).grid(row=0, column=0, sticky="nw")
        # Acciones de salir de pantalla completa
        self.state = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)
        return "break"