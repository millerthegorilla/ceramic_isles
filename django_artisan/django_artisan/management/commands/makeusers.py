import sys, faker, uuid, os
from random import randrange

from django import conf
from django.core.management import base
from django.contrib import auth
from django.core.files import images

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
            raise base.CommandError('Error! settings.DEBUG is not defined or false. \
                                This command only works with a development install')
            sys.exit(1)
        fake = faker.Faker()
        path = conf.settings.BASE_DIR + '/django_artisan/management/images/'
        try:
            path = conf.settings.MANAGEMENT_IMAGE_PATH
        except:
            pass
        imagefiles = ([f for f in os.listdir(path) 
                      if os.path.isfile(os.path.join(path, f))])
        user_ids = []
        for i in range(options['num_of_users']):
            self.stdout.write(self.style.SUCCESS('Creating user number {}'.format(i+1)))
            first_name = fake.unique.first_name()
            last_name = fake.unique.last_name()
            new_user = auth.get_user_model().objects.create(
                username=first_name + str(uuid.uuid4()),
                first_name=first_name,
                last_name=last_name,
                is_active=True)
            new_user.profile.display_name=first_name + '-' + last_name
            new_user.save()
            user_ids.append(new_user.id)
            pic = imagefiles[randrange(8)]
            try:
                new_user.profile.forum_images.create(
                    image_file=images.ImageFile(file=open(path + pic, 'rb')),
                    image_text=pic,
                    image_title=pic[:30],
                    active=True)
            except Exception as e:
                raise base.CommandError('Error! creating image for user {} failed! {}'.format(i, e))
                break

        self.stdout.write(self.style.SUCCESS('Successfully created {} users.'.format(i + 1)))
        self.stdout.write(self.style.SUCCESS('User ids: {}'.format(user_ids)))