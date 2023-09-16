from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from vinculacion.models import Noticia
from investigadores.models import Investigador, Investigacion, CategoriaA, CategoriaB, RevisoresCatA, RevisoresCatB
from usuarios.models import User, TipoUsuario
from empresas.models import Empresa
from vinculacion.models import Categoria
from instituciones_educativas.models import InstitucionEducativa
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from administracion.forms import (
    FormCategoria,
    FormNoticia,
    FormUser,
    FormContacto,
    FormAcercaDe,
    FormPremios
)
from administracion.user_tests import user_is_staff_member
from administracion.models import (
    Convocatoria,
    Contacto,
    AcercaDe,
    Premios
)
from investigadores.forms import (
    FormInvestigador,
    FormInvestigadorUpdate,
    FormInvestigacion,
)
from empresas.forms import (
    FormEmpresa,
    FormEmpresaUpdate,
)
from instituciones_educativas.forms import (
    FormInstitucionEducativa,
    FormInstitucionEducativaUpdate,
)
from django.contrib import messages
from administracion.helpers import (
    obtener_coordenadas,
    enviar_correo_respuesta_solicitud_ingreso
)
from django.utils import timezone as datetime
from investigadores.models import Investigador
from docxtpl import DocxTemplate
from docx import Document
import os
import subprocess
import datetime

@user_passes_test(user_is_staff_member)
def dashboard(request):
    usuarios = User.objects.all()
    usuarios_mes = {}
    usuarios_tipo = {}

    fecha_actual = datetime.datetime.now()
    mes_actual = "{}-{:02d}".format(fecha_actual.year, fecha_actual.month)
    usuarios_activos_mes = 0

    for usuario in usuarios:
        if usuario.last_login:
            mes_ultimo_login = "{}-{:02d}".format(
                usuario.last_login.year, usuario.last_login.month)
            if mes_actual == mes_ultimo_login:
                usuarios_activos_mes += 1

        mes_registro = "{}-{:02d}".format(usuario.date_joined.year,
                                          usuario.date_joined.month)
        if mes_registro not in usuarios_mes:
            usuarios_mes[mes_registro] = 0
        usuarios_mes[mes_registro] += 1
        tipo_usuario = (
            usuario.tipo_usuario if usuario.tipo_usuario
            else "Visitante")
        if tipo_usuario not in usuarios_tipo:
            usuarios_tipo[tipo_usuario] = 0
        usuarios_tipo[tipo_usuario] += 1

    registros_mes = [(k, v) for k, v in usuarios_mes.items()]
    registros_mes = sorted(
        registros_mes,
        key=lambda val: datetime.datetime.strptime(val[0], '%Y-%m'))
    actividad_usuarios = [("Activos este mes", usuarios_activos_mes),
                          ("Inactivos este mes",
                          len(usuarios) - usuarios_activos_mes)]
    solicitudes = {
        "investigadores": len(
            Investigador.objects.filter(user__aprobado=False)),
        "empresas": len(Empresa.objects.filter(encargado__aprobado=False)),
        "instituciones_educativas": len(
            InstitucionEducativa.objects.filter(encargado__aprobado=False)),
    }

    return render(
        request,
        "administracion/dashboard.html",
        {
            "registros_mes": registros_mes,
            "usuarios_tipo": usuarios_tipo.items(),
            "actividad_usuarios": actividad_usuarios,
            "solicitudes": solicitudes
        })


@user_passes_test(user_is_staff_member)
def aprobar_perfil(request, pk):
    mes = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    usuario = User.objects.get(pk=pk)
    investigador = Investigador.objects.get(user_id=pk)
    investigador.es_sei = True
    usuario.aprobado = True

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
    investigador.save()
    usuario.save()
    messages.success(request, "Solicitud aceptada")
    sitio = get_current_site(request)
    enviar_correo_respuesta_solicitud_ingreso(
        "Respuesta de solicitud de ingreso",
        "Su solicitud a sido aprobada por un administrador",
        [usuario.email],
        True,
        usuario,
        sitio
    )

    return redirect('administracion:dashboard')

