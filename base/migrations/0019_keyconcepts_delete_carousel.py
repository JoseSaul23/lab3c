# Generated by Django 4.0.3 on 2022-05-02 14:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_settings_intro_image_alter_inscription_pdf_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyConcepts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre del concepto')),
                ('description', models.CharField(max_length=200, verbose_name='Descripción del concepto')),
                ('pdf', models.FileField(upload_to='pdf/conceptos', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
            ],
            options={
                'verbose_name': 'Concepto',
                'verbose_name_plural': 'Conceptos',
                'db_table': 'Concepto',
                'ordering': ('-name',),
            },
        ),
        migrations.DeleteModel(
            name='Carousel',
        ),
    ]