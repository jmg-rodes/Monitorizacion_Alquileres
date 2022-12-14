"""
Created on Fri Oct 25 11:51:35 2020

@author: José Manuel García Rodes
"""

import logging
#import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup

def transform_html_to_data(html, data_list, datetime_now): 
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extraemos los links 'a' de la sopa     
    a_tag = []
    a_tag = soup.find_all('a',attrs={'class': 'ad-preview__title'})
     
    # Guardo las urls en una lista
    url_list = []
    for link in a_tag:
        url_list.append(link.get('href'))
       
    print ('url_list: {}'.format(url_list))
       
    # Para cada url de la lista extraemos los datos del anuncio    
    # anuncio = []
    for i in range(len(url_list)):
        try:
            print ('Anuncio: {}; \n URL: https://www.pisos.com{}'.format(i, url_list[i]))
            req = requests.get('https://www.pisos.com' + url_list[i])    
                    
            soup = BeautifulSoup(req.text, "lxml")
            
    
            # Asignación de variables
            euro = []
            part = []
            direc = []
            zona = []
            desc = []
            muebles = []
            baños = []
            dorm = []
            ca = []
            fecha_hora = []
            today = datetime.today()        
            url_sec_list = []
            portal = []
            url_sec_list = []
            
            fecha_hora.append(today.strftime("%Y.%m.%d"))
            
            portal.append('Pisos.com')
            
            url_sec_list.append('https://www.pisos.com' + url_list[i])
            
            
            euro_tag=soup.find('span',attrs={'class': 'h1 jsPrecioH1'})
            if euro_tag is not None:
                for st in euro_tag.stripped_strings:
                    euro.append(st)
            
            part_tag=soup.find('div',attrs={'class': 'owner-data-info'})
            if part_tag is not None:
                for st in part_tag.stripped_strings:
                    part.append(st)
        
            direc_tag=soup.find('h1',attrs={'class': 'title'})
            if direc_tag is not None:
                for st in direc_tag.stripped_strings:
                    direc.append(st)
                
            zona_tag=soup.find('h2',attrs={'class': 'position'})
            if zona_tag is not None:
                for st in zona_tag.stripped_strings:
                    zona.append(st)
                
            ca_tag = soup.find_all('ul',attrs={'class': 'charblock-list'})    
            
            if ca_tag is not None:
                for st in ca_tag:
                    ca_t = st.text.strip()
                    ca_t_replace_n = ca_t.replace('\n', ' ')
                    ca.append(ca_t_replace_n)
            
            desc_tag=soup.find('div',attrs={'class': 'description-container description-body'})
            if desc_tag is not None:
                for st in desc_tag.stripped_strings:
                    st_replace_n = st.replace('\n', '')
                    st_replace_r = st_replace_n.replace('\r', '')
                    desc.append(st_replace_r)
            
            muebles_tag=soup.find('ul',attrs={'class': 'charblock-element element-with-bullet'})
            if muebles_tag is not None:
                for st in muebles_tag.stripped_strings:
                    muebles.append(st)
                   
            baños_tag=soup.find('div',attrs={'class': 'icon icon-banyos'})
            if baños_tag is not None:
                for st in baños_tag.stripped_strings:
                    baños.append(st)
            
            dorm_tag=soup.find('div',attrs={'class': 'icon icon-habitaciones'})
            if dorm_tag is not None:           
                for st in dorm_tag.stripped_strings:
                    dorm.append(st)
                
            data_list.append(fecha_hora + portal + euro + part + url_sec_list + zona + direc + dorm + baños + ca + desc)
            
        except:
            logging.error('The url [' + url_list[i] + '] is advertasing')
        
    return data_list