@user_passes_test(user_is_staff_member)
def aprobar_empresa(request, pk):
    usuario = User.objects.get(pk=pk)
    usuario.aprobado = True
    usuario.save()
    messages.success(request, "Solicitud aceptada")
    sitio = get_current_site(request)
    enviar_correo_respuesta_solicitud_ingreso(
        "Respuesta de solicitud de ingreso",
        "Su solicitud a sido aprobada por un administrador",
        [usuario.email],
        True,
        usuario,
        sitio
    )

    return redirect('administracion:dashboard')

def perfil(request, id):
    investigador = Investigador.objects.get(user_id=id)
    return render(request, "administracion/perfil_en_revision.html", {"investigador": investigador})

@user_passes_test(user_is_staff_member)
def AsignarInvestigadores(request):
    fPremios = Premios.objects.first()
    if fPremios.fecha_fin >= datetime.date.today():
        messages.error(request, "La convocatoria sigue activa.")
        return redirect('administracion:dashboard')
    
    ReCatA = RevisoresCatA.objects.filter(estatus = "E")
    ReCatB = RevisoresCatB.objects.filter(estatus = "E")
    if ReCatA.count() >= 1 or ReCatB.count() >=1:
        messages.error(request, "Existen revisiones actualmente")
        return redirect('administracion:dashboard')
    
    revisores = User.objects.filter(es_revisor= True)
    cRevisores = revisores.count()
    categoriaA = CategoriaA.objects.filter(anio = datetime.date.today().year, estatus = "I")
    cCategoriaA = categoriaA.count()
    cont = 0
    indexRevisores = 0

    CantCatAPorR = cCategoriaA/cRevisores

    for elemento in categoriaA:
        elemento.estatus = "E"
        elemento.save()
        cont = cont + 1
        print(elemento)
        #Add code from new model 
        asignacion = RevisoresCatA.objects.create(revisor_id = revisores[indexRevisores].id, solicitud_id= elemento.id)
        asignacion.save
        if(indexRevisores == cRevisores - 1):
            cont = 0
        if cont == int(CantCatAPorR):
            cont = 0
            indexRevisores = indexRevisores + 1


    categoriaB = CategoriaB.objects.filter(anio = datetime.date.today().year, estatus = "I")
    cCategoriaB = categoriaB.count()
    cont = 0
    indexRevisores = 0

    CantCatBPorR = cCategoriaB/cRevisores

    for elemento in categoriaB:
        elemento.estatus = "E"
        elemento.save()
        cont = cont + 1
        asignacion = RevisoresCatB.objects.create(revisor_id = revisores[indexRevisores].id, solicitud_id= elemento.id)
        asignacion.save
        if(indexRevisores == cRevisores - 1):
            cont = 0
        if cont == int(CantCatBPorR):
            cont = 0
            indexRevisores = indexRevisores + 1
        
    messages.success(request, "Investigadores asignados exitosamente.")
    return redirect('administracion:dashboard')

@user_passes_test(user_is_staff_member)
def ListaCategoriaB(request):
    catB = RevisoresCatB.objects.filter(estatus="F").extra(select={'total': 'b1 + b2 + b3 + b4 + b5 + b6 + b7 + b8 + b9 + b10'}, order_by=('total',))
    return render(request, 'administracion/categoriab_lista.html', {"CategoriaB": catB})

@user_passes_test(user_is_staff_member)
def ListaCategoriaA(request):
    catA = RevisoresCatA.objects.filter(estatus="F").extra(select={'total': 'a1 + a2 + a3 + a4 + a5 + a6 + a7 + a8 + a9 + a10'}, order_by=('total',))
    return render(request, 'administracion/categoriaa_lista.html', {"CategoriaA": catA})

@user_passes_test(user_is_staff_member)
def GanadorCatA(request, id):
    CategoriaA.objects.filter(anio = datetime.date.today().year).update(estatus = "F")
    RevisoresCatA.objects.all().update(estatus = "I")
    CategoriaA.objects.filter(id = id).update(estatus = "G")
    messages.success(request, "El ganador ha sido publicado correctamente.")
    return redirect('administracion:premios-a-lista')

