# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 12:18:58 2019

@author: jomaga
"""
import pandas as pd
import numpy as np

# GEOLOCALIZACION DIRECCIONES

def geolocalizacion(Direcciones_dataframe):
    
    '''
    Basado en el seudo código: https:www
    '''
    
    #Direcciones_dataframe = pd.read_excel("./Geolocalizacion/Direcciones.xlsx")
    Barrios_dataframe = pd.read_excel("./Geolocalizacion/Barrios.xlsx")
    pd.options.display.max_rows = 10
    
    Direcciones_dataframe['Zona'] = 0
    
    D = Barrios_dataframe.iat[(len(Barrios_dataframe)-1), 2]
    
    result = np.zeros((len(Direcciones_dataframe), D)) # matriz de ceros
    
    for s in range(len(Direcciones_dataframe)): # desde 0 hasta 540
        print('Dirección =', s+1)
        x = Direcciones_dataframe[Direcciones_dataframe['id'] == s+1]
        for t in range(D): # desde 0 hasta nº de zonas
            p = Barrios_dataframe[Barrios_dataframe['Zona'] == t+1]
            if len(p) > 0:
                i = 0
                j = len(p)-1
                dentro = 0
                for i in range(len(p)): # desde 0 hasta el tamaño de la Zona i
                    
                    if (((p.iat[i,4] < x.iat[0,2]) and (p.iat[j,4] >= x.iat[0,2] )) or ((p.iat[j,4] < x.iat[0,2]) and (p.iat[i,4] >= x.iat[0,2]))):
                       A1 = float(p.iat[i,3])
                       A2 = float(x.iat[0,2] - p.iat[i,4])
                       A3 = float(p.iat[j,3] - p.iat[i,3]) 
                       A4 = float(p.iat[j,4] - p.iat[i,4])
                       AA = A1 + (A2 * A3) / A4 
    
                       if (AA < x.iat[0,1]):
                           dentro = 1 - dentro
                      
                    j = i
                
                result[s,t] = dentro
                if result[s,t]==1:
                    Direcciones_dataframe.iat[s,3] = t+1

    return Direcciones_dataframe


