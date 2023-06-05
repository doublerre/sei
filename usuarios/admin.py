from django.contrib import admin
from usuarios.models import User, TipoUsuario

# Register your models here.
admin.site.register(User)
admin.site.register(TipoUsuario)
