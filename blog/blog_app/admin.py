from django.contrib import admin

from blog_app.models import Post, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_date', 'is_important', 'is_publish', 'category']
    list_filter = ['author', 'is_important', 'is_publish', 'category']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
