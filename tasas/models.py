import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MinLengthValidator
from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy
from stdimage.models import StdImageField
from stdimage.validators import MinSizeValidator

import tasasrest.settings as settings
from .provincias import PROVINCIAS


class Curso(models.Model):
    """
    Representa un curso académico
    """
    anno = models.IntegerField(unique=True, blank=False, null=False, verbose_name='Año',
                               validators=[RegexValidator(regex=r'^\d{4}$')])
    activo = models.BooleanField(default=True, null=False, blank=False)
    actual = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return "%s (%s)" % (self.anno, 'Activo' if self.activo else 'Inactivo')

    def save(self, *args, **kwargs):
        """
        Solo un curso puede ser el actual, por lo que al guardar es necesario desmarcar todos
        los cursos marcados como activos.
        """
        if self.actual:
            Curso.objects.filter(actual=True).update(actual=False)
        super(Curso, self).save(*args, **kwargs)

    class Meta:
        ordering = ['anno']


    @staticmethod
    def get_current_curso():
        try:
            curso = Curso.objects.get(actual=True)
            return curso
        except Curso.DoesNotExist:
            return None

    @staticmethod
    def curso_choices():
        return tuple((curso.anno, "%s/%s" % (curso.anno, curso.anno + 1)) for curso in Curso.objects.all())




class Universidad(models.Model):
    PUBLICA = 0
    PRIVADA = 1

    def __init__(self, *args, **kwargs):
        self._get_siglas_no_centro = self.get_siglas_no_centro
        super(Universidad, self).__init__(*args, **kwargs)

    TIPO_UNIVERSIDAD_CHOICES = ((PUBLICA, 'Pública'), (PRIVADA, 'Privada'))

    siglas = models.CharField(max_length=20, unique=True, null=False, blank=False,
                              validators=[RegexValidator(regex=r'[A-Za-z\-]+', message=ugettext_lazy(
                                  "Las siglas de la universidad solo pueden contener letras y guiones (-)"))],
                              help_text=ugettext_lazy("Siglas de la universidad"))
    nombre = models.CharField(max_length=200, null=False, blank=False,
                              help_text=ugettext_lazy("Nombre de la universidad"))
    tipo = models.IntegerField(choices=TIPO_UNIVERSIDAD_CHOICES, null=False, blank=False,
                               help_text=ugettext_lazy("Tipo de centro (público/privado)"))
    centro = models.CharField(max_length=200, null=True, blank=True, help_text=ugettext_lazy("Nombre del centro"))
    provincia = models.CharField(max_length=50, choices=PROVINCIAS, blank=False, null=False,
                                 help_text=ugettext_lazy("Provincia"))
    logo = StdImageField(upload_to=settings.ESCUDOS_PATH, null=True, blank=True,
                         variations={'thumbnail': (100, 100, True)},
                         validators=[MinSizeValidator(100, 100)],
                         help_text=ugettext_lazy("Escudo de la universidad"))

    campus = models.CharField(max_length=200, null=True, blank=True,
                              help_text=ugettext_lazy("Nombre del campus"))  # TODO: Hacer obligatorio?
    url = models.URLField(max_length=300, null=True, blank=True,
                          help_text=ugettext_lazy("URL del centro"))

    def _get_siglas_no_centro(self):
        return self.get_siglas_no_centro(self.siglas)

    @staticmethod
    def get_siglas_no_centro(siglas):
        """
        Elimina el sufijo del centro, útil para procesar imágenes
        Returns:

        """
        return re.sub(r'-.*', '', siglas)

    def get_provincia_unicode(self):
        return dict(PROVINCIAS).get(self.provincia)

    @property
    def tipo_universidad_verbose(self):
        return self.get_tipo_universidad_verbose(self.tipo)

    @classmethod
    def get_tipo_universidad_verbose(cls, tipo_universidad):
        # self
        return str(dict((tipo, nombre) for tipo, nombre in cls.TIPO_UNIVERSIDAD_CHOICES).get(tipo_universidad))

    def __str__(self):
        return self.nombre


