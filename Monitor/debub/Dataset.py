# -*- coding: utf-8 -*-
"""
Cre ated on Thu Nov 24 16:52:53 2022

@author: José Manuel García Rodes
"""
import debug_fotocasa as fotocasa_dep
import debug_pisoscom as pisoscom_dep
import debug_idealista as idealista_dep
from constant_debug import *
import Geolocalizacion.Geolocalizacion as geo
import pandas as pd
import numpy as np
import os
import glob
from datetime import datetime
from pyod.models.knn import KNN

import kml2geojson
# Llegados a este punto explicar las distintas opciones de geolocalización
from geopy.geocoders import Nominatim 
#from geopy.geocoders import GoogleV3 # ---> De pago 0,005 cts la dirección

# Se muestra el año y el trimestre del informe

print(f"Año: {anyo}. Trimestre: {trim}")

############ FUNCIONES ############

def unir_excel(anyo, trim, portal,  drop):
    
    '''
    Escribimos un loop que irá a través de cada uno de los nombres de archivo 
    a través de globbing y el resultado final será la lista dataframes
    '''
    
    xlsx_files = glob.glob("../WebScraping/ouput/"+portal+"/"+anyo+"/"+trim+"/"+'*.xlsx')
    list_data = []
    
    for filename in xlsx_files:
        data = pd.read_excel(filename, thousands='.')
        list_data.append(data)
    
    anuncios = pd.concat(list_data,ignore_index=True).sort_values(1,ascending=True)
    
    # Primer filtrado para la eliminación de duplicados entre webs
    anuncios = anuncios.drop_duplicates(anuncios.columns[anuncios.columns.isin(drop)])
        
    return anuncios


def store_data(df, anyo, trim, portal):
    df.to_excel('../Resultados/Archivo/anuncios_'+portal+'_' + anyo + trim +'.xlsx', header=True, index=False,encoding='utf-8-sig')


def coord(direc, city):
    
    '''
    Función que recibe el municipio y las direciones y devuelve las coordenadas
    utilizando "geopy.geocoders.Nominatim"
    '''
    
    coordenadas = []
    geolocator = Nominatim(user_agent="josemanuel@gmail.com")
    geocode = lambda query: geolocator.geocode(city % query)
    
    #for i in range(5):    
    for i in range(len(direc)):
        print(i) 
        try:
            location = geocode(direc[i])
            coordenadas.append((location.latitude, location.longitude)) 
            print(location.address) 
        except:
            coordenadas.append((0.000, 0.000))
            print('Dirección no encontrada')
            
            
    # Guardamos el archivo depurado 
    Dir = pd.DataFrame(coordenadas)
    Dir.columns = ['y','x']
    Dir = Dir[['x','y']] 
    Dir['x'] = Dir['x'].replace(".", ",")
    Dir['id'] = range(1,len(Dir)+1)
    #Dir['id'] = range(len(Dir))
    Dir = Dir.iloc[:,[2,0,1]]
    
    return Dir


def direc_google(direc, ciudad, provincia, pais, anyo, trim):
    
    '''
    Función que crea el archivo los parametros para crear el archivo para 
    geolocalizar utilizando "google earth"
    '''

    Direc_google_earth =  pd.DataFrame(direc)
    Direc_google_earth['id'] = range(1,len(Direc_google_earth)+1)
    Direc_google_earth['Ciudad'] = ciudad
    Direc_google_earth['Provincia'] = provincia
    Direc_google_earth['Pais'] = pais
    Direc_google_earth.rename(columns={0:'Calle'}, inplace=True)
    Direc_google_earth = Direc_google_earth.loc[:,['id','Calle','Ciudad','Provincia','Pais']]
    Direc_google_earth.to_excel("./Geolocalizacion/Direcciones "+anyo+trim+".xlsx", header=True, index=False, encoding='utf-8-sig')


