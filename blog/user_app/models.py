from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from blog_app.models import Post


class User(AbstractUser):
    extended_info = models.TextField(max_length=2000, blank=True)
    favorites = models.ManyToManyField(Post, related_name='in_favorites', blank=True)

    def get_admin_absolute_url(self):
        return reverse('django_admin:user_profile_admin', args=[self.pk])
