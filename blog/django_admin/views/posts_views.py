from django.shortcuts import render, redirect
from django.views.generic.list import View

from blog_app.models import Post, Category

from user_app.models import User

from django_admin.forms.blog_app.post import PostForm


class ListPosts(View):
    model = Post
    template_name = 'blog_app/post/list_posts.html'
    list_display = ['title', 'author', 'created_date', 'is_important', 'is_publish', 'category']

    def get(self, request):
        posts = self.model.objects.all()
        return render(request, self.template_name, {'posts': posts,
                                                    'list_display': self.list_display})


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
        if form.is_valid():
            post = form.save()
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
