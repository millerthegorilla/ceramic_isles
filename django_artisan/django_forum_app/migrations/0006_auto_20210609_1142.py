# Generated by Django 3.2 on 2021-06-09 10:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_forum_app', '0005_alter_forumpost_subscribed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forumpost',
            name='subscribed',
        ),
        migrations.AddField(
            model_name='forumpost',
            name='subscribed_users',
            field=models.ManyToManyField(
                blank=True,
                related_name='subscribed_posts',
                to=settings.AUTH_USER_MODEL),
        ),
    ]
