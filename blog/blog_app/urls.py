from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from blog_app import post_views

app_name = 'blog_app'


urlpatterns = [
    path('', post_views.ListPosts.as_view(), name='list_view'),
    path('category/<int:category_id>', post_views.ListPosts.as_view(), name='list_category_view')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
