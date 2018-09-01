#importamos módulo para comunicarnos con la placa y librerias
import clase_voltaje.py

import numpy as np
import matplotlib.pyplot as plt
import pyaudio
from pyaudio import PyAudio as pa
import wave 


#%% Generamos una señal

señal = armonica(100,120) #esto lo elegimos según la señal que querramos emitir

#modo callback

def callback_emision(in_data, frame_count, time_info, status):  #stream_callback pide una función de 4 argumentos.
		data = señal.readframes(frame_count) #pedazo de señal
		return (data, pyaudio.paContinue)   

emision_call = emitir(BITRATE, callback_emision)     

#modo bloqueo

#emision_block = emitir(señal, BITRATE)


#%% Medimos señal

#modo callback

def callback_medición(in_data, frame_count, time_info, status):
    return (in_data, pyaudio.paContinue)
# no se si está bien así la callback para medir
    
medicion_call = medir(500, callback_medicion)

#modo bloqueo

#medicion_block = medir(500)
