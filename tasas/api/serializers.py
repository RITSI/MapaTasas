from rest_framework.serializers import ModelSerializer, SerializerMethodField
from ..models import Universidad, Tasa

import os.path

from stdimage.models import StdImageFieldFile

class UniversidadSerializer(ModelSerializer):
    logo_thumbnail = SerializerMethodField()
    class Meta:
        model = Universidad
        exclude = ('id',)
        depth = 1


    def get_logo_thumbnail(self, obj):
        if obj.logo:
            file, ext = os.path.splitext(os.path.basename(obj.logo.url))
            path = os.path.dirname(obj.logo.url)

            return os.path.join(path, "%s.%s%s" % (file, obj.logo.field.variations["thumbnail"]["name"], ext))

class TasaSerializer(ModelSerializer):
    class Meta:
        model = Tasa
        exclude = ('id',)
