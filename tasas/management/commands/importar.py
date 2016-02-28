from django.utils.translation import gettext as _
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db import models

import json
import os
import warnings

from tasas.models import Universidad, Tasa

class Command(BaseCommand):
    help_text = _("Carga en la base de datos el fichero JSON utilizado en el proyecto original")

    def add_arguments(self, parser):
        """

        Args:
            parser: Instancia de [argparse](https://docs.python.org/3.5/library/argparse.html?highlight=argparse#module-argparse)

        Returns:
            None
        """
        parser.add_argument('file', type=str, help=_("Archivo json"))
        parser.add_argument('img-dir', type=str, default='img/uni/',
                            help=_("Directorio con los logos de la universidad"))
        parser.add_argument('--overwrite', action='store_true',
                            help=_("Sobreescribe la información"), dest='overwrite')
        # TODO: Add help parameter
    def handle(self, *args, **options):
        try:
            with open(options.get('file', ''), 'r') as f:
                data = json.load(f)
        except IOError:
            print(_("Archivo no encontrado"))
            return

        self.parse_file(data, options.get('img-dir'), options.get('overwrite', False))


    def parse_file(self, data, img_path='img/uni', overwrite=False):
        unis = data.get('unis', None)

        if unis is None or type(unis) is not list:
            raise CommandError(_("Archivo sin formato correcto"))\

        for uni in unis:
            try:
                self.add_uni(uni, img_path, overwrite)
            except ValidationError as v:
                warnings.warn("Error en clave: %s: %s" % (uni.get('siglas'), v), UserWarning)

    def add_uni(self, uni, img_path, overwrite=False):
        """
        Añade la universidad a la base de datos
        Args:
            uni: dict Diccionario con los datos de la universidad

        Returns:

        """
        try:
            universidad = Universidad.objects.get(siglas=uni.get('siglas'))
            if not overwrite: return
        except Universidad.DoesNotExist:
            universidad = Universidad()
        universidad.siglas = uni.get('siglas')
        universidad.nombre = uni.get('nombre')

        universidad.tipo = self.get_tipo_uni(uni.get('tipo'))
        universidad.centro = uni.get('centro')
        universidad.provincia = uni.get('provincia')
        universidad.campus = uni.get('campus')
        universidad.url = uni.get('url')

        if self.validate_logo(uni, img_path) is True:
            try:
                with open(os.path.join(img_path, 'uni_%s.jpg' % Universidad.get_siglas_no_centro(uni.get('siglas'))), 'rb') as f:
                    logo = File(f)
                    universidad.logo.save('uni_%s.jpg' % Universidad.get_siglas_no_centro(uni.get('siglas')), logo, save=True)
            except IOError:
                warnings.warn("Error al abrir imagen %s" % uni+'.jpg')

        # TODO: Añadir convenios?
        universidad.clean_fields()
        universidad.save()

    def validate_logo(self, uni, img_path):
        if uni.get('siglas', None) is None:
            raise ValidationError("Siglas no válidas")

        if not os.path.isdir(img_path):
            warnings.warn("Directorio %s no válido" % img_path, UserWarning)
            return False

        return os.path.isfile(os.path.join(img_path, 'uni_%s.jpg' % Universidad.get_siglas_no_centro(uni.get('siglas'))))



    def get_tipo_uni(self, tipo):
        """
        Retorna el valor asociado al tipo de universidad en la base de datos
        Args:
            tipo: Valor leído de fichero

        Returns:
            int
        """
        return next((code for code, value in dict(Universidad.TIPO_UNIVERSIDAD_CHOICES).items() if value == tipo), None)