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
En esta primera fase se realiza el ***WebScraping***, para ello, en primer lugar se realiza una búsqueda de viviendas en alquiler en los portales inmobiliarios de interés, añadiendo posteriormente la url resultante como una constante en el script *constant.py*. Este script se ha configurado para la extracción de la información de los anuncios de vivienda en alquiler de la ciudad de Alicante. En el archivo *constant.py* también se puede configurar el número de días consecutivos que queremos que se realice el ***WebScraping***, así como, la frecuencia de las búsquedas o el número de páginas que queremos que se visite en cada raspado. 

La finalidad de este proceso es obtener el número suficiente de información de anuncios de alquiler para poder realizar nutrir a un cuadro de mando y que la información resultante sea de calidad. Se puede establecer cualquier periodicidad en la actualización del cuadro de mando siempre y cuando se hayan raspado anuncios suficientes para poder elaborar un informe de calidad. En nuestro caso por el tamaño de la ciudad de Alicante hemos establecido una periodicidad de 3 meses, por lo cual se realizada durante 90 días consecutivos el proceso de raspado anterior. 

El modo de ejecución es el siguiente:
- Estando en la carpeta WebScraping, ejecutar el fichero handler.py
```sh
~/Monitorizacion_Alquileres/Monitor/WebScraping$ python handler.py
```
Esto abrirá una ventana de Google Chrome y a través de Selenium se ejecutarán acciones automatizadas.

#### Fichero de salida
Después de una ejecución correcta se generará un xlsx por búsqueda con los resultados en:

*Monitorizacion_Alquileres/Monitor/WebScraping/pisoscom/2022/T4/anuncios_pisoscom 2022.12.04_12.16.52.xlsx*

*Monitorizacion_Alquileres/Monitor/WebScraping/fotocasa/2022/T4/anuncios_fotocasa 2022.12.04_12.16.52.xlsx*

*Monitorizacion_Alquileres/Monitor/WebScraping/particulares/2022/T4/anuncios_particulares 2022.12.04_12.16.52.xlsx*

### Depuración
Una vez terminado el trimestre pasamos a al tratamiento de los datos obtenidos en el *WebScraping*

El modo de ejecución es el siguiente:
- Estando en la carpeta WebScraping, ejecutar el fichero handler.py









