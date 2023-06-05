from pathlib import Path
from django.db import models
from vinculacion.models import Categoria
from usuarios.models import User, MUNICIPIOS
from investigadores.validators import curp_validador, google_scholar_link_valdador, limiteTamanioArchivo
from administracion.validators import cp_validator
from django.core.validators import FileExtensionValidator


class NivelInvestigador(models.Model):
    nivel = models.IntegerField()
    descripcion = models.TextField()

    def __str__(self):
        return "Nivel " + str(self.nivel)


def rutaImagenInvestigador(instance, filename):
    extension = Path(filename).suffix
    return 'usuarios/investigadores/investigador_{0}{1}'.format(
        instance.user.pk,
        extension)


def rutaCVInvestigador(instance, filename):
    extension = Path(filename).suffix
    return 'usuarios/investigadores/CVs/{0}{1}'.format(
        instance.curp,
        extension)

class Investigador(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name="Usuario",
        on_delete=models.CASCADE,
        primary_key=True)
    nivel = models.ForeignKey(NivelInvestigador,
                              on_delete=models.DO_NOTHING)
    curp = models.CharField(max_length=18,
                            validators=[curp_validador])
    latitud = models.FloatField()
    longitud = models.FloatField()
    codigo_postal = models.CharField(
        max_length=5,
        validators=[cp_validator])
    municipio = models.IntegerField(
        choices=MUNICIPIOS)
    colonia = models.CharField(max_length=100)
    calle = models.CharField(max_length=100)
    numero_exterior = models.PositiveIntegerField()
    acerca_de = models.TextField(
        verbose_name="Semblanza",
        max_length=1000,
        default="")
    imagen = models.ImageField(
        upload_to=rutaImagenInvestigador,
        verbose_name="Imagen de perfil",
        blank=True,
        null=True,
        default=None)
    link_google_scholar = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Link de su perfil en Google Scholar",
        validators=[google_scholar_link_valdador])
    curriculum_vitae = models.FileField(
        upload_to=rutaCVInvestigador,
        verbose_name="Curriculum Vitae",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator( ['pdf'] ), limiteTamanioArchivo ]
    )

    def __str__(self):
        return self.user.username


class Investigacion(models.Model):
    titulo = models.CharField(max_length=500)
    categorias = models.ManyToManyField(Categoria, blank=True)
    autores = models.ManyToManyField(Investigador, blank=True)
    contenido = models.TextField()

    def __str__(self):
        return self.titulo


class GrupoInvestigacion(models.Model):
    administradores = models.ManyToManyField(
        Investigador,
        related_name='%(class)s_administradores')
    integrantes = models.ManyToManyField(
        Investigador,
        related_name='%(class)s_integrantes')


ESTADOS = [
    ("E", "En espera"),
    ("A", "Aceptada"),
    ("P", "En proceso"),
    ("R", "Rechazada"),
    ("C", "Cancelada"),
]

ESTADOS_TRABAJO_FINALIZACION = [
    ("E", "En revisión"),
    ("P", "En proceso"),
    ("A", "Aceptada"),
    ("R", "Rechazada"),
    ("F", "Finalizada"),
]


class SolicitudTrabajo(models.Model):
    titulo = models.CharField(verbose_name="Título", max_length=200)
    descripcion = models.TextField(verbose_name="Descripción", max_length=5000)
    usuario_a_vincular = models.ForeignKey(
        Investigador,
        verbose_name="Usuario a vincular",
        on_delete=models.CASCADE)
    usuario_solicitante = models.ForeignKey(
        User,
        verbose_name="Usuario solicitante",
        on_delete=models.CASCADE)
    estado = models.CharField(
        choices=ESTADOS,
        verbose_name="Estado",
        max_length=1)
    estado_investigador = models.CharField(
        choices=ESTADOS_TRABAJO_FINALIZACION,
        verbose_name="Estado del investigador",
        default="A",
        max_length=1)
    estado_empleador = models.CharField(
        choices=ESTADOS_TRABAJO_FINALIZACION,
        verbose_name="Estado del empleador",
        default="P",
        max_length=1)
    descripcion = models.TextField(verbose_name="Descripción", max_length=5000)
    fecha = models.DateTimeField(auto_now=True)
    fecha_finalizado = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.titulo


class InvestigacionGoogleScholar(models.Model):
    investigador = models.ForeignKey("Investigador", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=500)

    class Meta:
        unique_together = ('investigador', 'titulo')
