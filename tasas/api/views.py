from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response

from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Avg

from .serializers import UniversidadSerializer, TasaSerializer
from ..models import Universidad, Tasa, get_current_curso

from tasasrest import settings

class UniversidadViewSet(ModelViewSet):

    queryset = Universidad.objects.all()
    serializer_class = UniversidadSerializer
    base_name = "universidades"

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        uni = get_object_or_404(queryset, siglas=pk)
        serializer = self.serializer_class(uni)

        return Response(serializer.data)


class ProvinciaViewSet(ModelViewSet):

    queryset = Universidad.objects.all().prefetch_related('tasas')
    serializer_class = UniversidadSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        provincia = kwargs.get('provincia', None)
        if provincia is None:
            #TODO
            pass

        unis = queryset.filter(provincia__iexact=provincia)#get_list_or_404(queryset, provincia__iexact=provincia)
        serializer = self.serializer_class(unis, many=True)

        return Response(serializer.data)

class TasasViewSet(ModelViewSet):
    queryset = Tasa.objects.all()
    serializer_class = TasaSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        universidad = kwargs.get('universidad', None)
        if universidad is None:
            #TODO
            pass

        unis = get_list_or_404(queryset, universidad__siglas=universidad)
        serializer = self.serializer_class(unis, many=True)

        return Response(serializer.data)

class AverageViewSet(ViewSet):
    queryset = Tasa.objects.all()
    #TODO: PAGO ÚNICO
    #serializer_class = AverageDataSerializer

    def list(self, request, *args, **kwargs):
        return_data = {}
        for curso in range(settings.MIN_YEAR, get_current_curso() + settings.YEARS_IN_ADVANCE):

            tasas = self.queryset.filter(curso = curso, tipo=Tasa.PRECIO_POR_CREDITO)
            avg_1 = list(tasas.filter(tasas1__gt=0).aggregate(Avg('tasas1')).values())[0]
            avg_2 = list(tasas.filter(tasas2__gt=0).aggregate(Avg('tasas2')).values())[0]
            avg_3 = list(tasas.filter(tasas3__gt=0).aggregate(Avg('tasas3')).values())[0]
            avg_4 = list(tasas.filter(tasas4__gt=0).aggregate(Avg('tasas4')).values())[0]

            data = {
                'media_1': {'complete': False, #TODO: Mark true/false if number of unis satisfies
                            'data':avg_1
                            },
                'media_2': {'complete':False,
                            'data':avg_2
                            },
                'media_3': {'complete':False,
                            'data':avg_3
                            },
                'media_4': {'complete':False,
                            'data':avg_4
                            }
            }

            return_data[curso] = data;

        return Response(return_data)

    def retrieve(self, request, *args, **kwargs):
        curso = kwargs.get('pk', None)
        if curso is None:
            return Response({})

        tasas = self.queryset.filter(curso=curso, tipo=Tasa.PRECIO_POR_CREDITO)
        avg_1 = list(tasas.filter(tasas1__gt=0).aggregate(Avg('tasas1')).values())[0]
        avg_2 = list(tasas.filter(tasas2__gt=0).aggregate(Avg('tasas2')).values())[0]
        avg_3 = list(tasas.filter(tasas3__gt=0).aggregate(Avg('tasas3')).values())[0]
        avg_4 = list(tasas.filter(tasas4__gt=0).aggregate(Avg('tasas4')).values())[0]

        data = {
            'media_1': {'complete': False, #TODO: Mark true/false if number of unis satisfies
                        'data':avg_1
                        },
            'media_2': {'complete':False,
                        'data':avg_2
                        },
            'media_3': {'complete':False,
                        'data':avg_3
                        },
            'media_4': {'complete':False,
                        'data':avg_4
                        }
        }

        return Response(data)
