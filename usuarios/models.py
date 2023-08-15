from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


class TipoUsuario(models.Model):
    tipo = models.CharField(max_length=30)

    def __str__(self):
        return self.tipo


class User(AbstractUser):
    tipo_usuario = models.ForeignKey(
        TipoUsuario,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True)
    email = models.EmailField(unique=True)
    password = models.TextField(
        validators=[MinLengthValidator(8)]
    )
    aprobado = models.BooleanField(default=False)
    es_revisor = models.BooleanField(default = False)

    def __str__(self):
        return self.username


MUNICIPIOS = list(enumerate([
    "Apozol",
    "Apulco",
    "Atolinga",
    "Benito Juárez",
    "Calera",
    "Cañitas de Felipe Pescador",
    "Concepción del Oro",
    "Cuauhtémoc",
    "Chalchihuites",
    "Fresnillo",
    "Trinidad García de la Cadena",
    "Genaro Codina",
    "General Enrique Estrada",
    "General Francisco R. Murguía",
    "El Plateado de Joaquín Amaro",
    "General Pánfilo Natera",
    "Guadalupe",
    "Huanusco",
    "Jalpa",
    "Jerez",
    "Jiménez del Teul",
    "Juan Aldama",
    "Juchipila",
    "Loreto",
    "Luis Moya",
    "Mazapil",
    "Melchor Ocampo",
    "Mezquital del Oro",
    "Miguel Auza",
    "Momax",
    "Monte Escobedo",
    "Morelos",
    "Moyahua de Estrada",
    "Nochistlán de Mejía",
    "Noria de Ángeles",
    "Ojocaliente",
    "Pánuco",
    "Pinos",
    "Río Grande",
    "Sain Alto",
    "El Salvador",
    "Sombrerete",
    "Susticacán",
    "Tabasco",
    "Tepechitlán",
    "Tepetongo",
    "Teúl de González Ortega",
    "Tlaltenango de Sánchez Román",
    "Valparaíso",
    "Vetagrande",
    "Villa de Cos",
    "Villa García",
    "Villa González Ortega",
    "Villa Hidalgo",
    "Villanueva",
    "Zacatecas",
    "Trancoso",
    "Santa María de la Paz"
]))
