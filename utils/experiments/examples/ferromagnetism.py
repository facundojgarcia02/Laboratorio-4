import nidaqmx
import numpy as np

from pandas import DataFrame

from utils.experiments.handler import Experiment
from utils.calculus import PT100
from utils.equipment.daq import DAQ


class Ferromagnetism(Experiment):
    
    def __init__(self, fs: float = 250000/2, Rref: float = 9.91*1000, PLOT = True, DEBUG = False):
        super().__init__(PLOT = PLOT, DEBUG = DEBUG)
        
        #Iniciación de objectos
        self.Tpoly = PT100().get_poly()
        daq = self.DAQ()
        
        #Parametros importantes del experimento.
        self.Rref = Rref
        
        #Medicion de V1 y V2
        medVs = lambda : daq.measure_one_time(channels = [3, 4], 
                                              duracion = 1, 
                                              fs = fs, 
                                              vals = [[-3, 3], [-3, 3]])
        
        #Medicion de R
        medVref = lambda : daq.measure_one_time(channels = 1, duracion = 0.01, fs = fs)
        medVplat = lambda : daq.measure_one_time(channels = 2, duracion = 0.01, fs = fs)

        def medRPlat():            
            Vref = medVref()
            Vplat = medVplat()                
            I = Vref/self.Rref        
            Rplat = Vplat/I        
            Rplat = Rplat.mean()
            
            return Rplat
        
        #Creamos el diccionario de funciones para medir.
        self.medFuncs = {"RplatPre": medRPlat, "Vs": medVs, "RplatPost": medRPlat} 
        
        #Requerido siempre.
        self.start_dict(extra_values = ["Tpre", "V1", "V2", "TPost"])
        
    def measure(self):
        super().measure()
        self.currentVals["TPre"] = self.Tpoly(self.currentVals["RplatPre"])
        self.currentVals["V1"] = (self.currentVals["Vs"][0, :])
        self.currentVals["V2"] = (self.currentVals["Vs"][1, :])
        self.currentVals["TPost"] = self.Tpoly(self.currentVals["RplatPost"])
        
    def get_plot(self):
        xkey = "V1"
        ykey = "V2"
        
        x = np.array(self.currentVals[xkey])
        y = np.array(self.currentVals[ykey])
        return x, y        
    
    def create_df():
        df = super().create_df()
        df.drop(columns = ["Vs"], inplace = True)
        return df