from django import urls
from . import views as messages_views

app_name = 'django_messages'

urlpatterns = [
    urls.path('messages/', messages_views.MessageList.as_view(), name='message_list'),
    urls.path('create_message/', messages_views.MessageCreate.as_view(), name='message_create'),
    urls.path('update_message/', messages_views.MessageUpdate.as_view(), name='message_update'),
    urls.path('<int:pk>/delete_message/', messages_views.MessageDelete.as_view(), name='message_delete'),
    urls.path('<int:pk>/<slug:slug>/', messages_views.MessageView.as_view(), name='post'),
]
