# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 11:51:35 2020

@author: José Manuel García Rodes
"""
import logging
import time
import os
from selenium.webdriver.common.keys import Keys
import soup_transformer_fotocasa as transformer
from selenium.webdriver.common.by import By
from constant import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from datetime import datetime
import pandas as pd

'''
######## PARA PRUEBAS ########
url = 'https://www.fotocasa.es/es/alquiler/viviendas/alicante-alacant/todas-las-zonas/l?sortType=publicationDate'
number_of_pages = 1
run = 0
df_fotocasa = pd.read_excel('./ouput/fotocasa/anuncios_fotocasa.xlsx')
df_fotocasa = df_fotocasa.drop(['Unnamed: 0'], axis=1)
'''

# Uso de selenium para cargar una web
# IMPORTANTE: El driver incluido es para Chrome version 108
# Si se usa otra versión hay que descargar de nuevo el driver 
# de https://chromedriver.chromium.org/downloads

def human_get(url: str, number_of_pages: int, run: int, anuncios_fotocasa):   
    
    '''
    Función principal que extrae las características del anuncio y las almacena 
    en un archivo xlsx
    '''
    
    # Establecemos la fecha
    today = datetime.today()
    fecha_hora = today.strftime("%Y.%m.%d_%H.%M.%S")
    fecha = today.strftime("%Y.%m.%d")
    trim = str((today.month-1)//3)+1
    anyo = str(today.year)
       
    # Se acumulan todos los anuncios de cada dia en una lista
    anuncios_fotocasa_dia, anuncios_fotocasa_dia2, anuncios_fotocasa_dia3 = scraping_fotocasa(url, number_of_pages)
    anuncios_fotocasa1 = []
    anuncios_fotocasa2 = []
    anuncios_fotocasa3 = []
    for anuncio in anuncios_fotocasa_dia:
        anuncios_fotocasa1.append(anuncio)
    for anuncio in anuncios_fotocasa_dia2:
        anuncios_fotocasa2.append(anuncio)
    for anuncio in anuncios_fotocasa_dia3:
        anuncios_fotocasa3.append(anuncio)    

    # Se crea un dataframe con los anuncios acumulados
    df_fotocasa1 = pd.DataFrame(anuncios_fotocasa1)
    df_fotocasa2 = pd.DataFrame(anuncios_fotocasa2)
    df_fotocasa3 = pd.DataFrame(anuncios_fotocasa3)
   
    # Se unen los dataframes
    df_fotocasa = pd.concat([df_fotocasa1, df_fotocasa2, df_fotocasa3], axis=1,)
    columns_names = df_fotocasa.columns.values
    columns_names = list(columns_names)
    columns_names = list(range(0,len(columns_names)))
    df_fotocasa.columns = columns_names
    
    # Se quitan los duplicados
    #df_fotocasa = df_fotocasa.drop_duplicates(df_fotocasa.columns[~df_fotocasa.columns.isin([0])])
    df_fotocasa = df_fotocasa.drop_duplicates(df_fotocasa.columns[df_fotocasa.columns.isin([7])])
    df_fotocasa = df_fotocasa.drop_duplicates(df_fotocasa.columns[df_fotocasa.columns.isin([8,9,11,13,15])])

    # Se guardan los datos en un archivo en la carpeta correspondiente al trimestre
    os.makedirs("./ouput/fotocasa/"+anyo+"/T"+trim, exist_ok=True)
    df_fotocasa.to_excel("./ouput/fotocasa/"+anyo+"/T"+trim+"/"+"anuncios_fotocasa "+ fecha_hora +".xlsx", encoding="utf-8-sig")
          
    # Anuncios particulares del día
    df_fotocasa_particulares = pd.DataFrame(df_fotocasa)[pd.DataFrame(df_fotocasa)[5].str.contains('particular:')]
    df_fotocasa_particulares = pd.DataFrame(df_fotocasa_particulares)[pd.DataFrame(df_fotocasa_particulares)[0].str.contains(fecha)]
    df_fotocasa_particulares = df_fotocasa_particulares.iloc[:,[0,1,2,6,7,8]]
    df_fotocasa_particulares.columns = ['Fecha', 'Portal','Renta', 'Titular', 'Web', 'Dirección' ]
    
    # Se crea un excel con los anuncios de particulares
    pd.DataFrame(df_fotocasa_particulares).to_excel('./ouput/particulares/fotocasa/anuncios_fotocasa_particulares_'+ str(run+1) + '_' + fecha +'.xlsx', encoding='utf-8-sig')
   
    
    
def scraping_fotocasa (url_link, number_of_pages: int):
    
    """
        
    Función que recibe un link de fotocasa y extrae las características del anuncio.
        
    """
    # Preparing the monitoring of the loop
    requests = 0
    
    # Init
    data_list = []
    data_list2 = []
    data_list3 = []
    datetime_now = datetime.now()

    browser = init_browser()
    browser.maximize_window()

    # Go to the url
    browser.get(url_link)
    time.sleep(SELENIUM_SLEEP_TIME)

        
    # Get the html and transform the data
    html = action_get_page(browser)
    transformer.transform_html_to_data(html, data_list, data_list2,  data_list3, datetime_now)
    
    # Go to next page and scroll and repeat the process
    j = 1
    while j < number_of_pages:
        print('página: {}'.format(j))
        action_next_page(browser)
        print('action_get_page')
        time.sleep(20)
        html = action_get_page(browser)
        print('transform_html_to_data')
        transformer.transform_html_to_data(html, data_list, datetime_now)
        print('#####################################################')
        #print(data_list[0])
        j += 1
    
    # Stop selenium
    browser.quit()
    
    return data_list, data_list2, data_list3

                 
def init_browser():
    # Use a random user agent and init selenium
    browser = webdriver.Chrome(executable_path=r'./selenium/chromedriver.exe')
    return browser

# Action to scroll down and get the html code
def action_get_page(browser):
    elem = browser.find_element(By.TAG_NAME, "body")
        
    # Scroll to the end of the page
    no_of_pagedowns = 30

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)

        time.sleep(1)
        no_of_pagedowns -= 1

    # Go to the paginator
    ActionChains(browser).move_to_element(browser.find_element(By.XPATH, build_path_for_paginator())).perform()
    time.sleep(SELENIUM_SLEEP_TIME)

    html = browser.page_source

    return html

# Action to go to the next page
def action_next_page(browser):
    next_page = browser.find_elements(By.XPATH, build_path_for_next_page())#[0]
    next_page = next_page[len(next_page)-1]
    
    next_page.click()
    
    time.sleep(SELENIUM_SLEEP_TIME)

# Get the xpath for the next page
def build_path_for_next_page():
    #return '//a[ancestor::li[@class="sui-AtomButton sui-AtomButton--primary sui-AtomButton--flat sui-AtomButton--center sui-AtomButton--fullWidth"]]'
    return '//*[@id="App"]/div[2]/div[1]/main/div/div[4]/ul/li[7]/a'
    #return '/html/body/div[1]/div[2]/div[1]/main/div/div[4]/ul/li[7]/a'
             
# Get the xpath for the paginator
def build_path_for_paginator():
    return '//div[@class="re-Pagination"]'



