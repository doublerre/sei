from django.contrib import admin
from investigadores.models import (
    Investigador,
    NivelInvestigador,
    Investigacion,
    SolicitudTrabajo)

# Register your models here.
admin.site.register(Investigador)
admin.site.register(NivelInvestigador)
admin.site.register(Investigacion)
admin.site.register(SolicitudTrabajo)
