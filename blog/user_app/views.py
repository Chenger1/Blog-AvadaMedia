from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View

from user_app.forms import LoginForm


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


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('blog_app:list_view')


class RegistrationView(View):
    pass