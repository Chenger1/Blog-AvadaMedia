from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, Permission
from django.views.generic import View

from common.paginator_mixin import PaginatorMixin

from django_admin.forms.user_app.group import GroupForm


class ListGroups(View):
    model = Group
    template_name = 'user_app/group/list_groups.html'
    list_display = ('name', 'option')

    def get(self, request, group_id=None):
        groups = Group.objects.all()
        page = request.GET.get('page')
        groups = PaginatorMixin.get_page(groups, 10, page)
        group = None
        group_permissions = None

        permissions = Permission.objects.all()

        if group_id:
            group = self.model.objects.get(pk=group_id)
            group_permissions = group.permissions.all()
            permissions = [perm for perm in permissions if perm not in group_permissions]

        return render(request, self.template_name, {'groups': groups,
                                                    'list_display': self.list_display,
                                                    'page': page,
                                                    'group': group,
                                                    'group_permissions': group_permissions,
                                                    'permissions': permissions})


class EditGroup(View):
    model = Group
    form = GroupForm

    def post(self, request, group_id=None):
        form = self.form(request.POST)
        group = None
        permissions_pk = request.POST.getlist('permissions')

        if group_id:
            group = self.model.objects.get(pk=group_id)

        if form.is_valid():
            group = form.save(group, commit=False)
            group = form.set_permissions(group, permissions_pk)
            group.save()
            return redirect('django_admin:list_groups_admin')


class DeleteGroup(View):
    model = Group

    def get(self, request, group_id):
        group = self.model.objects.get(pk=group_id)
        group.delete()
        return redirect('django_admin:list_groups_admin')
