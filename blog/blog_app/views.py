from django.shortcuts import render
from django.views.generic.list import View

from blog_app.models import Post


class ListPosts(View):
    model = Post
    template_name = 'post/list_post.html'

    def get(self, request):
        posts = self.model.objects.all()

        important_post = posts.filter(is_important=True).last()
        last_world_post = posts.filter(category__name='World').last()
        last_tech_post = posts.filter(category__name='Technology').last()

        return render(request, self.template_name, {'posts': posts,
                                                    'important': important_post,
                                                    'last_world_post': last_world_post,
                                                    'last_tech_post': last_tech_post})
