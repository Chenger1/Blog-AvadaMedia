from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from blog_app.models import Post, Category, Comment

from blog_app.forms import CreatePostForm, CreateCommentForm

from common.mixins import ExtendLoginRequiredMixin, UserPermissionsRequiredMixin


class ListPosts(View):
    model = Post
    template_name = 'post/list_post.html'

    def get(self, request, category_id=None, year=None):
        if category_id:
            posts = self.model.objects.filter(category=category_id, is_publish=True)
        else:
            posts = self.model.objects.filter(is_publish=True)
        if year:
            posts = posts.filter(published_date__year=year)

        paginator = Paginator(posts, 5)
        page = request.GET.get('page')

        important_posts = posts.filter(is_important=True).order_by('published_date').reverse()[:3]

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        categories = Category.objects.all()

        return render(request, self.template_name, {'posts': posts,
                                                    'important_posts': important_posts,
                                                    'categories': categories,
                                                    'current_category': category_id,
                                                    'page': page})


class EditPost(ExtendLoginRequiredMixin, UserPermissionsRequiredMixin, View):
    form = CreatePostForm
    template_name = 'post/create_post.html'

    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        form = self.form(instance=post)
        categories = Category.objects.all()
        return render(request, self.template_name, {'form': form,
                                                    'categories': categories})

    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        form = self.form(data=request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if request.POST.get('is_important'):
                post.is_important = True
            else:
                post.is_important = False
            post.save()
            return redirect(post.get_absolute_url())
        else:
            categories = Category.objects.all()
            return render(request, self.template_name, {'form': form, 'categories': categories})


class CreatePost(ExtendLoginRequiredMixin, UserPermissionsRequiredMixin, View):
    form = CreatePostForm
    template_name = 'post/create_post.html'

    def get(self, request):
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories})

    def post(self, request):
        form = self.form(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if request.POST.get('is_important'):
                post.is_important = True
            else:
                post.is_important = False
            post.save()
            return redirect(post.get_absolute_url())
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


class DeletePost(ExtendLoginRequiredMixin, UserPermissionsRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog_app:list_view')


class ChangeImportanceView(ExtendLoginRequiredMixin, View):
    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        post.is_important = not post.is_important
        post.save()
        return redirect(post.get_absolute_url())


class CreateComment(ExtendLoginRequiredMixin, UserPermissionsRequiredMixin, View):
    model = Comment
    form = CreateCommentForm

    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        form = self.form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
        return redirect(post.get_absolute_url())


class DeleteComment(ExtendLoginRequiredMixin, UserPermissionsRequiredMixin, View):
    model = Comment

    def post(self, request, comment_id):
        comment = self.model.objects.get(pk=comment_id)
        post = comment.post
        comment.delete()
        return redirect(post.get_absolute_url())


class EditComment(ExtendLoginRequiredMixin, UserPermissionsRequiredMixin, View):
    model = Comment
    form = CreateCommentForm

    def post(self, request, comment_id):
        comment = self.model.objects.get(pk=comment_id)
        form = CreateCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
        return redirect(comment.post.get_absolute_url())
