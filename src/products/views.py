from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from products.filters import ProductFilter


from common.views import CommonMixin
from products.models import Basket, Product


class IndexView(CommonMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Fesual Store'

    def get_context_data(self, objects_list=None, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['new_items'] = Product.objects.all().order_by('-id')[:4]  # order_by("-pub_date",
        return context


class CatalogListView(CommonMixin, ListView):
    model = Product
    template_name = 'products/catalog.html'
    paginate_by = 9
    title = 'Каталог'

    def get_queryset(self):
        queryset = super(CatalogListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CatalogListView, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        filter = ProductFilter(self.request.GET, queryset=queryset)
        context['filter'] = filter
        context['object_list'] = filter.qs
        context['current_category_id'] = self.kwargs.get('category_id')
        return context


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