def coord_google(D_g, anyo, trim):
    
    '''
    Función que recibe las direciones y crea el archivo xlsx para asignar las zonas
    '''
    
    Id = []
    x = []
    y = []
    
    coordenadas = pd.DataFrame()
    
    D = D_g[0]
    
    l = len(D['features'])
    
    for i in range(l):
        
        Id.append(int(D['features'][i]['properties']['id_2']))
        x.append(D['features'][i]['geometry']['coordinates'][0])
        y.append(D['features'][i]['geometry']['coordinates'][1])
    
    
    coordenadas['id'] = Id
    coordenadas['x'] = x
    coordenadas['y'] = y
    
    coordenadas.to_excel('./Geolocalizacion/coordenadas '+anyo+trim+'.xlsx', header=True, index=False, encoding='utf-8-sig')



def zona(df, Direcciones_Zona):
    
    '''
    Función que añade las zonas al dataframe
    '''
    
    df['Id_Zona'] = Direcciones_Zona['Zona']
    df['Fecha anuncio'] = pd.to_datetime(df['Fecha anuncio'], format="%Y%m%d")
    
    # Guardamos los que no hemos localizado la ubicación
    # NOTA: Aquí cabría investigar por si rescatamos alguna dirección
    df_N = df[df['Id_Zona'] == 0]
    
    # Se seleccionan las filas con zona asignada
    df = df[df['Id_Zona'] != 0]
    df = df.drop(['Calle'], axis=1)
    
    # Renumeramos el índice
    df.index = range(0,len(df))
    
    # Añadimos las zonas
    df_Zonas = pd.read_excel('./Geolocalizacion/Zonas.xlsx') ### añadir a constantes
    zona = []
    for i in range(len(df)):
      num = int(df.loc[i,['Id_Zona']]) 
      zona.append(df_Zonas['Zonas'][num-1])
      
    df['Zona']=zona
    df = df.iloc[:,[0,1,8,3,2,4,5,6,7]]
    

    return df, df_N


def elimina_dup(df):
    
    '''
    Función que elimina los duplicados existentes en las webs secundarias en base
    a criterios más laxos y mantiene los registros de la web principal.
    '''
    
    df_fotocasa_Y =df[df['Fuente'].str.contains('Fotocasa')]
    df_fotocasa_N =df[df['Fuente'].str.contains('Fotocasa')==False]
    df = df.drop_duplicates(df.columns[df.columns.isin(['Precio','Id_Zona','m2_U','Dormitorios','Baños'])])
    df_fotocasa_N =df[df['Fuente'].str.contains('Fotocasa')==False]
    df = pd.concat([df_fotocasa_Y, df_fotocasa_N])
    
    return df


def medias(df):
    
    '''
    Función que sustituye los valores faltantes de las columnas "m2_U", "Dormitorios"
    y "Baños" por sus medias
    '''
    
    df['m2_U'] = pd.to_numeric(df['m2_U'])
    df['m2_U'] = df['m2_U'].fillna(df['m2_U'].mean()) # No realizar si se hace regresión
    df['Dormitorios'] = pd.to_numeric(df['Dormitorios'])
    df['Dormitorios'] = df['Dormitorios'].fillna(df['Dormitorios'].mean())
    df['Baños'] = pd.to_numeric(df['Baños'])
    df['Baños'] = df['Baños'].fillna(df['Baños'].mean())
    
    df = df.drop(['m2_C'], axis=1) # No eliminar si se hace regresión

    return df


def trimestre(df):

    '''
    Construcción de la columna trimestre y ordenación del dataset
    '''
    
    df['year']= df['Fecha anuncio'].dt.year.astype(str)
    df['quarter'] = df['Fecha anuncio'].dt.quarter.astype(str)
    df['Trimestre'] = df['year'] + 'T' + df['quarter']
    
    df = df.iloc[:,[1,10,0,2,3,4,5,6,7]]
    
    return df


