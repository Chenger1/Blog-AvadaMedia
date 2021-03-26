from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ['name']
        db_table = 'category'

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField(max_length=5000)

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='author')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='category')

    is_publish = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(auto_now=True)

    is_important = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_date']
        db_table = 'post'
