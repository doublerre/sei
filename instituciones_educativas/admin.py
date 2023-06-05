from django.contrib import admin
from instituciones_educativas.models import (
    InstitucionEducativa,
    SolicitudIngreso)

# Register your models here.

admin.site.register(InstitucionEducativa)
admin.site.register(SolicitudIngreso)
