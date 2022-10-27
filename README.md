# Monitorizacion_Alquileres
Monitorización precios de alquiler para áreas geográficas determinadas

### Requisitos

| Tecnología | URL |
| ------ | ------ |
| Python 3 | [Enlace](https://www.python.org/downloads/) |
| Google Chrome (v86) | [Enlace](https://www.google.com/intl/es_es/chrome/) |
| Driver de Selenium (v86)| [Enlace](https://chromedriver.chromium.org/downloads/) |

### Instalación y ejecución
- Exportar a la variable de entorno PYTHONPATH la ruta de la carpeta HouseScraper
- Instalar las dependencias de Python contenidas en el fichero requirements.txt, ya sea a mano o a través de:

```sh
~/HouseScraper/src$ pip3 install -r requirements.txt
```
- Estando en la carpeta scraper, ejecutar el fichero handler.py
```sh
~/HouseScraper/src/scraper$ python handler.py
```
Esto abrirá una ventana de Google Chrome y a través de Selenium se ejecutarán acciones automatizadas.

### Fichero de salida
Después de una ejecución correcta se generará un csv con los resultados en **HouseScraper/src/resources/data.csv**
