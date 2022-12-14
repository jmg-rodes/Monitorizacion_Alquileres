# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 21:57:03 2022

@author: user
"""
import pandas as pd
import numpy as np


def debug_dataset(df_fotocasa):    
    
    '''
    Función que recibe como entrada el dataset en bruto y lo devuelve depurado
    '''
    # Se quitan los duplicados
    #df_fotocasa = df_fotocasa.drop_duplicates(df_fotocasa.columns[~df_fotocasa.columns.isin([0])])
    df_fotocasa = df_fotocasa.drop_duplicates(df_fotocasa.columns[df_fotocasa.columns.isin([7])])
    df_fotocasa = df_fotocasa.drop_duplicates(df_fotocasa.columns[df_fotocasa.columns.isin([8,9,11,13])])

    # Seleccion registros para el informe
    df_fotocasa = registros_informe(df_fotocasa)
    
    columns_names = df_fotocasa.columns.values
    columns_names = list(columns_names)

    # Insertamos celdas en WWW    
    df_fotocasa = insert_www(df_fotocasa, columns_names)
    
    # Se corrigen los NA
    df_fotocasa = df_fotocasa.replace({None: "BLANCO33"})

    # Se ordenan las columnas
    df_fotocasa = orden_col(df_fotocasa, columns_names)
           
    # Se elimina el caracter "." y "€"
    df_fotocasa[2]= df_fotocasa[2].str.replace('.', '', regex=True)
    df_fotocasa = extrae_valor(df_fotocasa, sep = ' €', col = 2, drop = 1, n_col = [2])

    # Se seleccionan las variables que se necesitan para el informe
    df_fotocasa = df_fotocasa.iloc[:,[0,1,16,7,12,8,10,14]]
    
    # Separo la columna dirección
    df_fotocasa = extrae_direccion(df_fotocasa, columns_names)   
    columns_names = list(range(0,df_fotocasa.shape[1]))
    df_fotocasa.columns = columns_names
     
    # Corregimos los NA
    df_fotocasa = correc_na(df_fotocasa, columns_names)
   
    return df_fotocasa
    
        
def registros_informe(df):
    
    '''
    Selección registros para el informe
    '''
    
    df = df.drop(['Unnamed: 0'], axis=1)
    
    # Quito los anuncios sin renta
    df =df[df[2] != 'A consultar']
    df =df[df[8].str.contains('Casa')==False]

    # Me quedo con las variables necesarias para el informe
    df = df.iloc[:,[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]]
    
    return df

    
def insert_www(df, columns_names):
    
    '''
    Insertamos celdas en WWW
    '''
    
    df_Y =df[df[7].str.contains('https')]
    df_N =df[df[7].str.contains('https')==False]

    try:
        df_N.insert(6, 6, '', True) 
        df_N = df_N.drop(16, axis=1)
        df_N.columns = columns_names
    
        df = pd.concat([df_Y, df_N])
    except:
        print("No hay ningún registro sin https")
    
    return df
  
def orden_col(df, columns_names):
    
    '''
    Ordenación de las columnas 
    '''
    
    var = ['hab','baño','m²','Planta']
    n=10
    i=10
    for i in range(10,17,2):
        df_Y =df[df[i].str.contains(var[i-n])]
        df_N =df[df[i].str.contains(var[i-n])==False]
        df_N.insert(i-1, 'c', '', True)
        df_N.insert(i-1, 'c', '', True) 
        df_N = df_N.drop([15,16], axis=1)
        df_N.columns = columns_names
        df = pd.concat([df_Y, df_N])
        n+=1
    
    return df

def extrae_valor(df, sep, col, drop, n_col):
    
    '''
    Extrae el valor deseado de la columna separando por caracter
    '''
    
    df_aux= df[col].str.split(sep, expand=True)
    df_aux= df_aux.drop([drop], axis=1)
    df = df.drop([col], axis=1)
    df_aux.columns = np.array(n_col)
    df = pd.concat([df, df_aux], axis=1)
    
    return df

def extrae_direccion(df, columns_names):
    
    '''
    Extrae la dirección de la columna
    '''
    
    # Separo la columna dirección
    df_8= df[8].str.split(' en ', expand=True)
    df_9 = df_8.iloc[:,[0]]
    df_9= df_9[0].str.split(' de ', expand=True)
    df_9 = df_9.iloc[:,[0]]
    df_9.columns = [10]
    df_8= df_8[1].str.split(', ', expand=True)
           
    # Direccones con número de portal
    df_8[2] = df_8[2].replace({None: "BLANCO33"})
    df_Y = df_8[df_8[2].str.contains("BLANCO33")]
    df_N = df_8[df_8[2].str.contains("BLANCO33")==False]
    df_N.iloc[:,0] = df_N.iloc[:,0] +', '+df_N.iloc[:,1]
    df_N = df_N.iloc[:,[0,2]]
    df_N.columns = [0,1]
    df_Y = df_Y.iloc[:,[0,1]]
    
    df_8 = pd.concat([df_Y, df_N])
    df_8.columns = [4,5]
    
    
    df = df.drop([8], axis=1)
    df = pd.concat([df, df_8, df_9], axis=1)
    df = df[[0,1,2,4,5,13,9,11,15,10]]
    df.insert(5, 5, '', True) 
    
    return df

def correc_na(df, columns_names):
    
    '''
    Se renombran todos los valores vacios
    '''
    
    df[4] = df[4].replace({None: "BLANCO33"})
    df_Y = df[df[4]=="BLANCO33"]
    df_N = df[df[4]!="BLANCO33"]
    df_Y = df_Y[[0,1,2,4,3,5,6,7,8,9,10]]
    
    columns_names = list(range(0,df.shape[1]))
    df_Y.columns = columns_names
    df_Y[3]=None
        
    df = pd.concat([df_Y, df_N])
    
    df[4] = df[4].replace({None: "BLANCO33"})
    df = df[df[4]!='BLANCO33']
    df = df.sort_index() 
    
    return df
    
    