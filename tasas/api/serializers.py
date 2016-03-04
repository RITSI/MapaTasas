from rest_framework.serializers import ModelSerializer, SerializerMethodField
from ..models import Universidad, Tasa, get_current_curso

import os.path

class TasaSerializer(ModelSerializer):
    class Meta:
        model = Tasa
        exclude = ('id',)

class UniversidadSerializer(ModelSerializer):
    logo_thumbnail = SerializerMethodField()
    tasas = TasaSerializer(many=True, read_only=True)
    tipo_verbose = SerializerMethodField(read_only=True)
    tasas_curso_actual = SerializerMethodField(read_only=True)

    class Meta:
        model = Universidad
        exclude = ('id',)
        depth = 1

    def get_tasas(self, obj):
        if obj.tasas:
            return obj.tasas


    def get_logo_thumbnail(self, obj):
        if obj.logo:
            file, ext = os.path.splitext(os.path.basename(obj.logo.url))
            path = os.path.dirname(obj.logo.url)

            return os.path.join(path, "%s.%s%s" % (file, obj.logo.field.variations["thumbnail"]["name"], ext))

    def get_tipo_verbose(self, obj):
        if obj.tipo is not None:
            return obj.get_tipo_universidad_verbose(obj.tipo)

    def get_tasas_curso_actual(self, obj):
        if obj is not None and obj.tasas is not None:
            current_curso = get_current_curso()
            print(current_curso)
            try:
                tasa = obj.tasas.get(curso=current_curso)
                return TasaSerializer(tasa).data
            except Tasa.DoesNotExist:
                pass
