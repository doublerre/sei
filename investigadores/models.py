from pathlib import Path
from django.db import models
from vinculacion.models import Categoria
from usuarios.models import User, MUNICIPIOS
from investigadores.validators import curp_validador, google_scholar_link_valdador, limiteTamanioArchivo, limite10MbArchivo
from administracion.validators import cp_validator
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator, MinLengthValidator
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

BOOLEAN_STATE = [
    ("True", "Si"),
    ("False", "No"),
]

CHOICES = [
    ([0, '0']),
    ([1, '1']),
    ([2, '2']),
    ([3, '3']),
    ([4, '4']),
    ([5, '5']),
    ([6, '6']),
    ([7, '7']),
    ([8, '8']),
    ([9, '9']),
    ([10, '10']),
]

CHOICES2 = [
    ([0, '0']),
    ([1, '1']),
    ([2, '2']),
    ([3, '3']),
    ([4, '4']),
    ([5, '5']),
]

CHOICES3 = [
    ([0, '0']),
    ([1, '1']),
    ([2, '2']),
    ([3, '3']),
    ([4, '4']),
    ([5, '5']),
    ([6, '6']),
    ([7, '7']),
    ([8, '8']),
    ([9, '9']),
    ([10, '10']),
    ([11, '11']),
    ([12, '12']),
    ([13, '13']),
    ([14, '14']),
    ([15, '15']),
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
    es_sni = models.CharField(default = False, max_length=6, choices=BOOLEAN_STATE, verbose_name="¿Esta adscrito al Sistema Nacional de Investigadores (SNI)?")
    es_prodep = models.CharField(default = False, max_length=6, choices=BOOLEAN_STATE, verbose_name="¿Esta adscrito al Programa para el Desarrollo Profecional Docente (PRODEP)?")
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
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
    )
    a2 = models.FileField(
        upload_to=rutaCategoriaA,
        verbose_name="Autoría y coautoría de libros y/o capítulos de libros científicos con arbitraje.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
    )
    a3 = models.FileField(
        upload_to=rutaCategoriaA,
        verbose_name="Trámite de solicitud u obtención de patentes.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
    )
    a4 = models.FileField(
        upload_to=rutaCategoriaA,
        verbose_name="Trámite de solicitud u obtención de derechos de obtentor.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
    )
    a5 = models.FileField(
        upload_to=rutaCategoriaA,
        verbose_name="Desarrollo de software/hardware con Derechos de Autor.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
    )
    a6 = models.FileField(
        upload_to=rutaCategoriaA,
        verbose_name="Implementaciones tecnológicas",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
    )
    a7 = models.FileField(
        upload_to=rutaCategoriaA,
        verbose_name="Artículos o notas científicas publicadas en revistas arbitradas de divulgación científica o tecnológica.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
    )
    a8 = models.FileField(
        upload_to=rutaCategoriaA,
        verbose_name="Participación en proyectos de investigación, desarrollo tecnológico e innovación con financiamiento externo obtenido mediante convocatoria.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
    )
    a9 = models.FileField(
        upload_to=rutaCategoriaA,
        verbose_name="Editor, compilador o coordinador de libros colectivos.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
    )
    a10 = models.FileField(
        upload_to=rutaCategoriaA,
        verbose_name="Pertenencia al Sistema Nacional de Investigadores.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
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
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
    )
    b2 = models.FileField(
        upload_to=rutaCategoriaB,
        verbose_name="Obtención del grado académico de Doctorado o Maestría o Especialidad de un programa nacional.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
    )
    b3 = models.FileField(
        upload_to=rutaCategoriaB,
        verbose_name="Dirección de Tesis o Artículo de Investigación de alumnos graduados en licenciatura, maestría, doctorado o especialidad médica.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
    )
    b4 = models.FileField(
        upload_to=rutaCategoriaB,
        verbose_name="Dirección de tesis de licenciatura de alumnos graduados en la modalidad de artículo científico.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
    )
    b5 = models.FileField(
        upload_to=rutaCategoriaB,
        verbose_name="Presentación de ponencias o carteles en eventos científicos, en México o el extranjero.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
    )
    b6 = models.FileField(
        upload_to=rutaCategoriaB,
        verbose_name="Estancias de investigación en instituciones académicas o de investigación.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
    )
    b7 = models.FileField(
        upload_to=rutaCategoriaB,
        verbose_name="Asignaturas con créditos impartidas en Especialidad, Maestría o Doctorado de programas del SNP.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
    )
    b8 = models.FileField(
        upload_to=rutaCategoriaB,
        verbose_name="Participación en proyectos de investigación con financiamiento interno o externo.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
    )
    b9 = models.FileField(
        upload_to=rutaCategoriaB,
        verbose_name="Publicación de artículos en revistas de divulgación científica o tecnológica no arbitradas.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
    )
    b10 = models.FileField(
        upload_to=rutaCategoriaB,
        verbose_name="Evaluación de trabajos de investigación o proyectos.",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator( ['pdf']), limite10MbArchivo]
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
    a1 = models.PositiveIntegerField(default=0, choices=CHOICES, verbose_name="A1 - Artículos científicos en revistas indexadas o arbitradas.", validators=[MinValueValidator(0), MaxValueValidator(10)])
    a1_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo A1 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    a2 = models.PositiveIntegerField(default=0, choices=CHOICES, verbose_name="A2 - Autoría y coautoría de libros y/o capítulos de libros científicos con arbitraje.", validators=[MinValueValidator(0), MaxValueValidator(10)])
    a2_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo A2 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    a3 = models.PositiveIntegerField(default=0, choices=CHOICES, verbose_name="A3 - Trámite de solicitud u obtención de patentes.", validators=[MinValueValidator(0), MaxValueValidator(10)])
    a3_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo A3 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    a4 = models.PositiveIntegerField(default=0, choices=CHOICES, verbose_name="A4 - Trámite de solicitud u obtención de derechos de obtentor.", validators=[MinValueValidator(0), MaxValueValidator(10)])
    a4_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo A4 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    a5 = models.PositiveIntegerField(default=0, choices=CHOICES, verbose_name="A5 - Desarrollo de software/hardware con Derechos de Autor.", validators=[MinValueValidator(0), MaxValueValidator(10)])
    a5_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo A5 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    a6 = models.PositiveIntegerField(default=0, choices=CHOICES, verbose_name="A6 - Implementaciones tecnológicas", validators=[MinValueValidator(0), MaxValueValidator(10)])
    a6_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo A6 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    a7 = models.PositiveIntegerField(default=0, choices=CHOICES, verbose_name="A7 - Artículos o notas científicas publicadas en revistas arbitradas de divulgación científica o tecnológica.", validators=[MinValueValidator(0), MaxValueValidator(10)])
    a7_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo A7 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    a8 = models.PositiveIntegerField(default=0, choices=CHOICES, verbose_name="A8 - Participación en proyectos de investigación, desarrollo tecnológico e innovación con financiamiento externo obtenido mediante convocatoria.", validators=[MinValueValidator(0), MaxValueValidator(10)])
    a8_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo A8 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    a9 = models.PositiveIntegerField(default=0, choices=CHOICES, verbose_name="A9 - Editor, compilador o coordinador de libros colectivos.", validators=[MinValueValidator(0), MaxValueValidator(10)])
    a9_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo A9 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    a10 = models.PositiveIntegerField(default=0, choices=CHOICES, verbose_name="A10 - Pertenencia al Sistema Nacional de Investigadores.", validators=[MinValueValidator(0), MaxValueValidator(10)])
    a10_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo A10 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    estatus = models.CharField(
        choices= ESTADOS_PREMIOS,
        verbose_name="Estatus de la revisión",
        default="E",
        max_length=1
    )
    downloadZipFile = models.BooleanField(default=False)

