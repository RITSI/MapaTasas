from django.contrib import admin
from .models import Reporte

class ReporteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Reporte, ReporteAdmin)