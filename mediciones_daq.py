# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 17:59:15 2018

@author: Publico
"""
import numpy as np
import funciones_daq as fdaq
import matplotlib.pyplot as plt
from importlib import reload

#%%
reload(fdaq)

#%%
#---------------------Medir conjuncion de los chunks------------------------------
#
#i=fdaq.medir_volt_anal()
#f=fdaq.medir_volt_anal()
#
#while i-f<0:
#    i=fdaq.medir_volt_anal()
#    f=fdaq.medir_volt_anal()
#    
signal=fdaq.medir_senal_anal(200,1000)
frec_rampa = 10/1000 #frecuencia en Hz de la rampa enviada con el generador
#
#f = np.array([1000])
#len_f = len(f)
#signal = []
#for n in range(len_f):
#    signal.append(str(f[n]))    
#    signal.append(fdaq.medir_senal_anal(2, f[n]))
##    freq = 'frecuencia='+str(f[n])
##    signal.append(freq+data)
#
#signal_ = np.asarray(signal).T

signal_ = np.asarray(signal)
np.savetxt('barrido_frec_rampa{}.txt'.format(frec_rampa), signal_, delimiter = ';')




