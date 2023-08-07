from django.db import models


class Convocatoria(models.Model):
    activa = models.BooleanField()


class Contacto(models.Model):
    datos = models.TextField()


class AcercaDe(models.Model):
    datos = models.TextField()


class FechasPremios(models.Model):
    fecha_de_inicio: models.TextField(verbose_name="Fecha de inicio", max_length=25)
    fecha_de_fin: models.TextField(verbose_name="Fecha de cierre", max_length=25)