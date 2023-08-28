from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
   path('<int:pk>/', views.DetailView.as_view(), name='detail'),
   path('<int:blog_id>/submit/', views.submit_commet, name='submit'),
]
