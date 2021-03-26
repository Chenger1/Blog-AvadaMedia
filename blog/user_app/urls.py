from django.conf import settings
from django.conf.urls.static import static

app_name = 'user_app'


urlpatterns = [

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
