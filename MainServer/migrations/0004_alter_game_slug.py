# Generated by Django 5.0.2 on 2024-02-22 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainServer', '0003_gamestudio_game_slug_game_studio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