def val_extremos(df):
    '''
    Función que depura los valores extremos del dataset
    '''
    
    df = df[df['m2_U'] <= m2_sup] #m2_sup = 200
    df = df[df['m2_U'] >= m2_inf] #m2_inf = 30
    df = df[df['Dormitorios'] <= Dorm] # Dorm = 6
    df = df[df['Baños'] <= banyos] # banyos = 4
    
    
    # Detección y eliminación de outliers
    X = pd.DataFrame(data={'Precio':df['Precio']})
    #clf = KNN(contamination=0.18)
    clf = KNN()
    clf.fit(X)
    y_pred = clf.predict(X)
    outliers = list(X[y_pred == 1].index)
    df = df.drop(outliers, axis=0)
    
    # Se extraen las zonas con 5 o más observaciones
    zona = df.groupby(['Id_Zona'])['Zona'].count()
    zona = zona[zona > 4]
    num_zona = zona.index
    df = df[df.Id_Zona.isin(num_zona)]
    
    # Depuramos outlier dentro de cada zona
    df['Precio']= df['Precio'].astype(str).astype(int)
    media = df.groupby(['Id_Zona'])['Precio'].mean()
    desv = df.groupby(['Id_Zona'])['Precio'].std()
    lim_inf = media - 1.96 * desv
    lim_sup = media + 1.96 * desv

    # Se eliminan los valores que se alejan de la media por exceso o defecto 1,96 desviaciones típicas
    for i in num_zona:
      a = int(lim_inf[lim_inf.index == i])
      b = int(lim_sup[lim_inf.index == i])
      df_aux = df[df['Id_Zona'] == i]
      outliers = df_aux[(df_aux['Precio'] < a) | (df_aux['Precio'] > b)].index
      df = df.drop(outliers, axis=0)
      
    return df

def estadisticos(df):
    '''
    Función agrupa el dataframe con los estadisticos de interés
    '''
    #df = df_informe
    Id_Zona = pd.DataFrame(df.groupby(['Id_Zona'])['Precio'].count().index)
    
    Zona = pd.DataFrame(df.groupby(['Zona'])['Precio'].count().index)
    
    n = pd.DataFrame(df.groupby(['Id_Zona'])['Precio'].count())
    n.index = range(n.shape[0])
    
    precio = pd.DataFrame(df.groupby(['Id_Zona'])['Precio'].mean())
    precio.index = range(n.shape[0])
    
    desv = pd.DataFrame(df.groupby(['Id_Zona'])['Precio'].std())
    desv.index = range(n.shape[0])
    
    minimo = pd.DataFrame(df.groupby(['Id_Zona'])['Precio'].min())
    minimo.index = range(n.shape[0])
    
    maximo = pd.DataFrame(df.groupby(['Id_Zona'])['Precio'].max())
    maximo.index = range(n.shape[0])
    
    dormitorios = pd.DataFrame(df.groupby(['Id_Zona'])['Dormitorios'].mean())
    dormitorios.index = range(n.shape[0])
    
    baños = pd.DataFrame(df.groupby(['Id_Zona'])['Baños'].mean())
    baños.index = range(n.shape[0])
    
    m2_U = pd.DataFrame(df.groupby(['Id_Zona'])['m2_U'].mean())
    m2_U.index = range(n.shape[0])
    
    # Creamos la fecha tipo para el trimestre.    
    if trim == 1:
        mes = '03'
    elif trim == 2:
        mes = '06'
    elif trim == 3:
        mes = '09'
    else:
        mes = '12'
    
    fecha_dt = '01'+'/'+mes+'/'+anyo
    #fecha_dt = datetime.strptime(fecha_dt, '%d/%m/%Y')
    
    Fecha_anuncio = pd.DataFrame()
    Fecha_anuncio.index = range(n.shape[0]) 
    Fecha_anuncio['Fecha anuncio'] = fecha_dt
    
    # Unimos el dataframe con los datos agrupados
    df1 = pd.concat([Fecha_anuncio, Id_Zona, Zona, n, precio, m2_U, dormitorios, baños, minimo, maximo, desv],  axis=1,)
    df1.columns = ['Fecha anuncio', 'Id_Zona', 'Zona', 'n', 'Precio', 'm2_U', 'Dormitorios', 'Baños', 'P_min', 'P_max', 'P_desv']
    
    # Añadir el valores para zona 0
    n = df['Precio'].count()
    precio = df['Precio'].mean()
    m2_U = df['m2_U'].mean()
    dormitorios = df['Dormitorios'].mean()
    baños = df['Baños'].mean()
    minimo = df['Precio'].min()
    maximo = df['Precio'].max()
    desv = df['Precio'].std()
     
    
    total ={'Fecha anuncio':fecha_dt, 'Id_Zona':0, 'Zona':ciudad_google_earth, 
            'n':n, 'Precio':precio, 'm2_U':m2_U, 'Dormitorios':dormitorios, 
            'Baños':baños, 'P_min':minimo, 'P_max':maximo, 'P_desv':desv}
    
    total = pd.DataFrame(total, index=[0])
    
    df = pd.concat([total, df1])
    df.index = range(df.shape[0])
    

    
    return df


