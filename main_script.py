
import os

import matplotlib.pyplot as plt
import numpy as np
import pylab
import requests
from dotenv import load_dotenv

from t8_spectrum.api_functions import decodificador, filtrar_ski_slope, url_generator

#Cargamos las credenciales desde el archivo de variables de entorno
load_dotenv()

usuario = os.getenv('T8_USER')
contraseña = os.getenv('T8_PASSWORD')
#Creamos la URL para solicitar la forma de onda
URL_forma_de_onda=url_generator('waves','LP_Turbine','MAD31CY005','AM1', 2019, 4, 11,
                                 18, 25, 54)

#hacemos el request con la URL generada con la función url_generator
respuesta = requests.get(URL_forma_de_onda, auth=(usuario, contraseña))

# Vamos a verificar si la resquest ha sido exitosa
if respuesta.status_code == 200:
    # Guardo el contenido dela forma de onda en un archivo
    with open("forma_de_onda", "wb") as file:
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
pylab.title('Forma de onda')
pylab.grid(True)
pylab.show()




#Creamos la URL para solicitar el espectro generado por el T8
URL_espectro_t8 = url_generator('spectra','LP_Turbine','MAD31CY005','AM1', 2019, 4, 11,
                                 18, 25, 54)

#hacemos el request con la URL generada con la función url_generator
respuesta = requests.get(URL_espectro_t8, auth=(usuario, contraseña))

# Vamos a verificar si la resquest ha sido exitosa
if respuesta.status_code == 200:
    # Guardo el contenido del espectro del T8 en un archivo
    with open("T8_spectrum", "wb") as file:
        file.write(respuesta.content)
    print("Descarga completada con éxito.")
else:
    print(f"Error al descargar el archivo: {respuesta.status_code}")




respuesta_json=respuesta.json()

# extract json fields
fmin = respuesta_json.get('min_freq', 0)
fmax = respuesta_json['max_freq']
factor = respuesta_json['factor']
raw = respuesta_json['data']

#Llamamos al decodificador que usará una función u otra dependiendo del formato recibido
#(zint en este caso)
sp = decodificador['zint'](raw)
sp *= factor

# Aplicar el filtro al espectro
freq_corte = 100.0  # Frecuencia de corte en Hz 
sp_filtrado = filtrar_ski_slope(sp, freq_corte, srate)

#Creamos un array para el eje de la frecuencia
freq = pylab.linspace(fmin, fmax, len(sp_filtrado))

#mostramos el espectro creado por el T8
pylab.plot(freq, sp_filtrado)
pylab.title('Espectro T8')
pylab.grid(True)
pylab.show()






#Voy ahora a hacer uso de la transformada de fourier para calcular el espectro a 
#partir de la forma de onda:

#Filtro la forma de onda antes de realizar el proceso para evitar problemas
#Esto es importante ya que si no daría errores
wave_filtrada=filtrar_ski_slope(wave, freq_corte, srate)

fourier_wave = np.fft.fft(wave_filtrada)
long_wave= len(fourier_wave)
mag_spectro_filtrado = np.abs(fourier_wave) 
#Creamos un vector de frecuencias adecuado para nuestro espectro 
vector_frecs = np.fft.fftfreq(long_wave, 1/srate)

#Representar el espectro creado por nosotros:
# Graficar el espectro de amplitud
plt.figure(figsize=(10, 6))
#Solo representamos la parte positiva ya que la negativa no aporta nada nuevo
plt.plot(vector_frecs[:long_wave//2], mag_spectro_filtrado[:long_wave//2])  
plt.title('Espectro propio')
plt.xlabel('Freq. (Hz)')
plt.ylabel('Displacement µm RMS')
plt.grid()
plt.show()




#representar los dos espectros superpuestos
plt.figure(figsize=(10, 6))
plt.plot(vector_frecs[:long_wave // 2], mag_spectro_filtrado[:long_wave // 2],
          label='Espectro propio')  
plt.plot(freq, sp_filtrado, label='Espectro T8')
plt.title('Comparación de Espectros')
plt.xlabel('Freq. (Hz)')
plt.ylabel('Displacement µm RMS')
plt.legend()
plt.grid()
plt.show()