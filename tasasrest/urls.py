"""tasasrest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, patterns
from django.conf.urls.static import static
from django.contrib import admin

from . import settings

from mapa.views import IndexView
from tasas.api.urls import urlpatterns as api_urlpatterns

urlpatterns = [
    url(r'^reporte/', include('mapa.urls')),
    url(r'^users/', include(admin.site.urls)),
    url(r'^admin/', include('tasas.urls', namespace="admin")), #TODO: Change namespace name
    url(r'^api/', include(api_urlpatterns, namespace="api")),
    url(r'^$', IndexView.as_view())
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)