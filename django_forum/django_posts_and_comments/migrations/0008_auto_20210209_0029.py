# Generated by Django 3.1.6 on 2021-02-09 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_posts_and_comments', '0007_auto_20210209_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=500),
        ),
    ]
