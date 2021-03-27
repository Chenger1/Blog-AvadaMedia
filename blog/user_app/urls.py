from django.urls import path

from user_app import views

app_name = 'user_app'


urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login_view'),
    path('logout/', views.LogoutView.as_view(), name='logout_view'),
    path('registration/', views.RegistrationView.as_view(), name='registration_view'),
    path('profile/<int:user_id>/', views.UserProfile.as_view(), name='profile_view'),
    path('profile/<int:user_id>/saved/', views.UserProfile.as_view(), {'is_publish': False},
         name='profile_saved_view'),
    path('update_personal_info/', views.UpdatePersonalInfo.as_view(), name='update_personal_info_view'),
]
