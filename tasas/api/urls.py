from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import UniversidadViewSet, ProvinciaViewSet

router = DefaultRouter()
router.register(r'universidades', UniversidadViewSet)
router.register(r'provincias/(?P<provincia>[A-Za-z]+)', ProvinciaViewSet)
urlpatterns = router.urls