from pandas import DataFrame
from utils.experiments.handler import ExperimentHandler
from utils.equipment import EdwardsManometer, Amprobe38XRA
        
class Vacuum(ExperimentHandler):
    """
    Cambios necesarios al iniciar el experimento:
          
        - Cambiar los puertos de Comunicación y el gauge al crear la clase.
          
        - Cambiar MEASURE_R, MEASURE_P según corresponda a medir.
          RECOMENDACION: Si van a cambiar los valores de estas variables,
          es recomendable reiniciar el código para terminar las comunicaciones
          anteriores.
    """
    
    def __init__(self, MEASURE_R: bool = False, MEASURE_P: bool = True,
                 DEBUG: bool = False, PLOT: bool = True,
                 mult_com: str = "COM1", manm_com: str = "COM2",
                 gauge: int = 1):
        
        
        super().__init__(DEBUG, PLOT) #Starts DEBUG and PLOT
        
        self.meds = []
        
        self.MEASURE_R = MEASURE_R
        self.MEASURE_P = MEASURE_P
        
        self.i_list = []
        self.dt_list = []
        
        if self.MEASURE_R:
            self.mult = Amprobe38XRA(port = mult_com)
            self.p_list = []
            self.p_time_list = []
            
        if self.MEASURE_P:
            self.manm = EdwardsManometer(port = manm_com, gauge = gauge)
            self.R_list = []
            self.R_time_list = []
        
    def measure(self):
        
        if self.MEASURE_P: 
            self.p = self.manm.GetPressure()
            self.p_time = time()
        
        if self.MEASURE_R:
            self.R, _ = self.mult.GetValue(verbose=False)
            self.R_time = time()

    def save_measure(self):
        
        self.i_list.append(self.i)
        self.dt_list.append(self.dt)
        
        if self.MEASURE_P:
            self.p_list.append(self.p)
            self.p_time_list.append(self.p_time)
                    
        if self.MEASURE_R:
            self.R_list.append(self.R_list)
            self.R_time_list.append(self.R_time_list)

    def get_plot(self):
        
        if self.MEASURE_P and self.MEASURE_R:
            raise Exception("Cant plot at same time R and P")
            
        elif self.MEASURE_P:
            return self.p_time_list, self.p_list
        
        elif self.MEASURE_R:
            return self.R_time_list, self.R_list
        
    def create_df(self):
        
        if self.MEASURE_P and self.MEASURE_R:
            return DataFrame({"i": self.i_list, "dt": self.dt_list, 
                              "p_time": self.p_time_list, "p": self.p_list,
                              "R_time": self.R_time_list, "R": self.R_list})

        elif self.MEASURE_P:
            return DataFrame({"i": self.i_list, "dt": self.dt_list, 
                              "p_time": self.p_time_list, "p": self.p_list})

        elif self.MEASURE_R:
            return DataFrame({"i": self.i_list, "dt": self.dt_list, 
                              "R_time": self.R_time_list, "R": self.R_list})
