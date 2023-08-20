from pathlib import Path
from django.db import models
from vinculacion.models import Categoria
from usuarios.models import User, MUNICIPIOS
from investigadores.validators import curp_validador, google_scholar_link_valdador, limiteTamanioArchivo, limite10MbArchivo
from administracion.validators import cp_validator
from django.core.validators import FileExtensionValidator
import uuid


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

def rutaCGInvestigador(instance, filename):
    extension = Path(filename).suffix
    return 'usuarios/investigadores/CGs/{0}{1}'.format(
        instance.curp,
        extension
    )

def rutaCategoriaA(instance, filename):
    extension = Path(filename).suffix
    return 'usuarios/investigadores/CategoriaA/{0}{1}'.format(
        uuid.uuid4(),
        extension
    )

def rutaCategoriaB(instance, filename):
    extension = Path(filename).suffix
    return 'usuarios/investigadores/CategoriaB/{0}{1}'.format(
        uuid.uuid4(),
        extension
    )

def rutaConstanciaInvestigador(instance, filename):
    extension = Path(filename).suffix
    return 'usuarios/investigadores/Constancias/{0}{1}.'.format(
        instance.curp,
        extension
    )

ESTADOS_TRABAJO_FINALIZACION = [
    ("E", "En revisión"),
    ("P", "En proceso"),
    ("A", "Aceptada"),
    ("R", "Rechazada"),
    ("F", "Finalizada"),
]

ESTADOS_PREMIOS = [
    ("I", "En proceso"),
    ("E", "En revisión"),
    ("G", "Ganador"),
    ("F", "Finalizada"),
]

class Investigador(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name="Usuario",
        on_delete=models.CASCADE,
        primary_key=True)
    nombre_completo = models.CharField(max_length = 100, null=True, blank=True)
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
    es_sni = models.BooleanField(default = False)
    es_sei = models.BooleanField(default = False)
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
    grado = models.FileField(
        upload_to = rutaCGInvestigador,
        verbose_name="Comprobante de grado",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf']), limiteTamanioArchivo]
    )
    constancia = models.FileField(
        upload_to = rutaConstanciaInvestigador,
        verbose_name="Constancia SEI",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf']), limiteTamanioArchivo]
    )

    def __str__(self):
        return self.user.username

