# Generated by Django 3.2 on 2021-05-21 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_posts_and_comments', '0002_auto_20210521_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
