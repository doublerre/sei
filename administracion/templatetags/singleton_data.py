from django import template
from administracion.models import Convocatoria

register = template.Library()


@register.simple_tag
def convocatorias_activas():
    return Convocatoria.objects.all()[0].activa
