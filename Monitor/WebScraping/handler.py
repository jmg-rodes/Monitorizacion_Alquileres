import particulares as provider_particulares
import fotocasa as provider_fotocasa
#import idealista as provider_idealista
import pisoscom as provider_pisoscom

import constant as constant
import sys
from constant import *
import time

'''
def is_first_arg_help(arg):
    if arg == '-h' or arg == '--help':
        print('handler.py [city_name] [pages_number]')
        sys.exit(2)
    return False


if __name__ == "__main__":
    city = constant.DEFAULT_CITY
    pages = constant.DEFAULT_PAGES

    args = sys.argv

    # Check arguments
    if len(args) >= 2:
        arg1 = args[1]
        # Check if the first arg is for help or the city
        is_help = is_first_arg_help(arg1)
        if not is_help:
            city = arg1

        # The second arg is the number of pages
        if len(args) == 3:
            pages = int(args[2])
'''
city = constant.DEFAULT_CITY
pages = constant.DEFAULT_PAGES

print('- City: ' + city)
print('- Pages: ' + str(pages))
print()
print('Launching...')

# Días para los que se realiza el webscraping
requests = 0 
anuncios_pisoscom = [] 
anuncios_fotocasa = [] 
anuncios_idealista = []

for i in range(DIAS):
    # Número de veces que se visita la página x día
    for run in range(FRECUENCIA):      
        try:
            provider_pisoscom.human_get(constant.BASE_URL_pisoscom, pages, run, anuncios_pisoscom)
        except:
               print('Ha fallado pisoscom')
        try:
            provider_fotocasa.human_get(constant.BASE_URL_fotocasa, pages, run, anuncios_fotocasa)
        except:
            print('Ha fallado fotocasa')
        '''try:         
            provider_idealista.human_get(constant.BASE_URL_idealista, pages, run, anuncios_idealista)
        except:
            print('Ha fallado idealista')'''
        try:    
            provider_particulares.anuncios_get(run)
        except:
            print('Ha fallado particulares')
            
        # Monitor the requests
        requests += 1
        print('Request:{}; Día: {}; Run: {}'.format(requests, i+1, run+1 ))
        
        # número de segundos por webscraping (5400 para que lo haga cada hora y media)
        #segundos = 86400/FRECUENCIA
        segundos = 5
        time.sleep(segundos)

#provider_fotocasa.debug_dataset(df_fotocasa)
print ('***** SE HAN REALIZADO {} VISITAS A LAS WEBS *****'.format(i+1))
        
                
            
