from django.conf.urls import url
from .views import ReporteView, ReporteSuccessView

urlpatterns = [
    url(r'success', ReporteSuccessView.as_view()),
    url(r'', ReporteView.as_view(), name="reporte")
]