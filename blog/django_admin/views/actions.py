from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth.models import Group

from blog_app.models import Post, Category
from user_app.models import User


class ActionsView(View):
    models = {
        'Post': Post,
        'Category': Category,
        'User': User,
        'Group': Group
    }
    urls = {
        'Post': 'django_admin:list_post_admin',
        'Category': 'django_admin:list_category_admin',
        'User': 'django_admin:list_users_admin',
        'Group': 'django_admin:list_groups_admin',
    }
    model = None

    def post(self, request, model_name):
        action_type = request.POST.get('action')
        self.model = self.models[model_name]
        if action_type == 'delete_selected':
            self._delete_selected(request.POST.getlist('_selected_action'))

        return redirect(self.urls[model_name])

    def _delete_selected(self, query):
        for instance in query:
            inst = self.model.objects.get(pk=int(instance))
            inst.delete()
