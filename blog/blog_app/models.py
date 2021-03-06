from django.db import models
from django.conf import settings
from django.shortcuts import reverse


class Category(models.Model):
    name = models.CharField(max_length=20)

    def get_admin_absolute_url(self):
        return reverse('django_admin:list_category_with_change_form_admin', args=[self.pk])

    class Meta:
        ordering = ['name']
        db_table = 'category'

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField(max_length=5000)

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='posts')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='category')

    is_publish = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(auto_now=True)

    is_important = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('blog_app:detail_post_view', args=[self.pk])

    def get_admin_absolute_url(self):
        return reverse('django_admin:change_post_admin', args=[self.pk])

    class Meta:
        ordering = ['-published_date']
        db_table = 'post'


class Comment(models.Model):
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')

    published_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment'
        ordering = ['-published_date']