import nidaqmx
import visa #Should be installed as pyvisa
import serial #Should be installed as pyserial

import numpy as np

class Amprobe38XRA:
    """
    Multimetro Amprobe 38XRA.
    """

    def __init__(self, port='COM1'):
        print("[LOG] - Iniciando comunicacion con Amprobe38XRA")
        self._mult = serial.Serial()        
        self._mult.baudrate = 9600
        self._mult.port = port
        self._mult.bytesize = 8
        self._mult.parity = 'N'
        self._mult.stopbits = 1
        self._mult.timeout = None    
        self.open() 
        print("[LOG] - Comunicación realizada con éxito")
            
    def open(self):
        if not self._mult.is_open:
            self._mult.open()            

    def close(self):
        self._mult.close()	        

    def __del__(self):
        self._mult.close()	        
        
    def __LeeStringAmprobe(self):
        #%Lee el string que manda el multimetro.
        #%A veces manda strings de distintas longitudes. Itero hasta que me da uno
        #%de 15 caracteres.
    
        self._mult.flushInput()
        count = 0
        mystr = ""
        while len(mystr)!=15:
            count = count+1
            mystr =self._mult.readline().decode('ascii')
            if len(mystr)==0:
                print('Salgo, probablemente timeout, desconecatado')
                return mystr
        return mystr        

    def __ProcesaStringAmprobe(self,mystr,verbose):
        #%extraigo los valores pertinentes del string
        code = mystr[0:2]
        data=(mystr[2:6])
        modo=float(mystr[6])
        exponente=float(mystr[8])
        acdc=float(mystr[9])
        absrel=(mystr[11]) # 8|A  8: rango fijo, A: Autorango
        signo=float(mystr[12])
        
        if data == 'B0DD':
            print('Resistencia infinita')
            data = float('inf')
        else:
            data = float(data)
    
        #%muestro en pantalla (si me lo piden)
        if verbose:
            print('Str:  %s'%(mystr))
            print('Code: %s'%(code))
            print('Data:   %04.0f'%(data))
            print('Modo:       %d'%(modo))
            print('str(8):      %s'%(mystr[7]))
            print('Exp:          %d'%(exponente))
            print('AC|DC|AC+DC:   %d'%(acdc))
            print('str(11):        %s'%(mystr[10]))
            print('absrel:          %s'%(absrel))
            print('Signo:            %d'%(signo))
        
        if code == '10': #Voltmeter ~
            if modo == 0:
                Ylab = 'Voltage ~ [V]'  
                value = data*1e-4*1.0*pow(10,exponente)
            else: 
                Ylab  = 'Voltage ~ [dBm]';
                value = pow(-1,signo)*data*0.01;
        elif code == '0C': #Voltmeter --
            Ylab = 'Voltage';        
            Ylab = Ylab +' DC [V]'
            value = pow(-1,signo)*data*1.0*pow(10,exponente-4)
        elif code=='08': # Ohm-meter
            Ylab  = 'Resistance [Ohm]';
            value = pow(-1,signo)*data*1.0*pow(10,4-exponente)
        elif code == '04':  # Test diode
            Ylab = 'Test diode [V]'
            value = data/1000
        elif code == '0F':  # Frequencemeter
            value = pow(-1,signo)*data*0.01*pow(10,exponente)
            if modo == 2:
                Ylab  = 'Cyclic Rate [%]'
            else:
                Ylab = 'Frequency [Hz]'
        elif code == '0B':  # Capacity
            Ylab = 'Capacity [µF]'    
            value = pow(-1,signo)*data*pow(10,exponente-5)
        elif code == '07':  # Current µA
            Ylab = 'Current [A]'
            value = pow(-1,signo)*data*pow(10,exponente-8)
            if acdc == 0:
                Ylab= 'DC ' + Ylab  
            elif acdc == 1:
                Ylab= 'AC ' + Ylab  
            elif acdc == 2:
                Ylab= 'AC+DC ' + Ylab  
        elif code == '0E':  # Current mA
            Ylab = 'Current [A]'
            value = pow(-1,signo)*data*pow(10,exponente-6)
            if acdc == 0:
                Ylab= 'DC ' + Ylab  
            elif acdc == 1:
                Ylab= 'AC ' + Ylab  
            elif acdc == 2:
                Ylab= 'AC+DC ' + Ylab  
        elif code == '0A':  # Current A
            Ylab = 'Current [A]'
            value = pow(-1,signo)*data/1000
            if acdc == 0:
                Ylab= 'DC ' + Ylab  
            elif acdc == 1:
                Ylab= 'AC ' + Ylab  
            elif acdc == 2:
                Ylab= 'AC+DC ' + Ylab  
        elif code == '03':  # mA 4-20 --
            Ylab = 'Current 4-20 [mA] --'
            value = data
        elif code == '06':  #Temperature [°C]
            Ylab = 'Temperature [°C]'
            value = pow(-1,signo)*data
        elif code == '02':  #Temperature [°F]
            Ylab = 'Temperature [°F]'
            value = pow(-1,signo)*data
        else:
            value = 0
            Ylab = ""
            
        if absrel=='8':
            Ylab= 'Delta ' + Ylab  
            
        return value,Ylab
    
    def GetValue(self,verbose=False):
        mystr = self.__LeeStringAmprobe()
        value, Ylab = self.__ProcesaStringAmprobe(mystr,verbose)
        return value, Ylab