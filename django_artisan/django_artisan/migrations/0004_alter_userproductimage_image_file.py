# Generated by Django 3.2.9 on 2022-01-17 23:10

from django.db import migrations
import django_artisan.models
import safe_imagefield.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_artisan', '0003_alter_userproductimage_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userproductimage',
            name='image_file',
            field=safe_imagefield.models.SafeImageField(allowed_extensions=None, check_content_type=False, max_length=250, max_size_limit=False, media_integrity=False, scan_viruses=False, upload_to=django_artisan.models.user_directory_path),
        ),
    ]
