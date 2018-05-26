# coding=utf-8
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

from tkinter.colorchooser import *
from redondeo import redondear

class AjustesMedidores(tk.Frame, object):
    def __init__(self, master, main, app, configuracion, **kwargs):
        super(AjustesMedidores, self).__init__(master, configuracion=None, **kwargs)
        self.master = master
        self.master.configure(bg='white', highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.main = main
        self.app = app
        self.nombre = configuracion["nombre"]
        self.unidad = configuracion["unidad"]
        self.umbrales_porc = configuracion["umbrales_porc"]
        self.umbrales_val = configuracion["umbrales_val"]
        self.colores = configuracion["colores"]
        self.n_colores = len(self.colores)
        self.tipo_umbral = configuracion["tipo_umbral"]
        minimo = configuracion["minimo"]
        if minimo.is_integer():
            minimo = int(minimo)
        maximo = configuracion["maximo"]
        if maximo.is_integer():
            maximo = int(maximo)
        # Elementos de los ajustes
        if self.tipo_umbral == 'P':
            self.umbrales_actual = self.umbrales_porc
            self.unidad_actual = "%"
        else:
            self.umbrales_actual = self.umbrales_val
            self.unidad_actual = " " + self.unidad
        self.rangoLabel = tk.Label(master, text="Rango", bg='white')
        self.minimoEntry = tk.Entry(master, bd=5, width=5)
        self.minimoEntry.insert(0, minimo)
        self.maximoEntry = tk.Entry(master, bd=5, width=5)
        self.maximoEntry.insert(0, maximo)
        self.umbralRadioLabel = tk.Label(master, text="Tipo de umbral", bg='white')
        self.umbralRadio0 = tk.Radiobutton(master, text="Porcentaje", variable=self.tipo_umbral, value='P', command=self.cambiar_umbral)
        self.umbralRadio1 = tk.Radiobutton(master, text="Valor", variable=self.tipo_umbral, value='V', command=self.cambiar_umbral)
        self.umbralLabel = tk.Label(master, text="Umbrales", bg='white')
        self.umbral0 = tk.StringVar()
        self.umbralEntry0 = tk.Entry(master, textvariable=self.umbral0, bd=5, width="7")
        self.umbralEntry0.insert(0, self.umbrales_actual[0])
        self.umbralEntry0.bind("<FocusOut>", lambda event, arg=self.umbral0: self.guardar_umbral(event, arg))
        self.umbral1 = tk.StringVar()
        self.umbralEntry1 = tk.Entry(master, textvariable=self.umbral1, bd=5, width="7")
        self.umbralEntry1.insert(0, self.umbrales_actual[1])
        self.umbralEntry1.bind("<FocusOut>", lambda event, arg=self.umbral1: self.guardar_umbral(event, arg))
        self.colorEntry0 = tk.Button(master, width="15", command = lambda: self.set_color(self.colorEntry0))
        self.colorEntry0.config(font='Helvetica 9 bold',text="< " + str(self.umbrales_actual[0]) + self.unidad_actual, bg=self.colores[0])
        self.colorEntry1 = tk.Button(master, width="15", command = lambda: self.set_color(self.colorEntry1))
        self.colorEntry1.config(font='Helvetica 9 bold',text=">= " + str(self.umbrales_actual[0]) + self.unidad_actual + " y < " + str(self.umbrales_actual[1]) + self.unidad_actual, bg=self.colores[1])
        self.colorEntry2 = tk.Button(master, width="15", command = lambda: self.set_color(self.colorEntry2))
        self.colorEntry2.config(font='Helvetica 9 bold',text=">= " + str(self.umbrales_actual[1]) + self.unidad_actual, bg=self.colores[2])
        self.aceptarButton = tk.Button(master, text='Aceptar', width=10, command= lambda: self.aceptar_ajustes('aceptar'))
        self.aplicarButton = tk.Button(master, text='Aplicar', width=10,command= lambda: self.aceptar_ajustes('aplicar'))
        # Ajustar la posición de los elementos
        self.rangoLabel.grid(row=0, column=0)
        self.minimoEntry.grid(row=1, column=0, sticky='w')
        self.maximoEntry.grid(row=1, column=0, sticky='e')
        self.umbralRadioLabel.grid(row=2, column=0)
        self.umbralRadio0.grid(row=3, column=0)
        self.umbralRadio1.grid(row=4, column=0)
        self.umbralLabel.grid(row=0, column=1)
        self.umbralEntry0.grid(row=1, column=1, sticky='w')
        self.umbralEntry1.grid(row=1, column=1, sticky='e')
        self.colorEntry0.grid(row=2, column=1)
        self.colorEntry1.grid(row=3, column=1)
        self.colorEntry2.grid(row=4, column=1)
        self.aceptarButton.grid(row=5, column=0)
        self.aplicarButton.grid(row=5, column=1)

    def set_color(self, widget):
        button_index = str(widget)[-1:]
        if button_index == 'n':
            button_index = 1
        print(button_index,widget)
        button_index = int(button_index)-1
        color = askcolor(initialcolor = self.colores[button_index])
        if button_index == 0:
            widget.config(font='Helvetica 9 bold',  text="< " + str(self.umbrales_actual[0]) + self.unidad_actual, bg=color[1])
        elif button_index == 1:
            widget.config(font='Helvetica 9 bold',  text=">= " + str(self.umbrales_actual[0]) + self.unidad_actual + " y < " + str(self.umbrales_actual[1]) + self.unidad_actual, bg=color[1])
        else:
            widget.config(font='Helvetica 9 bold',  text=">= " + str(self.umbrales_actual[1]) + self.unidad_actual, bg=color[1])

    def guardar_umbral(self, evento, umbral):
        umbral_index = str(evento.widget)[-1:]
        if umbral_index == '3':
            umbral_index = 0
        elif umbral_index == '4':
            umbral_index = 1
        if self.tipo_umbral == 'P':
            self.umbrales_porc[umbral_index] = redondear(float(umbral.get()),0)
        else:
            self.umbrales_val[umbral_index] = redondear(float(umbral.get()),0)

    def cambiar_umbral(self):
        self.minimoEntry.focus_set()
        if self.tipo_umbral == 'V':
            self.tipo_umbral = 'P'
            self.umbrales_actual = self.umbrales_porc
            self.unidad_actual = "%"
        else:
            self.tipo_umbral = 'V'
            self.umbrales_actual = self.umbrales_val
            self.unidad_actual = " " + self.unidad
        self.umbralEntry0.delete(0,'end')
        self.umbralEntry0.insert(0, self.umbrales_actual[0])
        self.umbralEntry1.delete(0,'end')
        self.umbralEntry1.insert(0, self.umbrales_actual[1])
        self.colorEntry0.config(text="< " + str(self.umbrales_actual[0]) + self.unidad_actual, bg=self.colores[0])
        self.colorEntry1.config(text=">= " + str(self.umbrales_actual[0]) + self.unidad_actual + " y < " + str(self.umbrales_actual[1]) + self.unidad_actual, bg=self.colores[1])
        self.colorEntry2.config(text=">= " + str(self.umbrales_actual[1]) + self.unidad_actual, bg=self.colores[2])

    def aceptar_ajustes(self, tipo_accion):
        if self.tipo_umbral == 'P':
            umbrales_porc = [float(self.umbralEntry0.get())]
            umbrales_porc.append(float(self.umbralEntry1.get()))
            umbrales_val = self.umbrales_val
        else:
            umbrales_val = [float(self.umbralEntry0.get())]
            umbrales_val.append(float(self.umbralEntry1.get()))
            umbrales_porc = self.umbrales_porc
        colores = [self.colorEntry0.cget('background')]
        colores.append(self.colorEntry1.cget('background'))
        colores.append(self.colorEntry2.cget('background'))
        minimo = self.minimoEntry.get()
        maximo = self.maximoEntry.get()
        ajustes = {
            "umbrales_porc": umbrales_porc,
            "umbrales_val": umbrales_val,
            "tipo_umbral": self.tipo_umbral,
            "colores": colores,
            "minimo": minimo,
            "maximo": maximo
        }
        self.main.save_ajustes_medidor(self, ajustes, tipo_accion)

    def set_ajustes(self, ajustes):
        self.colores = ajustes['colores']
        umbrales_porc_str = ajustes['umbrales_porc']
        umbrales_val_str = ajustes['umbrales_val']
        self.umbrales_porc = [float(numeric_string) for numeric_string in umbrales_porc_str]
        self.umbrales_val = [float(numeric_string) for numeric_string in umbrales_val_str]
        self.minimo_rango = float(ajustes['minimo'])
        self.maximo_rango = float(ajustes['maximo'])
        self.colorLabel0 = tk.Label(self.master, text="Color si: " + self.nombre + " < " + str(self.umbrales_actual[0]) + self.unidad_actual, bg='white')
        self.colorLabel1 = tk.Label(self.master, text="Color si: " + str(self.umbrales_actual[0]) + self.unidad_actual + " < " + self.nombre + " <= " + str(self.umbrales_actual[1]) + self.unidad_actual, bg='white')
        self.colorLabel2 = tk.Label(self.master, text="Color si: " + str(self.umbrales_actual[1]) + self.unidad_actual + " <= " + self.nombre, bg='white')