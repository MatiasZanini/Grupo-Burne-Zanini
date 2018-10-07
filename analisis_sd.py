# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 11:56:48 2018

@author: Matías
"""
import matplotlib.pyplot as plt
import numpy as np

#%%
#--------------------------------CALIBRACIÓN--------------------------------------------------------------------

t_cal, entrada_cal, canal1_cal, canal2_cal = np.loadtxt('medicion_calibracion_ch1_800.txt', delimiter = ',', unpack =True)

amp_ch1=np.max(canal1_cal) #amplitud medida en el canal 1

amp_medida=1.3 #voltaje medido por el osciloscopio 

factorconv=amp_medida/amp_ch1







#%%
#---------------------------------Barrido en frecuencia----------------------------



f, a = np.loadtxt('barrido_frec.txt', delimiter = ',', unpack =True)
f=f/1000
fzoom, azoom = np.loadtxt('barrido_frec2.txt', delimiter = ',', unpack =True)

plt.subplots(1,2, sharey=True)
plt.suptitle('Respuesta en frecuencia de la placa de audio')

g1 = plt.subplot(1,2,1)
plt.plot(f,a,linewidth=3)
plt.xlabel('Frecuencia (kHz)')
plt.ylabel('Amplitud')
plt.yticks(np.arange(0,0.45,0.05))
plt.grid(True)

plt.subplot(1,2,2, sharey=g1)
plt.plot(fzoom,azoom,linewidth=3)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud')
plt.xlim(xmin=0, xmax=3)
plt.grid(True)


#%%

#-------------------------------Señal cruda diodo--------------------------------------------

fs=20000
frecuencia=550
puntos_periodo = int(fs/frecuencia)

t, entrada, canal1, canal2 = np.loadtxt('medicion_diodo_550.txt', delimiter = ',', unpack =True)
plt.subplot(1,3,1)

plt.plot(t,canal1,'.')

plt.subplot(1,3,2)

plt.plot(t,canal2,'.')

plt.subplot(1,3,3)
plt.plot(t,entrada,'.')

#[0:puntos_periodo]




#%%
# ------------------------------Curva IV diodo--------------------------------
#path = r'C:\Users\Matías\Desktop\Matías\Instrumentacion\mediciones 3-10/'
t, entrada, canal1, canal2 = np.loadtxt('medicion_diodo_550.txt', delimiter = ',', unpack =True)
R2 = 900
fs=20000
frecuencia=550
Vdiodo=(canal1-canal2)*factorconv   #en volts
Idiodo=canal2/R2*factorconv*1000   #en miliamper

inicio_curva=(np.abs(Vdiodo - np.min(Vdiodo))).argmin()
fin_curva=(np.abs(Vdiodo -np.max(Vdiodo))).argmin()

#plt.plot(Vdiodo[inicio_curva:fin_curva], Idiodo[inicio_curva:fin_curva],'.')
plt.plot(Vdiodo, Idiodo,'.')
plt.tick_params(axis = 'both', which = 'both', length = 4, width = 2, labelsize = 20)

puntos_periodo = int(fs/frecuencia)
 
#plt.plot(Vdiodo[0:135*puntos_periodo], Idiodo[0:135*puntos_periodo],'.')
plt.xlabel('Voltaje (V)',size=20)
plt.ylabel('Corriente (mA)',size=20)
plt.grid(True)


Vdiodo2=Vdiodo[inicio_curva:fin_curva]
Idiodo2=Idiodo[inicio_curva:fin_curva]

Vf=np.max(Vdiodo2)

indicevf=(np.abs(Vdiodo2-Vf)).argmin()

If=Idiodo2[indicevf]

Pf=Vf*If*1000











