from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.view, name='home'),
    path('', views.Feed, name='feed'),
    path('results/', views.search_posts, name = 'search_posts')
]
