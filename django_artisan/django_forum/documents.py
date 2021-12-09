import elasticsearch_dsl
import django_elasticsearch_dsl
from django_elasticsearch_dsl.registries import registry

from django import conf

from . import models as forum_models


sugg_analyzer = elasticsearch_dsl.analyzer(
    'sugg_analyzer',
    tokenizer=elasticsearch_dsl.tokenizer(
        'trigram', 'ngram', min_gram=3, max_gram=3
    ),
    filter=['lowercase']
)

html_strip = elasticsearch_dsl.analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

try:
    abstract = conf.settings.ABSTRACTCOMMENT
except AttributeError:
    abstract = False
if not abstract:
    @registry.register_document
    class Comment(django_elasticsearch_dsl.Document):

        author_name = django_elasticsearch_dsl.fields.TextField(attr="get_author_name")

        text = django_elasticsearch_dsl.fields.TextField(
            attr='text',
            analyzer=html_strip,
        )

        class Index:
            # Name of the Elasticsearch index
            name = 'forum_comments_index'
            # See Elasticsearch Indices API reference for available settings
            settings = {'number_of_shards': 1,
                        'number_of_replicas': 0}

        class Django:
            """
               I no longer have an autocomplete defined, as the amount of requests is crazy.
            """

            model = forum_models.Comment

            """
              the commented code below allows searched comments to return a post as the 'found'
              record.
            """
            # related_models = [Post]

            # def get_queryset(self):
            #     return super().get_queryset().select_related(
            #         'forum_post'
            #     )


try:
    abstract = conf.settings.ABSTRACTPOST
except AttributeError:
    abstract = False
if not abstract:
    @registry.register_document
    class Post(django_elasticsearch_dsl.Document):

        author_name = django_elasticsearch_dsl.fields.TextField(attr="get_author_name")

        text = django_elasticsearch_dsl.fields.TextField(
            attr='text',
            analyzer=html_strip,
        )

        # category = django_elasticsearch_dsl.fields.TextField(
        #     attr='category_label'
        # )

        # location = django_elasticsearch_dsl.fields.TextField(
        #     attr='location_label'
        # )

        class Index:
            # Name of the Elasticsearch index
            name = 'forum_posts_index'
            # See Elasticsearch Indices API reference for available settings
            settings = {'number_of_shards': 1,
                        'number_of_replicas': 0}

        class Django:
            """
                I no longer have an autocomplete defined as the amount of requests goes
                through the roof.
            """
            model = forum_models.Post
            fields = [
                'title',
            ]
