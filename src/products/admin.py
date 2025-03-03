from django import forms
from django.contrib import admin

from products.models import Basket, Product, ProductCategory, ProductImage

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
    # Кастомное поле для загрузки нескольких изображений
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
    inlines = [ProductImageInline, ]
    list_display = ('name', 'price', 'category')
    fields = ('name', 'description', 'price', 'category', 'size', 'gender', 'images')
    search_fields = ('name', 'description')

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        product = form.instance
        # Обрабатываем каждое загруженное изображение
        for image in request.FILES.getlist('images'):
            ProductImage.objects.create(product=product, image=image)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
