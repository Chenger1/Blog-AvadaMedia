from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class PaginatorMixin:
    @staticmethod
    def get_page(objects, max_pages, current_page):
        paginator = Paginator(objects, max_pages)
        page = current_page

        try:
            objs = paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except EmptyPage:
            objs = paginator.page(paginator.num_pages)

        return objs
