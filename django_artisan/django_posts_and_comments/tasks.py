import logging
from . import models as posts_and_comments_models

logger = logging.getLogger('django_artisan')


def schedule_hard_delete(slug=None,
                         deleted_at=None,
                         type=None,
                         id=None,
                         **kwargs) -> None:
    logger.error("type = " + type + " id = " + id)
    if 'Comment' in type:
        posts_and_comments_models.Comment.all_objects.get(id=int(id)).hard_delete()
    else:
        posts_and_comments_models.Post.all_objects.get(id=int(id)).hard_delete()
