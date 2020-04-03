from django.contrib import admin
from .models import Curso


class CursoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Curso, CursoAdmin)
