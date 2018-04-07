import tkinter as tk
import gauge_marco as Marco


class App(tk.Tk):
    def __init__(self):
        super(App, self).__init__()
        # Obtener ancho/alto de la pantalla
        ancho_total = self.winfo_screenwidth()
        altura_total = self.winfo_screenheight()
        # Título de la ventana
        self.title('Gauge')
        # Medidores ****************************************************************************************************
        n_medidores = 2
        ancho_medidor = ancho_total / n_medidores/2
        altura_medidor = altura_total
        container_medidor = tk.Frame(self, bg='gray2').grid()
        # [Título, descripción, unidad, ancho, altura, minimo, maximo, intervalo, color_bajo, color_medio, color_alto]
        configuracion_medidor = [
            {"nombre":"Presión","unidad":"Pa","ancho":ancho_medidor,"altura":altura_medidor,"minimo":0,"maximo":100,
            "intervalo":3000,"color_bajo":"green","color_medio":"yellow","color_alto":"red"},
            {"nombre": "Par", "unidad": "rad/s", "ancho": ancho_medidor, "altura": altura_medidor, "minimo": 0,
             "maximo": 100, "intervalo": 1000, "color_bajo": "green", "color_medio": "yellow", "color_alto": "red"}
        ]

        i = 0
        while i < len(configuracion_medidor):
            gauge = Marco.GaugeMarco(container_medidor, configuracion=configuracion_medidor[i])
            gauge.grid(row=0, column=i, sticky="ns")
            i += 1
        # Pantalla completa
        self.attributes("-fullscreen", True)
        # Botón de salir
        salir = tk.Button(container_medidor, text='Salir', width=15, command=self.destroy).grid()
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