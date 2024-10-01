from django.urls import path

from orders.views import OrderCreateView

app_name = 'order'

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
]
