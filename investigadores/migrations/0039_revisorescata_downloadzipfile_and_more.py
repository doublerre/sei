# Generated by Django 4.1.3 on 2023-08-28 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investigadores', '0038_revisorescata_estatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='revisorescata',
            name='downloadZipFile',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='revisorescatb',
            name='downloadZipFile',
            field=models.BooleanField(default=False),
        ),
    ]
