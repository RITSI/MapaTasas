from django.conf.urls import url, include
from .views import IndexView, UniversidadView

urlpatterns =[
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^universidad/(?P<universidad>[A-Za-z\-]+)', UniversidadView.as_view(), name="edit"),
    url(r'^universidad/$', UniversidadView.as_view(), name="create")
]