class CategoriaA(models.Model):
    user = models.ForeignKey(
        Investigador,
        verbose_name="Investigador",
        on_delete=models.CASCADE,
        unique=False)
    a1 = models.FileField(
        upload_to=rutaCategoriaA,
        verbose_name="Artículos científicos en revistas indexadas o arbitradas.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    a2 = models.FileField(
        upload_to=rutaCategoriaA,
        verbose_name="Autoría y coautoría de libros y/o capítulos de libros científicos con arbitraje.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    a3 = models.FileField(
        upload_to=rutaCategoriaA,
        verbose_name="Trámite de solicitud u obtención de patentes.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    a4 = models.FileField(
        upload_to=rutaCategoriaA,
        verbose_name="Trámite de solicitud u obtención de derechos de obtentor.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    a5 = models.FileField(
        upload_to=rutaCategoriaA,
        verbose_name="Desarrollo de software/hardware con Derechos de Autor.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    a6 = models.FileField(
        upload_to=rutaCategoriaA,
        verbose_name="Implementaciones tecnológicas",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    a7 = models.FileField(
        upload_to=rutaCategoriaA,
        verbose_name="Artículos o notas científicas publicadas en revistas arbitradas de divulgación científica o tecnológica.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    a8 = models.FileField(
        upload_to=rutaCategoriaA,
        verbose_name="Participación en proyectos de investigación, desarrollo tecnológico e innovación con financiamiento externo obtenido mediante convocatoria.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    a9 = models.FileField(
        upload_to=rutaCategoriaA,
        verbose_name="Editor, compilador o coordinador de libros colectivos.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    a10 = models.FileField(
        upload_to=rutaCategoriaA,
        verbose_name="Pertenencia al Sistema Nacional de Investigadores.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    estatus = models.CharField(
        choices= ESTADOS_PREMIOS,
        verbose_name="Estatus de la solicitud",
        default="I",
        max_length=1
    )
    anio = models.CharField(max_length = 5, null=True, blank=True)
    

    def __str__(self):
        return self.user.nombre_completo


class CategoriaB(models.Model):
    user = models.ForeignKey(
        Investigador,
        verbose_name="Investigador",
        on_delete=models.CASCADE,
        unique=False)
    b1 = models.FileField(
        upload_to=rutaCategoriaB,
        verbose_name="Obtención del grado académico de Doctorado o Maestría o Especialidad de los programas del SNP o en el extranjero con beca CONACYT.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    b2 = models.FileField(
        upload_to=rutaCategoriaB,
        verbose_name="Obtención del grado académico de Doctorado o Maestría o Especialidad de un programa nacional.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    b3 = models.FileField(
        upload_to=rutaCategoriaB,
        verbose_name="Dirección de Tesis o Artículo de Investigación de alumnos graduados en licenciatura, maestría, doctorado o especialidad médica.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    b4 = models.FileField(
        upload_to=rutaCategoriaB,
        verbose_name="Dirección de tesis de licenciatura de alumnos graduados en la modalidad de artículo científico.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    b5 = models.FileField(
        upload_to=rutaCategoriaB,
        verbose_name="Presentación de ponencias o carteles en eventos científicos, en México o el extranjero.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    b6 = models.FileField(
        upload_to=rutaCategoriaB,
        verbose_name="Estancias de investigación en instituciones académicas o de investigación.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    b7 = models.FileField(
        upload_to=rutaCategoriaB,
        verbose_name="Asignaturas con créditos impartidas en Especialidad, Maestría o Doctorado de programas del SNP.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    b8 = models.FileField(
        upload_to=rutaCategoriaB,
        verbose_name="Participación en proyectos de investigación con financiamiento interno o externo.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    b9 = models.FileField(
        upload_to=rutaCategoriaB,
        verbose_name="Publicación de artículos en revistas de divulgación científica o tecnológica no arbitradas.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    b10 = models.FileField(
        upload_to=rutaCategoriaB,
        verbose_name="Evaluación de trabajos de investigación o proyectos.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(['pdf'], limite10MbArchivo)]
    )
    estatus = models.CharField(
        choices= ESTADOS_PREMIOS,
        verbose_name="Estatus de la solicitud",
        default="I",
        max_length=1
    )
    anio = models.CharField(max_length = 5, null=True, blank=True)
    

    def __str__(self):
        return self.user.nombre_completo

class RevisoresCatA(models.Model):
    revisor = models.ForeignKey(
        User,
        verbose_name="Usuario Revisor",
        on_delete=models.CASCADE,
        unique=False
    )
    solicitud = models.ForeignKey(
        CategoriaA, 
        verbose_name="Solicitud Categoria",
        on_delete=models.CASCADE,
        unique=False
    )
    a1 = models.PositiveIntegerField(default=0, null=True, blank=True)
    a2 = models.PositiveIntegerField(default=0, null=True, blank=True)
    a3 = models.PositiveIntegerField(default=0, null=True, blank=True)
    a4 = models.PositiveIntegerField(default=0, null=True, blank=True)
    a5 = models.PositiveIntegerField(default=0, null=True, blank=True)
    a6 = models.PositiveIntegerField(default=0, null=True, blank=True)
    a7 = models.PositiveIntegerField(default=0, null=True, blank=True)
    a8 = models.PositiveIntegerField(default=0, null=True, blank=True)
    a9 = models.PositiveIntegerField(default=0, null=True, blank=True)
    a10 = models.PositiveIntegerField(default=0, null=True, blank=True)


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
