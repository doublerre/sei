import asyncio
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from administracion.helpers import obtener_coordenadas
from administracion.user_tests import user_is_visitant
from administracion.user_tests import user_is_staff_member
from investigadores.models import (
    Investigador,
    Investigacion,
    NivelInvestigador,
    SolicitudTrabajo,
    InvestigacionGoogleScholar,
    CategoriaA,
    CategoriaB,
    RevisoresCatA,
    RevisoresCatB
)
from investigadores.forms import (
    FormInvestigadorBase,
    FormInvestigadorBaseUpdate,
    FormInvestigacion,
    FormCategoriaA,
    FormCategoriaB,
    FormRevisorCatA,
    FormRevisorCatB
)
from vinculacion.helpers import (
    get_author,
    get_publications
)
from usuarios.models import TipoUsuario
from urllib.parse import urlparse, parse_qs
from django.http import FileResponse
from django.contrib import messages
from django.http import HttpResponseForbidden
from docxtpl import DocxTemplate
from docx import Document
import datetime
import subprocess
import os
import zipfile
import zlib


class InvestigadorSolicitud(UserPassesTestMixin, CreateView):
    model = Investigador
    form_class = FormInvestigadorBase
    template_name = "vinculacion/formulario.html"
    extra_context = {"formulario_archivos": True}

    def test_func(self):
        return user_is_visitant(self.request.user)

    def form_valid(self, form):
        investigador = form.save(commit=False)
        investigador.user = self.request.user
        coordenadas = obtener_coordenadas(form.cleaned_data)

        if not coordenadas:
            messages.error(
                self.request,
                "Error al obtener los datos de ubicación, por favor" +
                " verifique que los datos de dirección" +
                " ingresados son correctos.")
            return super(InvestigadorSolicitud, self).form_invalid(form)

        investigador.latitud = coordenadas.latitud
        investigador.longitud = coordenadas.longitud
        investigador.user.tipo_usuario = TipoUsuario.objects.get(
            tipo="Investigador")
        investigador.nivel = NivelInvestigador.objects.get(nivel=1)

        investigador.save()
        investigador.user.save()

        messages.success(self.request, "Solicitud registrada correctamente")
        return redirect('vinculacion:perfil')

