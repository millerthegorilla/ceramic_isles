import logging

from django.core import exceptions

from . import models as messages_models

logger = logging.getLogger('django_artisan')


def schedule_hard_delete(slug=None,
                         deleted_at=None,
                         type=None,
                         id=None,
                         **kwargs) -> None:
  
    try:    
        messages_models.Message.all_objects.get(id=int(id)).hard_delete()
        return 'Succesfully hard deleted message!'
    except ObjectDoesNotExist as e:
    	return 'Failure - unable to find that message to hard delete...'
    # if 'Comment' in type:
    #     posts_and_comments_models.Comment.all_objects.get(id=int(id)).hard_delete()
    # else:
    #     posts_and_comments_models.Post.all_objects.get(id=int(id)).hard_delete()
