from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from investigadores.forms import SolicitudTrabajoForm
from usuarios.models import TipoUsuario
from vinculacion.models import Categoria, Noticia
from vinculacion.helpers import get_user_specific_data
from django.views.generic import CreateView, DeleteView, ListView
from investigadores.models import (
    Investigador,
    Investigacion,
    SolicitudTrabajo,
    CategoriaA,
    CategoriaB,
    RevisoresCatA,
    RevisoresCatB)
from empresas.models import Empresa
from instituciones_educativas.models import (
    InstitucionEducativa,
)
from administracion.models import (
    Convocatoria,
    AcercaDe,
    Contacto,
    Premios
)
from usuarios.models import User, MUNICIPIOS
import itertools
from . import helpers
import datetime


def index(request):
    return redirect("usuarios:login")


@login_required
def dashboard(request):
    #return redirect("vinculacion:perfil")
    tipos_usuario = TipoUsuario.objects.all()
    tipos_usuario_snake_case = [
        "_".join(t.tipo.split()).lower() for t in tipos_usuario]
    categorias = Categoria.objects.all()
    usuarios = []
    investigadores = Investigador.objects.all()
    empresas = Empresa.objects.all()
    instituciones_educativas = InstitucionEducativa.objects.all()

    usuarios.extend([{
        "username": u.user.username,
        "latitud": u.latitud,
        "longitud": u.longitud,
        "tipoUsuario": u.user.tipo_usuario.tipo,
        "categorias": list(set(itertools.chain.from_iterable(
            [list(
                map(
                    str,
                    investigacion.categorias.all())
            ) for investigacion in Investigacion.objects.filter(
                autores=u.pk)]))),
        "municipio": u.municipio,
        "url": reverse_lazy("investigadores:investigador_perfil", args=[u.pk])
    } for u in investigadores])
    usuarios.extend([{
        "username": u.encargado.username,
        "latitud": u.latitud,
        "longitud": u.longitud,
        "tipoUsuario": u.encargado.tipo_usuario.tipo,
        "categorias": list(map(str, u.especialidades.all())),
        "municipio": u.municipio,
        "url": ""
    } for u in empresas])
    usuarios.extend([{
        "username": u.encargado.username,
        "latitud": u.latitud,
        "longitud": u.longitud,
        "tipoUsuario": u.encargado.tipo_usuario.tipo,
        "categorias": list(map(str, u.especialidades.all())),
        "municipio": u.municipio,
        "url": ""
    } for u in instituciones_educativas])

    areas_conocimiento = list(
        set(map(lambda categoria: categoria.area_conocimiento, categorias)))
    areas_conocimiento = [{
        "area": area,
        "categorias": Categoria.objects.filter(
            area_conocimiento=area)
    } for area in areas_conocimiento]

    return render(
        request,
        "vinculacion/map.html",
        {
            "tipos_usuario": zip(tipos_usuario, tipos_usuario_snake_case),
            "categorias": categorias,
            "usuarios": usuarios,
            "municipios": MUNICIPIOS,
            "areas_conocimiento": areas_conocimiento
        })


@login_required
def noticias(request):
    noticias = Noticia.objects.all().order_by('fecha')

    return render(request, "vinculacion/noticias.html", {"noticias": noticias})


@login_required
def noticia(request, id):
    noticia = Noticia.objects.get(id=id)

    return render(request, "vinculacion/noticia.html", {"noticia": noticia})


@login_required
def perfil(request):
    usuario = request.user
    if usuario.is_staff:
        return redirect("administracion:dashboard")
    
    if usuario.es_revisor:
        return redirect("vinculacion:revisor")

    if not usuario.tipo_usuario:
        if Convocatoria.objects.all()[0].activa:
            return render(request, "vinculacion/perfil_seleccionar.html")
        else:
            messages.error(
                request,
                "La convocatoria se encuentra cerrada por el momento")
            return redirect("investigadores:investigadores_lista")

    if not usuario.aprobado:
        return render(request, "vinculacion/perfil_pendiente.html")

    usuario_data = get_user_specific_data(usuario)
    catA = CategoriaA.objects.filter(user_id = request.user.id)[:5]
    catB = CategoriaB.objects.filter(user_id = request.user.id)[:5]
    return render(
        request,
        "vinculacion/perfil.html",
        {"usuario_data": usuario_data, "categoriaA": catA, "categoriaB": catB})

@login_required
def premiosCyT(request):
    fechas = Premios.objects.first()

    if not fechas:
        messages.error(request, "Error, la convocatoria esta cerrada")
        return redirect("vinculacion:perfil")
    today = datetime.date.today()
    if today >= fechas.fecha_inicio and today <= fechas.fecha_fin: 
        tipo = request.user.tipo_usuario
        usuario_data = get_user_specific_data(request.user)
        if str(tipo) == "Investigador":
            if usuario_data["es_sei"]:
                try:
                    cA = CategoriaA.objects.get(user_id = request.user.id, anio=datetime.datetime.today().year)
                except:
                    cA = False

                try:
                    cB = CategoriaB.objects.get(user_id = request.user.id, anio=datetime.datetime.today().year)
                except:
                    cB = False
                return render(request, "vinculacion/perfil_premio_estatal.html", {
                    "CategoriaA": cA,
                    "CategoriaB": cB,
                    "Convocatoria": fechas.fecha_fin - today
                })
            else:
                messages.error(request, "Es necesario contar constancia de investigador para participar, comunicate al siguiente telefono: 492 921 3228 o al correo: lfaraiz@gmail.com")
                return redirect("vinculacion:perfil")
        else:
            messages.error(request, "Error, no eres un investigador")
            return redirect("vinculacion:perfil")
    else:
        messages.error(request, "Error, la convocatoria esta cerrada")
        return redirect("vinculacion:perfil")

