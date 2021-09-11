import logging
from .models import Comment, Post

logger = logging.getLogger('django')


def schedule_hard_delete(
        post_slug=None,
        deleted_at=None,
        type=None,
        id=None,
        **kwargs):
    logger.error("type = " + type + " id = " + id)
    if 'Comment' in type:
        Comment.all_objects.get(id=int(id)).hard_delete()
    else:
        Post.all_objects.get(id=int(id)).hard_delete()
