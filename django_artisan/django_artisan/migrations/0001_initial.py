# Generated by Django 3.2 on 2021-11-11 23:33

from django.db import migrations, models
import django.db.models.deletion
import django_artisan.models
import safe_imagefield.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_forum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtisanForumProfile',
            fields=[
                ('forumprofile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_forum.forumprofile')),
                ('bio', models.TextField(blank=True, default='', max_length=500, verbose_name='biographical information, max 500 chars')),
                ('image_file', models.ImageField(blank=True, null=True, upload_to=django_artisan.models.user_directory_path, verbose_name='A single image for your personal page')),
                ('shop_web_address', models.CharField(blank=True, default='', max_length=50, verbose_name='shop link')),
                ('outlets', models.CharField(blank=True, default='', max_length=400, verbose_name='places that sell my stuff, comma separated')),
                ('listed_member', models.BooleanField(default=False, verbose_name='List me on about page')),
                ('display_personal_page', models.BooleanField(default=False, verbose_name='Display personal page')),
            ],
            bases=('django_forum.forumprofile',),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('text', models.CharField(max_length=400)),
                ('time', models.TimeField()),
                ('every', models.CharField(blank=True, max_length=40, null=True)),
                ('date', models.DateField(blank=True, null=True)),
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
                ('image_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('id', models.PositiveIntegerField(default=0, editable=False)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_images', to='django_artisan.artisanforumprofile')),
            ],
            options={
                'permissions': [('approve_image', 'Approve Image')],
            },
        ),
    ]
