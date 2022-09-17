import nidaqmx
import visa #Should be installed as pyvisa
import serial #Should be installed as pyserial

import numpy as np

class EdwardsManometer:
    """
    Manómetro Edwards para la cámara de vacío.
    """
    
    def __init__(self, port: str = 'COM1', gauge: int = 1): 
        print("[LOG] - Iniciando comunicacion")
        self._gauge = serial.Serial(port, baudrate=9600)     
        self._gauge.baudrate = 9600
        self._gauge.port = port
        self._gauge.bytesize = 8
        self._gauge.parity = 'N'
        self._gauge.stopbits = 1
        self._gauge.timeout = 1   
        self.open() 
        
        if gauge == 1:
            self.g_str = b'?GA1\r'
        elif gauge == 2:
            self.g_str = b'?GA2\r'
        else:
            raise ValueError("Invalid gauge")
            
        print("[LOG] - Comunicación realizada con éxito")

    def open(self):
        if not self._gauge.is_open:
            self._gauge.open()            

    def close(self):
        self._gauge.close()	        

    def GetPressure(self):        
        pressure = ""
        while len(pressure) != 9:
            self._gauge.write(self.g_str) #Cambiar el numero por el que corresponda.        
            pressure = self._gauge.readline()
            if pressure[:2]=="ERR":
                print("Error message: ",pressure)
        try:
            pres = float(pressure.decode('ascii'))
        except:
            pres = "ERR"
        return pres