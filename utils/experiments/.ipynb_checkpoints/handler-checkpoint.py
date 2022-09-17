import matplotlib.pyplot as plt
import numpy as np

from pandas import DataFrame
from time import time, sleep

from utils.misc import NotImplementedError
from utils.plotting import BlitManager

class Experiment:
    """
    Every Experiment requires the following methods.
    """
    
    def __init__(self, DEBUG = False, PLOT = True):
        
        self.DEBUG = DEBUG
        self.PLOT = PLOT
    
    def get_plot(self):
        """
        Method for plotting.
        """
        raise NotImplementedError("Subclass responsability. Did you check if your experiment has all required methods?")
            
    """
    Optional methods.
    """
    def measure(self):
        """
        Method for taking measures.
        """
        self.currentVals = {}
        for k, f in self.medFuncs.items():
            self.currentVals[k] = f()
        self.currentVals["t"] = self.t
        self.currentVals["i"] = self.i 

    def start_dict(self, extra_values = []):
        all_keys = list(self.medFuncs) + extra_values + ["t", "i"]
        
        self.currentVals = {k: None for k in all_keys}
        self.storedVals = {k: [] for k in all_keys}
        
    def save_measure(self):
        """
        Method for saving measures.
        """
        for k, v in self.currentVals.items():
            self.storedVals[k].append(v)
    
    def create_df(self):
        "Creates pandas DataFrame with results"
        return DataFrame(self.storedVals)
    
        
    """
    Further custom methods for measuring and plotting. Not required in children classes.
    """
    def quick_measure(self):
        """
        Takes one measure and returns a dict.
        """
        self.measure()
        self.save_measure()
    
        df = self.create_df()
        return df.to_dict()
    
    def N_measure(self, N: int) -> DataFrame:
        """
        Takes N measures. Can be stopped from keyboard.
        """

        ### PLOT ----------------------------------------------------

        if self.PLOT:
            fig, ax = plt.subplots(figsize=(5,5))
            ax.set_xlim(0, 30)
            ax.set_ylim(100, 120)
            plt.show(block=False)
            plt.pause(.1)

            ln, = ax.plot([], [], "-", color="black",animated=True)
            bm = BlitManager(fig.canvas, [ln])

        ### MEASURES ------------------------------------------------
        try:
            for i in range(N): #Measures untils is stopped
                if self.DEBUG: print(f"[DEBUG] - Measuring {i}", end="\r")

                self.t = time()
                self.i = i
                self.measure()

                #PLOT ----------------------------------------------

                #Plots in real time.
                if self.PLOT:
                    ln.set_data(*self.get_plot())
                    bm.update()

                #Saves dt for checking plotting time purpose.
                self.dt = time() - self.t

                self.save_measure()

                #Waits until the next measure.
                sleep(0.1)

        except KeyboardInterrupt: #If While is stopped save the measurements.
            df = self.create_df()
        finally:
            df = self.create_df()

        return df
    
    def inf_measure(self) -> DataFrame:
        """
        Takes measures until the functions is stopped from keyboard.
        """

        self.i = 1 #Counter

        ### PLOT ----------------------------------------------------

        if self.PLOT:
            fig, ax = plt.subplots()
            ax.set_xlim(-0.5, 0.5)
            ax.set_ylim(0.5, 1.5)
            plt.show(block=False)
            plt.pause(.1)

            ln, = ax.plot([], [], "-", color="black",animated=True)
            bm = BlitManager(fig.canvas, [ln])

        ### MEASURES ------------------------------------------------
        try:
            while True: #Measures untils is stopped
                if self.DEBUG: print(f"[DEBUG] - Measuring {self.i}", end="\r")

                self.t = time()
                self.measure()

                #PLOT ----------------------------------------------

                #Plots in real time.
                if self.PLOT:
                    x, y = self.get_plot()
                    ln.set_data(x, y)                    
                    bm.update()

                #Saves dt for checking plotting time purpose.
                self.dt = time() - self.t

                self.save_measure()

                #Add counter and wait for the next measurement.
                self.i += 1
                sleep(0.1)

        except KeyboardInterrupt: #If While is stopped save the measurements.
            df = self.create_df()

        return df
