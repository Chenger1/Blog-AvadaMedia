from django.urls import path

from user_app import views

app_name = 'user_app'


urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login_view'),
    path('logout/', views.LogoutView.as_view(), name='logout_view'),
    path('registration/', views.RegistrationView.as_view(), name='registration_view'),
    path('profile/<int:user_id>/', views.UserProfilePosts.as_view(), name='profile_view'),
    path('profile/<int:user_id>/saved/', views.UserProfileSaved.as_view(),
         name='profile_saved_view'),
    path('profile/<int:user_id>/comments/', views.UserProfileComment.as_view(),
         name='profile_comments_view'),
    path('profile/<int:user_id>/favorites/', views.UserProfileFavorites.as_view(),
         name='profile_favorites_view'),
    path('update_personal_info/', views.UpdatePersonalInfo.as_view(), name='update_personal_info_view'),
    path('change_password/<int:pk>', views.ChangePassword.as_view(), name='change_password_view'),
    path('add_post_to_favorites/<int:post_id>', views.AddToFavorites.as_view(), name='add_to_favorites_view'),
    path('remove_post_from_favorites/<int:post_id>/', views.RemoveFromFavorites.as_view(),
         name='remove_post_from_favorites_view'),
]
