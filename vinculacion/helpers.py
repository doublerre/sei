import asyncio
from scholarly import scholarly, ProxyGenerator
from investigadores.models import Investigador
from empresas.models import Empresa
from instituciones_educativas.models import InstitucionEducativa
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from investigadores.models import (
    SolicitudTrabajo)
from usuarios.models import User
from django.utils import timezone


def get_author(user_id):
    pg = ProxyGenerator()
    pg.FreeProxies()
    scholarly.use_proxy(pg)

    try:
        return scholarly.search_author_id(user_id, filled=True)
    except Exception:
        return None


async def fetch_publication(publication_raw):
    try:
        publication = scholarly.fill(publication_raw)
        return publication
    except Exception:
        return None


async def get_publications(author):
    pg = ProxyGenerator()
    pg.FreeProxies()
    scholarly.use_proxy(pg)

    publicaciones = []

    for publication in author["publications"]:
        p = asyncio.create_task(fetch_publication(publication))
        publicaciones.append(p)

    res = await asyncio.gather(*publicaciones)
    publicaciones = []

    for publication in res:
        if not publication:
            continue

        titulo = publication.get("bib", {}).get("title")

        if not titulo:
            continue

        abstract = publication.get("bib", {}).get(
            "abstract", "Contenido no encontrado")
        pub_url = publication.get("pub_url")

        if pub_url:
            abstract += f"\n\nVer más: {pub_url}"

        publicaciones.append({
            "titulo": titulo,
            "contenido": abstract,
        })

    return publicaciones


def get_user_specific_data(usuario):
    tipo_usuario = "_".join(usuario.tipo_usuario.tipo.split()).lower()

    if tipo_usuario == "investigador":
        usuario_investigador = Investigador.objects.get(user=usuario)
        usuario_data = {
            'email': usuario_investigador.user.email,
            'imagen': usuario_investigador.imagen,
            'link_google_scholar': usuario_investigador.link_google_scholar,
            'curriculum_vitae': usuario_investigador.curriculum_vitae,
            'es_sei': usuario_investigador.es_sei,
            'es_sni': usuario_investigador.es_sni,
            'constancia': usuario_investigador.constancia
        }

    elif tipo_usuario == "empresa":
        usuario_empresa = Empresa.objects.get(encargado=usuario)
        usuario_data = {
            'email': usuario_empresa.encargado.email,
            'imagen': usuario_empresa.imagen,
        }

    elif tipo_usuario == "institucion_educativa":
        usuario_institucion = InstitucionEducativa.objects.get(
            encargado=usuario)
        usuario_data = {
            'email': usuario_institucion.encargado.email,
            'imagen': usuario_institucion.imagen,
        }

    return usuario_data
# Cambiar estados de trabajo


def cancelar_trabajo(pk, solicitud):
    if pk == solicitud.usuario_a_vincular.pk:
        solicitud.estado_investigador = "C"
        solicitud.estado = "C"
        solicitud.fecha_finalizado = timezone.now()

        empleador = User.objects.filter(
            pk=solicitud.usuario_solicitante.pk).first()
        empleado = User.objects.filter(
            pk=solicitud.usuario_a_vincular.pk).first()
        correos = [empleador.email, empleado.email]
        enviar_correo_estado(
            solicitud.pk,
            "Cancelación de trabajo",
            "El trabajo ha sido cancelado por el investigador",
            correos)
        solicitud.save()

    elif pk == solicitud.usuario_solicitante.pk:
        solicitud.estado_empleador = "C"
        solicitud.estado = "C"
        solicitud.fecha_finalizado = timezone.now()
        empleador = User.objects.filter(
            pk=solicitud.usuario_solicitante.pk).first()
        empleado = User.objects.filter(
            pk=solicitud.usuario_a_vincular.pk).first()
        correos = [empleador.email, empleado.email]
        enviar_correo_estado(
            solicitud.pk,
            "Cancelación de trabajo",
            "El trabajo ha sido cancelado por el solicitante",
            correos)
        solicitud.save()


