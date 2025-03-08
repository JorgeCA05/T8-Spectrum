
import os

import pylab
import requests
from dotenv import load_dotenv

from t8_spectrum.api_functions import decodificador, url_generator

#Cargamos las credenciales desde el archivo de variables de entorno
load_dotenv()

usuario = os.getenv('T8_USER')
contraseña = os.getenv('T8_PASSWORD')
#Creamos la URL para solicitar la forma de onda
URL = url_generator('waves','LP_Turbine','MAD31CY005','AM1', 2019, 4, 11, 18, 25, 54)

#hacemos el request con la URL generada con la función URL_gen 
respuesta = requests.get(URL, auth=(usuario, contraseña))

# Vamos a verificar si la resquest ha sido exitosa
if respuesta.status_code == 200:
    # Guardo el contenido dela forma de onda en un archivo
    with open("archivo_descargado", "wb") as file:
        file.write(respuesta.content)
    print("Descarga completada con éxito.")
else:
    print(f"Error al descargar el archivo: {respuesta.status_code}")

respuesta_json=respuesta.json()

#Extraemos las diferentes partes del archivo json
srate = float(respuesta_json['sample_rate'])
factor = float(respuesta_json.get('factor', 1))
raw = respuesta_json['data']

#Llamamos al decodificador que usará una función u otra dependiendo del formato recibido
#(zint en este caso)
wave = decodificador['zint'](raw)
wave *= factor

#Creamos un array que representará el eje del tiempo
t = pylab.linspace(0, len(wave)/srate, len(wave))

#Mostramos la forma de onda
pylab.plot(t, wave)
pylab.grid(True)
pylab.show()