class Tasa(models.Model):
    PRECIO_POR_CREDITO = 0
    PAGO_UNICO = 1
    MISCELANEO = 2

    TIPOS_TASA = (
        (PRECIO_POR_CREDITO, "Precio por crédito"),
        (PAGO_UNICO, "Pago único"),
        (MISCELANEO, "Misceláneo"),
    )

    GRADO = 0
    MASTER = 1

    TIPOS_TITULACION = (
        (GRADO, "Grado"),
        (MASTER, "Máster"),
    )

    TIPOS_TITULACION_ASCII = (
        (GRADO, "Grado"),
        (MASTER, "Master"),
    )

    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE, related_name='tasas',
                                    related_query_name='tasa',
                                    help_text=ugettext_lazy("Universidad asociada a esta tasa"),
                                    null=False,
                                    blank=True)

    tipo = models.IntegerField(choices=TIPOS_TASA, blank=False,  # null=False, default=0,
                               help_text=ugettext_lazy("Tipo de tasa"))
    tipo_titulacion = models.IntegerField(choices=TIPOS_TITULACION, blank=False, null=False,
                                          help_text=ugettext_lazy("Tipo de titulación (grado/máster)"))

    # El curso se representa con el año en el que da comienzo
    curso = models.ForeignKey(Curso, help_text=ugettext_lazy("Curso académico en el que esta tasa se aplica"))
    url = models.URLField(null=False, blank=False, validators=[MinLengthValidator(1)],
                          help_text=ugettext_lazy("URL del documento oficial"))

    tasa_global = models.FloatField(null=True, blank=True, help_text=ugettext_lazy("Tasa global"))
    descripcion = models.TextField(null=True, blank=True, max_length=500,
                                   help_text=ugettext_lazy("Texto informativo sobre la tasa"))
    tasas1 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.01)],
                               help_text=ugettext_lazy("Primera convocatoria"))
    tasas2 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.01)],
                               help_text=ugettext_lazy("Segunda convocatoria"))
    tasas3 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.01)],
                               help_text=ugettext_lazy("Tercera convocatoria"))
    tasas4 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.01)],
                               help_text=ugettext_lazy("Cuarta convocatoria"))

    def __unicode__(self):
        return self.universidad + ", " + self.TIPOS[int(self.tipo)][1] + ", " + self.curso

    def get_lista_tasas(self):
        return [self.tasas1, self.tasas2, self.tasas3, self.tasas4]

    def clean(self):
        """
        Valida los campos de las tasas de forma conjunta
        """

        if self.tipo == self.PRECIO_POR_CREDITO:
            tasas = self.get_lista_tasas()
            for tasa in tasas:
                if tasa is None:
                    raise ValidationError(_("Los %d campos de tasa deben ser rellenados" % len(tasas)))

            if self.tasa_global is not None:
                raise ValidationError(_("El campo 'tasa global' no es admitido para precios por crédito"))

        elif self.tipo == self.PAGO_UNICO:
            if self.tasa_global is None:
                raise ValidationError(_("La tasa global es obligatoria"))

            if next(iter([tasa for tasa in self.get_lista_tasas() if tasa is not None]), None):
                raise ValidationError(_("Los campos de tasa por crédito no son admitidos para pagos únicos"))

        elif self.tipo == self.MISCELANEO:
            if self.descripcion is None:
                raise ValidationError(_("Es necesario introducir una descripción sobre la tasa"))

            if next(iter([tasa for tasa in self.get_lista_tasas() if tasa is not None]), None):
                raise ValidationError(_("Los campos de tasa por crédito no son admitidos para tasas misceláneas"))

            if self.tasa_global is not None:
                raise ValidationError(_("El campo 'tasa global' no es admitido para tasas misceláneas"))
        else:
            raise ValidationError(_("Opción de tasa inválida"))

        super(Tasa, self).clean()

    def validate_curso(self, exclude=None):
        # TODO: see http://stackoverflow.com/a/14471010/2628463
        pass

    @property
    def tipo_titulacion_verbose(self):
        return dict((tipo, nombre) for tipo, nombre in self.TIPOS_TITULACION).get(self.tipo_titulacion)

    @property
    def tipo_titulacion_verbose_ascii(self):
        return dict((tipo, nombre) for tipo, nombre in self.TIPOS_TITULACION_ASCII).get(self.tipo_titulacion)

    @classmethod
    def get_tipo_titulacion_verbose(cls, tipo_titulacion):
        return dict((tipo, nombre) for tipo, nombre in cls.TIPOS_TITULACION).get(tipo_titulacion)

    @classmethod
    def get_tipo_titulacion_verbose_ascii(cls, tipo_titulacion):
        return dict((tipo, nombre) for tipo, nombre in cls.TIPOS_TITULACION_ASCII).get(tipo_titulacion)

    class Meta:
        ordering = ['curso__anno', 'tipo']
        unique_together = ('universidad', 'curso', 'tipo_titulacion')
