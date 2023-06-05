# Generated by Django 4.2.2 on 2023-06-05 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_card_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=250)),
                ('card', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_app.card')),
            ],
        ),
    ]
