from rest_framework.serializers import ModelSerializer
from ..models import Universidad

class UniversidadSerializer(ModelSerializer):
    class Meta:
        model = Universidad
        exclude = ('id',)
        depth = 1