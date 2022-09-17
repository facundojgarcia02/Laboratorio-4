import matplotlib.pyplot as plt
import numpy as np
import nidaqmx
import math
import time

def getDeviceName():
    system = nidaqmx.system.System.local()
    for device in system.devices:
        print(device)

DEVICE_NAME = "Dev2"

#%%
## Medicion por tiempo/samples de una sola vez
def medicion_una_vez(DevName, channel, duracion, fs):
    cant_puntos = int(duracion*fs)
    
    with nidaqmx.Task() as task:
        modo= nidaqmx.constants.TerminalConfiguration.DIFF #Differential
        
        task.ai_channels.add_ai_voltage_chan(f"{DevName}/ai{channel}", terminal_config = modo)
               
        task.timing.cfg_samp_clk_timing(fs,samps_per_chan = cant_puntos,
                                        sample_mode = nidaqmx.constants.AcquisitionType.FINITE)
        
        datos = task.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE)           
    datos = np.asarray(datos)    
    return datos

duracion = 0.1 #segundos
fs = 250000 #Frecuencia de muestreo

medVref = lambda : medicion_una_vez(DEVICE_NAME, 1, duracion, fs)
medVplat = lambda : medicion_una_vez(DEVICE_NAME, 2, duracion, fs)

#%%

Rplat_list = []
i = 0
measuring = True
try:
    while measuring:
        
        print(f"Midiendo {i}", end = "\r")
        Vref = medVref()
        Vplat = medVplat()
        
        Rref = 9.91*1000
        I = Vref/Rref
        
        Rplat = Vplat/I
        
        Rplat_list.append(Rplat.mean())
        
        i+=1

except KeyboardInterrupt:
    measuring = False
    plt.plot(Rplat_list)

#%%



#%%

fig, ax = plt.subplots(1, 2, figsize = (14,5))
ax[0].plot(Rplat_val, color = "blue", label = "Mediciones")
ax[1].plot(Rref_val, color = "blue", label = "Mediciones")

ax[0].axhline(np.mean(Rplat_val), color = "red", label = "Promedio")
ax[1].axhline(np.mean(Rref_val), color = "red", label = "Promedio")

ax[0].set_xlabel("Num Mediciones")
ax[0].set_ylabel("Voltaje [V]")
ax[0].set_title("Caida de voltaje sobre\nResistencia platino")

ax[1].set_xlabel("Num Mediciones")
ax[1].set_ylabel("Voltaje [V]")
ax[1].set_title("Caida de voltaje sobre\nResistencia referencia")

ax[1].grid()
ax[0].grid()

ax[0].legend(loc = "upper right")
ax[1].legend(loc = "upper right")

plt.show()
