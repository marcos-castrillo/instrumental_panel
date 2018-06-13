# coding=utf-8
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

from main import Main
import datetime as datetime
import random
import serial
import time

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # Inicializar variables
        self.job = None
        self.reiniciar = False
        self.vuelta = 0
        self.diente = 0
        self.tiempo = 0
        self.presion = 0
        self.par = -20
        self.csv = []
        self.file = []
        self.modo = tk.StringVar()

        self.serial_abierto = False
        # Procesos
        self.config_ventana()
        self.main = Main(self)
        self.main.pantallaCompletaButton.configure(relief='sunken')
        self.modo.set('Adquisición')
        self.main.estadoLabel.config(text=self.modo.get())
        if self.modo.get() == 'Simulación':
            self.simular_datos(0)
        else:
            self.adquirir_datos(0)

    def config_ventana(self):
        """Configura la ventana de la aplicación"""
        # Título de la ventana
        self.title('Panel instrumental')
        # Pantalla completa
        self.attributes("-fullscreen", True)
        # Acciones de salir de pantalla completa
        self.state = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)

    def set_datos(self):
        """Obtiene los datos y hace un main.set"""
        valores = {"vuelta": self.vuelta, "diente": self.diente, "tiempo": self.tiempo, "presion": self.presion, "par": self.par}
        self.main.set(valores, self.reiniciar)
        self.reiniciar = False

    def leer_datos(self, fila):
        self.fila_actual = fila
        if fila == 0:
            self.stop_set_datos()
            self.reiniciar = True
            self.modo_anterior = self.modo.get()
            self.modo.set('Reproducción')
            self.main.estadoLabel.config(text=self.modo.get())
        datos = self.csv[fila]
        self.vuelta = int(datos[0])
        self.diente = int(datos[1])
        self.tiempo = float(datos[2])
        self.presion = float(datos[3])
        self.par = float(datos[4])
        self.fila = fila + 1
        self.set_datos()
        # Se calcula un nuevo valor aleatorio cuando termina el intervalo
        if fila < len(self.csv) - 1:
            self.job = self.after(1, self.leer_datos, self.fila)
        else:
            self.cambiar_estado('pausa')
            self.reset()
            self.modo.set(self.modo_anterior)
            self.main.estadoLabel.config(text=self.modo.get())

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
        self.tiempo = random.uniform(0.00025, 0.0003)
        # Presión
        if self.presion < 15:
            self.presion += 0.5
        else:
            self.presion = random.uniform(15, 20)
            # Par
        if self.par < 15:
            self.par += 0.05
        else:
            self.par = random.uniform(15, 20)
        self.set_datos()
        if fila > 0:
            self.file.append(str(self.vuelta) + ',' + str(self.diente) + ',' + str(self.tiempo) + ',' + str(self.presion) + ',' + str(self.par) + '\n')
            self.job = self.after(1, self.simular_datos, fila + 1)
        else:
            self.job = self.after(1, self.simular_datos, 0)

    def adquirir_datos(self, fila):
        self.serial_abierto = True
        puerto = '/dev/ttyUSB0'
        if self.puerto_disponible(puerto):
            ser = serial.Serial(
                port=puerto,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
            while self.serial_abierto:
                datos = ser.readline()
                self.vuelta = datos.vuelta
                self.diente = datos.diente
                self.tiempo = datos.tiempo
                self.presion = datos.presion
                self.par = datos.par
                self.set_datos()
                if fila > 0:
                    self.file.append(str(self.vuelta) + ',' + str(self.diente) + ',' + str(self.tiempo) + ',' + str(self.presion) + ',' + str(self.par) + '\n')
                fila += 1
        else:
            def desconectar():
                toplevel.destroy()
                self.after_cancel(self.cuenta_atras)
                self.cuenta_atras = None
                self.unbind("<FocusIn>")
                self.unbind("<Map>")
                self.cambiar_estado('adquisicion')
            def reconectar():
                desconectar()
                self.adquirir_datos(fila)
            def bucle_reconectar(i):
                label2.config(text='Reconectando automáticamente en ' + str(i) + ' segundos')
                if self.modo.get() != 'Adquisición':
                    desconectar()
                elif i > 0:
                    i -= 1
                    self.cuenta_atras = self.after(1000, bucle_reconectar, i)
                else:
                    reconectar()
            def OnMap(event):
                reconectar()
            self.cambiar_estado('desconexion')
            # Recargar toplevel cuando se minimiza/maximiza o se abre de nuevo la ventana
            self.bind("<FocusIn>", OnMap)
            self.bind("<Map>", OnMap)
            toplevel = tk.Toplevel(self, bd=2, relief="solid")
            # Posición del TopLevel
            g = "+%s+%s" % (500, 200)
            toplevel.geometry(g)
            # Ocultar botones de minimizar, cerrar, expandir
            toplevel.overrideredirect(1)
            ERROR_CONEXION = 'No se ha podido establecer la conexión con ' + puerto + '.'
            label1 = tk.Label(toplevel, text=ERROR_CONEXION, height=5, width=60)
            desconexion = tk.PhotoImage(file='images/desconexion.png')
            imagen = tk.Label(toplevel, image=desconexion)
            imagen.image = desconexion
            boton = tk.Button(toplevel, text='Reconectar', command=reconectar)
            TIEMPO = 'Reconectando automáticamente en 10 segundos'
            label2 = tk.Label(toplevel, text=TIEMPO, font='Helvetica 12 bold')
            label1.grid(row=0, column=0)
            imagen.grid(row=1, column=0)
            boton.grid(row=3, column=0, pady=20)
            label2.grid(row=2, column=0)
            bucle_reconectar(10)

    def puerto_disponible(self, puerto):
        try:
            ser = serial.Serial(port=puerto)
            return True
        except:
            return False

    def stop_set_datos(self):
        """Detiene el proceso de adquirir o simular datos"""
        if self.job is not None:
            self.after_cancel(self.job)
            self.job = None
        self.serial_abierto = False

    def toggle_fullscreen(self, event=None):
        self.attributes("-fullscreen", self.state)
        if self.state:
            self.main.pantallaCompletaButton.configure(relief='sunken')
        else:
            self.main.pantallaCompletaButton.configure(relief='raised')
        self.state = not self.state
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)
        self.main.pantallaCompletaButton.configure(relief='raised')
        return "break"

    def set_opciones(self, opciones):
        modo = opciones['modo']
        estadoActual = self.main.estadoLabel['text']
        if estadoActual != self.modo.get():
            self.main.estadoLabel.config(text=modo)
            self.stop_set_datos()
            if modo == 'Simulación':
                self.reset()
                self.simular_datos(0)
            elif modo == 'Adquisición':
                self.reset()
                self.adquirir_datos(0)
        tipo_int = opciones["tipo_int"]
        if tipo_int == 0:
            self.main.breakpoint = ''
            self.main.vuelta_limite = ''
            self.main.diente_limite = ''
            self.main.breakpointLabel.grid_remove()
        elif tipo_int == 1:
            horas = opciones['horas']
            if horas == '':
                horas = 0
            minutos = opciones['minutos']
            if minutos == '':
                minutos = 0
            segundos = opciones['segundos']
            if segundos == '':
                segundos = 0
            milisegundos = opciones['milisegundos']
            if milisegundos == '':
                milisegundos = 0
            tiempo = datetime.timedelta(hours=float(horas), minutes=float(minutos), seconds=float(segundos), milliseconds=float(milisegundos))
            self.main.breakpoint = tiempo
            self.main.breakpointLabel.grid()
        else:
            vuelta = opciones['vuelta']
            if vuelta != '':
                vuelta = int(vuelta)
            diente = opciones['diente']
            if diente != '':
                diente = int(diente)
            self.main.vuelta_limite = vuelta
            self.main.diente_limite = diente
            self.main.breakpointLabel.grid()

    def stop(self):
        self.cambiar_estado('pausa')
        self.stop_set_datos()
        if self.modo.get() == 'Simulación' or self.modo.get() == 'Adquisición':
            file = tk.filedialog.asksaveasfile(mode='w',defaultextension=".csv", initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
            if not file:
                return
            for i in range(0, len(self.file), 1):
                file.write(self.file[i])
            file.close()
        elif self.modo.get() == 'Reproducción':
            self.modo.set(self.modo_anterior)
            self.main.estadoLabel.config(text=self.modo.get())

    def open(self):
        file = tk.filedialog.askopenfile(initialdir = "/",title = "Select file", filetypes = (("csv files","*.csv"),("all files","*.*")))
        if not file:
            return
        self.cambiar_estado('reproduccion')
        datos = str(file.read())
        array = datos.split('\n')
        csv = []
        for i in range(1, len(array) - 1, 1):
            csv.append(array[i].split(','))
        file.close()
        self.csv = csv
        self.reset()
        self.leer_datos(0)

    def record(self):
        self.stop_set_datos()
        self.cambiar_estado('grabacion')
        if self.modo.get() == 'Simulación':
            self.simular_datos(1)
        else:
            self.adquirir_datos(1)

    def pause(self):
        self.cambiar_estado('pausa')
        self.stop_set_datos()

    def play(self):
        self.cambiar_estado('adquisicion')
        if self.modo.get() == 'Simulación':
            self.simular_datos(0)
        elif self.modo.get() == 'Adquisición':
            self.adquirir_datos(0)
        else:
            self.cambiar_estado('reproduccion')
            self.leer_datos(self.fila_actual)

    def reset(self):
        self.reiniciar = True
        self.main.vuelta_actual = 0
        self.vuelta = 0
        self.main.timeLabel.config(text=str(datetime.timedelta(milliseconds=0)))

    def cambiar_estado(self, estado):
        if estado == 'adquisicion':
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
        elif estado == 'grabacion':
            self.main.stopButton.configure(state='normal')
            self.main.recordButton.configure(relief='sunken')
            self.main.recordButton.configure(state='disabled')
            self.main.playButton.configure(state='disabled')
            self.main.pauseButton.configure(relief='raised')
            self.main.pauseButton.configure(state='disabled')
            self.main.openButton.configure(state='disabled')
            self.main.openButton.configure(relief='raised')
        elif estado == 'pausa':
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
        elif estado == 'reproduccion':
            self.main.stopButton.configure(state='normal')
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
        elif estado == 'desconexion':
            self.main.stopButton.configure(state='disabled')
            self.main.recordButton.configure(state='disabled')
            self.main.playButton.configure(state='disabled')
            self.main.pauseButton.configure(state='disabled')
if __name__ == '__main__':
    app = App()
    app.mainloop()
