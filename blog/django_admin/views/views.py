from django.shortcuts import redirect
from django.views.generic import View


class DisplayAdminPage(View):
    template_name = 'admin_base.html'

    def get(self, request):
        return redirect('django_admin:list_post_admin')
