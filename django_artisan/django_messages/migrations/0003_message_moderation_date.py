# Generated by Django 3.2.9 on 2021-12-06 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_messages', '0002_alter_message_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='moderation_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
