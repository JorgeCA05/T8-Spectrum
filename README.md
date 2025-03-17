# Proyecto T8 Spectrum

## Introducción

Este proyecto tiene como objetivo descargar datos de la forma de onda de un dispositivo **T8 virtual** a través de su API, calcular su espectro y compararlo con el espectro calculado por el propio T8.

Para el entorno virtual, utilizamos las siguientes librerías:

- **requests**: Para realizar solicitudes a la API.
- **dotenv**: Para manejar variables de entorno y evitar exponer credenciales sensibles en el código.
- **numpy** y **matplotlib**: Para procesar los datos y visualizar los espectros.

> **Nota:** Es imprescindible crear un archivo `.gitignore` para evitar que Git suba el archivo `.env`, donde se almacenan las credenciales.

---

## Archivo de ejecución

El script principal se encuentra en `main_script.py`, donde se utilizan todos los paquetes creados para llevar a cabo la comparación entre los espectros.

### Flujo de trabajo:

1. Importamos las librerías necesarias (tanto externas como internas del proyecto).
2. Cargamos las credenciales desde variables de entorno con `dotenv`.
3. Generamos las URLs necesarias para las solicitudes API mediante `url_generator`.
4. Verificamos que las respuestas de la API sean exitosas y descargamos los datos.
5. Decodificamos la información usando la función `decodificador` del módulo `api_functions`.
6. Representamos la forma de onda descargada.
7. Aplicamos un filtro de frecuencias entre **50 Hz y 2000 Hz**.
8. Calculamos el espectro mediante la **Transformada de Fourier (FFT)** con ventana de Hanning y zero-padding.
9. Comparamos ambos espectros en una misma gráfica.

> **Nota:** Los archivos descargados deben incluirse en el `.gitignore` para evitar que sean subidos al repositorio.

---

## Paquetes

El código se encuentra estructurado dentro del paquete `t8_spectrum`, que contiene distintos módulos para la gestión y procesamiento de datos:

### `api_functions.py`

- **`url_generator`**:
  - Convierte **UTC** a **timestamp**.
  - Genera automáticamente el enlace de solicitud a la API.
- **`decodificador`**:
  - Contiene tres funciones para leer la información en los distintos formatos disponibles en la API.
  - Permite flexibilidad en el procesamiento de datos sin limitarse a un único formato.
- **`filtrar_ski_slope`** *(en desuso)*:
  - Filtro de paso alto para eliminar el ski-slope.
  - Reemplazado por un método de truncamiento para evitar modificaciones no deseadas en la onda.

---

## Requisitos e instalación

Para ejecutar el proyecto, asegúrate de tener Python y las dependencias necesarias instaladas.

```bash
pip install -r requirements.txt
```

Además, crea un archivo `.env` con las credenciales necesarias para acceder a la API:

```
T8_USER=tu_usuario
T8_PASSWORD=tu_contraseña
```
## Mejoras futuras

Algunas mejoras que se pueden implementar en el futuro:

- Agregar manejo de excepciones para errores en la solicitud de la API de manera aislada a internet usando pytest.
- Obtener el factor de conversión para la wave desde la API para evitar cambios de magnitud y no buscarlo manualmente 'EN PROCESO'
- Disminuir el número de inputs para generar las url 'HECHO'

