from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response

from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Avg

from .serializers import UniversidadSerializer, TasaSerializer
from ..models import Universidad, Tasa, Curso


class UniversidadViewSet(ModelViewSet):
    queryset = Universidad.objects.all().filter(activa=True)
    serializer_class = UniversidadSerializer
    base_name = "universidades"
    http_method_names = ['get', 'head', 'options']

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        fields = request.GET.getlist('fields[]', None)
        serializer = self.serializer_class(queryset, fields=fields, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        uni = get_object_or_404(queryset, siglas=pk)
        serializer = self.serializer_class(uni)

        return Response(serializer.data)


class ProvinciaViewSet(ModelViewSet):
    queryset = Universidad.objects.all().prefetch_related('tasas').filter(activa=True)
    serializer_class = UniversidadSerializer
    http_method_names = ['get', 'head', 'options']

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        provincia = kwargs.get('provincia', None)
        if provincia is None:
            # TODO
            pass

        tipo_titulacion = request.query_params.get('tipo_titulacion', None)

        unis = queryset.filter(provincia__iexact=provincia)  # get_list_or_404(queryset, provincia__iexact=provincia)
        serializer = self.serializer_class(unis, filtro_tipo_tasas=tipo_titulacion, many=True)

        return Response(serializer.data)


class TasasViewSet(ModelViewSet):
    queryset = Tasa.objects.all()
    serializer_class = TasaSerializer
    http_method_names = ['get', 'head', 'options']

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        universidad = kwargs.get('universidad', None)
        if universidad is None:
            # TODO
            pass

        unis = get_list_or_404(queryset, universidad__siglas=universidad)
        serializer = self.serializer_class(unis, many=True)

        return Response(serializer.data)


class AverageViewSet(ViewSet):
    queryset = Tasa.objects.all()
    # TODO: PAGO ÚNICO
    # serializer_class = AverageDataSerializer
    http_method_names = ['get', 'head', 'options']

    def list(self, request, *args, **kwargs):
        return_data = {}
        # TODO: Remove the 'complete' flag. Doesn't make much sense
        for curso in Curso.objects.filter(activo=True).order_by('anno'):
            tasas = self.queryset.filter(curso=curso, tipo=Tasa.PRECIO_POR_CREDITO)

            tasas1_filter = tasas.filter(tasas1__gt=0, universidad__tipo=Universidad.PUBLICA)
            avg_1 = tasas1_filter.aggregate(Avg('tasas1'))['tasas1__avg']
            avg_1_complete = tasas1_filter.count() == tasas.count()

            tasas2_filter = tasas.filter(tasas2__gt=0, universidad__tipo=Universidad.PUBLICA)
            avg_2 = tasas2_filter.aggregate(Avg('tasas2'))['tasas2__avg']
            avg_2_complete = tasas2_filter.count() == tasas.count()

            tasas3_filter = tasas.filter(tasas3__gt=0, universidad__tipo=Universidad.PUBLICA)
            avg_3 = tasas1_filter.aggregate(Avg('tasas3'))['tasas3__avg']
            avg_3_complete = tasas3_filter.count() == tasas.count()

            tasas4_filter = tasas.filter(tasas4__gt=0, universidad__tipo=Universidad.PUBLICA)
            avg_4 = tasas4_filter.aggregate(Avg('tasas4'))['tasas4__avg']
            avg_4_complete = tasas4_filter.count() == tasas.count()

            data = {
                'media_1': {'complete': avg_1_complete,  # TODO: Mark true/false if number of unis satisfies
                            'data': avg_1 or 0
                            },
                'media_2': {'complete': avg_2_complete,
                            'data': avg_2 or 0
                            },
                'media_3': {'complete': avg_3_complete,
                            'data': avg_3 or 0
                            },
                'media_4': {'complete': avg_4_complete,
                            'data': avg_4 or 0
                            }
            }

            return_data[curso.anno] = data

        return Response(return_data)

    # def retrieve(self, request, *args, **kwargs):
    #     curso = kwargs.get('curso', None)
    #     if curso is None:
    #         return Response({})
    #
    #     curso = get_object_or_404(Curso.objects.all(), anno=curso)
    #
    #     tasas = self.queryset.filter(curso=curso, tipo=Tasa.PRECIO_POR_CREDITO)
    #     avg_1 = list(tasas.filter(tasas1__gt=0).aggregate(Avg('tasas1')).values())[0]
    #     avg_2 = list(tasas.filter(tasas2__gt=0).aggregate(Avg('tasas2')).values())[0]
    #     avg_3 = list(tasas.filter(tasas3__gt=0).aggregate(Avg('tasas3')).values())[0]
    #     avg_4 = list(tasas.filter(tasas4__gt=0).aggregate(Avg('tasas4')).values())[0]
    #
    #     data = {
    #         'media_1': {'complete': False,  # TODO: Mark true/false if number of unis satisfies
    #                     'data': avg_1
    #                     },
    #         'media_2': {'complete': False,
    #                     'data': avg_2
    #                     },
    #         'media_3': {'complete': False,
    #                     'data': avg_3
    #                     },
    #         'media_4': {'complete': False,
    #                     'data': avg_4
    #                     }
    #     }
    #
    #     return Response(data)