@user_passes_test(user_is_staff_member)
def GanadorCatB(request, id):
    CategoriaB.objects.filter(anio = datetime.date.today().year).update(estatus = "F")
    RevisoresCatB.objects.all().update(estatus = "I")
    CategoriaB.objects.filter(id = id).update(estatus = "G")
    messages.success(request, "El ganador ha sido publicado correctamente.")
    return redirect('administracion:premios-b-lista')

@user_passes_test(user_is_staff_member)
def ComentariosCatA(request, id):
    CatA = RevisoresCatA.objects.filter(pk = id).first()
    print(CatA)
    return render(request, "administracion/comentarios.html",{
        "Categoria": CatA,
        })

@user_passes_test(user_is_staff_member)
def ComentariosCatB(request, id):
    CatB = RevisoresCatB.objects.filter(pk = id).first()
    return render(request, "administracion/comentariosB.html",{
        "Categoria": CatB,
        })

# Usuarios


class UsuarioLista(UserPassesTestMixin, ListView):
    model = User
    template_name = "administracion/usuarios_lista.html"
    context_object_name = "usuarios"

    def test_func(self):
        return user_is_staff_member(self.request.user)


class UsuarioNuevo(UserPassesTestMixin, CreateView):
    model = User
    form_class = FormUser
    success_url = reverse_lazy('administracion:usuarios_lista')
    template_name = "administracion/formulario.html"
    extra_context = {"accion": "Crear", "nombre_modelo": "usuario"}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Usuario registrado correctamente")
        return redirect(self.success_url)


class UsuarioEditar(UserPassesTestMixin, UpdateView):
    model = User
    form_class = FormUser
    success_url = reverse_lazy('administracion:usuarios_lista')
    template_name = "administracion/formulario.html"
    extra_context = {"accion": "Editar", "nombre_modelo": "usuario"}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Usuario actualizado correctamente")
        return redirect(self.success_url)


class UsuarioEliminar(UserPassesTestMixin, DeleteView):
    model = User
    success_url = reverse_lazy('administracion:usuarios_lista')
    template_name = "administracion/confirm_delete.html"
    extra_context = {"nombre_modelo": "usuario"}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def post(self, request, *args, **kwargs):
        messages.success(self.request, "Usuario eliminado correctamente")
        return self.delete(request, *args, **kwargs)

# Investigadores


class InvestigadorLista(UserPassesTestMixin, ListView):
    model = Investigador
    context_object_name = "investigadores"
    queryset = Investigador.objects.filter(user__aprobado=True)
    template_name = "administracion/investigadores_lista.html"

    def test_func(self):
        return user_is_staff_member(self.request.user)


class InvestigadorSolicitud(UserPassesTestMixin, ListView):
    model = Investigador
    context_object_name = "investigadores"
    queryset = Investigador.objects.filter(user__aprobado=False)
    template_name = "administracion/investigadores_solicitud.html"

    def test_func(self):
        return user_is_staff_member(self.request.user)


class InvestigadorNuevo(UserPassesTestMixin, CreateView):
    model = Investigador
    form_class = FormInvestigador
    success_url = reverse_lazy('administracion:investigadores_lista')
    template_name = "administracion/formulario.html"
    extra_context = {"accion": "Crear",
                     "nombre_modelo": "investigador",
                     "formulario_archivos": True}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def form_valid(self, form):
        investigador = form.save(commit=False)
        coordenadas = obtener_coordenadas(form.cleaned_data)

        if not coordenadas:
            messages.error(
                self.request, "Error al obtener los datos de ubicación," +
                " por favor verifique que los datos de dirección ingresados " +
                " son correctos.")
            return super(InvestigadorNuevo, self).form_invalid(form)

        investigador.latitud = coordenadas.latitud
        investigador.longitud = coordenadas.longitud
        investigador.user.tipo_usuario = TipoUsuario.objects.get(
            tipo="Investigador")
        investigador.user.aprobado = True

        investigador.save()
        investigador.user.save()

        messages.success(self.request, "Investigador registrado correctamente")
        return redirect(self.success_url)


