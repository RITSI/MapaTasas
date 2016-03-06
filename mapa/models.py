from django.db import models
from django.utils.translation import ugettext as _
from tasas.models import Universidad, CursoValidator


class Reporte(models.Model):
    """
    Permite reportar errores en los datos mostrados
    """
    universidad = models.ForeignKey(Universidad, related_name="reportes", blank=True, null=True)
    curso = models.IntegerField(validators=[CursoValidator()], help_text=_("Curso académico"), blank=True, null=True)
    email = models.EmailField(help_text=_("Indica un correo electrónico si deseas que nos pongamos en contacto contigo"),
                              blank=True, null=True)
    descripcion = models.TextField(help_text=_("Describe el problema"), max_length=100000,
                                   blank=False, null=False)