from django import forms


class DiscountForm(forms.Form):
    discount = forms.DecimalField(
        label="Размер скидки (%)",
        min_value=0,
        max_value=100,
        decimal_places=2,
        initial=0,
        help_text="Введите значение от 0 до 100"
    )