from django.db import models
from django.contrib.auth.models import AbstractUser

from blog_app.models import Post


class User(AbstractUser):
    extended_info = models.TextField(max_length=2000, blank=True)
    favorites = models.ForeignKey(Post, on_delete=models.CASCADE,
                                  related_name='favorite_users', blank=True, null=True)
