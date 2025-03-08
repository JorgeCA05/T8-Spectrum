#############################################    INTRODUCCIÓN     #################################################################

Este proyecto consiste en descargar datos de la forma de onda de un dispositivo T8 virtual a través de la API para calcular su espectro y compararlo con el espectro calculado por el propio T8. 

En el entorno virtual necesitamos 2 librerías, request para solicitar la información a la API y dotenv para hacer uso de variables de entorno ya que para acceder a la API necesitaremos introducir credenciales y obviamente no queremos publicarlas en github(imprescindible crear un archivo .gitignore para evitar que git suba el archivo .env donde se encuentran las credenciales)

############################################  ARCHIVO DE EJECUCIÓN   ###############################################################  

En 'main_script' encontraremos el archivo en el cual se hace uso de todos los paquetes creados para llevar a cabo el proyecto de comparación entre ambos espectros.

Primero se importan las librerías pertinentes comentadas en la introducción, así como las creadas por nosotros para llevar acabo el proceso de generar la URL o decodificar la información devuelta por la API.

Tras obtener la URL comprobamos que la request ha sido exitosa y descargamos el archivo. Lo decodificamos con la funcion 'decodificador' en el módulo api_functions y la representamos.


##############################################     PAQUETES      ###################################################################

En el paquete t8_spectrum se encuentra el módulo api_functions, en el que he creado las funciones para generar las urls necesarias para hacer los request para el host dado (https://lzfs45.mirror.twave.io/lzfs45). Así como para leer los datos devueltos por la API:

url_generator: Sirve sobre todo para tener una función que nos traduzca de UTC a timestamp y de paso te genera el link pasándole el resto de los datos.

decodificador: Contiene tres funciones con el objetivo de leer la información recibida, cada una para uno de los tres tipos de formato en los que podemos solicitar la informacion modificando el link. Podríamos limitarnos a solicitar la información en un único tipo de formato siempre modificando la función 'url_generator' pero de esta forma aportamos sotenibilidad al proyecto a la vez que flexibilidad.