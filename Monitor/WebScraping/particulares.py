# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 08:58:19 2021

@author: user
"""

from constant import *
from datetime import datetime
import pandas as pd

def anuncios_get(run):
    
    '''
    Se unen los anuncios de particulares en un dataframe
    '''
    
    requests = 0
       
    df_particulares = pd.DataFrame()
    
    # Portales para los que se realiza el webscraping
    for portal in portales:                
        # Establecemos la fecha
        today = datetime.today()
        fecha = today.strftime("%Y.%m.%d")            
        try:
            # Lectura xlsx del portal
            df_part = pd.read_excel('./ouput/particulares/' +portal+ '/anuncios_'+portal+'_particulares' +'_'+ str(run+1) +'_'+ fecha +'.xlsx')
            #df_part = df_part.drop(['Unnamed: 0'], axis=1)
            df_particulares = pd.concat([df_particulares, df_part])
            
        except:
            print('Hay {} anuncio de {}'.format(run, portal))
            
        # Monitor the requests
        requests += 1
        print('Request:{}; Portal: {}; Run: {}'.format(requests, portal, run+1 ))
    
       
    # Almacenaje de los anuncios de particulares
    df_particulares.columns = ['Anuncio', 'Fecha', 'Portal','Renta', 'Titular', 'Web', 'Dirección' ]
    pd.DataFrame(df_particulares).to_excel('../Resultados/Particulares/anuncios_particulares_' + fecha + '_' + str(run+1) +'.xlsx', encoding='utf-8-sig')
    
    print ('***** SE HAN REALIZADO {} VISITAS A LAS WEBS *****'.format(run+1))