class InvestigadorEditar(UserPassesTestMixin, UpdateView):
    model = Investigador
    form_class = FormInvestigadorUpdate
    success_url = reverse_lazy('administracion:investigadores_lista')
    template_name = "administracion/formulario.html"
    extra_context = {"accion": "Editar",
                     "nombre_modelo": "investigador",
                     "formulario_archivos": True}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def form_valid(self, form):
        investigador = form.save(commit=False)
        coordenadas = obtener_coordenadas(form.cleaned_data)

        if not coordenadas:
            messages.error(
                self.request, "Error al obtener los datos de ubicación," +
                " por favor verifique que los datos de dirección ingresados " +
                " son correctos.")
            return super(InvestigadorEditar, self).form_invalid(form)

        investigador.latitud = coordenadas.latitud
        investigador.longitud = coordenadas.longitud

        investigador.save()

        messages.success(
            self.request, "Investigador actualizado correctamente")
        return redirect(self.success_url)


class InvestigadorEliminar(UserPassesTestMixin, DeleteView):
    model = Investigador
    success_url = reverse_lazy('administracion:investigadores_lista')
    template_name = "administracion/confirm_delete.html"
    extra_context = {"nombre_modelo": "investigador"}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def post(self, request, *args, **kwargs):

        investigador = self.get_object()
        sitio = get_current_site(self.request)
        enviar_correo_respuesta_solicitud_ingreso(
            "Respuesta de solicitud de ingreso",
            "Su solicitud a sido rechazada por un administrador",
            [investigador.user.email],
            False,
            investigador.user,
            sitio
        )
        investigador.user.tipo_usuario = None
        investigador.user.aprobado = False
        investigador.user.save()

        messages.success(self.request, "Investigador eliminado correctamente")
        return self.delete(request, *args, **kwargs)

# Empresas


class EmpresaLista(UserPassesTestMixin, ListView):
    model = Empresa
    context_object_name = "empresas"
    queryset = Empresa.objects.filter(encargado__aprobado=True)
    template_name = "administracion/empresas_lista.html"

    def test_func(self):
        return user_is_staff_member(self.request.user)


class EmpresaSolicitud(UserPassesTestMixin, ListView):
    model = Empresa
    context_object_name = "empresas"
    queryset = Empresa.objects.filter(encargado__aprobado=False)
    template_name = "administracion/empresas_solicitud.html"

    def test_func(self):
        return user_is_staff_member(self.request.user)


class EmpresaNuevo(UserPassesTestMixin, CreateView):
    model = Empresa
    form_class = FormEmpresa
    success_url = reverse_lazy('administracion:empresas_lista')
    template_name = "administracion/formulario.html"
    extra_context = {"accion": "Crear",
                     "nombre_modelo": "empresa", "formulario_archivos": True}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def form_valid(self, form):
        empresa = form.save(commit=False)
        coordenadas = obtener_coordenadas(form.cleaned_data)

        if not coordenadas:
            messages.error(
                self.request, "Error al obtener los datos de ubicación," +
                " por favor verifique que los datos de dirección ingresados " +
                " son correctos.")
            return super(EmpresaNuevo, self).form_invalid(form)

        empresa.latitud = coordenadas.latitud
        empresa.longitud = coordenadas.longitud
        empresa.encargado.tipo_usuario = TipoUsuario.objects.get(
            tipo="Empresa")
        empresa.encargado.aprobado = True

        empresa.save()
        empresa.encargado.save()
        form.save_m2m()

        messages.success(self.request, "Empresa registrada correctamente")
        return redirect(self.success_url)


