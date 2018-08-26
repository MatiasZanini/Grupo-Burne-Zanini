# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 17:15:27 2018

@author: Mati
"""

#%%

#Importamos las librerías y seteamos el rate.

import numpy as np
import matplotlib.pyplot as plt
from pyaudio import PyAudio as pa
import math

BITRATE=44100

#%%
class Señal:

    #---------------Emision--------------------------

    #Señal armonica de amplitud V, frecuencia f, duracion T.

    def Armonica(V,f,T):

        onda=''
        onda_plot=''
        cant_puntos = int(BITRATE * T)
        silencios = cant_puntos % BITRATE
        
        for x in range(cant_puntos):
            onda += chr(int(math.sin(x / ((BITRATE / f) / math.pi)) * 127 + 128))
            #onda_plot += int(math.sin(x / ((BITRATE / f) / math.pi)) * 127 + 128)
        #Llenamos lo que falta de duracion con silencios
        for x in range(silencios): 
            onda += chr(128)
            #onda_plot += 0
        
        #plt.plot(onda)
            
        p = pa()
        stream = p.open(
            format=p.get_format_from_width(1),
            channels=1,
            rate=BITRATE,
            output=True,
            )
        stream.write(onda)
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        #return onda_plot
    
    