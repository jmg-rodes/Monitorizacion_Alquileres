# Monitorizacion_Alquileres
Monitorización precios de alquiler para áreas geográficas municipales determinadas. Caso de la ciudad de Alicante.

## Requisitos

| Tecnología | URL |
| ------ | ------ |
| Python 3 | [Enlace](https://www.python.org/downloads/) |
| Google Chrome (v108) | [Enlace](https://www.google.com/intl/es_es/chrome/) |
| Driver de Selenium (v108)| [Enlace](https://chromedriver.chromium.org/downloads/) |
| Nominatin (vxx) | [Enlace](https://nominatim.openstreetmap.org/ui/search.html) |

## Instalación
- Descargar proyecto.
- Exportar a la variable de entorno PYTHONPATH la ruta de la carpeta Monitorizacion_Alquileres.
- Instalar las dependencias de Python contenidas en el fichero requirements.txt, ya sea a mano o a través de:

```sh
~/Monitorizacion_Alquileres/Monitor$ pip3 install -r requirements.txt
```
## Ejecución
El proyecto de monitorización de rentas de alquiler se compone de tres fases: EXTRACCIÓN, DEPURACIÓN y VISUALIZACIÓN.

### Extracción
En esta primera fase se realiza el ***WebScraping***, para ello, en primer lugar se hace una búsqueda de viviendas en alquiler en los portales inmobiliarios de interés, añadiendo posteriormente la url resultante como una constante en el script *constant.py*. Este script se ha configurado para la extracción de la información de los anuncios de vivienda en alquiler de la ciudad de Alicante. En el archivo *constant.py* también se puede configurar el número de días consecutivos que queremos que se realice el *WebScraping*, así como, la frecuencia diaria de las búsquedas o el número de páginas que queremos que se visite en cada raspado. 

La finalidad de este proceso es obtener el número suficiente de información de los anuncios de alquiler para poder nutrir a un cuadro de mando y que la información resultante sea representativa del área en estudio. Se puede establecer cualquier periodicidad en la actualización del cuadro de mando siempre y cuando se hayan raspado anuncios suficientes para poder elaborar un informe de calidad. En nuestro caso por el tamaño de la ciudad de Alicante hemos establecido una periodicidad de 3 meses, por lo cual se realizada durante 92 días consecutivos el proceso de raspado anterior.

Otro producto que se obtiene es el archivo diario con el filtrado de los **anuncios publicados por propietarios particulares**.

El modo de ejecución es el siguiente:
- En la carpeta *WebScraping* abrir el script *constant.py* y ajustar los parámetros (NOTA: Está ya configurado por defecto para la ciudad de Alicante)
- Estando en la carpeta *WebScraping*, ejecutar el fichero *handler.py*.
```sh
~/Monitorizacion_Alquileres/Monitor/WebScraping$ python handler.py
```
Esto abrirá una ventana de Google Chrome y a través de Selenium se ejecutarán acciones automatizadas.

#### Fichero de salida
Después de una ejecución correcta se generará un xlsx por búsqueda guardando los resultados en:

*Monitorizacion_Alquileres/Monitor/WebScraping/pisoscom/2022/T4/anuncios_pisoscom 2022.12.04_12.16.52.xlsx*

*Monitorizacion_Alquileres/Monitor/WebScraping/fotocasa/2022/T4/anuncios_fotocasa 2022.12.04_12.16.52.xlsx*

*Monitorizacion_Alquileres/Monitor/WebScraping/particulares/fotocasa/2022/T4/anuncios_particulares_pisoscom 2022.12.04_12.16.52.xlsx*

*Monitorizacion_Alquileres/Monitor/WebScraping/particulares/pisoscom/2022/T4/anuncios_particulares_fotocasa 2022.12.04_12.16.52.xlsx*

El archivo con los **anuncios de particulares** de todos los portales en estudio se guarda en la siguiente ruta:

*Monitorizacion_Alquileres/Monitor/Resultados/particulares/anuncios_particulares 2022.12.04_12.16.52.xlsx*


### Depuración
Una vez terminado el trimestre pasamos al tratamiento de los datos obtenidos en el *WebScraping*, para ello ejecutamos el script *Dataset.py* cuyo proceso de ejecución se describe a continuación:

- **Normalización de los archivos**. Diariamente se guarda el resultado del raspado anterior para cada portal en la carpeta del trimestre correspondiente, al final del trimestre se unen estos archivos dentro de cada portal y procede a su estandarización. No todos los anuncios publicados en una misma web tienen la misma cantidad de características (variables), teniendo distintas columnas cada registro del archivo de datos, por ello hay que insertar y eliminar columnas y registros para que quede perfectamente tabulado y se tenga cada tipo de dato en su columna correspondiente. Este proceso hay que realizarlo de forma independiente para cada uno de los portales raspados anteriormente, ya que tienen estructuras diferentes.

- **Eliminación de duplicados dentro de cada web**. Una vez hemos unido y normalizado todos los registros de los anuncios del trimestre para un portal, se procede a eliminar los duplicados dentro del portal, para cada uno de los portales analizados.

- **Unión de los conjuntos de datos**. En este punto se unen los archivos resultantes del proceso anterior en un único conjunto de datos.

- **Eliminación de duplicados entre webs**. Manteniendo intacto el conjunto de datos de la web con mayor número de registros se eliminan los demás existentes en las otras webs que coincidan con estos.

- **Filtrado por los criterios de interés**. Una vez se tiene el conjunto de datos ordenado y depurado filtramos por los criterios de interés, estos se establecen en el script *constant_debug* que para nuestro caso son: viviendas comprendidas entre 35 y 200 m2 útilies, de no más de 5 dormitorios y 3 baños.

- **Extracción de las direcciones**. En este punto ya se tienen todos los registros de interés, ahora se extraen las direcciones para su geolocalización.

- **Geolocalización de las direcciones**. Para llevar a cabo este proceso existen distintas herramientas y API’s, en este caso se utiliza Nomiation por ser gratuita, con Google Earth o la API de Google V8 se obtienen mejores resultados, pero para la primera el proceso no se puede automatizar y la segunda es de pago.

- **Asignación de coordenadas a las zonas**. Con las viviendas geolocalizadas se aplica el algoritmo punto-polígono para la asignación de estas a sus zonas correspondientes.

- **Eliminación de duplicados dentro de la zona**. Con las viviendas asignadas a la zona se vuelve a realizar el proceso de eliminación de duplicados esta vez dentro de cada zona.

- **Eliminación de *outliers***. Para la eliminación de los valores extremos en primer lugar se aplica el algoritmo KNN, sobre todo el conjunto, a continuación se eliminan los valores que disten por exceso o defecto más de 1,96 desviaciones típicas de la media dentro de cada zona.

- **Valores perdídos (NA)**. El conjuto de datos va a ser agrupado en el proceso siguiente obteniendo medidas de tendencia central y de dispersión, por lo que los valores faltantes se sustituyen por las medias de la variable.

- **Agrupación de los datos**. Para un menor consumo de recursos se agrupa el conjunto de datos por zonas obteniendo los estadísticos de interés de cada zona, así como para intervalos de rentas y dormitorios.

- **Acumulación de datos trimestrales**. Una vez se tienen los datos del periodo, para este caso el trimestre, los unimos con el conjunto de datos que contiene los trimestres anteriores desde que se realiza el estudio y se guardan en la carpeta *CuadroMando* para que sean leídos por el cuadro de mando realizado en Tableau.

El modo de ejecución es el siguiente:
- En la carpeta *Debug* abrir el script *constant_debug.py* y ajustar los parámetros (NOTA: Está ya configurado por defecto con los parámetros de interés para el estudio).
- Estando en la carpeta *Debug*, ejecutar el fichero *Dataset.py*.
```sh
~/Monitorizacion_Alquileres/Monitor/Debugg$ python Dataset.py
```
Esto realizará automáticamente todas las operaciones enumeradas anteriormente.

#### Fichero de salida
Después de una ejecución correcta se generará un xlsx en:

*Monitorizacion_Alquileres/Monitor/Resultados/CuadroMando/data.xlsx* 

que es leido por el cuadro de mando realizado en *tableau*.

### Visualización
Por último, una vez depurado y agregado el conjunto de datos, este se útiliza para crear una visualización mediante un cuadro de mando construido en *tableau*. Este se puede visualizar en el siguiente enlace:

https://public.tableau.com/app/profile/jos.manuel6318/viz/Monitorizacinrentadealquiler/Alicante?publish=yes








