from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('submit/', views.on_search_submit, name='search_submit'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:blog_id>/submit/', views.submit_commet, name='submit'),
    path('list/', views.ListView.as_view(), name='list'),
    path('list/to/', views.to_page, name='list_to'),
    path('list/?page=<int:page>', views.ListView.as_view(), name='list_query'),
]
