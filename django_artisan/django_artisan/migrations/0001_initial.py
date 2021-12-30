# Generated by Django 3.2.9 on 2021-12-09 17:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_artisan.models
import django_forum.models
import safe_imagefield.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtisanForumProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line_1', models.CharField(blank=True, default='', max_length=30, verbose_name='address line 1')),
                ('address_line_2', models.CharField(blank=True, default='', max_length=30, verbose_name='address line 2')),
                ('parish', models.CharField(blank=True, default='', max_length=30, verbose_name='parish')),
                ('postcode', models.CharField(blank=True, default='', max_length=6, verbose_name='postcode')),
                ('rules_agreed', models.BooleanField(default='False')),
                ('display_name', models.CharField(blank=True, default=django_forum.models.default_display_name, max_length=37, unique=True)),
                ('bio', models.TextField(blank=True, default='', max_length=500, verbose_name='biographical information, max 500 chars')),
                ('image_file', models.ImageField(blank=True, null=True, upload_to=django_artisan.models.user_directory_path, verbose_name='A single image for your personal page')),
                ('shop_web_address', models.CharField(blank=True, default='', max_length=50, verbose_name='shop link')),
                ('outlets', models.CharField(blank=True, default='', max_length=400, verbose_name='places that sell my stuff, comma separated')),
                ('listed_member', models.BooleanField(default=False, verbose_name='List me on about page')),
                ('display_personal_page', models.BooleanField(default=False, verbose_name='Display personal page')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('text', models.CharField(max_length=400)),
                ('time', models.TimeField()),
                ('every', models.CharField(blank=True, max_length=40, null=True)),
                ('event_date', models.DateField(blank=True, null=True)),
                ('repeating', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProductImage',
            fields=[
                ('image_file', safe_imagefield.models.SafeImageField(allowed_extensions=None, check_content_type=False, max_size_limit=False, media_integrity=False, scan_viruses=False, upload_to=django_artisan.models.user_directory_path)),
                ('image_text', models.CharField(blank=True, default='', max_length=400)),
                ('image_title', models.CharField(blank=True, default='', max_length=30)),
                ('image_shop_link', models.CharField(blank=True, default='', max_length=50)),
                ('image_shop_link_title', models.CharField(blank=True, default='', max_length=30)),
                ('active', models.BooleanField(default=False)),
                ('image_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('id', models.PositiveIntegerField(auto_created=True,  primary_key=True, serialize=False, verbose_name='ID')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_images', to='django_artisan.artisanforumprofile')),
            ],
            options={
                'permissions': [('approve_image', 'Approve Image')],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default='True')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('text', models.TextField(max_length=3000)),
                ('moderation_date', models.DateField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=80, unique=True)),
                ('title', models.CharField(default='', max_length=100)),
                ('pinned', models.SmallIntegerField(default=0)),
                ('commenting_locked', models.BooleanField(default=False)),
                ('category', models.CharField(choices=[('EV', 'Event'), ('QN', 'Question'), ('GL', 'General'), ('PS', 'Pictures'), ('FS', 'For Sale')], default='GL', max_length=2)),
                ('location', models.CharField(choices=[('AI', 'Any'), ('AY', 'Alderney'), ('GY', 'Guernsey'), ('JE', 'Jersey'), ('SK', 'Sark')], default='AI', max_length=2)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='django_artisan_post_related', to=settings.AUTH_USER_MODEL)),
                ('subscribed_users', models.ManyToManyField(blank=True, related_name='subscribed_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'permissions': [('approve_post', 'Approve Post')],
                'abstract': False,
            },
        ),
    ]
