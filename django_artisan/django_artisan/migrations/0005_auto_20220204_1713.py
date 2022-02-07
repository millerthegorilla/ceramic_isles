# Generated by Django 3.2.9 on 2022-02-04 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_artisan', '0004_alter_userproductimage_image_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='event_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='userproductimage',
            old_name='image_file',
            new_name='file',
        ),
        migrations.RenameField(
            model_name='userproductimage',
            old_name='image_shop_link',
            new_name='shop_link',
        ),
        migrations.RenameField(
            model_name='userproductimage',
            old_name='image_shop_link_title',
            new_name='shop_link_title',
        ),
        migrations.RenameField(
            model_name='userproductimage',
            old_name='image_text',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='userproductimage',
            old_name='image_title',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='userproductimage',
            name='image_id',
        ),
        migrations.AddField(
            model_name='userproductimage',
            name='caption',
            field=models.CharField(blank=True, default='', max_length=400),
        ),
    ]