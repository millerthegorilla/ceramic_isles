# Generated by Django 3.2 on 2021-05-24 11:21

from django.db import migrations, models
import django_profile.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_profile', '0004_alter_profile_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='display_name',
            field=models.CharField(blank=True, default=django_profile.models.default_display_name, max_length=37, unique=True),
        ),
    ]
