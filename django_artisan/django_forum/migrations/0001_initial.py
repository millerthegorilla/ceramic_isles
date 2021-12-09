# Generated by Django 3.2.9 on 2021-12-09 17:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_forum.models
import safe_imagefield.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_artisan', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', safe_imagefield.models.SafeImageField(allowed_extensions=None, check_content_type=False, max_size_limit=False, media_integrity=False, scan_viruses=False, upload_to=django_forum.models.user_directory_path_avatar)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default='True')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('text', models.TextField(max_length=3000)),
                ('moderation_date', models.DateField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=80, unique=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='django_forum_comment_related', to=settings.AUTH_USER_MODEL)),
                ('post_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='django_artisan.post')),
            ],
            options={
                'ordering': ['created_at'],
                'permissions': [('approve_comment', 'Approve Comment')],
                'abstract': False,
            },
        ),
    ]
