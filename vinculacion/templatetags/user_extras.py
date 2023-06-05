from django import template
from investigadores.models import Investigador
from empresas.models import Empresa
from instituciones_educativas.models import InstitucionEducativa

register = template.Library()


@register.filter(name="user_image")
def user_image(usuario):
    if not usuario.tipo_usuario:
        return None

    tipo_usuario = "_".join(usuario.tipo_usuario.tipo.split()).lower()

    if tipo_usuario == "investigador":
        usuario_investigador = Investigador.objects.get(user=usuario)
        return usuario_investigador.imagen

    elif tipo_usuario == "empresa":
        usuario_empresa = Empresa.objects.get(encargado=usuario)
        return usuario_empresa.imagen

    elif tipo_usuario == "institucion_educativa":
        usuario_institucion = InstitucionEducativa.objects.get(
            encargado=usuario)
        return usuario_institucion.imagen

    else:
        return None
