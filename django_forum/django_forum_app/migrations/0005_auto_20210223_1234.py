# Generated by Django 3.1.6 on 2021-02-23 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_forum_app', '0004_auto_20210221_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumprofile',
            name='outlets',
            field=models.CharField(blank=True, default='', max_length=400, verbose_name='places that sell my stuff, comma separated'),
        ),
        migrations.AlterField(
            model_name='forumprofileimage',
            name='image_shop_link',
            field=models.CharField(default='', max_length=50),
        ),
    ]