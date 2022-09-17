from pandas import DataFrame
from utils.experiments.handler import Experiment
import time
import numpy as np

class Test(Experiment):
    
    def __init__(self, PLOT: bool = True, DEBUG: bool = False):
        """
        Method for starting arrays and required objects.
        """
        super().__init__(PLOT = PLOT, DEBUG = DEBUG) #Sets PLOT and DEBUG
        
        f = lambda x: x**0.5 #For testing.
        t0 = time.time()
        
        self.medFuncs = {"y": lambda : f(time.time() - t0)}
        self.start_dict()
        
    def get_plot(self) -> tuple:
        xkey = "i"
        ykey = "y"
        
        x = np.array(self.currentVals[xkey])
        y = np.array(self.currentVals[ykey])
        return x, y