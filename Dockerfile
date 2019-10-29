#FROM mhart/alpine-node
ARG BASE_IMAGE=python:3.6-alpine
FROM $BASE_IMAGE

ENV HOME /root
ENV SECRET_KEY no-secret-key #Set a secure Django secret key for production!
ENV LIBRARY_PATH=/lib:/usr/lib

WORKDIR $HOME

RUN apk add --no-cache --update \
	mariadb-connector-c-dev \
            build-base \
	mariadb-dev \
            git \
	    nodejs nodejs-npm \
	    gettext \
	    jpeg-dev zlib-dev \
 && npm install -g bower topojson ogr2ogr \
 && pip3 install --upgrade pip

COPY bower.json .bowerrc requirements.txt $HOME/
RUN pip3 install -r requirements.txt
RUN bower install --allow-root

## COPY PROJECT
COPY . $HOME

## DEPLOY Django
RUN python3 manage.py collectstatic --noinput && \
    python3 manage.py compilemessages && \
    python3 manage.py check --deploy # Comprueba que los ajustes definidos son apropiados para una configuración de despliegue

## DEPLOY MapaTasas
## RUN python3 manage.py importar mapa/data/uni/unis.json mapa/img/uni
## RUN python3 manage.py rendervariations 'tasas.universidad.logo'

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
