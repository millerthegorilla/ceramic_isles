import sys, faker, uuid

from django import conf
from django.core.management import base
from django.contrib import auth


class Command(base.BaseCommand):
    help = 'Adds fake users and images.  Defaults to 25, change this with --num_of_users arg.'

    def add_arguments(self, parser):
        parser.add_argument('--num_of_users', nargs='?', default=25, type=int)

    def handle(self, *args, **options):
        try:
            debug = bool(conf.settings.DEBUG)
        except KeyError:
            debug = False
        if not debug:
            raise CommandError('Error! settings.DEBUG is not defined or false. \
                                This command only works with a development install')
            sys.exit(1)
        fake = faker.Faker()
        for i in range(options['num_of_users']):
            first_name = fake.unique.first_name()
            last_name = fake.unique.last_name()
            new_user = auth.get_user_model().create('username'=first_name + str(uuid.uuid4()),
                                                    'first_name'=first_name,
                                                    'last_name'=last_name,
                                                     'email'=f"{first_name}.{last_name}@{fake.domain_name()}")
            new_user.save()
            new_user.profile.display_name=first_name + '-' + last_name
            new_user.profile.forum_images.objects.create(image_file=RANDOMPATH, image_text etc)

            self.stdout.write(self.style.SUCCESS('Successfully created "%s" users.' % options['num_of_users']))