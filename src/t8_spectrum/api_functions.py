from base64 import b64decode
from datetime import UTC, datetime
from struct import unpack
from zlib import decompress

import numpy as np


def url_generator(dato, nombre, punto_de_med, modo_proc, año, mes, dia, hora, min, seg):
#pasamos de UTC a timestamp ya que lo requiere la URL
    utc_time = datetime(año, mes, dia, hora, min, seg, tzinfo=UTC)
#muy importante aplicar int para que devuelva un numero entero y no un punto flotante
#ya que nos daría una URL errónea
    timestamp = int(utc_time.timestamp())

    URL=f'https://lzfs45.mirror.twave.io/lzfs45/rest/{dato}/{nombre}/{punto_de_med}/{modo_proc}/{timestamp}'

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