from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Universidad


class IndexView(TemplateView):
    template_name = "tasas/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['universidades'] = Universidad.objects.all()

        return context