def RevisorListaCategoriaA(request):
    revisiones = RevisoresCatA.objects.filter(revisor_id = request.user.id, estatus = "E")
    return render(request, "revisores/dashboard.html", {
        "revisiones": revisiones,
    })

def RevisorCategoriaB(request):
    revisiones = RevisoresCatB.objects.filter(revisor_id = request.user.id, estatus = "E")
    return render(request, "revisores/categoria-b.html", {
        "revisiones": revisiones,
    })

class UsuarioEliminar(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('vinculacion:index')
    template_name = "vinculacion/confirm_delete.html"

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        messages.success(self.request, "Cuenta eliminada correctamente")
        return self.delete(request, *args, **kwargs)


class CrearSolicitudTrabajo(LoginRequiredMixin, CreateView):
    model = SolicitudTrabajo
    form_class = SolicitudTrabajoForm
    template_name = "vinculacion/formulario.html"

    def form_valid(self, form):
        investigador_id = self.kwargs['investigador_id']
        if self.request.user.pk == investigador_id:
            messages.error(
                self.request,
                "Un investigador no puede hacer una solicitud a sí mismo")
            return super(CrearSolicitudTrabajo, self).form_invalid(form)
        solicitud = form.save(commit=False)
        solicitud.usuario_solicitante = User.objects.get(
            pk=self.request.user.pk)
        investigador = get_object_or_404(
            Investigador,
            pk=investigador_id
        )
        solicitud.usuario_a_vincular = investigador
        solicitud.estado = "E"
        solicitud.save()
        messages.success(
            self.request,
            "Solicitud de trabajo a el investigador " +
            str(investigador)+" enviada")
        return redirect("investigadores:investigador_perfil", investigador_id)


@login_required
def aceptar_solicitud(request, pk):
    investigador = get_object_or_404(
        Investigador,
        user=request.user
    )
    solicitud = get_object_or_404(
        SolicitudTrabajo,
        pk=pk,
        usuario_a_vincular=investigador,
        estado="E"
    )
    solicitud.estado = "A"
    solicitud.save()
    messages.success(request, "La solicitud ha sido aceptada")

    return redirect("investigadores:solicitudes_trabajo_lista")


@login_required
def rechazar_solicitud(request, pk):
    investigador = get_object_or_404(
        Investigador,
        user=request.user
    )
    solicitud = get_object_or_404(
        SolicitudTrabajo,
        pk=pk,
        usuario_a_vincular=investigador,
        estado="E"
    )
    solicitud.estado = "R"
    solicitud.estado_investigador = "R"
    solicitud.save()
    messages.success(request, "La solicitud ha sido rechazada")

    return redirect("investigadores:solicitudes_trabajo_lista")


@login_required
def trabajos_en_curso(request):
    usuario = get_object_or_404(User, pk=request.user.pk)
    trabajos = SolicitudTrabajo.objects.filter(
        Q(usuario_a_vincular__user=usuario) | Q(usuario_solicitante=usuario),
        estado__in=['A', 'P']).order_by('fecha').reverse()
    page = request.GET.get('page', 1)
    paginator = Paginator(trabajos, 5)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request,
        "vinculacion/trabajos_en_curso.html",
        {"trabajos": trabajos, "page_obj": page_obj})


@login_required
def historial_trabajos(request):
    investigador = get_object_or_404(User, pk=request.user.pk)
    trabajos = SolicitudTrabajo.objects.filter(
        Q(usuario_a_vincular__user=investigador) |
        Q(usuario_solicitante=investigador),
        estado__in=['R', 'C', 'F']).order_by('fecha').reverse()

    page = request.GET.get('page', 1)
    paginator = Paginator(trabajos, 5)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request,
        "vinculacion/historial_trabajos.html",
        {"trabajos": trabajos, "page_obj": page_obj})


@login_required
def cambiar_estado(request, pk, estado):
    solicitud = get_object_or_404(
        SolicitudTrabajo,
        pk=pk
    )

    if solicitud.estado == "F" or solicitud.estado == "C":
        messages.error(
            request,
            "No se puede cambiar el estado de una solicitud finalizada")
        return redirect('vinculacion:trabajos_lista')

    if estado == "C":
        messages.success(
            request,
            "Estado de trabajo canceldo")
        helpers.cancelar_trabajo(request.user.pk, solicitud)

    elif estado == "F":
        messages.success(
            request,
            "Estado de trabajo finalizado")
        helpers.finalizar_trabajo(request.user.pk, solicitud)

    elif estado == "R":
        messages.success(
            request,
            "Estado de trabajo rechazado")
        helpers.rechazar_trabajo(request.user.pk, solicitud)

    elif estado == "P":
        messages.success(
            request,
            "Estado de trabajo en proceso")
        helpers.trabajo_en_proceso(request.user.pk, solicitud)

    elif estado == "E":
        messages.success(
            request,
            "Estado de trabajo en Revision")
        helpers.trabajo_en_revision(request.user.pk, solicitud)

    else:
        messages.error(
            request,
            "Estado no válido")

    return redirect('vinculacion:trabajos_lista')


@login_required
def contacto(request):
    contacto = Contacto.objects.all()[0]
    return render(
        request,
        "vinculacion/info.html",
        {
            "info_titulo": "Contacto",
            "info": contacto
        }
    )


@login_required
def acerca_de(request):
    acerca_de = AcercaDe.objects.all()[0]
    return render(
        request,
        "vinculacion/info.html",
        {
            "info_titulo": "Acerca de",
            "info": acerca_de
        }
    )
