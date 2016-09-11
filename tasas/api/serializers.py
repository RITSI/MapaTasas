from rest_framework.serializers import ModelSerializer, SerializerMethodField, Serializer
from rest_framework import serializers
from ..models import Universidad, Tasa, get_current_curso

import os.path

class TasaSerializer(ModelSerializer):
    curso = SerializerMethodField(read_only=True)

    def get_curso(self, obj):
        if obj:
            return obj.curso.anno

    class Meta:
        model = Tasa
        exclude = ('id',)


class DynamicFieldsMixin(object):
    # From : https://gist.github.com/dbrgn/4e6fc1fe5922598592d6 and http://stackoverflow.com/a/31979444/2628463
    """
    A serializer mixin that takes an additional `fields` argument that controls
    which fields should be displayed.
    Usage::
        class MySerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
            class Meta:
                model = MyModel
    """
    def __init__(self, *args, **kwargs):

        fields = kwargs.pop('fields', None)
        super(DynamicFieldsMixin, self).__init__(*args, **kwargs)

        if fields is not None and len(fields) > 0:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing-allowed:
                self.fields.pop(field_name)

class UniversidadSerializer(DynamicFieldsMixin, ModelSerializer):
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
            try:
                tasa = obj.tasas.get(curso=current_curso)
                return TasaSerializer(tasa).data
            except Tasa.DoesNotExist:
                pass
