# Generated by Django 3.2.9 on 2021-12-07 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_forum.models
import safe_imagefield.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_messages', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_profile', '0001_initial'),
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
            name='Post',
            fields=[
                ('message_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_messages.message')),
                ('title', models.CharField(default='', max_length=100)),
                ('pinned', models.SmallIntegerField(default=0)),
                ('commenting_locked', models.BooleanField(default=False)),
                ('subscribed_users', models.ManyToManyField(blank=True, related_name='subscribed_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'permissions': [('approve_post', 'Approve Post')],
                'abstract': False,
            },
            bases=('django_messages.message',),
        ),
        migrations.CreateModel(
            name='ForumProfile',
            fields=[
                ('profile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_profile.profile')),
                ('address_line_1', models.CharField(blank=True, default='', max_length=30, verbose_name='address line 1')),
                ('address_line_2', models.CharField(blank=True, default='', max_length=30, verbose_name='address line 2')),
                ('parish', models.CharField(blank=True, default='', max_length=30, verbose_name='parish')),
                ('postcode', models.CharField(blank=True, default='', max_length=6, verbose_name='postcode')),
                ('rules_agreed', models.BooleanField(default='False')),
                ('avatar', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to='django_forum.avatar')),
            ],
            bases=('django_profile.profile',),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('message_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_messages.message')),
                ('forum_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_comments', to='django_forum.post')),
            ],
            options={
                'ordering': ['created_at'],
                'permissions': [('approve_comment', 'Approve Comment')],
            },
            bases=('django_messages.message',),
        ),
    ]
