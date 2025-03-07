Este proyecto consiste en descargar datos de la forma de onda de un dispositivo T8 virtual a través de la API para calcular su espectro y compararlo con el espectro calculado por el propio T8. 

En el entorno virtual necesitamos 2 librerías, request para solicitar la información a la API y dotenv para hacer uso de variables de entorno ya que para acceder a la API necesitaremos introducir credenciales y obviamente no queremos publicarlas en github(imprescindible crear un archivo .gitignore para evitar que git suba el archivo .env donde se encuentran las credenciales)

En el paquete APIfunc se encuentra el módulo RR, en el que he creado una función para generar las urls necesarias para hacer los request para el host dado (https://lzfs45.mirror.twave.io/lzfs45)