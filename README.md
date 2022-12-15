# Monitorizacion_Alquileres
Monitorización precios de alquiler para áreas geográficas municipales determinadas. Caso de la ciudad de Alicante.

## Requisitos

| Tecnología | URL |
| ------ | ------ |
| Python 3 | [Enlace](https://www.python.org/downloads/) |
| Google Chrome (v108) | [Enlace](https://www.google.com/intl/es_es/chrome/) |
| Driver de Selenium (v108)| [Enlace](https://chromedriver.chromium.org/downloads/) |

## Instalación
- Descargar proyecto
- Exportar a la variable de entorno PYTHONPATH la ruta de la carpeta Monitorizacion_Alquileres
- Instalar las dependencias de Python contenidas en el fichero requirements.txt, ya sea a mano o a través de:

```sh
~/Monitorizacion_Alquileres/Monitor$ pip3 install -r requirements.txt
```
## Ejecución
El proyecto de monitorización de rentas de alquiler se compone de tres fases: EXTRACCIÓN, DEPURACIÓN y VISUALIZACIÓN

### Extracción
En esta primera fase se realiza el ***WebScraping***, para ello, en primer lugar hemos realizado una búsqueda de viviendas en alquiler en los portales inmobiliarios de interés añadiendo la url resultante como una constante en el script *constant.py*, este se ha configurado para la extracción de la información de los anuncios de vivienda en alquiler de la ciudad de Alicante. En el archivo *constant.py* también se puede configurar el número de días consecutivos que queremos que se realice el ***WebScraping***, así como, la frecuencia de las búsquedas o el número de páginas que queremos que se visite en cada raspado. 

El modo de ejecución es el siguiente:
- Estando en la carpeta WebScraping, ejecutar el fichero handler.py
```sh
~/HouseScraper/src/scraper$ python handler.py
```
Esto abrirá una ventana de Google Chrome y a través de Selenium se ejecutarán acciones automatizadas.

### Fichero de salida
Después de una ejecución correcta se generará un csv con los resultados en **HouseScraper/src/resources/data.csv**
