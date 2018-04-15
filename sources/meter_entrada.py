import tkinter as tk
import meter as m
import serial

class Mainframe(tk.Frame):

    def __init__(self,master,*args,**kwargs):
        super(Mainframe,self).__init__(master,*args,**kwargs)

        self.meter = m.Meter(self,height = 400,width = 400)
        self.meter.setrange(20,90)
        self.meter.pack()

        tk.Scale(self,width = 15 ,from_ = 20, to = 90
        ,orient = tk.HORIZONTAL
        ,command = self.setmeter).pack()

        tk.Button(self,text = 'Quit',width = 15,command = master.destroy).pack()
        tk.Button(self,text = 'Zoom',width = 15).pack()

        #while (1):


        ser = serial.Serial('COM2', 2400, timeout=1)# /dev/ttyS1
        line = ser.readline()   # read a '\n' terminated line
        print (line)
        #      self.after(1000,self.recibir_serial)



        def setmeter(self,value):
            value = int(value)
            self.meter.set(value)



            class App(tk.Tk):
                def __init__(self):
                    super(App,self).__init__()

                    self.title('Try Meter')

                    Mainframe(self).pack()



                    #        ser = serial.Serial('COM2', 2400, timeout=1)
                    #        line = ser.readline()
                    #        print (line)

                    App().mainloop()
