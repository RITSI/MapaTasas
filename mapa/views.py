from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic import TemplateView, FormView

from .forms import ReporteForm


class IndexView(TemplateView):
    template_name = 'mapa/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context["mapa"] = static('mapa/maps/esp.json')
        context["template_universidad_provincia"] = static('mapa/templates/template_universidad_provincia.mst')
        context["template_universidad_detalle"] = static('mapa/templates/template_universidad_detalle.handlebars')
        return context


class ReporteView(FormView):
    form_class = ReporteForm
    template_name = 'mapa/reporte_form.html'
    success_url = 'success'

    def form_valid(self, form):
        reporte = form.save()

        return super(ReporteView, self).form_valid(form)


class ReporteSuccessView(TemplateView):
    template_name = 'mapa/success.html'
