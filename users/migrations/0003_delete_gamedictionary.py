# Generated by Django 5.0.2 on 2024-02-22 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_games_gamedictionary_userlist'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GameDictionary',
        ),
    ]
