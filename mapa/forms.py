from django.forms import ModelForm
from .models import Reporte
from tasas.models import Universidad
from django.forms.widgets import Select
from django.utils.functional import lazy
from tasas.models import Curso


class ReporteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReporteForm, self).__init__(*args, **kwargs)
        self.fields['universidad'].choices = [(e.id, "%s - %s" % (e.nombre, e.centro)) for e in Universidad.objects.all()]

    class Meta:
        model = Reporte
        exclude = ('id', 'estado')
        #widgets = {
            #'curso': Select(choices=lazy(lambda: ((0, "Curso académico"),) + Curso.curso_choices(), tuple)())
        #}
