# Generated by Django 5.1.1 on 2024-09-09 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substream', '0003_alter_video_video_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='subtitle_file',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
