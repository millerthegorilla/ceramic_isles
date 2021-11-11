from django import conf
from django.contrib.sites import models as site_models
from django.core import mail

from . import models as forum_models


def send_susbcribed_email(post_id: int = None, comment_id: int = None, path_info: str = None) -> None:
    post = comment = None
    posts = forum_models.ForumPost.objects.filter(id=post_id)
    if posts.count():
        post = posts.first()

    comments = forum_models.ForumComment.objects.filter(id=comment_id)
    if comments.count():
        comment = comments.first()

    if post and comment:
        if post.subscribed_users.count():
            href = "{0}://{1}{2}#{3}".format('https',
                                             site_models.Site.objects.get_current().domain,
                                             path_info,
                                             comment.title)

            email = mail.EmailMessage(
                'A new comment has been made at {}!'.format(
                    conf.settings.SITE_NAME),
                conf.settings.SUBSCRIBED_MSG.format(href),
                conf.settings.EMAIL_FROM_ADDRESS,
                ['subscribed_user@ceramicisles.org'],
                list(
                    post.subscribed_users.all().values_list(
                        'email',
                        flat=True)),
                reply_to=[
                    conf.settings.EMAIL_FROM_ADDRESS],
            )
            email.content_subtype = "html"
            email.send()