def intervalos(df):

    '''    
    Se crea la columna intervalo renta y se agrupa por zona e intervalo
    '''
    #df = df_informe
    
    df['intervalo'] = False

    df['intervalo'] = df['Precio'].apply(lambda x: 'Menor o igual 400 €' if x<=400 
                                         else ('401 € - 500 €' if (x>400) & (x<=500)  
                                             else ('501 € - 600 €' if (x>500) & (x<=600) 
                                                   else ('601 € - 700 €' if (x>600) & (x<=700) 
                                                         else ('701 € - 800 €' if (x>700) & (x<=800) 
                                                               else ('801 € - 900 €' if (x>800) & (x<=900) 
                                                                     else ('901 € - 1000 €' if (x>900) & (x<=1000) 
                                                                           else ('1001 € - 1100 €' if (x>1000) & (x<=1100) 
                                                                                 else ('1101 € - 1200 €' if (x>1100) & (x<=1200) 
                                                                                       else ('1201 € - 1300 €' if (x>1200) & (x<=1300) 
                                                                                             else ('Más de 1300 €') ) ) )))) ))))
        
    
    
    
    n = pd.DataFrame(df.groupby(['Id_Zona','intervalo'])['Precio'].count())
    n = n.reset_index()
    
    # Creamos la fecha tipo para el trimestre.    
    if trim == 1:
        mes = '03'
    elif trim == 2:
        mes = '06'
    elif trim == 3:
        mes = '09'
    else:
        mes = '12'
    
    fecha_dt = '01'+'/'+mes+'/'+anyo
    Fecha_anuncio = pd.DataFrame()
    Fecha_anuncio.index = range(n.shape[0]) 
    Fecha_anuncio['Fecha anuncio'] = fecha_dt
    
    # Unimos el dataframe con los datos agrupados
    df1 = pd.concat([Fecha_anuncio,  n],  axis=1)
    df1.columns = ['Fecha anuncio', 'Id_Zona', 'intervalo', 'n']
    
    # Añadir el valores para zona 0
    n = pd.DataFrame(df.groupby(['intervalo'])['Precio'].count())
    n = n.reset_index()
    Fecha_anuncio = pd.DataFrame()
    Fecha_anuncio.index = range(n.shape[0]) 
    Fecha_anuncio['Fecha anuncio'] = fecha_dt
    Id_Zona = pd.DataFrame()
    Id_Zona.index = range(n.shape[0])
    Id_Zona['Id_Zona'] = 0
        
    df = pd.concat([Fecha_anuncio, Id_Zona, n], axis=1)
    df.columns = ['Fecha anuncio', 'Id_Zona', 'intervalo', 'n']
    df = pd.concat([df, df1], axis=0)
    df.index = range(df.shape[0])
    
    return df


