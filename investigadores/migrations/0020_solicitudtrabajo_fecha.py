# Generated by Django 4.0.5 on 2022-11-04 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investigadores', '0019_alter_investigacion_titulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudtrabajo',
            name='fecha',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
