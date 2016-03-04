from django.views.generic import TemplateView
from django.contrib.staticfiles.templatetags.staticfiles import static
class IndexView(TemplateView):
    template_name = 'mapa/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context["mapa"] = static('mapa/maps/esp.json')

        return context