# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 20:39:52 2022

@author: user
"""
#import json
import kml2geojson
import pandas as pd
archivo = 'Alicante coord boton.kml'
D_g = kml2geojson.main.convert('./Geolocalizacion/'+archivo, './Geolocalizacion')


#D_google = json.loads(Direcciones_google[0])

def area_google(D_g):

    z = []
    
    coordenadas = pd.DataFrame()
    
    D = D_g[0]
    
    '''
    D.items()
    D.keys()
    D['features']
    '''
    
    l = len(D['features'])
    
    for i in range(l):
        
        #Id.append(int(D['features'][i]['properties']['id_2']))
        z.append(D['features'][i]['geometry']['coordinates'])
        #y.append(D['features'][i]['geometry']['coordinates'][1])
    
    
    #coordenadas['id'] = Id
    coordenadas['z'] = z
    #coordenadas['y'] = y
    
    #coordenadas.to_excel('./Geolocalizacion/coordenadas '+anyo+trim+'.xlsx', header=True, index=False, encoding='utf-8-sig')
    coordenadas.to_excel('./Geolocalizacion/coordenadas_alicante.xlsx', header=True, index=False, encoding='utf-8-sig')

area_google(D_g)

def coord_google(D_g):

    Id = []
    x = []
    y = []
    
    coordenadas = pd.DataFrame()
    
    D = D_g[0]
    
    '''
    D.items()
    D.keys()
    D['features']
    '''
    
    l = len(D['features'])
    
    for i in range(l):
        
        #Id.append(int(D['features'][i]['properties']['id_2']))
        x.append(D['features'][i]['geometry']['coordinates'][0])
        y.append(D['features'][i]['geometry']['coordinates'][1])
    
    
    coordenadas['id'] = Id
    coordenadas['x'] = x
    coordenadas['y'] = y
    
    #coordenadas.to_excel('./Geolocalizacion/coordenadas '+anyo+trim+'.xlsx', header=True, index=False, encoding='utf-8-sig')
    coordenadas.to_excel('./Geolocalizacion/coordenadas_alicante.xlsx', header=True, index=False, encoding='utf-8-sig')

coord_google(D_g)
