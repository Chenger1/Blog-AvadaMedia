from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.models import Group, Permission

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username',
                  'password1',
                  'password2',]

    def clean(self):
        username = self.cleaned_data['username']
        password_one = self.cleaned_data['password1']
        password_two = self.cleaned_data['password2']

        if User.objects.filter(username=username).exists():
            raise ValidationError({'username': 'There user already exists'})
        if password_one != password_two:
            raise ValidationError({'password1': 'Passwords don`t match'})
        validate_password(password_one)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UpdateUserInfoForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    extended_info = forms.CharField(widget=forms.Textarea)

    is_staff = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)

    def set_permissions(self, group_pk, permission_pk, user):
        groups = []
        permissions = []
        for group in group_pk:
            groups.append(Group.objects.get(pk=group))

        for perm in permission_pk:
            permissions.append(Permission.objects.get(pk=perm))

        user.user_permissions.clear()
        for perm in permissions:
            user.user_permissions.add(perm)

        user.groups.clear()
        for group in groups:
            user.groups.add(group)

        return user

    def save(self, user, commit=True):
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.extended_info = self.cleaned_data.get('extended_info', '')
        user.is_staff = bool(self.cleaned_data.get('is_staff'))
        user.is_superuser = bool(self.cleaned_data.get('is_superuser'))
        if commit:
            user.save()
        return user
