from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from blog_app import views

app_name = 'blog_app'


urlpatterns = [
    path('', views.ListPosts.as_view(), name='list_view')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
