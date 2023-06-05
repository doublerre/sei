from pathlib import Path
from django.db import models
from usuarios.models import User, MUNICIPIOS
from vinculacion.models import Categoria
from administracion.validators import cp_validator


def rutaImagenEmpresa(instance, filename):
    extension = Path(filename).suffix
    return 'usuarios/empresas/empresa_{0}{1}'.format(
        instance.encargado.pk,
        extension)


# Create your models here.
class Empresa(models.Model):
    encargado = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True)
    nombre_empresa = models.CharField(max_length=80)
    especialidades = models.ManyToManyField(Categoria, blank=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    codigo_postal = models.CharField(max_length=5, validators=[cp_validator])
    municipio = models.IntegerField(choices=MUNICIPIOS)
    colonia = models.CharField(max_length=100)
    calle = models.CharField(max_length=100)
    numero_exterior = models.PositiveIntegerField()
    acerca_de = models.TextField(
        verbose_name="Acerca de",
        max_length=1000,
        default="")
    imagen = models.ImageField(
        upload_to=rutaImagenEmpresa,
        verbose_name="Imagen de perfil",
        blank=True,
        null=True,
        default=None)

    def __str__(self):
        return self.nombre_empresa
