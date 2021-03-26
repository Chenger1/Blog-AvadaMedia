from django.urls import path

from user_app import views

app_name = 'user_app'


urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login_view'),
    path('logout/', views.LogoutView.as_view(), name='logout_view'),
    path('registration/', views.RegistrationView.as_view(), name='registration_view'),
]
