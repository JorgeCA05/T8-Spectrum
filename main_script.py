import os

import matplotlib.pyplot as plt
import numpy as np
import pylab
import requests
from dotenv import load_dotenv

from t8_spectrum.api_functions import decodificador, url_generator

# Cargamos las credenciales desde el archivo de variables de entorno
load_dotenv()
usuario = os.getenv('T8_USER')
contraseña = os.getenv('T8_PASSWORD')
# Creamos la URL para solicitar la forma de onda
URL_forma_de_onda = url_generator('waves', 'LP_Turbine', 'MAD31CY005', 'AM1', 2019, 4,
                                   11, 18, 25, 54)
# Hacemos el request con la URL generada con la función url_generator
respuesta = requests.get(URL_forma_de_onda, auth=(usuario, contraseña))
# Verificamos si la request ha sido exitosa
if respuesta.status_code == 200:
    with open("forma_de_onda", "wb") as file:
        file.write(respuesta.content)
    print("Descarga completada con éxito.")
else:
    print(f"Error al descargar el archivo: {respuesta.status_code}")



respuesta_json = respuesta.json()
# Extraemos las diferentes partes del archivo json
srate = float(respuesta_json['sample_rate'])
factor = float(respuesta_json.get('factor', 1))
raw = respuesta_json['data']
# Llamamos al decodificador que usará una función u otra dependiendo del formato 
# recibido (zint en este caso)
wave = decodificador['zint'](raw)
wave *= 0.0000238
# Creamos un array que representará el eje del tiempo
t = pylab.linspace(0, len(wave) / srate, len(wave))
# Mostramos la forma de onda
pylab.plot(t, wave)
pylab.title('Forma de onda')
pylab.grid(True)
pylab.show()



# Creamos la URL para solicitar el espectro generado por el T8
URL_espectro_t8 = url_generator('spectra', 'LP_Turbine', 'MAD31CY005', 'AM1', 2019, 4,
                                 11, 18, 25, 54)
# Hacemos el request con la URL generada con la función url_generator
respuesta = requests.get(URL_espectro_t8, auth=(usuario, contraseña))
# Verificamos si la request ha sido exitosa
if respuesta.status_code == 200:
    with open("T8_spectrum", "wb") as file:
        file.write(respuesta.content)
    print("Descarga completada con éxito.")
else:
    print(f"Error al descargar el archivo: {respuesta.status_code}")



respuesta_json = respuesta.json()
# Extraemos los campos del json
fmin = respuesta_json.get('min_freq', 0)
fmax = respuesta_json['max_freq']
factor = respuesta_json['factor']
raw = respuesta_json['data']
# Llamamos al decodificador que usará una función u otra dependiendo del formato
# recibido (zint en este caso)
sp = decodificador['zint'](raw)
sp *= factor
# Creamos un array para el eje de la frecuencia
freq = pylab.linspace(fmin, fmax, len(sp))
# Filtrar las frecuencias entre 50 Hz y 2000 Hz
mascara = (freq >= 50) & (freq <= 2000)
freq_t8_filtrada = freq[mascara]
sp_filtrada =sp[mascara]
# Mostramos el espectro creado por el T8
pylab.plot(freq_t8_filtrada, sp_filtrada)
pylab.title('Espectro T8 (50-2000 Hz)')
pylab.grid(True)
pylab.show()



# Uso de la transformada de Fourier para calcular el espectro a partir de la 
# forma de onda
# Aplicar una ventana Hanning a la forma de onda para suavizar los bordes
ventana = np.hanning(len(wave))
wave_vent = wave * ventana


# Zero-padding para mejorar la resolución del espectro artificialmente
n = len(wave_vent)
n_padeado = 2**int(np.ceil(np.log2(n)))  # Aseguramos que sea una potencia de 2
wave_padeado = np.pad(wave_vent, (0, n_padeado - n), 'constant')


# Realizar la FFT
fourier_wave = np.fft.fft(wave_padeado)
long_wave = len(fourier_wave)
mag_spectro= np.abs(fourier_wave)
# Creamos un vector de frecuencias adecuado para el espectro
vector_frecs = np.fft.fftfreq(long_wave, 1 / srate)
# Filtrar las frecuencias entre 50 Hz y 2000 Hz
mascara = (vector_frecs >= 50) & (vector_frecs <= 2000)
vector_frecs_filtrado = vector_frecs[mascara]
mag_spectro_filtrado = mag_spectro[mascara]
# Representar el espectro creado por nosotros
plt.figure(figsize=(10, 6))
plt.plot(vector_frecs_filtrado, mag_spectro_filtrado)
plt.title('Espectro propio (50-2000 Hz)')
plt.xlabel('Freq. (Hz)')
plt.ylabel('Displacement µm RMS')
plt.grid()
plt.show()



# Representar los dos espectros superpuestos
plt.figure(figsize=(10, 6))
plt.plot(vector_frecs_filtrado, mag_spectro_filtrado, label='Espectro propio')
plt.plot(freq_t8_filtrada, sp_filtrada, label='Espectro T8')
plt.title('Comparación de Espectros (50-2000 Hz)')
plt.xlabel('Freq. (Hz)')
plt.ylabel('Displacement µm RMS')
plt.legend()
plt.grid()
plt.show()
