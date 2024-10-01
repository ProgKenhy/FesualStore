import django_filters
from products.models import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Product
        fields = ['price', 'gender', 'size']

