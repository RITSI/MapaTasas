from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import UniversidadSerializer, TasaSerializer
from ..models import Universidad, Tasa

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

    queryset = Universidad.objects.all()
    serializer_class = UniversidadSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        provincia = kwargs.get('provincia', None)
        if provincia is None:
            #TODO
            pass

        unis = get_list_or_404(queryset, provincia__iexact=provincia)
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
