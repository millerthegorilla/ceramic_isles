# Generated by Django 3.1.6 on 2021-02-21 16:32

from django.db import migrations, models
import django_forum_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_forum_app', '0003_auto_20210221_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumprofile',
            name='bio',
            field=models.TextField(blank=True, default='', max_length=500, verbose_name='biographical information, max 500 chars'),
        ),
        migrations.AlterField(
            model_name='forumprofile',
            name='image_file',
            field=models.ImageField(null=True, upload_to=django_forum_app.models.user_directory_path, verbose_name='A single image for your personal page'),
        ),
    ]
