import os.path

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ..models import Universidad, Tasa


class TasaSerializer(ModelSerializer):
    curso = SerializerMethodField(read_only=True)
    actual = SerializerMethodField(read_only=True)

    @staticmethod
    def get_curso(obj):
        if obj:
            return obj.curso.anno

    @staticmethod
    def get_actual(obj):
        if obj:
            return obj.curso.actual

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

        fields = kwargs.pop('fields', [])
        super(DynamicFieldsMixin, self).__init__(*args, **kwargs)

        if fields is not None and len(fields) > 0:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UniversidadSerializer(DynamicFieldsMixin, ModelSerializer):
    logo_thumbnail = SerializerMethodField()
    #tasas = TasaSerializer(many=True, read_only=True)
    tasas = SerializerMethodField()
    tipo_verbose = SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        self.filtro_tipo_tasas = kwargs.pop("filtro_tipo_tasas", None)
        super().__init__(*args, **kwargs)

    def get_tasas(self, obj):
        if self.filtro_tipo_tasas is not None:
            tasas = obj.tasas.filter(tipo_titulacion=self.filtro_tipo_tasas)
        else:
            tasas = obj.tasas
        return TasaSerializer(tasas, many=True).data

    def get_logo_thumbnail(self, obj):
        if obj.logo:
            file, ext = os.path.splitext(os.path.basename(obj.logo.url))
            path = os.path.dirname(obj.logo.url)

            return os.path.join(path, "%s.%s%s" % (file, obj.logo.field.variations["thumbnail"]["name"], ext))

    def get_tipo_verbose(self, obj):
        if obj.tipo is not None:
            return obj.get_tipo_universidad_verbose(obj.tipo)

    class Meta:
        model = Universidad
        exclude = ('id',)
        depth = 1
