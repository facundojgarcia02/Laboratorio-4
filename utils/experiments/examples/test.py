from pandas import DataFrame
from utils.experiments.handler import ExperimentHandler

class Test(ExperimentHandler):
    
    def __init__(self, PLOT: bool = True, DEBUG: bool = False):
        """
        Method for starting arrays and required objects.
        """
        super().__init__() #Sets PLOT and DEBUG
        
        self.f = lambda x: x**0.5 #For testing.
        self.t_list = [] #For testing.

        self.i_list = [] #ID de la medición
        self.y_list = [] #Valor de la medición

    def measure(self):
        """
        Method for taking measures.
        """
            
        #Gets the interestings values.
        self.y = self.f(self.i)
           
    def save_measure(self):
        """
        Method for saving measures.
        """
        #Appends the measurements to lists.
        self.i_list.append(self.i)
        self.y_list.append(self.y)
        self.t_list.append(self.dt)
        
    def get_plot(self) -> tuple:
        x = self.i_list
        y = self.y_list
        return x, y
    
    def create_df(self) -> DataFrame:
        """
        Method for creating DataFrame with measures.
        """
        return DataFrame({"index": self.i_list, "value": self.y_list, "dt": self.t_list})