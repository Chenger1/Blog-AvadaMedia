from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'password1',
                  'password2',
                  'first_name',
                  'last_name']

    def clean(self):
        username = self.cleaned_data['username']
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if User.objects.filter(username=username).exists():
            raise ValidationError({'username': 'There user already exists'})
        if password1 != password2:
            raise ValidationError({'password1': 'Passwords don`t match'})
        validate_password(password1)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        group = Group.objects.get_or_create(name='DefaultUser')[0]
        user.groups.add(group)
        return user


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