def dormitorios(df):

    '''    
    Se crea la columna intervalo renta y se agrupa por zona e intervalo
    '''
    #df = df_informe
    
    df['Interv_dorm'] = False

    df['Interv_dorm'] = df['Dormitorios'].apply(lambda x: 'Estudio o 1 Dorm.' if x<2 
                                         else ('2 Dorm.' if (x>=2) & (x<3)  
                                             else ('3 Dorm.' if (x>=3) & (x<4) 
                                                   else ('4 o más Dorm.') )))
        
    n = pd.DataFrame(df.groupby(['Id_Zona','Interv_dorm'])['Precio'].count())
    Precio = pd.DataFrame(df.groupby(['Id_Zona','Interv_dorm'])['Precio'].mean())
    df1 = pd.concat([n, Precio],  axis=1)
    df1 = df1.reset_index()
    
    # Creamos la fecha tipo para el trimestre.    
    if trim == 1:
        mes = '03'
    elif trim == 2:
        mes = '06'
    elif trim == 3:
        mes = '09'
    else:
        mes = '12'
    
    fecha_dt = '01'+'/'+mes+'/'+anyo
    Fecha_anuncio = pd.DataFrame()
    Fecha_anuncio.index = range(n.shape[0]) 
    Fecha_anuncio['Fecha anuncio'] = fecha_dt
    
    # Unimos el dataframe con los datos agrupados
    df1 = pd.concat([Fecha_anuncio, df1],  axis=1)
    df1.columns = ['Fecha anuncio', 'Id_Zona', 'Dormitorios', 'n', 'Precio']
    
    # Añadir el valores para zona 0
    n = pd.DataFrame(df.groupby(['Interv_dorm'])['Precio'].count())
    Precio = pd.DataFrame(df.groupby(['Interv_dorm'])['Precio'].mean())
    df = pd.concat([n, Precio],  axis=1)
    df = df.reset_index()
    
    Fecha_anuncio = pd.DataFrame()
    Fecha_anuncio.index = range(n.shape[0]) 
    Fecha_anuncio['Fecha anuncio'] = fecha_dt
    Id_Zona = pd.DataFrame()
    Id_Zona.index = range(n.shape[0])
    Id_Zona['Id_Zona'] = 0
        
    df = pd.concat([Fecha_anuncio, Id_Zona, df], axis=1)
    df.columns = ['Fecha anuncio', 'Id_Zona', 'Dormitorios', 'n', 'Precio']
    df = pd.concat([df, df1], axis=0)
    df.index = range(df.shape[0])
    
    return df
      
############# CUERPO PRINCIPAL ##############

# Leemos y unimos los dataset diarios de cada portal
df_fotocasa = unir_excel(anyo, trim, portal='fotocasa', drop=[7])
df_pisoscom = unir_excel(anyo, trim, portal='pisoscom', drop=[6])
df_idealista = unir_excel(anyo, trim, portal='idealista', drop=[3])

# Guardamos los archivos por si queremos extraer otras variables posteriormente
store_data(df_fotocasa, anyo, trim, portal='fotocasa')
store_data(df_pisoscom, anyo, trim, portal='pisoscom')
store_data(df_idealista, anyo, trim, portal='idealista')
   
# Depuramos y unimos los dataset
df_fotocasa_dep = fotocasa_dep.debug_dataset(df_fotocasa)
df_pisoscom_dep = pisoscom_dep.debug_dataset(df_pisoscom)
df_idealista_dep = idealista_dep.debug_dataset(df_idealista)  
df_informe = pd.concat([df_idealista, df_fotocasa_dep, df_pisoscom_dep])
df_informe.columns = ['Fecha anuncio','Fuente','Precio','Calle','Zona','m2_C','m2_U','Dormitorios','Baños','Planta','Tipo']

# Se quitan los duplicados entre webs
df_informe = df_informe.drop_duplicates(df_informe.columns[df_informe.columns.isin(['Calle','Zona','m2_U','Dormitorios','Baños'])])

df_informe.index = range(0, len(df_informe))
df_informe['Id_Zona'] = False

df_informe = df_informe.drop(['Planta'], axis=1)
df_informe = df_informe.drop(['Tipo'], axis=1)

# obtenemos las coordenadas de las direcciones
direcciones = list(df_informe['Calle'])

######## NOMINATION ########
# Si utilizamos "geopy.geocoders.Nominatim" para obtener las coordenadas
Direcciones_coord = coord(direcciones, ciudad_Nominatim)
####################

