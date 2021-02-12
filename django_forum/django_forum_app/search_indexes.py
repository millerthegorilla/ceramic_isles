from haystack import indexes
from .models import ForumPost
from django.utils import timezone


class ForumPostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    text_auto = indexes.EdgeNgramField(model_attr='post_text')
    date_created = indexes.DateTimeField(model_attr='post_date_created')
    title = indexes.CharField(model_attr='post_title')
    
    def get_model(self):
        return ForumPost
    
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=timezone.now())