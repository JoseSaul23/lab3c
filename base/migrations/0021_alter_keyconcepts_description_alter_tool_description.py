# Generated by Django 4.0.3 on 2022-05-02 22:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyconcepts',
            name='description',
            field=models.TextField(max_length=400, validators=[django.core.validators.MaxLengthValidator(400)], verbose_name='Descripción del concepto'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='description',
            field=models.TextField(max_length=400, validators=[django.core.validators.MaxLengthValidator(400)], verbose_name='Descripción de la herramienta'),
        ),
    ]
