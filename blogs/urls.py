"""Defines URL patterns for blogs."""

from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'blogs'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    # Show all posts.
    path('posts/', views.posts, name='posts'),

    # Detail page for a single post
    path('posts/<int:post_id>/', views.post, name='post'),

    # Page for adding new post
    path('new_post/', views.new_post, name='new_post'),

    # Page for editing a post
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),

]
