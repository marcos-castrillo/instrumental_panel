import tkinter as tk
import meter as m

class Frame(tk.Frame):
	def __init__(self,master,*args,**kwargs):
		super(Frame,self).__init__(master,*args,**kwargs)
		# Meter toma 2 parámetros, altura y ancho
		height = int(self['height'])
		width = int(self['width'])
		rango_min = int(self['rango_min'])
		rango_max = int(self['rango_max'])
		self.meter = m.Meter(self,height = height,width = width)
		# Rango de valores útiles
		self.meter.setrange(rango_min, rango_max)
		self.meter.pack()
		# Rango de valores gráficos
		tk.Scale(self,width = 15 ,from_ = 0, to = 200
		,orient = tk.HORIZONTAL
		,command = self.setmeter).pack()
		# Botón de salir
		tk.Button(self,text = 'Salir',width = 15,command = master.destroy).pack()
	def setmeter(self,value):
		value = int(value)
		self.meter.set(value)
