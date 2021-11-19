# Generated by Django 3.2 on 2021-11-18 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_forum', '0002_auto_20211118_1648'),
        ('django_artisan', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtisanForumPost',
            fields=[
                ('forumpost_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_forum.forumpost')),
                ('category', models.CharField(choices=[('EV', 'Event'), ('QN', 'Question'), ('GL', 'General'), ('PS', 'Pictures'), ('FS', 'For Sale')], default='GL', max_length=2)),
                ('location', models.CharField(choices=[('AI', 'Any'), ('AY', 'Alderney'), ('GY', 'Guernsey'), ('JE', 'Jersey'), ('SK', 'Sark')], default='AI', max_length=2)),
            ],
            options={
                'abstract': False,
            },
            bases=('django_forum.forumpost',),
        ),
    ]