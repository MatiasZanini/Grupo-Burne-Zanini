# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 17:15:27 2018

@author: Mati
"""

#%%

#Importamos las librerías y seteamos el rate.

import numpy as np
#import matplotlib.pyplot as plt
import pyaudio
from pyaudio import PyAudio as pa
import math
import wave 
import time

BITRATE=44100

#%%
   #---------------Emision--------------------------

    

def armonica(freq_arm,dur_arm):  #Señal armonica de amplitud 256 bits (suponemos 5V), frecuencia freq_arm, duracion dur_arm.

    onda=''
    cant_puntos = int(BITRATE * dur_arm)
    silencios = cant_puntos % BITRATE
    
    for x in range(cant_puntos):
        onda += chr(int(math.sin(x / ((BITRATE / freq_arm) / math.pi)) * 126/2 + 128/2))
        
    #Llenamos lo que falta de duracion con silencios
    for x in range(silencios): 
        onda += chr(128)
    
    #dom= np.array(range(cant_puntos))
    
    #grafica la señal enviada
    #        onda_plot=np.sin(dom)*127+128
    #        plt.figure(1)
    #        plt.plot(dom,onda_plot)
    #        plt.xlabel('Frame')
    #        plt.ylabel('Intensidad')

#ejecuta la señal
    
def emitir(onda,bitrate,callback=None):    
    
            
    p = pa()
    if callback:
        stream = p.open(
        format=p.get_format_from_width(1),
        channels=1,
        rate=BITRATE,
        output=True,
        stream_callback=callback)
        stream.start_stream()

        # wait for stream to finish (5)
        while stream.is_active():
            time.sleep(0.1)
        
        # stop stream (6)
        stream.stop_stream()
        stream.close()
        
        
        # close PyAudio (7)
        p.terminate()

    else:
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
    
        
        
#def Cte(amp_cte,dur_cte):  #Señal constante de voltaje amp_cte y duracion dur_cte, asumiendo que la placa entrega de 0V a 5V
#    
#    if amp_cte <=1.20:
#        cant_puntos = int(BITRATE * dur_cte)
#        silencios = cant_puntos % BITRATE
#        amp_bit= amp_cte*256/1.20 #convierte de volts a bits
#        señal_cte_lista=list(np.zeros(cant_puntos)+amp_bit)
#        
#        señal_cte=''
#        
#        for x in range(cant_puntos):
#            señal_cte += chr(int(señal_cte_lista[x]))
#            
#        for x in range(silencios):
#            señal_cte += chr(128)
##            
##            #Llenamos lo que falta de duracion con silencios
##            señal_cte= np.append(señal_cte, np.zeros(silencios))
##            
##            señal_cte=señal_cte.astype(np.float32).tostring()
        
        
#            
        
        
#    
#        p = pa()
#        stream = p.open(
#                   format=p.get_format_from_width(1),
#                   channels=1,
#                   rate=BITRATE,
#                   output=True,
#                   )
#        stream.write(señal_cte)
#        stream.stop_stream()
#        stream.close()
#        p.terminate()
#    else:
#        return ('El voltaje debe ser menor a 1.20V')
    
    
    
    #------------Medicion-------------------------------------
    
def medir(dur_med):        #Devuelve un array con una medicion de voltaje de duracion dur_med.
    FORMAT = pyaudio.paInt16
    CHANNELS = 1   #creo que si ponemos 2 es estereo
    #RATE = 44100
    CHUNK = 1024          #Espacio que ocupa un bloque de datos del buffer. La señal se divide en estos "chunks".
    #RECORD_SECONDS = 5
    nombre_arch = 'arch.wav'
 
    p = pa()
 
# Empieza a grabar
    stream = p.open(format=FORMAT, channels=CHANNELS,
            rate=BITRATE, input=True,
            frames_per_buffer=CHUNK)
    print('grabando...')
    frames = []
 
    for i in range(0, int(BITRATE / CHUNK * dur_med)):
        data = stream.read(CHUNK)
    frames.append(data)
    print('finalizando grabación...')
    
    
# Termina de grabar
    stream.stop_stream()
    stream.close()
    p.terminate()
 
#Crea un archivo temporal .wav para poder recuperarlo como array mas tarde.
    waveFile = wave.open(nombre_arch, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(p.get_sample_size(FORMAT))
    waveFile.setframerate(BITRATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    
    arch_temp = wave.open('arch.wav','r')

#Extrae un array de la señal wav
    señal = arch_temp.readframes(-1)
    señal = np.fromstring(señal, 'Int16')

    return señal

##If Stereo
#if spf.getnchannels() == 2:       ---------esta sentencia impide ingresar dos canales. Chequear si es necesaria------
#    print 'Just mono files'
#    sys.exit(0)

#        plt.figure(1)
#        plt.title('Signal Wave...')  -------El ploteo prefiero dejarlo fuera de la clase-------
#        plt.plot(señal)
#        plt.show()
#        
        
    #----------------------------------------------COMENTARIO IMPORTANTE----------------------------------------------
    
    #queda chequear que este midiendo bien con el microfono y/o el cable del labo. Hay que ver si mide en bits (de 0 a 255), en cuyo
    #caso agregar la siguiente linea:    señal=señal*5/255   (suponiendo que la placa entrega de 0 a 5V)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    