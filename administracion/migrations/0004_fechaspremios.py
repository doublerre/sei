# Generated by Django 4.1.3 on 2023-08-07 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0003_convocatoria_activa'),
    ]

    operations = [
        migrations.CreateModel(
            name='FechasPremios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_de_inicio', models.TextField(verbose_name="Fecha de inicio", max_length=25)),
                ('fecha_de_fin', models.TextField(verbose_name="Fecha de cierre", max_length=25)),
            ],
        ),
    ]