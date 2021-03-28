from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from abc import ABC, abstractmethod

from user_app.forms import LoginForm, RegistrationForm, PersonalInfoForm

from common.mixins import ExtendLoginRequiredMixin


class UserLoginView(View):
    template_name = 'registration/login.html'
    form = LoginForm

    def get(self, request):
        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('blog_app:list_view')
            else:
                return render(request, self.template_name, {'form': form,
                                                            'error': 'Wrong username or password'})
        else:
            return render(request, self.template_name, {'form': form,
                                                        'error': 'Incorrect data'})


class LogoutView(ExtendLoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('blog_app:list_view')


class RegistrationView(View):
    template_name = 'registration/registration.html'
    form = RegistrationForm

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            login_user = authenticate(username=form.cleaned_data.get('username'),
                                      password=form.cleaned_data.get('password1'))
            if login_user:
                login(request, login_user)
            return redirect('blog_app:list_view')
        else:
            return render(request, self.template_name, {'form': form})


class UserProfileMixin(ABC, View):
    template_name = 'user/profile.html'
    current_page = {
        'posts': True,
        'saved': False
    }

    @abstractmethod
    def get(self, request, user, obj, current_page=None):
        paginator = Paginator(obj, 3)
        page = request.GET.get('page')
        try:
            obj = paginator.page(page)
        except PageNotAnInteger:
            obj = paginator.page(1)
        except EmptyPage:
            obj = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'user': user,
                                                    'objs': obj,
                                                    'page': page,
                                                    'current_page': current_page})


class UserProfilePosts(UserProfileMixin):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        obj = user.posts.filter(is_publish=True)
        return super().get(request, user, obj, current_page='publish_post')


class UserProfileSaved(UserProfileMixin):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        obj = user.posts.filter(is_publish=False)
        return super().get(request, user, obj, current_page='saved_post')


class UserProfileComment(UserProfileMixin):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        obj = user.comments.all()
        return super().get(request, user, obj, current_page='comments')


class UpdatePersonalInfo(ExtendLoginRequiredMixin, View):
    template_name = 'registration/update_info.html'
    form = PersonalInfoForm

    def get(self, request):
        user = User.objects.get(pk=request.user.pk)
        form = PersonalInfoForm(instance=user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PersonalInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_app:profile_view', user_id=request.user.pk)
        else:
            return render(request, self.template_name, {'form': form})


class ChangePassword(PasswordChangeView):
    template_name = 'registration/change_password_form.html'
    success_url = reverse_lazy('blog_app:list_view')
