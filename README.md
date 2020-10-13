# PYTHON INSTRUMENTAL PANEL

Monitorization of a Stirling engine.

The data is received from an Arduino and displayed on a LCD using a Raspberry Pi.

My contribution to the project was writing the code to analyze the received data and represent it in real time using different gauges and charts. I had to mock the data because that part of the project wasn't ready yet.

This code was written for my Thesis during 2017/2018.

# Dependencies:

* Python >= 3.5.3 (Installed by default in Raspbian)
* Tkinter module

# FAQ:

ImportError: No module named 'meter'
* Every .py file has to be in the same folder.
* Execute the next command being in this folder:
``` export PYTHONPATH=`pwd` ```

