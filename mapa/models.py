from django.db import models
from django.utils.translation import ugettext as _
from tasas.models import Universidad, CursoValidator


class Reporte(models.Model):
    """
    Permite reportar errores en los datos mostrados
    """
    universidad = models.ForeignKey(Universidad, verbose_name="Universidad",
                                    related_name="reportes", blank=True, null=True)
    curso = models.IntegerField(verbose_name="Curso académico", help_text=_("Curso académico"),
                                default=0, blank=True, null=True)
    email = models.EmailField(verbose_name="Correo electrónico",
                              help_text=_("Indica un correo electrónico si deseas que nos pongamos en contacto contigo"),
                              blank=True, null=True)
    descripcion = models.TextField(verbose_name="Descripción", help_text=_("Describe el problema"), max_length=100000,
                                   blank=False, null=False)

    estado = models.BooleanField(verbose_name="Estado", blank=True, null=False, default=False)
    fecha = models.DateTimeField(verbose_name="Fecha", blank=True, null=False, auto_now_add=True)

    class Meta:
        ordering = ['estado', '-fecha']

    def __str__(self):
        if self.universidad:
            return "[%s] Reporte sobre la %s" % (self.fecha.strftime('%H:%M %d-%m-%Y'), self.universidad)

        else:
            return "[%s]" % (self.fecha.strftime('%H:%M %d-%m-%Y'))