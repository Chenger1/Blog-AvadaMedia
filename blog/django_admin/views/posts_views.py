from django.shortcuts import render, redirect
from django.views.generic.list import View

from blog_app.models import Post, Category

from user_app.models import User

from django_admin.forms.blog_app.post import PostForm

from common.paginator_mixin import PaginatorMixin


class ListPosts(View):
    model = Post
    template_name = 'blog_app/post/list_posts.html'
    list_display = ['title', 'author', 'created_date', 'is_important', 'is_publish', 'category']

    def get(self, request, filter_name=None, filter_value=None):
        posts = self.filter_result(filter_name, filter_value)
        categories = Category.objects.all()
        page = request.GET.get('page')
        posts = PaginatorMixin.get_page(posts, 10, page)

        return render(request, self.template_name, {'posts': posts,
                                                    'list_display': self.list_display,
                                                    'categories': categories,
                                                    'current_filter': filter_name,
                                                    'filter_value': filter_value,
                                                    'page': page})

    def filter_result(self, filter_name=None, filter_value=None):
        if filter_name == 'is_publish':
            posts = self.model.objects.filter(is_publish=bool(filter_value))
        elif filter_name == 'is_important':
            posts = self.model.objects.filter(is_important=bool(filter_value))
        elif filter_name == 'category':
            posts = self.model.objects.filter(category__pk=int(filter_value))
        else:
            posts = self.model.objects.all()
        return posts


class ChangePost(View):
    model = Post
    form = PostForm
    template_name = 'blog_app/post/change_post.html'

    def get(self, request, post_id):
        post = self.model.objects.get(pk=post_id)
        form = PostForm(instance=post)
        return self.render_context(form, post)

    def post(self, request, post_id):
        post = self.model.objects.get(pk=post_id)
        form = self.form(request.POST, instance=post)
        multiple = int(request.POST.get('multiple'))
        if form.is_valid():
            post = form.save()
            if multiple:
                return redirect('django_admin:create_post_admin')
            return redirect(post.get_admin_absolute_url())
        else:
            return self.render_context(form, post)

    def get_context(self, post):
        users = User.objects.all().exclude(pk=post.author.pk)
        categories = Category.objects.all().exclude(pk=post.category.pk)
        return {'post': post, 'users': users, 'categories': categories}

    def render_context(self, form, post):
        context = self.get_context(post)
        return render(self.request, self.template_name, {'form': form,
                                                         'post_pk': context.get('post').pk,
                                                         'categories': context.get('categories'),
                                                         'users': context.get('users')})


class DeletePost(View):
    model = Post

    def get(self, request, post_id):
        post = self.model.objects.get(pk=post_id)
        post.delete()
        return redirect('django_admin:list_post_admin')


class CreatePost(View):
    model = Post
    form = PostForm
    template_name = 'blog_app/post/create_post.html'

    def get(self, request):
        form = PostForm()
        return self.render_context(form)

    def post(self, request):
        form = PostForm(request.POST)
        multiple = request.POST.get('multiple')
        if form.is_valid():
            post = form.save()
            if multiple and int(multiple) == True:
                return redirect('django_admin:create_post_admin')
            return redirect(post.get_admin_absolute_url())
        else:
            return self.render_context(form)

    def get_context(self):
        users = User.objects.all()
        categories = Category.objects.all()
        return {'users': users, 'categories': categories}

    def render_context(self, form):
        context = self.get_context()
        return render(self.request, self.template_name, {'form': form,
                                                         'categories': context.get('categories'),
                                                         'users': context.get('users')})

