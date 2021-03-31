from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model

from django_admin.forms.user_app.user import UserRegistrationForm, UpdateUserInfoForm

from common.paginator_mixin import PaginatorMixin

User = get_user_model()


class ListUsers(View):
    model = User
    template_name = 'user_app/user/list_users.html'
    list_display = ('username', 'email', 'first name', 'last name', 'staff status')

    def get(self, request, filter_name=None, filter_value=None):
        users = self.filter_results(filter_name, filter_value)
        page = request.GET.get('page')
        users = PaginatorMixin.get_page(users, 10, page)

        groups = Group.objects.all()
        return render(request, self.template_name, {'users': users,
                                                    'list_display': self.list_display,
                                                    'groups': groups,
                                                    'current_filter': filter_name,
                                                    'filter_value': filter_value,
                                                    'page': page})

    def filter_results(self, filter_name, filter_value):
        if filter_name == 'is_staff':
            users = self.model.objects.filter(is_staff=bool(filter_value))
        elif filter_name == 'is_superuser':
            users = self.model.objects.filter(is_superuser=bool(filter_value))
        elif filter_name == 'group':
            users = self.model.objects.filter(groups__pk=int(filter_value))
        else:
            users = self.model.objects.all()
        return users


class CreateUser(View):
    model = User
    form = UserRegistrationForm
    template_name = 'user_app/user/create_user.html'

    def get(self, request):
        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form(request.POST)
        multiple = int(request.POST.get('multiple'))
        if form.is_valid():
            user = form.save()
            if multiple:
                return redirect('django_admin:create_user_admin')
            return redirect(user.get_admin_absolute_url())
        else:
            return render(request, self.template_name, {'form': form})


class UserProfilePosts(View):
    model = User
    template_name = 'user_app/user/profile/profile.html'

    def get(self, request, user_id):
        user = self.model.objects.get(pk=user_id)
        posts = user.posts.filter(is_publish=True)
        page = request.GET.get('page')
        posts = PaginatorMixin.get_page(posts, 3, page)

        return render(request, self.template_name, {'user': user,
                                                    'posts': posts,
                                                    'current': 'posts',
                                                    'page': page})


class UserProfileSaved(View):
    model = User
    template_name = 'user_app/user/profile/profile.html'

    def get(self, request, user_id):
        user = self.model.objects.get(pk=user_id)
        saved_posts = user.posts.filter(is_publish=False)
        page = request.GET.get('page')
        saved_posts = PaginatorMixin.get_page(saved_posts, 3, page)

        return render(request, self.template_name, {'user': user,
                                                    'saved_posts': saved_posts,
                                                    'current': 'saved_posts',
                                                    'page': page})


class UserProfileComment(View):
    model = User
    template_name = 'user_app/user/profile/profile.html'

    def get(self, request, user_id):
        user = self.model.objects.get(pk=user_id)
        comments = user.comments.all()
        page = request.GET.get('page')
        comments = PaginatorMixin.get_page(comments, 3, page)

        return render(request, self.template_name, {'user': user,
                                                    'comments': comments,
                                                    'page': page,
                                                    'current': 'comments'})


class UserProfileSettings(View):
    model = User
    form = UpdateUserInfoForm
    template_name = 'user_app/user/profile/profile.html'

    def get(self, request, user_id):
        user = self.model.objects.get(pk=user_id)
        form = UpdateUserInfoForm()

        return self._render_context(user, form)

    def post(self, request, user_id):
        user = self.model.objects.get(pk=user_id)
        form = UpdateUserInfoForm(request.POST)
        if form.is_valid():
            user = form.save(user, commit=False)
            group_pk = request.POST.getlist('groups')
            permissions_pk = request.POST.getlist('permissions')
            user = form.set_permissions(group_pk, permissions_pk, user)
            user.save()

            return redirect(user.get_admin_absolute_url())
        else:
            return self._render_context(user, form)

    def _get_context(self, user, form):
        user_groups = user.groups.all()
        groups = [group for group in Group.objects.all() if group not in user_groups]

        user_permissions = user.user_permissions.all()
        permissions = [perm for perm in Permission.objects.all() if perm not in user_permissions]

        return {'user': user,
                'settings': True,
                'groups': groups,
                'user_groups': user_groups,
                'user_permissions': user_permissions,
                'permissions': permissions,
                'form': form}

    def _render_context(self, user, form):
        context = self._get_context(user, form)

        return render(self.request, self.template_name, context)


class DeleteUser(View):
    model = User

    def get(self, request, user_id):
        user = self.model.objects.get(pk=user_id)
        user.delete()
        return redirect('django_admin:list_users_admin')
