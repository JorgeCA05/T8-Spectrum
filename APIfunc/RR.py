from datetime import UTC, datetime


def URL_gen(dato, nombre, punto_de_med, modo_proc, año, mes, dia, hora, min, seg):
#pasamos de UTC a timestamp ya que lo requiere la URL
    utc_time = datetime(año, mes, dia, hora, min, seg, tzinfo=UTC)
#muy importante aplicar int para que devuelva un numero entero y no un punto flotante
#ya que nos daría una URL errónea
    timestamp = int(utc_time.timestamp())

    URL=f'https://lzfs45.mirror.twave.io/lzfs45/rest/{dato}/{nombre}/{punto_de_med}/{modo_proc}/{timestamp}'

    return URL