class SolicitudCategoriaA(LoginRequiredMixin, CreateView):
    model = CategoriaA
    form_class = FormCategoriaA
    template_name = "categoriaA.html"
    extra_context = {
        "formulario_archivos": True,
        "titulo": "Categoria A: Producción Científica y Tecnológica.",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.user.id
        
        context["c1"] = CategoriaA.objects.filter(user_id = userid, anio=datetime.datetime.today().year).count()
        context["c2"] = CategoriaB.objects.filter(user_id = userid, anio=datetime.datetime.today().year).count()
        return context

    def form_valid(self, form):
        categoria = form.save(commit=False)
        categoria.user = Investigador.objects.get(pk = self.request.user.id)
        categoria.anio = datetime.datetime.today().year
        
        categoria.save()
        categoria.user.save()
        messages.success(self.request, "Solicitud enviada con exito.")
        return redirect("vinculacion:perfil")

class UpdateSolicitudCategoriaA(LoginRequiredMixin, UpdateView):
    model = CategoriaA
    form_class = FormCategoriaA
    template_name = "categoriaA.html"
    extra_context = {
        "formulario_archivos": True,
        "titulo": "Categoria A: Producción Científica y Tecnológica.",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        investigador = Investigador.objects.get(user_id = self.request.user.id)
        context["curp"] = investigador.curp
        context["investigador"] = investigador
        context["user_id"] = self.request.user.id
        return context

    def form_valid(self, form):
        categoria = form.save(commit=False)
        
        categoria.save()
        categoria.user.save()
        messages.success(self.request, "Solicitud enviada con exito.")
        return redirect("vinculacion:perfil")

class SolicitudCategoriaB(LoginRequiredMixin, CreateView):
    model = CategoriaB
    form_class = FormCategoriaB
    template_name = "categoriaA.html"
    extra_context = {
        "formulario_archivos": True,
        "titulo": "Categoria B: Superación Académica, Formación de Recursos Humanos y Otros."
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.user.id
        investigador = Investigador.objects.get(user_id = self.request.user.id)
        context["c1"] = CategoriaA.objects.filter(user_id = userid, anio=datetime.datetime.today().year).count()
        context["c2"] = CategoriaB.objects.filter(user_id = userid, anio=datetime.datetime.today().year).count()
        context["curp"] = investigador.curp
        return context

    def form_valid(self, form):
        categoria = form.save(commit=False)
        categoria.user = Investigador.objects.get(pk = self.request.user.id)
        categoria.anio = datetime.datetime.today().year
        
        categoria.save()
        categoria.user.save()
        messages.success(self.request, "Solicitud enviada con exito.")
        return redirect("vinculacion:perfil")

class UpdateSolicitudCategoriaB(LoginRequiredMixin, UpdateView):
    model = CategoriaB
    form_class = FormCategoriaB
    template_name = "categoriaA.html"
    extra_context = {
        "formulario_archivos": True,
        "titulo": "Categoria B: Superación Académica, Formación de Recursos Humanos y Otros."
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        investigador = Investigador.objects.get(user_id = self.request.user.id)
        context["curp"] = investigador.curp
        context["investigador"] = investigador
        context["user_id"] = self.request.user.id
        return context

    def form_valid(self, form):
        categoria = form.save(commit=False)
        
        categoria.save()
        categoria.user.save()
        messages.success(self.request, "Solicitud enviada con exito.")
        return redirect("vinculacion:perfil")

class InvestigadorActualizar(LoginRequiredMixin, UpdateView):
    model = Investigador
    form_class = FormInvestigadorBaseUpdate
    template_name = "vinculacion/formulario_perfil.html"
    extra_context = {"formulario_archivos": True}

    def get_object(self):
        return get_object_or_404(Investigador, user=self.request.user)

    def form_valid(self, form):
        investigador = form.save(commit=False)
        coordenadas = obtener_coordenadas(form.cleaned_data)

        if not coordenadas:
            messages.error(
                self.request,
                "Error al obtener los datos de ubicación, por favor" +
                " verifique que los datos de dirección" +
                " ingresados son correctos.")
            return super(InvestigadorActualizar, self).form_invalid(form)

        investigador.latitud = coordenadas.latitud
        investigador.longitud = coordenadas.longitud

        investigador.save()

        messages.success(self.request, "Perfil actualizado correctamente")
        return redirect('vinculacion:perfil')


class InvestigadorLista(LoginRequiredMixin, ListView):
    model = Investigador
    template_name = "vinculacion/investigadores_lista.html"


class InvestigadorInvestigaciones(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Investigacion
    template_name = "vinculacion/investigaciones_lista.html"

    def get_queryset(self):
        investigador = get_object_or_404(Investigador, user=self.request.user)
        return Investigacion.objects.filter(
            autores__in=[investigador]).order_by('titulo')


class InvestigadorSolicitudesTrabajo(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = SolicitudTrabajo
    template_name = "vinculacion/solicitudes_trabajo_lista.html"

    def get_queryset(self):
        investigador = get_object_or_404(Investigador, user=self.request.user)
        return SolicitudTrabajo.objects.filter(
            usuario_a_vincular__in=[investigador],
            estado='E').order_by('fecha')


class InvestigacionNuevo(LoginRequiredMixin, CreateView):
    model = Investigacion
    form_class = FormInvestigacion
    success_url = reverse_lazy('investigadores:investigaciones_lista')
    template_name = "vinculacion/formulario_perfil.html"

    def form_valid(self, form):
        investigador = get_object_or_404(Investigador, user=self.request.user)
        investigacion = form.save()
        if investigador not in investigacion.autores.all():
            investigacion.autores.add(investigador)
        return redirect(self.success_url)

class EditarRevisionCatA(LoginRequiredMixin, UpdateView):
    model = RevisoresCatA
    form_class =FormRevisorCatA
    success_url = reverse_lazy('vinculacion:revisor')
    template_name = "revisores/formulario.html"
    extra_context = {
        "accion": "Agregar calificación",
        "nombre_modelo": "para la solicitud del investigador:",
        "formulario_archivos": False,
        "menu_activo": "categoria-a"
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        revisionid = self.kwargs['pk']
        revision = RevisoresCatA.objects.get(id = revisionid)
        investigador = Investigador.objects.get(user_id = revision.solicitud.user.user_id)
        context["investigador"] = investigador
        context["revision"] = revision
        context["revisor_id"] = self.request.user.id
        return context

    def form_valid(self, form):
        revision = form.save(commit=False)
        if revision.estatus == "F":
            messages.error(self.request, "Este investigador ya ha sido evaluado.")
            return redirect(self.success_url)
        revision.estatus = "F"
        revision.save()
        messages.success(self.request, "Evaluación guardada con exito.")
        return redirect(self.success_url)

class EditarRevisionCatB(LoginRequiredMixin, UpdateView):
    model = RevisoresCatB
    form_class =FormRevisorCatB
    success_url = reverse_lazy('vinculacion:revisor-categoria-b')
    template_name = "revisores/formulario.html"
    extra_context = {
        "accion": "Agregar calificación",
        "nombre_modelo": "para la solicitud del investigador:",
        "formulario_archivos": False,
        "menu_activo": "categoria-b"
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        revisionid = self.kwargs['pk']
        revision = RevisoresCatB.objects.get(id = revisionid)
        investigador = Investigador.objects.get(user_id = revision.solicitud.user.user_id)
        context["investigador"] = investigador
        context["revision_b"] = revision
        context["revisor_id_b"] = self.request.user.id
        return context

    def form_valid(self, form):
        revision = form.save(commit=False)
        if revision.estatus == "F":
            messages.error(self.request, "Este investigador ya ha sido evaluado.")
            return redirect(self.success_url)
        revision.estatus = "F"
        revision.save()
        messages.success(self.request, "Evaluación guardada con exito.")
        return redirect(self.success_url)

@login_required
def investigaciones_google(request):
    if request.method == "POST":
        investigador = get_object_or_404(Investigador, user=request.user)
        parsed = urlparse(request.POST["profile-url"])
        arguments = parse_qs(parsed.query)

        try:
            user_id = arguments['user'][0]
        except Exception:
            messages.error(
                request, "No se encontró el perfil de google scholar")
            return redirect("investigadores:investigaciones_lista")

        author = get_author(user_id)

        if author is None:
            messages.error(
                request, "No se encontró el perfil de google scholar")
            return redirect("investigadores:investigaciones_lista")

        publicaciones = asyncio.run(get_publications(author))

        for publicacion in publicaciones:
            try:
                InvestigacionGoogleScholar.objects.create(
                    titulo=publicacion["titulo"],
                    investigador=investigador,
                )
                investigacion = Investigacion.objects.create(
                    titulo=publicacion["titulo"],
                    contenido=publicacion["contenido"],
                )
                investigacion.autores.add(investigador),
                investigacion.save()
            except Exception:
                continue

    messages.success(
                request, "Carga de investigaciones exitosa")
    return redirect("investigadores:investigaciones_lista")


@login_required
def investigador_perfil(request, investigador_id):
    investigador = Investigador.objects.get(pk=investigador_id)
    investigaciones = Investigacion.objects.filter(autores__in=[investigador])

    return render(
        request,
        "vinculacion/perfil_investigador.html",
        {
            "investigador": investigador,
            "investigaciones_lista": investigaciones
        })


def mostrar_cv(request, investigador_id):
    investigador = get_object_or_404(Investigador, user=investigador_id)
    filepath = os.path.join('media', '{0}'.format(investigador.curriculum_vitae.name))
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')

def erroresHttp(request, error):
    messages.error(request, f"{str(error)}")
    success_url = reverse_lazy('vinculacion:revisor')
    return redirect(success_url)

def erroresHttpCatB(request, error):
    messages.error(request, f"{str(error)}")
    success_url = reverse_lazy('vinculacion:revisor-categoria-b')
    return redirect(success_url)

@login_required
def exportZipCatA(request, rev_id):
    try:
        cA = CategoriaA.objects.get(pk = rev_id)
        revisores = RevisoresCatA.objects.get(solicitud_id = rev_id)
    except:
        messages.error(request, "No se encontro la solicitud con este ID.")
        return redirect("vinculacion:revisor")
    
    try:
        compression = zipfile.ZIP_DEFLATED
    except:
        compression = zipfile.ZIP_STORED

    zf = zipfile.ZipFile(f"media/ZIPs/{str(cA.user.curp)}.zip", mode="w")
    
    try:
        if cA.a1:
            zf.write(f"media/{str(cA.a1)}", f"A1-{str(cA.user.curp)}.pdf", compress_type=compression)
        if cA.a2:
            zf.write(f"media/{str(cA.a2)}", f"A2-{str(cA.user.curp)}.pdf", compress_type=compression)
        if cA.a3:
            zf.write(f"media/{str(cA.a3)}", f"A3-{str(cA.user.curp)}.pdf", compress_type=compression)
        if cA.a4:
            zf.write(f"media/{str(cA.a4)}", f"A4-{str(cA.user.curp)}.pdf", compress_type=compression)
        if cA.a5:
            zf.write(f"media/{str(cA.a5)}", f"A5-{str(cA.user.curp)}.pdf", compress_type=compression)
        if cA.a6:
            zf.write(f"media/{str(cA.a6)}", f"A6-{str(cA.user.curp)}.pdf", compress_type=compression)
        if cA.a7:
            zf.write(f"media/{str(cA.a7)}", f"A7-{str(cA.user.curp)}.pdf", compress_type=compression)
        if cA.a8:
            zf.write(f"media/{str(cA.a8)}", f"A8-{str(cA.user.curp)}.pdf", compress_type=compression)
        if cA.a9:
            zf.write(f"media/{str(cA.a9)}", f"A9-{str(cA.user.curp)}.pdf", compress_type=compression)
        if cA.a10:
            zf.write(f"media/{str(cA.a10)}", f"A10-{str(cA.user.curp)}.pdf", compress_type=compression)
    finally:
        zf.close()
    revisores.downloadZipFile = True
    revisores.save()
    return FileResponse(open(f"media/ZIPs/{str(cA.user.curp)}.zip", 'rb'), content_type='application/zip')

@login_required
def exportZipCatB(request, rev_id):
    try:
        cB = CategoriaB.objects.get(pk = rev_id)
        revisores = RevisoresCatB.objects.get(solicitud_id = rev_id)
    except:
        messages.error(request, "No se encontro la solicitud con este ID.")
        return redirect("vinculacion:revisor")
    
    try:
        compression = zipfile.ZIP_DEFLATED
    except:
        compression = zipfile.ZIP_STORED

    zf = zipfile.ZipFile(f"media/ZIPs/{str(cB.user.curp)}.zip", mode="w")
    
    try:
        if cB.b1:
            zf.write(f"media/{str(cB.b1)}", f"B1-{str(cB.user.curp)}.pdf", compress_type=compression)
        if cB.b2:
            zf.write(f"media/{str(cB.b2)}", f"B2-{str(cB.user.curp)}.pdf", compress_type=compression)
        if cB.b3:
            zf.write(f"media/{str(cB.b3)}", f"B3-{str(cB.user.curp)}.pdf", compress_type=compression)
        if cB.b4:
            zf.write(f"media/{str(cB.b4)}", f"B4-{str(cB.user.curp)}.pdf", compress_type=compression)
        if cB.b5:
            zf.write(f"media/{str(cB.b5)}", f"B5-{str(cB.user.curp)}.pdf", compress_type=compression)
        if cB.b6:
            zf.write(f"media/{str(cB.b6)}", f"B6-{str(cB.user.curp)}.pdf", compress_type=compression)
        if cB.b7:
            zf.write(f"media/{str(cB.b7)}", f"B7-{str(cB.user.curp)}.pdf", compress_type=compression)
        if cB.b8:
            zf.write(f"media/{str(cB.b8)}", f"B8-{str(cB.user.curp)}.pdf", compress_type=compression)
        if cB.b9:
            zf.write(f"media/{str(cB.b9)}", f"B9-{str(cB.user.curp)}.pdf", compress_type=compression)
        if cB.b10:
            zf.write(f"media/{str(cB.b10)}", f"B10-{str(cB.user.curp)}.pdf", compress_type=compression)
    finally:
        zf.close()
    revisores.downloadZipFile = True
    revisores.save()
    return FileResponse(open(f"media/ZIPs/{str(cB.user.curp)}.zip", 'rb'), content_type='application/zip')

def mostrar_cg(request, investigador_id):
    investigador = get_object_or_404(Investigador, user=investigador_id)
    filepath = os.path.join('media', '{0}'.format(investigador.grado.name))
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')

@user_passes_test(user_is_staff_member)
def constancia_sei(request, investigador_id):
    mes = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    investigador = get_object_or_404(Investigador, user_id = investigador_id)
    doc = DocxTemplate("static/doc/formato.docx")
    fullname = investigador.nombre_completo
    id_user = investigador.pk
    date = f"Zacatecas, Zac. a {datetime.datetime.today().day} de {mes[datetime.datetime.today().month - 1]} de {datetime.datetime.today().year}"
    context = {'fullname': fullname, 'id_user': id_user, 'fulldate': date}
    doc.render(context)
    output_docx = f"media/usuarios/investigadores/Constancias/Word/{investigador.curp}.docx"
    output_pdf = f"media/usuarios/investigadores/Constancias/{investigador.curp}.pdf"
    doc.save(output_docx)

    docxFile = Document(output_docx)
    temp_output_file = f"{os.path.splitext(output_docx)[0]}.pdf"
    docxFile.save(temp_output_file)

    try:
        subprocess.run(["unoconv", "-f", "pdf", "-o", output_pdf, temp_output_file], check=True)
    except:
        print("Error.")
    os.remove(temp_output_file)

    investigador.constancia = f"usuarios/investigadores/Constancias/{investigador.curp}.pdf"
    investigador.save();
    
    messages.success(request, "Constancia creada correctamente.")
    return redirect("administracion:investigadores_lista")

@login_required
def solicitud_realizada(request):
    messages.error(request, "Error, no puedes participar en 2 categorias al mismo tiempo.")
    return render(request, "solicitud_realizada.html")

@login_required
def errorEdad(request):
    return render(request, "edad-mayor.html")