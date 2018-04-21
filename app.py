import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

from pagina1 import Pagina1
from pagina2 import Pagina2

import random

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.config_ventana()
        self.get_data()

    def get_data(self):
        # Se selecciona el puerto serial a utilizar
        # tasa_baudios = 9600
        # ser = serial.Serial('/dev/ttyACM0', tasa_baudios)
        serial = ""
        mensaje = [0]
        intervalo = 1000
        # (Se generan los valores aleatorios)
        vuelta = 100 * float(random.random())
        diente = 100 * float(random.random())
        tiempo = 100 * float(random.random())
        presion = 100 * float(random.random())
        par = 100 * float(random.random())
        valores = {"vuelta": vuelta, "diente": diente, "tiempo": tiempo, "presion": presion, "par": par}
        self.frame_actual.set(self.frame,valores)
        # Se calcula un nuevo valor aleatorio cuando termina el intervalo
        self.after(intervalo, self.get_data)

    def config_ventana(self):
        # Título de la ventana
        self.title('Panel instrumental')
        # Pantalla completa
        self.attributes("-fullscreen", True)
        # Acciones de salir de pantalla completa
        self.state = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        # Frames
        self.frame = None
        self.frame_actual = Pagina2
        self.cambiar_pagina()

    def cambiar_pagina(self):
        if self.frame_actual == Pagina1:
            self.frame_actual = Pagina2
        else:
            self.frame_actual = Pagina1
        new_frame = self.frame_actual(self)
        if self.frame is not None:
            self.frame.grid_forget()
        self.frame = new_frame

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    app = App()
    app.mainloop()
