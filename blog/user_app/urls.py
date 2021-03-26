from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

app_name = 'user_app'


urlpatterns = [
    path('login/', LoginView.as_view(), name='login_view'),
    path('logout/', LogoutView.as_view(), name='logout_view')
]
