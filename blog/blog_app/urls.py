from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from blog_app import post_views

app_name = 'blog_app'


urlpatterns = [
    path('', post_views.ListPosts.as_view(), name='list_view'),
    path('category/<int:category_id>/', post_views.ListPosts.as_view(), name='list_category_view'),
    path('create_post/', post_views.CreatePost.as_view(), name='create_post_view'),
    path('detail_post/<int:pk>/', post_views.PostDetail.as_view(), name='detail_post_view'),
    path('hide_post/<int:post_id>/', post_views.HidePost.as_view(), name='hide_post_view'),
    path('delete_post/<int:pk>/', post_views.DeletePost.as_view(), name='delete_post_view'),
    path('edit_post/<int:post_id>/', post_views.EditPost.as_view(), name='edit_post_view'),
    path('change_post_importance/<int:post_id>', staff_member_required(post_views.ChangeImportanceView.as_view()),
         name='change_importance_view'),
]
