import os
from datetime import datetime

import requests

from t8_spectrum.api_functions import url_generator

usuario = os.getenv('T8_USER')
contraseña = os.getenv('T8_PASSWORD')
fecha_hora = datetime(2019, 4, 11, 18, 25, 54)


def test_api_authentication():
    url = url_generator('https://lzfs45.mirror.twave.io/lzfs45/rest/','waves',
                         'LP_Turbine', 'MAD31CY005', 'AM1', fecha_hora)
    response = requests.get(url, auth=(usuario, contraseña))
    assert response.status_code == 200, f"Respuesta != a 200: {response.status_code}"