# Generated by Django 4.2.16 on 2024-10-27 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emotions', '0002_remove_emotion_predict_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
