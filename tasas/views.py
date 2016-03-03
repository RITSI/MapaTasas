from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.utils.translation import ugettext as _
from django.views.generic import View, TemplateView

from .models import Universidad, Tasa, get_current_curso
from .forms import TasaForm
from tasasrest import settings

import pdb

#TODO: Replace by ListView
class IndexView(TemplateView):
    template_name = "tasas/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['universidades'] = Universidad.objects.all()

        return context


class UniversidadView(View):

    template_name = "tasas/edit.html"
    template_confirmation_name = "tasas/confirmation.html"
    grado_verbose = Tasa.get_tipo_titulacion_verbose_ascii(Tasa.GRADO).lower()
    master_verbose = Tasa.get_tipo_titulacion_verbose_ascii(Tasa.MASTER).lower()

    def get(self, request, *args, **kwargs):
        uni = get_object_or_404(Universidad.objects.all(), siglas=kwargs.get('universidad', None))
        tasa_forms_grado = []
        tasa_forms_master = []

        tasas_grado = uni.tasas.filter(tipo_titulacion=Tasa.GRADO)
        tasas_master = uni.tasas.filter(tipo_titulacion=Tasa.MASTER)

        for curso in range(settings.MIN_YEAR, get_current_curso() + settings.YEARS_IN_ADVANCE):

            try:
                tasa = tasas_grado.get(curso=curso)
                tasa_form = TasaForm(instance=tasa, prefix="%s-%d" % (self.grado_verbose, curso))
            except Tasa.DoesNotExist:
                tasa_form = TasaForm(prefix="%s-%d" % (self.grado_verbose, curso))
                tasa_form.fields["curso"].initial = curso

            tasa_forms_grado.append(tasa_form)

            try:
                tasa = tasas_master.get(curso=curso)
                tasa_form = TasaForm(instance=tasa, prefix="%s-%d" % (self.master_verbose, curso))
            except Tasa.DoesNotExist:
                tasa_form = TasaForm(prefix="%s-%d" % (self.master_verbose, curso))
                tasa_form.fields["curso"].initial = curso

            tasa_forms_master.append(tasa_form)

        #TODO for tasa in tasas.filter(tipo_titulacion=Tasa.GRADO):
        #     tasa_forms_grado.append(TasaForm(instance=tasa,
        #                                      prefix="%s-%d" % (tasa.tipo_titulacion_verbose().lower(), tasa.curso)))
        #
        # for tasa in tasas.filter(tipo_titulacion=Tasa.MASTER):
        #     tasa_forms_master.append(TasaForm(instance=tasa,
        #                                       prefix="%s-%d" % (tasa.tipo_titulacion_verbose().lower(), tasa.curso)))

        return render(request, self.template_name, {'uni': uni,
                                                    'form_tasas_grado': tasa_forms_grado,
                                                    'form_tasas_master': tasa_forms_master})

    def post(self, request, *args, **kwargs):
        uni = get_object_or_404(Universidad.objects.all(), siglas=kwargs.get('universidad', None))

        forms_tasas_grado = []
        forms_tasas_master = []
        has_errors = False
        tasas_grado = uni.tasas.filter(tipo_titulacion=Tasa.GRADO)
        tasas_master = uni.tasas.filter(tipo_titulacion=Tasa.MASTER)

        for curso in range(settings.MIN_YEAR, get_current_curso() + settings.YEARS_IN_ADVANCE):
            # TODO: This is a very dirty fix. Change whenever possible
            request_data = request.POST.copy()

            request_data["grado-%s-curso" % curso] = curso
            request_data["grado-%s-tipo_titulacion"%curso]=Tasa.GRADO

            request_data["master-%s-curso" % curso] = curso
            request_data["master-%s-tipo_titulacion"%curso]=Tasa.MASTER

            try:
                tasa_instance = tasas_grado.get(curso=curso)
                form_grado = TasaForm(request_data, prefix="%s-%d" % (self.grado_verbose, curso),
                                  instance=tasa_instance)
            except Tasa.DoesNotExist:
                form_grado = TasaForm(request_data, prefix="%s-%d" % (self.grado_verbose, curso),
                                  instance=None)

            has_errors |=  (not form_grado.is_valid()) and ( form_grado.includes_information())

            if form_grado.includes_information():

                forms_tasas_grado.append(form_grado)
            else:
                f = TasaForm(prefix="%s-%d" % (self.grado_verbose, curso))
                f.fields["curso"].initial = curso
                forms_tasas_grado.append(f)

            try:
                tasa_instance = tasas_master.get(curso=curso)
                form_master = TasaForm(request_data, prefix="%s-%d" % (self.master_verbose, curso),
                                   instance=tasa_instance)
            except Tasa.DoesNotExist:
                form_master = TasaForm(request_data, prefix="%s-%d" % (self.master_verbose, curso),
                                   instance=None)

            has_errors |= (not form_master.is_valid()) and form_master.includes_information()

            if form_master.includes_information():
                forms_tasas_master.append(form_master)
            else:
                f = TasaForm(prefix="%s-%d" % (self.master_verbose, curso))
                f.fields["curso"].initial = curso
                forms_tasas_master.append(f)

        if has_errors:
            print("Here")
            return render(request, self.template_name, {'uni': uni,
                                                            'form_tasas_grado': forms_tasas_grado,
                                                            'form_tasas_master': forms_tasas_master})


        for form in [f for f in forms_tasas_grado + forms_tasas_master if f.includes_information()]:
            tasa = form.save(commit=False)
            tasa.universidad = uni
            tasa.save()

        return render(request, self.template_confirmation_name, {'back_url': "/admin/universidad/%s" % uni.siglas,
                                                                 'message': _("Datos actualizados correctamente"),
                                                                 'title': _("Datos actualizados")})
