from django.forms import ModelForm
from .models import Reporte
from django.forms.widgets import Select
from django.utils.functional import lazy
from tasas.models import Curso


class ReporteForm(ModelForm):
    class Meta:
        model = Reporte
        exclude = ('id', 'estado')
        #widgets = {
            #'curso': Select(choices=lazy(lambda: ((0, "Curso académico"),) + Curso.curso_choices(), tuple)())
        #}
