from django.urls import path

from blog_app import post_views

app_name = 'blog_app'


urlpatterns = [
    path('', post_views.ListPosts.as_view(), name='list_view'),
    path('category/<int:category_id>', post_views.ListPosts.as_view(), name='list_category_view'),
    path('create_post/', post_views.CreatePost.as_view(), name='create_post_view'),
]
