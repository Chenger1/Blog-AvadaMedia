from django.shortcuts import render, redirect
from django.views.generic import View

from blog_app.models import Category

from django_admin.forms.blog_app.category import CategoryForm

from common.paginator_mixin import PaginatorMixin


class ListCategory(View):
    model = Category
    template_name = 'blog_app/category/list_category.html'
    list_display = ['name', 'option']
    form = CategoryForm

    def get(self, request, category_id=None):
        form = CategoryForm()
        if category_id:
            category = Category.objects.get(pk=category_id)
            form = self.form(instance=category)

        categories = Category.objects.all()
        page = request.GET.get('page')
        categories = PaginatorMixin.get_page(categories, 10, page)

        return render(request, self.template_name, {'categories': categories,
                                                    'list_display': self.list_display,
                                                    'page': page,
                                                    'form': form})


class EditCategory(View):
    model = Category
    form = CategoryForm

    def post(self, request, category_id=None):
        if category_id:
            category = self.model.objects.get(pk=category_id)
            form = self.form(request.POST, instance=category)
        else:
            form = self.form(request.POST)
        multiple = int(request.POST.get('multiple'))

        if form.is_valid():
            category = form.save()
            if multiple:
                return redirect('django_admin:list_category_admin')
            else:
                return redirect(category.get_admin_absolute_url())
        else:
            return redirect('django_admin:list_category_admin')


class DeleteCategory(View):
    model = Category

    def get(self, request, category_id):
        category = self.model.objects.get(pk=category_id)
        category.delete()
        return redirect('django_admin:list_category_admin')
