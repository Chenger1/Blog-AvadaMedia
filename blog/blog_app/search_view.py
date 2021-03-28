from django.shortcuts import render
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.views.generic import View

from blog_app.forms import SearchForm
from blog_app.models import Post


class SearchView(View):
    form = SearchForm
    template_name = 'search.html'

    def get(self, request):
        if 'query' in request.GET:
            form = self.form(request.GET)
            if form.is_valid():
                query = form.cleaned_data.get('query')
                search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
                search_query = SearchQuery(query)
                posts = Post.objects.filter(is_publish=True)
                results = posts.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by(
                                                                                                                '-rank')
                return render(request, self.template_name, {'form': form,
                                                            'posts': results})
            else:
                form = self.form()
                return render(request, self.template_name, {'form': form})
        else:
            form = self.form()
            return render(request, self.template_name, {'form': form})
