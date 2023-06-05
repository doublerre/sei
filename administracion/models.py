from django.db import models


class Convocatoria(models.Model):
    activa = models.BooleanField()


class Contacto(models.Model):
    datos = models.TextField()


class AcercaDe(models.Model):
    datos = models.TextField()
