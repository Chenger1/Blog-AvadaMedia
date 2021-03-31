from django import forms
from django.contrib.auth.models import Group, Permission


class GroupForm(forms.Form):
    name = forms.CharField()

    def set_permissions(self, group, permissions_pk):
        permissions = []
        for perm in permissions_pk:
            permissions.append(Permission.objects.get(pk=perm))

        group.permissions.clear()
        for perm in permissions:
            group.permissions.add(perm)

        return group

    def save(self, group=None, commit=True):
        if group:
            group.name = self.cleaned_data['name']
        else:
            group = Group.objects.create(name=self.cleaned_data['name'])

        if commit:
            group.save()
        return group
