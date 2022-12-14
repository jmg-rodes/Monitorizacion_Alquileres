# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 11:51:35 2020

@author: José Manuel García Rodes
"""
import logging
import time
import os
from selenium.webdriver.common.keys import Keys
import soup_transformer_pisoscom as transformer
from selenium.webdriver.common.by import By

from constant import *
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from datetime import datetime

import pandas as pd
import numpy as np

'''
PARA PRUEBAS
url = 'https://www.pisos.com/alquiler/pisos-alicante_alacant/fecharecientedesde-desc/'
number_of_pages = 1
df_pisoscom = pd.read_excel('./ouput/pisoscom/anuncios_pisoscom.xlsx')
df_pisoscom = df_pisoscom.drop(['Unnamed: 0'], axis=1)

'''

# Uso de selenium para cargar una web
# IMPORTANTE: El driver incluido es para Chrome version 108
# Si se usa otra versión hay que descargar de nuevo el driver 
# de https://chromedriver.chromium.org/downloads

def human_get(url: str, number_of_pages: int, run, anuncios_pisoscom):
    
    '''
    Función principal que extrae las características del anuncio y las almacena 
    en un archivo xlsx
    '''
    
    # Se establece la fecha
    today = datetime.today()
    fecha_hora = today.strftime("%Y.%m.%d_%H.%M.%S")
    fecha = today.strftime("%Y.%m.%d")    
    trim =str((today.month-1)//3)+1
    anyo = str(today.year)
    
    
    # Se acumulan todos los anuncios de cada dia en una lista
    anuncios_pisoscom_dia = scraping_pisoscom(url, number_of_pages)
    for anuncio in anuncios_pisoscom_dia:
        anuncios_pisoscom.append(anuncio)

    # Se crea un dataframe con los anuncios acumulados
    df_pisoscom = pd.DataFrame(anuncios_pisoscom)
    
    # Se quitan los duplicados
    df_pisoscom = df_pisoscom.drop_duplicates(df_pisoscom.columns[df_pisoscom.columns.isin([6])])
    df_pisoscom = df_pisoscom.drop_duplicates(df_pisoscom.columns[df_pisoscom.columns.isin([8,9])])
    
    # Se guardan los datos en un archivo en la carpeta correspondiente al trimestre
    os.makedirs("./ouput/pisoscom/"+anyo+"/T"+trim, exist_ok=True)
    df_pisoscom.to_excel("./ouput/pisoscom/"+anyo+"/T"+trim+"/"+"anuncios_pisoscom "+ fecha_hora +".xlsx", encoding="utf-8-sig")

    # Anuncios particulares del día
    df_pisoscom_particulares = debug_dataset_part(df_pisoscom, fecha)
                   
    # Se crea un excel con los anuncios de particulares y se guarda en su carpeta
    pd.DataFrame(df_pisoscom_particulares).to_excel('./ouput/particulares/pisoscom/anuncios_pisoscom_particulares_'+ str(run+1) + '_'+ fecha +'.xlsx', encoding='utf-8-sig')
    

#######################################################################################
### Depuración de dataset particulares
#######################################################################################
    
def debug_dataset_part(df, fecha):

    '''
    Selecciona los anuncios de particuales y se toman las columnas de interés
    '''
    df_part = pd.DataFrame(df)[~pd.DataFrame(df)[4].str.contains('Inmuebles de')]
    df_part = pd.DataFrame(df_part)[pd.DataFrame(df_part)[0].str.contains(fecha)]
    df_part = df_part.iloc[:,[0,1,2,4,6,7]]
    df_part.columns = ['Fecha', 'Portal','Renta', 'Titular', 'Web', 'Dirección']

    return df_part
    
    
    
###############################################################################
def scraping_pisoscom (url_link, number_of_pages: int):
    
    """
        
    Función que recibe un link de Pisos.com y extrae las características del anuncio.
        
    """
    
    # Init
    data_list = []
    
    # Make a get request
    datetime_now = datetime.now()

    browser = init_browser()
    browser.maximize_window()

    # Go to the url
    browser.get(url_link)
    time.sleep(15)

    # action accept cookies
    #action_accept_cookies(browser)
    
    # Get the html and transform the data
    html = action_get_page(browser)
    transformer.transform_html_to_data(html, data_list, datetime_now)
    #soup = BeautifulSoup(html, 'html.parser')

    # Go to next page and scroll and repeat the process
    j = 1
    while j < number_of_pages:
        action_next_page(browser)
        html = action_get_page(browser)
        transformer.transform_html_to_data(html, data_list, datetime_now)
        # Convert the html string to a BeautifulSoup object
        #soup = BeautifulSoup(html, 'html.parser')
        j += 1
        
    # Stop selenium
    browser.quit()        
    
    return data_list
                     
# Action to intialiation broswser
def init_browser():
    browser = webdriver.Chrome(executable_path=r'./selenium/chromedriver.exe')
    return browser


# Action to scroll down and get the html code
def action_get_page(browser):
    elem = browser.find_element(By.TAG_NAME, "body")

    # Scroll to the end of the page
    no_of_pagedowns = 20

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)

        time.sleep(1)
        no_of_pagedowns -= 1

    # Go to the paginator
    ActionChains(browser).move_to_element(browser.find_element(By.XPATH, build_path_for_paginator())).perform()
    time.sleep(5)

    html = browser.page_source

    return html

# Action to go to the next page
def action_next_page(browser):
    next_page = browser.find_elements(By.XPATH, build_path_for_next_page())#[0]
    next_page = next_page[len(next_page)-1]
    
    next_page.click()
    
    time.sleep(SELENIUM_SLEEP_TIME)

'''
# Get the xpath for the cookies button
def build_path_for_cookies():
    return '//*[@id="didomi-notice-agree-button"]'
'''
# Get the xpath for the paginator
def build_path_for_paginator():
    return '//*[@id="main"]/div[3]/div/div[2]/div[36]/div[1]/div'


# Get the xpath for the next page
def build_path_for_next_page():
    return '//*[@id="main"]/div[3]/div/div[2]/div[36]/div[1]/div'




