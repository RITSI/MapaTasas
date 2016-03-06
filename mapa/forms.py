from django.forms import ModelForm
from .models import Reporte
from django.forms.widgets import Select
from django.utils.functional import lazy
from tasas.models import curso_choices

class ReporteForm(ModelForm):
    class Meta:
        model = Reporte
        exclude = ('id',)
        widgets = {
            'curso': Select(choices=lazy(curso_choices, tuple)())
        }

