# Generated by Django 4.2.6 on 2024-03-11 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seajb', '0011_alter_armas_calibres'),
    ]

    operations = [
        migrations.AlterField(
            model_name='armas',
            name='calibreS',
            field=models.TextField(null=True, verbose_name='Tipo,Modelo,Calibre:'),
        ),
    ]
