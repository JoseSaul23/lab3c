# Generated by Django 4.0.3 on 2022-04-15 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_partner_socialmedia_alter_carousel_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('introduction', models.CharField(max_length=500, verbose_name='Texto introductorio')),
            ],
            options={
                'verbose_name': 'Configuración',
                'verbose_name_plural': 'Configuraciones',
                'db_table': 'Configuracion',
            },
        ),
    ]
