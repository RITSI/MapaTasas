FROM mhart/alpine-node

ENV HOME /root
ENV SECRET_KEY no-secret-key #Set a secure Django secret key for production!
ENV LIBRARY_PATH=/lib:/usr/lib

WORKDIR $HOME

RUN apk add --update \
            build-base \
            git \
            python3 \
            python3-dev py3-pip jpeg-dev zlib-dev \
 && npm install -g bower@1.7.8 topojson ogr2ogr \
 && pip3 install --upgrade pip \
 && rm /var/cache/apk/*

COPY requirements.txt $HOME/
RUN pip3 install -r requirements.txt

COPY bower.json .bowerrc $HOME/
RUN bower install --allow-root

## COPY PROJECT
COPY . $HOME

## DEPLOY Django

RUN python3 manage.py migrate && \
    python3 manage.py collectstatic --noinput && \
    python3 manage.py compilemessages && \
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password')" | python3 manage.py shell  && \
    python3 manage.py check --deploy # Comprueba que los ajustes definidos son apropiados para una configuración de despliegue

## DEPLOY MapaTasas
RUN python3 manage.py importar mapa/data/uni/unis.json mapa/img/uni
RUN python3 manage.py rendervariations 'tasas.universidad.logo'


EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
