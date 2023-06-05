from django.db import models


class AreaConocimiento(models.Model):
    nombre = models.CharField(max_length=70)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=30)
    area_conocimiento = models.ForeignKey(
        AreaConocimiento,
        verbose_name="Área de conocimiento",
        on_delete=models.CASCADE)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Noticia(models.Model):
    titulo = models.CharField(verbose_name="Título", max_length=65)
    contenido = models.TextField(verbose_name="Contenido", max_length=5000)
    fecha = models.DateField(verbose_name="Fecha", auto_now=True)
    escritor = models.ForeignKey(
        'usuarios.User',
        verbose_name="Escritor",
        on_delete=models.DO_NOTHING)
    imagen = models.ImageField(upload_to="noticias/", verbose_name="Imagen")

    def __str__(self):
        return self.titulo
