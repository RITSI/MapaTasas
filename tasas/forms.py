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
        exclude = ('id','universidad')
        widgets = {
            'tipo': Select(choices=Tasa.TIPOS_TASA)
        }

    ##TODO: Maketests
    def includes_information(self):
        if not hasattr(self, 'cleaned_data'): return False
        fields = self.cleaned_data

        return ((fields.get("tipo") is not None))
