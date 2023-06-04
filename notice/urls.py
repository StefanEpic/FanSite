from django.urls import path
from .views import NoticeList, NoticeCreate, NoticeUpdate, NoticeDelete, NoticeDetail, CategoryList

urlpatterns = [
    path('', NoticeList.as_view(), name='notice_list'),
    path('<int:pk>/', NoticeDetail.as_view(), name='notice_detail'),
    path('create/', NoticeCreate.as_view(), name='notice_create'),
    path('<int:pk>/update/', NoticeUpdate.as_view(), name='notice_update'),
    path('<int:pk>/delete/', NoticeDelete.as_view(), name='notice_delete'),
    path('category/<int:pk>/', CategoryList.as_view(), name='category_list'),
]