class EmpresaEditar(UserPassesTestMixin, UpdateView):
    model = Empresa
    form_class = FormEmpresaUpdate
    success_url = reverse_lazy('administracion:empresas_lista')
    template_name = "administracion/formulario.html"
    extra_context = {"accion": "Editar",
                     "nombre_modelo": "empresa", "formulario_archivos": True}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def form_valid(self, form):
        empresa = form.save(commit=False)
        coordenadas = obtener_coordenadas(form.cleaned_data)

        if not coordenadas:
            messages.error(
                self.request, "Error al obtener los datos de ubicación," +
                " por favor verifique que los datos de dirección ingresados " +
                " son correctos.")
            return super(EmpresaEditar, self).form_invalid(form)

        empresa.latitud = coordenadas.latitud
        empresa.longitud = coordenadas.longitud

        empresa.save()
        form.save_m2m()

        messages.success(self.request, "Empresa actualizada correctamente")
        return redirect(self.success_url)


class EmpresaEliminar(UserPassesTestMixin, DeleteView):
    model = Empresa
    success_url = reverse_lazy('administracion:empresas_lista')
    template_name = "administracion/confirm_delete.html"
    extra_context = {"nombre_modelo": "empresa"}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def post(self, request, *args, **kwargs):

        empresa = self.get_object()
        sitio = get_current_site(self.request)
        enviar_correo_respuesta_solicitud_ingreso(
            "Respuesta de solicitud de ingreso",
            "Su solicitud a sido rechazada por un administrador",
            [empresa.encargado.email],
            False,
            empresa.encargado,
            sitio
        )
        empresa.encargado.tipo_usuario = None
        empresa.encargado.aprobado = False
        empresa.encargado.save()

        messages.success(self.request, "Empresa eliminada correctamente")
        return self.delete(request, *args, **kwargs)

# Instituciones Educativas


class InstitucionEducativaLista(UserPassesTestMixin, ListView):
    model = InstitucionEducativa
    context_object_name = "instituciones_educativas"
    queryset = InstitucionEducativa.objects.filter(encargado__aprobado=True)
    template_name = "administracion/instituciones_educativas_lista.html"

    def test_func(self):
        return user_is_staff_member(self.request.user)


class InstitucionEducativaSolicitud(UserPassesTestMixin, ListView):
    model = InstitucionEducativa
    context_object_name = "instituciones_educativas"
    queryset = InstitucionEducativa.objects.filter(encargado__aprobado=False)
    template_name = "administracion/instituciones_educativas_solicitud.html"

    def test_func(self):
        return user_is_staff_member(self.request.user)


class InstitucionEducativaNuevo(UserPassesTestMixin, CreateView):
    model = InstitucionEducativa
    form_class = FormInstitucionEducativa
    success_url = reverse_lazy('administracion:instituciones_educativas_lista')
    template_name = "administracion/formulario.html"
    extra_context = {"accion": "Crear",
                     "nombre_modelo": "institución educativa",
                     "formulario_archivos": True}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def form_valid(self, form):
        institucion_educativa = form.save(commit=False)
        coordenadas = obtener_coordenadas(form.cleaned_data)

        if not coordenadas:
            messages.error(
                self.request, "Error al obtener los datos de ubicación," +
                " por favor verifique que los datos de dirección ingresados " +
                " son correctos.")
            return super(InstitucionEducativaNuevo, self).form_invalid(form)

        institucion_educativa.latitud = coordenadas.latitud
        institucion_educativa.longitud = coordenadas.longitud
        institucion_educativa.encargado.tipo_usuario = TipoUsuario.objects.get(
            tipo="Institucion Educativa")
        institucion_educativa.encargado.aprobado = True

        institucion_educativa.save()
        institucion_educativa.encargado.save()
        form.save_m2m()

        messages.success(
            self.request, "Institución Educativa registrada correctamente")
        return redirect(self.success_url)


