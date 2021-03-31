from django.shortcuts import render
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.views.generic import View

from blog_app.forms import SearchForm
from blog_app.models import Post, Category
from user_app.models import User

search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')


class SearchView(View):
    form = SearchForm
    template_name = 'admin_search.html'
    vectors = {'Post': SearchVector('title', weight='A') + SearchVector('body', weight='B'),
               'Category': SearchVector('name', weight='A'),
               'User': SearchVector('username', weight='A')+SearchVector('last_name', weight='B')}
    models = [Post, Category, User]

    def get(self, request):
        if 'query' in request.GET:
            form = self.form(request.GET)
            if form.is_valid():
                query = form.cleaned_data.get('query')
                posts = Post.objects.filter(is_publish=True)
                post_vector = self.vectors['Post']
                post_results = self.search(posts, query, post_vector)

                categories = Category.objects.all()
                category_vector = self.vectors['Category']
                category_results = self.search(categories, query, category_vector)

                users = User.objects.all()
                user_vector = self.vectors['User']
                user_results = self.search(users, query, user_vector)

                return render(request, self.template_name, {'form': form,
                                                            'posts': post_results,
                                                            'categories': category_results,
                                                            'users': user_results})
            else:
                form = self.form()
                return render(request, self.template_name, {'form': form})
        else:
            form = self.form()
            return render(request, self.template_name, {'form': form})

    def search(self, obj, query, search_vector):
        search_query = SearchQuery(query)
        results = obj.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by('-rank')
        return results
