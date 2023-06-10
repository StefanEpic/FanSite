from django.urls import path
from .views import NewsList, NewsCreate, NewsUpdate, NewsDelete, subscribe_news, unsubscribe_news

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('subscribe/', subscribe_news, name='subscribe'),
    path('unsubscribe/', unsubscribe_news, name='unsubscribe'),
]
