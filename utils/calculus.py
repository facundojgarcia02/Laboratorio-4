import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

class PT100:

    def get_poly(self, filename: str = "files/Pt100_resistencia_temperatura.csv"):
        """
        Interpolates PT100 data.

        Parameters:
        -----------
            - filename: str -> Path to Pt100 DataSheet.
        """

        data = np.loadtxt(filename,delimiter=',', unpack = True) 
        temperature_vals = data[0, :]
        resistance_vals = data[1, :]

        poly = interp1d(resistance_vals, temperature_vals)

        return poly #Ohm -> Celcius

    def get_errorcoeff(self, filename: str = "files/Pt100_resistencia_temperatura.csv"):
        """
        Get polynomial coefficienties for calculating error.

        Parameters:
        -----------
            - filename: str -> Path to Pt100 DataSheet.
        Returns:
            - popt: np.ndarray -> Coefficients of interpolator polynomial.
        """
        df = pd.read_csv(filename, header = None, names = ["T", "R"])

        def func(x, coeffs):
            """
            c[0] + c[1]*x + ... + c[-1] * x**(len(c) - 1)
            """
            suma = 0
            for i, c in enumerate(coeffs):
                suma += x**i * c
            return suma

        def func2(*args):
            return func(args[0],args[1:])

        r = np.array(df["R"])
        t = np.array(df["T"])

        popt, pcov = curve_fit(func2, r, t, p0 = np.ones(12))

        return popt

    def get_errorpoly(self, filename: str = "files/Pt100_resistencia_temperatura.csv"):
        """
        Get function for calculating Temperature error in °C.

        Parameters:
        -----------
            - filename: str -> Path to Pt100 DataSheet.
        Returns:
        --------
            - Terr: callable -> Function for calculating Temperature error.
        """

        popt = self.get_errorcoeff(filename) #Consigo los coefiencientes del polinomio "interpolador"
        coeffs = popt[1:]*np.arange(1, len(popt)) #Multiplicamos por los coeficientes que bajan al derivar
        polyerr = np.polynomial.Polynomial(coeffs) # Construimos el polinomio.

        Rerr = lambda R: R*0.05 #Error de la resistencia.
        Terr = lambda R: polyerr(R)*Rerr(R) #sigma_T = dT/dR * sigma_R

        return Terr

class NTC:
    
    def get_poly(self):
        
        a,b,c,d,e,f = [ 8.30898289e+02, -4.43056704e+02,  1.16417971e+02, -1.87119140e+01,
                           1.63900559e+00, -5.96756860e-02]

        def f(R, a, b, c, d, e, f):
            logR = np.log10(R)
            return a + b*logR + c*logR**2 + d*logR**3 + e*logR**4 + f*logR**5
        
        return lambda R: f(R, a, b, c, d, e, f) #Devuelve un evaluador del polinomio.
    
    def get_errorpoly(self):
        
        a,b,c,d,e,f = [ 8.30898289e+02, -4.43056704e+02,  1.16417971e+02,
                           -1.87119140e+01,1.63900559e+00, -5.96756860e-02]
            
        def Terr(R, a, b, c, d, e, f):
            Rerr = R*0.05 + 1 * 8 #Segun manual para el rango de resistencias donde se realiza el experimento.
            logR = np.log(R)
            factor = lambda n: n*logR**(n-1)/np.log(10)**n/R
            dTdR = b*factor(1) + c*factor(2) + d*factor(3) + e*factor(4) + f*factor(5)
            return dTdR*Rerr
        
        return lambda R: Terr(R, a, b, c, d, e, f) #Devuelve un evaluador del polinomio para el error.
        
