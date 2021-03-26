from django.shortcuts import render
from django.views.generic.list import View

from blog_app.models import Post, Category


class ListPosts(View):
    model = Post
    template_name = 'post/list_post.html'

    def get(self, request, category_id=None):
        if category_id:
            posts = self.model.objects.filter(category=category_id, is_publish=True)
        else:
            posts = self.model.objects.filter(is_publish=True)

        categories = Category.objects.all()

        important_posts = posts.filter(is_important=True).reverse()[:3]

        return render(request, self.template_name, {'posts': posts,
                                                    'important_posts': important_posts,
                                                    'categories': categories})
