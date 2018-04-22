import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

from main import Main

import random

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.job = None
        self.intervalo = 1000
        self.config_ventana()
        self.main = Main(self)
        self.get_data()

    def get_data(self):
        # Se selecciona el puerto serial a utilizar
        # tasa_baudios = 9600
        # ser = serial.Serial('/dev/ttyACM0', tasa_baudios)
        serial = ""
        mensaje = [0]
        # (Se generan los valores aleatorios)
        vuelta = 100 * float(random.random())
        diente = 100 * float(random.random())
        tiempo = 100 * float(random.random())
        presion = 100 * float(random.random())
        par = 100 * float(random.random())
        valores = {"vuelta": vuelta, "diente": diente, "tiempo": tiempo, "presion": presion, "par": par}
        self.main.set(valores)
        # Se calcula un nuevo valor aleatorio cuando termina el intervalo
        self.job = self.after(self.intervalo, self.get_data)

    def cancel_get_data(self):
        if self.job is not None:
            self.after_cancel(self.job)
            self.job = None
    def config_ventana(self):
        # Título de la ventana
        self.title('Panel instrumental')
        # Pantalla completa
        self.attributes("-fullscreen", True)
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

    def set_opciones(self, opciones):
        intervalo = opciones['intervalo']
        self.cancel_get_data()
        self.intervalo = intervalo
        self.get_data()

if __name__ == '__main__':
    app = App()
    app.mainloop()
