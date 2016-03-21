# Mapa de Tasas v2

## Instalación y configuración

La instalación del mapa es similar a la de cualquier proyecto escrito en Django

### Python, virtualenv, pip

El proyecto ha sido desarrollado utilizando Python 3. La compatibilidad con Python 2 no está garantizada, y cualquier despliegue debería realizarse utilizando Python 3.
La mayoría de instalaciones de GNU/Linux incluyen el intérprete de Python por defecto.

Pip permite gestionar las dependencias del proyecto. `virtualenv` permite crear entornos virtuales con una versión del intérprete y un conjunto de dependencias independientes al resto del sistema. En Debian es posible instalar ambas con el comando `sudo apt-get install python3-pip virtualenvwrapper`

Una vez instalados, el comando `virtualenv -p python3 env` genera un directorio con el entorno virtual. Para activarlo, `source env/bin/activate`.

Para instalar las dependencias, ejecutar `pip install -r requirements.txt` con el entorno virtual activado.

También puede ser necesario instalar el paquete `python3-dev` que incluye los archivos de cabecera de Python, requeridos por alguna dependencia.
### Bower

Las dependencias del *frontent* están gestionadas con [Bower](http://bower.io/). Para instalarlo, es necesario instalar el gestor de paquetes de node.js, [npm](https://www.npmjs.com/)

Instalación de npm:

```
curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
sudo apt-get install -y nodejs
```

Instalación de Bower:

```
npm install bower
```

Este comando creará un directorio en la raíz del proyecto con el paquete. Ejecutando `./node_modules/bower/bin/bower` se instalarán los paquetes necesarios.

### Django

Antes de arrancar la aplicación es necesario crear la base de datos, recopilar los datos estáticos, etcétera.

#### settings.py

La mayoría de los ajustes de Django residen en el fichero `tasasrest/settings.py`. Por lo generar no es necesario alterar este fichero. En su lugar, sobreescribiremos los ajustes en otro fichero.

#### local_settings.py

Este fichero se importa al final de `settings.py`, por lo que cualquier previamente definida será sobreescrita por el valor dado en este fichero. En general, será necesario cambiar los ajustes de la base de datos, el modo de desarrollo y la clave secreta:

Ejemplo:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tasasbbdd',
        'USER': 'youruser',
        'PASSWORD': 'yourpassword'
    }
}
DEBUG = False # Importante, el modo de depuración incluye información sensible que no debe ser expuesta
SECRET_KEY = 'mykey'
```

**Importante**: la clave secreta se utiliza en [partes sensibles de la aplicación](http://stackoverflow.com/a/15383766/2628463). Debe mantenerse en secreto.
La clave es una combinación aleatoria de caracteres. Con [este *script*](https://gist.github.com/mattseymour/9205591) se puede generar fácilmente.

Una vez definidos los ajustes, el proyecto puede ser puesto en marcha:

```
source env/bin/activate
python manage.py migrate # Creación de la base de datos y definición de tablas
python manage.py collectstatic # Copia los ficheros estáticos de todas las aplicaciones a un directorio común
python manage.py test # Ejecuta los tests unitarios

python manage.py createsuperuser # Crea un superusuario
python manage.py check --deploy # Comprueba que los ajustes definidos son apropiados para una configuración de despliegue

# Opcional: Carga de datos de la versión inicial del mapa
python manage.py importar <unis.json> <imagenes>
```

Antes de pasar a la configuración del despliegue, es posible verificar el comportamiento del servidor ejecutando un servidor integrado:

```
python manage.py runserver 0.0.0.0:8000
```


## Despliegue

El despliegue de la aplicación depende del entorno en el que se desee instalar. En la documentación de [Django](https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/modwsgi/) hay una lista de opciones.
En nuestro caso, la aplicación será desplegada en un servidor nginx con Gunicorn y supervisord.

### Instalación de dependencias

Los siguientes paquetes son necesarios:

* [nginx](http://nginx.org/)
* [supervisord](http://supervisord.org/)
* [Gunicorn](http://gunicorn.org/)

####  Instalación de Gunicorn:

Gunicorn es un paquete de python, por lo que es instalado en el propio entorno virtual:

```
source env/bin/activate
pip install gunicorn
```

Gunicorn puede ser ejecutado con el comando `tasasrest.wsgi:application --bind dominio.com:8000` para comprobar que funciona de forma correcta. Sin embargo, algo más de configuración es necesaria a la hora de utilizarlo en un entorno de producción:

Ejemplo de archivo `gunicorn_start` de configuración:

```
#!/bin/bash

