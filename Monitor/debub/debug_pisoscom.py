# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 22:01:01 2022

@author: user
"""
import pandas as pd
import numpy as np


def debug_dataset(df_pisoscom):
    
    '''
    Función que recibe como entrada el dataset en bruto y lo devuelve depurado
    '''
    # Se quitan los duplicados
    df_pisoscom = df_pisoscom.drop_duplicates(df_pisoscom.columns[df_pisoscom.columns.isin([6])])
    df_pisoscom = df_pisoscom.drop_duplicates(df_pisoscom.columns[df_pisoscom.columns.isin([8,9])])
    
    # Seleccion registros para el informe
    df_pisoscom = registros_informe(df_pisoscom)
        
    # Se corrigen los NA
    df_pisoscom = df_pisoscom.replace({None: "BLANCO33"})

    # Se insertan celdas en superficie construida
    df_pisoscom = insert_to(df_pisoscom, sep = 'Superficie construida', col = 4)
    
    # Se insertan celdas en superficie útil
    df_pisoscom = insert_to(df_pisoscom, sep = 'Superficie útil', col = 6)
    
    df_pisoscom = df_pisoscom.drop([7], axis=1)
    columns_names = list(range(0,df_pisoscom.shape[1]))
    df_pisoscom.columns = columns_names
    
    # Se insertan celdas en habitaciones
    df_pisoscom = insert_to2(df_pisoscom, sep = 'Habitaciones', col = 7)
            
    # Se insertan celdas en baños
    df_pisoscom = insert_to2(df_pisoscom, sep = 'Baño', col = 8)   
    
    # Se insertan celdas en Planta
    df_pisoscom = insert_to2(df_pisoscom, sep = 'Planta', col = 9) 
           
    # Se eliminan las variables que no son necesarias para el informe
    df_pisoscom = df_pisoscom.iloc[:,[0,1,2,3,4,6,7,8,9]] 
    
    # Se elimina el caracter €
    df_pisoscom[2]= df_pisoscom[2].str.replace('.', '', regex=True)
    df_pisoscom = extrae_valor(df_pisoscom, sep = ' €', col = 2, drop = 1, n_col = [2])
  
    # Se separa la columna Superficie construida   
    df_pisoscom = extrae_superficie(df_pisoscom, sep = ' : ', sep2 = ' m²', col = 4, drop = 0, col2 = 1)
    
    # Se separa la columna Superficie útil
    df_pisoscom = extrae_superficie(df_pisoscom, sep = ' : ', sep2 = ' m²', col = 6, drop = 0, col2 = 1)   
    
    # Se separa la columna Habitaciones   
    df_pisoscom = extrae_valor(df_pisoscom, sep = ' : ', col = 7, drop = 0, n_col = [7])
    
    # Se separa la columna Baños
    df_pisoscom = extrae_valor(df_pisoscom, sep = ' : ', col = 8, drop = 0, n_col = [8])
    
    # Se separa la columna Planta
    df_pisoscom = extrae_valor(df_pisoscom, sep = ' : ', col = 9, drop = 0, n_col = [9])
              
    # Se separa la columna dirección
    df_pisoscom = extrae_valor(df_pisoscom, sep = ' en ', col = 3, drop = 1, n_col = [10,3])
    
    # Se ordena el dataframe   
    df_pisoscom = df_pisoscom[[0,1,2,3,4,6,7,8,9,10]]
    
    # Se añade la columna zona
    df_pisoscom.insert(4, 4, '', True) 
    
    columns_names = list(range(0,df_pisoscom.shape[1]))
    df_pisoscom.columns = columns_names
    
    # Se separa las direcciones de las zonas
    df_pisoscom = extrae_valor(df_pisoscom, sep = ', cerca de ', col = 3, drop = 1, n_col = [3])
      
    df_pisoscom = df_pisoscom.reindex(columns=range(0, 11, 1))
    
    df_pisoscom = direcciones(df_pisoscom)
       
    return df_pisoscom   
    
    
def registros_informe(df):

    '''
    Selección registros para el informe
    '''
    
    df = df.drop(['Unnamed: 0'], axis=1)
    df = df.iloc[:,[0,1,2,8,9]]    
    # Se eliminan los anuncios sin renta, y las casas 
    df = df[df[2] != 'A consultar']
    df = df[df[8].str.contains('Casa')==False]
    df = df[df[8].str.contains('Chalet')==False]
    
    # Separo la columna con las caracteristicas
    df_9 = df[9].str.split('  ', expand=True)
    df = df.drop([9], axis=1)
    df = pd.concat([df, df_9], axis=1)
    columns_names = list(range(0,df.shape[1]))
    df.columns = columns_names
    
    return df


def insert_to(df, sep, col):

    '''
    Insertamos celdas en superficie
    '''

    df_Y =df[df[col].str.contains(sep)]
    df_N =df[df[col].str.contains(sep)==False]

    df_N.insert(col, col, '', True)
    df_N.insert(col, col, '', True)
    columns_names = list(range(0,df_N.shape[1]))
    df_N.columns = columns_names
    df_N = df_N.drop(df_N.shape[1]-1, axis=1) 
    df_N = df_N.drop(df_N.shape[1]-1, axis=1)
    
    df = pd.concat([df_Y, df_N])
    
    return df
    
  
def insert_to2(df, sep, col):

    '''
    Insertamos celdas en columnas de interés
    '''

    df_Y =df[df[col].str.contains(sep)]
    df_N =df[df[col].str.contains(sep)==False]

    df_N.insert(col, col, '', True)
    columns_names = list(range(0,df_N.shape[1]))
    df_N.columns = columns_names
    df_N = df_N.drop(df_N.shape[1]-1, axis=1) 
            
    df = pd.concat([df_Y, df_N])
    
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
   
    
def extrae_superficie(df, sep, sep2, col, drop, col2):
    
    '''
    Extrae la superficie de la columna separando el por caracter
    '''

    df_aux= df[col].str.split(sep, expand=True)
    df_aux= df_aux.drop([0], axis=1)
    df_aux= df_aux[col2].str.split(sep2, expand=True)
    df_aux= df_aux.drop([col2], axis=1)
    df = df.drop([col], axis=1)
    df_aux.columns = [col]
    df = pd.concat([df, df_aux], axis=1)

    return df


def direcciones(df):
    
    '''
    Separamos las direcciones de las zonas
    '''
    
    df_Av =df[df[3].str.contains('Avenida ')]
    df_Avg =df[df[3].str.contains('Avinguda ')]
    df_Calle =df[df[3].str.contains('Calle ')]
    df_Carrer =df[df[3].str.contains('Carrer ')]
    df_Cno =df[df[3].str.contains('Camino ')]
    df_Cmi =df[df[3].str.contains('Camí ')]
    df_Pz =df[df[3].str.contains('Plaza ')]
    df_Pc =df[df[3].str.contains('Plaça ')]
    
    df_Y = pd.concat([df_Av, df_Avg, df_Calle, df_Carrer, df_Cno, df_Cmi, df_Pz, df_Pc])
    
    index_pisoscom_Y = list(df_Y.index.values)
    df_N = df.drop(index_pisoscom_Y, axis=0)
    df_N = df_N[[0,1,2,4,3,5,6,7,8,9,10]]
    columns_names = list(range(0,df_N.shape[1]))
    df_N.columns = columns_names    

    df = pd.concat([df_Y, df_N])
    
    df = df.sort_index()    
    
    return df
    
