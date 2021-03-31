from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from django_admin.views import views
from django_admin.views import posts_views
from django_admin.views import category_views
from django_admin.views import users_views
from django_admin.views import groups_views
from django_admin.views import actions

app_name = 'django_admin'

urlpatterns = [
    path('', staff_member_required(views.DisplayAdminPage.as_view()), name='admin_panel'),
    path('actions/<str:model_name>/', staff_member_required(actions.ActionsView.as_view()), name='action_view'),

    # BLOG_APP

    #  # POSTS
    path('blog_app/post/', staff_member_required(posts_views.ListPosts.as_view()), name='list_post_admin'),
    path('blog_app/change_post/<int:post_id>/', staff_member_required(posts_views.ChangePost.as_view()),
         name='change_post_admin'),
    path('blog_app/delete_post/<int:post_id>/', staff_member_required(posts_views.DeletePost.as_view()),
         name='delete_post_admin'),
    path('blog_app/post/filter/<str:filter_name>/<int:filter_value>/', staff_member_required(posts_views.ListPosts.as_view()),
         name='list_post_admin_by_filter'),
    path('blog_app/post/add_post/', staff_member_required(posts_views.CreatePost.as_view()),
         name='create_post_admin'),

    # # Categories
    path('blog_app/category/', staff_member_required(category_views.ListCategory.as_view()),
         name='list_category_admin'),
    path('blog_app/category/change_category_form/<int:category_id>/',
         staff_member_required(category_views.ListCategory.as_view()),
         name='list_category_with_change_form_admin'),
    path('blog_app/category/create_category/', staff_member_required(category_views.EditCategory.as_view()),
         name='create_category_admin'),
    path('blog_app/category/edit_category/<int:category_id>/', staff_member_required(category_views.EditCategory.as_view()),
         name='edit_category_admin'),
    path('blog_app/category/delete_category/<int:category_id>/', staff_member_required(category_views.DeleteCategory.as_view()),
         name='delete_category_admin'),


    # USER_APP

    # # USERS
    path('user_app/users/', staff_member_required(users_views.ListUsers.as_view()),
         name='list_users_admin'),
    path('user_app/users/filter/<str:filter_name>/<int:filter_value>/', staff_member_required(users_views.ListUsers.as_view()),
         name='list_users_admin_by_filter'),
    path('user_app/users/create_user/', staff_member_required(users_views.CreateUser.as_view()),
         name='create_user_admin'),
    path('user_app/users/profile/<int:user_id>/', staff_member_required(users_views.UserProfilePosts.as_view()),
         name='user_profile_admin'),
    path('user_app/users/profile/<int:user_id>/saved/', staff_member_required(users_views.UserProfileSaved.as_view()),
         name='user_profile_saved_posts_admin'),
    path('user_app/users/profile/<int:user_id>/comments/', staff_member_required(users_views.UserProfileComment.as_view()),
         name='user_profile_comments_admin'),
    path('user_app/users/profile/<int:user_id>/settings/', staff_member_required(users_views.UserProfileSettings.as_view()),
         name='user_profile_settings_admin'),
    path('user_app/users/profile/<int:user_id>/settings/update_info/',
         staff_member_required(users_views.UserProfileSettings.as_view()),
         name='user_profile_update_info_admin'),
    path('user_app/users/profile/<int:user_id>/settings/delete_user/',
         staff_member_required(users_views.DeleteUser.as_view()),
         name='user_profile_delete_admin'),

    # # GROUPS
    # path('user_app/groups/', staff_member_required(groups_views.ListGroups.as_view()),
    #      name='list_groups_admin'),
]
