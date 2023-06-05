from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView
from administracion.helpers import obtener_coordenadas
from administracion.user_tests import user_is_visitant
from investigadores.models import Investigador
from instituciones_educativas.models import (
    InstitucionEducativa,
    SolicitudIngreso
)
from instituciones_educativas.forms import FormInstitucionEducativaUpdate
from usuarios.models import TipoUsuario


class InstitucionEducativaSolicitud(UserPassesTestMixin, CreateView):
    model = InstitucionEducativa
    form_class = FormInstitucionEducativaUpdate
    template_name = "vinculacion/formulario.html"
    extra_context = {"formulario_archivos": True}

    def test_func(self):
        return user_is_visitant(self.request.user)

    def form_valid(self, form):
        institucion_educativa = form.save(commit=False)
        institucion_educativa.encargado = self.request.user
        coordenadas = obtener_coordenadas(form.cleaned_data)

        if not coordenadas:
            messages.error(
                self.request,
                "Error al obtener los datos de ubicación, por favor" +
                " verifique que los datos de dirección" +
                " ingresados son correctos.")
            return super(
                InstitucionEducativaSolicitud, self).form_invalid(form)

        institucion_educativa.latitud = coordenadas.latitud
        institucion_educativa.longitud = coordenadas.longitud
        institucion_educativa.encargado.tipo_usuario = TipoUsuario.objects.get(
            tipo="Institucion Educativa")

        institucion_educativa.save()
        institucion_educativa.encargado.save()
        form.save_m2m()

        messages.success(self.request, "Solicitud registrada correctamente")
        return redirect('vinculacion:perfil')


class InstitucionEducativaActualizar(LoginRequiredMixin, UpdateView):
    model = InstitucionEducativa
    form_class = FormInstitucionEducativaUpdate
    template_name = "vinculacion/formulario_perfil.html"
    extra_context = {"formulario_archivos": True}

    def get_object(self):
        return get_object_or_404(
            InstitucionEducativa,
            encargado=self.request.user)

    def form_valid(self, form):
        institucion_educativa = form.save(commit=False)
        coordenadas = obtener_coordenadas(form.cleaned_data)

        if not coordenadas:
            messages.error(
                self.request,
                "Error al obtener los datos de ubicación, por favor" +
                " verifique que los datos de dirección" +
                " ingresados son correctos.")
            return super(
                InstitucionEducativaActualizar, self).form_invalid(form)

        institucion_educativa.latitud = coordenadas.latitud
        institucion_educativa.longitud = coordenadas.longitud

        institucion_educativa.save()
        form.save_m2m()

        messages.success(self.request, "Perfil actualizado correctamente")
        return redirect('vinculacion:perfil')


@login_required
def solicitud_ingreso_lista(request):
    institucion = get_object_or_404(
        InstitucionEducativa, encargado=request.user)
    solicitudes = SolicitudIngreso.objects.filter(
        institucion_educativa=institucion)

    return render(
        request,
        "vinculacion/solicitudes_ingreso.html",
        {"solicitudes": solicitudes})


@login_required
def instituciones_educativas_lista(request):
    instituciones = InstitucionEducativa.objects.filter(
        encargado__aprobado=True)
    if (request.user.tipo_usuario
            and request.user.tipo_usuario.tipo == "Investigador"):
        investigador = Investigador.objects.get(user=request.user)

        for institucion in instituciones:
            solicitudes = SolicitudIngreso.objects.filter(
                institucion_educativa=institucion)
            institucion.es_posible_solicitar = True

            for solicitud in solicitudes:
                if solicitud.investigador == investigador:
                    institucion.es_posible_solicitar = False
                    break

            institucion.es_miembro = False
            if investigador in institucion.miembros.all():
                institucion.es_miembro = True
                institucion.es_posible_solicitar = False

    paginator = Paginator(instituciones, 10)
    page_number = request.GET.get('page')
    instituciones = paginator.get_page(page_number)

    return render(
        request,
        "vinculacion/instituciones_educativas_lista.html",
        {"instituciones": instituciones})


@login_required
def crear_solicitud_ingreso(request, institucion_id):
    institucion = InstitucionEducativa.objects.get(pk=institucion_id)
    investigador = Investigador.objects.get(user=request.user)
    solicitud_ingreso = SolicitudIngreso(
        institucion_educativa=institucion, investigador=investigador)
    solicitud_ingreso.save()
    messages.success(
        request,
        "Solicitud de ingreso a la institución "+str(institucion)+" enviada")

    return redirect("instituciones_educativas:instituciones_educativas_lista")


@login_required
def contestar_solicitud_ingreso(request, investigador_id, respuesta):
    investigador = get_object_or_404(Investigador, pk=investigador_id)
    solicitud = get_object_or_404(SolicitudIngreso, investigador=investigador)

    if respuesta == 1:
        messages.success(
            request, "Se ha aceptado la solicitud del investigador")
        institucion = InstitucionEducativa.objects.get(encargado=request.user)
        institucion.miembros.add(investigador)
    else:
        messages.error(
            request, "Se ha rechazado la solicitud del investigador")

    solicitud.delete()

    return redirect(
        "instituciones_educativas:institucion_educativa_solicitudes")


@login_required
def miembros_lista(request):
    institucion = InstitucionEducativa.objects.get(encargado=request.user)
    miembros = institucion.miembros.all()

    return render(
        request,
        "vinculacion/miembros_lista.html",
        {"miembros": miembros})


@login_required
def miembro_eliminar(request, investigador_id):
    institucion = InstitucionEducativa.objects.get(encargado=request.user)
    investigador = Investigador.objects.get(pk=investigador_id)
    institucion.miembros.remove(investigador)

    return redirect("instituciones_educativas:institucion_educativa_miembros")
