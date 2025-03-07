import os

import requests
from dotenv import load_dotenv

from APIfunc.RR import URL_gen

#Cargamos las credenciales desde el archivo de variables de entorno
load_dotenv()

usuario = os.getenv('T8_USER')
contraseña = os.getenv('T8_PASSWORD')
#Creamos la URL para solicitar la forma de onda
URL = URL_gen('waves','LP_Turbine','MAD31CY005','AM1', 2019, 4, 11, 18, 25, 54)

#hacemos el request con la URL generada con la función URL_gen 
respuesta = requests.get(URL, auth=(usuario, contraseña))


print(respuesta)