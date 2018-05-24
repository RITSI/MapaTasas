from django.conf.urls import url, include
from django.contrib import admin
from .views import IndexView, UniversidadView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns =[
    url(r'^logout', auth_views.logout, {'next_page': '/'}),
    url(r'^universidad/(?P<universidad>[A-Za-z\-]+)', login_required(UniversidadView.as_view()), name="edit"),
    url(r'^universidad', login_required(UniversidadView.as_view()), name="create"),
    url(r'^$', login_required(IndexView.as_view()), name="index")
]