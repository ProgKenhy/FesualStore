from django.urls import path
from . import views

app_name = 'information'

urlpatterns = [
    path('delivery/', views.delivery, name='delivery'),
    # path('payment/', views.payment, name='payment'),
    path('contacts/', views.contacts, name='contacts'),
    path('team/', views.team, name='team'),
    # path('faq/', views.faq, name='faq'),
    path('company-history/', views.history, name='company-history'),
    # path('public-offer/', views.public_offer, name='public-offer'),
]
