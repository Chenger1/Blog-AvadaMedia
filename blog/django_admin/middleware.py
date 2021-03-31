from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AdminCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user

        if 'django-admin' in request.path:
            if user.is_authenticated:
                if not user.is_staff or not user.is_superuser:
                    return redirect('blog_app:list_view')
            elif 'login/' not in request.path:
                return redirect('user_app:login_view')
        return self.get_response(request)
