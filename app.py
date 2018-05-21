import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

from bin.main import Main

import random

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # Inicializar variables
        self.job = None
        self.intervalo = 1  #Borrar
        self.vuelta = 0
        self.diente = 0
        self.tiempo = 0
        self.presion = 0
        self.par = 0
        self.csv = []
        self.file = []
        # Procesos
        self.config_ventana()
        self.main = Main(self)
        self.simular_datos(0)

    def config_ventana(self):
        """Configura la ventana de la aplicación"""
        # Título de la ventana
        self.title('Panel instrumental')
        # Pantalla completa
        #self.attributes("-fullscreen", True)
        # Acciones de salir de pantalla completa
        self.state = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        
    def set_datos(self):
        """Obtiene los datos y hace un main.set cada cierto intervalo de tiempo"""
        # Se selecciona el puerto serial a utilizar
        # tasa_baudios = 9600
        # ser = serial.Serial('/dev/ttyACM0', tasa_baudios)
        serial = ""
        mensaje = [0]
        valores = {"vuelta": self.vuelta, "diente": self.diente, "tiempo": self.tiempo, "presion": self.presion, "par": self.par}
        self.main.set(valores)

    def leer_datos(self, fila):
        if fila == 0:
            self.stop_set_datos()
        datos = self.csv[fila]
        self.vuelta = int(datos[0])
        self.diente = int(datos[1])
        self.tiempo = float(datos[2])*1000
        self.presion = float(datos[3])
        self.par = float(datos[4])
        self.fila = fila + 1
        self.set_datos()
        # Se calcula un nuevo valor aleatorio cuando termina el intervalo
        if fila < len(self.csv) - 1:
            self.job = self.after(1, self.leer_datos, self.fila)
        else:
            self.cambiar_estado('pause')

    def simular_datos(self, fila):
        # (Se generan los valores aleatorios)
        # Diente
        self.diente += 1
        if self.diente > 360:
            self.diente = 1
        self.diente = int(self.diente)
        # Vuelta
        if (self.diente == 360):
            self.vuelta += 1
        # Tiempo
        self.tiempo += random.uniform(0.00006, 0.0001)
        # Presión
        if self.presion < 40:
            self.presion += 0.5
        else:
            self.presion = random.uniform(40, 80)
            # Par
        if self.par < 2:
            self.par += 0.05
        else:
            self.par = random.uniform(2, 6)
        self.set_datos()
        if fila > 0:
            self.file.append(str(self.vuelta) + ',' + str(self.diente) + ',' + str(self.tiempo) + ',' + str(self.presion) + ',' + str(self.par) + '\n')
            self.job = self.after(1, self.simular_datos, fila + 1)
        else:
            self.job = self.after(1, self.simular_datos, 0)
    def stop_set_datos(self):
        """Detiene el proceso de set_datos"""
        if self.job is not None:
            self.after_cancel(self.job)
            self.job = None

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)
        return "break"

    def set_opciones(self, opciones):
        intervalo = opciones['intervalo']
        self.stop_set_datos()
        self.intervalo = intervalo
        self.set_datos()

    def stop(self):
        self.cambiar_estado('pause')
        self.stop_set_datos()
        file = tk.filedialog.asksaveasfile(mode='w',defaultextension=".csv", initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
        if not file:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        for i in range(0, len(self.file), 1):
            file.write(self.file[i])
        file.close()  # `()` was missing.

    def open(self):
        file = tk.filedialog.askopenfile(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
        if not file:
            return
        self.cambiar_estado('open')
        datos = str(file.read())
        array = datos.split('\n')
        csv = []
        for i in range(1, len(array) - 1, 1):
            csv.append(array[i].split(','))
        file.close()
        self.csv = csv
        self.leer_datos(0)

    def record(self):
        self.stop_set_datos()
        self.cambiar_estado('record')
        self.simular_datos(1)

    def pause(self):
        self.cambiar_estado('pause')
        self.stop_set_datos()

    def play(self):
        self.cambiar_estado('simular')
        self.simular_datos(0)

    def cambiar_estado(self, estado):
        if estado == 'simular':
            self.main.stopButton.configure(state='disabled')
            self.main.recordButton.configure(relief='raised')
            self.main.recordButton.configure(state='normal')
            self.main.playButton.configure(relief='raised')
            self.main.playButton.configure(state='normal')
            self.main.pauseButton.configure(relief='raised')
            self.main.pauseButton.configure(state='normal')
            self.main.playButton.grid_remove()
            self.main.pauseButton.grid()
            self.main.openButton.configure(state='normal')
            self.main.openButton.configure(relief='raised')
        elif estado == 'record':
            self.main.stopButton.configure(state='normal')
            self.main.recordButton.configure(relief='sunken')
            self.main.recordButton.configure(state='disabled')
            self.main.playButton.configure(state='disabled')
            self.main.pauseButton.configure(relief='raised')
            self.main.pauseButton.configure(state='disabled')
            self.main.openButton.configure(state='disabled')
            self.main.openButton.configure(relief='raised')
        elif estado == 'pause':
            self.main.stopButton.configure(state='disabled')
            self.main.recordButton.configure(relief='raised')
            self.main.recordButton.configure(state='normal')
            self.main.playButton.configure(state='normal')
            self.main.playButton.grid()
            self.main.pauseButton.configure(relief='sunken')
            self.main.pauseButton.configure(state='disabled')
            self.main.pauseButton.grid_remove()
            self.main.openButton.configure(state='normal')
            self.main.openButton.configure(relief='raised')
        elif estado == 'open':
            self.main.stopButton.configure(state='disabled')
            self.main.recordButton.configure(relief='raised')
            self.main.recordButton.configure(state='normal')
            self.main.playButton.configure(relief='raised')
            self.main.playButton.configure(state='normal')
            self.main.pauseButton.configure(relief='raised')
            self.main.pauseButton.configure(state='normal')
            self.main.playButton.grid_remove()
            self.main.pauseButton.grid()
            self.main.openButton.configure(state='disabled')
            self.main.openButton.configure(relief='sunken')
if __name__ == '__main__':
    app = App()
    app.mainloop()
