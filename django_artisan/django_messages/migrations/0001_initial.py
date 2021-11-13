# Generated by Django 3.2 on 2021-11-13 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default='True')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('author', models.CharField(default='', max_length=40)),
                ('text', models.TextField(max_length=500)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
