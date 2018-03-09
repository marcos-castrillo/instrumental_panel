import tkinter as tk
import meter as m
import random


rango_min=0
rango_max=200
limite_warning=150
height=800
width=800

tk.Button(self,text = 'Salir',width = 15,command = master.destroy).pack()
meter=tk.Tk()
meter.title("Medidor")
meter=m.Meter(meter,height=height,width=width)
meter.setrange(rango_min,rango_max)
meter.pack()
meter.blob("black")

		
def newvalue():
    value=rango_max*float(random.random())
    meter.set(int(value))
    if value>limite_warning:
            meter.blob("red")
    else:
            meter.blob("black")
    meter.after(200,newvalue)

meter.after(200,newvalue())
meter.mainloop()
