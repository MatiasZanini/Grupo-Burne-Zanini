#importamos módulo para comunicarnos con la placa
import clase_voltaje.py

#%% Generamos una señal (modo callback)

señal = armonica(100,120) #esto lo elegimos según la señal que querramos emitir

def callback_emision(in_data, frame_count, time_info, status):  #stream_callback pide una función de 4 argumentos.
		data = señal.readframes(frame_count) #pedazo de señal
		return (data, pyaudio.paContinue)        
        
        