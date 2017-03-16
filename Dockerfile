FROM ubuntu:16.10

ENV HOME /root
ENV SECRET_KEY no-secret-key #Set a secure Django secret key for production!

WORKDIR $HOME
COPY . $HOME

## ENVRIOMENT DEPENDENCIES
RUN apt-get update && \
    apt-get install -y -q libjpeg8-dev zlib1g-dev python3-pip nodejs-legacy npm git && \
    echo '{ "allow_root": true }' > /root/.bowerrc && \
    pip3 install --upgrade pip  && \
    npm install -g bower topojson ogr2ogr

## PROJECT DEPENDENCIES
RUN pip3 install -r requirements.txt && \
    bower install

## DEPLOY

RUN python3 manage.py migrate # Creación de la base de datos y definición de tablas
RUN python3 manage.py collectstatic --noinput # Copia los ficheros estáticos de todas las aplicaciones a un directorio común
#RUN python3 manage.py test # Ejecuta los tests unitarios
RUN python3 manage.py createsuperuser # Crea un superusuario
RUN python3 manage.py check --deploy # Comprueba que los ajustes definidos son apropiados para una configuración de despliegue

EXPOSE 8000

#CMD ["python3", "manage.py runserver 0.0.0.0:8000"]
