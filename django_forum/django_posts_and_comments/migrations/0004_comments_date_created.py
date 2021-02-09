# Generated by Django 3.1.6 on 2021-02-08 23:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('django_posts_and_comments', '0003_auto_20210208_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
