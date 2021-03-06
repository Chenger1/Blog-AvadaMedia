from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from blog_app import post_views
from blog_app import search_view

app_name = 'blog_app'


urlpatterns = [
    path('', post_views.ListPosts.as_view(), name='list_view'),
    path('category/<int:category_id>/', post_views.ListPosts.as_view(), name='list_category_view'),
    path('archive/<int:year>/', post_views.ListPosts.as_view(), name='list_archive_view'),
    path('archive/<int:year>/<int:category_id>/', post_views.ListPosts.as_view(), name='list_archive_category_view'),
    path('create_post/', post_views.CreatePost.as_view(), name='create_post_view'),
    path('detail_post/<int:pk>/', post_views.PostDetail.as_view(), name='detail_post_view'),
    path('hide_post/<int:post_id>/', post_views.HidePost.as_view(), name='hide_post_view'),
    path('delete_post/<int:pk>/', post_views.DeletePost.as_view(), name='delete_post_view'),
    path('edit_post/<int:post_id>/', post_views.EditPost.as_view(), name='edit_post_view'),
    path('change_post_importance/<int:post_id>', staff_member_required(post_views.ChangeImportanceView.as_view()),
         name='change_importance_view'),
    path('add_comments/<int:post_id>/', post_views.CreateComment.as_view(), name='create_comment_view'),
    path('delete_comment/<int:comment_id>/', post_views.DeleteComment.as_view(), name='delete_comment_view'),
    path('edit_comment/<int:comment_id>/', post_views.EditComment.as_view(), name='edit_comment_view'),

    path('search/', search_view.SearchView.as_view(), name='search_view'),
]
