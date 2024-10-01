from products.models import ProductCategory, Basket, ProductImage, Product
from django.core.cache import cache


def categories(request):
    return {'categories': cache.get_or_set('categories', ProductCategory.objects.all(), 30)}


def baskets(request):
    user = request.user
    return {'baskets': Basket.objects.filter(user=user) if user.is_authenticated else []}