class RevisoresCatB(models.Model):
    revisor = models.ForeignKey(
        User,
        verbose_name="Usuario Revisor",
        on_delete=models.CASCADE,
        unique=False
    )
    solicitud = models.ForeignKey(
        CategoriaB, 
        verbose_name="Solicitud Categoria",
        on_delete=models.CASCADE,
        unique=False
    )
    b1 = models.PositiveIntegerField(default=0, choices=CHOICES3, verbose_name="B1 - Obtención del grado académico de Doctorado o Maestría o Especialidad de los programas del SNP o en el extranjero con beca CONACYT.")
    b1_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo B1 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    b2 = models.PositiveIntegerField(default=0, choices=CHOICES2, verbose_name="B2 - Obtención del grado académico de Doctorado o Maestría o Especialidad de un programa nacional.")
    b2_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo B2 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    b3 = models.PositiveIntegerField(default=0, choices=CHOICES, verbose_name="B3 - Dirección de Tesis o Artículo de Investigación de alumnos graduados en licenciatura, maestría, doctorado o especialidad médica.")
    b3_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo B3 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    b4 = models.PositiveIntegerField(default=0, choices=CHOICES, verbose_name="B4 - Dirección de tesis de licenciatura de alumnos graduados en la modalidad de artículo científico.")
    b4_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo B4 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    b5 = models.PositiveIntegerField(default=0, choices=CHOICES, verbose_name="B5 - Presentación de ponencias o carteles en eventos científicos, en México o el extranjero.")
    b5_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo B5 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    b6 = models.PositiveIntegerField(default=0, choices=CHOICES3, verbose_name="B6 - Estancias de investigación en instituciones académicas o de investigación.")
    b6_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo B6 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    b7 = models.PositiveIntegerField(default=0, choices=CHOICES, verbose_name="B7 - Asignaturas con créditos impartidas en Especialidad, Maestría o Doctorado de programas del SNP.")
    b7_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo B7 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    b8 = models.PositiveIntegerField(default=0, choices=CHOICES, verbose_name="B8 - Participación en proyectos de investigación con financiamiento interno o externo.")
    b8_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo B8 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    b9 = models.PositiveIntegerField(default=0, choices=CHOICES2, verbose_name="B9 - Publicación de artículos en revistas de divulgación científica o tecnológica no arbitradas.")
    b9_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo B9 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    b10 = models.PositiveIntegerField(default=0, choices=CHOICES, verbose_name="B10 - Evaluación de trabajos de investigación o proyectos.")
    b10_comentario = models.TextField(
        verbose_name="Retroalimentación de la documentación enviada correspondiente al campo B10 (Minimo 250 caracteres)",
        max_length=2000,
        null=False, blank=False,
        default="",
        validators=[MinLengthValidator(250)])
    estatus = models.CharField(
        choices= ESTADOS_PREMIOS,
        verbose_name="Estatus de la revisión",
        default="E",
        max_length=1
    )
    downloadZipFile = models.BooleanField(default=False)

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
