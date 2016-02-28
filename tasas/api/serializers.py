from rest_framework.serializers import ModelSerializer
from ..models import Universidad, Tasa

class UniversidadSerializer(ModelSerializer):
    class Meta:
        model = Universidad
        exclude = ('id',)
        depth = 1

class TasaSerializer(ModelSerializer):
    class Meta:
        model = Tasa
        exclude = ('id',)
