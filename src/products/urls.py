from django.urls import path

from products.views import CatalogListView, basket_add, basket_remove

app_name = 'catalog'

urlpatterns = [
    path('', CatalogListView.as_view(), name='index'),
    path('category/<int:category_id>/', CatalogListView.as_view(), name='category'),
    path('page/<int:page>/', CatalogListView.as_view(), name='paginator'),
    path('category/<int:category_id>/page/<int:page>/', CatalogListView.as_view(), name='category_page'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
