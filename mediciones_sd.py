import numpy as np
import matplotlib.pyplot as plt
import time
import voltaje_sd as volt
#%% emitir armonica y medir
frecuencia = 5000  # frecuencia del tono que se desea emitir
duracion = 1       # duracion del tono
amplitud = 0.5

tiempo, data, grabacion = volt.playrec_tone(frecuencia,duracion,amplitud)                # datos contiene los arrays concatenados de tiempo, data, grabacion

with open("resultados_frecuencia=" + str(frecuencia) + ".txt", "w") as out_file:     # abre un archivo .txt, str(imprime el valor de la frecuencia)
    for i in range(len(tiempo)):                                           # tiempo, data y grabacion tienen las mismas dimensiones, un for para leer todo el array
        out_string = ""                                                    # string vacio
        out_string += str(tiempo[i])                                       # escribimos los valores de tiempo,data y grabacion
        out_string += "," + str(data[i])
        out_string += "," + str(grabacion[i])
        out_string += "\n"
        out_file.write(out_string)                                         # escribe el string en el archivo de salida
#%%
#Respuesta en frecuencia de la placa de audio.
amp, dur = 0.5, 5    
freqs=np.concatenate(np.arange(0,105,5) , np.linspace(105, 20000, 10) , np.linspace(20000,44100,30))
Nfreq=len(freqs)

amplitudes = np.empty(Nfreq)
for i in range(Nfreq):
    amplitudes[i] = np.max(volt.playrec_tone(freqs[i],dur,amp,ch_in=1,ch_out=1,block)[2])
    time.sleep(0.5)
#comentario: en vez de un sleep podriamos hacer algun tipo de lazo de control
# que solo continue iterando una vez finalizada la iteracion anterior
# este lazo iria en playrec_tone, como indicador de finalizacion de medicion

plt.plot(freqs, amplitudes)

#%% prueba de lectura de argumentos
#def suma(a,b,c=3,d=5):
#    return a+b+c+d
#
#S = suma(1,1,d=1)
#print(S)