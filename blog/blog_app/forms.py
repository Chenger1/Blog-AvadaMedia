from django import forms
from django.core.exceptions import ValidationError

from blog_app.models import Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'category', 'is_publish')
