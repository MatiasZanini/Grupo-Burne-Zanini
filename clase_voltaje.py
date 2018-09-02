#Importamos las librerías

import numpy as np
import matplotlib.pyplot as plt
import pyaudio
from pyaudio import PyAudio as pa
import math
import wave 
import time
from scipy import signal

#%% Seteamos el rate

BITRATE=44100

#%% Creamos funciones para comunicarnos con la placa de audio


   #---------------Emision--------------------------

#---------------------------------------------------------------------------------------------------------------------------
#Tipos de ondas    

def armonica(freq_arm,dur_arm):  #Señal armonica de amplitud 256 bits (suponemos 1.2V), frecuencia freq_arm, duracion dur_arm.

    onda=''
    cant_puntos = int(BITRATE * dur_arm)
    silencios = cant_puntos % BITRATE
    
    for x in range(cant_puntos):
        onda += chr(int(math.sin(x / ((BITRATE / freq_arm) / math.pi)) * 126/2 + 128/2))
        
    #Llenamos lo que falta de duracion con silencios
    for x in range(silencios): 
        onda += chr(128)
    
    #test: grafica un pedazo de la señal enviada (si no hay que hacer mucho zoom para ver)
    t = np.arange(0,dur_arm/10**3,1/BITRATE)
    onda_plot=np.sin(t*freq_arm)*126/2+128/2
    plt.figure(1)
    plt.plot(t, onda_plot)
    plt.xlabel('Tiempo')
    plt.ylabel('Intensidad')
    plt.show()
    
# esto es igual pero en vez de graficar vs t grafica por cant de puntos    
#    #test: grafica un pedazo de la señal enviada (si no hay que hacer mucho zoom para ver)
#    #dom= np.array(range(cant_puntos/10**3))
#    onda_plot=np.sin(dom / ((BITRATE / freq_arm) / math.pi))*126/2+128/2
#    plt.figure(1)
#    plt.plot(dom, onda_plot)
#    plt.xlabel('Frame')
#    plt.ylabel('Intensidad')
#    plt.show()
#    
    return onda;
    



def cuadrada(amp, frec, dur):
    t = np.arange(0,dur,1/BITRATE)
   
    if amp <= 1.20:
        amp_bit= amp*256/1.20 #convierte de volts a bits
        cuadrada = amp_bit*signal.square(2 * np.pi * frec * t)
        for i in range(len(t)):
            if cuadrada[i] < 0:
                cuadrada[i] = 0
         
        cuadrada_lista = list(cuadrada)
        señal = ''
        for x in range(len(t)):
            señal += chr(int(cuadrada_lista[x]))

        #test: grafica un pedazo de la señal enviada
        t_plot = np.arange(0,dur/10**3,1/BITRATE)
        plt.figure(2)
        plt.plot(t_plot, cuadrada[:len(t_plot)])
        plt.xlabel('Tiempo')
        plt.ylabel('Intensidad')
        plt.show()
        
        return cuadrada;
    
    else:
        return ('El voltaje debe ser menor a 1.20V')


def sawtooth(amp, frec, dur):
    t = np.arange(0,dur,1/BITRATE)
   
    if amp <= 1.20:
        amp_bit= amp*256/1.20 #convierte de volts a bits
        sawtooth = (amp_bit/2)*(signal.sawtooth(2 * np.pi * frec * t) + 1) #si pongo 0.5 en el segundo arg de signal.sawtooth obtengo una triangular

         
        sawtooth_lista = list(sawtooth)
        señal = ''
        for x in range(len(t)):
            señal += chr(int(sawtooth_lista[x]))

        #test: grafica un pedazo de la señal enviada
        t_plot = np.arange(0,dur/10**3,1/BITRATE)
        plt.figure(2)
        plt.plot(t_plot, sawtooth[:len(t_plot)]*amp/amp_bit)
        plt.xlabel('Tiempo')
        plt.ylabel('Intensidad')
        plt.show()
        
        return sawtooth;
    
    else:
        return ('El voltaje debe ser menor a 1.20V')
  

#---------------------------------------------------------------------------------------------------------------------------
#Ejecución de la señal de emisión
    
def emitir(onda=None,bitrate,callback=None):    
              
    p = pa()
    if callback: #modo callback
        stream = p.open(
        format=p.get_format_from_width(1),
        channels=1,
        rate=BITRATE,
        output=True,
        stream_callback=callback)
        stream.start_stream()

        while stream.is_active():
            time.sleep(0.1)

    elif onda: #modo bloqueo
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
    
    
    
#---------------------------------------------------------------------------------------------------------------------------
    
    #------------Medicion-------------------------------------
    
def medir(dur_med, callback=None):        #Devuelve un array con una medicion de voltaje de duracion dur_med.
    FORMAT = pyaudio.paInt16
    CHANNELS = 1   #creo que si ponemos 2 es estereo
    CHUNK = 1024          #Espacio que ocupa un bloque de datos del buffer. La señal se divide en estos "chunks".
    nombre_arch = 'arch.wav'
    frames = []
 
    p = pa()
 
# Empieza a grabar
    
    if callback:
        stream = p.open(format=FORMAT, channels=CHANNELS,
        rate=BITRATE, input=True,
        frames_per_buffer=CHUNK, stream_callback=callback)
        stream.start_stream()
        
        while stream.is_active():
           time.sleep(0.1)
           print('grabando...')
           for i in range(0, int(BITRATE / CHUNK * dur_med)):
               data = stream.read(CHUNK)
           frames.append(data)
           print('finalizando grabación...')

#no se si esta bien implementada la funcion callback. está bien pedir el read??
    
    else: # modo bloqueo
        stream = p.open(format=FORMAT, channels=CHANNELS,
                rate=BITRATE, input=True,
                frames_per_buffer=CHUNK)
   
        print('grabando...')
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


#---------------------------------------------------------------------------------------------------------------------------

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
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    