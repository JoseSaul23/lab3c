# Generated by Django 4.0.3 on 2022-04-12 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_tools'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Inscriptions',
            new_name='Inscription',
        ),
        migrations.RenameModel(
            old_name='Tools',
            new_name='Tool',
        ),
    ]
