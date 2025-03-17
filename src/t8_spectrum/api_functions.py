from base64 import b64decode
from datetime import UTC
from struct import unpack
from zlib import decompress

import numpy as np
from scipy.signal import butter, filtfilt


def url_generator(direccion, dato, nombre, punto_de_med, modo_proc, fecha_hora):
    # Convertimos la fecha y hora a timestamp
    utc_time = fecha_hora.replace(tzinfo=UTC)
    timestamp = int(utc_time.timestamp())

    URL = f'{direccion}{dato}/{nombre}/{punto_de_med}/{modo_proc}/{timestamp}'

    return URL


def zint_to_float(raw):
    d = decompress(b64decode(raw.encode()))
    return np.array([unpack('h', d[i*2:(i+1)*2])[0] for i in range(int(len(d)/2))], 
                    dtype='f')

def zlib_to_float(raw):
    d = decompress(b64decode(raw.encode()))
    return np.array([unpack('f', d[i*4:(i+1)*4])[0] for i in range(int(len(d)/4))], 
                    dtype='f')

def b64_to_float(raw):
    return np.fromstring(b64decode(raw.encode()), dtype='f')

decodificador = {
    'zint': zint_to_float,
    'zlib': zlib_to_float,
    'b64': b64_to_float
}

#Función para filtrar ski-slope
#Basicamente elimina las la informacion de frecuencias inferiores a 'filtro'
def filtrar_ski_slope(base, filtro, f_muestreo, orden=5):
    nyquist = 0.5 * f_muestreo
    frec_corte = filtro / nyquist
    b, a = butter(orden, frec_corte, btype='high', analog=False)
    y = filtfilt(b, a, base)
    return y