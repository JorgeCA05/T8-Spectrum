import os

import requests

from t8_spectrum.api_functions import url_generator

usuario = os.getenv('T8_USER')
contraseña = os.getenv('T8_PASSWORD')

def test_api_authentication():
    url = url_generator('waves', 'LP_Turbine', 'MAD31CY005', 'AM1', 2019, 4,
                         11, 18, 25, 54)
    response = requests.get(url, auth=(usuario, contraseña))
    assert response.status_code == 200, f"Respuesta != a 200: {response.status_code}"