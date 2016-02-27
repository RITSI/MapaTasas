from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import UniversidadSerializer
from ..models import Universidad

class UniversidadViewSet(ModelViewSet):
    queryset = Universidad.objects.all()
    serializer_class = UniversidadSerializer

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

        provincia = kwargs.get('provincia')
        unis = get_list_or_404(queryset, provincia__iexact=provincia)
        serializer = self.serializer_class(unis, many=True)

        return Response(serializer.data)

    # """def get_queryset(self, *args, **kwargs):
    #     pk = self.request.query_params.get('provincia')
    #     print(pk)
    #     unis = get_list_or_404(Universidad.objects.all(), provincia__iexact=pk)
    #     serializer = self.serializer_class(unis)
    #
    #     return Response(serializer.data)"""