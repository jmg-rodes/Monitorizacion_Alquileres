"""
Created on Fri Oct 25 11:51:35 2020

@author: José Manuel García Rodes
"""

import logging
import requests
from datetime import datetime
from bs4 import BeautifulSoup


def transform_html_to_data(html, data_list, data_list2, data_list3, datetime_now): 
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extraemos los links 'a' de la sopa 
    a_tag = []
    a_tag = soup.find_all('a',attrs={'class': 're-CardPackMinimal-info-container'})
     
    # Guardo las urls en una lista
    url_list = []
    for link in a_tag:
        url_list.append(link.get('href'))
        
    #print(url_list)
    
    # Para cada url de la lista extraemos los datos del anuncio       
    for i in range(len(url_list)):  
       
        try:
            url_link_sec='https://www.fotocasa.es' + url_list[i] 
            
            print ('Anuncio: {}; \n URL: https://www.fotocasa.es{}'.format(i, url_list[i]))
            req = requests.get(url = url_link_sec)
            soup = BeautifulSoup(req.text, "lxml")
            
            # Asignación de variables
            euro=[]
            caract=[]
            zona=[]
            desc =[]
            otras_caract =[]
            extras =[]
            contacto =[]
            fecha_hora = []
            today = datetime.today()
            fecha_hora.append(today.strftime("%Y.%m.%d"))
            portal = []
            url_sec_list = []
            
            
            portal.append('Fotocasa')
            
            url_sec_list.append('https://www.fotocasa.es' + url_list[i])
                     
            euro_tag=soup.find('span','re-DetailHeader-price')
            if euro_tag is not None:
                for st in euro_tag.stripped_strings:
                    euro.append(st)
        
            caract_tag=soup.find('ul','re-DetailHeader-features')
            if caract_tag is not None:
                for st in caract_tag.stripped_strings:
                    caract.append(st)
                
            zona_tag=soup.find('h1','re-DetailHeader-propertyTitle')
            if zona_tag is not None:
                for st in zona_tag.stripped_strings:
                    zona.append(st)
        
            desc_tag=soup.find('div','re-DetailFeaturesList')
            if desc_tag is not None:
                for st in desc_tag.stripped_strings:
                    desc.append(st)
            
            otras_caract_tag=soup.find('section','re-DetailFeaturesList')
            if otras_caract_tag is not None:
                for st in otras_caract_tag.stripped_strings:
                    otras_caract.append(st)
            
            extras_tag=soup.find('ul','re-DetailExtras-list')
            if extras_tag is not None:           
                for st in extras_tag.stripped_strings:
                    extras.append(st)
                
            contacto_tag=soup.find('div','re-ContactDetailPhoneContainer')
            if contacto_tag is not None:   
                for st in contacto_tag.stripped_strings:
                    contacto.append(st)
                if len(contacto) <= 2:
                    contacto.insert(1,'Inmobiliaria')
                
            
            data_list.append(fecha_hora + portal + euro + contacto + url_sec_list + zona + caract + otras_caract)
            data_list2.append(desc)
            data_list3.append(extras)
                        
        except:
            logging.error('The url [' + url_list[i] + '] is advertasing')
        
    return data_list, data_list2, data_list3