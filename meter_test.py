import tkinter as tk
import tkinter.font as tkf
import math
import random

# La clase App invoca a MeterFrame, que a su vez invoca a Meter
class App(tk.Tk):
    def __init__(self):
        super(App, self).__init__()
        # Título de la ventana
        self.title('Velocimetro')
        # create all of the main containers
        center = tk.Frame(self, bg='gray2', width=50, height=420, padx=3, pady=3)
        bottom = tk.Frame(self, bg='#c9d3db', width=800, height=10, padx=3, pady=3)
        # btm_frame = tk.Frame(self, bg='white', width=800, height=45, pady=3)
        # btm_frame2 = tk.Frame(self, bg='lavender', width=800, height=60, pady=3)
        # frame1 = MeterFrame(self,height = 500, width = 500).grid(row=0, column=0)
        # frame2 = MeterFrame(self,height = 500, width = 500).grid(row=0, column=0)

        # layout all of the main containers
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center.grid(row=0, sticky="nsew")
        bottom.grid(row=1, sticky="ew")
        # btm_frame.grid(row=3, sticky="ew")
        # btm_frame2.grid(row=4, sticky="ew")

        # create the widgets for the top frame
        left_label = tk.Label(bottom, text='Velocidad', font=("Helvetica", 16), bg='#c9d3db')
        right_label = tk.Label(bottom, text='Temperatura', font=("Helvetica", 16), bg='#c9d3db', padx=3, pady=3)
        # length_label = tk.Label(top_frame, text='Length:')
        # entry_W = tk.Entry(top_frame, background="pink")
        # entry_L = tk.Entry(top_frame, background="orange")

        # Botón de salir
        # tk.Button(bottom,text = 'Salir',width = 15,command = self.destroy).grid(row=1, column=1)

        # layout the widgets in the top frame
        left_label.grid(row=0, column=0, sticky="ns")
        right_label.grid(row=0, column=1, sticky="nsew")
        # length_label.grid(row=1, column=2)
        # entry_W.grid(row=1, column=1)
        # entry_L.grid(row=1, column=3)

        # create the center widgets
        center.grid_rowconfigure(1, weight=1)
        center.grid_columnconfigure(0, weight=1)

        gauge_left = MeterFrame(center, bg='green', width=400, height=420, padx=3, pady=3)
        gauge_right = MeterFrame(center, bg='yellow', width=400, height=420, padx=3, pady=3)

        gauge_left.grid(row=0, column=0, sticky="ns")
        gauge_right.grid(row=0, column=1, sticky="nsew")

        # Crear los widgets del bottom
        bottom.grid_rowconfigure(1, weight=0)
        bottom.grid_columnconfigure(1, weight=1)

        # label_left = tk.Frame(bottom, bg='white', width=400, height=10)
        # label_right = tk.Frame(bottom, bg='white', width=400, height=10)


class MeterFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super(MeterFrame, self).__init__(master, *args, **kwargs)
        interval = 1000

        def redondeo(value):
            value_s = str(value)
            length = len(value_s)
            if value == 0:
                return 0
            coma = value_s.find('.')
            n = 0
            ceros = -1
            while True:
                digito = value_s[n]
                if digito != ".":
                    if int(digito) > 0:
                        break
                    else:
                        ceros += 1
                        n += 1
                else:
                    n += 1
            if digito == '1':
                corr = 4
            else:
                corr = 3
            if coma <= n:
                length -= 1
                n -= 1
            if length < 4:
                cifras = 0
            elif n == 0 and coma == -1:
                cifras = corr - length
            elif int(digito) > 1 and n > 0:
                cifras = corr + n - 1
            elif int(digito) == 1 and n > 0:
                cifras = corr + n - 1
            elif int(digito) == 1 and n == 0:
                if coma > 1:
                    cifras = corr - n - 1 - coma
                else:
                    cifras = corr - n - 1
            elif int(digito) > 1 and n == 0:
                cifras = corr - coma
            else:
                cifras = 0
            resultado = round(value, cifras)
            if float(resultado).is_integer():
                resultado = int(resultado)
            return resultado

        def newvalue():
            value = rango_max * float(random.random())
            value = redondeo(value)
            self.meter.set(value)
            self.meter.after(interval, newvalue)

        # Meter toma 2 parámetros, altura y ancho
        height = int(self['height'])
        width = int(self['width'])
        rango_min = 0
        rango_max = 1
        self.meter = Meter(self, height=height, width=width)
        # Rango de valores útiles
        self.meter.graphics(rango_min, rango_max)
        self.meter.createhand()
        self.meter.setrange(rango_min, rango_max)
        self.meter.grid(row=0, column=0)
        newvalue()


