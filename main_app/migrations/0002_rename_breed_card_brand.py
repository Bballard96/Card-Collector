# Generated by Django 4.2.1 on 2023-06-02 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='breed',
            new_name='brand',
        ),
    ]
