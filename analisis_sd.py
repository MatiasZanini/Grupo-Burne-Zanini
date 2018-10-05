# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 11:56:48 2018

@author: Matías
"""
import matplotlib.pyplot as plt
import numpy as np
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
# ------------------------------Curva IV diodo--------------------------------
path = r'C:\Users\Matías\Desktop\Matías\Instrumentacion\mediciones 3-10/'
t, entrada, canal1, canal2 = np.loadtxt(path+'medicion_diodo_700.txt', delimiter = ',', unpack =True)







