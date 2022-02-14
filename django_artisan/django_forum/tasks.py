import logging
from typing import Type
import django_q

from django import conf
from django.contrib.sites import models as site_models
from django.core import mail, exceptions

from . import models as forum_models

logger = logging.getLogger('django_artisan')

def send_subscribed_email(post_model: Type[forum_models.Post],
                          comment_model: Type[forum_models.Comment],
                          post_id: int = None, 
                          comment_id: int = None, 
                          path_info: str = None,
                          s_name: str = None) -> str:
    post = comment = None
    posts = post_model.objects.filter(id=post_id)
    if posts.exists():
        post = posts.first()

    comments = comment_models.objects.filter(id=comment_id)
    if comments.exists():
        comment = comments.first()

    if post and comment:
        if post.subscribed_users.exists():
            href = "{0}://{1}{2}#{3}".format('https',
                                             site_models.Site.objects.get_current().domain,
                                             path_info,
                                             comment.slug)

            email = mail.EmailMessage(
                'A new comment has been made at {}!'.format(
                    conf.settings.SITE_NAME),
                conf.settings.SUBSCRIBED_MSG.format(href),
                conf.settings.EMAIL_FROM_ADDRESS,
                ['subscribed_user@ceramicisles.org'],
                list(   #bcc
                    post.subscribed_users.all().values_list(
                        'email',
                        flat=True)),
                reply_to=[
                    conf.settings.EMAIL_FROM_ADDRESS],
            )
            email.content_subtype = "html"
            email.send()
            return 'Email Sent!'
    else:
        return 'No Email Sent - either post or comment has been deleted...'
    #     try:
    #         schedule = django_q.models.Schedule.objects.get(name=s_name).delete()
    #     except exceptions.ObjectDoesNotExist as e:
    #         logger.error("Schedule doesn't exist : " + str(e))
       # remove scheduled job
