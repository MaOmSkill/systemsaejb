# Generated by Django 4.2.6 on 2024-03-06 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seajb', '0006_alter_armas_armas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='municiones',
            name='fechaAG',
            field=models.DateField(verbose_name='Fecha de Asignación'),
        ),
    ]