def finalizar_trabajo(pk, solicitud):
    if pk == solicitud.usuario_a_vincular.pk:
        solicitud.estado_investigador = "F"
        solicitud.estado_empleador = "E"
        empleador = User.objects.filter(
            pk=solicitud.usuario_solicitante.pk).first()
        empleado = User.objects.filter(
            pk=solicitud.usuario_a_vincular.pk).first()
        correos = [empleador.email, empleado.email]
        enviar_correo_estado(
            solicitud.pk,
            "Finalización de trabajo",
            "El trabajo ha sido finalizado por el investigador",
            correos)
        solicitud.save()
    elif pk == solicitud.usuario_solicitante.pk:
        solicitud.estado_empleador = "F"
        solicitud.estado = "F"
        empleador = User.objects.filter(
            pk=solicitud.usuario_solicitante.pk).first()
        empleado = User.objects.filter(
            pk=solicitud.usuario_a_vincular.pk).first()
        correos = [empleador.email, empleado.email]
        enviar_correo_estado(
            solicitud.pk,
            "Finalización de trabajo",
            "El trabajo ha sido finalizado por el solicitante",
            correos)
        solicitud.save()


def rechazar_trabajo(pk, solicitud):
    if pk == solicitud.usuario_solicitante.pk:
        solicitud.estado_empleador = "R"
        solicitud.estado_investigador = "E"
        empleador = User.objects.filter(
            pk=solicitud.usuario_solicitante.pk).first()
        empleado = User.objects.filter(
            pk=solicitud.usuario_a_vincular.pk).first()
        correos = [empleador.email, empleado.email]

        enviar_correo_estado(
            solicitud.pk,
            "Rechazo de trabajo",
            "El trabajo ha sido rechazado por el solicitante",
            correos)
        solicitud.save()


def trabajo_en_proceso(pk, solicitud):
    if pk == solicitud.usuario_a_vincular.pk:
        solicitud.estado_investigador = "P"
        solicitud.estado = "P"
        empleador = User.objects.filter(
            pk=solicitud.usuario_solicitante.pk).first()
        empleado = User.objects.filter(
            pk=solicitud.usuario_a_vincular.pk).first()
        correos = [empleador.email, empleado.email]
        enviar_correo_estado(
            solicitud.pk,
            "Estado de trabajo en proceso",
            "El trabajo ha sido colocado en proceso por el investigador",
            correos)
        solicitud.save()


def trabajo_en_revision(pk, solicitud):
    if pk == solicitud.usuario_solicitante.pk:
        solicitud.estado_empleador = "E"
        empleador = User.objects.filter(
            pk=solicitud.usuario_solicitante.pk).first()
        empleado = User.objects.filter(
            pk=solicitud.usuario_a_vincular.pk).first()
        correos = [empleador.email, empleado.email]
        enviar_correo_estado(
            solicitud.pk,
            "Estado de trabajo en espera",
            "El trabajo ha sido colocado en revision por el solicitante",
            correos)
        solicitud.save()
    elif pk == solicitud.usuario_a_vincular.pk:
        solicitud.estado_investigador = "E"
        empleador = User.objects.filter(
            pk=solicitud.usuario_solicitante.pk).first()
        empleado = User.objects.filter(
            pk=solicitud.usuario_a_vincular.pk).first()
        correos = [empleador.email, empleado.email]
        enviar_correo_estado(
            solicitud.pk,
            "Estado de trabajo en espera",
            "El trabajo ha sido colocado en revision por el investigador",
            correos)
        solicitud.save()

# Envio de correo para notificar la finalización de un trabajo


def enviar_correo_estado(trabajo_pk, subject, message, remitentes):
    template = get_template("correo_cambio_estado.html")
    trabajo = SolicitudTrabajo.objects.get(pk=trabajo_pk)
    contenido = template.render({'trabajo': trabajo})
    correo = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=remitentes)
    correo.attach_alternative(contenido, "text/html")
    try:
        correo.send()
        return True
    except Exception:
        return False
