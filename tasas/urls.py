from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from .views import IndexView, UniversidadView

admin.autodiscover()

urlpatterns = [
    url(r'logout', auth_views.LogoutView, {'next_page': '/'}),
    url(r'^universidad/(?P<siglas>[A-Za-z0-9\-]+)', login_required(UniversidadView.as_view()), name="edit"),
    url(r'universidad', login_required(UniversidadView.as_view()), name="create"),
    url(r'^$', login_required(IndexView.as_view()), name="index")
]
