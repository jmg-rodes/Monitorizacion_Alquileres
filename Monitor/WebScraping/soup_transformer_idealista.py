from datetime import datetime
import requests
from bs4 import BeautifulSoup
 

def transform_html_to_data(html, data_list, datetime_now): 
    soup = BeautifulSoup(html, "lxml")
  
    
    # Extraemos los links 'a' de la sopa 
    a_tag = []
    a_tag = soup.find_all('a',attrs={'class': 'item-link'})
       
    # Guardo las urls en una lista
    url_list = []
    for link in a_tag:
        url_list.append(link.get('href'))
       
    print ('url_list: {}'.format(url_list))
    
    
    # Para cada url de la lista extraemos los datos del anuncio    
    for i in range(len(url_list)):
        print ('Anuncio: {}; \n URL: https://www.idealista.com{}'.format(i, url_list[i]))
        
        url_link_sec='https://www.idealista.com' + url_list[i]
        
        try:    
            req = requests.get(url = url_link_sec)
            soup = BeautifulSoup(req.text, "lxml")
                    
            # Asignación de variables
            euro=[]
            caract=[]
            zona=[]
            desc =[]
            caract_basic =[]
            edificio =[]
            equipamiento = []
            contacto = []
            telefono = []
            fecha_hora = []
            today = datetime.today()        
            portal = []
            url_sec_list = []
            
            fecha_hora.append(today.strftime("%Y.%m.%d"))
            
            portal.append('Idealista')
            
            url_sec_list.append('https://www.idealista.com' + url_list[i])
                 
            euro_tag=soup.find('span',attrs={'class': 'txt-bold'})
            if euro_tag is not None:
                for st in euro_tag.stripped_strings:
                    euro.append(st)
            
            caract_tag=soup.find('div',attrs={'class': 'info-features'})
            if caract_tag is not None:
                for st in caract_tag.stripped_strings:
                    caract.append(st)
                
            zona_tag=soup.find('span',attrs={'class': 'main-info__title-main'})
            if zona_tag is not None:
                for st in zona_tag.stripped_strings:
                    zona.append(st)
            
            desc_tag=soup.find('div',attrs={'class': 'adCommentsLanguage expandable'})
            if desc_tag is not None:
                for st in desc_tag.stripped_strings:
                    desc.append(st)
            
            caract_basic_tag=soup.find('div',attrs={'class': 'details-property-feature-one'})
            if caract_basic_tag is not None:
                for st in caract_basic_tag.stripped_strings:
                    caract_basic.append(st)
        
            edificio_tag=soup.find('div',attrs={'class': 'details-property-feature-two'})
            if edificio_tag is not None:           
                for st in edificio_tag.stripped_strings:
                    edificio.append(st)
        
            equipamiento_tag=soup.find('div',attrs={'class': 'details-property-feature-three'})
            if equipamiento_tag is not None:           
                for st in equipamiento_tag.stripped_strings:
                    equipamiento.append(st)
                
            telefono_tag=soup.find('span','phone-btn-number')
            if telefono_tag is not None:   
                for st in telefono_tag.stripped_strings:
                    telefono.append(st)
        
            #contacto_tag=soup.find('div','name')
            contacto_tag=soup.find('div','professional-name')
            #print("CONTACTO {}".format(contacto_tag))
            if contacto_tag is not None:   
                for st in contacto_tag.stripped_strings:
                    contacto.append(st)
                    #print("contacto {}".format(contacto))
        
            data_list.append(fecha_hora + portal + euro + url_sec_list + zona + contacto + telefono + caract + caract_basic + edificio + equipamiento + desc)
            
        except:
            print ('No pasó el captcha del anuncio {}'.format(i))
        
    return data_list
    


