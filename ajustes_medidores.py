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
        self.tipo_umbral = tk.StringVar()
        self.tipo_umbral.set(configuracion["tipo_umbral"])
        self.minimo_rango = configuracion["minimo"]
        if self.minimo_rango.is_integer():
            self.minimo_rango = int(self.minimo_rango)
        self.maximo_rango = configuracion["maximo"]
        if self.maximo_rango.is_integer():
            self.maximo_rango = int(self.maximo_rango)
        # Elementos de los ajustes
        if self.tipo_umbral.get() == 'P':
            self.umbrales_actual = self.umbrales_porc
            self.unidad_actual = "%"
        else:
            self.umbrales_actual = self.umbrales_val
            self.unidad_actual = " " + self.unidad
        self.rangoLabel = tk.Label(master, text="Rango", bg='white', font='Helvetica 10 bold')
        self.minimoEntry = tk.Entry(master, bd=5, width=7)
        self.minimoEntry.insert(0, self.minimo_rango)
        self.maximoEntry = tk.Entry(master, bd=5, width=7)
        self.maximoEntry.insert(0, self.maximo_rango)
        self.umbralRadioLabel = tk.Label(master, text="Tipo de umbral", bg='white', font='Helvetica 10 bold')
        self.umbralRadio0 = tk.Radiobutton(master, text="Porcentaje", variable=self.tipo_umbral, value='P', command=self.cambiar_umbral)
        self.umbralRadio1 = tk.Radiobutton(master, text="Valor", variable=self.tipo_umbral, value='V', command=self.cambiar_umbral)
        self.umbralLabel = tk.Label(master, text="Umbrales", bg='white', font='Helvetica 10 bold')
        self.umbral0 = tk.StringVar()
        self.umbralEntry0 = tk.Entry(master, textvariable=self.umbral0, bd=5, width=7)
        self.umbralEntry0.insert(0, self.umbrales_actual[0])
        self.umbral1 = tk.StringVar()
        self.umbralEntry1 = tk.Entry(master, textvariable=self.umbral1, bd=5, width=7)
        self.umbralEntry1.insert(0, self.umbrales_actual[1])
        self.colorButton0 = tk.Button(master, width="18", command = lambda: self.set_color(self.colorButton0))
        self.colorButton0.config(font='Helvetica 9 bold', text="< " + str(self.umbrales_actual[0]) + self.unidad_actual, bg=self.colores[0])
        self.colorButton1 = tk.Button(master, width="18", command = lambda: self.set_color(self.colorButton1))
        self.colorButton1.config(font='Helvetica 9 bold', text=">= " + str(self.umbrales_actual[0]) + self.unidad_actual + " y < " + str(self.umbrales_actual[1]) + self.unidad_actual, bg=self.colores[1])
        self.colorButton2 = tk.Button(master, width="18", command = lambda: self.set_color(self.colorButton2))
        self.colorButton2.config(font='Helvetica 9 bold', text=">= " + str(self.umbrales_actual[1]) + self.unidad_actual, bg=self.colores[2])
        self.aceptarButton = tk.Button(master, text='Aceptar', width=10, command= lambda: self.aceptar_ajustes('aceptar'))
        self.aplicarButton = tk.Button(master, text='Aplicar', width=10, command= lambda: self.aceptar_ajustes('aplicar'))
        self.cancelarButton = tk.Button(master, text='Cancelar', width=10, command=self.cancelar_ajustes)
        # Ajustar la posición de los elementos
        self.rangoLabel.grid(row=0, column=0, padx=(5, 25), pady=(25,0))
        self.minimoEntry.grid(row=1, column=0, padx=(10, 10), sticky='W')
        self.maximoEntry.grid(row=1, column=0, padx=(10, 25), sticky='E')
        self.umbralRadioLabel.grid(row=2, column=0, padx=(5, 25), pady=(25,0))
        self.umbralRadio0.grid(row=3, column=0, padx=(5, 25))
        self.umbralRadio1.grid(row=4, column=0, padx=(5, 25))
        self.umbralLabel.grid(row=0, column=1, padx=(0, 25), pady=(25,0))
        self.umbralEntry0.grid(row=1, column=1, padx=(10, 25), sticky='W')
        self.umbralEntry1.grid(row=1, column=1, padx=(0, 25), sticky='E')
        self.colorButton0.grid(row=2, column=1, padx=(0, 5), pady=(25,0))
        self.colorButton1.grid(row=3, column=1, padx=(0, 5))
        self.colorButton2.grid(row=4, column=1, padx=(0, 5))
        self.aceptarButton.grid(row=5, column=0, padx=(10, 25), pady=(25,25), sticky='W')
        self.aplicarButton.grid(row=5, column=0, columnspan=2, padx=(25, 25), pady=(25,25))
        self.cancelarButton.grid(row=5, column=1, padx=(0, 10), pady=(25,25), sticky='E')

    def set_color(self, widget):
        button_index = str(widget)[-1:]
        if button_index == 'n':
            button_index = 1
        button_index = int(button_index)-1
        color = askcolor(initialcolor = self.colores[button_index])
        if button_index == 0:
            widget.config(font='Helvetica 9 bold',  text="< " + str(self.umbrales_actual[0]) + self.unidad_actual, bg=color[1])
        elif button_index == 1:
            widget.config(font='Helvetica 9 bold',  text=">= " + str(self.umbrales_actual[0]) + self.unidad_actual + " y < " + str(self.umbrales_actual[1]) + self.unidad_actual, bg=color[1])
        else:
            widget.config(font='Helvetica 9 bold',  text=">= " + str(self.umbrales_actual[1]) + self.unidad_actual, bg=color[1])

    def cambiar_umbral(self):
        self.minimoEntry.focus_set()
        if self.tipo_umbral.get() == 'P':
            self.tipo_umbral.set('P')
            self.umbrales_actual = self.umbrales_porc
            self.unidad_actual = "%"
        elif self.tipo_umbral.get() == 'V':
            self.tipo_umbral.set('V')
            self.umbrales_actual = self.umbrales_val
            self.unidad_actual = " " + self.unidad
        self.umbralEntry0.delete(0,'end')
        self.umbralEntry0.insert(0, self.umbrales_actual[0])
        self.umbralEntry1.delete(0,'end')
        self.umbralEntry1.insert(0, self.umbrales_actual[1])
        self.colorButton0.config(text="< " + str(self.umbrales_actual[0]) + self.unidad_actual, bg=self.colores[0])
        self.colorButton1.config(text=">= " + str(self.umbrales_actual[0]) + self.unidad_actual + " y < " + str(self.umbrales_actual[1]) + self.unidad_actual, bg=self.colores[1])
        self.colorButton2.config(text=">= " + str(self.umbrales_actual[1]) + self.unidad_actual, bg=self.colores[2])

    def aceptar_ajustes(self, tipo_accion):
        umbral0 = redondear(float(self.umbralEntry0.get()), float(self.umbralEntry1.get()))
        umbral1 = redondear(float(self.umbralEntry1.get()), float(self.umbralEntry1.get()))
        umbral0, umbral1 = self.validar_entries(umbral0, umbral1)
        if self.tipo_umbral.get() == 'P':
            umbrales_porc = [umbral0]
            umbrales_porc.append(umbral1)
            umbrales_val = self.umbrales_val
            self.colorButton0.config(text="< " + str(umbrales_porc[0]) + self.unidad_actual, bg=self.colores[0])
            self.colorButton1.config(text=">= " + str(umbrales_porc[0]) + self.unidad_actual + " y < " + str(umbrales_porc[1]) + self.unidad_actual, bg=self.colores[1])
            self.colorButton2.config(text=">= " + str(umbrales_porc[1]) + self.unidad_actual, bg=self.colores[2])
        else:
            umbrales_val = [umbral0]
            umbrales_val.append(umbral1)
            umbrales_porc = self.umbrales_porc
            self.colorButton0.config(text="< " + str(umbrales_val[0]) + self.unidad_actual, bg=self.colores[0])
            self.colorButton1.config(text=">= " + str(umbrales_val[0]) + self.unidad_actual + " y < " + str(umbrales_val[1]) + self.unidad_actual, bg=self.colores[1])
            self.colorButton2.config(text=">= " + str(umbrales_val[1]) + self.unidad_actual, bg=self.colores[2])
        colores = [self.colorButton0.cget('background')]
        colores.append(self.colorButton1.cget('background'))
        colores.append(self.colorButton2.cget('background'))
        minimo = redondear(float(self.minimoEntry.get()), float(self.maximoEntry.get()))
        maximo = redondear(float(self.maximoEntry.get()), float(self.maximoEntry.get()))
        # Validar entries
        minimo, maximo = self.validar_entries(minimo, maximo)
        if self.minimoEntry.get() != str(minimo):
            self.minimoEntry.delete(0,'end')
            self.minimoEntry.insert(0, str(minimo))
        if self.maximoEntry.get() != str(maximo):
            self.maximoEntry.delete(0,'end')
            self.maximoEntry.insert(0, str(maximo))
        ajustes = {
            "umbrales_porc": umbrales_porc,
            "umbrales_val": umbrales_val,
            "tipo_umbral": self.tipo_umbral.get(),
            "colores": colores,
            "minimo": str(minimo),
            "maximo": str(maximo)
        }
        self.main.save_ajustes_medidor(self, ajustes, tipo_accion)

    def cancelar_ajustes(self):
        self.minimoEntry.delete(0,'end')
        self.minimoEntry.insert(0, self.minimo_rango)
        self.maximoEntry.delete(0,'end')
        self.maximoEntry.insert(0, self.maximo_rango)
        self.umbralEntry0.delete(0,'end')
        self.umbralEntry0.insert(0, self.umbrales_actual[0])
        self.umbralEntry1.delete(0,'end')
        self.umbralEntry1.insert(0, self.umbrales_actual[1])
        self.colorButton0.config(font='Helvetica 9 bold', text="< " + str(self.umbrales_actual[0]) + self.unidad_actual,bg=self.colores[0])
        self.colorButton1.config(font='Helvetica 9 bold',text=">= " + str(self.umbrales_actual[0]) + self.unidad_actual + " y < " + str(self.umbrales_actual[1]) + self.unidad_actual, bg=self.colores[1])
        self.colorButton2.config(font='Helvetica 9 bold',text=">= " + str(self.umbrales_actual[1]) + self.unidad_actual, bg=self.colores[2])
        self.main.desplegar_ajustes(self.master)

    def validar_entries(self, valor1, valor2):
        if valor1 > valor2:
            # Si el valor1 es mayor que el valor2, se intercambian
            aux = valor2
            valor2 = valor1
            valor1 = aux
        elif valor1 == valor2:
            # Si son iguales, se le suma 1 al valor2
            valor2 += 1
        return valor1, valor2

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