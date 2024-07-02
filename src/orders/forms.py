from django import forms

from orders.models import Order
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import RegionalPhoneNumberWidget


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Иван'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Иванов'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'you@example.com'}))
    phone = PhoneNumberField(widget=RegionalPhoneNumberWidget(region='RU', attrs={
        'class': 'form-control', 'placeholder': '+7 912 345 67-89'
    }))

    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Россия, Москва, ул. Мира, дом 6'}))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']
