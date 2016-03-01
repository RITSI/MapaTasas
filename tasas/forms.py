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
        exclude = ('id','universidad', 'tipo', 'tipo_titulacion')
        widgets = {
            'tipo': Select(choices=Tasa.TIPOS_TASA)
        }

    def remove_invalid_fields(self):
        """
        Elimina la información de los campos contradictorios con la información dada
        """
        # TODO
        pass

    ##TODO: Maketests
    def includes_information(self):
        fields = self.cleaned_data

        return (fields.get("curso") is not None) and (fields.get("tipo") is not None)
