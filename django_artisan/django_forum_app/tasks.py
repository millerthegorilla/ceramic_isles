from django.conf import settings
from django.contrib.sites.models import Site
from .models import ForumPost, ForumComment

def send_susbcribed_email(post_id=None, comment_id=None, path_info=None):
    post = comment = None
    posts = ForumPost.objects.filter(id=post_id)
    if posts.count():
        post = posts.first()

    comments = ForumComment.objects.filter(id=comment_id)
    if comments.count():
        comment = comments.first()
    
    if post and comment:
        if post.subscribed_users.count():
            href = "{0}://{1}{2}#{3}".format('https', Site.objects.get_current().domain, path_info, comment.title)
            
            email = EmailMessage(
                'A new comment has been made at {}!'.format(settings.SITE_NAME),
                settings.SUBSCRIBED_MSG.format(href),
                settings.EMAIL_FROM_ADDRESS,
                ['subscribed_user@ceramicisles.org'],
                list(post.subscribed_users.all().values_list('email', flat=True)),
                reply_to=[settings.EMAIL_FROM_ADDRESS],
            )
            email.content_subtype = "html"
            email.send()