class InstitucionEducativaEditar(UserPassesTestMixin, UpdateView):
    model = InstitucionEducativa
    form_class = FormInstitucionEducativaUpdate
    success_url = reverse_lazy('administracion:instituciones_educativas_lista')
    template_name = "administracion/formulario.html"
    extra_context = {"accion": "Editar",
                     "nombre_modelo": "institución educativa",
                     "formulario_archivos": True}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def form_valid(self, form):
        institucion_educativa = form.save(commit=False)
        coordenadas = obtener_coordenadas(form.cleaned_data)

        if not coordenadas:
            messages.error(
                self.request, "Error al obtener los datos de ubicación," +
                " por favor verifique que los datos de dirección ingresados " +
                " son correctos.")
            return super(InstitucionEducativaEditar, self).form_invalid(form)

        institucion_educativa.latitud = coordenadas.latitud
        institucion_educativa.longitud = coordenadas.longitud

        institucion_educativa.save()
        form.save_m2m()

        messages.success(
            self.request, "Institución Educativa actualizada correctamente")
        return redirect(self.success_url)


class InstitucionEducativaEliminar(UserPassesTestMixin, DeleteView):
    model = InstitucionEducativa
    success_url = reverse_lazy('administracion:instituciones_educativas_lista')
    template_name = "administracion/confirm_delete.html"
    extra_context = {"nombre_modelo": "institución educativa"}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def post(self, request, *args, **kwargs):
        institucion_educativa = self.get_object()
        sitio = get_current_site(self.request)
        enviar_correo_respuesta_solicitud_ingreso(
            "Respuesta de solicitud de ingreso",
            "Su solicitud a sido rechazada por un administrador",
            [institucion_educativa.encargado.email],
            False,
            institucion_educativa.encargado,
            sitio
        )
        institucion_educativa.encargado.tipo_usuario = None
        institucion_educativa.encargado.aprobado = False
        institucion_educativa.encargado.save()

        messages.success(
            self.request, "Institución Educativa eliminada correctamente")
        return self.delete(request, *args, **kwargs)

# Categorias


class CategoriaLista(UserPassesTestMixin, ListView):
    model = Categoria
    context_object_name = "categorias"
    template_name = "administracion/categorias_lista.html"

    def test_func(self):
        return user_is_staff_member(self.request.user)


class CategoriaNuevo(UserPassesTestMixin, CreateView):
    model = Categoria
    form_class = FormCategoria
    success_url = reverse_lazy('administracion:categorias_lista')
    template_name = "administracion/formulario.html"
    extra_context = {"accion": "Crear", "nombre_modelo": "categoria"}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Categoría registrada correctamente")
        return redirect(self.success_url)


class CategoriaEditar(UserPassesTestMixin, UpdateView):
    model = Categoria
    form_class = FormCategoria
    success_url = reverse_lazy('administracion:categorias_lista')
    template_name = "administracion/formulario.html"
    extra_context = {"accion": "Editar", "nombre_modelo": "categoria"}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Categoría actualizada correctamente")
        return redirect(self.success_url)


class CategoriaEliminar(UserPassesTestMixin, DeleteView):
    model = Categoria
    success_url = reverse_lazy('administracion:categorias_lista')
    template_name = "administracion/confirm_delete.html"
    extra_context = {"nombre_modelo": "categoria"}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def post(self, request, *args, **kwargs):
        messages.success(self.request, "Categoría eliminada correctamente")
        return self.delete(request, *args, **kwargs)

# Investigaciones


class InvestigacionLista(UserPassesTestMixin, ListView):
    model = Investigacion
    context_object_name = "investigaciones"
    template_name = "administracion/investigaciones_lista.html"

    def test_func(self):
        return user_is_staff_member(self.request.user)


class InvestigacionNuevo(UserPassesTestMixin, CreateView):
    model = Investigacion
    form_class = FormInvestigacion
    success_url = reverse_lazy('administracion:investigaciones_lista')
    template_name = "administracion/formulario.html"
    extra_context = {"accion": "Crear", "nombre_modelo": "investigacion"}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, "Investigación registrada correctamente")
        return redirect(self.success_url)


class InvestigacionEditar(UserPassesTestMixin, UpdateView):
    model = Investigacion
    form_class = FormInvestigacion
    success_url = reverse_lazy('administracion:investigaciones_lista')
    template_name = "administracion/formulario.html"
    extra_context = {"accion": "Editar", "nombre_modelo": "investigacion"}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, "Investigación actualizada correctamente")
        return redirect(self.success_url)


