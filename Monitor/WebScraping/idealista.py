# -*- coding: utf-8 -*-
"""
Created on Fri May 15 11:51:35 2020

@author: user
"""
import logging
import time
from datetime import datetime

from selenium.webdriver.common.keys import Keys
import soup_transformer_idealista as transformer
from bs4 import BeautifulSoup

from constant import *
import pandas as pd

from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver


# Valores de variables para pruebas
#url = BASE_URL_idealista
#url_link = url
#number_of_pages = 1
#run = 1
#anuncios_idealista = []

# Use selenium to load a web
# IMPORTANT: The driver included is for Chrome version 86
# If you use another version you can download it from https://chromedriver.chromium.org/downloads

def human_get(url: str, number_of_pages: int, run, anuncios_idealista):
    # Establecemos la fecha
    today = datetime.today()
    fecha_hora = today.strftime("%Y.%m.%d_%H.%M.%S")
    fecha = today.strftime("%Y.%m.%d")
    
    # Acumulo todos los anuncios de cada dia en una lista
    anuncios_idealista_dia = scraping_idealista(url, number_of_pages)
    print('data_list: {}'.format(anuncios_idealista_dia))
    for anuncio in anuncios_idealista_dia:
        anuncios_idealista.append(anuncio)

    # Creo un dataframe con los anuncios acumulados
    df_idealista = pd.DataFrame(anuncios_idealista)
    
    # Quito los duplicados
    df_idealista = df_idealista.drop_duplicates(df_idealista.columns[~df_idealista.columns.isin([0])])
    print('df_idealista: {}'.format(df_idealista))
    
    # Acumulamos los datos en un único archivo
    df_idealista.to_excel('./ouput/idealista/anuncios_idealista '+ fecha_hora +'.xlsx', encoding='utf-8-sig')
    print('dataframe total')
    
    # Me quedo con los particulares del día
    df_idealista_particulares = pd.DataFrame(df_idealista)[~pd.DataFrame(df_idealista)[5].str.contains('Profesional')]
    df_idealista_particulares = pd.DataFrame(df_idealista_particulares)[pd.DataFrame(df_idealista_particulares)[0].str.contains(fecha)]
    df_idealista_particulares[2] = df_idealista_particulares[2] + ' €'
    df_idealista_particulares = df_idealista_particulares.iloc[:,[0,1,2,5,3,4]]
    df_idealista_particulares.columns = ['Fecha', 'Portal','Renta', 'Titular', 'Web', 'Dirección']
    print('df_idealista_particulares: {}'.format(df_idealista_particulares))
    # Creo un excel con los anuncios de particulares
    pd.DataFrame(df_idealista_particulares).to_excel('./ouput/idealista/anuncios_idealista_particulares_'+ str(run+1) +'_'+ fecha +'.xlsx', encoding='utf-8-sig')
    print('dataframe particulares')
    

def scraping_idealista (url_link, number_of_pages: int):
    
    """
        
    Función que recibe un link de Idealista y extrae las características del anuncio.
        
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
    transformer.transform_html_to_data(html, data_list, datetime_now)
    
    
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
    print(html)
    return data_list, data_list2, data_list3

                 
def init_browser():
    # Use a random user agent and init selenium
    options = Options()
    user_agent = UserAgent()
    random_user_agent = user_agent.random

    options.add_argument(f'user-agent={random_user_agent}')
    browser = webdriver.Chrome(chrome_options=options, executable_path=r'./selenium/chromedriver.exe')
    
    browser = webdriver.Chrome(executable_path=r'./selenium/chromedriver.exe')
    return browser

# Action to scroll down and get the html code
def action_get_page(browser):
    elem = browser.find_element_by_tag_name('body')
    
    # Scroll to the end of the page
    no_of_pagedowns = 30

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)

        time.sleep(1)
        no_of_pagedowns -= 1

    # Go to the paginator
    ActionChains(browser).move_to_element(browser.find_element_by_xpath(build_path_for_paginator())).perform()
    time.sleep(SELENIUM_SLEEP_TIME)

    html = browser.page_source

    return html

# Action to go to the next page
def action_next_page(browser):
    next_page = browser.find_elements_by_xpath(build_path_for_next_page())#[0]
    next_page = next_page[len(next_page)-1]
    
    next_page.click()
    
    time.sleep(SELENIUM_SLEEP_TIME)



# Get the xpath for the next page
def build_path_for_next_page():
    #return '//a[ancestor::li[@class="sui-AtomButton sui-AtomButton--primary sui-AtomButton--flat sui-AtomButton--center sui-AtomButton--fullWidth"]]'
    #return '//*[@id="App"]/div[2]/div[1]/main/div/div[4]/ul/li[7]/a'
    return '//a[@class="icon-arrow-right-after"]'
             
# Get the xpath for the paginator
def build_path_for_paginator():
    return '//a[@class="icon-arrow-right-after"]'


