from django.contrib import admin
from vinculacion.models import Categoria, Noticia, AreaConocimiento
from administracion.models import FechasPremios

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Noticia)
admin.site.register(AreaConocimiento)

admin.site.register(FechasPremios)