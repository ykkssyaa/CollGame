# Generated by Django 5.0.2 on 2024-02-22 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='status',
        ),
        migrations.AddField(
            model_name='game',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]