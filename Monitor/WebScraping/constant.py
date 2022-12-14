############ CONSTANTES WEBSCRAPING ############

ENCODING_UTF8 = 'utf-8'

HTTP_STATUS_OK = 200

REQUEST_TIMEOUT = 5

portales = ['pisoscom', 'fotocasa']
#portales = ['fotocasa','idealista','pisoscom']
 
# ALICANTE 
BASE_URL_pisoscom = 'https://www.pisos.com/alquiler/pisos-alicante_alacant/fecharecientedesde-desc/'
BASE_URL_fotocasa = 'https://www.fotocasa.es/es/alquiler/viviendas/alicante-alacant/todas-las-zonas/l?sortType=publicationDate'
#BASE_URL_idealista = 'https://www.idealista.com/alquiler-viviendas/alicante-alacant-alicante/?ordenado-por=fecha-publicacion-desc'

DEFAULT_CITY = 'Alicante / Alacant'


SELENIUM_SLEEP_TIME = 5

POS_FIRST = '1'
POS_SECOND = '2'

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

DIAS = 1
FRECUENCIA = 1
DEFAULT_PAGES = 1

############ CONSTANTES DEPURACIÓN DATASET ############

ciudad_Nominatim = "%s, Alacant / Alicante, l'Alacantí, Alacant / Alicante"

ciudad_google_earth = 'Alicante / Alacant'

provincia = 'Alicante'
pais = 'España'

# Criterios de filtrado del dataset para incluir el anuncio
m2_sup = 200 # m2 útiles máximo
m2_inf = 30  # m2 útiles mínimo
Dorm = 5     # máximo de dormitorios
banyos = 3   # máximo de baños
