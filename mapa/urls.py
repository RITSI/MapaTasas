from django.conf.urls import url
from .views import ReporteView

urlpatterns = [
    url(r'^(?P<universidad>[A-Za-z\-]*)$', ReporteView.as_view(), name="reporte")
]