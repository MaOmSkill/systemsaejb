# Generated by Django 4.2.6 on 2024-03-06 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seajb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='armas',
            name='cantidadS',
            field=models.IntegerField(null=True, verbose_name='Cantidad Segundario'),
        ),
    ]