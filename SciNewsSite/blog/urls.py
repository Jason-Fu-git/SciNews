from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),  # 首页
    path('search/submit/', views.on_search_submit, name='search_submit'),  # 提交搜索后中转页面
    path('search/?<str:content>/', views.SearchView.as_view(), name='search'),  # 搜索结果页
    path('search/?<str:content>/?page=<int:page>', views.SearchView.as_view(), name='search_page'),  # 搜索结果页分页
    path('search/?<str:content>/to/', views.search_to_page, name='search_to'),  # 搜索结果页分页中转页面
    path('detail/<int:pk>/', views.DetailView.as_view(), name='detail'),  # 详情页
    path('detail/<int:blog_id>/submit/', views.submit_commet, name='submit'),  # 评论提交中转页面
    path('list/', views.ListView.as_view(), name='list'),  # 列表页面
    path('list/to/', views.list_to_page, name='list_to'),  # 列表输入分页中转页面
    path('list/?page=<int:page>', views.ListView.as_view(), name='list_query'),  # 列表分页
]
