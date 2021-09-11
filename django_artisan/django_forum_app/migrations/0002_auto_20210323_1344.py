# Generated by Django 3.1.7 on 2021-03-23 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_forum_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='forumcomment',
            options={'ordering': ['date_created'], 'permissions': [
                ('approve_comment', 'Approve Comment')]},
        ),
        migrations.AlterModelOptions(
            name='forumpost',
            options={'ordering': ['-date_created'],
                     'permissions': [('approve_post', 'Approve Post')]},
        ),
    ]
