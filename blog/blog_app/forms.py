from django import forms

from blog_app.models import Post, Comment


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'category', 'is_publish')


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

