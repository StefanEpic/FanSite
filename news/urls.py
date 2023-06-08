from django.urls import path
from .views import NewsList, NewsCreate, NewsUpdate, NewsDelete

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    # path('create/', NewsCreate.as_view(), name='news_create'),
    # path('<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    # path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    # path('subscribe/', NewsDelete.as_view(), name='news_delete'),
    # path('unsubscribe/', NewsDelete.as_view(), name='news_delete'),
]
