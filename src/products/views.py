from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from products.filters import ProductFilter
from django.views.generic.detail import DetailView
from django.contrib import messages

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
    paginate_by = 15
    title = 'Каталог'

    def get_queryset(self):
        queryset = super(CatalogListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        queryset = queryset.order_by('-id')
        filter = ProductFilter(self.request.GET, queryset=queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super(CatalogListView, self).get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET, queryset=self.object_list)
        context['current_category_id'] = self.kwargs.get('category_id')
        return context


@login_required
def basket_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
        messages.success(request, 'Товар успешно добавлен в корзину!')
    else:
        messages.warning(request, 'Товар уже находится в вашей корзине.')

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = get_object_or_404(Basket, id=basket_id)
    basket.delete()
    messages.success(request, 'Товар успешно удален из корзины.')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавьте дополнительные данные в контекст при необходимости
        context['title'] = self.object.name
        return context