class InvestigacionEliminar(UserPassesTestMixin, DeleteView):
    model = Investigacion
    success_url = reverse_lazy('administracion:investigaciones_lista')
    template_name = "administracion/confirm_delete.html"
    extra_context = {"nombre_modelo": "investigacion"}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def post(self, request, *args, **kwargs):
        messages.success(self.request, "Investigación eliminada correctamente")
        return self.delete(request, *args, **kwargs)


class NoticiaLista(UserPassesTestMixin, ListView):
    model = Noticia
    context_object_name = "noticias"
    template_name = "administracion/noticias_lista.html"

    def test_func(self):
        return user_is_staff_member(self.request.user)


class NoticiaNueva(UserPassesTestMixin, CreateView):
    model = Noticia
    form_class = FormNoticia
    success_url = reverse_lazy('administracion:noticias_lista')
    template_name = "administracion/formulario.html"
    extra_context = {"accion": "Crear",
                     "nombre_modelo": "noticia", "formulario_archivos": True}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Noticia registrada correctamente")
        return redirect(self.success_url)


class NoticiaEditar(UserPassesTestMixin, UpdateView):
    model = Noticia
    form_class = FormNoticia
    success_url = reverse_lazy('administracion:noticias_lista')
    template_name = "administracion/formulario.html"
    extra_context = {"accion": "Crear",
                     "nombre_modelo": "noticia", "formulario_archivos": True}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Noticia actualizada correctamente")
        return redirect(self.success_url)


class NoticiaEliminar(UserPassesTestMixin, DeleteView):
    model = Noticia
    success_url = reverse_lazy('administracion:noticias_lista')
    template_name = "administracion/confirm_delete.html"
    extra_context = {"nombre_modelo": "noticia"}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def post(self, request, *args, **kwargs):
        messages.success(self.request, "Noticia eliminada correctamente")
        return self.delete(request, *args, **kwargs)


# Misc

class ContactoEditar(UserPassesTestMixin, UpdateView):
    model = Contacto
    form_class = FormContacto
    success_url = reverse_lazy('administracion:dashboard')
    template_name = "administracion/formulario.html"
    extra_context = {"accion": "Editar",
                     "nombre_modelo": "información de contacto",
                     "formulario_archivos": False,
                     "menu_activo": "contacto"}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def get_object(self):
        return Contacto.objects.all()[0]

    def form_valid(self, form):
        form.save()

        messages.success(self.request, "Información de contacto actualizada")
        return redirect(self.success_url)


class AcercaDeEditar(UserPassesTestMixin, UpdateView):
    model = AcercaDe
    form_class = FormAcercaDe
    success_url = reverse_lazy('administracion:dashboard')
    template_name = "administracion/formulario.html"
    extra_context = {"accion": "Editar",
                     "nombre_modelo": "acerca de",
                     "formulario_archivos": False,
                     "menu_activo": "acerca_de"}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def get_object(self):
        return AcercaDe.objects.all()[0]

    def form_valid(self, form):
        form.save()

        messages.success(self.request, "Información acerca de actualizada")
        return redirect(self.success_url)

class FechaPremiosEditar(UserPassesTestMixin, UpdateView):
    model = Premios
    form_class = FormPremios
    success_url = reverse_lazy('administracion:dashboard')
    template_name = "administracion/formulario.html"
    extra_context = {"accion": "Editar",
                     "nombre_modelo": "Fecha para obtención de premios",
                     "formulario_archivos": False,
                     "menu_activo": "premios"}

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def get_object(self):
        return Premios.objects.first()

    def form_valid(self, form):
        form.save()

        messages.success(self.request, "Fechas actualizadas con exito")
        return redirect(self.success_url)


class CambiarEstadoConvocatoria(UserPassesTestMixin, View):

    def test_func(self):
        return user_is_staff_member(self.request.user)

    def post(self, request):
        convocatoria = Convocatoria.objects.all()[0]
        convocatoria.activa = not convocatoria.activa
        convocatoria.save()
        print(convocatoria.activa)
        return redirect("administracion:dashboard")
