from django.test import TestCase

from blog_app.models import Category, Post
from django.contrib.auth.models import User


class TestCategory(TestCase):
    def test_creating(self):
        temp = Category.objects.create(name='Category-1')
        temp.save()
        category = Category.objects.get(name='Category-1')
        self.assertEqual(temp.name, category.name)


class TestPost(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Category-1')
        cls.category.save()

        cls.user = User(username='User-1', password='pass')
        cls.user.save()

    def test_creating(self):
        temp = Post.objects.create(title='Title-1', body='Body-1',
                                   author=self.user, category=self.category)
        temp.save()
        post = Post.objects.get(title='Title-1')
        self.assertEqual(post.title, temp.title)