'''
######## GOOGLE EARTH ########
# Si utilizamos "google earth" para obtener las coordenadas
direc_google(direcciones, ciudad_google_earth, provincia, pais, anyo, trim)

#### EL CÓDIGO SE EJECUTA HASTA AQUÍ ------------------------------------------

# El archivo resultante se geolocaliza en google earth, se descarga 
# con el nombre "Direcciones 2022T3.KML" correspondiente y se guarda 
# en la ruta: "./Geolocalizacion/".

#### CONTINUAMOS CON LA EJECUCIÓN DEL CÓDIGO ----------------------------------
se lee y de este se extraen las coordenadas de cada dirección
Direcciones_google = kml2geojson.main.convert('./Geolocalizacion/Direcciones 2022T3.KML', './Geolocalizacion')
coord_google(Direcciones_google, anyo, trim)

# Se lee el archivo con las coordenadas
Direcciones_coord = pd.read_excel('./Geolocalizacion/coordenadas '+anyo+trim+'.xlsx')
# Direcciones_coord = Direcciones_coord.head(100)
######################
'''

# Se asignan las zonas a las coordenadas de las direcciones
Direcciones_Zona = geo.geolocalizacion(Direcciones_coord)

# Se añade la columna zona al dataset
df_informe, df_informe_N = zona(df_informe, Direcciones_Zona)

'''
# Se guarda el archivo con las direccones no encontradas
os.makedirs("./ouput/informe/"+anyo+"/"+trim, exist_ok=True)
df_informe_N.to_excel("./ouput/informe/"+anyo+"/"+trim+"/"+"df_informe_N "+anyo+trim+".xlsx", header=True, index=False, encoding='utf-8-sig')  
'''
# Se eliminan las viviendas posibles duplicados de las sucesivas webs y se añaden a la principal
df_informe = elimina_dup(df_informe)

# Sustitución de los na por las medias
df_informe = medias(df_informe)

'''
# Construcción de columna Trimestre y ordenación del dataset
df_informe = trimestre(df_informe)
'''

# Depuración del dataframe
# En este punto se depura el dataframe en función de los criterios establecidos en el apartado x.xx
df_informe = val_extremos(df_informe)
#df2 = df_informe
# Agrupación del dataframe para obtener principales estadísticos
df_informe_agrup = estadisticos(df_informe)

# Agrupación del dataframe por zona e intervalo de renta para obtener el total de anuncios en cada categoria
df_intervalo_agrup = intervalos(df_informe)

# Agrupación del dataframe por zona y dormitorios para obtener el total de anuncios en cada categoria
df_dormitorio_agrup = dormitorios(df_informe)

'''
# Guarda datos en un archivo xlsx
writer = pd.ExcelWriter("./ouput/informe/"+anyo+"/"+trim+"/"+"data "+anyo+trim+".xlsx")
df_informe_agrup.to_excel(writer, sheet_name="data", header=True, index=False, encoding='utf-8-sig')
df_dormitorio_agrup.to_excel(writer, sheet_name="dormitorios", header=True, index=False, encoding='utf-8-sig')
df_intervalo_agrup.to_excel(writer, sheet_name="Intervalos renta", header=True, index=False, encoding='utf-8-sig')
writer.save()
writer.close()
'''

# Se une con el dataset del trimestre anterior y se guarda en el imput del cuadro de mando
df_data = pd.read_excel("../Resultados/CuadroMando/data.xlsx", sheet_name='data')
df_dormitorios = pd.read_excel("../Resultados/CuadroMando/data.xlsx", sheet_name='dormitorios')
df_intervalos = pd.read_excel("../Resultados/CuadroMando/data.xlsx", sheet_name='Intervalos renta')

df_data = pd.concat([df_data, df_informe_agrup])
df_dormitorios = pd.concat([df_dormitorios, df_dormitorio_agrup])
df_intervalos = pd.concat([df_intervalos, df_intervalo_agrup])

# Guarda datos los datos actualizados en un archivo xlsx en la carpeta imput del cuadro de mando
writer = pd.ExcelWriter("../Resultados/CuadroMando/data.xlsx")
df_data.to_excel(writer, sheet_name="data", header=True, index=False, encoding='utf-8-sig')
df_dormitorios.to_excel(writer, sheet_name="dormitorios", header=True, index=False, encoding='utf-8-sig')
df_intervalos.to_excel(writer, sheet_name="Intervalos renta", header=True, index=False, encoding='utf-8-sig')
writer.save()
writer.close()






