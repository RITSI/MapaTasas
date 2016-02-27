from django.utils.translation import gettext as _
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import ValidationError

import json

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
        #parser.add_argument('img-dir', nargs=1, type=str, default='img',
        #                    help=_("Directorio con los logos de la universidad"))
        # TODO: Add help parameter
    def handle(self, *args, **options):
        try:
            with open(options.get('file', None), 'r') as f:
                data = json.load(f)
        except IOError:
            print(_("Archivo no encontrado"))
            return

        self.parse_file(data)


    def parse_file(self, data, img_dir='img'):
        unis = data.get('unis', None)

        if unis is None or type(unis) is not list:
            raise CommandError(_("Archivo sin formato correcto"))\

        for uni in unis:
            try:
                self.add_uni(uni)
            except ValidationError as v:
                print("Error en clave: %s: %s" % (uni.get('nombre'), v))
        """
            logo = models.ImageField(upload_to=settings.ESCUDOS_PATH, null=True, blank=True,
                                     help_text=ugettext_lazy("Escudo de la universidad"))
        """

    def add_uni(self, uni):
        """
        Añade la universidad a la base de datos
        Args:
            uni: dict Diccionario con los datos de la universidad

        Returns:

        """
        universidad = Universidad()
        universidad.siglas = uni.get('siglas')
        universidad.nombre = uni.get('nombre')

        universidad.tipo = self.get_tipo_uni(uni.get('tipo'))
        universidad.centro = uni.get('centro')
        universidad.provincia = uni.get('provincia')
        universidad.campus = uni.get('campus')
        universidad.url = uni.get('url')
        universidad.logo = self.add_logo(uni)
        # TODO: Añadir convenios?
        universidad.clean_fields()
        universidad.save()

    def add_logo(self, uni):
        pass
    
    def get_tipo_uni(self, tipo):
        """
        Retorna el valor asociado al tipo de universidad en la base de datos
        Args:
            tipo: Valor leído de fichero

        Returns:
            int
        """
        return next((code for code, value in dict(Universidad.TIPO_UNIVERSIDAD_CHOICES).items() if value == tipo), None)