NAME="mapa-tasas-backend"
DJANGODIR=<ruta>/mapa-tasas-backend # Ruta raíz del proyecto de Django
SOCKFILE=<ruta>/mapa-tasas-backend/run/gunicorn.sock # Ruta donde el fichero socket será creado
USER=www-data # Usuario y grupo de nginx
GROUP=www-data
NUM_WORKERS=3 # Número de procesos a crear que ejecutarán la aplicación de forma concurrente
DJANGO_SETTINGS_MODULE=tasasrest.settings # Módulo de ajustes
DJANGO_WSGI_MODULE=tasasrest.wgsi # Módulo de  la interfaz WGSI

echo "Arrancando $NAME as `whoami`"

cd $DJANGODIR
source env/bin/activate

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Creación del directorio de ejecución
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec env/bin/gunicorn tasasrest.wsgi:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER--group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug 
  --log-file=

```

Marcar el archivo como ejecutable con `chmod +x gunicorn_start`

El número de procesos puede ser modificado, generalmente siguiendo la regla `2 * num_cpus + 1`. El parámetro NAME idenficará el nombre del proceso, puede ser necesario instalar el paquete `setproctitle` de Python, de nuevo mediante `pip install setproctitle`.

#### supervisord

supervisord es una herramienta de monitorización de trabajos, que se encarga de administrar logs, reiniciar servicios que han fallado, etc. Para instalarlo:

```
sudo apt-get install supervisor
```

Archivo de configuración a alojar en /etc/supervisor/conf.d:

```
[program:tasasrest]
command = <ruta a >/gunicorn_start ; Comando de arranque
user = www-data ; Usuario a ejecutar el comando
stdout = <ruta al proyecto>/logs/gunicorn_supervisor.log ; Directorio de logs
redirect_stderr = true
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8 
```

Nota: el directorio de logs no será creado automáticamente

Una vez creado el fichero, es necesario carcarlo en supervisor:

```
sudo supervisorctl reread
sudo supervisorctl update
```


### Nginx

Por último, es necesario dar acceso a la aplicación desde el exterior.

Archivo de ejemplo de nginx:


```
upstream mapa_tasas_backend_app_server{
	server unix:<ruta a>gunicorn.sock fail_timeout=0;
}

server {
	listen 80;
	server_name tasas.dominio.net;
	client_max_body_size 50M;
	access_log <ruta a>/logs/nginx-access.log;
	error_log <ruta a>/logs/nginx-error.log;
	
	location /static/ {
		autoindex on;

		alias <ruta a proyecto>/static/;
	}	
	location /media/ {
		autoindex on;
		alias <ruta a proyecto>/media/;
	}


	location / {
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header Host $http_host;
		proxy_redirect off;
		if (!-f $request_filename) {
            		proxy_pass http://mapa_tasas_backend_app_server;
            		break;
        	}
	}
	# Error pages
    #error_page 500 502 503 504 /500.html;
    #location = /500.html {
    #    root /webapps/hello_django/static/;
    #}
}

```

Notas:

* Los directorios `/media/` y `/static/` contienen únicamente ficheros estáticos. Definiéndolos directamente en nginx evita que estas peticiones sean procesadas (de forma menos eficiente) por Django.
* El usuario que ejecute la aplicación debe tener permisos de escritura en la carpeta `/media/`.

Una vez recargado nginx con `nginx -s reload`, la aplicación estará lista para funcionar.

Créditos: http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/
