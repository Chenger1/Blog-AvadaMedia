from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ExtendLoginRequiredMixin(LoginRequiredMixin):
    login_url = 'user_app:login_view'


class UserPermissionsRequiredMixin(PermissionRequiredMixin):
    permission_required = ('blog_app.add_post', 'blog_app.change_post', 'blog_app.delete_post',
                           'blog_app.view_post', 'blog_app.view_category', 'auth.view_user',
                           'blog_app.add_comment', 'blog_app.delete_comment',  'blog_app.view_comment',
                           'blog_app.change_comment')
