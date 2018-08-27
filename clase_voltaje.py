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

    

    def Armonica(freq_arm,dur_arm):  #Señal armonica de amplitud 256 bits (suponemos 5V), frecuencia freq_arm, duracion dur_arm.

        onda=''
        cant_puntos = int(BITRATE * dur_arm)
        silencios = cant_puntos % BITRATE
        
        for x in range(cant_puntos):
            onda += chr(int(math.sin(x / ((BITRATE / freq_arm) / math.pi)) * 127 + 128))
            
        #Llenamos lo que falta de duracion con silencios
        for x in range(silencios): 
            onda += chr(128)
        
        dom= np.array(range(cant_puntos))
        
        #grafica la señal enviada
        onda_plot=np.sin(dom)*127+128
        plt.figure(1)
        plt.plot(dom,onda_plot)
        plt.xlabel('Frame')
        plt.ylabel('Intensidad')
        
        #ejecuta la señal
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
        
    def Cte(amp_cte,dur_cte):  #Señal constante de voltaje amp_cte y duracion dur_cte, asumiendo que la placa entrega de 0V a 5V
        
        if amp_cte <=5:
            cant_puntos = int(BITRATE * dur_cte)
            silencios = cant_puntos % BITRATE
            amp_bit= amp_cte*256/5 #convierte de volts a bits
            señal_cte=np.zeros(cant_puntos)+amp_bit
            
            #Llenamos lo que falta de duracion con silencios
            señal_cte= np.append(señal_cte, np.zeros(silencios))
            
            señal_cte=señal_cte.astype(np.float32).tostring()
            
            
            
        
            p = pa()
            stream = p.open(
                       format=p.get_format_from_width(1),
                       channels=1,
                       rate=BITRATE,
                       output=True,
                       )
            stream.write(señal_cte)
            stream.stop_stream()
            stream.close()
            p.terminate()
        else:
            return ('El voltaje debe ser menor a 5V')
        
        
        
        #------------Medicion-------------------------------------
        
        
#        FORMAT = pyaudio.paInt16
#CHANNELS = 2
#RATE = 44100
#CHUNK = 1024
#RECORD_SECONDS = 5
#WAVE_OUTPUT_FILENAME = "file.wav"
# 
#audio = pyaudio.PyAudio()
# 
## start Recording
#stream = audio.open(format=FORMAT, channels=CHANNELS,
#                rate=RATE, input=True,
#                frames_per_buffer=CHUNK)
#print "recording..."
#frames = []
# 
#for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#    data = stream.read(CHUNK)
#    frames.append(data)
#print "finished recording"
# 
# 
## stop Recording
#stream.stop_stream()
#stream.close()
#audio.terminate()
# 
#waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#waveFile.setnchannels(CHANNELS)
#waveFile.setsampwidth(audio.get_sample_size(FORMAT))
#waveFile.setframerate(RATE)
#waveFile.writeframes(b''.join(frames))
#waveFile.close()
        
        #LA IDEA ES MODIFICAR ESO PARA OBTENER UN ARRAY PLOTEABLE COMO RESULTADO. LA PARTE DEL WAV SE PUEDE SALTEAR
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    