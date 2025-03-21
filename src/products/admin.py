from django import forms
from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render

from products.models import Basket, Product, ProductCategory, ProductImage
from products.forms import DiscountForm

admin.site.register(ProductCategory)


class ProductImageInline(admin.TabularInline):
    fk_name = 'product'
    model = ProductImage
    extra = 0


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductAdminForm(forms.ModelForm):
    images = MultipleFileField(
        required=False,
        label='Добавить несколько изображений'
    )

    class Meta:
        model = Product
        fields = '__all__'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    actions = ['set_discount']

    inlines = [ProductImageInline, ]
    list_display = ('name', 'price', 'discount', 'category', 'reservation')
    fields = ('name', 'description', 'price', 'discount', 'reservation', 'category', 'size', 'gender', 'images')
    search_fields = ('name', 'description', 'reservation')

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        product = form.instance
        # Обрабатываем каждое загруженное изображение
        for image in request.FILES.getlist('images'):
            ProductImage.objects.create(product=product, image=image)

    @admin.action(description="Установить скидку")
    def set_discount(self, request, queryset):
        if 'apply' in request.POST:
            form = DiscountForm(request.POST)
            if form.is_valid():
                discount = form.cleaned_data['discount']

                # Добавим отладочную информацию
                self.message_user(
                    request,
                    f"Пытаемся обновить {queryset.count()} товаров со скидкой {discount}%",
                    messages.INFO
                )

                # Проверим, что queryset не пустой
                if queryset.exists():
                    # Сохраним ID товаров для проверки
                    product_ids = list(queryset.values_list('id', flat=True))

                    # Применяем скидку к выбранным товарам
                    updated = queryset.update(discount=discount)

                    # Проверим, что обновление действительно произошло
                    products_after = Product.objects.filter(id__in=product_ids)
                    successful = all(p.discount == discount for p in products_after)

                    if successful:
                        self.message_user(
                            request,
                            f"Скидка {discount}% успешно установлена для {updated} товаров.",
                            messages.SUCCESS
                        )
                    else:
                        self.message_user(
                            request,
                            "Скидка не была применена ко всем товарам. Проверьте модель Product.",
                            messages.ERROR
                        )
                else:
                    self.message_user(
                        request,
                        "Не выбрано товаров для обновления.",
                        messages.WARNING
                    )

                return  # Завершаем выполнение после обновления

        # Если форма не была отправлена или данные невалидны, показываем форму
        form = DiscountForm(initial={'discount': 0})

        return render(
            request,
            'admin/set_discount.html',  # Шаблон для отображения формы
            context={
                'products': queryset,
                'form': form,
                'title': 'Установить скидку для выбранных товаров',
            }
        )


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
