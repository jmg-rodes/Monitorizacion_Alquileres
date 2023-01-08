# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 20:35:50 2023

@author: user
"""

import pandas as pd
import numpy as np


def debug_dataset(df):    
    
    '''
    Función que recibe como entrada el dataset en bruto y lo devuelve depurado
    '''
    # Se quitan los duplicados
    #df = df.drop_duplicates(df.columns[~df.columns.isin([0])])
    df = df.drop_duplicates(df.columns[df.columns.isin([3])])
    df = df.drop_duplicates(df.columns[df.columns.isin([4,7,9,11,12,13,14,15,16,17])])

       
    # Seleccion registros para el informe
    df = registros_informe(df)
    
    columns_names = df.columns.values
    columns_names = list(columns_names)

    # Insertamos celdas en WWW    
    df = insert_www(df, columns_names)
    
    # Se corrigen los NA
    df = df.replace({None: "BLANCO33"})

    # Se insertan celdas
    df = insert_to(df, sep = 'm²', col = 6)
    df = insert_to2(df, sep = 'm²', col = 7)
    df = insert_to3(df, sep = 'hab.', col = 10)
    df = insert_to4(df, sep = 'Características básicas', col = 11, c=6)
    df = insert_to4(df, sep = 'Características básicas', col = 12, c=5)
    df = insert_to4(df, sep = 'Características básicas', col = 13, c=4)
    df = insert_to4(df, sep = 'Características básicas', col = 14, c=3)
    df = insert_to4(df, sep = 'Características básicas', col = 15, c=2)
    df = insert_to5(df, sep = 'Características básicas', col = 16)
    
    # Se separa la columna caracteristias
    df = extrae_valor(df, sep = ', ', col = 18, drop = 0, n_col = [18])
    df = extrae_valor(df, sep = ' m²', col = 18, drop = 1, n_col = ['18'])
    
    # Se seleccionan las variables que se necesitan para el informe
    df = df.iloc[:,[0,1,2,4,7,20,9,19,11]]
    
    # Se ordena el dataframe   
    #df = df[[0,1,2,3,4,6,7,8,9,10]]
    
    # Separo la columna dirección
    df = extrae_direccion(df)   
    columns_names = list(range(0,df.shape[1]))
    df.columns = columns_names
        
    df = direcciones(df)
    
    # Se separa la columna baños
    df = extrae_valor(df, sep = ' ', col = 8, drop = 1, n_col = [8])
    
    # Se ordena el dataframe   
    df = df[[0,1,2,3,4,6,7,8,9,10]]
   
    return df
    
        
def registros_informe(df):
    
    '''
    Selección registros para el informe
    '''
    
    df = df.drop(['Unnamed: 0'], axis=1)
    
    # Quito los anuncios sin renta
    #df =df[df[2] != 'A consultar']
    df =df[df[4].str.contains('Casa')==False]
    df =df[df[4].str.contains('Chalet')==False]

    # Me quedo con las variables necesarias para el informe
    df = df.iloc[:,[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]]
    
    return df

    
def insert_www(df, columns_names):
    
    '''
    Insertamos celdas en WWW
    '''
    
    df_Y =df[df[3].str.contains('https')]
    df_N =df[df[3].str.contains('https')==False]

    try:
        df_N.insert(2, 2, '', True) 
        df_N = df_N.drop(18, axis=1)
        df_N.columns = columns_names
    
        df = pd.concat([df_Y, df_N])
    except:
        df("No hay ningún registro sin https")
    
    return df
  

def insert_to(df, sep, col):

    '''
    Insertamos celdas en m²
    '''

    df_N =df[df[col]==sep]
    df_Y =df[df[col]!=sep]

    df_N.insert(col-1, col-1, '', True)
    df_N.insert(col-1, col-1, '', True)
        
    columns_names = list(range(0,df_N.shape[1]))
    df_N.columns = columns_names
    df_N = df_N.drop(df_N.shape[1]-1, axis=1) 
    df_N = df_N.drop(df_N.shape[1]-1, axis=1)
    
    df = pd.concat([df_Y, df_N])
    
    return df

def insert_to2(df, sep, col):

    '''
    Insertamos celdas en m²
    '''

    df_N =df[df[col]==sep]
    df_Y =df[df[col]!=sep]

    df_N.insert(col-2, col-2, '', True)
            
    columns_names = list(range(0,df_N.shape[1]))
    df_N.columns = columns_names
    df_N = df_N.drop(df_N.shape[1]-1, axis=1) 
        
    df = pd.concat([df_Y, df_N])
    
    return df

def insert_to3(df, sep, col):

    '''
    Insertamos celdas en m²
    '''

    df_Y =df[df[col]==sep]
    df_N =df[df[col]!=sep]

    df_N.insert(col-1, col-1, '', True)
    df_N.insert(col-1, col-1, '', True)
        
    columns_names = list(range(0,df_N.shape[1]))
    df_N.columns = columns_names
    df_N = df_N.drop(df_N.shape[1]-1, axis=1) 
    df_N = df_N.drop(df_N.shape[1]-1, axis=1)
    
    df = pd.concat([df_Y, df_N])
    
    return df

def insert_to4(df, sep, col, c):

    '''
    Insertamos celdas 
    '''

    df_N =df[df[col]==sep]
    df_Y =df[df[col]!=sep]

    for i in range(c-1):
        df_N.insert(col, col, '', True)
    
        
    columns_names = list(range(0,df_N.shape[1]))
    df_N.columns = columns_names
    
    for i in range(c-1):
        df_N = df_N.drop(df_N.shape[1]-1, axis=1) 
    
    
    df = pd.concat([df_Y, df_N])
    
    return df

def insert_to5(df, sep, col):

    '''
    Insertamos celdas 
    '''

    df_N =df[df[col]==sep]
    df_Y =df[df[col]!=sep]

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

def extrae_direccion(df):
    
    '''
    Extrae la dirección de la columna
    '''
    
    # Separo la columna dirección
    df_8= df[4].str.split(' en ', expand=True)
    df_9 = df_8.iloc[:,[0]]
    df_9= df_9[0].str.split(' de ', expand=True)
    df_9 = df_9.iloc[:,[1]]
    df_9.columns = [10]
    df_8= df_8[[1]]
    df_8.columns = [4]       
        
    df = df.drop([4], axis=1)
    df = pd.concat([df, df_8, df_9], axis=1)
    df = df[[0,1,2,4,7,'18',9,20,11,10]]
    #df.insert(5, 5, '', True) 
    
    return df


def direcciones(df):
    
    '''
    Separamos las direcciones de las zonas
    '''
    
    df_Av =df[df[3].str.contains('avenida ')]
    df_Avg =df[df[3].str.contains('avinguda ')]
    df_Calle =df[df[3].str.contains('calle ')]
    df_Carrer =df[df[3].str.contains('carrer ')]
    df_Cno =df[df[3].str.contains('camino ')]
    df_Cmi =df[df[3].str.contains('camí ')]
    df_Pz =df[df[3].str.contains('plaza ')]
    df_Pc =df[df[3].str.contains('plaça ')]
    df_Gl =df[df[3].str.contains('glorieta ')]
    df_C =df[df[3].str.contains('C/')]
    
    df_Y = pd.concat([df_Av, df_Avg, df_Calle, df_Carrer, df_Cno, df_Cmi, df_Pz, df_Pc, df_Gl, df_C])
    df_Y.insert(4, 4, '', True)
    columns_names = list(range(0,df_Y.shape[1]))
    df_Y.columns = columns_names
    
    index_idealista_Y = list(df_Y.index.values)
    df_N = df.drop(index_idealista_Y, axis=0)
    df_N.insert(3, 3, '', True)
    columns_names = list(range(0,df_N.shape[1]))
    df_N.columns = columns_names

    df = pd.concat([df_Y, df_N])
    
    df = df.sort_index()    
    
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
    
