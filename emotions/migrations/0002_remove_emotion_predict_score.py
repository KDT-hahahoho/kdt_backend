# Generated by Django 4.2.16 on 2024-10-27 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emotions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emotion',
            name='predict_score',
        ),
    ]
