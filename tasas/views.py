from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import View, TemplateView

from .models import Universidad, Tasa
from .forms import TasaForm


#TODO: Replace by ListView
class IndexView(TemplateView):
    template_name = "tasas/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['universidades'] = Universidad.objects.all()

        return context


class UniversidadView(View):

    template_name = "tasas/edit.html"

    def get(self, request, *args, **kwargs):
        uni = get_object_or_404(Universidad.objects.all(), siglas=kwargs.get('universidad', None))
        tasa_forms_grado = []
        tasa_forms_master = []
        for tasa in uni.tasas.filter(tipo_titulacion=Tasa.GRADO):
            tasa_forms_grado.append(TasaForm(instance=tasa,
                                       prefix="%s-%d" % (tasa.get_tipo_titulacion_verbose().lower(), tasa.curso)))

        for tasa in uni.tasas.filter(tipo_titulacion=Tasa.MASTER):
            tasa_forms_master.append(TasaForm(instance=tasa,
                                       prefix="%s-%d" % (tasa.get_tipo_titulacion_verbose().lower(), tasa.curso)))

        return render(request, self.template_name, {'uni': uni,
                                                    'form_tasas_grado': tasa_forms_grado,
                                                    'form_tasas_master': tasa_forms_master})