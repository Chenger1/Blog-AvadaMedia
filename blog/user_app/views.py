from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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
                                                            'error': 'Неправильный логин или пароль'})
        else:
            return render(request, self.template_name, {'form': form,
                                                        'error': 'Введены некорректные данные'})


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


class UserProfile(ExtendLoginRequiredMixin, View):
    template_name = 'user/profile.html'

    def get(self, request, user_id, is_publish=True):
        user = User.objects.get(pk=user_id)
        posts = user.posts.filter(is_publish=is_publish)
        paginator = Paginator(posts, 3)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'user': user,
                                                    'posts': posts,
                                                    'page': page,
                                                    'is_publish': is_publish})


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
