from django.utils.translation import gettext as _
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.core.files import File

import json
import os
import warnings
import sys
import re

from tasas.models import Curso, Universidad, Tasa


class Command(BaseCommand):
    """
    Carga en la aplicación los datos sobre tasas recogidos en un fichero .json
    """
    help_text = _("Carga en la base de datos el fichero JSON utilizado en el proyecto original")

    def add_arguments(self, parser):
        """
        Añade argumentos al parseador del comando
        Args:
            parser: Instancia de [argparse](https://docs.python.org/3.5/library/argparse.html)

        Returns:
            None
        """
        parser.add_argument('file', type=str, help="Archivo json que contiene los datos a importar")
        parser.add_argument('img-dir', type=str, default='img/uni/',
                            help="Directorio con los logos de la universidad, siguiendo la convención uni_[siglas].jpg")
        parser.add_argument('--overwrite', action='store_true',
                            help="Sobreescribe la información de la base de datos", dest='overwrite')

    def handle(self, *args, **options):
        try:
            with open(options.get('file', ''), 'r') as f:
                data = json.load(f)
        except IOError:
            sys.stderr.write("Archivo '%s' no encontrado\n" % options.get('file', ''))
            return

        self.parse_file(data, img_path=options.get('img-dir'), overwrite=options.get('overwrite', False))

    def parse_file(self, data, img_path='img/uni', overwrite=False):
        unis = data.get('unis', None)

        if unis is None or type(unis) is not list:
            raise CommandError(_("Formato de archivo incorrecto"))\

        for uni in unis:
            try:
                self.add_uni(uni, img_path, overwrite)
            except ValidationError as v:
                sys.stderr.write("Error en clave: %s: %s\n" % (uni.get('siglas'), v))

    def parse_float(self, value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0

    def add_uni(self, uni_data, img_path, overwrite=False):
        """
        Añade la universidad a la base de datos
        Args:
            uni_data: dict Diccionario con los datos de la universidad
            img_path: Directorio que contiene el logo de la universidad
            overwrite: Indica si la información preexistente puede ser sobreescrita.
        """
        try:
            universidad = Universidad.objects.get(siglas=uni_data.get('siglas'))
            if overwrite:
                universidad.tasas.all().delete()
            else:
                return
        except Universidad.DoesNotExist:
            universidad = Universidad()
        universidad.siglas = uni_data.get('siglas')
        universidad.nombre = uni_data.get('nombre')

        tipo = self.get_tipo_uni(uni_data.get('tipo'))

        if tipo is None:
            raise ValidationError("Tipo de universidad '%s' no válido para %s. Omitiendo."
                                  % (uni_data.get('tipo'), uni_data.get('nombre')))

        universidad.tipo = tipo
        universidad.centro = uni_data.get('centro')
        universidad.provincia = uni_data.get('provincia')
        universidad.campus = uni_data.get('campus')
        universidad.url = uni_data.get('url')

        if self.validate_logo(uni_data, img_path):
            try:
                with open(os.path.join(img_path, 'uni_%s.jpg'
                          % Universidad.get_siglas_no_centro(uni_data.get('siglas'))), 'rb') as f:
                    logo = File(f)
                    universidad.logo.save('uni_%s.jpg' % Universidad.get_siglas_no_centro(uni_data.get('siglas')),
                                          logo, save=True)
            except IOError:
                warnings.warn("Error al abrir imagen %s" % uni_data + '.jpg')

        # TODO: Añadir convenios?
        universidad.clean_fields()
        universidad.save()

        self.add_tasas(uni_data, universidad)

    def validate_logo(self, uni_data, img_path):
        """
        Comprueba que las siglas de la universidad y el directorio de imágenes sean válidos
        :param uni_data: Datos de la universidad
        :param img_path: Directorio de imágenes
        :return: Boolean
        """
        if len(uni_data.get('siglas', '')) == 0:
            sys.stderr.write("Siglas '%s' no válidas\n" % uni_data.get('siglas', ''))
            return False

        if not os.path.isdir(img_path):
            sys.stderr.write("Directorio '%s' no válido\n" % img_path)
            return False

        return os.path.isfile(os.path.join(img_path,
                                           'uni_%s.jpg' % Universidad.get_siglas_no_centro(uni_data.get('siglas'))))

    def get_tipo_uni(self, tipo):
        """
        Retorna el valor asociado al tipo de universidad en la base de datos
        Args:
            tipo: Valor leído de fichero

        Returns:
            int
        """
        return next((code for code, value in dict(Universidad.TIPO_UNIVERSIDAD_CHOICES).items() if value == tipo), None)

    def add_tasas(self, data, universidad):
        r = re.compile(r'tasas_(\d+)')
        for key in [k for k in data.keys() if r.match(k)]:
            tasa_data = data.get(key)
            if tasa_data:
                curso = int(r.search(key).group(1))
                tasa = Tasa()
                tasa.tipo = Tasa.PRECIO_POR_CREDITO
                tasa.tipo_titulacion = Tasa.GRADO
                (tasa.curso, _) = Curso.objects.get_or_create(anno=curso)

                tasa.tasas1 = self.parse_float(tasa_data.get('tasas1', 0))
                tasa.tasas2 = self.parse_float(tasa_data.get('tasas2', 0))
                tasa.tasas3 = self.parse_float(tasa_data.get('tasas3', 0))
                tasa.tasas4 = self.parse_float(tasa_data.get('tasas4', 0))

                tasa.url = tasa_data.get('url', None)

                tasa.universidad = universidad

                try:
                    tasa.full_clean()
                    tasa.save()
                except ValidationError as v:
                    sys.stderr.write("Tasas de %s no válidas para universidad %s: %s\n" %
                                     (curso, universidad.nombre, v))

    # def add_tasas(self, data, uni):
    #     for year in range(settings.MIN_YEAR, get_current_curso()+settings.YEARS_IN_ADVANCE):
    #         tasa_data = data.get('tasas_%d' % year)
    #         if tasa_data is not None:
    #             tasa = Tasa()
    #             tasa.tipo = Tasa.PRECIO_POR_CREDITO
    #             tasa.tipo_titulacion = Tasa.GRADO
    #             tasa.curso = year
    #
    #             tasa.tasas1 = self.parse_float(tasa_data.get('tasas1', 0))
    #             tasa.tasas2 = self.parse_float(tasa_data.get('tasas2', 0))
    #             tasa.tasas3 = self.parse_float(tasa_data.get('tasas3', 0))
    #             tasa.tasas4 = self.parse_float(tasa_data.get('tasas4', 0))
    #
    #             tasa.url = tasa_data.get('url', None)
    #
    #             tasa.universidad = uni
    #
    #             try:
    #                 tasa.full_clean()
    #                 tasa.save()
    #             except ValidationError as v:
    #                 sys.stderr.write("Tasas de %s no válidas para universidad: %s: %s\n" %
    #                                  (year, uni.nombre, v.messages))
    #
    #         else:
    #             sys.stderr.write("Tasas de %s no válidas para universidad: %s\n" % (year, uni.nombre))
