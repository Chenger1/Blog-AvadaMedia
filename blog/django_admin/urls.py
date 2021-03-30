from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from django_admin.views import views
from django_admin.views import posts_views
from django_admin.views import actions

app_name = 'django_admin'

urlpatterns = [
    path('', staff_member_required(views.DisplayAdminPage.as_view()), name='admin_panel'),
    path('actions/<str:model_name>/', staff_member_required(actions.ActionsView.as_view()), name='action_view'),

    # BLOG_APP

    path('blog_app/post/', staff_member_required(posts_views.ListPosts.as_view()), name='list_post_admin'),
    path('blog_app/change_post/<int:post_id>/', staff_member_required(posts_views.ChangePost.as_view()),
         name='change_post_admin'),
    path('blog_app/delete_post/<int:post_id>/', staff_member_required(posts_views.DeletePost.as_view()),
         name='delete_post_admin'),
    path('blog_app/post/filter/<str:filter_name>/<int:filter_value>/', staff_member_required(posts_views.ListPosts.as_view()),
         name='list_post_admin_by_filter'),
    path('blog_app/post/add_post/', staff_member_required(posts_views.CreatePost.as_view()),
         name='create_post_admin'),
]
