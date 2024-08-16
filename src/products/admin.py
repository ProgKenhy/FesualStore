from django.contrib import admin

from products.models import Basket, Product, ProductCategory, ProductImage

admin.site.register(ProductCategory)


class ProductImageInline(admin.TabularInline):
    fk_name = 'product'
    model = ProductImage
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ]
    list_display = ('name', 'price', 'category')
    fields = ('name', 'description', 'price', 'category', 'size', 'gender')
    search_fields = ('name', 'description')


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
