import nidaqmx
import visa #Should be installed as pyvisa
import serial #Should be installed as pyserial

import numpy as np

class DAQ:
    """
    Handler Placa DAQ.
    """
    
    def __init__(self):
        system = nidaqmx.system.System.local()
        for device in system.devices:
            print(device)
        self.DeviceName = input("Write the target device name")

    def measure_one_time(self, channels, duracion, fs, vals = None):
        if self.DeviceName is None:
            raise ValueError("DeviceName not selected.")
        cant_puntos = int(duracion*fs)

        with nidaqmx.Task() as task:
            modo= nidaqmx.constants.TerminalConfiguration.DIFF #Differential
            
            if type(channels) == list: #Si hay dos canales o mas
                for i, channel in enumerate(channels):
                    if vals[i] is None:                
                        task.ai_channels.add_ai_voltage_chan(f"{self.DeviceName}/ai{channel}", terminal_config = modo)
                    else:
                        task.ai_channels.add_ai_voltage_chan(f"{self.DeviceName}/ai{channel}", terminal_config = modo, min_val = vals[0], max_val = vals[1])
                        
            else: #Si hay un solo canal
                if vals is None:                
                    task.ai_channels.add_ai_voltage_chan(f"{self.DeviceName}/ai{channel}", terminal_config = modo)
                else:
                    task.ai_channels.add_ai_voltage_chan(f"{self.DeviceName}/ai{channel}", terminal_config = modo, min_val
                

            task.timing.cfg_samp_clk_timing(fs,samps_per_chan = cant_puntos,
                                            sample_mode = nidaqmx.constants.AcquisitionType.FINITE)

            datos = task.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE)           

        datos = np.asarray(datos)    
        return datos