class Meter(tk.Canvas, object):
    def __init__(self, master, *args, **kwargs):
        super(Meter, self).__init__(master, *args, **kwargs)

        self.layoutparams()
        # self.graphics()
        # self.createhand()
        # self.setrange()

    def layoutparams(self):
        # set parameters that control the layout
        height = int(self['height'])
        width = int(self['width'])

        # find a square that fits in the window
        if height * 2 > width:
            side = width
        else:
            side = height * 2

        # set axis for hand
        self.centrex = side / 2
        self.centrey = side / 2

        # standard with of lines
        self.linewidth = 2

        # outer radius for dial
        self.radius = int(0.40 * float(side))

        # set width of bezel
        self.bezel = self.radius / 20
        self.bezelcolour1 = '#000000'
        self.bezelcolour2 = '#808080'

        # set lengths of ticks and hand
        self.majortick = self.radius / 8
        self.minortick = self.majortick / 2
        self.handlen = self.radius - self.majortick - self.bezel - 1
        self.blobrad = self.handlen / 6

    def graphics(self, rango_min, rango_max):
        # create the static components
        self.create_oval(self.centrex - self.radius
                         , self.centrey - self.radius
                         , self.centrex + self.radius
                         , self.centrey + self.radius
                         , width=self.bezel
                         , outline=self.bezelcolour2)

        self.create_arc(self.centrex - self.radius
                        , self.centrey - self.radius
                        , self.centrex + self.radius
                        , self.centrey + self.radius
                        , width=self.bezel * 1.25
                        , outline="#F0F0F0"
                        , start=242, extent=55)

        self.create_arc(self.centrex - 1.25 * self.radius
                        , self.centrey - 1.25 * self.radius
                        , self.centrex + 1.25 * self.radius
                        , self.centrey + 1.25 * self.radius
                        , width=self.bezel * 1.5
                        , outline="#F0F0F0"
                        , start=242, extent=55)

        self.create_oval(self.centrex - self.radius - 2 * self.bezel
                         , self.centrey - self.radius - 2 * self.bezel
                         , self.centrex + self.radius + 2 * self.bezel
                         , self.centrey + self.radius + 2 * self.bezel
                         , width=self.bezel
                         , outline=self.bezelcolour1)

        for deg in range(-60, 241, 6):
            self.createtick(deg, self.minortick, rango_min, rango_max)
        for deg in range(-60, 241, 30):
            self.createtick(deg, self.majortick, rango_min, rango_max)

    def createhand(self):
        # create text display
        self.textid = self.create_text(self.centrex
                                       , self.centrey * 2
                                       , fill="black"
                                       , font=tkf.Font(size=-int(2 * self.majortick)))

        # create moving and changeable bits
        self.handid = self.create_line(self.centrex, self.centrey
                                       , self.centrex - self.handlen, self.centrey
                                       , width=2 * self.linewidth
                                       , fill="red")

        self.blobid = self.create_oval(self.centrex - self.blobrad
                                       , self.centrey - self.blobrad
                                       , self.centrex + self.blobrad
                                       , self.centrey + self.blobrad
                                       , outline='black', fill='black')

    def createtick(self, angle, length, rango_min, rango_max):
        # helper function to create one tick
        rad = math.radians(angle)
        cos = math.cos(rad)
        sin = math.sin(rad)
        radius = self.radius - self.bezel
        if length == 20:
            canvas_id = self.create_text(self.centrex - 0.73 * radius * cos, self.centrey - 0.73 * radius * sin)
            numero = (angle + 60) / 30 * (rango_max - rango_min) / 10
            if (numero.is_integer()):
                numero = int(numero)
            self.itemconfig(canvas_id, text=str(numero), font=tkf.Font(size=int(1.5 * self.minortick)))
        self.create_line(self.centrex - radius * cos
                         , self.centrey - radius * sin
                         , self.centrex - (radius - length) * cos
                         , self.centrey - (radius - length) * sin
                         , width=self.linewidth)

    def setrange(self, start=0, end=100):
        self.start = start
        self.range = end - start

    def set(self, value):
        # call this to set the hand
        # convert value to range 0,100
        deg = 300 * (value - self.start) / self.range - 240

        self.itemconfigure(self.textid, text=str(value))
        rad = math.radians(deg)
        # reposition hand
        self.coords(self.handid, self.centrex, self.centrey, self.centrex + self.handlen * math.cos(rad),
                    self.centrey + self.handlen * math.sin(rad))

    def blob(self, colour):
        # call this to change the colour of the blob
        self.itemconfigure(self.blobid, fill=colour, outline=colour)


App().mainloop()
