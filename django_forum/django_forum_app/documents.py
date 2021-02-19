from elasticsearch_dsl import analyzer, tokenizer
from django_elasticsearch_dsl import Document, fields, Index
from django_elasticsearch_dsl.registries import registry
from .models import ForumPost, ForumComment


sugg_analyzer = analyzer('sugg_analyzer',
    tokenizer=tokenizer('trigram', 'ngram', min_gram=3, max_gram=3),
    filter=['lowercase']
)

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

@registry.register_document
class ForumPostDocument(Document):
    forum_comments = fields.NestedField(properties={
                                                         'author':fields.TextField(
                                                            attr="author",
                                                            fields={'raw': fields.TextField(analyzer=html_strip),
                                                                    'suggest': fields.Completion(analyzer=sugg_analyzer)}),
                                                         'date_created':fields.DateField(),
                                                         'text':fields.TextField(
                                                            attr="text",
                                                            fields={'raw': fields.TextField(analyzer=html_strip),
                                                                    'suggest': fields.Completion(analyzer=sugg_analyzer)})
                                                      })

    class Index:
            # Name of the Elasticsearch index
            name = 'forum_posts_index'
            # See Elasticsearch Indices API reference for available settings
            settings = {'number_of_shards': 1,
                        'number_of_replicas': 0}

    class Django:

        text = fields.TextField(
            attr='text',
            fields={
                'raw': fields.TextField(analyzer=html_strip),
                'suggest': fields.Completion(analyzer=sugg_analyzer),
            }
        )

        title = fields.TextField(
            attr='title',
            fields={
                'raw': fields.TextField(analyzer=html_strip),
                'suggest': fields.Completion(analyzer=sugg_analyzer),
            }
        )

        date_created = fields.DateField(
            attr='date_created',
            fields={
                'raw': fields.DateField(analyzer=html_strip),
                'suggest': fields.Completion(analyzer=sugg_analyzer),
            }
        )

        author = fields.TextField(
            attr='title',
            fields={
                'raw': fields.TextField(analyzer=html_strip),
                'suggest': fields.Completion(analyzer=sugg_analyzer),
            })
        
        model = ForumPost
        fields = [
            'title',
            'text',
            'date_created',
            'category',
            'author',
            'id',
        ]

        related_models = [ForumComment]

    def get_queryset(self):
        return super().get_queryset().select_related(
            'user_profile'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, ForumPost):
            return related_instance.comments.all()


# @registry.register_document
# class ForumCommentDocument(Document):

#     class Index:
#             # Name of the Elasticsearch index
#             name = 'forum_comments_index'
#             # See Elasticsearch Indices API reference for available settings
#             settings = {'number_of_shards': 1,
#                         'number_of_replicas': 0}

#     class Django:

#         model = ForumComment
#         fields = [
#             'text',
#             'date_created',
#             'author',
#             'id',
#         ]
