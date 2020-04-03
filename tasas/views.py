from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic import View, TemplateView

from .models import Universidad, Tasa, Curso
from .forms import TasaForm, UniversidadForm


class IndexView(TemplateView):
    template_name = "tasas/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['universidades_activas'] = Universidad.objects.filter(activa=True)
        context['universidades_inactivas'] = Universidad.objects.filter(activa=False)

        return context


class UniversidadView(View):

    template_name = "tasas/edit.html"
    template_confirmation_name = "tasas/confirmation.html"
    grado_verbose = Tasa.get_tipo_titulacion_verbose_ascii(Tasa.GRADO).lower()
    master_verbose = Tasa.get_tipo_titulacion_verbose_ascii(Tasa.MASTER).lower()

    def get(self, request, **kwargs):
        siglas = kwargs.get('siglas', None)
        if siglas is None:
            universidad_form = UniversidadForm()
            tasa_forms_grado = []
            tasa_forms_master = []

            for curso in Curso.objects.filter(activo=True):
                tasa_form = TasaForm(prefix="%s-%d" % (self.grado_verbose, curso.anno))
                tasa_forms_grado.append((curso.anno, tasa_form))

                tasa_form = TasaForm(prefix="%s-%d" % (self.master_verbose, curso.anno))
                tasa_forms_master.append((curso.anno, tasa_form))
            uni_nombre = None
        else:
            if any(x.isupper() for x in siglas):
                kwargs['siglas'] = kwargs['siglas'].lower()
                return HttpResponseRedirect(redirect_to=reverse('admin:edit', kwargs=kwargs))

            uni = get_object_or_404(Universidad.objects.all(), siglas=kwargs.get('siglas').lower())
            uni_nombre = uni.nombre
            universidad_form = UniversidadForm(instance=uni)
            tasa_forms_grado = []
            tasa_forms_master = []

            tasas_grado = uni.tasas.filter(tipo_titulacion=Tasa.GRADO)
            tasas_master = uni.tasas.filter(tipo_titulacion=Tasa.MASTER)

            for curso in Curso.objects.filter(activo=True):
                try:
                    tasa = tasas_grado.get(curso=curso)
                    tasa_form = TasaForm(instance=tasa, prefix="%s-%d" % (self.grado_verbose, curso.anno))
                except Tasa.DoesNotExist:
                    tasa_form = TasaForm(prefix="%s-%d" % (self.grado_verbose, curso.anno))

                tasa_forms_grado.append((curso.anno, tasa_form))

                try:
                    tasa = tasas_master.get(curso=curso)
                    tasa_form = TasaForm(instance=tasa, prefix="%s-%d" % (self.master_verbose, curso.anno))
                except Tasa.DoesNotExist:
                    tasa_form = TasaForm(prefix="%s-%d" % (self.master_verbose, curso.anno))

                tasa_forms_master.append((curso.anno, tasa_form))

        return render(request, self.template_name, {'nombre_universidad': uni_nombre,
                                                    'universidad_form': universidad_form,
                                                    'form_tasas_grado': tasa_forms_grado,
                                                    'form_tasas_master': tasa_forms_master})

    def post(self, request, siglas=None):
        has_errors = False

        nombre_universidad = None

        forms_tasas_grado = []
        forms_tasas_master = []
        if siglas is None:
            uni_form = UniversidadForm(request.POST, request.FILES)
        else:
            uni = get_object_or_404(Universidad.objects.all(), siglas=siglas)
            uni_form = UniversidadForm(request.POST, request.FILES, instance=uni)

        if uni_form.is_valid():
            uni = uni_form.save(commit=False)
            nombre_universidad = uni.nombre

            tasas_grado = uni.tasas.filter(tipo_titulacion=Tasa.GRADO)
            tasas_master = uni.tasas.filter(tipo_titulacion=Tasa.MASTER)

            for curso in Curso.objects.filter(activo=True):
                request_data = request.POST.copy()

                request_data["grado-%s-curso" % curso.anno] = curso.anno
                request_data["grado-%s-tipo_titulacion" % curso.anno] = Tasa.GRADO

                request_data["master-%s-curso" % curso.anno] = curso.anno
                request_data["master-%s-tipo_titulacion" % curso.anno] = Tasa.MASTER

                try:
                    tasa_instance = tasas_grado.get(curso=curso)
                    form_grado = TasaForm(request_data, prefix="%s-%d" % (self.grado_verbose, curso.anno),
                                          instance=tasa_instance)
                except Tasa.DoesNotExist:
                    form_grado = TasaForm(request_data, prefix="%s-%d" % (self.grado_verbose, curso.anno),
                                          instance=None)

                has_errors |= (not form_grado.is_valid()) and (form_grado.includes_information())

                if form_grado.includes_information():
                    forms_tasas_grado.append((curso.anno, form_grado))
                else:
                    f = TasaForm(prefix="%s-%d" % (self.grado_verbose, curso.anno))
                    forms_tasas_grado.append((curso.anno, f))

                try:
                    tasa_instance = tasas_master.get(curso=curso)
                    form_master = TasaForm(request_data, prefix="%s-%d" % (self.master_verbose, curso.anno),
                                           instance=tasa_instance)
                except Tasa.DoesNotExist:
                    form_master = TasaForm(request_data, prefix="%s-%d" % (self.master_verbose, curso.anno),
                                           instance=None)

                has_errors |= (not form_master.is_valid()) and form_master.includes_information()

                if form_master.includes_information():
                    forms_tasas_master.append((curso.anno, form_master))
                else:
                    f = TasaForm(prefix="%s-%d" % (self.master_verbose, curso.anno))
                    forms_tasas_master.append((curso.anno, f))

        else:
            has_errors = True

        if has_errors:
            return render(request, self.template_name, {'nombre_universidad': nombre_universidad,
                                                        'universidad_form': uni_form,
                                                        'form_tasas_grado': forms_tasas_grado,
                                                        'form_tasas_master': forms_tasas_master})

        for anno, form in [f for f in forms_tasas_grado + forms_tasas_master if f[1].includes_information()]:
            tasa = form.save(commit=False)
            tasa.universidad = uni
            tasa.curso = Curso.objects.get(anno=anno)
            tasa.save()
        uni.save()

        # WTF: message variable unused -@ismael at 2018-5-24 16:01:28
        # 
        if siglas is None:
            message = _("Universidad creada correctamente")
        else:
            message = _("Datos actualizados correctamente")

        return render(request, self.template_confirmation_name, {'back_url': "/admin/universidad/%s" % uni.siglas,
                                                                 'message': message,
                                                                 'title': _("Datos actualizados")})


class CreateUniversidadView(View):
    """
    Permite la creación de una nueva universidad
    """
    template_name = "tasas/edituni.html"

class AboutView(TemplateView):
    template_name = 'tasas/about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        return context
