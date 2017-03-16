# MapaTasas

Versión en producción del Mapa de Tasas. Proyecto solo de mantenimiento de datos del JSON de Universidades.

## Instalación

El mapa ha sido probado en Python 3.5. Para instalar el proyecto:

```
## Clonar el repositorio
git clone <url>
Crear un entorno virtual:
virtualenv -p python3 env

## Activar el entorno virtual
source env/bin/activate
Instalar dependencias
pip install -r requirements.txt

## Instalar dependencias estáticas
bower install

## Crear base de datos:
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

También se puede hacer con Docker mediante dos comandos.

```bash
$ git clone https://github.com/RITSI/MapaTasas && cd MapaTasas
$ docker build -t mapa-tasas .
```

Si queremos poner en marcha el servidor web, lo hacemos con:

```
docker run -it -d --rm -p 8000:8000 mapa-tasas python3 manage.py runserver 0.0.0.0:8000
```

## Scripts

El paquete incluye varios scripts de interés:

### raw-map/makemap.sh

Crea el archivo topojson con los datos geográficos del mapa de España adaptados para el mapa (Canarias desplazadas)
 
## python manage.py importar

A partir de un fichero ``unis.json`` y un directorio de imágenes, carga los datos de las universidades en la base de datos. Este *script* está pensado para facilitar el desarrollo en paralelo de la versión anterior del proyecto

## python manage.py rendervariations

En caso de que se hayan importado imágenes con el comando `importar`, es necesario generar las miniaturas de las imágenes añadidas. Ejecutar:

`python manage.py rendervariations 'tasas.universidad.logo' [--replace]`

## Tests unitarios

El paquete incluye tests unitarios para la lógica del *backend*. Para ejecutar:

`python manage.py test`

En el directorio `cover` albergará un informe sobre la cobertura de los tests
