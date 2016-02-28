from django.forms import ModelForm
from .models import Universidad, Tasa
from django.forms.widgets import Select

class UniversidadForm(ModelForm):
    class Meta:
        model = Universidad
        #provincia = ChoiceField(choices=Universidad.PROVINCIAS)
        exclude = ('id',)

class TasaForm(ModelForm):
    class Meta:
        model = Tasa
        exclude = ('id',)
        widgets = {
            'tipo': Select(choices=Tasa.TIPOS_TASA)
        }

