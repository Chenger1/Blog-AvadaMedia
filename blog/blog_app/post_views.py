from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.detail import DetailView

from blog_app.models import Post, Category

from blog_app.forms import CreatePostForm

from common.mixins import ExtendLoginRequiredMixin, UserPermissionsRequiredMixin


class ListPosts(View):
    model = Post
    template_name = 'post/list_post.html'

    def get(self, request, category_id=None):
        if category_id:
            posts = self.model.objects.filter(category=category_id, is_publish=True)
        else:
            posts = self.model.objects.filter(is_publish=True)

        categories = Category.objects.all()

        important_posts = posts.filter(is_important=True).order_by('published_date').reverse()[:3]

        return render(request, self.template_name, {'posts': posts,
                                                    'important_posts': important_posts,
                                                    'categories': categories})


class CreatePost(ExtendLoginRequiredMixin, UserPermissionsRequiredMixin, View):
    template_name = 'post/create_post.html'
    form = CreatePostForm

    def get(self, request):
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories})

    def post(self, request):
        form = self.form(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_app:list_view')
        else:
            categories = Category.objects.all()
            return render(request, self.template_name, {'form': form, 'categories': categories})


class PostDetail(DetailView):
    model = Post
    template_name = 'post/detail_post.html'


class HidePost(ExtendLoginRequiredMixin, UserPermissionsRequiredMixin, View):
    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        post.is_publish = not post.is_publish
        post.save()
        return redirect(post.get_absolute_url())
